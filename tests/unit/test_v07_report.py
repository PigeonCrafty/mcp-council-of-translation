from council_of_translation.localization.digest import render_display_report
from council_of_translation.localization.models import (
    MinorityReport,
    ProcessDigestV2,
    RoleLens,
)
from council_of_translation.localization.roles import build_council_plan


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
