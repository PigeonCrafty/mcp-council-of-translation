from council_of_translation.localization.clustering import cluster_findings
from council_of_translation.localization.deliberation import build_decision_points
from council_of_translation.localization.models import FindingV2
from council_of_translation.localization.orchestration import (
    _decisions_from_elicitation,
    _form_mapping,
    _interaction_form,
    _interaction_message,
)
from council_of_translation.localization.runtime import ElicitationResult


def _continue_point():
    findings = [
        FindingV2(
            agent_name="ux_copy_reviewer",
            source_span="Continue",
            candidate_span="继续",
            issue_type="ux",
            severity="minor",
            finding_kind="choice",
            proposed_value="下一步",
            problem="UI outcome choice",
            evidence="navigation context",
            action="Consider the next screen",
            confidence=0.9,
        )
    ]
    return build_decision_points(
        cluster_findings(findings, current_candidate="继续")
    )[0]


def test_continue_form_uses_readable_outcomes_and_safe_round_trip_values():
    point = _continue_point()
    mapping = _form_mapping(point)
    schema = _interaction_form([point]).model_json_schema()["properties"][point.decision_id]
    assert schema["enum"] == list(mapping)
    assert len(mapping) == 3
    assert all(value.startswith(("choice_", "delegate_")) for value in mapping)
    assert all(option.option_id not in schema["description"] for option in point.options)
    assert "继续" in schema["description"]
    assert "下一步" in schema["description"]
    assert "暂不决定，由 Council 裁决" in schema["description"]
    message = _interaction_message([point])
    assert "继续" in message and "下一步" in message
    assert all(option.option_id not in message for option in point.options)

    alternative_value = next(
        value for value, option in mapping.items()
        if option is not None and option.outcome_value == "下一步"
    )
    decision = _decisions_from_elicitation(
        [point], ElicitationResult(action="accept", data={point.decision_id: alternative_value})
    )[0]
    assert decision.elicitation_action == "accept"
    assert decision.selected_outcome_value == "下一步"
    assert decision.selected_option_id == point.options[1].option_id


def test_explicit_delegation_is_distinct_from_failure_and_bad_values_are_rejected():
    point = _continue_point()
    delegate_value = next(value for value, option in _form_mapping(point).items() if option is None)
    delegated = _decisions_from_elicitation(
        [point], ElicitationResult(action="accept", data={point.decision_id: delegate_value})
    )[0]
    assert delegated.elicitation_action == "delegate"
    assert delegated.selection_kind == "council_delegation"

    for data in ({}, {point.decision_id: "stale_value"}, {"wrong_point": delegate_value}):
        decision = _decisions_from_elicitation(
            [point], ElicitationResult(action="accept", data=data)
        )[0]
        assert decision.elicitation_action == "malformed"


def test_batched_duplicate_or_mismatched_values_are_rejected():
    first = _continue_point()
    second = first.model_copy(deep=True)
    second.decision_id = "decision_second"
    first_value = next(iter(_form_mapping(first)))
    decisions = _decisions_from_elicitation(
        [first, second],
        ElicitationResult(
            action="accept",
            data={first.decision_id: first_value, second.decision_id: first_value},
        ),
    )
    assert [decision.elicitation_action for decision in decisions] == ["malformed", "malformed"]
