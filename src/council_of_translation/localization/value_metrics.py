"""Deterministic diagnostics for the marginal value of Council participation."""

from __future__ import annotations

from collections import defaultdict
from typing import Any, Iterable

from council_of_translation.localization.clustering import outcome_key
from council_of_translation.localization.models import (
    CouncilValueMetrics,
    DiscussionRound,
    IssueCluster,
    RoleContribution,
    option_id_for_action,
)


def _sample_statuses(independent_reviews: Iterable[dict[str, Any]]) -> dict[str, str]:
    statuses: dict[str, str] = {}
    for review in independent_reviews:
        if not isinstance(review, dict):
            continue
        role_id = review.get("agent_name")
        if isinstance(role_id, str) and role_id:
            statuses[role_id] = str(review.get("sample_status", "unavailable"))
    return statuses


def _material_roles(cluster: IssueCluster, active_roles: set[str]) -> set[str]:
    """Return issue-local roles once, independent of duplicate finding volume."""
    if not cluster.finding_ids:
        return set()
    return {
        role_id
        for role_id in cluster.participant_role_ids
        if role_id in active_roles
    }


def _discussion_deltas(
    clusters: Iterable[IssueCluster],
    discussion_rounds: Iterable[DiscussionRound],
) -> tuple[int, int, int, str]:
    rounds = list(discussion_rounds)
    if not rounds:
        return 0, 0, 0, "not_applicable"

    by_issue = {cluster.issue_id: cluster for cluster in clusters}
    baseline_evidence = {
        issue_id: {outcome_key(item) for item in cluster.evidence if outcome_key(item)}
        for issue_id, cluster in by_issue.items()
    }
    new_evidence: set[tuple[str, str]] = set()
    changed_positions: set[tuple[str, str]] = set()
    for round_ in rounds:
        for turn in round_.turns:
            cluster = by_issue.get(turn.issue_id)
            if cluster is None:
                continue
            for evidence in turn.evidence:
                normalized = outcome_key(evidence)
                if normalized and normalized not in baseline_evidence[turn.issue_id]:
                    new_evidence.add((turn.issue_id, normalized))
            if not turn.position_changed or not turn.proposed_action:
                continue
            expected_option = option_id_for_action(
                cluster.issue_id, outcome_key(turn.proposed_action)
            )
            final_position = next(
                (position for position in cluster.positions if position.role_id == turn.speaker),
                None,
            )
            if final_position is not None and final_position.option_id == expected_option:
                changed_positions.add((turn.issue_id, turn.speaker))

    resolved: set[str] = set()
    for issue_id, cluster in by_issue.items():
        if cluster.consensus_status != "disputed" or not _material_roles(cluster, set(cluster.participant_role_ids)):
            continue
        final_options = {
            position.option_id
            for position in cluster.positions
            if position.role_id in cluster.participant_role_ids and position.option_id
        }
        if len(final_options) == 1 and any(changed_issue == issue_id for changed_issue, _ in changed_positions):
            resolved.add(issue_id)

    marginal_value = (
        "material"
        if changed_positions or resolved
        else "low"
        if new_evidence
        else "none"
    )
    return len(new_evidence), len(changed_positions), len(resolved), marginal_value


def compute_council_value_metrics(
    *,
    active_role_ids: Iterable[str],
    independent_reviews: Iterable[dict[str, Any]],
    clusters: Iterable[IssueCluster],
    discussion_rounds: Iterable[DiscussionRound],
) -> CouncilValueMetrics:
    """Project contribution without votes, weights, prose scoring, or side effects."""
    active_roles = list(dict.fromkeys(active_role_ids))[:8]
    active_set = set(active_roles)
    statuses = _sample_statuses(independent_reviews)
    clusters_list = list(clusters)

    unique_by_role: dict[str, set[str]] = defaultdict(set)
    corroborated_by_role: dict[str, set[str]] = defaultdict(set)
    unique_issues: set[str] = set()
    corroborated_issues: set[str] = set()
    for cluster in clusters_list:
        roles = _material_roles(cluster, active_set)
        if len(roles) == 1:
            role_id = next(iter(roles))
            unique_by_role[role_id].add(cluster.issue_id)
            unique_issues.add(cluster.issue_id)
        elif len(roles) > 1:
            corroborated_issues.add(cluster.issue_id)
            for role_id in roles:
                corroborated_by_role[role_id].add(cluster.issue_id)

    contributions: list[RoleContribution] = []
    for role_id in active_roles:
        unique_count = len(unique_by_role[role_id])
        corroborated_count = len(corroborated_by_role[role_id])
        unavailable = statuses.get(role_id) != "structured_success"
        contribution_kind = (
            "unavailable"
            if unavailable
            else "unique_material"
            if unique_count
            else "corroborating"
            if corroborated_count
            else "confirmation_only"
        )
        contributions.append(
            RoleContribution(
                role_id=role_id,
                contribution_kind=contribution_kind,
                unique_issue_count=unique_count,
                corroborated_issue_count=corroborated_count,
                material_finding_count=unique_count + corroborated_count,
            )
        )

    new_evidence, position_changes, resolved, marginal = _discussion_deltas(
        clusters_list, discussion_rounds
    )
    return CouncilValueMetrics(
        role_contributions=contributions,
        unique_material_issue_count=len(unique_issues),
        corroborated_issue_count=len(corroborated_issues),
        confirmation_only_role_count=sum(
            item.contribution_kind == "confirmation_only" for item in contributions
        ),
        unavailable_role_count=sum(
            item.contribution_kind == "unavailable" for item in contributions
        ),
        discussion_new_evidence_count=new_evidence,
        discussion_position_change_count=position_changes,
        discussion_resolved_issue_count=resolved,
        discussion_marginal_value=marginal,
    )
