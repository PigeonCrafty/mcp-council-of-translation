from council_of_translation.localization.clustering import cluster_findings
from council_of_translation.localization.deliberation import build_decision_points
from council_of_translation.localization.models import FindingV2, option_id_for_action
from council_of_translation.localization.policy import adjudicate_decision_point


def _choice(role: str, value: str, *, action: str = "instruction") -> FindingV2:
    return FindingV2(
        agent_name=role,
        source_span="Continue",
        candidate_span="继续",
        issue_type="ux",
        severity="minor",
        problem="按钮结果存在上下文选择",
        evidence="UI button",
        action=action,
        finding_kind="choice",
        proposed_value=value,
        confidence=0.8,
    )


def test_outcomes_use_proposed_values_include_current_and_collapse_duplicates():
    clusters = cluster_findings(
        [
            _choice("ux_copy_reviewer", " 下一步 "),
            _choice("ux_copy_reviewer", "下一步", action="different advice"),
            _choice("terminology_reviewer", "下一步"),
        ],
    )
    assert len(clusters) == 1
    assert clusters[0].candidate_actions == ["继续", "下一步"]
    assert len([p for p in clusters[0].positions if p.role_id == "ux_copy_reviewer"]) == 1

    points = build_decision_points(clusters)
    assert len(points) == 1
    assert [option.label for option in points[0].options] == ["继续", "下一步"]
    assert points[0].options[0].is_current_candidate is True


def test_affirmations_create_no_cluster_or_decision_point():
    finding = FindingV2(
        agent_name="fluency_reviewer",
        source_span="Continue",
        candidate_span="继续",
        issue_type="fluency",
        finding_kind="affirmation",
        problem="当前译文自然",
    )
    clusters = cluster_findings([finding])
    assert clusters == []
    assert build_decision_points(clusters) == []


def test_affirmations_support_current_candidate_in_mixed_choice_cluster():
    affirmations = [
        FindingV2(
            agent_name=role,
            source_span="Continue",
            candidate_span="继续",
            issue_type="fluency",
            finding_kind="affirmation",
            problem="当前候选可接受",
            evidence="natural UI wording",
            confidence=0.8,
        )
        for role in (
            "fidelity_reviewer",
            "terminology_reviewer",
            "product_context_reviewer",
            "ux_copy_reviewer",
            "fluency_reviewer",
        )
    ]
    cluster = cluster_findings(
        [*affirmations, _choice("brand_voice_reviewer", "下一步")],
    )[0]
    point = build_decision_points([cluster])[0]
    current = point.options[0]
    assert current.outcome_value == "继续"
    assert set(current.support_role_ids) == {finding.agent_name for finding in affirmations}
    selected, basis, human = adjudicate_decision_point(point, cluster.positions, None)
    assert selected == current.option_id
    assert "position_matrix" in basis
    assert human is False


def test_one_valid_outcome_and_action_prose_do_not_create_decision_point():
    issue = FindingV2(
        agent_name="fluency_reviewer",
        source_span="Continue",
        candidate_span="继续",
        issue_type="fluency",
        problem="可微调",
        action="请结合页面流程考虑",
        finding_kind="issue",
    )
    choice = _choice("ux_copy_reviewer", "继续")
    clusters = cluster_findings([issue, choice])
    assert build_decision_points(clusters) == []


def test_materially_distinct_punctuation_is_not_merged():
    clusters = cluster_findings(
        [_choice("ux_copy_reviewer", "下一步"), _choice("terminology_reviewer", "下一步！")],
    )
    assert clusters[0].candidate_actions == ["继续", "下一步", "下一步!"]


def test_empty_contradictory_and_overlong_spans_do_not_invent_current_outcome():
    cases = [
        [_choice("ux_copy_reviewer", "下一步").model_copy(update={"candidate_span": ""}),
         _choice("terminology_reviewer", "前进").model_copy(update={"candidate_span": ""})],
        [_choice("ux_copy_reviewer", "下一步"),
         _choice("terminology_reviewer", "前进").model_copy(update={"candidate_span": "前进"})],
        [_choice("ux_copy_reviewer", "下一步").model_copy(update={"candidate_span": "长" * 501}),
         _choice("terminology_reviewer", "前进").model_copy(update={"candidate_span": "长" * 501})],
    ]
    for findings in cases:
        cluster = cluster_findings(findings)[0]
        assert cluster.current_outcome == ""
        assert cluster.outcome_anchor == ""
        assert cluster.candidate_actions == ["下一步", "前进"]
        point = build_decision_points([cluster])[0]
        assert all(option.is_current_candidate is False for option in point.options)


def test_issue_invalid_and_incomplete_choice_actions_never_become_outcomes():
    action = "请结合完整页面流程执行一段很长的内部评审指令"
    base = {
        "agent_name": "ux_copy_reviewer",
        "source_span": "Continue",
        "candidate_span": "继续",
        "issue_type": "ux",
        "problem": "wording issue",
        "action": action,
    }
    findings = [
        FindingV2.model_validate(base),
        FindingV2.model_validate({**base, "finding_kind": "issue"}),
        FindingV2.model_validate({**base, "finding_kind": "invalid-kind"}),
        FindingV2.model_validate({**base, "finding_kind": "choice", "proposed_value": ""}),
        FindingV2.model_validate({**base, "finding_kind": "choice", "proposed_value": 123}),
        FindingV2.model_validate({**base, "finding_kind": "choice", "proposed_value": "长" * 501}),
    ]
    for finding in findings:
        cluster = cluster_findings([finding])[0]
        assert cluster.candidate_actions == ["继续"]
        assert option_id_for_action(cluster.issue_id, action) not in {
            position.option_id for position in cluster.positions
        }
        assert build_decision_points([cluster]) == []


def test_valid_choice_with_issue_and_affirmation_keeps_only_concrete_outcomes():
    choice = _choice("ux_copy_reviewer", "下一步")
    issue = choice.model_copy(update={
        "agent_name": "product_context_reviewer",
        "finding_kind": "issue",
        "proposed_value": "",
        "action": "结合页面流程进一步判断",
    })
    affirmation = choice.model_copy(update={
        "agent_name": "fluency_reviewer",
        "finding_kind": "affirmation",
        "proposed_value": "",
        "action": "保留自然度说明",
    })
    cluster = cluster_findings([choice, issue, affirmation])[0]
    assert cluster.candidate_actions == ["继续", "下一步"]
    assert build_decision_points([cluster])[0].options[0].is_current_candidate is True
    assert all(
        action not in cluster.candidate_actions
        for action in (issue.action, affirmation.action)
    )
