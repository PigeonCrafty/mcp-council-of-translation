"""Policy Gate and evidence-weighted Council adjudication (never vote counts)."""

from __future__ import annotations

from collections import defaultdict
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
    evidence_strength: dict[str, int] = defaultdict(int)
    for position in positions:
        if position.option_id not in valid_ids or position.blocking:
            continue
        relevance = _ROLE_RELEVANCE.get(position.role_id, 0.4)
        scores[position.option_id] += relevance * position.confidence * _STANCE_WEIGHT[position.stance]
        evidence_strength[position.option_id] += len(position.evidence)
    if not scores:
        return "", True
    ranked = sorted(scores, key=lambda option_id: (scores[option_id], evidence_strength[option_id], option_id), reverse=True)
    if len(ranked) > 1:
        first, second = ranked[:2]
        indistinguishable = scores[first] == scores[second] and evidence_strength[first] == evidence_strength[second]
        if indistinguishable:
            return "", True
    return ranked[0], False


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
        return selected, ["position_matrix", "role_relevance", "evidence", "confidence"], False
    fallback = point.fallback_option_id if point.fallback_option_id in valid_ids else ""
    if fallback and not human_needed:
        return fallback, ["configured_fallback"], False
    return "", ["indistinguishable_valid_alternatives"], True


def build_chief_decision(
    clusters: list[IssueCluster],
    decision_points: list[DecisionPoint],
    user_decisions: list[UserDecision],
) -> tuple[ChiefEditorDecisionV2, DecisionTrace]:
    decisions_by_id = {decision.decision_id: decision for decision in user_decisions}
    must_fix = [cluster.topic for cluster in clusters if cluster.blocking]
    should_fix = [cluster.topic for cluster in clusters if not cluster.blocking and cluster.severity in {"critical", "major"}]
    optional = [cluster.topic for cluster in clusters if cluster.severity in {"minor", "preference"}]
    entries: list[DecisionTraceEntry] = []
    human_needed = bool(must_fix)
    clusters_by_id = {cluster.issue_id: cluster for cluster in clusters}
    for point in decision_points:
        cluster = clusters_by_id.get(point.issue_id)
        selected, basis, needs_human = adjudicate_decision_point(
            point,
            cluster.positions if cluster else [],
            decisions_by_id.get(point.decision_id),
        )
        human_needed = human_needed or needs_human
        entries.append(
            DecisionTraceEntry(
                issue_id=point.issue_id,
                decision=selected or "human_review_required",
                basis=basis,
                rejected_options=[
                    {"option": option.option_id, "reason": option.invalid_reason or "not selected"}
                    for option in point.options
                    if option.option_id != selected
                ],
            )
        )
    publishability = "需人工复核" if human_needed else "修改后可发布" if should_fix else "可发布"
    chief = ChiefEditorDecisionV2(
        publishability=publishability,
        must_fix=must_fix,
        should_fix=should_fix,
        optional_improvements=optional,
        conflict_resolutions=[f"{entry.issue_id}: {entry.decision}" for entry in entries],
        execution_order=[*must_fix, *should_fix, *optional],
        decision_rationale="Policy Gate 后依据有效用户选择或证据加权 Position Matrix 裁决；未使用票数多数。",
        review_needed="是" if human_needed else "否",
        review_reason="存在阻断项或无法区分的有效方案。" if human_needed else "",
    )
    return chief, DecisionTrace(entries=entries)

