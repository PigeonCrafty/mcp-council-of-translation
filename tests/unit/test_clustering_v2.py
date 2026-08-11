from council_of_translation.localization.clustering import cluster_findings, normalize_findings
from council_of_translation.localization.preflight import run_preflight


def _finding(agent, issue_type, source_span, candidate_span, action, **extra):
    return {
        "agent_name": agent,
        "role_perspective": agent,
        "issue_type": issue_type,
        "source_span": source_span,
        "candidate_span": candidate_span,
        "problem": f"problem from {agent}",
        "evidence": "sampled observation",
        "action": action,
        "confidence": 0.8,
        **extra,
    }


def test_same_issue_different_wording_clusters_together():
    clusters = cluster_findings(
        [
            _finding("terminology", "terminology", "account permissions", "账户权限", "使用账户权限"),
            _finding("fluency", "fluency", "permissions for account", "账号的权限", "使用账号权限"),
        ]
    )
    assert len(clusters) == 1
    assert set(clusters[0].participant_role_ids) == {"terminology", "fluency"}
    assert clusters[0].consensus_status == "disputed"


def test_different_issue_same_span_does_not_false_merge():
    clusters = cluster_findings(
        [
            _finding("technical", "technical", "{count}", "{count}", "preserve placeholder"),
            _finding("fluency", "fluency", "{count}", "{count}", "improve surrounding wording"),
        ]
    )
    assert len(clusters) == 2
    assert {cluster.category for cluster in clusters} == {"integrity", "language_choice"}


def test_model_claim_cannot_propagate_immutable_constraint():
    clusters = cluster_findings(
        [_finding("reviewer", "technical", "token", "token", "block it", blocking=True, constraint_tier="hard")]
    )
    assert clusters[0].blocking is False
    assert clusters[0].immutable_hard_constraints == []


def test_preflight_blocker_propagates_as_immutable_constraint():
    preflight = run_preflight("Delete {count}", "删除")
    clusters = cluster_findings([], preflight)
    blocker = next(cluster for cluster in clusters if cluster.blocking)
    assert blocker.constraint_tier == "hard"
    assert blocker.immutable_hard_constraints == ["braced-placeholder-parity"]
    assert blocker.needs_user_input is False


def test_finding_ids_are_stable_for_same_input():
    raw = [_finding("reviewer", "accuracy", "Save", "保存", "retain meaning")]
    first = normalize_findings(raw)[0].finding_id
    second = normalize_findings(raw)[0].finding_id
    assert first == second
