from council_of_translation.localization.clustering import cluster_findings
from council_of_translation.localization.deliberation import apply_discussion_updates, normalize_discussion_round
from council_of_translation.localization.models import FindingV2
from council_of_translation.localization.preflight import run_preflight
from council_of_translation.localization.value_metrics import compute_council_value_metrics


def _review(role_id, *, status="structured_success"):
    return {"agent_name": role_id, "sample_status": status}


def _finding(role_id, *, problem="Meaning is reversed", evidence="source and candidate differ"):
    return FindingV2(
        agent_name=role_id,
        issue_type="accuracy",
        severity="major",
        source_span="Enable sync",
        candidate_span="禁用同步",
        problem=problem,
        evidence=evidence,
        action="Correct the meaning",
        confidence=0.9,
    )


def test_duplicate_and_rephrased_same_role_findings_count_once():
    roles = ["fidelity_reviewer", "fluency_reviewer"]
    clusters = cluster_findings([
        _finding(roles[0]),
        _finding(roles[0]),
        _finding(roles[0], problem="The candidate reverses the source meaning"),
    ])
    metrics = compute_council_value_metrics(
        active_role_ids=roles,
        independent_reviews=[_review(role) for role in roles],
        clusters=clusters,
        discussion_rounds=[],
    )

    fidelity, fluency = metrics.role_contributions
    assert len(clusters) == 1
    assert fidelity.contribution_kind == "unique_material"
    assert fidelity.unique_issue_count == fidelity.material_finding_count == 1
    assert fluency.contribution_kind == "confirmation_only"
    assert metrics.unique_material_issue_count == 1


def test_corroboration_and_unavailable_priority_are_deterministic():
    roles = ["fidelity_reviewer", "risk_ambiguity_reviewer", "fluency_reviewer"]
    clusters = cluster_findings([_finding(roles[0]), _finding(roles[1])])
    metrics = compute_council_value_metrics(
        active_role_ids=roles,
        independent_reviews=[_review(roles[0]), _review(roles[1], status="unavailable"), _review(roles[2])],
        clusters=clusters,
        discussion_rounds=[],
    )

    assert [item.contribution_kind for item in metrics.role_contributions] == [
        "corroborating", "unavailable", "confirmation_only"
    ]
    assert metrics.corroborated_issue_count == 1
    assert metrics.unavailable_role_count == 1


def test_preflight_placeholder_is_material_and_correlates_exact_model_support_once():
    role = "technical_safety_reviewer"
    preflight = run_preflight("Delete {count} files", "删除文件")
    findings = [FindingV2(
        agent_name=role,
        issue_type="technical",
        severity="critical",
        source_span="{count}",
        candidate_span="",
        problem="Required placeholder is missing",
        evidence="{count}",
        action="Restore the placeholder",
    )]
    clusters = cluster_findings(findings, preflight)
    metrics = compute_council_value_metrics(
        active_role_ids=[role],
        independent_reviews=[_review(role)],
        clusters=clusters,
        discussion_rounds=[],
    )

    contribution = metrics.role_contributions[0]
    assert len(clusters) == 2
    assert contribution.contribution_kind == "unique_material"
    assert contribution.unique_issue_count == contribution.material_finding_count == 1
    assert metrics.unique_material_issue_count == 1


def test_preflight_markup_is_material_when_technical_sample_is_unavailable():
    role = "technical_safety_reviewer"
    clusters = cluster_findings([], run_preflight("Click <b>Save</b>", "点击保存"))
    metrics = compute_council_value_metrics(
        active_role_ids=[role],
        independent_reviews=[_review(role, status="unavailable")],
        clusters=clusters,
        discussion_rounds=[],
    )

    contribution = metrics.role_contributions[0]
    assert contribution.contribution_kind == "unavailable"
    assert contribution.unique_issue_count == contribution.material_finding_count == 1
    assert metrics.unique_material_issue_count == 1
    assert metrics.unavailable_role_count == 1


def test_rephrased_discussion_claim_alone_has_no_marginal_value():
    roles = ["fidelity_reviewer", "risk_ambiguity_reviewer"]
    clusters = cluster_findings([_finding(roles[0]), _finding(roles[1])])
    round_ = normalize_discussion_round(
        "round_1",
        clusters,
        [{
            "issue_id": clusters[0].issue_id,
            "speaker": roles[0],
            "claim": "The wording is different but no trace delta was supplied",
            "evidence": [],
            "position_changed": False,
        }],
    )
    metrics = compute_council_value_metrics(
        active_role_ids=roles,
        independent_reviews=[_review(role) for role in roles],
        clusters=clusters,
        discussion_rounds=[round_],
    )

    assert metrics.discussion_marginal_value == "none"
    assert metrics.discussion_new_evidence_count == 0


def test_new_evidence_is_low_value_and_real_resolution_is_material():
    roles = ["terminology_reviewer", "fluency_reviewer"]
    findings = [
        FindingV2(
            agent_name=roles[0], issue_type="terminology", severity="minor",
            source_span="Continue", candidate_span="继续", problem="wording choice",
            evidence="glossary allows both", finding_kind="choice", proposed_value="继续",
        ),
        FindingV2(
            agent_name=roles[1], issue_type="fluency", severity="minor",
            source_span="Continue", candidate_span="继续", problem="wording choice",
            evidence="both are natural", finding_kind="choice", proposed_value="下一步",
        ),
    ]
    clusters = cluster_findings(findings)
    cluster = clusters[0]
    evidence_round = normalize_discussion_round(
        "round_1", clusters, [{
            "issue_id": cluster.issue_id, "speaker": roles[0],
            "evidence": ["UI flow proceeds to a new step"], "position_changed": False,
        }]
    )
    low = compute_council_value_metrics(
        active_role_ids=roles,
        independent_reviews=[_review(role) for role in roles],
        clusters=clusters,
        discussion_rounds=[evidence_round],
    )
    assert low.discussion_marginal_value == "low"
    assert low.discussion_new_evidence_count == 1

    resolution_round = normalize_discussion_round(
        "round_2", clusters, [{
            "issue_id": cluster.issue_id, "speaker": roles[1],
            "proposed_action": "继续", "position_changed": True,
        }]
    )
    assert apply_discussion_updates(clusters, resolution_round) == 1
    material = compute_council_value_metrics(
        active_role_ids=roles,
        independent_reviews=[_review(role) for role in roles],
        clusters=clusters,
        discussion_rounds=[resolution_round],
    )
    assert material.discussion_marginal_value == "material"
    assert material.discussion_position_change_count == 1
    assert material.discussion_resolved_issue_count == 1
