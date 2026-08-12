import asyncio
import json

from council_of_translation.localization.models import ReviewTaskV2
from council_of_translation.localization.orchestration import run_structured_review
from council_of_translation.localization.persistence import ReviewStore
from council_of_translation.localization.roles import ROLE_REGISTRY, build_council_plan
from council_of_translation.localization.runtime import (
    RuntimeTelemetry,
    ScriptedModelExecutor,
    ScriptedUserInteractionGateway,
)


def _affirmation(role_id: str, index: int) -> str:
    return json.dumps({
        "role_feedback": "当前译文准确、自然且适合既定界面场景。",
        "findings": [{
            "agent_name": role_id,
            "source_span": "Continue",
            "candidate_span": "继续",
            "issue_type": "ux",
            "severity": "preference",
            "finding_kind": "affirmation",
            "proposed_value": "继续",
            "problem": "角色职责内确认当前候选可保留",
            "evidence": f"职责证据锚点 {index}",
            "action": "保持当前译文",
            "confidence": 0.9,
        }],
    }, ensure_ascii=False)


def test_six_live_shaped_affirmations_form_positive_consensus_and_distinct_lenses(tmp_path):
    roles = build_council_plan("standard").active_role_ids
    telemetry = RuntimeTelemetry(sample_budget=13)
    record = asyncio.run(run_structured_review(
        ReviewTaskV2(
            source_text="Continue",
            candidate_translation="继续",
            content_type="ui",
            briefing_mode="off",
        ),
        ScriptedModelExecutor([
            _affirmation(role_id, index) for index, role_id in enumerate(roles)
        ], telemetry),
        ScriptedUserInteractionGateway([], telemetry=telemetry),
        store=ReviewStore(tmp_path, include_legacy=False),
    ))

    assert record.runtime_metadata.reviewer_coverage == "full"
    assert record.runtime_metadata.sampling_calls == 6
    assert record.process_digest.consensus == [
        "所有专业视角均未发现阻碍发布的问题；共同支持保留“继续”。"
    ]
    assert "共同支持保留“继续”" in record.display_report
    assert "未形成需合并的实质共识项" not in record.display_report
    assert len(record.process_digest.role_lenses) == 6
    perspectives = [lens.perspective for lens in record.process_digest.role_lenses]
    assert len(set(perspectives)) == 6
    for role_id in roles:
        assert record.display_report.count(ROLE_REGISTRY[role_id].display_name) == 1
        assert role_id not in record.display_report
    assert len(record.display_report) <= 1_800


def test_partial_coverage_cannot_become_positive_consensus(tmp_path):
    roles = build_council_plan("standard").active_role_ids
    telemetry = RuntimeTelemetry(sample_budget=13)
    record = asyncio.run(run_structured_review(
        ReviewTaskV2(
            source_text="Continue",
            candidate_translation="继续",
            content_type="ui",
            briefing_mode="off",
        ),
        ScriptedModelExecutor([
            _affirmation(role_id, index) for index, role_id in enumerate(roles[:-1])
        ], telemetry),
        ScriptedUserInteractionGateway([], telemetry=telemetry),
        store=ReviewStore(tmp_path, include_legacy=False),
    ))

    assert record.runtime_metadata.reviewer_coverage == "partial"
    assert "共同支持" not in " ".join(record.process_digest.consensus)
    assert "评审覆盖不足" in record.display_report
    assert "结构化评审不可用" in record.display_report
    assert record.chief_editor_decision.review_needed == "是"
