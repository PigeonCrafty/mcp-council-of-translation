import asyncio
import json

from council_of_translation.localization.clustering import cluster_findings
from council_of_translation.localization.deliberation import build_decision_points
from council_of_translation.localization.models import FindingV2, ReviewTaskV2, option_id_for_action
from council_of_translation.localization.orchestration import _form_mapping, run_structured_review
from council_of_translation.localization.persistence import ReviewStore
from council_of_translation.localization.roles import (
    REVIEWER_ROLES,
    ROLE_DEFINITIONS,
    ROLE_REGISTRY,
    ROUTING_PORTFOLIOS,
    build_council_plan,
)
from council_of_translation.localization.runtime import (
    ElicitationResult,
    RuntimeTelemetry,
    ScriptedModelExecutor,
    ScriptedUserInteractionGateway,
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


def test_clean_legal_routing_adds_no_sampling_or_elicitation_calls(tmp_path):
    clean = json.dumps({"role_feedback": "未发现实质问题", "findings": []}, ensure_ascii=False)
    for mode, independent_count in (("lightweight", 4), ("standard", 6), ("strict", 7)):
        telemetry = RuntimeTelemetry(sample_budget={"lightweight": 6, "standard": 13, "strict": 18}[mode])
        record = asyncio.run(run_structured_review(
            ReviewTaskV2(
                source_text="You may cancel after notice.",
                candidate_translation="通知后可以取消。",
                content_type="legal_risk",
                mode=mode,
                briefing_mode="off",
                interactive_mode="off",
            ),
            ScriptedModelExecutor([clean] * independent_count, telemetry),
            ScriptedUserInteractionGateway([], telemetry=telemetry),
            store=ReviewStore(tmp_path / mode, include_legacy=False),
        ))
        assert record.runtime_metadata.sampling_calls == independent_count
        assert record.runtime_metadata.elicitation_calls == 0
        assert record.council_plan.active_role_ids == LEGAL_PORTFOLIOS[mode]
        assert record.runtime_metadata.sampling_calls <= record.council_plan.sample_budget


def test_legal_standard_deep_path_is_exactly_thirteen_calls(tmp_path):
    roles = build_council_plan("standard", "legal_risk").active_role_ids
    findings = [
        FindingV2(
            agent_name=role_id,
            source_span="may cancel",
            candidate_span="可以取消",
            issue_type="style",
            severity="minor",
            finding_kind="choice",
            proposed_value="可取消" if index < 3 else "有权取消",
            problem="权利措辞需要按使用语境确定",
            evidence="原文使用 may 并需要已确认语境",
            action="选择不扩大义务的表达",
            confidence=0.8,
        )
        for index, role_id in enumerate(roles)
    ]
    cluster = cluster_findings(findings)[0]
    point = build_decision_points([cluster])[0]
    selected_value = next(
        value for value, option in _form_mapping(point).items()
        if option is not None and option.outcome_value == "有权取消"
    )
    reviews = []
    for index, finding in enumerate(findings):
        payload = {"role_feedback": f"role-{index}", "findings": [finding.model_dump(mode="json")]}
        if index == 0:
            payload["context_gaps"] = [{
                "question": "该句描述权利还是操作提示？",
                "materiality": "用途会改变措辞判断",
                "affected_role_ids": roles[:3],
            }]
        reviews.append(json.dumps(payload, ensure_ascii=False))
    context_reconsiderations = [
        json.dumps({"change_effect": "unchanged", "findings": []}, ensure_ascii=False)
        for _ in range(3)
    ]
    discussion = json.dumps({"turns": []})
    outcome_reconsiderations = [
        json.dumps({"positions": [{
            "issue_id": cluster.issue_id,
            "stance": "accept",
            "option_id": option_id_for_action(cluster.issue_id, "有权取消"),
            "claim": "接受有效用户选择",
            "evidence": ["已确认用途"],
            "confidence": 0.8,
        }]}, ensure_ascii=False)
        for _ in range(3)
    ]
    telemetry = RuntimeTelemetry(sample_budget=13)
    executor = ScriptedModelExecutor(
        [*reviews, *context_reconsiderations, discussion, *outcome_reconsiderations], telemetry
    )
    gateway = ScriptedUserInteractionGateway([
        ElicitationResult(action="accept", data={"context_1": "这是权利说明。"}),
        ElicitationResult(action="accept", data={"review_choice_1": selected_value}),
    ], telemetry=telemetry)

    record = asyncio.run(run_structured_review(
        ReviewTaskV2(
            source_text="You may cancel.",
            candidate_translation="可以取消。",
            content_type="legal_risk",
            mode="standard",
            briefing_mode="off",
        ),
        executor,
        gateway,
        store=ReviewStore(tmp_path / "deep", include_legacy=False),
    ))
    assert record.runtime_metadata.sampling_calls == record.runtime_metadata.sample_budget == 13
    assert record.runtime_metadata.elicitation_calls == 2
    assert len(record.context_reconsideration_provenance.completed_role_ids) == 3
    assert len(record.outcome_reconsideration_provenance.completed_role_ids) == 3
    assert len(record.discussion_rounds) == 1
