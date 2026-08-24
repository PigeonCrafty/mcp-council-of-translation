from __future__ import annotations

import pytest
from pydantic import ValidationError

from council_of_translation.localization.compatibility import parse_review_record
from council_of_translation.localization.decision_support import (
    INSUFFICIENT_REVIEW_REASON,
    classify_decision_support,
    finalize_decision_support,
)
from council_of_translation.localization.models import (
    ChiefEditorDecisionV2,
    ContextGapInteraction,
    ContextGapV2,
    CouncilPlan,
    CouncilValueMetrics,
    DecisionSupportAssessment,
    DecisionTrace,
    DecisionTraceEntry,
    IssueCluster,
    PreflightCheck,
    PreflightResult,
    ReconsiderationProvenance,
    ReviewBriefV2,
    ReviewRecordV2,
    ReviewTaskV2,
    RuntimeMetadata,
    UserDecision,
)


def _record(**updates: object) -> ReviewRecordV2:
    record = ReviewRecordV2(
        schema_version="2.5",
        review_id="review_support_test",
        task=ReviewTaskV2(source_text="ignored", candidate_translation="ignored"),
        council_plan=CouncilPlan(active_role_ids=["a", "b", "c"]),
        runtime_metadata=RuntimeMetadata(
            reviewer_coverage="full",
            reviewer_samples_successful=3,
            reviewer_samples_unavailable=0,
        ),
        effective_brief=ReviewBriefV2(context_confidence="full"),
        chief_editor_decision=ChiefEditorDecisionV2(
            publishability="可发布", review_needed="否"
        ),
        status="COMPLETED",
    )
    return record.model_copy(update=updates)


def test_clean_full_coverage_is_well_supported() -> None:
    assessment = classify_decision_support(_record())
    assert assessment.level == "well_supported"
    assert assessment.basis_codes == ["full_reviewer_coverage", "clean_confirmation"]
    assert assessment.limitation_codes == []
    assert assessment.outcome_coherent is True


@pytest.mark.parametrize("coverage", ["partial", "none"])
def test_incomplete_coverage_is_insufficient(coverage: str) -> None:
    assessment = classify_decision_support(_record(runtime_metadata=RuntimeMetadata(
        reviewer_coverage=coverage,
        reviewer_samples_successful=1 if coverage == "partial" else 0,
        reviewer_samples_unavailable=2 if coverage == "partial" else 3,
    )))
    assert assessment.level == "insufficient"
    assert "reviewer_unavailable" in assessment.limitation_codes
    expected_code = "partial_reviewer_coverage" if coverage == "partial" else "no_reviewer_coverage"
    assert expected_code in assessment.limitation_codes
    assert assessment.outcome_coherent is False


def test_deterministic_blocker_precedes_model_issue_and_is_well_supported() -> None:
    blocker = PreflightResult(checks=[PreflightCheck(
        check_id="required_literal", kind="required_literal", status="fail",
        severity="critical", blocking=True,
    )])
    issue = IssueCluster(
        issue_id="issue_model", severity="critical", consensus_status="disputed"
    )
    assessment = classify_decision_support(_record(
        preflight=blocker,
        policy_gate_result={"passed": False, "blocking_issue_ids": ["preflight_required"]},
        issue_clusters=[issue],
        chief_editor_decision=ChiefEditorDecisionV2(
            publishability="需人工复核", review_needed="是"
        ),
        status="NEEDS_HUMAN_REVIEW",
    ))
    assert assessment.level == "well_supported"
    assert assessment.basis_codes == [
        "full_reviewer_coverage", "structured_material_evidence",
        "deterministic_blocker", "policy_gate_enforced",
    ]
    assert assessment.limitation_codes == ["material_disagreement"]


def test_unresolved_context_precedes_deterministic_blocker() -> None:
    assessment = classify_decision_support(_record(
        preflight=PreflightResult(checks=[PreflightCheck(
            check_id="numeric", kind="numeric", status="fail", severity="critical", blocking=True,
        )]),
        policy_gate_result={"passed": False, "blocking_issue_ids": ["preflight_numeric"]},
        context_gaps=[ContextGapV2(
            gap_id="gap_1", question="bounded", materiality="material", disposition="unanswered"
        )],
        context_gap_interaction=ContextGapInteraction(
            requested=True, action="decline", asked_gap_ids=["gap_1"]
        ),
        degraded=True,
        chief_editor_decision=ChiefEditorDecisionV2(
            publishability="需人工复核", review_needed="是"
        ),
        status="NEEDS_HUMAN_REVIEW",
    ))
    assert assessment.level == "insufficient"
    assert "deterministic_blocker" in assessment.basis_codes
    assert "unresolved_material_context" in assessment.limitation_codes


def test_degraded_clean_review_is_insufficient() -> None:
    assessment = classify_decision_support(_record(
        degraded=True,
        fallback_reason="decision_validation_degraded",
        chief_editor_decision=ChiefEditorDecisionV2(
            publishability="需人工复核", review_needed="是"
        ),
        status="NEEDS_HUMAN_REVIEW",
    ))
    assert assessment.level == "insufficient"
    assert assessment.limitation_codes == ["degraded_execution", "runtime_fallback"]


def test_non_degraded_user_delegation_is_supported_with_limits() -> None:
    assessment = classify_decision_support(_record(
        user_decisions=[UserDecision(decision_id="d1", elicitation_action="delegate")],
        fallback_reason="user_delegated_to_council",
        status="COMPLETED_WITH_FALLBACK",
    ))
    assert assessment.level == "supported_with_limits"
    assert assessment.limitation_codes == ["council_fallback"]
    assert "runtime_fallback" not in assessment.limitation_codes


def test_valid_user_decision_and_completed_reconsideration_are_well_supported() -> None:
    assessment = classify_decision_support(_record(
        user_decisions=[UserDecision(
            decision_id="d1", selected_option_id="option_valid",
            elicitation_action="accept",
        )],
        reconsideration_provenance=ReconsiderationProvenance(
            requested_role_ids=["a"], completed_role_ids=["a"]
        ),
    ))
    assert assessment.level == "well_supported"
    assert assessment.basis_codes == [
        "full_reviewer_coverage", "clean_confirmation", "valid_user_decision",
        "completed_reconsideration",
    ]


def test_remaining_disagreement_limits_valid_user_decision() -> None:
    assessment = classify_decision_support(_record(
        issue_clusters=[IssueCluster(
            issue_id="issue_choice", severity="major", consensus_status="disputed"
        )],
        user_decisions=[UserDecision(
            decision_id="d1", selected_option_id="option_valid", elicitation_action="accept"
        )],
    ))
    assert assessment.level == "supported_with_limits"
    assert "valid_user_decision" in assessment.basis_codes
    assert "material_disagreement" in assessment.limitation_codes


def test_model_only_critical_human_review_is_supported_with_limits() -> None:
    assessment = classify_decision_support(_record(
        issue_clusters=[IssueCluster(
            issue_id="issue_risk", severity="critical", consensus_status="consensus"
        )],
        chief_editor_decision=ChiefEditorDecisionV2(
            publishability="需人工复核", review_needed="是"
        ),
        status="NEEDS_HUMAN_REVIEW",
    ))
    assert assessment.level == "supported_with_limits"
    assert "deterministic_blocker" not in assessment.basis_codes


def test_council_adjudication_records_basis_and_limit() -> None:
    assessment = classify_decision_support(_record(
        decision_trace=DecisionTrace(entries=[DecisionTraceEntry(
            issue_id="issue_1", decision="bounded", outcome="council_fallback"
        )]),
    ))
    assert assessment.level == "supported_with_limits"
    assert "council_adjudication" in assessment.basis_codes
    assert assessment.limitation_codes == ["council_fallback"]


def test_pending_and_incomplete_reconsideration_are_insufficient() -> None:
    assessment = classify_decision_support(_record(
        reconsideration_provenance=ReconsiderationProvenance(
            requested_role_ids=["a", "b"], completed_role_ids=["a"], skipped_role_ids=["b"]
        ),
        status="RETURNED_PENDING",
        chief_editor_decision=ChiefEditorDecisionV2(
            publishability="需人工复核", review_needed="是"
        ),
    ))
    assert assessment.level == "insufficient"
    assert assessment.limitation_codes == ["pending_user_input", "incomplete_reconsideration"]
    assert assessment.outcome_coherent is True


def test_context_confidence_alone_limits_but_does_not_make_support_insufficient() -> None:
    for confidence, code in (("minimal", "minimal_context"), ("partial", "partial_context")):
        assessment = classify_decision_support(_record(
            effective_brief=ReviewBriefV2(context_confidence=confidence)
        ))
        assert assessment.level == "supported_with_limits"
        assert assessment.limitation_codes == [code]


def test_codes_dedupe_and_serialize_in_canonical_order() -> None:
    assessment = DecisionSupportAssessment(
        level="supported_with_limits",
        basis_codes=["valid_user_decision", "full_reviewer_coverage", "valid_user_decision"],
        limitation_codes=["runtime_fallback", "partial_context", "runtime_fallback"],
        assessment_basis="deterministic_structured_trace_v1",
        outcome_coherent=True,
    )
    assert assessment.basis_codes == ["full_reviewer_coverage", "valid_user_decision"]
    assert assessment.limitation_codes == ["partial_context", "runtime_fallback"]


@pytest.mark.parametrize("field", ["basis_codes", "limitation_codes"])
def test_unknown_codes_are_rejected(field: str) -> None:
    with pytest.raises(ValidationError):
        DecisionSupportAssessment.model_validate({
            "level": "well_supported",
            field: ["unknown_code"],
            "assessment_basis": "deterministic_structured_trace_v1",
            "outcome_coherent": True,
        })


def test_not_recorded_state_is_exact() -> None:
    assert DecisionSupportAssessment().model_dump(mode="json") == {
        "level": "not_recorded",
        "support_target": "chief_disposition",
        "basis_codes": [],
        "limitation_codes": [],
        "assessment_basis": "not_recorded",
        "outcome_coherent": None,
    }
    with pytest.raises(ValidationError):
        DecisionSupportAssessment(
            level="not_recorded", basis_codes=["full_reviewer_coverage"]
        )


def test_free_prose_and_numeric_confidence_do_not_affect_classification() -> None:
    original = _record(independent_reviews=[{
        "role_feedback": "A", "findings": [{"confidence": 0.0, "evidence": "first"}]
    }])
    hostile = original.model_copy(update={
        "task": ReviewTaskV2(source_text="different", candidate_translation="different"),
        "independent_reviews": [{
            "role_feedback": "entirely different prose",
            "findings": [{"confidence": 1.0, "evidence": "different"}],
        }],
    })
    assert classify_decision_support(original) == classify_decision_support(hostile)


def test_classifier_is_total_for_historical_default_record() -> None:
    assessment = classify_decision_support(ReviewRecordV2(
        review_id="historical", task=ReviewTaskV2()
    ))
    assert assessment.level == "supported_with_limits"
    assert assessment.assessment_basis == "deterministic_structured_trace_v1"


def test_finalizer_tightens_only_disposition_fields_and_freezes_schema_26() -> None:
    record = _record(
        runtime_metadata=RuntimeMetadata(
            reviewer_coverage="partial",
            reviewer_samples_successful=2,
            reviewer_samples_unavailable=1,
        ),
        chief_editor_decision=ChiefEditorDecisionV2(
            publishability="修改后可发布",
            review_needed="否",
            must_fix=["bounded must fix"],
            should_fix=["bounded should fix"],
            execution_order=["bounded order"],
            suggested_translation="bounded suggestion",
        ),
    )
    finalized = finalize_decision_support(record)
    assert finalized.schema_version == "2.6"
    assert finalized.version_metadata["record_schema"] == "2.6"
    assert finalized.status == "NEEDS_HUMAN_REVIEW"
    assert finalized.chief_editor_decision.publishability == "需人工复核"
    assert finalized.chief_editor_decision.review_needed == "是"
    assert finalized.chief_editor_decision.review_reason == INSUFFICIENT_REVIEW_REASON
    assert finalized.chief_editor_decision.must_fix == ["bounded must fix"]
    assert finalized.chief_editor_decision.should_fix == ["bounded should fix"]
    assert finalized.chief_editor_decision.execution_order == ["bounded order"]
    assert finalized.chief_editor_decision.suggested_translation == "bounded suggestion"
    assert finalized.decision_support.level == "insufficient"
    assert finalized.decision_support.outcome_coherent is True


def test_non_insufficient_levels_never_change_chief_authority() -> None:
    chief = ChiefEditorDecisionV2(publishability="需人工复核", review_needed="是")
    finalized = finalize_decision_support(_record(
        issue_clusters=[IssueCluster(
            issue_id="issue_model", severity="critical", consensus_status="consensus"
        )],
        chief_editor_decision=chief,
        status="NEEDS_HUMAN_REVIEW",
    ))
    assert finalized.decision_support.level == "supported_with_limits"
    assert finalized.chief_editor_decision == chief


def test_schema_26_requires_current_assessment_for_new_model_validation() -> None:
    with pytest.raises(ValidationError, match="recorded decision support"):
        ReviewRecordV2(
            schema_version="2.6", review_id="invalid_new", task=ReviewTaskV2()
        )


@pytest.mark.parametrize("version", ["2.0", "2.1", "2.2", "2.3", "2.4", "2.5"])
def test_historical_v2_assessment_is_never_inferred(version: str) -> None:
    payload = _record().model_dump(mode="json")
    payload["schema_version"] = version
    payload["decision_support"] = {
        "level": "well_supported",
        "basis_codes": ["full_reviewer_coverage"],
        "limitation_codes": [],
        "assessment_basis": "deterministic_structured_trace_v1",
        "outcome_coherent": True,
    }
    parsed = parse_review_record(payload)
    assert parsed.decision_support == DecisionSupportAssessment()


def test_hostile_schema_26_assessment_is_conservatively_unrecorded() -> None:
    payload = finalize_decision_support(_record()).model_dump(mode="json")
    payload["decision_support"]["basis_codes"] = ["unknown_code"]
    parsed = parse_review_record(payload)
    assert parsed.schema_version == "2.6"
    assert parsed.decision_support == DecisionSupportAssessment()
