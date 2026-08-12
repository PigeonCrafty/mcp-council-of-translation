"""Versioned domain models for the structured deliberation workflow.

Models that can be populated from sampled output use conservative defaults.  In
particular, sampled findings are evidence only: they cannot manufacture hard
constraints or deterministic blockers.
"""

from __future__ import annotations

from datetime import datetime, timezone
import hashlib
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator


ReviewMode = Literal["lightweight", "standard", "strict"]
HistoryMode = Literal["off", "metadata", "full"]
TraceLevel = Literal["summary", "full"]
ConstraintTier = Literal["hard", "contextual", "preference", "advisory"]
Severity = Literal["critical", "major", "minor", "preference"]
EvidenceOrigin = Literal["caller", "preflight", "model", "user", "system"]
FindingKind = Literal["issue", "choice", "affirmation"]
BriefingMode = Literal["auto", "always", "off"]
ContextConfidence = Literal["full", "partial", "minimal"]
FieldProvenance = Literal["caller", "user_briefing", "normalized_alias", "inferred_default"]


def option_id_for_action(issue_id: str, action: str) -> str:
    """Return the single authoritative identity for an issue/action option."""
    normalized_action = str(action).strip()
    digest = hashlib.sha256(f"{issue_id}\x1f{normalized_action}".encode("utf-8")).hexdigest()[:12]
    return f"option_{digest}"


class DomainModel(BaseModel):
    model_config = ConfigDict(extra="ignore", str_strip_whitespace=True)


class InputDiagnostics(DomainModel):
    source_original_length: int = Field(default=0, ge=0)
    source_reviewed_length: int = Field(default=0, ge=0)
    source_truncated: bool = False
    candidate_original_length: int = Field(default=0, ge=0)
    candidate_reviewed_length: int = Field(default=0, ge=0)
    candidate_truncated: bool = False


class FindingV2(DomainModel):
    finding_id: str = ""
    agent_name: str = "unknown_reviewer"
    role_perspective: str = "unknown"
    source_span: str = ""
    candidate_span: str = ""
    issue_type: Literal[
        "accuracy", "fluency", "style", "terminology", "context", "risk", "technical", "ux", "other"
    ] = "other"
    severity: Severity = "minor"
    constraint_tier: ConstraintTier = "advisory"
    blocking: bool = False
    problem: str = ""
    evidence: str = ""
    evidence_type: str = "model_observation"
    evidence_origin: EvidenceOrigin = "model"
    rule_refs: list[str] = Field(default_factory=list)
    action: str = ""
    finding_kind: FindingKind = "issue"
    proposed_value: str = ""
    confidence: float = Field(default=0.0, ge=0.0, le=1.0)

    @model_validator(mode="before")
    @classmethod
    def accept_legacy_span_and_normalize_untrusted(cls, value: Any) -> Any:
        if not isinstance(value, dict):
            return {}
        data = dict(value)
        legacy_span = data.get("span", "")
        data.setdefault("source_span", legacy_span)
        data.setdefault("candidate_span", legacy_span)
        valid_issue_types = {"accuracy", "fluency", "style", "terminology", "context", "risk", "technical", "ux", "other"}
        if data.get("issue_type") not in valid_issue_types:
            data["issue_type"] = "other"
        if data.get("severity") not in {"critical", "major", "minor", "preference"}:
            data["severity"] = "minor"
        if data.get("constraint_tier") not in {"hard", "contextual", "preference", "advisory"}:
            data["constraint_tier"] = "advisory"
        if data.get("evidence_origin") not in {"caller", "preflight", "model", "user", "system"}:
            data["evidence_origin"] = "model"
        # Missing V2.0 classification is deliberately treated as an issue.  In
        # particular, legacy action prose is never promoted into an outcome.
        if data.get("finding_kind") not in {"issue", "choice", "affirmation"}:
            data["finding_kind"] = "issue"
        proposal = data.get("proposed_value", "")
        data["proposed_value"] = proposal.strip() if isinstance(proposal, str) and len(proposal) <= 500 else ""
        # Sampled prose cannot escalate itself into a hard rule or blocker.
        if data.get("evidence_origin", "model") == "model":
            data["blocking"] = False
            if data.get("constraint_tier") == "hard":
                data["constraint_tier"] = "advisory"
        if data["finding_kind"] == "affirmation":
            data["blocking"] = False
            if data.get("constraint_tier") == "hard":
                data["constraint_tier"] = "advisory"
        return data


class RoleDefinition(DomainModel):
    id: str
    display_name: str
    role_type: Literal["reviewer", "adjudicator"] = "reviewer"
    mission: str
    scope: list[str] = Field(default_factory=list)
    must_check: list[str] = Field(default_factory=list)
    must_not_decide: list[str] = Field(default_factory=list)
    evidence_policy: list[str] = Field(default_factory=list)
    blocking_conditions: list[str] = Field(default_factory=list)
    applicable_modes: list[ReviewMode] = Field(default_factory=lambda: ["standard"])
    applicable_content_types: list[str] = Field(default_factory=lambda: ["*"])
    discussion_policy: Literal["never", "when_relevant", "adjudicate"] = "when_relevant"
    priority: int = Field(default=100, ge=0)
    output_contract_version: str = "2.0"
    prompt_version: str = "2.0"


class CouncilPlan(DomainModel):
    mode: ReviewMode = "standard"
    content_type: str = "unspecified"
    active_role_ids: list[str] = Field(default_factory=list)
    discussion_enabled: bool = True
    interactive_enabled: bool = True
    sample_budget: int = Field(default=13, ge=0, le=18)
    max_discussion_rounds: int = Field(default=1, ge=0, le=1)
    max_decision_points: int = Field(default=3, ge=0, le=3)


class PreflightCheck(DomainModel):
    check_id: str
    kind: str
    status: Literal["pass", "warning", "fail"] = "pass"
    severity: Severity = "minor"
    source_evidence: list[str] = Field(default_factory=list)
    candidate_evidence: list[str] = Field(default_factory=list)
    blocking: bool = False
    message: str = ""


class PreflightResult(DomainModel):
    checks: list[PreflightCheck] = Field(default_factory=list)
    blocking: bool = False

    @model_validator(mode="after")
    def derive_blocking(self) -> "PreflightResult":
        self.blocking = any(check.blocking and check.status == "fail" for check in self.checks)
        return self


class RolePosition(DomainModel):
    role_id: str
    stance: Literal["accept", "accept_with_conditions", "reject", "not_applicable"] = "not_applicable"
    option_id: str = ""
    claim: str = ""
    evidence: list[str] = Field(default_factory=list)
    evidence_origin: EvidenceOrigin = "model"
    constraint_tier: ConstraintTier = "advisory"
    rule_refs: list[str] = Field(default_factory=list)
    confidence: float = Field(default=0.0, ge=0.0, le=1.0)
    blocking: bool = False
    conditions: list[str] = Field(default_factory=list)

    @model_validator(mode="before")
    @classmethod
    def normalize_stance(cls, value: Any) -> Any:
        if not isinstance(value, dict):
            return {}
        data = dict(value)
        if data.get("stance") not in {"accept", "accept_with_conditions", "reject", "not_applicable"}:
            data["stance"] = "not_applicable"
            data["blocking"] = False
        if data.get("evidence_origin") not in {"caller", "preflight", "model", "user", "system"}:
            data["evidence_origin"] = "model"
        if data.get("constraint_tier") not in {"hard", "contextual", "preference", "advisory"}:
            data["constraint_tier"] = "advisory"
        if data.get("evidence_origin", "model") == "model":
            data["blocking"] = False
            if data.get("constraint_tier") == "hard":
                data["constraint_tier"] = "advisory"
        return data


class IssueCluster(DomainModel):
    issue_id: str
    topic: str = ""
    category: str = "other"
    source_spans: list[str] = Field(default_factory=list)
    candidate_spans: list[str] = Field(default_factory=list)
    finding_ids: list[str] = Field(default_factory=list)
    participant_role_ids: list[str] = Field(default_factory=list)
    candidate_actions: list[str] = Field(default_factory=list)
    current_outcome: str = ""
    outcome_anchor: str = ""
    positions: list[RolePosition] = Field(default_factory=list)
    evidence: list[str] = Field(default_factory=list)
    immutable_hard_constraints: list[str] = Field(default_factory=list)
    severity: Severity = "minor"
    constraint_tier: ConstraintTier = "advisory"
    blocking: bool = False
    consensus_status: Literal["consensus", "disputed", "insufficient_evidence"] = "insufficient_evidence"
    needs_user_input: bool = False

    @model_validator(mode="after")
    def bound_issue_summary(self) -> "IssueCluster":
        self.topic = self.topic[:240]
        self.source_spans = [item[:240] for item in self.source_spans[:8]]
        self.candidate_spans = [item[:240] for item in self.candidate_spans[:8]]
        self.evidence = [item[:240] for item in self.evidence[:8]]
        if len(self.current_outcome) > 500 or len(self.outcome_anchor) > 500:
            self.current_outcome = ""
            self.outcome_anchor = ""
        return self


class DiscussionTurn(DomainModel):
    round_id: str
    issue_id: str
    speaker: str
    target: str = ""
    stance: Literal["support", "challenge", "qualify", "reconsider"] = "qualify"
    claim: str = ""
    evidence: list[str] = Field(default_factory=list)
    proposed_action: str = ""
    confidence: float = Field(default=0.0, ge=0.0, le=1.0)
    position_changed: bool = False


class DiscussionRound(DomainModel):
    round_id: str
    issue_ids: list[str] = Field(default_factory=list)
    turns: list[DiscussionTurn] = Field(default_factory=list)


class DecisionOption(DomainModel):
    option_id: str
    outcome_value: str = ""
    label: str
    description: str = ""
    support_role_ids: list[str] = Field(default_factory=list)
    support_rationale: str = ""
    policy_basis: list[str] = Field(default_factory=list)
    is_current_candidate: bool = False
    is_delegation: bool = False
    valid: bool = True
    invalid_reason: str = ""

    @model_validator(mode="after")
    def bound_display_and_provenance(self) -> "DecisionOption":
        self.label = self.label[:48]
        self.description = self.description[:160]
        self.support_rationale = self.support_rationale[:240]
        self.support_role_ids = list(dict.fromkeys(self.support_role_ids))[:8]
        self.policy_basis = list(dict.fromkeys(self.policy_basis))[:8]
        if len(self.outcome_value) > 500:
            self.outcome_value = ""
            self.valid = False
            self.invalid_reason = self.invalid_reason or "outcome_value_too_long"
        if self.is_delegation:
            self.outcome_value = ""
            self.is_current_candidate = False
        return self


class DecisionPoint(DomainModel):
    decision_id: str
    issue_id: str
    question: str
    options: list[DecisionOption] = Field(default_factory=list)
    recommended_option_id: str = ""
    reason_user_input_useful: str = ""
    fallback_option_id: str = ""

    @model_validator(mode="after")
    def enforce_meaningful_choice(self) -> "DecisionPoint":
        self.question = self.question[:240]
        self.reason_user_input_useful = self.reason_user_input_useful[:240]
        self.options = self.options[:4]
        valid_ids = {option.option_id for option in self.options if option.valid}
        if self.recommended_option_id not in valid_ids:
            self.recommended_option_id = ""
        if self.fallback_option_id not in valid_ids:
            self.fallback_option_id = ""
        return self


class UserDecision(DomainModel):
    decision_id: str
    selected_option_id: str = ""
    selected_outcome_value: str = ""
    selection_kind: Literal["outcome", "council_delegation", "none"] = "none"
    authority_mode: Literal["decisive_within_valid_options", "advisory", "policy_override"] = "decisive_within_valid_options"
    classification: Literal["preference", "context_update", "policy_override"] = "preference"
    context: str = ""
    elicitation_action: Literal["accept", "delegate", "decline", "cancel", "unsupported", "pending", "malformed"] = "pending"
    provenance: str = "user"

    @model_validator(mode="after")
    def normalize_selection(self) -> "UserDecision":
        if len(self.selected_outcome_value) > 500:
            self.selected_outcome_value = ""
        if self.elicitation_action == "delegate":
            self.selection_kind = "council_delegation"
            self.selected_option_id = ""
            self.selected_outcome_value = ""
        elif self.elicitation_action == "accept" and self.selected_option_id:
            self.selection_kind = "outcome"
        elif self.elicitation_action != "accept":
            self.selection_kind = "none"
            self.selected_option_id = ""
            self.selected_outcome_value = ""
        return self


class Reconsideration(DomainModel):
    issue_id: str
    role_id: str
    trigger_decision_id: str
    previous_position: RolePosition | None = None
    revised_position: RolePosition | None = None
    changed: bool = False
    status: Literal["requested", "completed", "skipped", "failed"] = "completed"
    reason_code: str = ""


class ReconsiderationProvenance(DomainModel):
    requested_role_ids: list[str] = Field(default_factory=list)
    completed_role_ids: list[str] = Field(default_factory=list)
    skipped_role_ids: list[str] = Field(default_factory=list)
    failed_role_ids: list[str] = Field(default_factory=list)

    @model_validator(mode="after")
    def deduplicate_roles(self) -> "ReconsiderationProvenance":
        for name in (
            "requested_role_ids",
            "completed_role_ids",
            "skipped_role_ids",
            "failed_role_ids",
        ):
            setattr(self, name, list(dict.fromkeys(getattr(self, name)))[:8])
        return self


class ReviewBriefV2(DomainModel):
    domain: str = "unspecified"
    content_type: str = "unspecified"
    location: str = ""
    audience: str = ""
    tone_goal: str = ""
    primary_focus: str = ""
    usage_context: str = ""
    assumptions: list[str] = Field(default_factory=list)
    context_confidence: ContextConfidence = "minimal"
    field_provenance: dict[str, FieldProvenance] = Field(default_factory=dict)

    @model_validator(mode="after")
    def bound_brief(self) -> "ReviewBriefV2":
        bounds = {
            "domain": 120,
            "content_type": 80,
            "location": 160,
            "audience": 160,
            "tone_goal": 160,
            "primary_focus": 160,
            "usage_context": 240,
        }
        for name, limit in bounds.items():
            setattr(self, name, getattr(self, name)[:limit])
        self.assumptions = list(dict.fromkeys(item[:240] for item in self.assumptions if item))[:6]
        allowed = set(bounds) | {"context_confidence"}
        self.field_provenance = {
            key: value for key, value in self.field_provenance.items() if key in allowed
        }
        return self


class BriefingInteraction(DomainModel):
    requested: bool = False
    action: Literal["accept", "decline", "cancel", "unsupported", "malformed", "error", "skipped"] = "skipped"
    asked_fields: list[str] = Field(default_factory=list)
    accepted_answers: dict[str, str] = Field(default_factory=dict)
    answer_provenance: dict[str, FieldProvenance] = Field(default_factory=dict)
    retry_hint: str = ""

    @model_validator(mode="after")
    def bound_interaction(self) -> "BriefingInteraction":
        self.asked_fields = list(dict.fromkeys(item[:64] for item in self.asked_fields if item))[:6]
        allowed = set(self.asked_fields)
        self.accepted_answers = {
            key: value[:240]
            for key, value in self.accepted_answers.items()
            if key in allowed and isinstance(value, str) and value.strip()
        }
        self.answer_provenance = {
            key: value for key, value in self.answer_provenance.items() if key in self.accepted_answers
        }
        self.retry_hint = self.retry_hint[:240]
        return self


class ContextGapV2(DomainModel):
    gap_id: str
    question: str
    materiality: str
    affected_role_ids: list[str] = Field(default_factory=list)
    source_role_id: str = ""
    provenance: Literal["model", "system"] = "model"
    disposition: Literal["unanswered", "answered", "suppressed"] = "unanswered"
    reason: str = ""
    answer: str = ""

    @model_validator(mode="after")
    def bound_gap(self) -> "ContextGapV2":
        self.gap_id = self.gap_id[:64]
        self.question = self.question[:240]
        self.materiality = self.materiality[:240]
        self.affected_role_ids = list(dict.fromkeys(self.affected_role_ids))[:8]
        self.source_role_id = self.source_role_id[:64]
        self.reason = self.reason[:160]
        self.answer = self.answer[:240]
        if not self.question or not self.materiality:
            self.disposition = "suppressed"
            self.reason = self.reason or "invalid_gap"
            self.answer = ""
        if self.disposition != "answered":
            self.answer = ""
        return self


class ContextGapInteraction(DomainModel):
    requested: bool = False
    action: Literal["accept", "decline", "cancel", "unsupported", "malformed", "error", "skipped"] = "skipped"
    asked_gap_ids: list[str] = Field(default_factory=list)
    answered_gap_ids: list[str] = Field(default_factory=list)
    asked_count: int = Field(default=0, ge=0, le=2)
    answered_count: int = Field(default=0, ge=0, le=2)

    @model_validator(mode="after")
    def bound_gap_interaction(self) -> "ContextGapInteraction":
        self.asked_gap_ids = list(dict.fromkeys(self.asked_gap_ids))[:2]
        self.answered_gap_ids = [item for item in dict.fromkeys(self.answered_gap_ids) if item in self.asked_gap_ids][:2]
        self.asked_count = max(self.asked_count, len(self.asked_gap_ids))
        self.answered_count = max(self.answered_count, len(self.answered_gap_ids))
        self.answered_count = min(self.answered_count, self.asked_count)
        return self


class PhaseReconsiderationProvenance(ReconsiderationProvenance):
    change_effects: list[str] = Field(default_factory=list)

    @field_validator("change_effects")
    @classmethod
    def bound_effects(cls, value: list[str]) -> list[str]:
        return list(dict.fromkeys(item[:240] for item in value if item))[:8]


PhaseName = Literal[
    "briefing", "preflight", "planning", "independent_review", "blind_spot_mapping",
    "context_gap", "context_reconsideration", "discussion", "outcome_decision",
    "outcome_reconsideration", "policy_gate", "adjudication", "digest_construction",
]


class PhaseRecord(DomainModel):
    phase: PhaseName
    disposition: str = "completed"
    counts: dict[str, int] = Field(default_factory=dict)
    summary: str = ""

    @model_validator(mode="after")
    def bound_phase(self) -> "PhaseRecord":
        self.disposition = self.disposition[:64]
        self.counts = {
            key[:48]: max(0, min(int(value), 10_000))
            for key, value in list(self.counts.items())[:8]
            if isinstance(value, int) and not isinstance(value, bool)
        }
        self.summary = self.summary[:240]
        return self


class PhaseTrace(DomainModel):
    phases: list[PhaseRecord] = Field(default_factory=list)

    @field_validator("phases")
    @classmethod
    def bound_phases(cls, value: list[PhaseRecord]) -> list[PhaseRecord]:
        return value[:13]


class RoleLens(DomainModel):
    role_id: str
    perspective: str = ""
    evidence: list[str] = Field(default_factory=list)
    disposition: str = ""

    @model_validator(mode="after")
    def bound_lens(self) -> "RoleLens":
        self.role_id = self.role_id[:64]
        self.perspective = self.perspective[:240]
        self.evidence = list(dict.fromkeys(item[:240] for item in self.evidence if item))[:4]
        self.disposition = self.disposition[:120]
        return self


class MinorityReport(DomainModel):
    dissent: str = ""
    decisive_condition: str = ""
    role_ids: list[str] = Field(default_factory=list)

    @model_validator(mode="after")
    def bound_minority(self) -> "MinorityReport":
        self.dissent = self.dissent[:240]
        self.decisive_condition = self.decisive_condition[:240]
        self.role_ids = list(dict.fromkeys(self.role_ids))[:8]
        return self


class ProcessDigestV2(DomainModel):
    case_brief: list[str] = Field(default_factory=list)
    assumptions_context_confidence: list[str] = Field(default_factory=list)
    blind_spots: list[str] = Field(default_factory=list)
    role_lenses: list[RoleLens] = Field(default_factory=list)
    consensus: list[str] = Field(default_factory=list)
    minority_report: MinorityReport = Field(default_factory=MinorityReport)
    material_disagreements: list[str] = Field(default_factory=list)
    context_gaps_answers: list[str] = Field(default_factory=list)
    user_decisions: list[str] = Field(default_factory=list)
    reconsideration_changes: list[str] = Field(default_factory=list)
    editor_synthesis: list[str] = Field(default_factory=list)
    execution_checklist_final_disposition: list[str] = Field(default_factory=list)

    @model_validator(mode="after")
    def bound_digest(self) -> "ProcessDigestV2":
        list_fields = (
            "case_brief", "assumptions_context_confidence", "blind_spots", "consensus",
            "material_disagreements", "context_gaps_answers", "user_decisions",
            "reconsideration_changes", "editor_synthesis", "execution_checklist_final_disposition",
        )
        for name in list_fields:
            items = getattr(self, name)
            setattr(self, name, list(dict.fromkeys(item[:240] for item in items if item))[:8])
        self.role_lenses = self.role_lenses[:8]
        return self


class EffectiveTask(DomainModel):
    content_type: str = "unspecified"
    audience: str = ""
    mode: ReviewMode = "standard"
    material_rule_context: list[str] = Field(default_factory=list)

    @model_validator(mode="after")
    def bound_snapshot(self) -> "EffectiveTask":
        self.content_type = self.content_type[:80]
        self.audience = self.audience[:160]
        self.material_rule_context = [item[:160] for item in self.material_rule_context[:8]]
        return self


class DeliberationSummary(DomainModel):
    consensus: list[str] = Field(default_factory=list)
    material_disagreement: list[str] = Field(default_factory=list)
    evidence_basis: list[str] = Field(default_factory=list)
    user_selection: str = ""
    delegated_to_council: bool = False
    final_outcome: str = ""
    reconsidered_role_ids: list[str] = Field(default_factory=list)
    reconsideration_effect: str = ""

    @model_validator(mode="after")
    def bound_summary(self) -> "DeliberationSummary":
        for name in ("consensus", "material_disagreement", "evidence_basis"):
            setattr(self, name, [item[:240] for item in getattr(self, name)[:8]])
        self.user_selection = self.user_selection[:500]
        self.final_outcome = self.final_outcome[:500]
        self.reconsideration_effect = self.reconsideration_effect[:240]
        self.reconsidered_role_ids = list(dict.fromkeys(self.reconsidered_role_ids))[:8]
        return self


class DecisionTraceEntry(DomainModel):
    issue_id: str
    decision: str
    selected_option_id: str = ""
    outcome: Literal["valid_user_choice", "council_fallback", "human_review"] = "human_review"
    basis: list[str] = Field(default_factory=list)
    rejected_options: list[dict[str, str]] = Field(default_factory=list)


class DecisionTrace(DomainModel):
    entries: list[DecisionTraceEntry] = Field(default_factory=list)


class RuntimeMetadata(DomainModel):
    sampling_calls: int = Field(default=0, ge=0)
    elicitation_calls: int = Field(default=0, ge=0)
    elicitation_actions: list[str] = Field(default_factory=list)
    parse_failures: int = Field(default=0, ge=0)
    fallbacks: list[str] = Field(default_factory=list)
    elapsed_ms: int = Field(default=0, ge=0)
    sample_budget: int = Field(default=13, ge=0, le=18)
    reviewer_samples_successful: int = Field(default=0, ge=0, le=8)
    reviewer_samples_unavailable: int = Field(default=0, ge=0, le=8)
    reviewer_coverage: Literal["full", "partial", "none", "not_applicable"] = "not_applicable"
    briefing_elicitation_calls: int = Field(default=0, ge=0)
    briefing_elicitation_actions: list[str] = Field(default_factory=list)
    context_gap_elicitation_calls: int = Field(default=0, ge=0)
    context_gap_elicitation_actions: list[str] = Field(default_factory=list)
    outcome_elicitation_calls: int = Field(default=0, ge=0)
    outcome_elicitation_actions: list[str] = Field(default_factory=list)
    package_version: str = "0.6.0"
    diagnostic_build: str = "guided-deliberation-v4"


class ReviewTaskV2(DomainModel):
    source_text: str = ""
    candidate_translation: str = ""
    source_language: str = "auto"
    target_language: str = "zh-CN"
    content_type: str = "unspecified"
    context: str = ""
    audience: str = ""
    mode: ReviewMode = "standard"
    output_mode: Literal["review_only", "with_snippets", "full_rewrite"] = "review_only"
    interactive_mode: Literal["auto", "off", "required"] = "auto"
    briefing_mode: BriefingMode = "auto"
    decision_fallback: Literal["council_adjudication", "return_pending"] = "council_adjudication"
    trace_level: TraceLevel = "summary"
    history_mode: HistoryMode = "full"
    term_glossary: str = ""
    style_guide: str = ""
    project_rules: str = ""
    brand_guidelines: str = ""
    technical_constraints: str = ""
    do_not_translate_literals: list[str] = Field(default_factory=list)
    hard_constraints: list[str] = Field(default_factory=list)
    reference_translations: str = ""
    known_exceptions: str = ""
    notes: str = ""


class ChiefEditorDecisionV2(DomainModel):
    publishability: Literal["可发布", "修改后可发布", "需人工复核"] = "需人工复核"
    must_fix: list[str] = Field(default_factory=list)
    should_fix: list[str] = Field(default_factory=list)
    optional_improvements: list[str] = Field(default_factory=list)
    terminology_decisions: list[str] = Field(default_factory=list)
    conflict_resolutions: list[str] = Field(default_factory=list)
    execution_order: list[str] = Field(default_factory=list)
    decision_rationale: str = ""
    review_needed: Literal["是", "否"] = "是"
    review_reason: str = ""
    suggested_translation: str | None = None

    @model_validator(mode="after")
    def bound_execution_output(self) -> "ChiefEditorDecisionV2":
        for name in (
            "must_fix",
            "should_fix",
            "optional_improvements",
            "terminology_decisions",
            "conflict_resolutions",
            "execution_order",
        ):
            setattr(self, name, [item[:240] for item in getattr(self, name)[:12]])
        self.decision_rationale = self.decision_rationale[:1_000]
        self.review_reason = self.review_reason[:500]
        if self.suggested_translation is not None:
            self.suggested_translation = self.suggested_translation[:12_000]
        return self


class ReviewRecordV2(DomainModel):
    schema_version: Literal["2.0", "2.1", "2.2"] = "2.2"
    review_id: str
    parent_review_id: str | None = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    completed_at: datetime | None = None
    task: ReviewTaskV2
    input_diagnostics: InputDiagnostics = Field(default_factory=InputDiagnostics)
    runtime_metadata: RuntimeMetadata = Field(default_factory=RuntimeMetadata)
    council_plan: CouncilPlan = Field(default_factory=CouncilPlan)
    preflight: PreflightResult = Field(default_factory=PreflightResult)
    independent_reviews: list[dict[str, Any]] = Field(default_factory=list)
    issue_clusters: list[IssueCluster] = Field(default_factory=list)
    discussion_rounds: list[DiscussionRound] = Field(default_factory=list)
    decision_points: list[DecisionPoint] = Field(default_factory=list)
    user_decisions: list[UserDecision] = Field(default_factory=list)
    reconsiderations: list[Reconsideration] = Field(default_factory=list)
    reconsideration_provenance: ReconsiderationProvenance = Field(default_factory=ReconsiderationProvenance)
    effective_brief: ReviewBriefV2 = Field(default_factory=ReviewBriefV2)
    briefing_interaction: BriefingInteraction = Field(default_factory=BriefingInteraction)
    context_gaps: list[ContextGapV2] = Field(default_factory=list)
    context_gap_interaction: ContextGapInteraction = Field(default_factory=ContextGapInteraction)
    context_reconsideration_provenance: PhaseReconsiderationProvenance = Field(default_factory=PhaseReconsiderationProvenance)
    outcome_reconsideration_provenance: PhaseReconsiderationProvenance = Field(default_factory=PhaseReconsiderationProvenance)
    policy_gate_result: dict[str, Any] = Field(default_factory=dict)
    chief_editor_decision: ChiefEditorDecisionV2 = Field(default_factory=ChiefEditorDecisionV2)
    decision_trace: DecisionTrace = Field(default_factory=DecisionTrace)
    status: Literal[
        "COMPLETED", "COMPLETED_WITH_FALLBACK", "NEEDS_HUMAN_REVIEW", "RETURNED_PENDING"
    ] = "NEEDS_HUMAN_REVIEW"
    fallback_reason: str = ""
    effective_task: EffectiveTask = Field(default_factory=EffectiveTask)
    deliberation_summary: DeliberationSummary = Field(default_factory=DeliberationSummary)
    degraded: bool = False
    warnings: list[str] = Field(default_factory=list)
    phase_trace: PhaseTrace = Field(default_factory=PhaseTrace)
    process_digest: ProcessDigestV2 = Field(default_factory=ProcessDigestV2)
    display_report: str = ""
    version_metadata: dict[str, str] = Field(default_factory=lambda: {
        "package_version": "0.6.0",
        "diagnostic_build": "guided-deliberation-v4",
        "record_schema": "2.2",
    })

    @field_validator("decision_points")
    @classmethod
    def cap_decision_points(cls, value: list[DecisionPoint]) -> list[DecisionPoint]:
        return value[:3]

    @field_validator("warnings")
    @classmethod
    def bound_warnings(cls, value: list[str]) -> list[str]:
        return list(dict.fromkeys(item[:240] for item in value))[:8]

    @field_validator("context_gaps")
    @classmethod
    def bound_context_gaps(cls, value: list[ContextGapV2]) -> list[ContextGapV2]:
        return value[:16]

    @field_validator("display_report")
    @classmethod
    def bound_display_report(cls, value: str) -> str:
        return value[:8_000]
