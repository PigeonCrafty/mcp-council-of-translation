import asyncio
import json

from council_of_translation.localization.digest import render_display_report
from council_of_translation.localization.models import (
    CouncilValueMetrics,
    MinorityReport,
    ProcessDigestV2,
    ReviewTaskV2,
    RoleContribution,
    RoleLens,
)
from council_of_translation.localization.orchestration import run_structured_review
from council_of_translation.localization.persistence import ReviewStore
from council_of_translation.localization.roles import ROLE_REGISTRY
from council_of_translation.localization.runtime import (
    RuntimeTelemetry,
    ScriptedModelExecutor,
    ScriptedUserInteractionGateway,
)


HEADINGS = [
    "## 审校背景",
    "## Council 新增视角",
    "## 角色覆盖与分工",
    "## 共识、分歧与盲区",
    "## 主编结论",
]


def test_clean_runtime_report_collapses_confirmations_and_accounts_for_roles_once(tmp_path):
    clean = json.dumps({"role_feedback": "completed", "findings": []})
    telemetry = RuntimeTelemetry(sample_budget=13)
    record = asyncio.run(run_structured_review(
        ReviewTaskV2(
            source_text="Save", candidate_translation="保存", content_type="ui",
            briefing_mode="off", interactive_mode="off",
        ),
        ScriptedModelExecutor([clean] * 6, telemetry),
        ScriptedUserInteractionGateway([], telemetry=telemetry),
        store=ReviewStore(tmp_path, include_legacy=False),
    ))

    headings = [line for line in record.display_report.splitlines() if line.startswith("## ")]
    assert headings == HEADINGS
    assert len(record.display_report) <= 1_200
    assert "完成确认性覆盖" in record.display_report
    assert "依据：" not in record.display_report
    for role_id in record.council_plan.active_role_ids:
        assert record.display_report.count(ROLE_REGISTRY[role_id].display_name) == 1
    assert record.display_report.splitlines()[-1].startswith("- 最终处置：")


def test_value_order_minority_degradation_and_discussion_truth_remain_visible():
    role_ids = ["fidelity_reviewer", "terminology_reviewer", "fluency_reviewer"]
    digest = ProcessDigestV2(
        case_brief=["语言方向：en → zh-CN"],
        blind_spots=["授权场景仍未确认。"],
        role_lenses=[
            RoleLens(role_id=role_ids[0], perspective="发现否定关系反转。", evidence=["not 被遗漏"]),
            RoleLens(role_id=role_ids[1], perspective="术语证据支持该语义风险。", evidence=["TB-12"]),
            RoleLens(role_id=role_ids[2], perspective="未发现职责范围内的实质问题。"),
        ],
        consensus=["语义风险必须先修复。"],
        minority_report=MinorityReport(
            dissent="若此处是反讽文案，语义判断可能不同。",
            decisive_condition="补充经确认的品牌场景。",
            role_ids=[role_ids[2]],
        ),
        material_disagreements=["授权语境仍有实质分歧。"],
        editor_synthesis=["当前证据不支持直接发布。"],
        execution_checklist_final_disposition=[
            "必须修复：恢复否定关系。",
            "最终处置：需人工复核；需人工复核：是",
        ],
    )
    metrics = CouncilValueMetrics(
        role_contributions=[
            RoleContribution(role_id=role_ids[0], contribution_kind="unique_material", unique_issue_count=1, material_finding_count=1),
            RoleContribution(role_id=role_ids[1], contribution_kind="corroborating", corroborated_issue_count=1, material_finding_count=1),
            RoleContribution(role_id=role_ids[2], contribution_kind="confirmation_only"),
        ],
        unique_material_issue_count=1,
        corroborated_issue_count=1,
        confirmation_only_role_count=1,
        discussion_new_evidence_count=1,
        discussion_position_change_count=1,
        discussion_resolved_issue_count=1,
        discussion_marginal_value="material",
    )

    report = render_display_report(digest, metrics=metrics, degraded=True)
    headings = [line for line in report.splitlines() if line.startswith("## ")]
    assert headings == HEADINGS
    assert report.index("新增 1 个独立问题") < report.index("完成确认性覆盖")
    assert "讨论新增证据 1 条、改变立场 1 次、解决问题 1 个" in report
    assert "少数意见" in report and "决定条件" in report
    assert "授权场景仍未确认" in report and "存在降级或回退" in report
    assert "依据：not 被遗漏" in report and "依据：TB-12" in report
    assert len(report) <= 3_200
    assert report.splitlines()[-1] == "- 最终处置：需人工复核；需人工复核：是"


def test_discussion_line_is_absent_when_no_discussion_occurred():
    digest = ProcessDigestV2(
        role_lenses=[RoleLens(role_id="fluency_reviewer", perspective="未发现职责范围内的实质问题。")],
        execution_checklist_final_disposition=["最终处置：可发布；需人工复核：否"],
    )
    metrics = CouncilValueMetrics(
        role_contributions=[RoleContribution(role_id="fluency_reviewer", contribution_kind="confirmation_only")],
        confirmation_only_role_count=1,
    )
    report = render_display_report(digest, metrics=metrics)
    assert "讨论" not in report
