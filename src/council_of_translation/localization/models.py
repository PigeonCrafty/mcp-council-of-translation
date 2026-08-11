"""Versioned domain models for the structured deliberation workflow.

Models that can be populated from sampled output use conservative defaults.  In
particular, sampled findings are evidence only: they cannot manufacture hard
constraints or deterministic blockers.
"""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator


ReviewMode = Literal["lightweight", "standard", "strict"]
HistoryMode = Literal["off", "metadata", "full"]
TraceLevel = Literal["summary", "full"]
ConstraintTier = Literal["hard", "contextual", "preference", "advisory"]
Severity = Literal["critical", "major", "minor", "preference"]
EvidenceOrigin = Literal["caller", "preflight", "model", "user", "system"]


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
        # Sampled prose cannot escalate itself into a hard rule or blocker.
        if data.get("evidence_origin", "model") == "model":
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
    sample_budget: int = Field(default=10, ge=0, le=14)
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
    positions: list[RolePosition] = Field(default_factory=list)
    evidence: list[str] = Field(default_factory=list)
    immutable_hard_constraints: list[str] = Field(default_factory=list)
    severity: Severity = "minor"
    constraint_tier: ConstraintTier = "advisory"
    blocking: bool = False
    consensus_status: Literal["consensus", "disputed", "insufficient_evidence"] = "insufficient_evidence"
    needs_user_input: bool = False


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
    label: str
    description: str = ""
    valid: bool = True
    invalid_reason: str = ""


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
        self.options = self.options[:8]
        valid_ids = {option.option_id for option in self.options if option.valid}
        if self.recommended_option_id not in valid_ids:
            self.recommended_option_id = ""
        if self.fallback_option_id not in valid_ids:
            self.fallback_option_id = ""
        return self


class UserDecision(DomainModel):
    decision_id: str
    selected_option_id: str = ""
    authority_mode: Literal["decisive_within_valid_options", "advisory", "policy_override"] = "decisive_within_valid_options"
    classification: Literal["preference", "context_update", "policy_override"] = "preference"
    context: str = ""
    elicitation_action: Literal["accept", "decline", "cancel", "unsupported", "pending", "malformed"] = "pending"
    provenance: str = "user"


class Reconsideration(DomainModel):
    issue_id: str
    role_id: str
    trigger_decision_id: str
    previous_position: RolePosition | None = None
    revised_position: RolePosition | None = None
    changed: bool = False


class DecisionTraceEntry(DomainModel):
    issue_id: str
    decision: str
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
    sample_budget: int = Field(default=10, ge=0, le=14)
    package_version: str = "0.4.0"
    diagnostic_build: str = "structured-deliberation-v2"


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


class ReviewRecordV2(DomainModel):
    schema_version: Literal["2.0"] = "2.0"
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
    policy_gate_result: dict[str, Any] = Field(default_factory=dict)
    chief_editor_decision: ChiefEditorDecisionV2 = Field(default_factory=ChiefEditorDecisionV2)
    decision_trace: DecisionTrace = Field(default_factory=DecisionTrace)
    status: Literal[
        "COMPLETED", "COMPLETED_WITH_FALLBACK", "NEEDS_HUMAN_REVIEW", "RETURNED_PENDING"
    ] = "NEEDS_HUMAN_REVIEW"
    fallback_reason: str = ""
    version_metadata: dict[str, str] = Field(default_factory=lambda: {
        "package_version": "0.4.0",
        "diagnostic_build": "structured-deliberation-v2",
        "record_schema": "2.0",
    })

    @field_validator("decision_points")
    @classmethod
    def cap_decision_points(cls, value: list[DecisionPoint]) -> list[DecisionPoint]:
        return value[:3]
