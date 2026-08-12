"""V2 structured deliberation orchestration independent of FastMCP Context."""

from __future__ import annotations

from datetime import datetime, timezone
import json
import re
from time import perf_counter
from typing import Any, Iterable, Literal

from pydantic import Field, create_model

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
    InputDiagnostics,
    IssueCluster,
    Reconsideration,
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
from council_of_translation.localization.roles import ROLE_REGISTRY, build_council_plan
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


def _review_findings(raw: dict[str, Any] | None, role_id: str) -> tuple[str, list[FindingV2]]:
    if raw is None:
        return "评审采样不可用；未将缺失输出升级为阻断项。", []
    role_feedback = str(raw.get("role_feedback", ""))[:2_000]
    findings: list[FindingV2] = []
    value = raw.get("findings", [])
    if isinstance(value, list):
        for index, item in enumerate(value[:5]):
            if not isinstance(item, dict):
                continue
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
            if finding.problem or finding.action:
                findings.append(finding)
    return role_feedback, findings


def _interaction_form(decision_points: list) -> type:
    fields: dict[str, tuple[Any, Any]] = {}
    for point in decision_points:
        options = valid_options(point)
        option_type = Literal.__getitem__(tuple(options))
        mapping = "; ".join(
            f"{option.option_id} = {option.label}（{option.description or option.label}）"
            for option in point.options
            if option.valid
        )
        fields[point.decision_id] = (
            option_type,
            Field(description=f"{point.question} 可选值：{mapping}"),
        )
    return create_model("CouncilDecisionForm", **fields)


def _interaction_message(decision_points: list) -> str:
    lines = ["Council 发现以下均满足硬约束的选择，请在一个表单中决定："]
    for point in decision_points:
        lines.append(f"- {point.question}")
        for option in point.options:
            if option.valid:
                lines.append(
                    f"  - {option.option_id}: {option.label} — {option.description or option.label}"
                )
    return "\n".join(lines)


def _decisions_from_elicitation(decision_points: list, result: ElicitationResult) -> list[UserDecision]:
    decisions: list[UserDecision] = []
    for point in decision_points:
        selected = str(result.data.get(point.decision_id, "")) if result.action == "accept" else ""
        action = result.action
        if action == "error":
            action = "malformed"
        if action == "accept" and selected not in valid_options(point):
            action = "malformed"
        decisions.append(
            UserDecision(
                decision_id=point.decision_id,
                selected_option_id=selected,
                elicitation_action=action,
                provenance="mcp_elicitation",
            )
        )
    return decisions


def _fallback_decisions(decision_points: list, action: str) -> list[UserDecision]:
    normalized = action if action in {"decline", "cancel", "unsupported", "pending", "malformed"} else "malformed"
    return [UserDecision(decision_id=point.decision_id, elicitation_action=normalized) for point in decision_points]


async def _reconsider(
    task: ReviewTaskV2,
    clusters: list[IssueCluster],
    decisions: list[UserDecision],
    executor: ModelExecutor,
    telemetry: RuntimeTelemetry,
    budget: SampleBudget,
) -> list[Reconsideration]:
    points_by_issue = {f"decision_{cluster.issue_id.removeprefix('issue_')}": cluster for cluster in clusters}
    accepted = [decision for decision in decisions if decision.elicitation_action == "accept"]
    affected: dict[str, list[tuple[IssueCluster, UserDecision]]] = {}
    for decision in accepted:
        cluster = points_by_issue.get(decision.decision_id)
        if cluster is None:
            continue
        for role_id in cluster.participant_role_ids:
            affected.setdefault(role_id, []).append((cluster, decision))

    reconsiderations: list[Reconsideration] = []
    for role_id, packets in affected.items():
        if budget.remaining <= 0 or role_id not in ROLE_REGISTRY:
            telemetry.record(RuntimeEvent("fallback", "reconsideration_budget_unavailable", detail=role_id))
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
        raw_positions = raw.get("positions", []) if raw else []
        by_issue = {
            str(item.get("issue_id", "")): item
            for item in raw_positions
            if isinstance(item, dict)
        }
        for issue, decision in packets:
            previous = next((position for position in issue.positions if position.role_id == role_id), None)
            item = by_issue.get(issue.issue_id)
            revised = None
            valid_ids = {option_id_for_action(issue.issue_id, action) for action in issue.candidate_actions}
            if item is not None and previous is not None and str(item.get("option_id", "")) in valid_ids:
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
                issue.positions = [position for position in issue.positions if position.role_id != role_id] + [revised]
            reconsiderations.append(
                Reconsideration(
                    issue_id=issue.issue_id,
                    role_id=role_id,
                    trigger_decision_id=decision.decision_id,
                    previous_position=previous,
                    revised_position=revised or previous,
                    changed=bool(revised and revised != previous),
                )
            )
    return reconsiderations


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
    for role_id in plan.active_role_ids:
        raw = await _sample_json(
            executor,
            telemetry,
            budget,
            build_v2_reviewer_prompt(ROLE_REGISTRY[role_id], task, preflight),
            max_tokens=1_400,
        )
        feedback, findings = _review_findings(raw, role_id)
        all_findings.extend(findings)
        independent_reviews.append(
            {
                "agent_name": role_id,
                "role_feedback": feedback,
                "findings": [finding.model_dump(mode="json") for finding in findings],
            }
        )

    clusters = cluster_findings(all_findings, preflight)
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

    decision_points = build_decision_points(clusters, plan.max_decision_points)
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
        if any(decision.elicitation_action != "accept" for decision in user_decisions):
            fallback_reason = f"user_interaction_{action}"
            telemetry.record(RuntimeEvent("fallback", fallback_reason))
            if task.decision_fallback == "return_pending":
                returned_pending = True

    reconsiderations = [] if returned_pending else await _reconsider(
        task, clusters, user_decisions, executor, telemetry, budget
    )
    gate_result = policy_gate(decision_points, clusters)
    chief, trace = build_chief_decision(clusters, decision_points, user_decisions)
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
        runtime_metadata=telemetry.snapshot(),
        council_plan=plan,
        preflight=preflight,
        independent_reviews=independent_reviews,
        issue_clusters=clusters,
        discussion_rounds=discussion_rounds,
        decision_points=decision_points,
        user_decisions=user_decisions,
        reconsiderations=reconsiderations,
        policy_gate_result=gate_result,
        chief_editor_decision=chief,
        decision_trace=trace,
        status=status,
        fallback_reason=fallback_reason,
    )
    (store or ReviewStore()).save(record, history_mode=task.history_mode)
    return record


def normalize_continuation_decisions(
    parent: ReviewRecordV2,
    values: Iterable[dict[str, Any]],
) -> list[UserDecision]:
    points = {point.decision_id: point for point in parent.decision_points}
    decisions: list[UserDecision] = []
    for value in values:
        decision_id = str(value.get("decision_id", ""))
        point = points.get(decision_id)
        if point is None:
            raise ValueError(f"unknown decision_id: {decision_id}")
        selected = str(value.get("selected_option_id", ""))
        if selected not in valid_options(point):
            raise ValueError(f"invalid option for {decision_id}: {selected}")
        decisions.append(
            UserDecision.model_validate(
                {
                    **value,
                    "decision_id": decision_id,
                    "selected_option_id": selected,
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
    budget = SampleBudget(task.mode)
    clusters = [cluster.model_copy(deep=True) for cluster in parent.issue_clusters]
    reconsiderations = await _reconsider(task, clusters, decisions, executor, telemetry, budget)
    chief, trace = build_chief_decision(clusters, parent.decision_points, decisions)
    status = "NEEDS_HUMAN_REVIEW" if chief.review_needed == "是" else "COMPLETED"
    record = parent.model_copy(deep=True)
    record.review_id = build_review_id()
    record.parent_review_id = parent.review_id
    record.created_at = datetime.now(timezone.utc)
    record.completed_at = datetime.now(timezone.utc)
    record.user_decisions = decisions
    record.reconsiderations = reconsiderations
    record.issue_clusters = clusters
    record.policy_gate_result = policy_gate(parent.decision_points, clusters)
    record.chief_editor_decision = chief
    record.decision_trace = trace
    record.runtime_metadata = telemetry.snapshot()
    record.status = status
    record.fallback_reason = ""
    (store or ReviewStore()).save(record, history_mode=task.history_mode)
    return record


def compact_review_response(record: ReviewRecordV2) -> dict[str, Any]:
    disputed = [cluster.topic for cluster in record.issue_clusters if cluster.consensus_status == "disputed"]
    consensus = [cluster.topic for cluster in record.issue_clusters if cluster.consensus_status == "consensus"]
    response = {
        "schema_version": record.schema_version,
        "review_id": record.review_id,
        "parent_review_id": record.parent_review_id,
        "status": record.status,
        "chief_editor": record.chief_editor_decision.model_dump(mode="json", exclude_none=True),
        "blind_spots": [cluster.topic for cluster in record.issue_clusters],
        "consensus": consensus,
        "material_disagreements": disputed,
        "user_decisions": [decision.model_dump(mode="json") for decision in record.user_decisions],
        "fallback_reason": record.fallback_reason,
        "runtime_metadata": record.runtime_metadata.model_dump(mode="json"),
    }
    if record.status == "RETURNED_PENDING":
        response["decision_points"] = [point.model_dump(mode="json") for point in record.decision_points]
    return response
