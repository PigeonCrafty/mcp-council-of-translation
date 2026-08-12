from council_of_translation.localization.digest import render_display_report
from council_of_translation.localization.models import (
    MinorityReport,
    ProcessDigestV2,
    RoleLens,
)
from council_of_translation.localization.roles import build_council_plan
from council_of_translation.presentation import dual_channel_result


def _digest(*, interactions: bool = False, hostile: bool = False) -> ProcessDigestV2:
    repeated = "各项表达准确自然，未发现阻碍发布的问题。"
    if hostile:
        repeated += "长" * 10_000
    lenses = [
        RoleLens(
            role_id=role_id,
            perspective=f"{repeated} 角色关注点 {index}",
            evidence=[f"证据锚点 {index}"],
            disposition="完成职责内审校",
        )
        for index, role_id in enumerate(build_council_plan("standard").active_role_ids)
    ]
    return ProcessDigestV2(
        case_brief=["语言方向：en → zh-CN", "领域/内容类型：协作软件 / ui"],
        assumptions_context_confidence=["上下文置信度：full"],
        blind_spots=["结论仅覆盖当前文本与调用方规则包。"],
        role_lenses=lenses,
        consensus=["六个专业视角均未发现阻碍发布的问题。"],
        minority_report=MinorityReport(dissent="未识别有效少数异议。"),
        material_disagreements=["无已记录的实质分歧。"],
        context_gaps_answers=["背景问题已回答"] if interactions else ["未提出需跟进的实质背景问题。"],
        user_decisions=["用户选择：保留当前译文"] if interactions else ["未请求用户结果选择。"],
        reconsideration_changes=["结果重审：结论未改变"] if interactions else ["未触发重审。"],
        editor_synthesis=["主编确认当前候选满足发布要求。"],
        execution_checklist_final_disposition=["最终处置：可发布；需人工复核：否"],
    )


def test_clean_report_has_four_chinese_sections_and_is_concise():
    report = render_display_report(_digest())
    headings = [line for line in report.splitlines() if line.startswith("## ")]
    assert headings == ["## 审校背景", "## 专业视角", "## 共识、分歧与盲区", "## 主编结论"]
    assert len(report) <= 1_800
    assert report.splitlines()[-1] == "- 最终处置：可发布；需人工复核：否"


def test_interaction_section_is_conditional_and_precedes_conclusion():
    report = render_display_report(_digest(interactions=True))
    headings = [line for line in report.splitlines() if line.startswith("## ")]
    assert headings == [
        "## 审校背景", "## 专业视角", "## 共识、分歧与盲区",
        "## 你的决定与复议", "## 主编结论",
    ]
    assert "用户选择：保留当前译文" in report
    assert "结果重审：结论未改变" in report


def test_hostile_report_is_hard_capped_and_degradation_remains_visible():
    report = render_display_report(
        _digest(hostile=True),
        status="COMPLETED_WITH_FALLBACK",
        degraded=True,
        warnings=["internal_warning_token"],
        fallback_reason="internal_fallback_token",
    )
    assert len(report) <= 3_200
    assert "存在降级或回退" in report
    assert "internal_warning_token" not in report
    assert "internal_fallback_token" not in report
    assert report.splitlines()[-1] == "- 最终处置：可发布；需人工复核：否"


def test_every_rendered_field_sanitizes_mixed_case_internal_ids_without_erasing_content():
    role_id = build_council_plan("standard").active_role_ids[0]
    digest = ProcessDigestV2(
        case_brief=[
            "来源词 preissue_reference、issue tracking；内部 ISSUE_DEADBEEF",
            "候选保留 {count}；内部 ClUsTeR_C0FFEE12",
        ],
        assumptions_context_confidence=[
            "普通 clustered_positioning；内部 POSITION_F00DBABE",
        ],
        blind_spots=["上线风险 Decision_DEADBEEF 尚待确认。"],
        role_lenses=[RoleLens(
            role_id=role_id,
            perspective="占位符缺失会阻碍发布；OPTION_A1B2C3D4；TECHNICAL_SAFETY_REVIEWER",
            evidence=["需保留 {count}；GaP_FEEDFACE"],
            disposition="完成职责内审校",
        )],
        consensus=["普通 decision support 保留；内部 issue_ABCDEF12 已处理。"],
        minority_report=MinorityReport(
            dissent="少数意见依赖 CLUSTER_1234ABCD。",
            decisive_condition="补充 Position_ABC12345 的可核查证据。",
        ),
        material_disagreements=["分歧关联 DECISION_0123ABCD。"],
        context_gaps_answers=["背景问题 OPTION_89ABCDEF 已回答。"],
        user_decisions=["用户选择 GAP_AABBCC11。"],
        reconsideration_changes=["复议移除 Issue_112233AA。"],
        editor_synthesis=[
            "Policy Gate、Position Matrix、actor_action_object 与 schema_version 不外显。",
        ],
        execution_checklist_final_disposition=[
            "必须修复：恢复 {count}，不显示 diagnostic_build 或 suggested_translation。",
            "最终处置：需人工复核；需人工复核：是",
        ],
    )
    report = render_display_report(
        digest,
        status="COMPLETED_WITH_FALLBACK",
        degraded=True,
        warnings=["reconsideration_failed:technical_safety_reviewer"],
    )
    review_id = "20260812T130000000000Z_aaaaaaaaaaaa"
    result = dual_channel_result({"review_id": review_id, "display_report": report})
    primary = result.content[0].text

    forbidden = (
        "ISSUE_DEADBEEF", "ClUsTeR_C0FFEE12", "POSITION_F00DBABE",
        "Decision_DEADBEEF", "OPTION_A1B2C3D4", "GaP_FEEDFACE",
        "issue_ABCDEF12", "CLUSTER_1234ABCD", "Position_ABC12345",
        "DECISION_0123ABCD", "OPTION_89ABCDEF", "GAP_AABBCC11",
        "Issue_112233AA", "TECHNICAL_SAFETY_REVIEWER", "Policy Gate",
        "Position Matrix", "actor_action_object", "schema_version",
        "diagnostic_build", "suggested_translation",
    )
    assert all(token.casefold() not in primary.casefold() for token in forbidden)
    for preserved in (
        "preissue_reference", "issue tracking", "clustered_positioning",
        "decision support", "{count}", "占位符缺失会阻碍发布",
        "少数意见", "存在降级或回退", review_id,
    ):
        assert preserved in primary
    assert "技术与占位符审校员" in primary
    assert len(primary) <= 3_200
    assert report.splitlines()[-1] == "- 最终处置：需人工复核；需人工复核：是"
