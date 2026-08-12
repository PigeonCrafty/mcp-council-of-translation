"""Policy Gate and evidence-weighted Council adjudication (never vote counts)."""

from __future__ import annotations

from collections import defaultdict
from math import isclose
from typing import Iterable

from council_of_translation.localization.models import (
    ChiefEditorDecisionV2,
    DecisionPoint,
    DecisionTrace,
    DecisionTraceEntry,
    IssueCluster,
    RolePosition,
    UserDecision,
)


_ROLE_RELEVANCE = {
    "technical_safety_reviewer": 1.0,
    "fidelity_reviewer": 0.95,
    "risk_ambiguity_reviewer": 0.85,
    "product_context_reviewer": 0.75,
    "terminology_reviewer": 0.7,
    "ux_copy_reviewer": 0.65,
    "brand_voice_reviewer": 0.5,
    "fluency_reviewer": 0.45,
}
_STANCE_WEIGHT = {"accept": 1.0, "accept_with_conditions": 0.7, "reject": -1.0, "not_applicable": 0.0}
_ORIGIN_WEIGHT = {"preflight": 1.4, "caller": 1.3, "user": 1.15, "system": 1.0, "model": 0.7}
_TIER_WEIGHT = {"hard": 1.6, "contextual": 1.25, "preference": 0.9, "advisory": 0.75}


def valid_options(point: DecisionPoint) -> dict[str, str]:
    return {option.option_id: option.label for option in point.options if option.valid}


def policy_gate(
    points: Iterable[DecisionPoint],
    clusters: Iterable[IssueCluster],
) -> dict[str, object]:
    blocking_issues = [cluster.issue_id for cluster in clusters if cluster.blocking]
    return {
        "blocking_issue_ids": blocking_issues,
        "valid_options": {point.decision_id: list(valid_options(point)) for point in points},
        "invalid_options": {
            point.decision_id: {option.option_id: option.invalid_reason for option in point.options if not option.valid}
            for point in points
        },
        "passed": not blocking_issues,
    }


def _matrix_choice(positions: Iterable[RolePosition], valid_ids: set[str]) -> tuple[str, bool]:
    scores: dict[str, float] = defaultdict(float)
    for position in positions:
        if position.option_id not in valid_ids:
            continue
        relevance = _ROLE_RELEVANCE.get(position.role_id, 0.4)
        provenance = _ORIGIN_WEIGHT[position.evidence_origin]
        tier = _TIER_WEIGHT[position.constraint_tier]
        evidence = 1.0 + min(len(position.evidence), 3) * 0.08 + min(len(position.rule_refs), 2) * 0.12
        blocking = 1.75 if position.blocking else 1.0
        scores[position.option_id] += (
            relevance
            * position.confidence
            * _STANCE_WEIGHT[position.stance]
            * provenance
            * tier
            * evidence
            * blocking
        )
    if not scores:
        return "", True
    ranked = sorted(scores, key=lambda option_id: (scores[option_id], option_id), reverse=True)
    first = ranked[0]
    if scores[first] <= 0:
        return "", True
    if len(ranked) > 1 and isclose(scores[first], scores[ranked[1]], rel_tol=1e-9, abs_tol=1e-9):
        return "", True
    return first, False


def adjudicate_decision_point(
    point: DecisionPoint,
    positions: Iterable[RolePosition],
    user_decision: UserDecision | None,
) -> tuple[str, list[str], bool]:
    options = valid_options(point)
    valid_ids = set(options)
    if (
        user_decision is not None
        and user_decision.elicitation_action == "accept"
        and user_decision.selected_option_id in valid_ids
        and user_decision.authority_mode in {"decisive_within_valid_options", "policy_override"}
    ):
        return user_decision.selected_option_id, ["valid_user_decision"], False
    selected, human_needed = _matrix_choice(positions, valid_ids)
    if selected:
        return selected, [
            "position_matrix",
            "role_relevance",
            "evidence_provenance",
            "constraint_tier",
            "blocking_state",
            "confidence",
        ], False
    return "", ["indistinguishable_or_insufficient_valid_evidence"], human_needed


def build_chief_decision(
    clusters: list[IssueCluster],
    decision_points: list[DecisionPoint],
    user_decisions: list[UserDecision],
) -> tuple[ChiefEditorDecisionV2, DecisionTrace]:
    decisions_by_id = {decision.decision_id: decision for decision in user_decisions}
    clusters_by_id = {cluster.issue_id: cluster for cluster in clusters}
    resolved_issue_ids = {point.issue_id for point in decision_points}
    must_fix = [cluster.topic for cluster in clusters if cluster.blocking]
    should_fix = [
        cluster.topic
        for cluster in clusters
        if cluster.issue_id not in resolved_issue_ids
        and not cluster.blocking
        and cluster.severity in {"critical", "major"}
    ]
    optional = [
        cluster.topic
        for cluster in clusters
        if cluster.issue_id not in resolved_issue_ids and cluster.severity in {"minor", "preference"}
    ]
    entries: list[DecisionTraceEntry] = []
    conflict_resolutions: list[str] = []
    terminology_decisions: list[str] = []
    resolved_actions: list[str] = []
    human_needed = bool(must_fix)

    for point in decision_points:
        cluster = clusters_by_id.get(point.issue_id)
        user_decision = decisions_by_id.get(point.decision_id)
        selected, basis, needs_human = adjudicate_decision_point(
            point,
            cluster.positions if cluster else [],
            user_decision,
        )
        human_needed = human_needed or needs_human
        labels = valid_options(point)
        label = labels.get(selected, "")
        if selected and basis == ["valid_user_decision"]:
            outcome = "valid_user_choice"
            basis_summary = "用户在有效选项内决定"
        elif selected:
            outcome = "council_fallback"
            basis_summary = "Council 依据证据加权 Position Matrix 裁决"
        else:
            outcome = "human_review"
            basis_summary = "有效证据不足或无法区分"

        topic = cluster.topic if cluster else point.question
        if label:
            action = f"对“{topic}”采用“{label}”"
            conflict_resolutions.append(f"{action}；{basis_summary}。")
            resolved_actions.append(action)
            if cluster and cluster.category == "language_choice":
                terminology_decisions.append(action)
        entries.append(
            DecisionTraceEntry(
                issue_id=point.issue_id,
                decision=label or "需要人工复核",
                selected_option_id=selected,
                outcome=outcome,
                basis=basis,
                rejected_options=[
                    {"option": option.label, "reason": option.invalid_reason or "未选用"}
                    for option in point.options
                    if option.option_id != selected
                ],
            )
        )

    optional.extend(resolved_actions)
    publishability = "需人工复核" if human_needed else "修改后可发布" if should_fix else "可发布"
    outcome_counts = {
        name: sum(entry.outcome == name for entry in entries)
        for name in ("valid_user_choice", "council_fallback", "human_review")
    }
    rationale = (
        "Policy Gate 后裁决："
        f"用户有效选择 {outcome_counts['valid_user_choice']} 项，"
        f"Council fallback {outcome_counts['council_fallback']} 项，"
        f"人工复核 {outcome_counts['human_review']} 项；未使用票数多数。"
    )
    chief = ChiefEditorDecisionV2(
        publishability=publishability,
        must_fix=must_fix,
        should_fix=should_fix,
        optional_improvements=optional,
        terminology_decisions=terminology_decisions,
        conflict_resolutions=conflict_resolutions,
        execution_order=[*must_fix, *should_fix, *resolved_actions, *optional[: len(optional) - len(resolved_actions)]],
        decision_rationale=rationale,
        review_needed="是" if human_needed else "否",
        review_reason="存在阻断项或有效证据不足/无法区分。" if human_needed else "",
    )
    return chief, DecisionTrace(entries=entries)
