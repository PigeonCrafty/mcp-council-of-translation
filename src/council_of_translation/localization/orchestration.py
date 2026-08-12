"""V2 structured deliberation orchestration independent of FastMCP Context."""

from __future__ import annotations

from datetime import datetime, timezone
import json
import re
from time import perf_counter
from typing import Any, Iterable, Literal

from pydantic import Field, ValidationError, create_model

from council_of_translation.localization.clustering import cluster_findings
from council_of_translation.localization.deliberation import (
    SampleBudget,
    apply_discussion_updates,
    build_decision_points,
    normalize_discussion_round,
    select_discussion_issues,
)
from council_of_translation.localization.models import (
    FindingV2,
    DeliberationSummary,
    EffectiveTask,
    InputDiagnostics,
    IssueCluster,
    Reconsideration,
    ReconsiderationProvenance,
    ReviewRecordV2,
    ReviewTaskV2,
    RolePosition,
    UserDecision,
    option_id_for_action,
)
from council_of_translation.localization.persistence import ReviewStore, build_review_id
from council_of_translation.localization.policy import build_chief_decision, policy_gate, valid_options
from council_of_translation.localization.preflight import run_preflight
from council_of_translation.localization.prompt_builders import (
    build_discussion_prompt,
    build_reconsideration_prompt,
    build_v2_reviewer_prompt,
)
from council_of_translation.localization.roles import (
    ROLE_REGISTRY,
    build_council_plan,
    normalize_content_type,
)
from council_of_translation.localization.runtime import (
    ElicitationResult,
    ModelExecutor,
    RuntimeEvent,
    RuntimeTelemetry,
    UserInteractionGateway,
)


def _json_object(text: str) -> dict[str, Any]:
    cleaned = text.strip()
    if cleaned.startswith("```"):
        cleaned = re.sub(r"^```(?:json)?\s*", "", cleaned, flags=re.IGNORECASE)
        cleaned = re.sub(r"\s*```$", "", cleaned)
    decoder = json.JSONDecoder()
    try:
        value, _ = decoder.raw_decode(cleaned[cleaned.find("{") :])
    except (json.JSONDecodeError, ValueError) as exc:
        raise ValueError("sample did not contain a JSON object") from exc
    if not isinstance(value, dict):
        raise ValueError("sample JSON must be an object")
    return value


def _telemetry_for(executor: ModelExecutor, gateway: UserInteractionGateway, budget: int) -> RuntimeTelemetry:
    executor_telemetry = getattr(executor, "telemetry", None)
    gateway_telemetry = getattr(gateway, "telemetry", None)
    if isinstance(executor_telemetry, RuntimeTelemetry):
        executor_telemetry.sample_budget = budget
        if gateway_telemetry is not executor_telemetry and hasattr(gateway, "telemetry"):
            setattr(gateway, "telemetry", executor_telemetry)
        return executor_telemetry
    telemetry = RuntimeTelemetry(sample_budget=budget)
    if hasattr(executor, "telemetry"):
        setattr(executor, "telemetry", telemetry)
    if hasattr(gateway, "telemetry"):
        setattr(gateway, "telemetry", telemetry)
    return telemetry


async def _sample_json(
    executor: ModelExecutor,
    telemetry: RuntimeTelemetry,
    budget: SampleBudget,
    prompt: str,
    *,
    max_tokens: int,
) -> dict[str, Any] | None:
    budget.consume()
    result = await executor.sample(prompt, temperature=0.2, max_tokens=max_tokens)
    if result.status != "success":
        telemetry.record(RuntimeEvent("fallback", f"sample_{result.status}", detail=result.error))
        return None
    try:
        return _json_object(result.text)
    except ValueError as exc:
        telemetry.record(RuntimeEvent("parse_failure", "invalid_json", detail=str(exc)))
        return None


def _review_findings(
    raw: dict[str, Any] | None,
    role_id: str,
) -> tuple[str, list[FindingV2], str]:
    """Validate one reviewer envelope; any malformed entry invalidates the sample."""
    if raw is None:
        return "评审采样不可用；未将缺失输出升级为阻断项。", [], "runtime_unavailable"
    if "role_feedback" not in raw or not isinstance(raw["role_feedback"], str):
        return "评审响应结构无效；未将其视为完成评审。", [], "invalid_role_feedback"
    if "findings" not in raw or not isinstance(raw["findings"], list):
        return "评审响应结构无效；未将其视为完成评审。", [], "invalid_findings_container"
    if len(raw["findings"]) > 5:
        return "评审响应包含过多 findings；未将其视为完成评审。", [], "too_many_findings"

    role_feedback = raw["role_feedback"][:2_000]
    findings: list[FindingV2] = []
    for item in raw["findings"]:
        if not isinstance(item, dict):
            return "评审响应包含无效 finding；已丢弃该样本的全部 findings。", [], "invalid_finding_entry"
        try:
            finding = FindingV2.model_validate(
                {
                    **item,
                    "finding_id": "",
                    "agent_name": role_id,
                    "role_perspective": ROLE_REGISTRY[role_id].display_name,
                    "evidence_origin": "model",
                    "blocking": False,
                }
            )
        except (ValidationError, TypeError, ValueError):
            return "评审响应包含无效 finding；已丢弃该样本的全部 findings。", [], "invalid_finding_value"
        if not (finding.problem or finding.action or finding.proposed_value):
            return "评审响应包含空 finding；已丢弃该样本的全部 findings。", [], "inert_finding"
        findings.append(finding)

    if not findings and not role_feedback.strip():
        return "评审响应缺少有效反馈；未将其视为完成评审。", [], "empty_reviewer_response"
    return role_feedback, findings, ""


def _delegate_form_value(decision_id: str) -> str:
    del decision_id
    return "暂不决定，由 Council 裁决"


def _bounded_form_value(prefix: str, label: str, suffix: str = "") -> str:
    maximum = 64
    available = max(1, maximum - len(prefix) - len(suffix))
    return f"{prefix}{label[:available]}{suffix}"


def _form_mapping(point: Any) -> dict[str, Any | None]:
    ordered = sorted(
        [option for option in point.options if option.valid and not option.is_delegation],
        key=lambda option: not option.is_current_candidate,
    )[:3]
    mapping: dict[str, Any | None] = {}
    for option in ordered:
        prefix = "保留：" if option.is_current_candidate else "改为："
        label = (option.label or option.outcome_value or "未命名结果").strip()
        value = _bounded_form_value(prefix, label)
        collision = 2
        while value in mapping:
            suffix = f"（选项 {collision}）"
            value = _bounded_form_value(prefix, label, suffix)
            collision += 1
        mapping[value] = option
    mapping[_delegate_form_value(point.decision_id)] = None
    return mapping


def _interaction_form(decision_points: list) -> type:
    fields: dict[str, tuple[Any, Any]] = {}
    for point in decision_points[:3]:
        mapping = _form_mapping(point)
        option_type = Literal.__getitem__(tuple(mapping))
        mapping = "; ".join(
            f"{value} = {option.label if option else '暂不决定，由 Council 裁决'}"
            f"（{option.description if option else '由证据加权 Position Matrix 裁决'}）"
            for value, option in _form_mapping(point).items()
        )
        fields[point.decision_id] = (
            option_type,
            Field(
                title=point.question,
                description=f"{point.question} 可选值：{mapping}",
            ),
        )
    return create_model("CouncilDecisionForm", **fields)


def _interaction_message(decision_points: list) -> str:
    lines = ["Council 发现以下均满足硬约束的选择，请在一个表单中决定："]
    for point in decision_points[:3]:
        lines.append(f"- {point.question}")
        for option in _form_mapping(point).values():
            if option is not None:
                lines.append(
                    f"  - {option.label} — {option.description or option.label}"
                )
        lines.append("  - 暂不决定，由 Council 裁决 — 由证据加权 Position Matrix 裁决")
    return "\n".join(lines)


def _decisions_from_elicitation(decision_points: list, result: ElicitationResult) -> list[UserDecision]:
    points = decision_points[:3]
    if result.action == "accept":
        expected = {point.decision_id for point in points}
        malformed = (
            set(result.data) != expected
            or any(not isinstance(value, str) for value in result.data.values())
        )
        if not malformed:
            malformed = any(
                result.data[point.decision_id] not in _form_mapping(point)
                for point in points
            )
        if malformed:
            return [
                UserDecision(decision_id=point.decision_id, elicitation_action="malformed")
                for point in points
            ]
    decisions: list[UserDecision] = []
    for point in points:
        selected = result.data.get(point.decision_id, "") if result.action == "accept" else ""
        action = result.action
        if action == "error":
            action = "malformed"
        option = _form_mapping(point).get(selected) if action == "accept" else None
        if action == "accept" and selected == _delegate_form_value(point.decision_id):
            action = "delegate"
        decisions.append(
            UserDecision(
                decision_id=point.decision_id,
                selected_option_id=option.option_id if option is not None else "",
                selected_outcome_value=option.outcome_value or option.label if option is not None else "",
                elicitation_action=action,
                provenance="mcp_elicitation",
            )
        )
    return decisions


def _fallback_decisions(decision_points: list, action: str) -> list[UserDecision]:
    normalized = action if action in {"decline", "cancel", "unsupported", "pending", "malformed"} else "malformed"
    return [UserDecision(decision_id=point.decision_id, elicitation_action=normalized) for point in decision_points]


def _reconstruct_candidate(
    task: ReviewTaskV2,
    cluster: IssueCluster,
    option: Any,
) -> tuple[str | None, str]:
    """Build the complete candidate for one issue-local option, or refuse safely."""
    if option.is_current_candidate:
        return task.candidate_translation, "unchanged_candidate"
    anchor = cluster.outcome_anchor
    if not anchor:
        return None, "missing_candidate_anchor"
    occurrences = task.candidate_translation.count(anchor)
    if occurrences == 0:
        return None, "missing_candidate_anchor"
    if occurrences != 1:
        return None, "ambiguous_candidate_anchor"
    return task.candidate_translation.replace(anchor, option.outcome_value, 1), "reconstructed_candidate"


_DECISION_SUPPRESSION_REASONS = {
    "missing_candidate_anchor",
    "ambiguous_candidate_anchor",
}


def _bounded_decision_suppressions(values: Any) -> list[dict[str, str]]:
    """Keep only bounded, content-free reconstruction suppression provenance."""
    if not isinstance(values, list):
        return []
    suppressions: list[dict[str, str]] = []
    seen: set[tuple[str, str, str]] = set()
    for value in values:
        if not isinstance(value, dict):
            continue
        issue_id = value.get("issue_id", "")
        decision_id = value.get("decision_id", "")
        reason_code = value.get("reason_code", "")
        if (
            not isinstance(issue_id, str)
            or not isinstance(decision_id, str)
            or not isinstance(reason_code, str)
            or reason_code not in _DECISION_SUPPRESSION_REASONS
            or re.fullmatch(r"issue_[0-9a-f]{12}", issue_id) is None
            or re.fullmatch(r"decision_[0-9a-f]{12}", decision_id) is None
        ):
            continue
        key = (issue_id, decision_id, reason_code)
        if key in seen:
            continue
        seen.add(key)
        suppressions.append({
            "issue_id": issue_id,
            "decision_id": decision_id,
            "reason_code": reason_code,
        })
        if len(suppressions) >= 8:
            break
    return suppressions


def _suppression_warnings(suppressions: list[dict[str, str]]) -> list[str]:
    return list(dict.fromkeys(
        f"decision_suppressed:{item['reason_code']}"
        for item in suppressions
    ))


def _validate_outcome_options(
    decision_points: list[Any],
    task: ReviewTaskV2,
    clusters: list[IssueCluster],
    *,
    suppression_provenance: list[dict[str, str]] | None = None,
) -> list[Any]:
    """Apply deterministic caller/preflight constraints to every outcome."""
    validated_points: list[Any] = []
    clusters_by_issue = {cluster.issue_id: cluster for cluster in clusters}
    for point in decision_points[:3]:
        cluster = clusters_by_issue.get(point.issue_id)
        if cluster is None:
            continue
        options = []
        for option in point.options[:3]:
            candidate, reconstruction = _reconstruct_candidate(task, cluster, option)
            if candidate is None:
                if reconstruction in _DECISION_SUPPRESSION_REASONS:
                    suppression = {
                        "issue_id": point.issue_id,
                        "decision_id": point.decision_id,
                        "reason_code": reconstruction,
                    }
                    if suppression_provenance is not None:
                        suppression_provenance[:] = _bounded_decision_suppressions([
                            *suppression_provenance,
                            suppression,
                        ])
                options.append(option.model_copy(update={
                    "valid": False,
                    "invalid_reason": option.invalid_reason or reconstruction,
                    "policy_basis": list(dict.fromkeys([
                        *option.policy_basis,
                        reconstruction,
                    ])),
                }))
                continue
            result = run_preflight(
                task.source_text,
                candidate,
                do_not_translate=task.do_not_translate_literals,
                hard_constraints=task.hard_constraints,
            )
            blocking_checks = [
                check.check_id
                for check in result.checks
                if check.blocking and check.status == "fail"
            ]
            options.append(option.model_copy(update={
                "valid": option.valid and not blocking_checks,
                "invalid_reason": option.invalid_reason
                or ("deterministic_constraint:" + ",".join(blocking_checks) if blocking_checks else ""),
                "policy_basis": list(dict.fromkeys([
                    *option.policy_basis,
                    reconstruction,
                    *(["deterministic_preflight_passed"] if not blocking_checks else blocking_checks),
                ])),
            }))
        valid = [option for option in options if option.valid and option.outcome_value]
        if len(valid) < 2:
            continue
        validated_points.append(point.model_copy(update={
            "options": options,
            "recommended_option_id": (
                point.recommended_option_id
                if any(option.option_id == point.recommended_option_id for option in valid)
                else valid[0].option_id
            ),
            "fallback_option_id": (
                point.fallback_option_id
                if any(option.option_id == point.fallback_option_id for option in valid)
                else valid[0].option_id
            ),
        }))
    return validated_points


def _effective_task(task: ReviewTaskV2) -> EffectiveTask:
    material_context: list[str] = []
    for name in (
        "context",
        "term_glossary",
        "style_guide",
        "project_rules",
        "brand_guidelines",
        "technical_constraints",
        "reference_translations",
        "known_exceptions",
    ):
        if getattr(task, name):
            material_context.append(f"{name}:provided")
    if task.do_not_translate_literals:
        material_context.append(f"do_not_translate_literals:{len(task.do_not_translate_literals)}")
    for constraint in task.hard_constraints:
        kind = constraint.partition(":")[0].strip() or "hard_constraint"
        material_context.append(f"hard_constraint:{kind[:80]}")
    return EffectiveTask(
        content_type=normalize_content_type(task.content_type),
        audience=task.audience,
        mode=task.mode,
        material_rule_context=list(dict.fromkeys(material_context)),
    )


def _deliberation_summary(
    clusters: list[IssueCluster],
    decisions: list[UserDecision],
    trace: Any,
    provenance: ReconsiderationProvenance,
    reconsiderations: list[Reconsideration] | None = None,
) -> DeliberationSummary:
    consensus = [cluster.topic for cluster in clusters if cluster.consensus_status == "consensus"]
    if not clusters:
        consensus = ["no_material_issues_identified"]
    disagreements = [cluster.topic for cluster in clusters if cluster.consensus_status == "disputed"]
    evidence_basis: list[str] = []
    if any(cluster.category == "integrity" for cluster in clusters):
        evidence_basis.append("deterministic_preflight")
    if clusters:
        evidence_basis.append("structured_role_evidence")
    if any(decision.elicitation_action == "accept" for decision in decisions):
        evidence_basis.append("valid_user_selection")
    if any(decision.elicitation_action == "delegate" for decision in decisions):
        evidence_basis.append("council_position_matrix")
    selected_values = [
        decision.selected_outcome_value
        for decision in decisions
        if decision.elicitation_action == "accept" and decision.selected_outcome_value
    ]
    final_values = [
        entry.decision
        for entry in trace.entries
        if entry.decision and entry.outcome != "human_review"
    ]
    return DeliberationSummary(
        consensus=list(dict.fromkeys(consensus)),
        material_disagreement=list(dict.fromkeys(disagreements)),
        evidence_basis=list(dict.fromkeys(evidence_basis)),
        user_selection="；".join(dict.fromkeys(selected_values)),
        delegated_to_council=any(
            decision.elicitation_action == "delegate" for decision in decisions
        ),
        final_outcome="；".join(dict.fromkeys(final_values)),
        reconsidered_role_ids=provenance.completed_role_ids,
        reconsideration_effect=(
            f"completed={len(provenance.completed_role_ids)};"
            f"changed={sum(item.changed for item in (reconsiderations or []) if item.status == 'completed')};"
            f"unchanged={sum(not item.changed for item in (reconsiderations or []) if item.status == 'completed')}"
            if provenance.requested_role_ids
            else "not_requested"
        ),
    )


async def _reconsider(
    task: ReviewTaskV2,
    clusters: list[IssueCluster],
    decisions: list[UserDecision],
    executor: ModelExecutor,
    telemetry: RuntimeTelemetry,
    budget: SampleBudget,
) -> tuple[list[Reconsideration], ReconsiderationProvenance, list[str]]:
    points_by_issue = {f"decision_{cluster.issue_id.removeprefix('issue_')}": cluster for cluster in clusters}
    accepted = [decision for decision in decisions if decision.elicitation_action == "accept"]
    affected: dict[str, list[tuple[IssueCluster, UserDecision]]] = {}
    for decision in accepted:
        cluster = points_by_issue.get(decision.decision_id)
        if cluster is None:
            continue
        for position in cluster.positions:
            if (
                position.role_id in cluster.participant_role_ids
                and position.option_id
                and position.option_id != decision.selected_option_id
            ):
                affected.setdefault(position.role_id, []).append((cluster, decision))

    origin_rank = {"preflight": 5, "caller": 4, "user": 3, "system": 2, "model": 1}
    tier_rank = {"hard": 4, "contextual": 3, "preference": 2, "advisory": 1}
    category_relevance = {
        "integrity": {"technical_safety_reviewer": 5, "fidelity_reviewer": 4},
        "correctness": {"fidelity_reviewer": 5, "risk_ambiguity_reviewer": 4},
        "language_choice": {
            "terminology_reviewer": 5,
            "product_context_reviewer": 5,
            "ux_copy_reviewer": 5,
            "fluency_reviewer": 4,
            "brand_voice_reviewer": 3,
        },
    }

    for cluster in clusters:
        decision = next(
            (item for item in accepted if item.decision_id == f"decision_{cluster.issue_id.removeprefix('issue_')}"),
            None,
        )
        if decision is None:
            continue
        positions_by_role = {position.role_id: position for position in cluster.positions}
        relevance = category_relevance.get(cluster.category, {})
        for role_id in cluster.participant_role_ids:
            position = positions_by_role.get(role_id)
            materially_affected = (
                relevance.get(role_id, 0) >= 4
                and (position is None or position.stance == "accept_with_conditions")
            )
            if materially_affected:
                packets = affected.setdefault(role_id, [])
                if not any(issue.issue_id == cluster.issue_id for issue, _ in packets):
                    packets.append((cluster, decision))

    def role_rank(role_id: str) -> tuple[int, int, int, int, int, str]:
        positions = [
            position
            for issue, _ in affected[role_id]
            for position in issue.positions
            if position.role_id == role_id
        ]
        return (
            -max(
                (
                    category_relevance.get(issue.category, {}).get(role_id, 0)
                    for issue, _ in affected[role_id]
                ),
                default=0,
            ),
            -max((int(position.blocking) for position in positions), default=0),
            -max((tier_rank[position.constraint_tier] for position in positions), default=0),
            -max((origin_rank[position.evidence_origin] for position in positions), default=0),
            ROLE_REGISTRY.get(role_id, ROLE_REGISTRY["chief_editor"]).priority,
            role_id,
        )

    requested_role_ids = sorted(affected, key=role_rank)
    provenance = ReconsiderationProvenance(requested_role_ids=requested_role_ids)
    warnings: list[str] = []

    reconsiderations: list[Reconsideration] = []
    for index, role_id in enumerate(requested_role_ids):
        packets = affected[role_id]
        if index >= 3:
            provenance.skipped_role_ids.append(role_id)
            warnings.append(f"reconsideration_skipped_limit:{role_id}")
            for issue, decision in packets:
                previous = next((position for position in issue.positions if position.role_id == role_id), None)
                reconsiderations.append(Reconsideration(
                    issue_id=issue.issue_id,
                    role_id=role_id,
                    trigger_decision_id=decision.decision_id,
                    previous_position=previous,
                    revised_position=previous,
                    status="skipped",
                    reason_code="affected_role_limit",
                ))
            continue
        if budget.remaining <= 0 or role_id not in ROLE_REGISTRY:
            telemetry.record(RuntimeEvent("fallback", "reconsideration_budget_unavailable", detail=role_id))
            provenance.skipped_role_ids.append(role_id)
            warnings.append(f"reconsideration_skipped_budget:{role_id}")
            for issue, decision in packets:
                previous = next((position for position in issue.positions if position.role_id == role_id), None)
                reconsiderations.append(Reconsideration(
                    issue_id=issue.issue_id,
                    role_id=role_id,
                    trigger_decision_id=decision.decision_id,
                    previous_position=previous,
                    revised_position=previous,
                    status="skipped",
                    reason_code="budget_unavailable",
                ))
            continue
        issues = [packet[0] for packet in packets]
        role_decisions = [packet[1] for packet in packets]
        raw = await _sample_json(
            executor,
            telemetry,
            budget,
            build_reconsideration_prompt(task, ROLE_REGISTRY[role_id], issues, role_decisions),
            max_tokens=1_200,
        )
        raw_positions = raw.get("positions", []) if raw and isinstance(raw.get("positions", []), list) else []
        by_issue = {
            str(item.get("issue_id", "")): item
            for item in raw_positions
            if isinstance(item, dict)
        }
        role_results: list[Reconsideration] = []
        role_failed = raw is None
        for issue, decision in packets:
            previous = next((position for position in issue.positions if position.role_id == role_id), None)
            item = by_issue.get(issue.issue_id)
            revised = None
            valid_ids = {option_id_for_action(issue.issue_id, action) for action in issue.candidate_actions}
            if item is not None and str(item.get("option_id", "")) in valid_ids:
                try:
                    revised = RolePosition.model_validate(
                        {
                            **item,
                            "role_id": role_id,
                            "evidence_origin": "model",
                            "constraint_tier": "advisory",
                            "rule_refs": [],
                            "blocking": False,
                        }
                    )
                except (ValidationError, TypeError, ValueError):
                    revised = None
                if revised is not None:
                    issue.positions = [position for position in issue.positions if position.role_id != role_id] + [revised]
            if revised is None:
                role_failed = True
            role_results.append(
                Reconsideration(
                    issue_id=issue.issue_id,
                    role_id=role_id,
                    trigger_decision_id=decision.decision_id,
                    previous_position=previous,
                    revised_position=revised or previous,
                    changed=bool(revised and revised != previous),
                    status="completed" if revised is not None else "failed",
                    reason_code="" if revised is not None else "invalid_or_missing_reconsideration",
                )
            )
        reconsiderations.extend(role_results)
        if role_failed:
            provenance.failed_role_ids.append(role_id)
            warnings.append(f"reconsideration_failed:{role_id}")
            telemetry.record(RuntimeEvent("fallback", "reconsideration_failed", detail=role_id))
        else:
            provenance.completed_role_ids.append(role_id)
    return reconsiderations, ReconsiderationProvenance(
        requested_role_ids=provenance.requested_role_ids,
        completed_role_ids=provenance.completed_role_ids,
        skipped_role_ids=provenance.skipped_role_ids,
        failed_role_ids=provenance.failed_role_ids,
    ), warnings


async def run_structured_review(
    task: ReviewTaskV2,
    executor: ModelExecutor,
    gateway: UserInteractionGateway,
    *,
    store: ReviewStore | None = None,
    input_diagnostics: InputDiagnostics | None = None,
) -> ReviewRecordV2:
    started = perf_counter()
    plan = build_council_plan(task.mode, task.content_type, interactive_mode=task.interactive_mode)
    telemetry = _telemetry_for(executor, gateway, plan.sample_budget)
    budget = SampleBudget(task.mode)
    preflight = run_preflight(
        task.source_text,
        task.candidate_translation,
        do_not_translate=task.do_not_translate_literals,
        hard_constraints=task.hard_constraints,
    )

    independent_reviews: list[dict[str, Any]] = []
    all_findings: list[FindingV2] = []
    successful_reviewers = 0
    for role_id in plan.active_role_ids:
        raw = await _sample_json(
            executor,
            telemetry,
            budget,
            build_v2_reviewer_prompt(ROLE_REGISTRY[role_id], task, preflight),
            max_tokens=1_400,
        )
        feedback, findings, sample_error = _review_findings(raw, role_id)
        sample_status = "structured_success" if not sample_error else "unavailable"
        if raw is not None and sample_error:
            telemetry.record(RuntimeEvent("parse_failure", "reviewer_schema_invalid", detail=sample_error))
            telemetry.record(RuntimeEvent("fallback", f"reviewer_{sample_error}"))
        successful_reviewers += int(not sample_error)
        all_findings.extend(findings)
        independent_reviews.append(
            {
                "agent_name": role_id,
                "sample_status": sample_status,
                "sample_error": sample_error,
                "role_feedback": feedback,
                "findings": [finding.model_dump(mode="json") for finding in findings],
            }
        )

    unavailable_reviewers = len(plan.active_role_ids) - successful_reviewers
    if unavailable_reviewers == 0:
        reviewer_coverage = "full"
    elif successful_reviewers == 0:
        reviewer_coverage = "none"
    else:
        reviewer_coverage = "partial"
    if reviewer_coverage != "full":
        telemetry.record(RuntimeEvent("fallback", f"reviewer_coverage_{reviewer_coverage}"))

    clusters = cluster_findings(
        all_findings,
        preflight,
    )
    discussion_issues = select_discussion_issues(clusters, task.mode) if plan.discussion_enabled else []
    discussion_rounds = []
    if discussion_issues and budget.remaining:
        raw = await _sample_json(
            executor,
            telemetry,
            budget,
            build_discussion_prompt(task, discussion_issues),
            max_tokens=1_500,
        )
        round_ = normalize_discussion_round(
            "round_1", discussion_issues, raw.get("turns", []) if raw else []
        )
        apply_discussion_updates(clusters, round_)
        discussion_rounds.append(round_)

    decision_suppressions: list[dict[str, str]] = []
    decision_points = _validate_outcome_options(
        build_decision_points(clusters, plan.max_decision_points),
        task,
        clusters,
        suppression_provenance=decision_suppressions,
    )
    user_decisions: list[UserDecision] = []
    fallback_reason = ""
    returned_pending = False
    if decision_points:
        if task.interactive_mode == "off" or not gateway.capabilities().form_elicitation:
            action = "unsupported"
            user_decisions = _fallback_decisions(decision_points, action)
        else:
            elicited = await gateway.elicit(
                _interaction_message(decision_points),
                response_type=_interaction_form(decision_points),
            )
            user_decisions = _decisions_from_elicitation(decision_points, elicited)
            action = elicited.action
        failed_actions = [
            decision.elicitation_action
            for decision in user_decisions
            if decision.elicitation_action not in {"accept", "delegate"}
        ]
        delegated = any(decision.elicitation_action == "delegate" for decision in user_decisions)
        if failed_actions:
            fallback_reason = f"user_interaction_{action}"
            telemetry.record(RuntimeEvent("fallback", fallback_reason))
            if task.decision_fallback == "return_pending":
                returned_pending = True
        elif delegated:
            fallback_reason = "user_delegated_to_council"
            telemetry.record(RuntimeEvent("fallback", fallback_reason))

    if returned_pending:
        reconsiderations = []
        reconsideration_provenance = ReconsiderationProvenance()
        reconsideration_warnings: list[str] = []
    else:
        reconsiderations, reconsideration_provenance, reconsideration_warnings = await _reconsider(
            task, clusters, user_decisions, executor, telemetry, budget
        )
    reconsideration_degraded = bool(
        reconsideration_provenance.skipped_role_ids
        or reconsideration_provenance.failed_role_ids
    )
    decision_validation_degraded = bool(decision_suppressions)
    degraded = reconsideration_degraded or decision_validation_degraded
    if reconsideration_degraded:
        fallback_reason = ";".join(filter(None, (fallback_reason, "reconsideration_degraded")))
    if decision_validation_degraded:
        fallback_reason = ";".join(filter(None, (fallback_reason, "decision_validation_degraded")))
        telemetry.record(RuntimeEvent("fallback", "decision_validation_degraded"))
    gate_result = policy_gate(decision_points, clusters)
    gate_result["decision_suppressions"] = decision_suppressions
    chief, trace = build_chief_decision(clusters, decision_points, user_decisions)
    if reviewer_coverage != "full":
        coverage_reason = f"reviewer_coverage_{reviewer_coverage}"
        fallback_reason = ";".join(filter(None, (coverage_reason, fallback_reason)))
        chief.review_needed = "是"
        chief.publishability = "需人工复核"
        chief.review_reason = (
            f"独立评审覆盖率 {successful_reviewers}/{len(plan.active_role_ids)}；"
            "采样覆盖不完整，需人工复核。"
        )
        chief.decision_rationale = (
            f"{chief.decision_rationale} 独立评审覆盖率 "
            f"{successful_reviewers}/{len(plan.active_role_ids)}；未将缺失采样视为无问题。"
        ).strip()
    if returned_pending:
        chief.review_needed = "是"
        chief.review_reason = "等待用户决定。"
        chief.publishability = "需人工复核"

    if returned_pending:
        status = "RETURNED_PENDING"
    elif chief.review_needed == "是":
        status = "NEEDS_HUMAN_REVIEW"
    elif fallback_reason:
        status = "COMPLETED_WITH_FALLBACK"
    else:
        status = "COMPLETED"

    telemetry.elapsed_ms = max(telemetry.elapsed_ms, int((perf_counter() - started) * 1_000))
    runtime_metadata = telemetry.snapshot().model_copy(
        update={
            "reviewer_samples_successful": successful_reviewers,
            "reviewer_samples_unavailable": unavailable_reviewers,
            "reviewer_coverage": reviewer_coverage,
        }
    )
    record = ReviewRecordV2(
        review_id=build_review_id(),
        created_at=datetime.now(timezone.utc),
        completed_at=datetime.now(timezone.utc),
        task=task,
        input_diagnostics=input_diagnostics or InputDiagnostics(
            source_original_length=len(task.source_text),
            source_reviewed_length=len(task.source_text),
            candidate_original_length=len(task.candidate_translation),
            candidate_reviewed_length=len(task.candidate_translation),
        ),
        runtime_metadata=runtime_metadata,
        council_plan=plan,
        preflight=preflight,
        independent_reviews=independent_reviews,
        issue_clusters=clusters,
        discussion_rounds=discussion_rounds,
        decision_points=decision_points,
        user_decisions=user_decisions,
        reconsiderations=reconsiderations,
        reconsideration_provenance=reconsideration_provenance,
        policy_gate_result=gate_result,
        chief_editor_decision=chief,
        decision_trace=trace,
        status=status,
        fallback_reason=fallback_reason,
        effective_task=_effective_task(task),
        deliberation_summary=_deliberation_summary(
            clusters, user_decisions, trace, reconsideration_provenance, reconsiderations
        ),
        degraded=degraded,
        warnings=[*reconsideration_warnings, *_suppression_warnings(decision_suppressions)],
    )
    (store or ReviewStore()).save(record, history_mode=task.history_mode)
    return record


def normalize_continuation_decisions(
    parent: ReviewRecordV2,
    values: Iterable[dict[str, Any]],
) -> list[UserDecision]:
    points = {point.decision_id: point for point in parent.decision_points}
    decisions: list[UserDecision] = []
    seen_decision_ids: set[str] = set()
    for value in values:
        if not isinstance(value, dict):
            raise ValueError("continuation decision must be an object")
        decision_id = str(value.get("decision_id", ""))
        if decision_id in seen_decision_ids:
            raise ValueError(f"duplicate decision_id: {decision_id}")
        seen_decision_ids.add(decision_id)
        point = points.get(decision_id)
        if point is None:
            raise ValueError(f"unknown decision_id: {decision_id}")
        selected_value = value.get("selected_option_id", "")
        if not isinstance(selected_value, str):
            raise ValueError(f"invalid option for {decision_id}")
        selected = selected_value
        if selected not in valid_options(point):
            raise ValueError(f"invalid option for {decision_id}: {selected}")
        option = next(
            option for option in point.options
            if option.valid and option.option_id == selected and not option.is_delegation
        )
        decisions.append(
            UserDecision.model_validate(
                {
                    **value,
                    "decision_id": decision_id,
                    "selected_option_id": selected,
                    "selected_outcome_value": option.outcome_value or option.label,
                    "elicitation_action": "accept",
                    "provenance": "continue_review",
                }
            )
        )
    return decisions


async def continue_structured_review(
    parent: ReviewRecordV2,
    user_decision_values: Iterable[dict[str, Any]],
    executor: ModelExecutor,
    *,
    store: ReviewStore | None = None,
) -> ReviewRecordV2:
    decisions = normalize_continuation_decisions(parent, user_decision_values)
    task = parent.task.model_copy(deep=True)
    plan = parent.council_plan.model_copy(deep=True)
    telemetry = getattr(executor, "telemetry", None)
    if not isinstance(telemetry, RuntimeTelemetry):
        telemetry = RuntimeTelemetry(sample_budget=plan.sample_budget)
        if hasattr(executor, "telemetry"):
            setattr(executor, "telemetry", telemetry)
    telemetry.sample_budget = plan.sample_budget
    budget = SampleBudget(
        task.mode,
        used=min(parent.runtime_metadata.sampling_calls, plan.sample_budget),
    )
    clusters = [cluster.model_copy(deep=True) for cluster in parent.issue_clusters]
    reconsiderations, reconsideration_provenance, reconsideration_warnings = await _reconsider(
        task, clusters, decisions, executor, telemetry, budget
    )
    chief, trace = build_chief_decision(clusters, parent.decision_points, decisions)
    reviewer_coverage = parent.runtime_metadata.reviewer_coverage
    if reviewer_coverage in {"partial", "none"}:
        chief.review_needed = "是"
        chief.publishability = "需人工复核"
        chief.review_reason = (
            f"独立评审覆盖率 {parent.runtime_metadata.reviewer_samples_successful}/"
            f"{parent.runtime_metadata.reviewer_samples_successful + parent.runtime_metadata.reviewer_samples_unavailable}；"
            "采样覆盖不完整，需人工复核。"
        )
        chief.decision_rationale = (
            f"{chief.decision_rationale} 延续父记录的独立评审覆盖率；"
            "未将后续用户决定视为缺失评审证据的替代。"
        ).strip()
    decision_suppressions = _bounded_decision_suppressions(
        parent.policy_gate_result.get("decision_suppressions", [])
    )
    reconsideration_degraded = bool(
        reconsideration_provenance.skipped_role_ids
        or reconsideration_provenance.failed_role_ids
    )
    decision_validation_degraded = bool(decision_suppressions)
    degraded = reconsideration_degraded or decision_validation_degraded
    status = (
        "NEEDS_HUMAN_REVIEW"
        if chief.review_needed == "是"
        else "COMPLETED_WITH_FALLBACK"
        if degraded
        else "COMPLETED"
    )
    record = parent.model_copy(deep=True)
    record.review_id = build_review_id()
    record.parent_review_id = parent.review_id
    record.created_at = datetime.now(timezone.utc)
    record.completed_at = datetime.now(timezone.utc)
    record.user_decisions = decisions
    record.reconsiderations = reconsiderations
    record.reconsideration_provenance = reconsideration_provenance
    record.issue_clusters = clusters
    record.policy_gate_result = policy_gate(parent.decision_points, clusters)
    record.policy_gate_result["decision_suppressions"] = decision_suppressions
    record.chief_editor_decision = chief
    record.decision_trace = trace
    record.effective_task = _effective_task(task)
    record.deliberation_summary = _deliberation_summary(
        clusters, decisions, trace, reconsideration_provenance, reconsiderations
    )
    record.runtime_metadata = telemetry.snapshot().model_copy(
        update={
            "reviewer_samples_successful": parent.runtime_metadata.reviewer_samples_successful,
            "reviewer_samples_unavailable": parent.runtime_metadata.reviewer_samples_unavailable,
            "reviewer_coverage": reviewer_coverage,
        }
    )
    record.status = status
    record.degraded = degraded
    record.warnings = [
        *reconsideration_warnings,
        *_suppression_warnings(decision_suppressions),
    ]
    record.fallback_reason = ";".join(filter(None, (
        f"reviewer_coverage_{reviewer_coverage}"
        if reviewer_coverage in {"partial", "none"}
        else "",
        "reconsideration_degraded" if reconsideration_degraded else "",
        "decision_validation_degraded" if decision_validation_degraded else "",
    )))
    (store or ReviewStore()).save(record, history_mode=task.history_mode)
    return record


def compact_review_response(record: ReviewRecordV2) -> dict[str, Any]:
    disputed = [
        cluster.topic[:240]
        for cluster in record.issue_clusters
        if cluster.consensus_status == "disputed"
    ][:8]
    consensus = [
        cluster.topic[:240]
        for cluster in record.issue_clusters
        if cluster.consensus_status == "consensus"
    ][:8]
    response = {
        "schema_version": record.schema_version,
        "review_id": record.review_id,
        "parent_review_id": record.parent_review_id,
        "status": record.status,
        "chief_editor": record.chief_editor_decision.model_dump(mode="json", exclude_none=True),
        "blind_spots": [cluster.topic[:240] for cluster in record.issue_clusters[:8]],
        "consensus": consensus,
        "material_disagreements": disputed,
        "user_decisions": [decision.model_dump(mode="json") for decision in record.user_decisions],
        "fallback_reason": record.fallback_reason,
        "effective_task": record.effective_task.model_dump(mode="json"),
        "deliberation_summary": record.deliberation_summary.model_dump(mode="json"),
        "degraded": record.degraded,
        "warnings": record.warnings,
        "runtime_metadata": record.runtime_metadata.model_dump(mode="json"),
        "retrieval_hint": "Use view_review_record(review_id, detail_level='full') for structured evidence and trace.",
    }
    if record.status == "RETURNED_PENDING":
        response["decision_points"] = [point.model_dump(mode="json") for point in record.decision_points]
    return response
