import json

from council_of_translation.localization.digest import build_process_digest, render_display_report
from council_of_translation.localization.models import (
    ChiefEditorDecisionV2,
    CouncilValueMetrics,
    IssueCluster,
    PhaseReconsiderationProvenance,
    ProcessDigestV2,
    ReviewBriefV2,
    ReviewTaskV2,
)
from council_of_translation.localization.roles import build_council_plan
from council_of_translation.localization.runtime import RuntimeTelemetry


MODIFIED_FINAL = "最终处置：修改后可发布；需人工复核：否"
HUMAN_FINAL = "最终处置：需人工复核；需人工复核：是"
PUBLISHABLE_FINAL = "最终处置：可发布；需人工复核：否"


def _legal_digest(final: str, *, action_count: int = 7, padded: bool = False) -> ProcessDigestV2:
    suffix = "；需保留完整风险含义" + "甲" * 180 if padded else ""
    return ProcessDigestV2(
        case_brief=[
            "领域/内容类型：法律风险审校",
            "风险审校路线：覆盖语义、术语、产品语境、用户理解、风险歧义与语言自然度。",
        ],
        blind_spots=["结论限于调用方提供的规则和文本。" + ("乙" * 220 if padded else "")],
        editor_synthesis=["主编按结构化证据保留最终处置。" + ("丙" * 220 if padded else "")],
        execution_checklist_final_disposition=[
            *[f"建议修复：法律风险事项 {index}{suffix}" for index in range(action_count)],
            final,
        ],
    )


def _bytes(value) -> bytes:
    return json.dumps(
        value.model_dump(mode="json"),
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")


def test_long_legal_action_projection_preserves_structured_modified_final_once_and_last():
    task = ReviewTaskV2(
        source_text="You may withdraw after notice.",
        candidate_translation="通知后可以撤回。",
        content_type="legal_risk",
        briefing_mode="off",
        interactive_mode="off",
    )
    plan = build_council_plan("standard", "legal_risk")
    reviews = [
        {
            "agent_name": role_id,
            "sample_status": "structured_success",
            "role_feedback": "完成职责内审校。",
            "findings": [],
        }
        for role_id in plan.active_role_ids
    ]
    chief = ChiefEditorDecisionV2(
        publishability="修改后可发布",
        review_needed="否",
        should_fix=[f"法律风险事项 {index}" for index in range(9)],
    )
    clusters = [
        IssueCluster(
            issue_id="issue_scope",
            topic="授权范围需要收窄。",
            category="correctness",
            finding_ids=["finding_scope"],
        )
    ]
    digest = build_process_digest(
        task=task,
        brief=ReviewBriefV2(content_type="legal_risk"),
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
    metrics = CouncilValueMetrics()
    telemetry = RuntimeTelemetry(sample_budget=13)
    before = (_bytes(digest), _bytes(chief), [_bytes(cluster) for cluster in clusters], _bytes(metrics))
    telemetry_before = telemetry.snapshot().model_dump(mode="json")

    report = render_display_report(digest, metrics=metrics, clusters=clusters)

    assert report.count(MODIFIED_FINAL) == 1
    assert HUMAN_FINAL not in report
    assert report.splitlines()[-1] == f"- {MODIFIED_FINAL}"
    assert report.split("## 主编结论", 1)[1].count("建议修复：") == 4
    assert before == (_bytes(digest), _bytes(chief), [_bytes(cluster) for cluster in clusters], _bytes(metrics))
    assert telemetry.snapshot().model_dump(mode="json") == telemetry_before
    assert telemetry.sampling_calls == telemetry.elicitation_calls == 0


def test_long_true_human_review_and_clean_publishable_dispositions_remain_truthful():
    human = render_display_report(_legal_digest(HUMAN_FINAL), metrics=CouncilValueMetrics())
    clean = render_display_report(
        ProcessDigestV2(
            case_brief=["清洁法律风险对照。"],
            execution_checklist_final_disposition=[PUBLISHABLE_FINAL],
        ),
        metrics=CouncilValueMetrics(),
    )

    assert human.count(HUMAN_FINAL) == 1
    assert human.splitlines()[-1] == f"- {HUMAN_FINAL}"
    assert clean.count(PUBLISHABLE_FINAL) == 1
    assert clean.splitlines()[-1] == f"- {PUBLISHABLE_FINAL}"


def test_pending_and_degraded_long_case_keeps_warnings_and_never_grants_release():
    report = render_display_report(
        _legal_digest(HUMAN_FINAL),
        metrics=CouncilValueMetrics(),
        status="RETURNED_PENDING",
        degraded=True,
        warnings=["部分独立评审不可用。"],
        fallback_reason="reviewer_coverage_partial",
    )

    assert "存在降级或回退" in report
    assert "审校尚待补充信息或决定" in report
    assert MODIFIED_FINAL not in report and PUBLISHABLE_FINAL not in report
    assert report.count(HUMAN_FINAL) == 1
    assert report.splitlines()[-1] == f"- {HUMAN_FINAL}"


def test_terminal_disposition_survives_hard_cap_as_exact_last_line():
    digest = _legal_digest(MODIFIED_FINAL, action_count=7, padded=True)
    digest.assumptions_context_confidence = [f"上下文假设 {index} " + "丁" * 220 for index in range(8)]
    digest.consensus = [f"共识 {index} " + "戊" * 220 for index in range(6)]
    digest.material_disagreements = [f"分歧 {index} " + "己" * 220 for index in range(6)]
    digest.context_gaps_answers = [f"背景缺口 {index} " + "庚" * 220 for index in range(6)]
    digest.user_decisions = [f"用户决定 {index} " + "辛" * 220 for index in range(6)]
    digest.reconsideration_changes = [f"复议变化 {index} " + "壬" * 220 for index in range(6)]
    before = _bytes(digest)

    report = render_display_report(digest, metrics=CouncilValueMetrics())

    assert len(report) <= 3_200
    assert report.count(MODIFIED_FINAL) == 1
    assert report.splitlines()[-1] == f"- {MODIFIED_FINAL}"
    assert _bytes(digest) == before
