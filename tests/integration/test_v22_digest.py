import asyncio
import json

from council_of_translation.localization.clustering import cluster_findings
from council_of_translation.localization.deliberation import build_decision_points
from council_of_translation.localization.models import FindingV2, ReviewTaskV2, option_id_for_action
from council_of_translation.localization.orchestration import (
    _form_mapping,
    compact_review_response,
    run_structured_review,
)
from council_of_translation.localization.persistence import ReviewStore
from council_of_translation.localization.roles import build_council_plan
from council_of_translation.localization.runtime import (
    ElicitationResult,
    RuntimeTelemetry,
    ScriptedModelExecutor,
    ScriptedUserInteractionGateway,
)


def _clean(role_index):
    return json.dumps({
        "role_feedback": f"角色 {role_index} 从自身职责检查了译文并保留独立视角。",
        "findings": [],
    }, ensure_ascii=False)


def test_process_first_digest_has_frozen_order_six_lenses_and_bounded_display(tmp_path):
    task = ReviewTaskV2(
        source_text="Save", candidate_translation="保存", briefing_mode="off"
    )
    telemetry = RuntimeTelemetry(sample_budget=13)
    record = asyncio.run(run_structured_review(
        task,
        ScriptedModelExecutor([_clean(index) for index in range(6)], telemetry),
        ScriptedUserInteractionGateway([], telemetry=telemetry),
        store=ReviewStore(tmp_path, include_legacy=False),
    ))
    compact = compact_review_response(record)
    assert len(record.process_digest.role_lenses) == 6
    assert [lens.role_id for lens in record.process_digest.role_lenses] == record.council_plan.active_role_ids
    assert list(type(record.process_digest).model_fields) == [
        "case_brief", "assumptions_context_confidence", "blind_spots", "role_lenses",
        "consensus", "minority_report", "material_disagreements",
        "context_gaps_answers", "user_decisions", "reconsideration_changes",
        "editor_synthesis", "execution_checklist_final_disposition",
    ]
    headers = ["## 审校背景", "## 专业视角", "## 共识、分歧与盲区", "## 主编结论"]
    offsets = [record.display_report.index(header) for header in headers]
    assert offsets == sorted(offsets)
    assert "## 你的决定与复议" not in record.display_report
    assert len(record.display_report) <= 1_800
    assert record.display_report.splitlines()[-1].startswith("- 最终处置：")
    assert compact["process_digest"] == record.process_digest.model_dump(mode="json")
    assert compact["display_report"] == record.display_report
    assert "suggested_translation" not in compact["chief_editor"]
    assert [phase.phase for phase in record.phase_trace.phases] == [
        "briefing", "preflight", "planning", "independent_review", "blind_spot_mapping",
        "context_gap", "context_reconsideration", "discussion", "outcome_decision",
        "outcome_reconsideration", "policy_gate", "adjudication", "digest_construction",
    ]


def test_hostile_long_prose_is_bounded_and_hidden_reasoning_keys_are_not_exposed(tmp_path):
    hostile = json.dumps({
        "role_feedback": "有界角色反馈 " + "长" * 10_000,
        "findings": [],
        "hidden_reasoning": "SECRET-CHAIN-OF-THOUGHT",
    }, ensure_ascii=False)
    telemetry = RuntimeTelemetry(sample_budget=13)
    record = asyncio.run(run_structured_review(
        ReviewTaskV2(source_text="Save", candidate_translation="保存", briefing_mode="off"),
        ScriptedModelExecutor([hostile] * 6, telemetry),
        ScriptedUserInteractionGateway([], telemetry=telemetry),
        store=ReviewStore(tmp_path, include_legacy=False),
    ))
    serialized = json.dumps(compact_review_response(record), ensure_ascii=False)
    assert len(record.display_report) <= 3_200
    assert all(len(lens.perspective) <= 240 for lens in record.process_digest.role_lenses)
    assert "SECRET-CHAIN-OF-THOUGHT" not in serialized
    assert "hidden_reasoning" not in serialized


def test_deep_standard_reference_flow_uses_exact_thirteen_samples_in_phase_order(tmp_path):
    role_ids = build_council_plan("standard").active_role_ids
    findings = [
        FindingV2(
            agent_name=role_id,
            source_span="Continue",
            candidate_span="继续",
            issue_type="ux",
            severity="minor",
            finding_kind="choice",
            proposed_value="继续" if index < 3 else "下一步",
            problem="按钮措辞选择",
            evidence="界面操作语义",
            action="按证据选择",
            confidence=0.8,
        )
        for index, role_id in enumerate(role_ids)
    ]
    reference_cluster = cluster_findings(findings)[0]
    point = build_decision_points([reference_cluster])[0]
    selected_value = next(
        value for value, option in _form_mapping(point).items()
        if option is not None and option.outcome_value == "下一步"
    )
    reviews = []
    for index, finding in enumerate(findings):
        payload = {"role_feedback": f"role-{index}", "findings": [finding.model_dump(mode="json")]}
        if index == 0:
            payload["context_gaps"] = [{
                "question": "该按钮位于哪个流程阶段？",
                "materiality": "答案会改变措辞判断和建议选项",
                "affected_role_ids": role_ids[:3],
            }]
        reviews.append(json.dumps(payload, ensure_ascii=False))
    context_reconsiderations = [
        json.dumps({"change_effect": "unchanged", "findings": []}) for _ in range(3)
    ]
    discussion = json.dumps({"turns": []})
    outcome_responses = []
    for role_id in role_ids[:3]:
        outcome_responses.append(json.dumps({"positions": [{
            "issue_id": reference_cluster.issue_id,
            "stance": "accept",
            "option_id": option_id_for_action(reference_cluster.issue_id, "下一步"),
            "claim": "接受用户选择",
            "evidence": ["有效用户选择"],
            "confidence": 0.8,
            "blocking": False,
            "conditions": [],
        }]}, ensure_ascii=False))

    telemetry = RuntimeTelemetry(sample_budget=13)
    executor = ScriptedModelExecutor(
        [*reviews, *context_reconsiderations, discussion, *outcome_responses], telemetry
    )
    gateway = ScriptedUserInteractionGateway([
        ElicitationResult(action="accept", data={"context_1": "设置流程主按钮"}),
        ElicitationResult(action="accept", data={"review_choice_1": selected_value}),
    ], telemetry=telemetry)
    record = asyncio.run(run_structured_review(
        ReviewTaskV2(
            source_text="Continue", candidate_translation="继续", content_type="ui",
            briefing_mode="off", mode="standard",
        ),
        executor,
        gateway,
        store=ReviewStore(tmp_path, include_legacy=False),
    ))
    assert record.runtime_metadata.sampling_calls == record.runtime_metadata.sample_budget == 13
    assert record.runtime_metadata.context_gap_elicitation_calls == 1
    assert record.runtime_metadata.outcome_elicitation_calls == 1
    assert len(record.context_reconsideration_provenance.completed_role_ids) == 3
    assert len(record.outcome_reconsideration_provenance.completed_role_ids) == 3
    markers = [
        "CONTEXT_RECONSIDERATION" if "CONTEXT_RECONSIDERATION" in prompt
        else "DISCUSSION" if "ISSUE_PACKETS" in prompt
        else "OUTCOME_RECONSIDERATION" if "RECONSIDERATION_PACKET" in prompt
        else "INDEPENDENT"
        for prompt in executor.prompts
    ]
    assert markers == ["INDEPENDENT"] * 6 + ["CONTEXT_RECONSIDERATION"] * 3 + ["DISCUSSION"] + ["OUTCOME_RECONSIDERATION"] * 3
