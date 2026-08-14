import asyncio
import json

from council_of_translation.localization.clustering import cluster_findings
from council_of_translation.localization.deliberation import normalize_discussion_round
from council_of_translation.localization.digest import build_process_digest, render_display_report
from council_of_translation.localization.models import (
    ChiefEditorDecisionV2,
    FindingV2,
    PhaseReconsiderationProvenance,
    ReviewBriefV2,
    ReviewRecordV2,
    ReviewTaskV2,
)
from council_of_translation.localization.orchestration import run_structured_review
from council_of_translation.localization.persistence import ReviewStore
from council_of_translation.localization.preflight import run_preflight
from council_of_translation.localization.roles import ROLE_REGISTRY, build_council_plan
from council_of_translation.localization.runtime import (
    RuntimeTelemetry,
    ScriptedModelExecutor,
    ScriptedUserInteractionGateway,
)
from council_of_translation.localization.value_metrics import compute_council_value_metrics


HEADINGS = [
    "## 审校背景",
    "## Council 新增视角",
    "## 角色覆盖与分工",
    "## 共识、分歧与盲区",
    "## 主编结论",
]


def test_live_shaped_case_a_groups_six_confirmations_without_mutating_full_record(tmp_path):
    clean = json.dumps({
        "role_feedback": "职责范围内未发现实质问题。",
        "findings": [],
    })
    telemetry = RuntimeTelemetry(sample_budget=13)
    record = asyncio.run(run_structured_review(
        ReviewTaskV2(
            source_text="Bigger than bigger",
            candidate_translation="比大更大",
            content_type="marketing",
            context="官网首页的纯品牌标语，不承担交互动作。",
            audience="中国大陆普通消费者",
            term_glossary="Bigger than bigger = 比大更大（项目批准译法）",
            style_guide="品牌标语保持短促、自然、有冲击力。",
            project_rules="保留项目批准译法。",
            briefing_mode="off",
            interactive_mode="off",
        ),
        ScriptedModelExecutor([clean] * 6, telemetry),
        ScriptedUserInteractionGateway([], telemetry=telemetry),
        store=ReviewStore(tmp_path, include_legacy=False),
    ))
    before = record.model_dump(mode="json")

    rerendered = render_display_report(
        record.process_digest,
        metrics=record.council_value_metrics,
        status=record.status,
        clusters=record.issue_clusters,
    )

    assert rerendered == record.display_report
    assert record.model_dump(mode="json") == before
    assert len(record.independent_reviews) == len(record.council_plan.active_role_ids) == 6
    assert all(review["sample_status"] == "structured_success" for review in record.independent_reviews)
    assert all(review["findings"] == [] for review in record.independent_reviews)
    assert all(
        item.contribution_kind == "confirmation_only"
        for item in record.council_value_metrics.role_contributions
    )
    assert [line for line in rerendered.splitlines() if line.startswith("## ")] == HEADINGS
    coverage_line = next(line for line in rerendered.splitlines() if "完成确认性覆盖" in line)
    assert rerendered.count("完成确认性覆盖") == 1
    for role_id in record.council_plan.active_role_ids:
        role_name = ROLE_REGISTRY[role_id].display_name
        assert rerendered.count(role_name) == 1
        assert role_name in coverage_line
    assert len(rerendered) <= 1_200
    assert rerendered.splitlines()[-1] == "- 最终处置：可发布；需人工复核：否"


def test_live_shaped_case_b_keeps_full_evidence_but_collapses_primary_repetition():
    task = ReviewTaskV2(
        source_text="Delete {count} files? This action cannot be undone.",
        candidate_translation="删除文件吗？此操作可以撤销。",
        content_type="ui",
        context="批量永久删除前的确认对话框正文。",
        audience="中国大陆普通软件用户",
        project_rules="不得遗漏数量占位符；不得把不可撤销改成可以撤销。",
        technical_constraints="必须逐字保留 {count}。",
        do_not_translate_literals=["{count}"],
        hard_constraints=["required_literal:{count}"],
        briefing_mode="off",
        interactive_mode="off",
    )
    plan = build_council_plan("standard", "ui")
    findings = [
        FindingV2(
            agent_name=role_id,
            role_perspective=ROLE_REGISTRY[role_id].display_name,
            issue_type="technical",
            severity="critical",
            source_span="{count}",
            problem="The protected placeholder is missing.",
            evidence="{count}",
            action="Restore {count}.",
        )
        for role_id in plan.active_role_ids
    ]
    findings.append(FindingV2(
        agent_name="fidelity_reviewer",
        role_perspective=ROLE_REGISTRY["fidelity_reviewer"].display_name,
        issue_type="accuracy",
        severity="critical",
        source_span="cannot",
        candidate_span="可以",
        problem="The irreversibility meaning is reversed.",
        evidence="cannot differs from 可以",
        action="Restore the cannot meaning.",
    ))
    preflight = run_preflight(
        task.source_text,
        task.candidate_translation,
        do_not_translate=task.do_not_translate_literals,
        hard_constraints=task.hard_constraints,
    )
    clusters = cluster_findings(findings, preflight)
    placeholder_cluster = next(
        cluster
        for cluster in clusters
        if cluster.finding_ids and "{count}" in cluster.source_spans
    )
    paraphrases = [
        "The {count} placeholder must remain.",
        "Permanent deletion is the supplied context.",
        "Cannot must not become can.",
        "The existing project rule forbids reversibility.",
        "Keep {count} exactly as already required.",
        "The permanent-delete and cannot facts are unchanged.",
    ]
    discussion = normalize_discussion_round(
        "round_1",
        clusters,
        [
            {
                "issue_id": placeholder_cluster.issue_id,
                "speaker": role_id,
                "claim": "Restates an existing validated fact.",
                "evidence": [paraphrases[index]],
                "position_changed": False,
            }
            for index, role_id in enumerate(plan.active_role_ids)
        ],
    )
    reviews = [
        {
            "agent_name": role_id,
            "sample_status": "structured_success",
            "role_feedback": "完成职责内审校。",
            "findings": [
                finding.model_dump(mode="json")
                for finding in findings
                if finding.agent_name == role_id
            ],
        }
        for role_id in plan.active_role_ids
    ]
    chief = ChiefEditorDecisionV2(
        publishability="需人工复核",
        must_fix=[
            "恢复缺失的 {count} 占位符。",
            "满足 required_literal:{count} 硬规则。",
            "修复 {count} 的数量插值完整性。",
            "不得把 cannot 改成可以。",
        ],
        execution_order=["先恢复 {count}，再修复 cannot 语义。"],
        review_needed="是",
        review_reason="存在确定性技术阻断与独立语义反转。",
    )
    brief = ReviewBriefV2(content_type="ui", usage_context=task.context, audience=task.audience)
    digest = build_process_digest(
        task=task,
        brief=brief,
        plan=plan,
        independent_reviews=reviews,
        clusters=clusters,
        context_gaps=[],
        user_decisions=[],
        context_provenance=PhaseReconsiderationProvenance(),
        outcome_provenance=PhaseReconsiderationProvenance(),
        chief=chief,
        reviewer_coverage="full",
    )
    metrics = compute_council_value_metrics(
        active_role_ids=plan.active_role_ids,
        independent_reviews=reviews,
        clusters=clusters,
        discussion_rounds=[discussion],
    )
    record = ReviewRecordV2(
        review_id="synthetic-case-b",
        task=task,
        council_plan=plan,
        preflight=preflight,
        independent_reviews=reviews,
        issue_clusters=clusters,
        discussion_rounds=[discussion],
        chief_editor_decision=chief,
        status="NEEDS_HUMAN_REVIEW",
        process_digest=digest,
        council_value_metrics=metrics,
    )
    before = record.model_dump(mode="json")

    report = render_display_report(
        record.process_digest,
        metrics=record.council_value_metrics,
        status=record.status,
        clusters=record.issue_clusters,
    )

    assert metrics.discussion_new_evidence_count == 0
    assert metrics.discussion_position_change_count == 0
    assert metrics.discussion_resolved_issue_count == 0
    assert metrics.discussion_marginal_value == "none"
    assert "讨论补充 6 条新证据" not in report
    assert "讨论未增加新的结构化证据，也未改变立场" in report
    assert sum("{count}" in item for item in chief.must_fix) == 3
    chief_section = report.split("## 主编结论", 1)[1]
    assert sum("{count}" in line for line in chief_section.splitlines()) == 1
    assert "不得把 cannot 改成可以" in chief_section
    assert report.splitlines()[-1] == "- 最终处置：需人工复核；需人工复核：是"
    assert record.model_dump(mode="json") == before
    assert len(record.independent_reviews) == 6
    assert len(record.preflight.checks) >= 3
    assert len(record.issue_clusters) >= 3
    assert len(record.discussion_rounds[0].turns) == 6
    assert len(record.chief_editor_decision.must_fix) == 4
