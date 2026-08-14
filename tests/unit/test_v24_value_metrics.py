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


def _technical_anchor_finding(source_span="", candidate_span=""):
    return FindingV2(
        agent_name="technical_safety_reviewer",
        issue_type="technical",
        severity="critical",
        source_span=source_span,
        candidate_span=candidate_span,
        problem="Deterministic structure differs",
        evidence="bounded reviewer evidence",
        action="Restore the required source structure",
    )


def _preflight_metrics(preflight, finding=None, *, status="structured_success"):
    role = "technical_safety_reviewer"
    clusters = cluster_findings([finding] if finding else [], preflight)
    before = [cluster.model_dump(mode="json") for cluster in clusters]
    metrics = compute_council_value_metrics(
        active_role_ids=[role],
        independent_reviews=[_review(role, status=status)],
        clusters=clusters,
        discussion_rounds=[],
    )
    assert [cluster.model_dump(mode="json") for cluster in clusters] == before
    return clusters, metrics


def test_required_and_forbidden_literals_correlate_only_by_exact_literal():
    required_clusters, required = _preflight_metrics(
        run_preflight("Launch", "启动", hard_constraints=["required_literal:Acme"]),
        _technical_anchor_finding(source_span="Acme"),
    )
    forbidden_clusters, forbidden = _preflight_metrics(
        run_preflight("Safe", "危险", hard_constraints=["forbidden_literal:危险"]),
        _technical_anchor_finding(candidate_span="危险"),
    )

    assert len(required_clusters) == len(forbidden_clusters) == 2
    assert required.unique_material_issue_count == 1
    assert forbidden.unique_material_issue_count == 1


def test_numeric_parity_and_exact_reviewer_anchor_count_once():
    clusters, metrics = _preflight_metrics(
        run_preflight("Keep 10 files", "保留 9 个文件", hard_constraints=["numeric_parity"]),
        _technical_anchor_finding(source_span="10"),
    )

    assert len(clusters) == 2
    assert metrics.unique_material_issue_count == 1
    assert metrics.role_contributions[0].unique_issue_count == 1


def test_each_markdown_signal_correlates_by_exact_structured_anchor():
    cases = [
        ("# Title", "标题", "heading"),
        ("- Item", "项目", "list"),
        ("[Docs](docs)", "文档", "link"),
        ("```\ncode\n```", "代码", "fence"),
    ]
    for source, candidate, signal in cases:
        clusters, metrics = _preflight_metrics(
            run_preflight(source, candidate, hard_constraints=["markdown_parity"]),
            _technical_anchor_finding(source_span=signal),
        )
        assert len(clusters) == 2
        assert metrics.unique_material_issue_count == 1


def test_explicit_dnt_and_matching_reviewer_anchor_count_once():
    clusters, metrics = _preflight_metrics(
        run_preflight("Open Pigeon", "打开", do_not_translate=["Pigeon"]),
        _technical_anchor_finding(source_span="Pigeon"),
    )

    assert len(clusters) == 2
    assert metrics.unique_material_issue_count == 1


def test_overlapping_url_scanners_keep_clusters_but_count_one_issue():
    clusters, metrics = _preflight_metrics(
        run_preflight("Visit https://example.com", "访问"),
    )

    assert len(clusters) == 2
    assert {span for cluster in clusters for span in cluster.source_spans} == {
        "/example", "https://example.com"
    }
    assert metrics.unique_material_issue_count == 1


def test_distinct_placeholder_url_and_caller_literals_do_not_overmerge():
    token_clusters, token_metrics = _preflight_metrics(
        run_preflight("Delete {count} at https://example.com", "删除"),
    )
    literal_clusters, literal_metrics = _preflight_metrics(
        run_preflight(
            "Launch",
            "启动",
            hard_constraints=["required_literal:Acme", "required_literal:Beta"],
        ),
    )

    assert len(token_clusters) == 3
    assert token_metrics.unique_material_issue_count == 2
    assert len(literal_clusters) == 2
    assert literal_metrics.unique_material_issue_count == 2


def test_cross_family_model_clusters_keep_production_identity_at_same_span():
    roles = ["fidelity_reviewer", "terminology_reviewer"]
    findings = [
        FindingV2(
            agent_name=roles[0], issue_type="accuracy", severity="major",
            source_span="Continue", candidate_span="继续", problem="Meaning risk",
            evidence="semantic comparison", action="Correct the meaning",
        ),
        FindingV2(
            agent_name=roles[1], issue_type="terminology", severity="major",
            source_span="Continue", candidate_span="继续", problem="Term policy",
            evidence="terminology policy", action="Apply the approved term",
        ),
    ]
    clusters = cluster_findings(findings)
    metrics = compute_council_value_metrics(
        active_role_ids=roles,
        independent_reviews=[_review(role) for role in roles],
        clusters=clusters,
        discussion_rounds=[],
    )

    assert len(clusters) == 2
    assert {cluster.category for cluster in clusters} == {"correctness", "language_choice"}
    assert metrics.unique_material_issue_count == 2
    assert metrics.corroborated_issue_count == 0
    assert [item.contribution_kind for item in metrics.role_contributions] == [
        "unique_material", "unique_material"
    ]
    assert [item.unique_issue_count for item in metrics.role_contributions] == [1, 1]


def test_same_family_model_findings_keep_production_corroboration_identity():
    roles = ["fidelity_reviewer", "risk_ambiguity_reviewer"]
    clusters = cluster_findings([
        _finding(roles[0]),
        _finding(roles[1], problem="The same reversal creates a material risk"),
    ])
    metrics = compute_council_value_metrics(
        active_role_ids=roles,
        independent_reviews=[_review(role) for role in roles],
        clusters=clusters,
        discussion_rounds=[],
    )

    assert len(clusters) == 1
    assert metrics.unique_material_issue_count == 0
    assert metrics.corroborated_issue_count == 1
    assert [item.contribution_kind for item in metrics.role_contributions] == [
        "corroborating", "corroborating"
    ]


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


def test_live_shaped_case_b_paraphrases_do_not_manufacture_new_evidence():
    roles = ["technical_safety_reviewer", "fidelity_reviewer"]
    clusters = cluster_findings([
        FindingV2(
            agent_name=role,
            issue_type="accuracy",
            severity="major",
            source_span="Delete {count} files? This action cannot be undone.",
            candidate_span="删除文件吗？此操作可以撤销。",
            problem="The protected meaning and placeholder differ",
            evidence="Project rule requires {count} and permanent-delete meaning",
            action="Restore the protected facts",
            rule_refs=["required_literal:{count}", "project_rule:permanent_delete"],
        )
        for role in roles
    ])
    issue_id = clusters[0].issue_id
    turns = [
        {
            "issue_id": issue_id,
            "speaker": roles[index % 2],
            "claim": f"Existing fact restated {index}",
            "evidence": [evidence],
            "position_changed": False,
        }
        for index, evidence in enumerate([
            "The {count} placeholder must remain.",
            "Permanent deletion is the supplied context.",
            "Cannot must not become can.",
            "The existing project rule forbids reversibility.",
            "Keep {count} exactly as already required.",
            "The permanent-delete and cannot facts are unchanged.",
        ])
    ]
    round_ = normalize_discussion_round("round_1", clusters, turns)
    metrics = compute_council_value_metrics(
        active_role_ids=roles,
        independent_reviews=[_review(role) for role in roles],
        clusters=clusters,
        discussion_rounds=[round_],
    )

    assert metrics.discussion_new_evidence_count == 0
    assert metrics.discussion_position_change_count == 0
    assert metrics.discussion_resolved_issue_count == 0
    assert metrics.discussion_marginal_value == "none"


def test_existing_structured_evidence_repeated_across_rounds_stays_zero():
    roles = ["fidelity_reviewer", "risk_ambiguity_reviewer"]
    clusters = cluster_findings([_finding(roles[0]), _finding(roles[1])])
    cluster = clusters[0].model_copy(update={"evidence": ["{count}"]})
    rounds = [
        normalize_discussion_round(
            f"round_{index}",
            [cluster],
            [{
                "issue_id": cluster.issue_id,
                "speaker": roles[index % 2],
                "evidence": ["Existing anchor {count} is unchanged"],
            }],
        )
        for index in range(3)
    ]
    metrics = compute_council_value_metrics(
        active_role_ids=roles,
        independent_reviews=[_review(role) for role in roles],
        clusters=[cluster],
        discussion_rounds=rounds,
    )

    assert metrics.discussion_new_evidence_count == 0
    assert metrics.discussion_marginal_value == "none"


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
            "evidence": ["https://example.com/new-ui-flow"], "position_changed": False,
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
