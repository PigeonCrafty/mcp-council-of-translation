"""Issue-centric normalization and deterministic hybrid clustering."""

from __future__ import annotations

from collections import defaultdict
import hashlib
import re
from typing import Any, Iterable

from council_of_translation.localization.models import (
    FindingV2,
    IssueCluster,
    PreflightResult,
    RolePosition,
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


def _model_cluster(group: list[FindingV2]) -> IssueCluster:
    first = group[0]
    family = _ISSUE_FAMILY[first.issue_type]
    anchors = sorted({anchor for finding in group for anchor in (finding.source_span, finding.candidate_span) if anchor})
    issue_id = _stable_id("issue", family, *anchors)
    actions = list(dict.fromkeys(finding.action for finding in group if finding.action))
    positions = [
        RolePosition(
            role_id=finding.agent_name,
            stance="reject" if finding.problem else "not_applicable",
            option_id=_stable_id("option", issue_id, finding.action or finding.problem),
            claim=finding.problem,
            evidence=[finding.evidence] if finding.evidence else [],
            confidence=finding.confidence,
            blocking=False,
        )
        for finding in group
    ]
    unique_position_ids = {position.option_id for position in positions if position.option_id}
    return IssueCluster(
        issue_id=issue_id,
        topic=first.problem or first.issue_type,
        category=family,
        source_spans=list(dict.fromkeys(finding.source_span for finding in group if finding.source_span)),
        candidate_spans=list(dict.fromkeys(finding.candidate_span for finding in group if finding.candidate_span)),
        finding_ids=[finding.finding_id for finding in group],
        participant_role_ids=list(dict.fromkeys(finding.agent_name for finding in group)),
        candidate_actions=actions,
        positions=positions,
        evidence=list(dict.fromkeys(finding.evidence for finding in group if finding.evidence)),
        severity=_severity(group),
        constraint_tier="advisory",
        blocking=False,
        consensus_status="disputed" if len(unique_position_ids) > 1 else "consensus",
        needs_user_input=len(actions) > 1 and len(unique_position_ids) > 1,
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
) -> list[IssueCluster]:
    """Cluster findings around issues, never around named production examples."""
    findings = normalize_findings(raw_findings)
    clusters = [_model_cluster(group) for group in _cluster_model_findings(findings)]
    if preflight is not None:
        clusters = [*_preflight_clusters(preflight), *clusters]
    return sorted(clusters, key=lambda cluster: (not cluster.blocking, cluster.issue_id))
