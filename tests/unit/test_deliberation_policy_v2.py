import pytest

from council_of_translation.localization.deliberation import (
    MODE_SAMPLE_BUDGETS,
    SampleBudget,
    build_decision_points,
    normalize_discussion_round,
    select_discussion_issues,
)
from council_of_translation.localization.models import (
    DecisionOption,
    DecisionPoint,
    IssueCluster,
    RolePosition,
    UserDecision,
)
from council_of_translation.localization.policy import adjudicate_decision_point, build_chief_decision, policy_gate


def _issue(issue_id="issue_1", **updates):
    data = {
        "issue_id": issue_id,
        "topic": "button wording",
        "participant_role_ids": ["terminology_reviewer", "fluency_reviewer"],
        "candidate_actions": ["继续", "下一步"],
        "positions": [
            RolePosition(role_id="terminology_reviewer", stance="accept", option_id="a", evidence=["TB"], confidence=0.9),
            RolePosition(role_id="fluency_reviewer", stance="accept", option_id="b", evidence=["usage"], confidence=0.9),
        ],
        "severity": "major",
        "consensus_status": "disputed",
        "needs_user_input": True,
    }
    data.update(updates)
    return IssueCluster(**data)


def test_no_conflict_skips_discussion():
    assert select_discussion_issues([_issue(consensus_status="consensus")], "standard") == []


def test_discussion_is_bounded_by_mode_and_participants():
    issues = [_issue(f"issue_{index}", participant_role_ids=["a", "b", "c", "d", "e"]) for index in range(4)]
    standard = select_discussion_issues(issues, "standard")
    strict = select_discussion_issues(issues, "strict")
    assert len(standard) == 1 and len(standard[0].participant_role_ids) == 3
    assert len(strict) == 2 and all(len(issue.participant_role_ids) == 4 for issue in strict)


def test_discussion_trace_filters_unaffected_roles_and_hidden_fields():
    issue = _issue()
    round_ = normalize_discussion_round(
        "round_1",
        [issue],
        [
            {"issue_id": issue.issue_id, "speaker": "terminology_reviewer", "stance": "challenge", "claim": "claim", "reasoning": "hidden"},
            {"issue_id": issue.issue_id, "speaker": "unrelated", "stance": "support", "claim": "ignore"},
        ],
    )
    assert len(round_.turns) == 1
    assert "reasoning" not in round_.turns[0].model_dump()


@pytest.mark.parametrize("mode", ["lightweight", "standard", "strict"])
def test_sampling_budgets_are_hard(mode):
    budget = SampleBudget(mode)
    budget.consume(MODE_SAMPLE_BUDGETS[mode])
    with pytest.raises(RuntimeError):
        budget.consume()


def test_at_most_three_meaningful_decision_points():
    points = build_decision_points([_issue(f"issue_{index}") for index in range(5)])
    assert len(points) == 3
    assert all(len(point.options) >= 2 for point in points)


def test_user_choice_is_decisive_only_when_valid():
    point = DecisionPoint(
        decision_id="d",
        issue_id="i",
        question="q",
        options=[DecisionOption(option_id="a", label="A"), DecisionOption(option_id="bad", label="Bad", valid=False, invalid_reason="placeholder missing")],
    )
    valid_user = UserDecision(decision_id="d", selected_option_id="a", elicitation_action="accept")
    selected, basis, human = adjudicate_decision_point(point, [], valid_user)
    assert (selected, basis, human) == ("a", ["valid_user_decision"], False)

    invalid_user = UserDecision(decision_id="d", selected_option_id="bad", elicitation_action="accept")
    selected, _, human = adjudicate_decision_point(point, [], invalid_user)
    assert selected == ""
    assert human is True


def test_policy_gate_and_chief_preserve_technical_blocker():
    blocker = _issue("placeholder", blocking=True, constraint_tier="hard", immutable_hard_constraints=["placeholder-parity"], needs_user_input=False)
    gate = policy_gate([], [blocker])
    chief, trace = build_chief_decision([blocker], [], [])
    assert gate["passed"] is False
    assert chief.publishability == "需人工复核"
    assert chief.must_fix == [blocker.topic]
    assert trace.entries == []


def test_position_matrix_uses_relevance_not_raw_majority():
    point = DecisionPoint(
        decision_id="d",
        issue_id="i",
        question="q",
        options=[DecisionOption(option_id="safe", label="Safe"), DecisionOption(option_id="pretty", label="Pretty")],
    )
    positions = [
        RolePosition(role_id="technical_safety_reviewer", stance="accept", option_id="safe", evidence=["constraint"], confidence=1.0),
        RolePosition(role_id="brand_voice_reviewer", stance="accept", option_id="pretty", evidence=["style"], confidence=0.6),
        RolePosition(role_id="fluency_reviewer", stance="accept", option_id="pretty", evidence=["usage"], confidence=0.6),
    ]
    selected, basis, _ = adjudicate_decision_point(point, positions, None)
    assert selected == "safe"
    assert "position_matrix" in basis
