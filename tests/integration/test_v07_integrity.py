import asyncio

from council_of_translation.localization.models import (
    MinorityReport,
    ProcessDigestV2,
    ReviewTaskV2,
    RoleLens,
)
from council_of_translation.localization.digest import render_display_report
from council_of_translation.localization.orchestration import run_structured_review
from council_of_translation.localization.persistence import ReviewStore
from council_of_translation.localization.roles import ROLE_REGISTRY, build_council_plan
from council_of_translation.localization.runtime import (
    ElicitationResult,
    RuntimeTelemetry,
    ScriptedModelExecutor,
    ScriptedUserInteractionGateway,
)
from council_of_translation.presentation import dual_channel_result


CLEAN = '{"role_feedback":"未发现职责范围内的实质问题。","findings":[]}'


def test_tone_and_focus_sentinels_round_trip_schema_record_prompt_and_storage(tmp_path):
    tone = "TONE_SENTINEL_独立语气"
    focus = "FOCUS_SENTINEL_独立重点"
    answers = {
        "domain": "协作软件",
        "content_type": "界面文案",
        "audience": "普通用户",
        "tone_goal": tone,
        "primary_focus": focus,
        "usage_context": "设置页主按钮",
    }
    telemetry = RuntimeTelemetry(sample_budget=13)
    executor = ScriptedModelExecutor([CLEAN] * 6, telemetry)
    gateway = ScriptedUserInteractionGateway(
        [ElicitationResult(action="accept", data=answers)], telemetry=telemetry
    )
    store = ReviewStore(tmp_path, include_legacy=False)
    record = asyncio.run(run_structured_review(
        ReviewTaskV2(source_text="Save", candidate_translation="保存"),
        executor,
        gateway,
        store=store,
    ))

    schema = gateway.requests[0][1].model_json_schema()["properties"]
    assert schema["tone_goal"]["title"] == "语气与沟通目标"
    assert schema["primary_focus"]["title"] == "本次审校重点"
    assert record.briefing_interaction.accepted_answers["tone_goal"] == tone
    assert record.briefing_interaction.accepted_answers["primary_focus"] == focus
    assert record.effective_brief.tone_goal == tone
    assert record.effective_brief.primary_focus == focus
    assert all(f'"tone_goal":"{tone}"' in prompt for prompt in executor.prompts)
    assert all(f'"primary_focus":"{focus}"' in prompt for prompt in executor.prompts)
    loaded = store.load(record.review_id)
    assert loaded.effective_brief.tone_goal == tone
    assert loaded.effective_brief.primary_focus == focus


def test_disputed_blocker_pending_and_degraded_meaning_remains_visible():
    role_id = build_council_plan("standard").active_role_ids[0]
    digest = ProcessDigestV2(
        case_brief=["语言方向：en → zh-CN"],
        blind_spots=["关键上线场景尚未确认。"],
        role_lenses=[RoleLens(
            role_id=role_id,
            perspective="发现占位符缺失，当前候选不能安全发布。",
            evidence=["候选缺少 {count}"],
        )],
        consensus=["当前候选存在技术完整性阻断。"],
        minority_report=MinorityReport(
            dissent="若占位符由运行时自动补齐，可重新评估。",
            decisive_condition="提供可核查的运行时插值证据。",
            role_ids=[role_id],
        ),
        material_disagreements=["是否由运行时补齐占位符仍有分歧。"],
        user_decisions=["用户明确委托 Council 按证据裁决。"],
        reconsideration_changes=["结果重审：结论未改变"],
        editor_synthesis=["Policy Gate 后裁决：option_deadbeef 无效。"],
        execution_checklist_final_disposition=[
            "必须修复：恢复 {count} 占位符。",
            "最终处置：需人工复核；需人工复核：是",
        ],
    )
    report = render_display_report(
        digest,
        status="RETURNED_PENDING",
        degraded=True,
        warnings=["reconsideration_failed:technical_safety_reviewer"],
        fallback_reason="reconsideration_degraded",
    )

    assert "关键上线场景尚未确认" in report
    assert "少数意见" in report and "决定条件" in report
    assert "用户明确委托" in report and "结论未改变" in report
    assert "必须修复：恢复 {count}" in report
    assert "存在降级或回退" in report and "审校尚待补充" in report
    assert "Policy Gate" not in report and "option_deadbeef" not in report
    assert "technical_safety_reviewer" not in report
    assert report.splitlines()[-1] == "- 最终处置：需人工复核；需人工复核：是"


def test_primary_text_hard_cap_keeps_footer_and_structured_full_evidence():
    payload = {
        "review_id": "20260812T130000000000Z_aaaaaaaaaaaa",
        "status": "COMPLETED",
        "display_report": "## 审校背景\n\n- " + "长" * 5_000,
        "independent_reviews": [{"role_feedback": "PRIVATE_FULL_EVIDENCE"}] * 6,
        "task": {"source_text": "PRIVATE_SOURCE", "candidate_translation": "PRIVATE_TARGET"},
    }
    result = dual_channel_result(payload)
    text = result.content[0].text
    assert len(text) <= 3_200
    assert "审校记录：20260812T130000000000Z_aaaaaaaaaaaa" in text
    assert "PRIVATE_FULL_EVIDENCE" not in text
    assert "PRIVATE_SOURCE" not in text and "PRIVATE_TARGET" not in text
    assert len(result.structured_content["independent_reviews"]) == 6
    assert result.structured_content["task"]["source_text"] == "PRIVATE_SOURCE"


def test_clean_presentation_adds_no_sampling_and_uses_only_chinese_role_labels(tmp_path):
    telemetry = RuntimeTelemetry(sample_budget=13)
    record = asyncio.run(run_structured_review(
        ReviewTaskV2(
            source_text="Save", candidate_translation="保存", briefing_mode="off"
        ),
        ScriptedModelExecutor([CLEAN] * 6, telemetry),
        ScriptedUserInteractionGateway([], telemetry=telemetry),
        store=ReviewStore(tmp_path, include_legacy=False),
    ))
    assert record.runtime_metadata.sampling_calls == 6
    assert len(record.process_digest.role_lenses) == 6
    for role_id in record.council_plan.active_role_ids:
        assert role_id not in record.display_report
        assert record.display_report.count(ROLE_REGISTRY[role_id].display_name) == 1
    forbidden = (
        "Case Brief", "Role Lenses", "Policy Gate", "actor_action_object",
        "schema_version", "diagnostic_build", "suggested_translation",
    )
    assert all(token not in record.display_report for token in forbidden)
