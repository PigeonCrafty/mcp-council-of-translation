"""Issue-centric normalization and deterministic hybrid clustering."""

from __future__ import annotations

from collections import defaultdict
import hashlib
import re
import unicodedata
from typing import Any, Iterable

from council_of_translation.localization.models import (
    FindingV2,
    IssueCluster,
    PreflightResult,
    RolePosition,
    option_id_for_action,
)


_ISSUE_FAMILY = {
    "technical": "integrity",
    "accuracy": "correctness",
    "risk": "correctness",
    "terminology": "language_choice",
    "fluency": "language_choice",
    "style": "language_choice",
    "ux": "language_choice",
    "context": "language_choice",
    "other": "other",
}


def _stable_id(prefix: str, *parts: str) -> str:
    digest = hashlib.sha256("\x1f".join(parts).encode("utf-8")).hexdigest()[:12]
    return f"{prefix}_{digest}"


def _normalize_anchor(text: str) -> str:
    return re.sub(r"[^\w\u3400-\u9fff]+", "", text.casefold())


def outcome_key(value: str) -> str:
    """Normalize harmless Unicode/whitespace variation without erasing wording."""
    return " ".join(unicodedata.normalize("NFKC", value).strip().split())


def _distinct_outcomes(values: Iterable[str]) -> list[str]:
    outcomes: list[str] = []
    seen: set[str] = set()
    for value in values:
        if not isinstance(value, str):
            continue
        normalized = outcome_key(value)
        if not normalized or len(normalized) > 500 or normalized in seen:
            continue
        seen.add(normalized)
        outcomes.append(normalized)
    return outcomes


def _ngrams(text: str) -> set[str]:
    normalized = _normalize_anchor(text)
    if len(normalized) < 2:
        return {normalized} if normalized else set()
    return {normalized[index : index + 2] for index in range(len(normalized) - 1)}


def _similar(left: str, right: str) -> bool:
    left_norm = _normalize_anchor(left)
    right_norm = _normalize_anchor(right)
    if not left_norm or not right_norm:
        return False
    if left_norm in right_norm or right_norm in left_norm:
        return True
    left_grams, right_grams = _ngrams(left_norm), _ngrams(right_norm)
    union = left_grams | right_grams
    return bool(union) and len(left_grams & right_grams) / len(union) >= 0.5


def normalize_findings(raw_findings: Iterable[FindingV2 | dict[str, Any]]) -> list[FindingV2]:
    normalized: list[FindingV2] = []
    for index, raw in enumerate(raw_findings):
        finding = raw if isinstance(raw, FindingV2) else FindingV2.model_validate(raw)
        if not finding.finding_id:
            finding.finding_id = _stable_id(
                "finding",
                finding.agent_name,
                finding.issue_type,
                finding.source_span,
                finding.candidate_span,
                finding.problem,
                str(index),
            )
        normalized.append(finding)
    return normalized


def _cluster_model_findings(findings: list[FindingV2]) -> list[list[FindingV2]]:
    groups: list[list[FindingV2]] = []
    for finding in findings:
        family = _ISSUE_FAMILY[finding.issue_type]
        for group in groups:
            representative = group[0]
            representative_family = _ISSUE_FAMILY[representative.issue_type]
            if family != representative_family:
                continue
            source_matches = _similar(finding.source_span, representative.source_span)
            candidate_matches = _similar(finding.candidate_span, representative.candidate_span)
            if source_matches or candidate_matches:
                group.append(finding)
                break
        else:
            groups.append([finding])
    return groups


def _severity(findings: list[FindingV2]) -> str:
    order = {"preference": 0, "minor": 1, "major": 2, "critical": 3}
    return max((finding.severity for finding in findings), key=order.__getitem__, default="minor")


def _model_cluster(group: list[FindingV2], current_candidate: str = "") -> IssueCluster:
    first = next(
        (finding for finding in group if finding.finding_kind != "affirmation"),
        group[0],
    )
    family = _ISSUE_FAMILY[first.issue_type]
    anchors = sorted({anchor for finding in group for anchor in (finding.source_span, finding.candidate_span) if anchor})
    issue_id = _stable_id("issue", family, *anchors)
    proposals = _distinct_outcomes(
        finding.proposed_value
        for finding in group
        if finding.finding_kind == "choice"
    )
    # Preserve the accepted V2.0 direct clustering API only when no current
    # candidate was supplied. V2.1 orchestration always supplies it and never
    # promotes action advice into a selectable outcome.
    legacy_actions = _distinct_outcomes(
        finding.action for finding in group if finding.action
    ) if not current_candidate and not proposals else []
    current = _distinct_outcomes([current_candidate])
    outcomes = _distinct_outcomes([*current, *proposals]) if proposals else legacy_actions
    position_groups: dict[tuple[str, str], list[FindingV2]] = defaultdict(list)
    for finding in group:
        position_value = (
            outcome_key(finding.proposed_value)
            if finding.finding_kind == "choice" and finding.proposed_value
            else outcome_key(current_candidate)
            if finding.finding_kind == "affirmation" and current_candidate
            else outcome_key(finding.action)
            if legacy_actions and finding.action
            else finding.problem
        )
        position_groups[(finding.agent_name, position_value)].append(finding)
    positions: list[RolePosition] = []
    for (role_id, position_value), role_findings in position_groups.items():
        representative = max(role_findings, key=lambda item: item.confidence)
        is_outcome = position_value in outcomes
        positions.append(
            RolePosition(
                role_id=role_id,
                stance="accept" if is_outcome else "reject" if representative.problem else "not_applicable",
                option_id=option_id_for_action(issue_id, position_value),
                claim=representative.problem,
                evidence=list(dict.fromkeys(item.evidence for item in role_findings if item.evidence)),
                evidence_origin=representative.evidence_origin,
                constraint_tier=representative.constraint_tier,
                rule_refs=list(dict.fromkeys(ref for item in role_findings for ref in item.rule_refs)),
                confidence=max(item.confidence for item in role_findings),
                blocking=False,
            )
        )
    unique_position_ids = {position.option_id for position in positions if position.option_id}
    return IssueCluster(
        issue_id=issue_id,
        topic=first.problem or first.issue_type,
        category=family,
        source_spans=list(dict.fromkeys(finding.source_span for finding in group if finding.source_span)),
        candidate_spans=list(dict.fromkeys(finding.candidate_span for finding in group if finding.candidate_span)),
        finding_ids=[finding.finding_id for finding in group],
        participant_role_ids=list(dict.fromkeys(finding.agent_name for finding in group)),
        candidate_actions=outcomes,
        positions=positions,
        evidence=list(dict.fromkeys(finding.evidence for finding in group if finding.evidence)),
        severity=_severity(group),
        constraint_tier="advisory",
        blocking=False,
        consensus_status="disputed" if len(unique_position_ids) > 1 else "consensus",
        needs_user_input=len(outcomes) > 1,
    )


def _preflight_clusters(preflight: PreflightResult) -> list[IssueCluster]:
    clusters: list[IssueCluster] = []
    for check in preflight.checks:
        if check.status == "pass":
            continue
        issue_id = _stable_id("issue", "preflight", check.check_id)
        evidence = [*check.source_evidence, *check.candidate_evidence]
        clusters.append(
            IssueCluster(
                issue_id=issue_id,
                topic=check.message or check.kind,
                category="integrity" if check.blocking else "signal",
                source_spans=check.source_evidence,
                candidate_spans=check.candidate_evidence,
                participant_role_ids=["technical_safety_reviewer"],
                candidate_actions=["restore required source token or structure"],
                evidence=evidence,
                immutable_hard_constraints=[check.check_id] if check.blocking else [],
                severity=check.severity,
                constraint_tier="hard" if check.blocking else "advisory",
                blocking=check.blocking,
                consensus_status="consensus",
                needs_user_input=False,
            )
        )
    return clusters


def cluster_findings(
    raw_findings: Iterable[FindingV2 | dict[str, Any]],
    preflight: PreflightResult | None = None,
    *,
    current_candidate: str = "",
) -> list[IssueCluster]:
    """Cluster findings around issues, never around named production examples."""
    findings = normalize_findings(raw_findings)
    clusters = [
        _model_cluster(group, current_candidate=current_candidate)
        for group in _cluster_model_findings(findings)
        if any(finding.finding_kind != "affirmation" for finding in group)
    ]
    if preflight is not None:
        clusters = [*_preflight_clusters(preflight), *clusters]
    return sorted(clusters, key=lambda cluster: (not cluster.blocking, cluster.issue_id))
