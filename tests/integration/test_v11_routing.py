from council_of_translation.localization.roles import (
    REVIEWER_ROLES,
    ROLE_DEFINITIONS,
    ROLE_REGISTRY,
    ROUTING_PORTFOLIOS,
    build_council_plan,
)


LEGAL_PORTFOLIOS = {
    "lightweight": [
        "fidelity_reviewer",
        "terminology_reviewer",
        "risk_ambiguity_reviewer",
        "fluency_reviewer",
    ],
    "standard": [
        "fidelity_reviewer",
        "terminology_reviewer",
        "product_context_reviewer",
        "ux_copy_reviewer",
        "risk_ambiguity_reviewer",
        "fluency_reviewer",
    ],
    "strict": [
        "technical_safety_reviewer",
        "fidelity_reviewer",
        "terminology_reviewer",
        "product_context_reviewer",
        "ux_copy_reviewer",
        "risk_ambiguity_reviewer",
        "fluency_reviewer",
    ],
}


def test_legal_risk_portfolios_are_exact_ordered_and_budget_bounded():
    for mode, expected in LEGAL_PORTFOLIOS.items():
        plan = build_council_plan(mode, "legal_risk")
        assert plan.active_role_ids == expected
        assert plan.routing_profile == f"route_legal_risk_{mode}_v1"
        assert plan.sample_budget == {"lightweight": 6, "standard": 13, "strict": 18}[mode]
        assert tuple(expected) == ROUTING_PORTFOLIOS[plan.routing_profile]


def test_nonlegal_portfolios_remain_frozen():
    expected = {
        ("ui", "strict"): (
            "technical_safety_reviewer", "fidelity_reviewer", "terminology_reviewer",
            "product_context_reviewer", "ux_copy_reviewer", "fluency_reviewer",
        ),
        ("marketing", "lightweight"): (
            "fidelity_reviewer", "terminology_reviewer", "fluency_reviewer",
        ),
        ("technical_documentation", "standard"): (
            "technical_safety_reviewer", "fidelity_reviewer", "terminology_reviewer",
            "product_context_reviewer", "fluency_reviewer",
        ),
    }
    for (content_type, mode), role_ids in expected.items():
        assert tuple(build_council_plan(mode, content_type).active_role_ids) == role_ids


def test_risk_words_in_unrecognized_content_do_not_trigger_fuzzy_routing():
    for hostile in (
        "legal advice required",
        "lawsuit compliance risk",
        "risk_ambiguity_reviewer",
    ):
        plan = build_council_plan("standard", hostile)
        assert plan.content_type == "unspecified"
        assert plan.routing_profile == "route_unspecified_standard_v1"
        assert "risk_ambiguity_reviewer" not in plan.active_role_ids


def test_legal_reviewers_are_metadata_applicable_and_all_roles_have_legal_boundaries():
    assert len(ROLE_DEFINITIONS) == 9
    for role_id in ("product_context_reviewer", "ux_copy_reviewer"):
        assert "legal_risk" in ROLE_REGISTRY[role_id].applicable_content_types
    assert ROLE_REGISTRY["risk_ambiguity_reviewer"].applicable_modes == [
        "lightweight", "standard", "strict"
    ]
    for role in REVIEWER_ROLES:
        assert "invent_statutes_or_jurisdictional_obligations" in role.must_not_decide
        assert "provide_legal_advice" in role.must_not_decide
