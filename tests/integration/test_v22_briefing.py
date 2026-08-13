import asyncio
import time

import pytest

import council_of_translation.localization.orchestration as orchestration
from council_of_translation.localization.guided import context_is_sufficient
from council_of_translation.localization.models import ReviewTaskV2
from council_of_translation.localization.orchestration import run_structured_review
from council_of_translation.localization.persistence import ReviewStore
from council_of_translation.localization.roles import build_council_plan, normalize_content_type
from council_of_translation.localization.runtime import (
    ElicitationResult,
    RuntimeTelemetry,
    ScriptedModelExecutor,
    ScriptedUserInteractionGateway,
)


CLEAN = '{"role_feedback":"该角色未发现职责范围内的实质问题。","findings":[]}'
BRIEF_ANSWERS = {
    "domain": "协作软件",
    "content_type": "界面文案",
    "audience": "首次使用的普通用户",
    "tone_goal": "清晰并促成下一步操作",
    "primary_focus": "按钮是否准确可执行",
    "usage_context": "设置页主按钮",
}


def _executor(task: ReviewTaskV2) -> ScriptedModelExecutor:
    calls = len(build_council_plan(task.mode, task.content_type).active_role_ids)
    return ScriptedModelExecutor([CLEAN] * calls, RuntimeTelemetry(sample_budget=18))


def test_auto_context_sufficiency_requires_recognized_content_and_two_categories():
    def task(**values):
        return ReviewTaskV2(source_text="Save", candidate_translation="保存", **values)

    cases = {
        "recognized_plus_two": task(
            content_type="ui", context="设置页按钮", audience="普通用户"
        ),
        "alias_plus_two": task(
            content_type="UI button",
            reference_translations="Save=保存",
            brand_guidelines="简洁",
        ),
        "recognized_plus_one": task(content_type="ui", audience="普通用户"),
        "unknown_plus_two": task(
            content_type="mystery surface", context="设置页按钮", audience="普通用户"
        ),
        "unknown_plus_three": task(
            content_type="mystery surface",
            context="设置页按钮",
            audience="普通用户",
            style_guide="简洁",
        ),
        "unknown_plus_all_four": task(
            content_type="unspecified",
            context="设置页按钮",
            audience="普通用户",
            style_guide="简洁",
            term_glossary="Save=保存",
        ),
        "source_target_only": task(),
    }
    assert {name: context_is_sufficient(value) for name, value in cases.items()} == {
        "recognized_plus_two": True,
        "alias_plus_two": True,
        "recognized_plus_one": False,
        "unknown_plus_two": False,
        "unknown_plus_three": False,
        "unknown_plus_all_four": False,
        "source_target_only": False,
    }
    assert context_is_sufficient(
        task(
            content_type="ui",
            known_exceptions="已获准例外",
            notes="内部备注",
            hard_constraints=["numeric_parity"],
            do_not_translate_literals=["Save"],
        )
    ) is False


def test_unspecified_content_with_all_four_categories_still_requests_auto_briefing(tmp_path):
    task = ReviewTaskV2(
        source_text="Save",
        candidate_translation="保存",
        content_type="unspecified",
        context="设置页按钮",
        audience="普通用户",
        style_guide="简洁",
        term_glossary="Save=保存",
    )
    executor = _executor(task)
    gateway = ScriptedUserInteractionGateway(
        [ElicitationResult(
            action="accept",
            data={
                "content_type": "界面文案",
                "primary_focus": "按钮是否准确可执行",
            },
        )],
        telemetry=executor.telemetry,
    )

    record = asyncio.run(run_structured_review(
        task, executor, gateway, store=ReviewStore(tmp_path, include_legacy=False)
    ))

    assert len(gateway.requests) == 1
    assert record.briefing_interaction.action == "accept"
    assert record.runtime_metadata.briefing_elicitation_calls == 1


def test_source_target_only_auto_briefing_happens_before_first_sample(tmp_path):
    events: list[str] = []

    class OrderedExecutor(ScriptedModelExecutor):
        async def sample(self, *args, **kwargs):
            events.append("sample")
            return await super().sample(*args, **kwargs)

    class OrderedGateway(ScriptedUserInteractionGateway):
        async def elicit(self, *args, **kwargs):
            events.append("briefing")
            return await super().elicit(*args, **kwargs)

    task = ReviewTaskV2(source_text="Save", candidate_translation="保存")
    executor = OrderedExecutor([CLEAN] * 6, RuntimeTelemetry(sample_budget=18))
    gateway = OrderedGateway(
        [ElicitationResult(action="accept", data=BRIEF_ANSWERS)], telemetry=executor.telemetry
    )
    record = asyncio.run(run_structured_review(
        task, executor, gateway, store=ReviewStore(tmp_path, include_legacy=False)
    ))

    assert events[0] == "briefing" and events[1] == "sample"
    assert len(gateway.requests) == 1
    assert record.briefing_interaction.action == "accept"
    assert record.effective_brief.content_type == record.council_plan.content_type == "ui"
    assert record.effective_brief.audience == "首次使用的普通用户"
    assert record.effective_brief.field_provenance["audience"] == "user_briefing"
    assert all("EFFECTIVE_BRIEF" in prompt and "首次使用的普通用户" in prompt for prompt in executor.prompts)


def test_rich_auto_skips_but_always_and_off_are_explicit(tmp_path):
    rich = ReviewTaskV2(
        source_text="Save", candidate_translation="保存", content_type="ui",
        context="设置页主按钮", audience="普通用户", style_guide="简洁",
    )
    auto_gateway = ScriptedUserInteractionGateway([])
    auto = asyncio.run(run_structured_review(
        rich, _executor(rich), auto_gateway, store=ReviewStore(tmp_path / "auto", include_legacy=False)
    ))
    assert auto.briefing_interaction.action == "skipped"
    assert auto_gateway.requests == []

    always = rich.model_copy(update={"briefing_mode": "always"})
    always_executor = _executor(always)
    always_gateway = ScriptedUserInteractionGateway(
        [ElicitationResult(action="accept", data=BRIEF_ANSWERS)], telemetry=always_executor.telemetry
    )
    accepted = asyncio.run(run_structured_review(
        always, always_executor, always_gateway,
        store=ReviewStore(tmp_path / "always", include_legacy=False),
    ))
    assert accepted.briefing_interaction.action == "accept"
    assert len(always_gateway.requests) == 1

    off = ReviewTaskV2(source_text="Save", candidate_translation="保存", briefing_mode="off")
    off_gateway = ScriptedUserInteractionGateway([])
    skipped = asyncio.run(run_structured_review(
        off, _executor(off), off_gateway, store=ReviewStore(tmp_path / "off", include_legacy=False)
    ))
    assert skipped.briefing_interaction == skipped.briefing_interaction.model_copy(update={})
    assert skipped.briefing_interaction.action == "skipped" and off_gateway.requests == []


@pytest.mark.parametrize(
    ("result", "expected"),
    [
        (ElicitationResult(action="decline"), "decline"),
        (ElicitationResult(action="cancel"), "cancel"),
        (ElicitationResult(action="unsupported"), "unsupported"),
        (ElicitationResult(action="malformed"), "malformed"),
        (ElicitationResult(action="accept", data={"content_type": "bad"}), "malformed"),
    ],
)
def test_always_nonaccept_matrix_stops_before_sampling(tmp_path, result, expected):
    task = ReviewTaskV2(
        source_text="Save", candidate_translation="保存", briefing_mode="always"
    )
    telemetry = RuntimeTelemetry(sample_budget=18)
    executor = ScriptedModelExecutor([CLEAN] * 6, telemetry)
    gateway = ScriptedUserInteractionGateway([result], telemetry=telemetry)
    record = asyncio.run(run_structured_review(
        task, executor, gateway, store=ReviewStore(tmp_path / expected, include_legacy=False)
    ))
    assert record.status == "RETURNED_PENDING"
    assert record.briefing_interaction.action == expected
    assert record.runtime_metadata.sampling_calls == 0
    assert executor.prompts == []
    assert record.briefing_interaction.accepted_answers == {}
    assert record.chief_editor_decision.review_needed == "是"


def test_required_briefing_wall_clock_includes_late_display_finalization(tmp_path, monkeypatch):
    original_render = orchestration.render_display_report

    def delayed_render(*args, **kwargs):
        time.sleep(0.025)
        return original_render(*args, **kwargs)

    monkeypatch.setattr(orchestration, "render_display_report", delayed_render)
    task = ReviewTaskV2(
        source_text="Save", candidate_translation="保存", briefing_mode="always"
    )
    telemetry = RuntimeTelemetry(sample_budget=18)
    store = ReviewStore(tmp_path / "late-briefing", include_legacy=False)
    record = asyncio.run(run_structured_review(
        task,
        ScriptedModelExecutor([CLEAN] * 6, telemetry),
        ScriptedUserInteractionGateway(
            [ElicitationResult(action="decline")], telemetry=telemetry
        ),
        store=store,
    ))

    assert record.status == "RETURNED_PENDING"
    assert record.runtime_metadata.sampling_calls == 0
    assert 20 <= record.runtime_metadata.wall_clock_ms < 2_000
    assert store.load(record.review_id).runtime_metadata.wall_clock_ms == record.runtime_metadata.wall_clock_ms


def test_auto_decline_continues_with_truthful_assumptions_and_rules(tmp_path):
    task = ReviewTaskV2(
        source_text="Save {count}", candidate_translation="保存 {count}",
        hard_constraints=["required_literal:{count}"],
    )
    telemetry = RuntimeTelemetry(sample_budget=18)
    executor = ScriptedModelExecutor([CLEAN] * 6, telemetry)
    gateway = ScriptedUserInteractionGateway(
        [ElicitationResult(action="decline")], telemetry=telemetry
    )
    record = asyncio.run(run_structured_review(
        task, executor, gateway, store=ReviewStore(tmp_path, include_legacy=False)
    ))
    assert record.briefing_interaction.action == "decline"
    assert record.effective_brief.context_confidence == "minimal"
    assert record.effective_brief.assumptions
    assert record.task.hard_constraints == ["required_literal:{count}"]
    assert record.runtime_metadata.briefing_elicitation_actions == ["decline"]


def test_ui_button_alias_routes_to_ui_without_silent_unknown_normalization():
    assert normalize_content_type("UI button") == "ui"
    assert normalize_content_type("mystery surface") == "unspecified"
