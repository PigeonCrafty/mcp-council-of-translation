"""Deterministic diagnostics for the marginal value of Council participation."""

from __future__ import annotations

from collections import defaultdict
import re
import unicodedata
from typing import Any, Iterable

from council_of_translation.localization.clustering import outcome_key
from council_of_translation.localization.models import (
    CouncilValueMetrics,
    DiscussionRound,
    IssueCluster,
    RoleContribution,
    option_id_for_action,
)


_STRUCTURED_TOKEN = re.compile(
    r"(?<!\{)\{[A-Za-z_][\w.-]*(?:![rsa])?(?::[^{}]+)?\}(?!\})"
    r"|%(?!%)(?:\d+\$)?[-+#0 ']*(?:\d+|\*)?(?:\.(?:\d+|\*))?[hlLzjt]*[diuoxXfFeEgGaAcspn]"
    r"|\$\{[A-Za-z_][A-Za-z0-9_]*\}|\$[A-Za-z_][A-Za-z0-9_]*"
    r"|</?[A-Za-z][A-Za-z0-9:-]*\b[^>]*>"
    r"|https?://[^\s<>\]\[\"']+"
    r"|(?<![\w-])--[A-Za-z][\w-]*|(?<!\w)/[A-Za-z][\w-]*(?!\w)"
)
_STRUCTURED_PROVENANCE = re.compile(
    r"(?i)(?:rule_ref|constraint_ref):[A-Za-z0-9][A-Za-z0-9_.:/-]{0,119}"
)
_PROVENANCE_VALUE = re.compile(r"[A-Za-z0-9][A-Za-z0-9_.:/-]{0,119}")


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
    return {
        role_id
        for role_id in cluster.participant_role_ids
        if role_id in active_roles
    }


def _normalize_anchor(value: str) -> str:
    """Return a bounded exact-comparison form for a structured span."""
    return " ".join(unicodedata.normalize("NFKC", value).casefold().split())[:240]


def _structured_issue_keys(cluster: IssueCluster) -> set[tuple[str, str]]:
    """Return bounded aliases from source/candidate spans, never issue prose."""
    values = [*cluster.source_spans, *cluster.candidate_spans]
    keys: set[tuple[str, str]] = set()
    for value in values:
        bounded = unicodedata.normalize("NFKC", str(value)).strip()[:240]
        anchor = _normalize_anchor(bounded)
        if anchor:
            keys.add(("anchor", anchor))

        prefix, separator, literal = bounded.partition(":")
        if separator and literal and prefix in {"required_literal", "forbidden_literal"}:
            literal_anchor = _normalize_anchor(literal)
            if literal_anchor:
                keys.add(("anchor", literal_anchor))

        for match in _STRUCTURED_TOKEN.finditer(bounded):
            token = _normalize_anchor(match.group(0))
            if token:
                keys.add(("token", token))
                tag = re.fullmatch(r"</?([a-z][a-z0-9:-]*)\b[^>]*>", token)
                slash = re.fullmatch(r"/([a-z][\w-]*)", token)
                # The preflight command scanner also sees an HTML closing tag as
                # ``/name``.  This bounded structural alias joins that duplicate
                # diagnostic to the actual tag check without reading issue prose.
                if tag:
                    keys.add(("markup-name", tag.group(1)))
                elif slash:
                    keys.add(("markup-name", slash.group(1)))

                # The command scanner sees the second slash and first host label
                # of a URL as a slash command (for example ``/example``).  Give
                # only deterministic URL structure that exact scanner alias.
                url = re.fullmatch(r"https?://([^/:?#]+)(?:[/:?#].*)?", token)
                if url:
                    first_host_label = url.group(1).split(".", 1)[0]
                    if re.fullmatch(r"[a-z][\w-]*", first_host_label):
                        keys.add(("token", f"/{first_host_label}"))
    return keys


def _logical_issue_groups(clusters: list[IssueCluster]) -> list[list[IssueCluster]]:
    """Correlate reviewer anchors only through deterministic preflight aliases."""
    groups: list[tuple[set[tuple[str, str]], list[IssueCluster]]] = []
    deterministic = [cluster for cluster in clusters if not cluster.finding_ids]
    reviewer = [cluster for cluster in clusters if cluster.finding_ids]

    # First collapse exact overlapping views from deterministic scanners.  These
    # groups remain projections only; the original clusters are never mutated.
    for cluster in deterministic:
        keys = _structured_issue_keys(cluster)
        matching = [index for index, (known, _) in enumerate(groups) if keys and known & keys]
        if not matching:
            groups.append((set(keys), [cluster]))
            continue
        first = matching[0]
        groups[first][0].update(keys)
        groups[first][1].append(cluster)
        for index in reversed(matching[1:]):
            other_keys, other_clusters = groups.pop(index)
            groups[first][0].update(other_keys)
            groups[first][1].extend(other_clusters)

    deterministic_group_count = len(groups)
    # A reviewer cluster may support each deterministic issue whose exact anchor
    # it carries, but it cannot bridge two otherwise distinct deterministic issues.
    # Model-only clusters remain separate because production clustering already
    # owns their issue identity and semantic deduplication.
    for cluster in reviewer:
        keys = _structured_issue_keys(cluster)
        matching = [
            index
            for index, (known, _) in enumerate(groups[:deterministic_group_count])
            if keys and known & keys
        ]
        if matching:
            for index in matching:
                groups[index][1].append(cluster)
        else:
            groups.append((set(keys), [cluster]))
    return [members for _, members in groups]


def _bounded_structured_evidence_keys(value: str) -> set[str]:
    """Extract only independently checkable, bounded evidence anchors.

    Natural-language claims are deliberately not evidence identities.  They may
    explain an existing fact, but without typed provenance the metric cannot prove
    that a differently worded sentence added information.
    """
    bounded = unicodedata.normalize("NFKC", str(value)).strip()[:240]
    keys = {
        f"token:{_normalize_anchor(match.group(0))}"
        for match in _STRUCTURED_TOKEN.finditer(bounded)
        if _normalize_anchor(match.group(0))
    }
    if provenance := _STRUCTURED_PROVENANCE.fullmatch(bounded):
        keys.add(f"provenance:{_normalize_anchor(provenance.group(0))}")
    return keys


def _canonical_provenance_key(kind: str, value: str) -> str:
    """Map a typed-field value to the same identity used by discussion markers."""
    bounded = unicodedata.normalize("NFKC", str(value)).strip()
    prefix = f"{kind}:"
    while bounded.casefold().startswith(prefix):
        bounded = bounded[len(prefix):]
    if not _PROVENANCE_VALUE.fullmatch(bounded):
        return ""
    return f"provenance:{kind}:{_normalize_anchor(bounded)}"


def _pre_discussion_inventory(cluster: IssueCluster) -> set[str]:
    """Build the issue-local structured inventory available before deliberation."""
    inventory = {f"issue:{_normalize_anchor(cluster.issue_id)}"}
    values = [
        *cluster.source_spans,
        *cluster.candidate_spans,
        *cluster.immutable_hard_constraints,
        *cluster.evidence,
        cluster.current_outcome,
        cluster.outcome_anchor,
    ]
    for position in cluster.positions:
        values.extend([
            position.option_id,
            position.claim,
            *position.evidence,
            *position.rule_refs,
            *position.conditions,
        ])
        for rule_ref in position.rule_refs:
            if key := _canonical_provenance_key("rule_ref", rule_ref):
                inventory.add(key)
    for constraint_ref in cluster.immutable_hard_constraints:
        if key := _canonical_provenance_key("constraint_ref", constraint_ref):
            inventory.add(key)
    for value in values:
        normalized = _normalize_anchor(str(value))
        if normalized:
            inventory.add(f"exact:{normalized}")
        inventory.update(_bounded_structured_evidence_keys(str(value)))
    return inventory


def _discussion_deltas(
    clusters: Iterable[IssueCluster],
    discussion_rounds: Iterable[DiscussionRound],
) -> tuple[int, int, int, str]:
    rounds = list(discussion_rounds)
    if not rounds:
        return 0, 0, 0, "not_applicable"

    by_issue = {cluster.issue_id: cluster for cluster in clusters}
    seen_structured_evidence = {
        issue_id: _pre_discussion_inventory(cluster)
        for issue_id, cluster in by_issue.items()
    }
    new_evidence: set[tuple[str, tuple[str, ...]]] = set()
    changed_positions: set[tuple[str, str]] = set()
    for round_ in rounds:
        for turn in round_.turns:
            cluster = by_issue.get(turn.issue_id)
            if cluster is None:
                continue
            for evidence in turn.evidence:
                keys = _bounded_structured_evidence_keys(evidence)
                novel = tuple(sorted(keys - seen_structured_evidence[turn.issue_id]))
                if novel:
                    new_evidence.add((turn.issue_id, novel))
                    seen_structured_evidence[turn.issue_id].update(novel)
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
    for group in _logical_issue_groups(clusters_list):
        deterministic_ids = [cluster.issue_id for cluster in group if not cluster.finding_ids]
        issue_identity = min(deterministic_ids or [cluster.issue_id for cluster in group])
        roles = set().union(*(_material_roles(cluster, active_set) for cluster in group))
        if len(roles) == 1:
            role_id = next(iter(roles))
            unique_by_role[role_id].add(issue_identity)
            unique_issues.add(issue_identity)
        elif len(roles) > 1:
            corroborated_issues.add(issue_identity)
            for role_id in roles:
                corroborated_by_role[role_id].add(issue_identity)

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
