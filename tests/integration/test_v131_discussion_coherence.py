import asyncio
import json

import pytest

from council_of_translation.localization.clustering import cluster_findings
from council_of_translation.localization.models import FindingV2
from council_of_translation.localization.models import ReviewTaskV2
from council_of_translation.localization.orchestration import run_structured_review
from council_of_translation.localization.persistence import ReviewStore
from council_of_translation.localization.runtime import (
    ModelExecutionResult,
    RuntimeTelemetry,
    ScriptedModelExecutor,
    ScriptedUserInteractionGateway,
)


def _review(findings=None):
    return json.dumps({"role_feedback": "bounded review", "findings": findings or []})


def _finding(action):
    return {
        "source_span": "Continue button",
        "candidate_span": "继续",
        "issue_type": "terminology",
        "severity": "major",
        "problem": "wording choice",
        "evidence": "bounded wording evidence",
        "action": action,
        "finding_kind": "choice",
        "proposed_value": action,
        "confidence": 0.8,
    }


def _reviews():
    return [
        _review(),
        _review(),
        _review([_finding("继续")]),
        _review(),
        _review(),
        _review([_finding("下一步")]),
    ]


def _run(tmp_path, discussion):
    telemetry = RuntimeTelemetry(sample_budget=13)
    executor = ScriptedModelExecutor([*_reviews(), discussion], telemetry)
    record = asyncio.run(
        run_structured_review(
            ReviewTaskV2(
                source_text="Continue button",
                candidate_translation="继续",
                content_type="ui",
                briefing_mode="off",
            ),
            executor,
            ScriptedUserInteractionGateway(supported=False, telemetry=telemetry),
            store=ReviewStore(tmp_path / "records", legacy_dir=tmp_path / "legacy"),
        )
    )
    return record, executor


def _issue_id():
    findings = []
    for role, action in (("terminology_reviewer", "继续"), ("fluency_reviewer", "下一步")):
        findings.append(FindingV2.model_validate({
            **_finding(action),
            "agent_name": role,
            "role_perspective": role,
        }))
    return cluster_findings(findings)[0].issue_id


@pytest.mark.parametrize(
    "discussion",
    [
        json.dumps({}),
        json.dumps({"turns": None}),
        json.dumps({"turns": "bad"}),
        json.dumps({"turns": 7}),
        json.dumps({"turns": ["bad"]}),
        json.dumps({"turns": [7]}),
        json.dumps({"turns": [None]}),
        json.dumps({"turns": [{}]}),
        json.dumps({"turns": [{"issue_id": "unknown", "speaker": "terminology_reviewer"}]}),
        json.dumps({"turns": [{"issue_id": "issue_missing", "speaker": "unknown"}]}),
        json.dumps({"turns": [{"issue_id": "issue_missing", "speaker": "terminology_reviewer", "stance": "bad"}]}),
        "not json",
        ModelExecutionResult(status="error", error="discussion executor failed"),
    ],
)
def test_malformed_discussion_fails_closed_without_retry(tmp_path, discussion):
    record, executor = _run(tmp_path, discussion)

    assert record.discussion_rounds == []
    assert record.degraded is True
    assert record.status == "NEEDS_HUMAN_REVIEW"
    assert record.chief_editor_decision.publishability == "需人工复核"
    assert record.chief_editor_decision.review_needed == "是"
    assert "discussion_unavailable" in record.warnings
    assert "discussion_unavailable" in record.fallback_reason
    assert next(item for item in record.phase_trace.phases if item.phase == "discussion").disposition == "degraded"
    assert record.runtime_metadata.sampling_calls == 7
    assert len(executor.prompts) == 7


def test_valid_empty_discussion_is_completed_without_discussion_degradation(tmp_path):
    record, executor = _run(tmp_path, json.dumps({"turns": []}))

    assert len(record.discussion_rounds) == 1
    assert record.discussion_rounds[0].turns == []
    assert "discussion_unavailable" not in record.warnings
    assert "discussion_unavailable" not in record.fallback_reason
    assert next(item for item in record.phase_trace.phases if item.phase == "discussion").disposition == "completed"
    assert len(executor.prompts) == 7


def test_valid_discussion_convergence_updates_every_derived_view(tmp_path):
    issue_id = _issue_id()
    discussion = json.dumps({"turns": [{
        "issue_id": issue_id,
        "speaker": "terminology_reviewer",
        "stance": "reconsider",
        "claim": "bounded context favors the alternative",
        "evidence": ["candidate_span:继续"],
        "proposed_action": "下一步",
        "confidence": 0.9,
        "position_changed": True,
    }]})
    record, _ = _run(tmp_path, discussion)

    cluster = record.issue_clusters[0]
    assert cluster.consensus_status == "consensus"
    assert len({position.option_id for position in cluster.positions if position.option_id}) == 1
    assert record.council_value_metrics.discussion_position_change_count == 1
    assert record.council_value_metrics.discussion_resolved_issue_count == 1
    assert cluster.topic in record.deliberation_summary.consensus
    assert cluster.topic not in record.deliberation_summary.material_disagreement
    assert cluster.topic not in record.process_digest.material_disagreements
    assert record.process_digest.minority_report.role_ids == []
    assert "material_disagreement" not in record.decision_support.limitation_codes


def test_valid_discussion_without_position_change_preserves_genuine_split(tmp_path):
    issue_id = _issue_id()
    discussion = json.dumps({"turns": [{
        "issue_id": issue_id,
        "speaker": "terminology_reviewer",
        "stance": "challenge",
        "claim": "the alternatives remain materially distinct",
        "evidence": [],
        "confidence": 0.8,
        "position_changed": False,
    }]})
    record, _ = _run(tmp_path, discussion)

    cluster = record.issue_clusters[0]
    assert cluster.consensus_status == "disputed"
    assert cluster.topic in record.deliberation_summary.material_disagreement
    assert cluster.topic in record.process_digest.material_disagreements
    assert "material_disagreement" in record.decision_support.limitation_codes
