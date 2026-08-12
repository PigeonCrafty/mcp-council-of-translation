from council_of_translation.localization.clustering import cluster_findings
from council_of_translation.localization.deliberation import build_decision_points
from council_of_translation.localization.models import FindingV2
from council_of_translation.localization.orchestration import (
    _decisions_from_elicitation,
    _form_mapping,
    _interaction_form,
    _interaction_message,
    normalize_continuation_decisions,
    run_structured_review,
)
from council_of_translation.localization.models import ReviewRecordV2, ReviewTaskV2
from council_of_translation.localization.models import DecisionOption, DecisionPoint
from council_of_translation.localization.persistence import ReviewStore
from council_of_translation.localization.runtime import (
    ElicitationResult,
    RuntimeTelemetry,
    ScriptedModelExecutor,
    ScriptedUserInteractionGateway,
)
import asyncio
import json


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


def test_production_path_rejects_proposal_that_loses_required_placeholder(tmp_path):
    proposal = {
        "source_span": "Continue {count}",
        "candidate_span": "继续 {count}",
        "issue_type": "ux",
        "severity": "minor",
        "finding_kind": "choice",
        "proposed_value": "下一步",
        "problem": "wording choice",
        "evidence": "UI context",
        "action": "consider navigation wording",
        "confidence": 0.8,
    }
    scripts = [
        json.dumps({"role_feedback": "checked", "findings": [proposal]}),
        *[json.dumps({"role_feedback": "clean", "findings": []}) for _ in range(5)],
    ]
    telemetry = RuntimeTelemetry(sample_budget=10)
    gateway = ScriptedUserInteractionGateway(supported=True, telemetry=telemetry)
    record = asyncio.run(run_structured_review(
        ReviewTaskV2(
            source_text="Continue {count}",
            candidate_translation="继续 {count}",
            content_type="ui",
        ),
        ScriptedModelExecutor(scripts, telemetry),
        gateway,
        store=ReviewStore(tmp_path / "records", legacy_dir=tmp_path / "legacy"),
    ))
    assert record.decision_points == []
    assert gateway.requests == []
    assert record.runtime_metadata.sampling_calls == 6


def test_continuation_derives_exact_outcome_and_rejects_duplicate_points():
    point = _continue_point()
    parent = ReviewRecordV2(
        review_id="20260812T010203000004Z_ab12cd34",
        task=ReviewTaskV2(),
        decision_points=[point],
    )
    selected = point.options[1]
    decisions = normalize_continuation_decisions(parent, [{
        "decision_id": point.decision_id,
        "selected_option_id": selected.option_id,
        "selected_outcome_value": "MISMATCHED CALLER VALUE",
    }])
    assert decisions[0].selected_outcome_value == selected.outcome_value
    assert decisions[0].selection_kind == "outcome"

    import pytest
    with pytest.raises(ValueError, match="duplicate decision_id"):
        normalize_continuation_decisions(parent, [
            {"decision_id": point.decision_id, "selected_option_id": selected.option_id},
            {"decision_id": point.decision_id, "selected_option_id": point.options[0].option_id},
        ])


def test_hostile_unicode_form_is_bounded_to_three_points_and_four_choices():
    points = [
        DecisionPoint(
            decision_id=f"decision_{index}",
            issue_id=f"issue_{index}",
            question="问" * 1000,
            options=[
                DecisionOption(
                    option_id=f"option_{index}_{choice}",
                    outcome_value=f"结果{choice}",
                    label="👩🏽‍💻" * 100,
                    description="描" * 1000,
                )
                for choice in range(8)
            ],
        )
        for index in range(5)
    ]
    schema = _interaction_form(points).model_json_schema()
    assert len(schema["properties"]) == 3
    assert all(len(field["enum"]) <= 4 for field in schema["properties"].values())
    assert all(len(point.question) <= 240 for point in points)
    assert all(len(option.label) <= 48 and len(option.description) <= 160 for point in points for option in point.options)
