from council_of_translation.localization.guided import (
    BRIEF_FIELDS,
    build_briefing_form,
    build_context_gap_form,
)
from council_of_translation.localization.models import (
    ContextGapV2,
    DecisionOption,
    DecisionPoint,
)
from council_of_translation.localization.orchestration import (
    _decisions_from_elicitation,
    _form_mapping,
    _interaction_form,
)
from council_of_translation.localization.runtime import ElicitationResult


def _assert_flat_bounded(schema):
    assert 1 <= len(schema["properties"]) <= 6
    serialized = str(schema)
    assert "issue_" not in serialized and "decision_" not in serialized and "option_" not in serialized
    for field in schema["properties"].values():
        assert len(field.get("title", "")) <= 48
        assert len(field.get("description", "")) <= 160
        assert field.get("title", "") not in field.get("description", "")
        assert field.get("type") in {"string", None}


def test_briefing_and_context_forms_are_flat_bounded_and_nonrepeating():
    brief = build_briefing_form(list(BRIEF_FIELDS)).model_json_schema()
    _assert_flat_bounded(brief)
    assert len(brief["properties"]) == 6

    context_form, mapping = build_context_gap_form([
        ContextGapV2(
            gap_id="gap_aaaaaaaaaaaa",
            question="问" * 1_000,
            materiality="答案会改变判断" * 100,
            affected_role_ids=["fidelity_reviewer"],
        ),
        ContextGapV2(
            gap_id="gap_bbbbbbbbbbbb",
            question="目标用户的专业程度？",
            materiality="答案会改变术语建议",
            affected_role_ids=["terminology_reviewer"],
        ),
    ])
    schema = context_form.model_json_schema()
    _assert_flat_bounded(schema)
    assert list(schema["properties"]) == ["context_1", "context_2"]
    assert list(mapping) == ["context_1", "context_2"]


def test_outcome_form_has_deterministic_human_title_and_exact_round_trip():
    point = DecisionPoint(
        decision_id="decision_aaaaaaaaaaaa",
        issue_id="issue_aaaaaaaaaaaa",
        question="“Continue” 的措辞结果",
        options=[
            DecisionOption(
                option_id="option_111111111111", outcome_value="继续", label="继续",
                description="保留当前候选译文", is_current_candidate=True,
            ),
            DecisionOption(
                option_id="option_222222222222", outcome_value="下一步", label="下一步",
                description="采用候选结果：下一步",
            ),
        ],
    )
    schema = _interaction_form([point]).model_json_schema()
    _assert_flat_bounded(schema)
    assert list(schema["properties"]) == ["review_choice_1"]
    assert "reviewer problem" not in str(schema)

    selected = next(
        value for value, option in _form_mapping(point).items()
        if option is not None and option.outcome_value == "下一步"
    )
    decisions = _decisions_from_elicitation(
        [point], ElicitationResult(action="accept", data={"review_choice_1": selected})
    )
    assert decisions[0].selected_option_id == "option_222222222222"
    assert decisions[0].selected_outcome_value == "下一步"
