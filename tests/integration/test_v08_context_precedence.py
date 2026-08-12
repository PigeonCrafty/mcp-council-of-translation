import asyncio
import json

import pytest

from council_of_translation.localization.guided import CONTEXT_ASSUMPTION_VALUE
from council_of_translation.localization.models import ReviewTaskV2
from council_of_translation.localization.orchestration import run_structured_review
from council_of_translation.localization.persistence import ReviewStore
from council_of_translation.localization.roles import build_council_plan
from council_of_translation.localization.runtime import (
    ElicitationResult,
    InteractionCapabilities,
    RuntimeTelemetry,
    ScriptedModelExecutor,
)


def _review(role_id, *, with_gap=False):
    return json.dumps({
        "role_feedback": "完成职责检查。",
        "findings": [{
            "source_span": "bigger than bigger",
            "candidate_span": "比大更大",
            "issue_type": "ux",
            "severity": "minor",
            "finding_kind": "choice",
            "proposed_value": "胜过伟大",
            "problem": "措辞用途需要确认",
            "evidence": "当前表达存在用途歧义",
            "action": "考虑替换",
            "confidence": 0.8,
        }],
        "context_gaps": ([{
            "question": "该文案用于品牌标语还是功能按钮？",
            "materiality": "答案会改变建议选项和最终结论",
            "affected_role_ids": [role_id, "unknown_role"],
        }] if with_gap else []),
    }, ensure_ascii=False)


class ContextThenOutcomeGateway:
    def __init__(self, context_result, *, supported=True):
        self.context_result = context_result
        self.supported = supported
        self.requests = []

    def capabilities(self):
        return InteractionCapabilities(form_elicitation=self.supported)

    async def elicit(self, message, *, response_type):
        self.requests.append((message, response_type))
        if len(self.requests) == 1:
            return self.context_result
        properties = response_type.model_json_schema()["properties"]
        field = next(iter(properties))
        selected = next(value for value in properties[field]["enum"] if value.startswith("改为："))
        return ElicitationResult(action="accept", data={field: selected})


def _run(tmp_path, context_result, *, supported=True):
    task = ReviewTaskV2(
        source_text="bigger than bigger",
        candidate_translation="比大更大",
        content_type="marketing",
        mode="standard",
        briefing_mode="off",
    )
    roles = build_council_plan("standard", "marketing").active_role_ids
    reviews = [_review(role, with_gap=index == 0) for index, role in enumerate(roles)]
    reviews.append(json.dumps({"change_effect": "unchanged", "findings": []}))
    telemetry = RuntimeTelemetry(sample_budget=13)
    executor = ScriptedModelExecutor(reviews, telemetry)
    gateway = ContextThenOutcomeGateway(context_result, supported=supported)
    record = asyncio.run(run_structured_review(
        task,
        executor,
        gateway,
        store=ReviewStore(tmp_path, include_legacy=False),
    ))
    return record, gateway, roles


@pytest.mark.parametrize("action", ["decline", "cancel", "error"])
def test_unresolved_context_actions_block_outcomes_and_require_review(tmp_path, action):
    record, gateway, _ = _run(tmp_path / action, ElicitationResult(action=action))
    assert len(gateway.requests) == 1
    assert record.context_gap_interaction.action == action
    assert record.runtime_metadata.outcome_elicitation_calls == 0
    assert record.user_decisions == []
    assert record.effective_brief.context_confidence != "full"
    assert record.status == "NEEDS_HUMAN_REVIEW"
    assert record.chief_editor_decision.publishability == "需人工复核"
    assert record.chief_editor_decision.review_needed == "是"
    assert "material_context_unresolved" in record.fallback_reason
    assert "material_context_unresolved" in record.warnings
    assert any(gap.disposition == "unanswered" for gap in record.context_gaps)
    assert record.context_gaps[0].question in record.display_report
    assert "## 你的决定与复议" not in record.display_report
    assert record.display_report.splitlines()[-1] == "- 最终处置：需人工复核；需人工复核：是"


def test_unsupported_and_malformed_context_are_unresolved(tmp_path):
    unsupported, gateway, _ = _run(
        tmp_path / "unsupported", ElicitationResult(action="error"), supported=False
    )
    assert gateway.requests == []
    assert unsupported.context_gap_interaction.action == "unsupported"
    assert unsupported.runtime_metadata.outcome_elicitation_calls == 0
    assert unsupported.status == "NEEDS_HUMAN_REVIEW"

    malformed, gateway, _ = _run(
        tmp_path / "malformed",
        ElicitationResult(action="accept", data={"wrong_field": "value"}),
    )
    assert len(gateway.requests) == 1
    assert malformed.context_gap_interaction.action == "malformed"
    assert malformed.user_decisions == []
    assert malformed.status == "NEEDS_HUMAN_REVIEW"


def test_explicit_assumption_is_not_an_answer_and_blocks_outcome(tmp_path):
    result = ElicitationResult(
        action="accept", data={"context_1": CONTEXT_ASSUMPTION_VALUE}
    )
    record, gateway, _ = _run(tmp_path, result)
    assert len(gateway.requests) == 1
    assert record.context_gap_interaction.action == "accept"
    assert record.context_gap_interaction.answered_gap_ids == [record.context_gaps[0].gap_id]
    assert record.context_gaps[0].disposition == "unanswered"
    assert record.context_gaps[0].reason == "explicit_assumption"
    assert record.runtime_metadata.outcome_elicitation_calls == 0
    assert record.status == "NEEDS_HUMAN_REVIEW"


def test_actual_answer_reconsiders_affected_active_role_before_outcome(tmp_path):
    result = ElicitationResult(
        action="accept", data={"context_1": "这是官网品牌标语，不是功能按钮。"}
    )
    record, gateway, roles = _run(tmp_path, result)
    assert len(gateway.requests) == 2
    assert "背景" in gateway.requests[0][0]
    assert record.context_gap_interaction.answered_count == 1
    assert record.context_reconsideration_provenance.requested_role_ids == [roles[0]]
    assert record.context_reconsideration_provenance.completed_role_ids == [roles[0]]
    assert "unknown_role" not in record.context_reconsideration_provenance.requested_role_ids
    assert record.runtime_metadata.outcome_elicitation_calls == 1
    assert any(decision.elicitation_action == "accept" for decision in record.user_decisions)
    assert record.status == "COMPLETED"
    assert record.runtime_metadata.sampling_calls == len(roles) + 1
    phase_names = [phase.phase for phase in record.phase_trace.phases]
    assert phase_names.index("context_gap") < phase_names.index("context_reconsideration")
    assert phase_names.index("context_reconsideration") < phase_names.index("outcome_decision")
