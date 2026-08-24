import pytest

from council_of_translation.localization.models import RoleDefinition
from council_of_translation.localization.roles import (
    CHIEF_EDITOR,
    REVIEWER_ROLES,
    ROLE_DEFINITIONS,
    ROLE_REGISTRY,
    ROUTING_PORTFOLIOS,
    SAMPLE_BUDGETS,
    build_council_plan,
    get_reviewers_for_mode,
    get_reviewers_for_plan,
    normalize_content_type,
    routing_profile_for,
)


def _ids(roles):
    return [role.id for role in roles]


def test_registry_contains_data_backed_roles_with_unique_ids():
    assert len(ROLE_DEFINITIONS) == 9
    assert len(ROLE_REGISTRY) == len(ROLE_DEFINITIONS)
    assert len({role.id for role in ROLE_DEFINITIONS}) == len(ROLE_DEFINITIONS)

    for role in ROLE_DEFINITIONS:
        assert isinstance(role, RoleDefinition)
        assert role.scope
        assert role.must_check
        assert role.must_not_decide
        assert role.evidence_policy
        assert role.applicable_modes
        assert role.applicable_content_types
        assert role.output_contract_version == "2.0"
        assert role.prompt_version == "2.0"


def test_chief_editor_is_adjudicator_and_never_selected_as_reviewer():
    assert CHIEF_EDITOR.role_type == "adjudicator"
    assert CHIEF_EDITOR.discussion_policy == "adjudicate"
    assert "count_raw_votes" in CHIEF_EDITOR.must_not_decide

    for mode in ("lightweight", "standard", "strict"):
        assert "chief_editor" not in _ids(get_reviewers_for_mode(mode))
    assert all(role.role_type == "reviewer" for role in REVIEWER_ROLES)


def test_role_permissions_evidence_and_blockers_are_specific_and_conservative():
    technical = ROLE_REGISTRY["technical_safety_reviewer"]
    terminology = ROLE_REGISTRY["terminology_reviewer"]
    fluency = ROLE_REGISTRY["fluency_reviewer"]

    assert "placeholder_parity" in technical.must_check
    assert any("preflight" in policy.lower() for policy in technical.evidence_policy)
    assert all("caller_or_preflight" in condition for condition in technical.blocking_conditions)
    assert "claim_hard_tb_violation_without_explicit_tb_evidence" in terminology.must_not_decide
    assert "explicit_hard_tb_or_project_rule_violation" in terminology.blocking_conditions
    assert fluency.blocking_conditions == []
    assert "promote_style_preference_to_blocker" in fluency.must_not_decide


def test_legacy_reviewer_attributes_remain_read_only_views():
    role = REVIEWER_ROLES[0]
    assert role.agent_name == role.id
    assert role.role == role.display_name
    assert role.role_mission == role.mission
    assert role.review_focus.endswith("。")
    assert role.modes == tuple(role.applicable_modes)


@pytest.mark.parametrize(
    ("mode", "expected_ids", "budget"),
    [
        (
            "lightweight",
            ["technical_safety_reviewer", "fidelity_reviewer", "terminology_reviewer", "fluency_reviewer"],
            6,
        ),
        (
            "standard",
            [
                "technical_safety_reviewer",
                "fidelity_reviewer",
                "terminology_reviewer",
                "product_context_reviewer",
                "ux_copy_reviewer",
                "fluency_reviewer",
            ],
            13,
        ),
        ("strict", _ids(REVIEWER_ROLES), 18),
    ],
)
def test_mode_plans_are_deterministic_and_preserve_budgets(mode, expected_ids, budget):
    first = build_council_plan(mode)
    second = build_council_plan(mode)

    assert first == second
    assert first.active_role_ids == expected_ids
    assert first.sample_budget == budget == SAMPLE_BUDGETS[mode]
    assert first.max_decision_points == 3
    assert first.max_discussion_rounds == (0 if mode == "lightweight" else 1)


def test_content_routing_is_deterministic_and_role_data_backed():
    ui = build_council_plan("strict", "product-ui")
    marketing = build_council_plan("strict", "marketing copy")
    technical_docs = build_council_plan("strict", "docs")

    assert ui.content_type == "ui"
    assert ui.active_role_ids == [
        "technical_safety_reviewer",
        "fidelity_reviewer",
        "terminology_reviewer",
        "product_context_reviewer",
        "ux_copy_reviewer",
        "fluency_reviewer",
    ]
    assert marketing.active_role_ids == [
        "fidelity_reviewer",
        "terminology_reviewer",
        "product_context_reviewer",
        "brand_voice_reviewer",
        "risk_ambiguity_reviewer",
        "fluency_reviewer",
    ]
    assert technical_docs.active_role_ids == [
        "technical_safety_reviewer",
        "fidelity_reviewer",
        "terminology_reviewer",
        "product_context_reviewer",
        "fluency_reviewer",
    ]

    for role in get_reviewers_for_plan("strict", ui.content_type):
        assert "*" in role.applicable_content_types or ui.content_type in role.applicable_content_types


def test_marketing_route_is_exact_for_each_mode_and_strict_preserves_relative_order():
    frozen = [
        "fidelity_reviewer",
        "terminology_reviewer",
        "product_context_reviewer",
        "brand_voice_reviewer",
        "risk_ambiguity_reviewer",
        "fluency_reviewer",
    ]
    lightweight = build_council_plan("lightweight", "marketing")
    standard = build_council_plan("standard", "marketing")
    strict = build_council_plan("strict", "marketing")
    assert lightweight.active_role_ids == [
        "fidelity_reviewer", "terminology_reviewer", "fluency_reviewer"
    ]
    assert standard.active_role_ids == frozen
    assert [role for role in strict.active_role_ids if role in frozen] == frozen
    assert strict.active_role_ids == frozen
    assert (lightweight.sample_budget, standard.sample_budget, strict.sample_budget) == (6, 13, 18)


def test_unknown_content_and_mode_fall_back_without_empty_council():
    assert normalize_content_type("new-content-kind") == "unspecified"
    plan = build_council_plan("not-a-mode", "new-content-kind")
    assert plan.mode == "standard"
    assert plan.content_type == "unspecified"
    assert plan.active_role_ids == _ids(get_reviewers_for_mode("standard"))
    assert plan.sample_budget == 13


def test_interaction_toggle_does_not_change_role_or_budget_routing():
    auto = build_council_plan("standard", "ui", interactive_mode="auto")
    off = build_council_plan("standard", "ui", interactive_mode="off")

    assert auto.interactive_enabled is True
    assert off.interactive_enabled is False
    assert auto.active_role_ids == off.active_role_ids
    assert auto.sample_budget == off.sample_budget == 13


def test_all_fifteen_profiles_are_explicit_deterministic_and_registry_backed():
    contents = ("unspecified", "ui", "marketing", "technical_documentation", "legal_risk")
    modes = ("lightweight", "standard", "strict")
    observed = {}
    for content in contents:
        for mode in modes:
            first = build_council_plan(mode, content)
            second = build_council_plan(mode, content)
            expected_profile = f"route_{content}_{mode}_v1"
            assert first == second
            assert first.routing_profile == expected_profile == routing_profile_for(mode, content)
            assert first.active_role_ids == list(ROUTING_PORTFOLIOS[expected_profile])
            assert all(role_id in ROLE_REGISTRY for role_id in first.active_role_ids)
            assert first.routing_reason_codes[:2] == [f"content_{content}", f"mode_{mode}"]
            assert "deterministic_preflight_coverage" in first.routing_reason_codes
            observed[first.routing_profile] = tuple(first.active_role_ids)
    assert len(observed) == len(ROUTING_PORTFOLIOS) == 15


def test_council_plan_routing_provenance_rejects_arbitrary_prose_and_role_ids():
    from council_of_translation.localization.models import CouncilPlan

    hostile = CouncilPlan.model_validate({
        "routing_profile": "PRIVATE caller prose / arbitrary_profile",
        "routing_reason_codes": [
            "content_ui", "PRIVATE user explanation", "fidelity_reviewer", "content_ui",
        ],
    })
    assert hostile.routing_profile == "legacy_unrecorded"
    assert hostile.routing_reason_codes == ["legacy_routing_unrecorded"]

    legacy = CouncilPlan.model_validate({"mode": "standard", "active_role_ids": ["unknown"]})
    assert legacy.routing_profile == "legacy_unrecorded"
    assert legacy.routing_reason_codes == ["legacy_routing_unrecorded"]
