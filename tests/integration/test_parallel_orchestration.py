import asyncio
import json
import time

import council_of_translation.localization.orchestration as orchestration
from council_of_translation.localization.models import ReviewTaskV2
from council_of_translation.localization.orchestration import run_structured_review
from council_of_translation.localization.persistence import ReviewStore
from council_of_translation.localization.runtime import (
    ElicitationResult,
    InteractionCapabilities,
    ModelExecutionResult,
    RuntimeEvent,
    RuntimeTelemetry,
    ScriptedModelExecutor,
    ScriptedUserInteractionGateway,
)


class RoleDelayedExecutor:
    def __init__(self, roles, *, fail_role="", context_gap=False):
        self.roles = roles
        self.fail_role = fail_role
        self.context_gap = context_gap
        self.telemetry = RuntimeTelemetry(sample_budget=13)
        self.active = 0
        self.peak = 0
        self.calls = {role: 0 for role in roles}
        self.completed = []

    async def sample(self, prompt, *, temperature=0.2, max_tokens=1_400):
        del temperature, max_tokens
        role = next(role for role in self.roles if f'"id":"{role}"' in prompt)
        self.calls[role] += 1
        self.active += 1
        self.peak = max(self.peak, self.active)
        try:
            index = self.roles.index(role)
            await asyncio.sleep(0.006 * (len(self.roles) - index))
            if role == self.fail_role:
                raise RuntimeError("isolated role failure")
            payload = {"role_feedback": f"{role} completed", "findings": []}
            if self.context_gap and index == 0:
                payload["context_gaps"] = [{
                    "question": "该文案是品牌标语还是功能按钮？",
                    "materiality": "用途会改变角色路由与建议选项",
                    "affected_role_ids": [role],
                }]
            self.completed.append(role)
            result = ModelExecutionResult(status="success", text=json.dumps(payload, ensure_ascii=False))
        finally:
            self.active -= 1
        self.telemetry.record(RuntimeEvent("sampling", result.status, 6))
        return result


class PhaseGateway:
    def __init__(self, executor):
        self.executor = executor
        self.telemetry = executor.telemetry
        self.requests = []

    def capabilities(self):
        return InteractionCapabilities(form_elicitation=True)

    async def elicit(self, message, *, response_type):
        assert self.executor.active == 0
        assert all(self.executor.calls.values())
        self.requests.append((message, response_type))
        self.telemetry.record(RuntimeEvent("elicitation", "decline"))
        return ElicitationResult(action="decline")


def run_review(tmp_path, monkeypatch, *, limit="3", fail_role="", context_gap=False):
    monkeypatch.setenv("COUNCIL_REVIEW_CONCURRENCY", limit)
    roles = [
        "fidelity_reviewer", "terminology_reviewer", "product_context_reviewer",
        "brand_voice_reviewer", "risk_ambiguity_reviewer", "fluency_reviewer",
    ]
    executor = RoleDelayedExecutor(roles, fail_role=fail_role, context_gap=context_gap)
    gateway = PhaseGateway(executor)
    record = asyncio.run(run_structured_review(
        ReviewTaskV2(
            source_text="Bigger", candidate_translation="更大", content_type="marketing",
            audience="官网访客", context="品牌活动页面", briefing_mode="off",
            interactive_mode="auto", mode="standard",
        ),
        executor,
        gateway,
        store=ReviewStore(tmp_path, include_legacy=False),
    ))
    return record, executor, gateway, roles


def test_parallel_core_is_exact_once_reversed_completion_and_plan_order(tmp_path, monkeypatch):
    record, executor, _, roles = run_review(tmp_path, monkeypatch)
    assert executor.peak == 3
    assert executor.completed != roles
    assert executor.calls == {role: 1 for role in roles}
    assert [item["agent_name"] for item in record.independent_reviews] == roles
    assert record.runtime_metadata.sampling_calls == 6
    assert record.runtime_metadata.reviewer_coverage == "full"
    assert record.runtime_metadata.wall_clock_ms > 0
    assert record.runtime_metadata.sampling_wait_ms >= 36
    assert record.runtime_metadata.independent_review_concurrency_limit == 3
    assert record.runtime_metadata.independent_review_peak_concurrency == 3
    assert record.runtime_metadata.independent_review_batch_count == 2
    assert record.runtime_metadata.independent_review_concurrency_disposition == "configured"


def test_normal_review_wall_clock_includes_late_display_finalization(tmp_path, monkeypatch):
    monkeypatch.setenv("COUNCIL_REVIEW_CONCURRENCY", "3")
    original_render = orchestration.render_display_report

    def delayed_render(*args, **kwargs):
        time.sleep(0.025)
        return original_render(*args, **kwargs)

    monkeypatch.setattr(orchestration, "render_display_report", delayed_render)
    telemetry = RuntimeTelemetry(sample_budget=13)
    clean = json.dumps({"role_feedback": "clean review", "findings": []})
    store = ReviewStore(tmp_path / "late-normal", include_legacy=False)
    record = asyncio.run(run_structured_review(
        ReviewTaskV2(
            source_text="Save", candidate_translation="保存", content_type="ui",
            briefing_mode="off", interactive_mode="off",
        ),
        ScriptedModelExecutor([clean] * 6, telemetry),
        ScriptedUserInteractionGateway([], telemetry=telemetry),
        store=store,
    ))

    assert 20 <= record.runtime_metadata.wall_clock_ms < 2_000
    assert record.runtime_metadata.elapsed_ms >= record.runtime_metadata.sampling_wait_ms
    assert store.load(record.review_id).runtime_metadata.wall_clock_ms == record.runtime_metadata.wall_clock_ms


def test_sequential_override_preserves_order_without_overlap(tmp_path, monkeypatch):
    record, executor, _, roles = run_review(tmp_path, monkeypatch, limit="1")
    assert executor.peak == 1
    assert executor.completed == roles
    assert [item["agent_name"] for item in record.independent_reviews] == roles
    assert executor.calls == {role: 1 for role in roles}
    assert record.runtime_metadata.independent_review_concurrency_limit == 1
    assert record.runtime_metadata.independent_review_peak_concurrency == 1
    assert record.runtime_metadata.independent_review_batch_count == 6


def test_invalid_configuration_falls_back_to_visible_sequential_mode(tmp_path, monkeypatch):
    record, executor, _, roles = run_review(tmp_path, monkeypatch, limit="invalid")
    assert executor.peak == 1
    assert executor.calls == {role: 1 for role in roles}
    assert record.runtime_metadata.independent_review_concurrency_limit == 1
    assert record.runtime_metadata.independent_review_peak_concurrency == 1
    assert record.runtime_metadata.independent_review_batch_count == 6
    assert record.runtime_metadata.independent_review_concurrency_disposition == "invalid_fallback"
    assert record.runtime_metadata.fallbacks == ["review_concurrency_invalid"]


def test_role_exception_is_partial_coverage_without_replay(tmp_path, monkeypatch):
    failed = "product_context_reviewer"
    record, executor, _, roles = run_review(tmp_path, monkeypatch, fail_role=failed)
    assert executor.calls == {role: 1 for role in roles}
    by_role = {item["agent_name"]: item for item in record.independent_reviews}
    assert by_role[failed]["sample_status"] == "unavailable"
    assert all(by_role[role]["sample_status"] == "structured_success" for role in roles if role != failed)
    assert record.runtime_metadata.sampling_calls == 6
    assert record.runtime_metadata.reviewer_coverage == "partial"
    assert record.status == "NEEDS_HUMAN_REVIEW"


def test_context_interaction_waits_until_independent_batch_settles(tmp_path, monkeypatch):
    record, executor, gateway, _ = run_review(
        tmp_path, monkeypatch, context_gap=True
    )
    assert executor.peak == 3
    assert len(gateway.requests) == 1
    assert record.context_gap_interaction.action == "decline"
    assert record.runtime_metadata.outcome_elicitation_calls == 0
    assert record.status == "NEEDS_HUMAN_REVIEW"
