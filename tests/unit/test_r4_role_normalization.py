from council_of_translation.localization.clustering import cluster_findings
from council_of_translation.localization.deliberation import build_decision_points
from council_of_translation.localization.models import FindingV2
from council_of_translation.localization.policy import _matrix_scores, adjudicate_decision_point


def _finding(role: str, action: str) -> FindingV2:
    return FindingV2(
        agent_name=role,
        role_perspective=role,
        source_span="Continue",
        candidate_span="继续",
        issue_type="terminology" if role == "terminology_reviewer" else "fluency",
        problem="wording choice",
        evidence="observable wording evidence",
        action=action,
        confidence=0.8,
    )


def _cluster(fluency_duplicates: int):
    return cluster_findings(
        [
            _finding("terminology_reviewer", "继续"),
            *[_finding("fluency_reviewer", "下一步") for _ in range(fluency_duplicates)],
        ]
    )[0]


def test_one_and_five_identical_same_role_findings_have_identical_scores_and_selection():
    one = _cluster(1)
    five = _cluster(5)
    one_point = build_decision_points([one])[0]
    five_point = build_decision_points([five])[0]

    one_scores = _matrix_scores(one.positions, {option.option_id for option in one_point.options})
    five_scores = _matrix_scores(five.positions, {option.option_id for option in five_point.options})
    one_result = adjudicate_decision_point(one_point, one.positions, None)
    five_result = adjudicate_decision_point(five_point, five.positions, None)

    assert one_scores == five_scores
    assert one_result == five_result
    assert one_result[0] == next(option.option_id for option in one_point.options if option.label == "继续")
    assert len(one.positions) == len(five.positions) == 2
    assert len(five.finding_ids) == 6


def test_one_role_with_distinct_actions_has_fixed_normalized_influence_and_ties_conservatively():
    one_each = cluster_findings(
        [_finding("terminology_reviewer", "继续"), _finding("terminology_reviewer", "下一步")]
    )[0]
    repeated = cluster_findings(
        [*[_finding("terminology_reviewer", "继续") for _ in range(5)], _finding("terminology_reviewer", "下一步")]
    )[0]
    one_point = build_decision_points([one_each])[0]
    repeated_point = build_decision_points([repeated])[0]

    one_scores = _matrix_scores(one_each.positions, {option.option_id for option in one_point.options})
    repeated_scores = _matrix_scores(repeated.positions, {option.option_id for option in repeated_point.options})

    assert one_scores == repeated_scores
    assert len(one_each.positions) == len(repeated.positions) == 2
    assert len({abs(score) for score in one_scores.values()}) == 1
    assert adjudicate_decision_point(repeated_point, repeated.positions, None) == (
        "",
        ["indistinguishable_or_insufficient_valid_evidence"],
        True,
    )
