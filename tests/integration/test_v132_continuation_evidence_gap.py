import asyncio
import json

from council_of_translation.localization.models import ReviewTaskV2
from council_of_translation.localization.orchestration import (
    compact_review_response,
    continue_structured_review,
    run_structured_review,
)
from council_of_translation.localization.persistence import ReviewStore
from council_of_translation.localization.runtime import (
    RuntimeTelemetry,
    ScriptedModelExecutor,
    ScriptedUserInteractionGateway,
)
from council_of_translation.localization.verification import (
    CANONICAL_RECEIPT_LABEL,
    append_canonical_receipt_json,
    build_verification_receipt,
    render_verification_report,
)


class CountingReviewStore(ReviewStore):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.save_calls = 0

    def save(self, record, *, history_mode=None):
        self.save_calls += 1
        return super().save(record, history_mode=history_mode)


def _review(findings=None):
    return json.dumps({"role_feedback": "bounded review", "findings": findings or []})


def _choice(*, source_span, candidate_span, severity, action):
    return {
        "source_span": source_span,
        "candidate_span": candidate_span,
        "issue_type": "terminology",
        "severity": severity,
        "problem": "bounded wording choice",
        "evidence": "bounded wording evidence",
        "action": action,
        "finding_kind": "choice",
        "proposed_value": action,
        "confidence": 0.8,
    }


def test_continuation_preserves_unresolved_discussion_gap_and_unrelated_valid_choice(tmp_path):
    parent_telemetry = RuntimeTelemetry(sample_budget=13)
    parent_executor = ScriptedModelExecutor(
        [
            _review(),
            _review(),
            _review([_choice(
                source_span="Continue",
                candidate_span="继续",
                severity="major",
                action="继续",
            )]),
            _review([_choice(
                source_span="Save",
                candidate_span="保存",
                severity="minor",
                action="存储",
            )]),
            _review(),
            _review([_choice(
                source_span="Continue",
                candidate_span="继续",
                severity="major",
                action="下一步",
            )]),
            json.dumps({}),
        ],
        parent_telemetry,
    )
    store = CountingReviewStore(tmp_path / "records", legacy_dir=tmp_path / "legacy")
    parent_gateway = ScriptedUserInteractionGateway(
        supported=False,
        telemetry=parent_telemetry,
    )
    parent = asyncio.run(run_structured_review(
        ReviewTaskV2(
            source_text="Continue Save",
            candidate_translation="继续 保存",
            content_type="ui",
            briefing_mode="off",
        ),
        parent_executor,
        parent_gateway,
        store=store,
    ))

    point = next(point for point in parent.decision_points if "Save" in point.question)
    selected = next(option for option in point.options if option.is_current_candidate)
    parent_snapshot = parent.model_dump(mode="json")
    parent_path = store.path_for(parent.review_id)
    parent_bytes = parent_path.read_bytes()
    reconsideration = json.dumps({
        "positions": [{
            "issue_id": point.issue_id,
            "stance": "accept",
            "option_id": selected.option_id,
            "claim": "the caller selected the valid current wording",
            "evidence": ["explicit caller choice"],
            "confidence": 0.9,
        }]
    })
    child_telemetry = RuntimeTelemetry(sample_budget=13)
    child_executor = ScriptedModelExecutor([reconsideration], child_telemetry)
    child = asyncio.run(continue_structured_review(
        parent,
        [{"decision_id": point.decision_id, "selected_option_id": selected.option_id}],
        child_executor,
        store=store,
    ))

    assert parent.status == "NEEDS_HUMAN_REVIEW"
    assert parent.degraded is True
    assert parent.fallback_reason == "discussion_unavailable;user_interaction_unsupported"
    assert parent.warnings == ["discussion_unavailable"]
    assert parent.chief_editor_decision.publishability == "需人工复核"
    assert parent.chief_editor_decision.review_needed == "是"
    assert parent.decision_support.level == "insufficient"

    assert child.status == "NEEDS_HUMAN_REVIEW"
    assert child.degraded is True
    assert child.fallback_reason == "discussion_unavailable"
    assert child.warnings == ["discussion_unavailable"]
    assert child.chief_editor_decision.publishability == "需人工复核"
    assert child.chief_editor_decision.review_needed == "是"
    assert child.decision_support.level == "insufficient"

    assert child.user_decisions[0].selected_option_id == selected.option_id
    assert child.user_decisions[0].selected_outcome_value == selected.outcome_value
    assert child.reconsideration_provenance.completed_role_ids == ["product_context_reviewer"]
    assert child.reconsiderations[0].status == "completed"
    assert child.decision_trace.entries[0].outcome == "valid_user_choice"
    assert child.decision_trace.entries[0].selected_option_id == selected.option_id

    assert child.parent_review_id == parent.review_id
    assert child.review_id != parent.review_id
    assert parent.model_dump(mode="json") == parent_snapshot
    assert parent_path.read_bytes() == parent_bytes
    assert store.save_calls == 2
    assert len(parent_executor.prompts) == 7
    assert len(child_executor.prompts) == 1
    assert parent.runtime_metadata.sampling_calls == 7
    assert child.runtime_metadata.sampling_calls == 1
    assert parent.runtime_metadata.elicitation_calls == 0
    assert child.runtime_metadata.elicitation_calls == 0
    assert parent_gateway.requests == []

    compact = compact_review_response(child)
    assert compact["status"] == child.status
    assert compact["fallback_reason"] == "discussion_unavailable"
    assert compact["warnings"] == ["discussion_unavailable"]
    assert compact["degraded"] is True
    assert compact["chief_editor"]["publishability"] == "需人工复核"
    assert compact["chief_editor"]["review_needed"] == "是"
    assert compact["decision_support"]["level"] == "insufficient"
    discussion_phase = next(
        phase for phase in child.phase_trace.phases if phase.phase == "discussion"
    )
    assert discussion_phase.disposition == "degraded"
    assert "本次执行存在降级或回退；相关风险需在发布前人工确认。" in child.display_report
    assert child.display_report.rstrip().endswith("- 最终处置：需人工复核；需人工复核：是")

    receipt = build_verification_receipt(child)
    assert receipt["outcome"] == {
        "status": "NEEDS_HUMAN_REVIEW",
        "degraded": True,
        "warning_count": 1,
        "fallback_reason_code": "discussion_unavailable",
        "fallback_reason_redacted": False,
        "publishability": "需人工复核",
        "review_needed": "是",
        "suggested_translation_present": False,
    }
    assert receipt["decision_support"]["level"] == "insufficient"
    assert receipt["decision_support"]["outcome_coherent"] is True
    assert receipt["coherence"]["terminal_disposition_occurrences"] == 1
    assert receipt["coherence"]["terminal_disposition_is_last_report_line"] is True
    assert receipt["coherence"]["terminal_disposition_matches_structured"] is True
    assert receipt["availability"]["verification_complete"] is True
    assert receipt["availability"]["redacted_fields"] == []
    verification_report = render_verification_report(receipt)
    verification_text = append_canonical_receipt_json(verification_report, receipt)
    marker = f"\n\n{CANONICAL_RECEIPT_LABEL}\n```json\n"
    rendered_report, separator, fenced_receipt = verification_text.partition(marker)
    assert separator == marker
    assert rendered_report == verification_report
    assert fenced_receipt.endswith("\n```")
    assert json.loads(fenced_receipt[:-4]) == receipt


def test_clean_parent_continuation_does_not_invent_sticky_discussion_gap(tmp_path):
    parent_telemetry = RuntimeTelemetry(sample_budget=13)
    parent_executor = ScriptedModelExecutor(
        [
            _review(),
            _review(),
            _review([_choice(
                source_span="Continue",
                candidate_span="继续",
                severity="minor",
                action="继续",
            )]),
            _review(),
            _review(),
            _review([_choice(
                source_span="Continue",
                candidate_span="继续",
                severity="minor",
                action="下一步",
            )]),
            json.dumps({"turns": []}),
        ],
        parent_telemetry,
    )
    store = CountingReviewStore(tmp_path / "records", legacy_dir=tmp_path / "legacy")
    parent = asyncio.run(run_structured_review(
        ReviewTaskV2(
            source_text="Continue",
            candidate_translation="继续",
            content_type="ui",
            briefing_mode="off",
        ),
        parent_executor,
        ScriptedUserInteractionGateway(supported=False, telemetry=parent_telemetry),
        store=store,
    ))
    point = parent.decision_points[0]
    selected = next(option for option in point.options if option.is_current_candidate)
    reconsideration = json.dumps({
        "positions": [{
            "issue_id": point.issue_id,
            "stance": "accept",
            "option_id": selected.option_id,
            "claim": "the caller selected the valid current wording",
            "confidence": 0.9,
        }]
    })
    child_telemetry = RuntimeTelemetry(sample_budget=13)
    child_executor = ScriptedModelExecutor([reconsideration], child_telemetry)

    child = asyncio.run(continue_structured_review(
        parent,
        [{"decision_id": point.decision_id, "selected_option_id": selected.option_id}],
        child_executor,
        store=store,
    ))

    assert "discussion_unavailable" not in parent.warnings
    assert "discussion_unavailable" not in parent.fallback_reason.split(";")
    assert "discussion_unavailable" not in child.warnings
    assert "discussion_unavailable" not in child.fallback_reason.split(";")
    assert child.degraded is False
    assert child.status == "COMPLETED"
    assert child.chief_editor_decision.review_needed == "否"
    assert child.decision_trace.entries[0].outcome == "valid_user_choice"
    assert child.reconsideration_provenance.completed_role_ids == ["fluency_reviewer"]
    assert len(parent_executor.prompts) == 7
    assert len(child_executor.prompts) == 1
    assert child.runtime_metadata.sampling_calls == 1
    assert child.runtime_metadata.elicitation_calls == 0
    assert store.save_calls == 2
