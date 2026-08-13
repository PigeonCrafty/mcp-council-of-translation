import asyncio
import json

from council_of_translation.localization.digest import build_process_digest, render_display_report
from council_of_translation.localization.models import (
    ChiefEditorDecisionV2,
    ContextGapV2,
    MinorityReport,
    PhaseReconsiderationProvenance,
    ProcessDigestV2,
    ReviewBriefV2,
    ReviewTaskV2,
    RoleLens,
)
from council_of_translation.localization.orchestration import run_structured_review
from council_of_translation.localization.persistence import ReviewStore
from council_of_translation.localization.roles import ROLE_REGISTRY, build_council_plan
from council_of_translation.localization.runtime import (
    RuntimeTelemetry,
    ScriptedModelExecutor,
    ScriptedUserInteractionGateway,
)


def test_suppressed_gap_is_not_rendered_as_user_interaction():
    task = ReviewTaskV2(content_type="marketing")
    digest = build_process_digest(
        task=task,
        brief=ReviewBriefV2(content_type="marketing"),
        plan=build_council_plan("standard", "marketing"),
        independent_reviews=[],
        clusters=[],
        context_gaps=[ContextGapV2(
            gap_id="gap_suppressed",
            question="产品经理最喜欢哪种颜色？",
            materiality="只是好奇",
            disposition="suppressed",
            reason="immaterial_gap",
        )],
        user_decisions=[],
        context_provenance=PhaseReconsiderationProvenance(),
        outcome_provenance=PhaseReconsiderationProvenance(),
        chief=ChiefEditorDecisionV2(publishability="可发布", review_needed="否"),
        reviewer_coverage="full",
    )
    report = render_display_report(digest)
    assert "产品经理最喜欢哪种颜色" not in report
    assert "已抑制" not in report
    assert "## 你的决定与复议" not in report


def test_raw_ux_and_composed_punctuation_are_normalized_without_hiding_evidence():
    digest = ProcessDigestV2(
        role_lenses=[RoleLens(
            role_id="product_context_reviewer",
            perspective="发现ux问题：按钮用途不明确。",
            evidence=["需要确认是品牌标语还是功能按钮。"],
        )],
        blind_spots=["品牌用途尚待确认。"],
        minority_report=MinorityReport(
            dissent="若它是功能按钮，当前译法可能误导。",
            decisive_condition="确认真实组件用途。",
        ),
        editor_synthesis=["关键背景未解决，必须人工确认。"],
        execution_checklist_final_disposition=["最终处置：需人工复核；需人工复核：是"],
    )
    report = render_display_report(digest, degraded=True)
    assert "发现用户体验问题" in report
    assert "ux" not in report.casefold()
    assert "。；依据" not in report and "；；" not in report
    assert "依据：需要确认是品牌标语还是功能按钮。" in report
    assert "少数意见" in report and "决定条件" in report
    assert len(report) <= 3_200
    assert report.splitlines()[-1] == "- 最终处置：需人工复核；需人工复核：是"


def test_literal_v22_record_runtime_and_role_invariants(tmp_path):
    roles = build_council_plan("standard", "marketing").active_role_ids
    reviews = [json.dumps({
        "role_feedback": "职责内检查完成。",
        "findings": [{
            "source_span": "Bigger",
            "candidate_span": "更大",
            "issue_type": "style",
            "severity": "minor",
            "finding_kind": "affirmation",
            "problem": "当前译法可接受",
            "evidence": "与品牌语境一致",
            "action": "保留",
            "confidence": 0.8,
        }],
    }, ensure_ascii=False) for _ in roles]
    telemetry = RuntimeTelemetry(sample_budget=13)
    record = asyncio.run(run_structured_review(
        ReviewTaskV2(
            source_text="Bigger", candidate_translation="更大",
            content_type="marketing", briefing_mode="off",
        ),
        ScriptedModelExecutor(reviews, telemetry),
        ScriptedUserInteractionGateway([], telemetry=telemetry),
        store=ReviewStore(tmp_path, include_legacy=False),
    ))
    payload = record.model_dump(mode="json")
    assert payload["schema_version"] == "2.3"
    assert payload["council_plan"]["active_role_ids"] == roles
    assert all(role_id in ROLE_REGISTRY for role_id in roles)
    assert {review["sample_status"] for review in payload["independent_reviews"]} == {"structured_success"}
    assert payload["runtime_metadata"]["reviewer_coverage"] == "full"
    assert payload["runtime_metadata"]["reviewer_samples_successful"] == 6
    assert payload["runtime_metadata"]["reviewer_samples_unavailable"] == 0
    assert payload["runtime_metadata"]["sampling_calls"] == 6
    assert payload["runtime_metadata"]["elicitation_calls"] == 0
    assert len(payload["process_digest"]["role_lenses"]) == 6
