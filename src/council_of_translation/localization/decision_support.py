"""Deterministic support assessment for the chief editor disposition.

The classifier deliberately consumes only bounded structured trace fields. It
does not inspect source, candidate, reviewer feedback, evidence prose, or model
confidence values and performs no external execution.
"""

from __future__ import annotations

from council_of_translation.localization.models import (
    DECISION_SUPPORT_BASIS_ORDER,
    DECISION_SUPPORT_LIMITATION_ORDER,
    DecisionSupportAssessment,
    IssueCluster,
    ReviewRecordV2,
)


_MATERIAL_SEVERITIES = {"critical", "major"}
_PENDING_BRIEFING_ACTIONS = {"decline", "cancel", "unsupported", "malformed", "error"}
_RUNTIME_FALLBACK_EXEMPTION = "user_delegated_to_council"
INSUFFICIENT_REVIEW_REASON = "结论依据不足；需人工复核后再决定是否发布。"


def _ordered(selected: set[str], order: tuple[str, ...]) -> list[str]:
    return [code for code in order if code in selected]


def _material_cluster(cluster: IssueCluster) -> bool:
    return bool(
        cluster.severity in _MATERIAL_SEVERITIES
        or cluster.blocking
        or cluster.needs_user_input
    )


def _fallback_codes(record: ReviewRecordV2) -> set[str]:
    codes = {code for code in record.runtime_metadata.fallbacks if code}
    codes.update(code for code in record.fallback_reason.split(";") if code)
    return codes


def _expected_status(record: ReviewRecordV2) -> str:
    if record.chief_editor_decision.review_needed == "是":
        return "NEEDS_HUMAN_REVIEW"
    if record.fallback_reason:
        return "COMPLETED_WITH_FALLBACK"
    return "COMPLETED"


def classify_decision_support(record: ReviewRecordV2) -> DecisionSupportAssessment:
    """Classify support for the disposition from validated structured trace only."""

    basis: set[str] = set()
    limitations: set[str] = set()
    coverage = record.runtime_metadata.reviewer_coverage
    unavailable = bool(
        record.runtime_metadata.reviewer_samples_unavailable
        or record.council_value_metrics.unavailable_role_count
    )
    material_clusters = [cluster for cluster in record.issue_clusters if _material_cluster(cluster)]
    material_disagreement = any(
        cluster.consensus_status in {"disputed", "insufficient_evidence"}
        for cluster in material_clusters
    )
    deterministic_blocker = bool(
        record.preflight.blocking
        or record.policy_gate_result.get("blocking_issue_ids")
        or record.policy_gate_result.get("passed") is False
    )
    valid_user_decision = any(
        decision.elicitation_action == "accept"
        and decision.selection_kind == "outcome"
        and bool(decision.selected_option_id)
        for decision in record.user_decisions
    )
    council_adjudication = any(
        entry.outcome == "council_fallback" for entry in record.decision_trace.entries
    )
    delegated_to_council = any(
        decision.elicitation_action == "delegate"
        or decision.selection_kind == "council_delegation"
        for decision in record.user_decisions
    )
    provenances = (
        record.reconsideration_provenance,
        record.context_reconsideration_provenance,
        record.outcome_reconsideration_provenance,
    )
    requested = {
        role_id for provenance in provenances for role_id in provenance.requested_role_ids
    }
    completed = {
        role_id for provenance in provenances for role_id in provenance.completed_role_ids
    }
    incomplete_reconsideration = bool(
        any(provenance.failed_role_ids for provenance in provenances)
        or any(provenance.skipped_role_ids for provenance in provenances)
        or requested - completed
    )
    completed_reconsideration = bool(requested) and not incomplete_reconsideration
    selected_gap_ids = set(record.context_gap_interaction.asked_gap_ids)
    resolved_gap_ids = {
        gap.gap_id for gap in record.context_gaps
        if gap.gap_id in selected_gap_ids and gap.disposition == "answered"
    }
    unresolved_material_context = bool(selected_gap_ids - resolved_gap_ids)
    briefing_pending = bool(
        record.task.briefing_mode == "always"
        and
        record.briefing_interaction.requested
        and record.briefing_interaction.action in _PENDING_BRIEFING_ACTIONS
    )
    user_input_pending = any(
        decision.elicitation_action in {"pending", "decline", "cancel", "unsupported", "malformed"}
        for decision in record.user_decisions
    )
    pending = record.status == "RETURNED_PENDING" or briefing_pending or user_input_pending
    fallback_codes = _fallback_codes(record)
    non_exempt_fallbacks = fallback_codes - {_RUNTIME_FALLBACK_EXEMPTION}
    runtime_fallback = bool(non_exempt_fallbacks) or bool(
        _RUNTIME_FALLBACK_EXEMPTION in fallback_codes and record.degraded
    )

    if coverage == "full":
        basis.add("full_reviewer_coverage")
    elif coverage == "partial":
        limitations.add("partial_reviewer_coverage")
    elif coverage == "none":
        limitations.add("no_reviewer_coverage")
    if unavailable:
        limitations.add("reviewer_unavailable")
    if record.effective_brief.context_confidence == "minimal":
        limitations.add("minimal_context")
    elif record.effective_brief.context_confidence == "partial":
        limitations.add("partial_context")
    if material_clusters:
        basis.add("structured_material_evidence")
    elif coverage == "full" and not record.issue_clusters:
        basis.add("clean_confirmation")
    if record.council_value_metrics.corroborated_issue_count:
        basis.add("corroborated_material_evidence")
    if deterministic_blocker:
        basis.update({"deterministic_blocker", "policy_gate_enforced"})
    if valid_user_decision:
        basis.add("valid_user_decision")
    if completed_reconsideration:
        basis.add("completed_reconsideration")
    if council_adjudication:
        basis.add("council_adjudication")
    if material_disagreement:
        limitations.add("material_disagreement")
    if council_adjudication or delegated_to_council:
        limitations.add("council_fallback")
    if unresolved_material_context:
        limitations.add("unresolved_material_context")
    if pending:
        limitations.add("pending_user_input")
    if incomplete_reconsideration:
        limitations.add("incomplete_reconsideration")
    if record.degraded:
        limitations.add("degraded_execution")
    if runtime_fallback:
        limitations.add("runtime_fallback")

    insufficient = bool(
        pending
        or unresolved_material_context
        or coverage in {"partial", "none"}
        or unavailable
        or incomplete_reconsideration
        or record.degraded
        or runtime_fallback
    )
    if insufficient:
        level = "insufficient"
    elif (
        deterministic_blocker
        and record.chief_editor_decision.publishability == "需人工复核"
        and record.chief_editor_decision.review_needed == "是"
    ):
        level = "well_supported"
    elif material_clusters or material_disagreement or limitations & {
        "minimal_context", "partial_context", "council_fallback"
    }:
        level = "supported_with_limits"
    else:
        level = "well_supported"

    if level == "insufficient":
        coherent = bool(
            record.chief_editor_decision.publishability == "需人工复核"
            and record.chief_editor_decision.review_needed == "是"
            and record.status in {"NEEDS_HUMAN_REVIEW", "RETURNED_PENDING"}
        )
    else:
        coherent = record.status == _expected_status(record)

    return DecisionSupportAssessment(
        level=level,
        basis_codes=_ordered(basis, DECISION_SUPPORT_BASIS_ORDER),
        limitation_codes=_ordered(limitations, DECISION_SUPPORT_LIMITATION_ORDER),
        assessment_basis="deterministic_structured_trace_v1",
        outcome_coherent=coherent,
    )


def finalize_decision_support(record: ReviewRecordV2) -> ReviewRecordV2:
    """Apply the one-way insufficient-support rule and freeze Schema 2.6."""

    assessment = classify_decision_support(record)
    if assessment.level == "insufficient" and (
        record.chief_editor_decision.publishability != "需人工复核"
        or record.chief_editor_decision.review_needed != "是"
    ):
        record.chief_editor_decision.publishability = "需人工复核"
        record.chief_editor_decision.review_needed = "是"
        record.chief_editor_decision.review_reason = INSUFFICIENT_REVIEW_REASON
        if record.status != "RETURNED_PENDING":
            record.status = "NEEDS_HUMAN_REVIEW"
    record.decision_support = classify_decision_support(record)
    payload = record.model_dump(mode="json")
    payload["schema_version"] = "2.6"
    payload["version_metadata"] = {
        **payload.get("version_metadata", {}),
        "record_schema": "2.6",
    }
    return ReviewRecordV2.model_validate(payload)
