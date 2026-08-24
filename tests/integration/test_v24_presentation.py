import asyncio
import json

from council_of_translation.localization.digest import render_display_report
from council_of_translation.localization.models import (
    CouncilValueMetrics,
    IssueCluster,
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
    assert record.display_report.count("完成确认性覆盖") == 1
    coverage_line = next(
        line for line in record.display_report.splitlines()
        if "完成确认性覆盖" in line
    )
    assert "依据：" not in coverage_line
    for role_id in record.council_plan.active_role_ids:
        role_name = ROLE_REGISTRY[role_id].display_name
        assert record.display_report.count(role_name) == 1
        assert role_name in coverage_line
    assert record.display_report.splitlines()[-1].startswith("- 最终处置：")


def test_legal_standard_report_uses_natural_route_wording_without_mutation(tmp_path):
    clean = json.dumps({"role_feedback": "完成职责内审校", "findings": []}, ensure_ascii=False)
    telemetry = RuntimeTelemetry(sample_budget=13)
    record = asyncio.run(run_structured_review(
        ReviewTaskV2(
            source_text="You may withdraw after notice.",
            candidate_translation="通知后可以撤回。",
            content_type="legal_risk",
            briefing_mode="off",
            interactive_mode="off",
        ),
        ScriptedModelExecutor([clean] * 6, telemetry),
        ScriptedUserInteractionGateway([], telemetry=telemetry),
        store=ReviewStore(tmp_path / "legal", include_legacy=False),
    ))
    before = (
        record.process_digest.model_dump(mode="json"),
        record.council_plan.model_dump(mode="json"),
        record.council_value_metrics.model_dump(mode="json"),
        [cluster.model_dump(mode="json") for cluster in record.issue_clusters],
    )

    rerendered = render_display_report(
        record.process_digest,
        metrics=record.council_value_metrics,
        status=record.status,
        degraded=record.degraded,
        warnings=record.warnings,
        fallback_reason=record.fallback_reason,
        clusters=record.issue_clusters,
    )

    assert record.runtime_metadata.sampling_calls == 6
    assert record.runtime_metadata.elicitation_calls == 0
    assert [line for line in rerendered.splitlines() if line.startswith("## ")] == HEADINGS
    assert "风险审校路线：覆盖语义、术语、产品语境、用户理解、风险歧义与语言自然度" in rerendered
    assert "确定性技术预检照常执行" in rerendered
    assert len(rerendered) <= 1_200
    assert rerendered.splitlines()[-1].startswith("- 最终处置：")
    for private in ("routing_profile", "routing_reason_codes", "route_legal_risk_standard_v1", "risk_panorama"):
        assert private not in rerendered
    assert before == (
        record.process_digest.model_dump(mode="json"),
        record.council_plan.model_dump(mode="json"),
        record.council_value_metrics.model_dump(mode="json"),
        [cluster.model_dump(mode="json") for cluster in record.issue_clusters],
    )


def test_hostile_report_keeps_five_sections_and_whole_material_lines_under_cap():
    role_ids = list(ROLE_REGISTRY)[:8]
    internal = (
        "ISSUE_SECRET cluster_SECRET POSITION_SECRET decision_SECRET OPTION_SECRET gap_SECRET "
        "routing_profile routing_reason_codes route_legal_risk_strict_v1 risk_strict"
    )
    digest = ProcessDigestV2(
        case_brief=[f"背景 {index} {internal} " + "甲" * 220 for index in range(6)],
        assumptions_context_confidence=[f"假设 {index} {internal} " + "乙" * 220 for index in range(4)],
        blind_spots=[f"盲区 {index} {internal} " + "丙" * 220 for index in range(6)],
        role_lenses=[
            RoleLens(
                role_id=role_id,
                perspective=f"新增风险 {index} {internal} " + "丁" * 220,
                evidence=[f"完整依据 {index} " + "戊" * 60],
            )
            for index, role_id in enumerate(role_ids)
        ],
        consensus=[f"共识 {index} {internal} " + "己" * 220 for index in range(4)],
        material_disagreements=[f"分歧 {index} {internal} " + "庚" * 220 for index in range(4)],
        minority_report=MinorityReport(
            dissent=f"少数意见 {internal} " + "辛" * 220,
            decisive_condition=f"决定条件 {internal} " + "壬" * 220,
        ),
        context_gaps_answers=[f"背景缺口 {index} {internal} " + "癸" * 220 for index in range(3)],
        user_decisions=[f"用户决定 {index} {internal} " + "子" * 220 for index in range(3)],
        reconsideration_changes=[f"复议变化 {index} {internal} " + "丑" * 220 for index in range(3)],
        editor_synthesis=[f"主编依据 {index} {internal} " + "寅" * 220 for index in range(3)],
        execution_checklist_final_disposition=[
            *[f"必须修复：风险后果 {index} {internal} " + "卯" * 220 for index in range(6)],
            "最终处置：需人工复核；需人工复核：是",
        ],
    )
    metrics = CouncilValueMetrics(
        role_contributions=[
            RoleContribution(
                role_id=role_id,
                contribution_kind="unique_material",
                unique_issue_count=1,
                material_finding_count=1,
            )
            for role_id in role_ids
        ],
        unique_material_issue_count=len(role_ids),
        unavailable_role_count=1,
        discussion_marginal_value="material",
        discussion_new_evidence_count=2,
        discussion_position_change_count=1,
        discussion_resolved_issue_count=1,
    )

    report = render_display_report(digest, metrics=metrics, degraded=True)

    assert [line for line in report.splitlines() if line.startswith("## ")] == HEADINGS
    assert len(report) <= 3_200
    assert report.splitlines()[-1] == "- 最终处置：需人工复核；需人工复核：是"
    assert "覆盖风险" in report
    assert "盲区" in report
    assert "存在降级或回退" in report
    lowered = report.casefold()
    for token in (
        "issue_secret", "cluster_secret", "position_secret", "decision_secret",
        "option_secret", "gap_secret", "routing_profile", "routing_reason_codes",
        "route_legal_risk_strict_v1", "risk_strict",
    ):
        assert token not in lowered


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


def test_case_b_groups_corroboration_and_collapses_exact_chief_anchor_only():
    roles = [
        "technical_safety_reviewer", "fidelity_reviewer",
        "risk_ambiguity_reviewer", "terminology_reviewer",
        "ux_copy_reviewer", "fluency_reviewer",
    ]
    digest = ProcessDigestV2(
        case_brief=["删除确认对话框；{count} 必须原样保留。"],
        role_lenses=[
            RoleLens(role_id=roles[0], perspective="占位符 {count} 缺失。"),
            RoleLens(role_id=roles[1], perspective="占位符 {count} 缺失。"),
            RoleLens(role_id=roles[2], perspective="cannot 被反转为可以。"),
            *[
                RoleLens(role_id=role_id, perspective="未发现职责范围内的其他实质问题。")
                for role_id in roles[3:]
            ],
        ],
        consensus=["占位符 {count} 缺失。"],
        material_disagreements=["cannot 被反转为可以。"],
        minority_report=MinorityReport(
            dissent="占位符 {count} 缺失。",
            decisive_condition="若运行时可核查地补齐 {count}，可重新评估。",
        ),
        execution_checklist_final_disposition=[
            "必须修复：恢复 {count}。",
            "必须修复：按 required_literal:{count} 保留 {count}。",
            "执行顺序：先恢复 {count}。",
            "必须修复：不得把 cannot 改成可以。",
            "最终处置：需人工复核；需人工复核：是",
        ],
    )
    clusters = [
        IssueCluster(
            issue_id="issue_preflight", topic="占位符 {count} 缺失。",
            category="integrity", source_spans=["{count}"], finding_ids=[],
            participant_role_ids=[roles[0]], blocking=True,
        ),
        IssueCluster(
            issue_id="issue_model_placeholder", topic="占位符 {count} 缺失。",
            category="integrity", source_spans=["{count}"], finding_ids=["finding_1"],
            participant_role_ids=roles[:2],
        ),
        IssueCluster(
            issue_id="issue_reversal", topic="cannot 被反转为可以。",
            category="correctness", source_spans=["cannot"], candidate_spans=["可以"],
            finding_ids=["finding_2"], participant_role_ids=[roles[2]],
        ),
    ]
    metrics = CouncilValueMetrics(
        role_contributions=[
            RoleContribution(role_id=roles[0], contribution_kind="corroborating", corroborated_issue_count=1, material_finding_count=1),
            RoleContribution(role_id=roles[1], contribution_kind="corroborating", corroborated_issue_count=1, material_finding_count=1),
            RoleContribution(role_id=roles[2], contribution_kind="unique_material", unique_issue_count=1, material_finding_count=1),
            *[
                RoleContribution(role_id=role_id, contribution_kind="confirmation_only")
                for role_id in roles[3:]
            ],
        ],
        unique_material_issue_count=1,
        corroborated_issue_count=1,
        confirmation_only_role_count=3,
        discussion_marginal_value="none",
    )
    digest_before = digest.model_dump(mode="json")
    clusters_before = [cluster.model_dump(mode="json") for cluster in clusters]

    report = render_display_report(digest, metrics=metrics, clusters=clusters)

    coverage = report.split("## 角色覆盖与分工", 1)[1].split("## 共识、分歧与盲区", 1)[0]
    assert '技术与占位符审校员、忠实度审校员：共同交叉印证“' in coverage
    assert coverage.count("完成确认性覆盖") == 1
    assert report.count("必须修复：恢复 {count}") == 1
    assert "按 required_literal:{count}" not in report
    assert "执行顺序：先恢复 {count}" not in report
    assert "必须修复：不得把 cannot 改成可以" in report
    assert "讨论补充 6 条新证据" not in report
    assert report.splitlines()[-1] == "- 最终处置：需人工复核；需人工复核：是"
    assert digest.model_dump(mode="json") == digest_before
    assert [cluster.model_dump(mode="json") for cluster in clusters] == clusters_before


def test_corroborated_disputed_topic_is_rendered_once_before_deduplication():
    roles = ["fidelity_reviewer", "terminology_reviewer"]
    topic = "候选译文把“trial”误写成“正式版”，会改变授权状态。"
    condition = "只有确认该功能已结束试用并正式授权时，才可采用“正式版”。"
    digest = ProcessDigestV2(
        case_brief=["软件授权状态审校。"],
        role_lenses=[
            RoleLens(role_id=roles[0], perspective="发现授权状态发生实质变化。"),
            RoleLens(role_id=roles[1], perspective="术语选择改变了产品授权层级。"),
        ],
        material_disagreements=[topic],
        minority_report=MinorityReport(
            dissent=topic,
            decisive_condition=condition,
            role_ids=[roles[1]],
        ),
        editor_synthesis=["当前证据不能支持直接发布。"],
        execution_checklist_final_disposition=[
            "最终处置：需人工复核；需人工复核：是",
        ],
    )
    cluster = IssueCluster(
        issue_id="issue_trial_tier",
        topic=topic,
        category="terminology",
        source_spans=["trial"],
        candidate_spans=["正式版"],
        finding_ids=["finding_fidelity", "finding_terminology"],
        participant_role_ids=roles,
        consensus_status="disputed",
    )
    metrics = CouncilValueMetrics(
        role_contributions=[
            RoleContribution(
                role_id=role,
                contribution_kind="corroborating",
                corroborated_issue_count=1,
                material_finding_count=1,
            )
            for role in roles
        ],
        corroborated_issue_count=1,
    )
    digest_before = digest.model_dump(mode="json")
    cluster_before = cluster.model_dump(mode="json")

    report = render_display_report(digest, metrics=metrics, clusters=[cluster])

    assert report.count(topic) == 1
    for role in roles:
        assert report.count(ROLE_REGISTRY[role].display_name) == 1
    assert condition in report
    assert report.splitlines()[-1] == "- 最终处置：需人工复核；需人工复核：是"
    assert digest.model_dump(mode="json") == digest_before
    assert cluster.model_dump(mode="json") == cluster_before


def test_case_c_exact_cross_family_repair_renders_once_with_distinct_consequences():
    source = "only use your location while the app is open"
    candidate = "使用您的位置信息"
    topics = [
        "遗漏使用时段限定，扩大了原文所述的数据使用范围。",
        "用户可能误解为应用关闭后仍会持续使用定位。",
    ]
    clusters = [
        IssueCluster(
            issue_id="issue_scope_accuracy",
            topic=topics[0],
            category="correctness",
            source_spans=[source],
            candidate_spans=[candidate],
            finding_ids=["finding_accuracy"],
            participant_role_ids=["fidelity_reviewer"],
            candidate_actions=[candidate],
            current_outcome=candidate,
            outcome_anchor=candidate,
            severity="major",
        ),
        IssueCluster(
            issue_id="issue_scope_user_impact",
            topic=topics[1],
            category="language_choice",
            source_spans=[source],
            candidate_spans=[candidate],
            finding_ids=["finding_user_impact"],
            participant_role_ids=["ux_copy_reviewer"],
            candidate_actions=[],
            current_outcome=candidate,
            outcome_anchor=candidate,
            severity="major",
        ),
    ]
    digest = ProcessDigestV2(
        case_brief=["定位权限说明审校。"],
        material_disagreements=topics,
        execution_checklist_final_disposition=[
            *(f"建议修复：{topic}" for topic in topics),
            *(f"执行顺序：{topic}" for topic in topics),
            "最终处置：修改后可发布；需人工复核：否",
        ],
    )
    metrics = CouncilValueMetrics()
    before = (
        digest.model_dump(mode="json"),
        [cluster.model_dump(mode="json") for cluster in clusters],
        metrics.model_dump(mode="json"),
    )

    report = render_display_report(digest, metrics=metrics, clusters=clusters)
    chief = report.split("## 主编结论", 1)[1]

    assert chief.count("建议修复：") == 1
    assert chief.count(topics[0].rstrip("。")) == 1
    assert chief.count(topics[1].rstrip("。")) == 1
    assert "执行顺序" not in chief
    assert report.splitlines()[-1] == "- 最终处置：修改后可发布；需人工复核：否"
    assert before == (
        digest.model_dump(mode="json"),
        [cluster.model_dump(mode="json") for cluster in clusters],
        metrics.model_dump(mode="json"),
    )


def test_case_b_nested_actionless_reversal_is_one_item_beside_placeholder():
    source = "Delete {count} files? This action cannot be undone."
    candidate = "删除文件吗？此操作可以撤销。"
    topics = [
        "不可撤销被改成可以撤销。",
        "危险操作的后果提示会误导用户。",
    ]
    clusters = [
        IssueCluster(
            issue_id="issue_placeholder",
            topic="missing=['{count}']; extra=[]",
            category="integrity",
            source_spans=["{count}"],
            immutable_hard_constraints=["braced-placeholder-parity"],
            blocking=True,
        ),
        IssueCluster(
            issue_id="issue_reversal_accuracy",
            topic=topics[0],
            category="correctness",
            source_spans=["cannot be undone"],
            candidate_spans=["可以撤销"],
            finding_ids=["finding_reversal_accuracy"],
            candidate_actions=["可以撤销"],
            current_outcome="可以撤销",
        ),
        IssueCluster(
            issue_id="issue_reversal_impact",
            topic=topics[1],
            category="language_choice",
            source_spans=[source],
            candidate_spans=[candidate],
            finding_ids=["finding_reversal_impact"],
        ),
    ]
    checklist = [
        "必须修复：missing=['{count}']; extra=[]",
        *(f"建议修复：{topic}" for topic in topics),
        *(f"执行顺序：{topic}" for topic in topics),
    ]
    report, cluster_before, _, _ = _render_negative_control(clusters, checklist)
    chief = report.split("## 主编结论", 1)[1]

    assert chief.count("恢复并原样保留占位符 {count}") == 1
    assert chief.count("建议修复：") == 1
    assert chief.count(topics[0].rstrip("。")) == 1
    assert chief.count(topics[1].rstrip("。")) == 1
    assert "执行顺序" not in chief
    assert [cluster.model_dump(mode="json") for cluster in clusters] == cluster_before


def _render_negative_control(
    clusters: list[IssueCluster],
    checklist: list[str],
) -> tuple[str, list[dict], dict, dict]:
    digest = ProcessDigestV2(
        execution_checklist_final_disposition=[
            *checklist,
            "最终处置：需人工复核；需人工复核：是",
        ],
    )
    metrics = CouncilValueMetrics()
    cluster_before = [cluster.model_dump(mode="json") for cluster in clusters]
    digest_before = digest.model_dump(mode="json")
    metrics_before = metrics.model_dump(mode="json")
    report = render_display_report(digest, metrics=metrics, clusters=clusters)
    return report, cluster_before, digest_before, metrics_before


def test_primary_work_items_do_not_merge_different_required_literals():
    clusters = [
        IssueCluster(
            issue_id=f"issue_literal_{index}",
            topic="explicit caller hard constraint violated",
            category="integrity",
            source_spans=[f"required_literal:{literal}"],
            immutable_hard_constraints=[f"explicit-required-literal-{index}"],
            blocking=True,
        )
        for index, literal in enumerate(("ALPHA", "BETA"), start=1)
    ]
    report, cluster_before, _, _ = _render_negative_control(
        clusters,
        ["必须修复：explicit caller hard constraint violated"] * 2,
    )
    chief = report.split("## 主编结论", 1)[1]
    assert chief.count("恢复并原样保留受保护内容") == 2
    assert "ALPHA" in chief and "BETA" in chief
    assert [cluster.model_dump(mode="json") for cluster in clusters] == cluster_before


def test_primary_work_items_do_not_merge_placeholder_and_url_loss():
    clusters = [
        IssueCluster(
            issue_id="issue_placeholder",
            topic="missing=['{count}']; extra=[]",
            category="integrity",
            source_spans=["{count}"],
            immutable_hard_constraints=["braced-placeholder-parity"],
            blocking=True,
        ),
        IssueCluster(
            issue_id="issue_url",
            topic="missing=['https://example.com/help']; extra=[]",
            category="integrity",
            source_spans=["https://example.com/help"],
            immutable_hard_constraints=["url-parity"],
            blocking=True,
        ),
    ]
    report, cluster_before, _, _ = _render_negative_control(
        clusters,
        [f"必须修复：{cluster.topic}" for cluster in clusters],
    )
    chief = report.split("## 主编结论", 1)[1]
    assert chief.count("恢复并原样保留占位符") == 1
    assert chief.count("恢复并原样保留链接") == 1
    assert [cluster.model_dump(mode="json") for cluster in clusters] == cluster_before


def test_whole_sentence_placeholder_span_does_not_absorb_semantic_reversal():
    sentence = "Delete {count} files? This action cannot be undone."
    clusters = [
        IssueCluster(
            issue_id="issue_placeholder",
            topic="missing=['{count}']; extra=[]",
            category="integrity",
            source_spans=["{count}"],
            immutable_hard_constraints=["braced-placeholder-parity"],
            blocking=True,
        ),
        IssueCluster(
            issue_id="issue_reversal",
            topic="不可撤销被改成可以撤销。",
            category="correctness",
            source_spans=[sentence],
            candidate_spans=["删除文件吗？此操作可以撤销。"],
            finding_ids=["finding_reversal"],
            participant_role_ids=["fidelity_reviewer"],
            severity="critical",
        ),
    ]
    report, cluster_before, _, _ = _render_negative_control(
        clusters,
        [f"必须修复：{cluster.topic}" for cluster in clusters],
    )
    chief = report.split("## 主编结论", 1)[1]
    assert "恢复并原样保留占位符 {count}" in chief
    assert "不可撤销被改成可以撤销" in chief
    assert [cluster.model_dump(mode="json") for cluster in clusters] == cluster_before


def test_same_spans_with_different_repair_actions_remain_separate():
    source = "Open settings"
    candidate = "打开"
    clusters = [
        IssueCluster(
            issue_id="issue_action_settings",
            topic="补足设置对象。",
            category="correctness",
            source_spans=[source],
            candidate_spans=[candidate],
            finding_ids=["finding_settings"],
            candidate_actions=[candidate, "打开设置"],
            current_outcome=candidate,
        ),
        IssueCluster(
            issue_id="issue_action_preferences",
            topic="改用偏好设置名称。",
            category="language_choice",
            source_spans=[source],
            candidate_spans=[candidate],
            finding_ids=["finding_preferences"],
            candidate_actions=[candidate, "打开偏好设置"],
            current_outcome=candidate,
        ),
    ]
    report, cluster_before, _, _ = _render_negative_control(
        clusters,
        [f"建议修复：{cluster.topic}" for cluster in clusters],
    )
    chief = report.split("## 主编结论", 1)[1]
    assert "补足设置对象" in chief
    assert "改用偏好设置名称" in chief
    assert [cluster.model_dump(mode="json") for cluster in clusters] == cluster_before


def _actionless_cluster_pair(
    source_spans: tuple[str, str],
    candidate_spans: tuple[str, str],
) -> list[IssueCluster]:
    return [
        IssueCluster(
            issue_id=f"issue_one_sided_{index}",
            topic=f"独立问题 {index}。",
            category=category,
            source_spans=[source_spans[index]],
            candidate_spans=[candidate_spans[index]],
            finding_ids=[f"finding_one_sided_{index}"],
        )
        for index, category in enumerate(("correctness", "language_choice"))
    ]


def test_source_related_but_candidate_unrelated_work_items_remain_separate():
    clusters = _actionless_cluster_pair(
        ("cannot be undone", "This action cannot be undone"),
        ("可以撤销", "删除后仍可恢复"),
    )
    report, cluster_before, _, _ = _render_negative_control(
        clusters,
        [f"建议修复：{cluster.topic}" for cluster in clusters],
    )
    chief = report.split("## 主编结论", 1)[1]
    assert chief.count("建议修复：") == 2
    assert [cluster.model_dump(mode="json") for cluster in clusters] == cluster_before


def test_candidate_related_but_source_unrelated_work_items_remain_separate():
    clusters = _actionless_cluster_pair(
        ("cannot be undone", "permanent deletion"),
        ("可以撤销", "此操作可以撤销"),
    )
    report, cluster_before, _, _ = _render_negative_control(
        clusters,
        [f"建议修复：{cluster.topic}" for cluster in clusters],
    )
    chief = report.split("## 主编结论", 1)[1]
    assert chief.count("建议修复：") == 2
    assert [cluster.model_dump(mode="json") for cluster in clusters] == cluster_before
