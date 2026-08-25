import asyncio
import json

import pytest

from council_of_translation.localization.models import ReviewRecordV2, ReviewTaskV2
from council_of_translation.localization.orchestration import (
    _bounded_decision_suppressions,
    compact_review_response,
    run_structured_review,
)
from council_of_translation.localization.persistence import ReviewStore
from council_of_translation.localization.runtime import (
    RuntimeTelemetry,
    ScriptedModelExecutor,
    ScriptedUserInteractionGateway,
)


def _envelope(findings=None):
    return json.dumps(
        {"role_feedback": "checked", "findings": findings or []},
        ensure_ascii=False,
    )


def _finding(**updates):
    value = {
        "source_span": "Continue",
        "candidate_span": "继续",
        "issue_type": "ux",
        "severity": "minor",
        "problem": "wording choice",
        "evidence": "UI context",
        "action": "review advice only",
    }
    value.update(updates)
    return value


def _run_case(tmp_path, findings, *, task=None, name="case"):
    scripts = [_envelope([finding]) for finding in findings]
    scripts.extend(_envelope() for _ in range(6 - len(scripts)))
    telemetry = RuntimeTelemetry(sample_budget=10)
    gateway = ScriptedUserInteractionGateway(supported=True, telemetry=telemetry)
    store = ReviewStore(tmp_path / name / "records", legacy_dir=tmp_path / name / "legacy")
    record = asyncio.run(run_structured_review(
        task or ReviewTaskV2(
            source_text="Continue",
            candidate_translation="继续",
            content_type="ui",
            briefing_mode="off",
        ),
        ScriptedModelExecutor(scripts, telemetry),
        gateway,
        store=store,
    ))
    return record, compact_review_response(record), gateway, store


def test_two_omitted_classification_actions_create_no_selectable_outcome(tmp_path):
    actions = [
        "请结合完整页面流程决定是否保留当前措辞。",
        "请改为更明确且更长的下一步操作说明。",
    ]
    record, _, gateway, _ = _run_case(
        tmp_path,
        [_finding(action=action) for action in actions],
        name="omitted",
    )
    language_cluster = next(
        cluster for cluster in record.issue_clusters if cluster.category == "language_choice"
    )
    assert language_cluster.candidate_actions == ["继续"]
    assert record.decision_points == []
    assert gateway.requests == []
    selectable = json.dumps(
        {
            "candidate_actions": language_cluster.candidate_actions,
            "decision_points": [point.model_dump() for point in record.decision_points],
        },
        ensure_ascii=False,
    )
    assert all(action not in selectable for action in actions)


@pytest.mark.parametrize(
    "updates",
    [
        {"finding_kind": "issue"},
        {"finding_kind": "invalid-kind"},
        {"finding_kind": "choice", "proposed_value": ""},
        {"finding_kind": "choice", "proposed_value": 123},
        {"finding_kind": "choice", "proposed_value": "长" * 501},
    ],
)
def test_invalid_or_incomplete_classification_never_promotes_action(tmp_path, updates):
    action = "不得成为选项的内部操作说明"
    record, _, gateway, _ = _run_case(
        tmp_path,
        [_finding(action=action, **updates)],
        name=str(len(json.dumps(updates, ensure_ascii=False))),
    )
    assert record.decision_points == []
    assert gateway.requests == []
    assert all(
        action not in cluster.candidate_actions
        for cluster in record.issue_clusters
    )


@pytest.mark.parametrize(
    ("name", "candidate", "candidate_span", "reason"),
    [
        ("ambiguous", "继续 / 继续", "继续", "ambiguous_candidate_anchor"),
        ("missing", "继续", "不存在", "missing_candidate_anchor"),
    ],
)
def test_anchor_suppression_persists_and_surfaces_truthful_degradation(
    tmp_path, name, candidate, candidate_span, reason
):
    record, compact, gateway, store = _run_case(
        tmp_path,
        [_finding(
            candidate_span=candidate_span,
            finding_kind="choice",
            proposed_value="下一步",
        )],
        task=ReviewTaskV2(
            source_text="Continue / Continue" if name == "ambiguous" else "Continue",
            candidate_translation=candidate,
            content_type="ui",
            briefing_mode="off",
        ),
        name=name,
    )
    expected = [{
        "issue_id": record.issue_clusters[0].issue_id,
        "decision_id": f"decision_{record.issue_clusters[0].issue_id.removeprefix('issue_')}",
        "reason_code": reason,
    }]
    warning = f"decision_suppressed:{reason}"
    assert record.decision_points == []
    assert gateway.requests == []
    assert record.policy_gate_result["decision_suppressions"] == expected
    assert record.warnings == compact["warnings"] == [warning]
    assert record.degraded is compact["degraded"] is True
    assert record.fallback_reason == compact["fallback_reason"] == "decision_validation_degraded"
    assert record.decision_support.level == "insufficient"
    assert record.decision_support.outcome_coherent is True
    assert record.chief_editor_decision.publishability == "需人工复核"
    assert record.chief_editor_decision.review_needed == "是"
    assert record.status == compact["status"] == "NEEDS_HUMAN_REVIEW"
    loaded = store.load(record.review_id)
    assert isinstance(loaded, ReviewRecordV2)
    assert loaded.policy_gate_result["decision_suppressions"] == expected
    assert set(expected[0]) == {"issue_id", "decision_id", "reason_code"}
    assert all(len(value) <= 80 for value in expected[0].values())


def test_metadata_keeps_safe_degraded_disposition_but_not_suppression_details(tmp_path):
    record, _, _, store = _run_case(
        tmp_path,
        [_finding(finding_kind="choice", proposed_value="下一步")],
        task=ReviewTaskV2(
            source_text="Continue / Continue",
            candidate_translation="继续 / 继续",
            content_type="ui",
            history_mode="metadata",
            briefing_mode="off",
        ),
        name="metadata",
    )
    payload = store.path_for(record.review_id).read_text(encoding="utf-8")
    loaded = store.load(record.review_id)
    assert isinstance(loaded, ReviewRecordV2)
    assert loaded.decision_support.level == "insufficient"
    assert loaded.decision_support.outcome_coherent is True
    assert loaded.chief_editor_decision.publishability == "需人工复核"
    assert loaded.chief_editor_decision.review_needed == "是"
    assert loaded.status == "NEEDS_HUMAN_REVIEW"
    assert loaded.degraded is True
    assert loaded.policy_gate_result == {}
    assert loaded.warnings == []
    assert "decision_suppressions" not in payload
    assert "ambiguous_candidate_anchor" not in payload
    assert "继续" not in payload
    assert "下一步" not in payload


def test_suppression_provenance_is_bounded_deduplicated_and_content_free():
    valid = {
        "issue_id": "issue_123456789abc",
        "decision_id": "decision_123456789abc",
        "reason_code": "missing_candidate_anchor",
        "private_text": "不得保留",
    }
    values = [valid, valid, {
        **valid,
        "issue_id": "issue_abcdefabcdef",
        "decision_id": "decision_abcdefabcdef",
        "reason_code": "ambiguous_candidate_anchor",
    }]
    values.extend({
        **valid,
        "issue_id": f"issue_{index:012d}",
        "decision_id": f"decision_{index:012d}",
    } for index in range(20))
    values.extend([
        {**valid, "reason_code": "PRIVATE REASON"},
        {**valid, "issue_id": "private text with spaces"},
        {**valid, "decision_id": "x" * 81},
    ])
    normalized = _bounded_decision_suppressions(values)
    assert len(normalized) == 8
    assert len({tuple(item.values()) for item in normalized}) == 8
    assert all(set(item) == {"issue_id", "decision_id", "reason_code"} for item in normalized)
    assert all(item["reason_code"] in {
        "missing_candidate_anchor",
        "ambiguous_candidate_anchor",
    } for item in normalized)
    assert "不得保留" not in json.dumps(normalized, ensure_ascii=False)


def test_protected_token_loss_is_normal_policy_invalidation_not_degradation(tmp_path):
    record, compact, gateway, _ = _run_case(
        tmp_path,
        [_finding(
            source_span="Continue {count}",
            candidate_span="继续 {count}",
            finding_kind="choice",
            proposed_value="下一步",
        )],
        task=ReviewTaskV2(
            source_text="Continue {count}",
            candidate_translation="继续 {count}",
            content_type="ui",
            briefing_mode="off",
        ),
        name="protected-loss",
    )
    assert record.decision_points == []
    assert gateway.requests == []
    assert record.policy_gate_result["decision_suppressions"] == []
    assert record.warnings == compact["warnings"] == []
    assert record.degraded is compact["degraded"] is False
    assert "decision_validation_degraded" not in record.fallback_reason
    assert record.status == "COMPLETED"
