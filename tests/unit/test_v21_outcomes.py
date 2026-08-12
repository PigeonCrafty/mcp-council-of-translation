from council_of_translation.localization.clustering import cluster_findings
from council_of_translation.localization.deliberation import build_decision_points
from council_of_translation.localization.models import FindingV2


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
        current_candidate="继续",
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
    clusters = cluster_findings([finding], current_candidate="继续")
    assert clusters == []
    assert build_decision_points(clusters) == []


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
    clusters = cluster_findings([issue, choice], current_candidate="继续")
    assert build_decision_points(clusters) == []


def test_materially_distinct_punctuation_is_not_merged():
    clusters = cluster_findings(
        [_choice("ux_copy_reviewer", "下一步"), _choice("terminology_reviewer", "下一步！")],
        current_candidate="继续",
    )
    assert clusters[0].candidate_actions == ["继续", "下一步", "下一步!"]
