from council_of_translation.localization.digest import render_display_report
from council_of_translation.localization.models import (
    MinorityReport,
    ProcessDigestV2,
    RoleLens,
)
from council_of_translation.localization.roles import ROLE_REGISTRY, build_council_plan


def _roles() -> list[str]:
    return build_council_plan("standard").active_role_ids


def test_live_shaped_clean_report_hides_procedure_and_redundant_evidence_only():
    canonical = (
        "Policy Gate 后裁决：用户有效选择 0 项，Council fallback 0 项，"
        "人工复核 0 项；未使用票数多数。"
    )
    lenses = [
        RoleLens(
            role_id=role_id,
            perspective="围绕职责确认当前译文可接受：未发现实质问题",
            evidence=["Preflight placeholder_parity 与 tag_integrity 均通过。"],
        )
        for role_id in _roles()
    ]
    digest = ProcessDigestV2(
        case_brief=["Effective Brief：Context 完整"],
        role_lenses=lenses,
        consensus=["所有专业视角均未发现阻碍发布的问题。"],
        minority_report=MinorityReport(dissent="未识别有效少数异议。"),
        editor_synthesis=[canonical],
        execution_checklist_final_disposition=["最终处置：可发布；需人工复核：否"],
    )
    before = digest.model_dump(mode="json")

    report = render_display_report(digest)

    assert report.count("；依据：") == 0
    assert all(token not in report for token in (
        "用户有效选择 0 项", "Council fallback 0 项", "人工复核 0 项",
        "未使用票数多数", "Preflight", "placeholder_parity", "tag_integrity",
        "Effective Brief", "Context",
    ))
    assert "有效背景：上下文 完整" in report
    assert "所有专业视角均未发现阻碍发布的问题" in report
    assert all(report.count(ROLE_REGISTRY[role_id].display_name) == 1 for role_id in _roles())
    assert report.splitlines()[-1] == "- 最终处置：可发布；需人工复核：否"
    assert digest.model_dump(mode="json") == before
    assert digest.editor_synthesis == [canonical]
    assert all(lens.evidence for lens in digest.role_lenses)


def test_clean_zero_finding_lens_omits_redundant_evidence_suffix():
    digest = ProcessDigestV2(
        role_lenses=[RoleLens(
            role_id=_roles()[0],
            perspective="未发现职责范围内的实质问题；已检查占位符。",
            evidence=["重复说明没有发现问题。"],
        )],
        execution_checklist_final_disposition=["最终处置：可发布；需人工复核：否"],
    )
    assert "；依据：" not in render_display_report(digest)


def test_material_evidence_is_complete_or_omitted_and_risks_remain_visible():
    long_evidence = "超长证据片段，" * 30
    digest = ProcessDigestV2(
        blind_spots=["独立评审覆盖不足；缺失角色不能解释为无问题。"],
        role_lenses=[
            RoleLens(
                role_id=_roles()[0],
                perspective="发现高优先级技术问题：占位符缺失，当前候选不能安全发布。",
                evidence=["技术预检发现候选缺少 {count}。"],
            ),
            RoleLens(
                role_id=_roles()[1],
                perspective="提出具体措辞选择“继续”：当前行动含义不明确。",
                evidence=["上下文按钮应明确下一步动作。"],
            ),
            RoleLens(
                role_id=_roles()[2],
                perspective="发现术语问题：术语与调用方词表不一致。",
                evidence=[long_evidence],
            ),
        ],
        minority_report=MinorityReport(
            dissent="少数意见认为运行时会补齐占位符。",
            decisive_condition="若提供可核查的插值证据，可重新评估。",
        ),
        material_disagreements=["占位符是否由运行时补齐仍有分歧。"],
        editor_synthesis=["存在重大技术完整性风险，发布前必须修复。"],
        execution_checklist_final_disposition=[
            "必须修复：恢复 {count}。",
            "最终处置：需人工复核；需人工复核：是",
        ],
    )

    report = render_display_report(digest, degraded=True)

    assert "；依据：技术预检发现候选缺少 {count}。" in report
    assert "；依据：上下文按钮应明确下一步动作。" in report
    assert long_evidence not in report
    assert "超长证据片段…" not in report
    assert "少数意见" in report and "决定条件" in report
    assert "覆盖不足" in report and "存在降级或回退" in report
    assert "必须修复：恢复 {count}" in report
    assert report.splitlines()[-1] == "- 最终处置：需人工复核；需人工复核：是"


def test_primary_vocabulary_is_natural_chinese_without_changing_source_tokens():
    digest = ProcessDigestV2(
        case_brief=[
            "Preflight / placeholder_parity / tag_integrity / Effective Brief / Context",
            "ordinary preflight_check and contextual token stay intact",
        ],
        editor_synthesis=["Policy Gate 使用 Position Matrix 完成审查。"],
        execution_checklist_final_disposition=["最终处置：可发布；需人工复核：否"],
    )
    report = render_display_report(digest)
    assert "技术预检 / 占位符一致性 / 标签完整性 / 有效背景 / 上下文" in report
    assert "约束审查 使用 证据矩阵" in report
    assert "preflight_check" in report and "contextual" in report
