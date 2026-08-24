import asyncio
import json

import pytest

from council_of_translation.localization.models import FindingV2, ReviewTaskV2
from council_of_translation.localization.orchestration import run_structured_review
from council_of_translation.localization.persistence import ReviewStore
from council_of_translation.localization.runtime import (
    ElicitationResult,
    RuntimeTelemetry,
    ScriptedModelExecutor,
    ScriptedUserInteractionGateway,
)


def run(coro):
    return asyncio.run(coro)


def _review(findings=None):
    return json.dumps({"role_feedback": "focused feedback", "findings": findings or []})


def _finding(action: str, *, confidence: float = 0.8):
    return {
        "source_span": "Continue button",
        "candidate_span": "继续",
        "issue_type": "terminology",
        "severity": "minor",
        "problem": "wording choice",
        "evidence": "both preserve meaning",
        "action": action,
        "finding_kind": "choice",
        "proposed_value": action,
        "confidence": confidence,
    }


def _standard_script(*, discussion=None, reconsider=False):
    reviews = [
        _review(),
        _review(),
        _review([_finding("继续")]),
        _review(),
        _review(),
        _review([_finding("下一步")]),
    ]
    script = [*reviews, json.dumps({"turns": discussion or []})]
    if reconsider:
        from council_of_translation.localization.clustering import cluster_findings
        from council_of_translation.localization.deliberation import build_decision_points

        findings = [
            FindingV2(agent_name="terminology_reviewer", source_span="Continue button", candidate_span="继续", issue_type="terminology", problem="wording choice", evidence="both preserve meaning", action="继续", finding_kind="choice", proposed_value="继续", confidence=0.8),
            FindingV2(agent_name="fluency_reviewer", source_span="Continue button", candidate_span="继续", issue_type="fluency", problem="wording choice", evidence="both preserve meaning", action="下一步", finding_kind="choice", proposed_value="下一步", confidence=0.8),
        ]
        point = build_decision_points(cluster_findings(findings))[0]
        selected = point.options[1].option_id
        payload = json.dumps({"positions": [{"issue_id": point.issue_id, "stance": "accept", "option_id": selected, "claim": "accepted", "confidence": 0.9}]})
        script.extend([payload, payload])
    return script


@pytest.mark.parametrize("action", ["unsupported", "decline", "cancel", "off"])
def test_production_noninteractive_fallback_selects_expected_non_tied_option(action, tmp_path):
    telemetry = RuntimeTelemetry(sample_budget=3)
    if action == "unsupported":
        gateway = ScriptedUserInteractionGateway(supported=False, telemetry=telemetry)
        interactive_mode = "auto"
    elif action == "off":
        gateway = ScriptedUserInteractionGateway(supported=True, telemetry=telemetry)
        interactive_mode = "off"
    else:
        gateway = ScriptedUserInteractionGateway([ElicitationResult(action=action)], telemetry=telemetry)
        interactive_mode = "auto"
    record = run(
        run_structured_review(
            ReviewTaskV2(source_text="Continue", candidate_translation="继续", content_type="ui", interactive_mode=interactive_mode, briefing_mode="off"),
            ScriptedModelExecutor(_standard_script(), telemetry),
            gateway,
            store=ReviewStore(tmp_path / action, legacy_dir=tmp_path / "legacy"),
        )
    )

    point_ids = {option.option_id for option in record.decision_points[0].options}
    position_ids = {position.option_id for position in record.issue_clusters[0].positions}
    entry = record.decision_trace.entries[0]
    assert point_ids == position_ids
    assert record.decision_support.level == "insufficient"
    assert record.decision_support.outcome_coherent is True
    assert record.chief_editor_decision.publishability == "需人工复核"
    assert record.chief_editor_decision.review_needed == "是"
    assert record.status == "NEEDS_HUMAN_REVIEW"
    assert entry.outcome == "council_fallback"
    assert entry.decision == "继续"
    assert entry.selected_option_id in point_ids
    assert "position_matrix" in entry.basis
    assert record.fallback_reason == (
        "user_interaction_unsupported" if action in {"unsupported", "off"}
        else f"user_interaction_{action}"
    )
    assert record.degraded is False
    assert record.warnings == []
    assert record.runtime_metadata.sampling_calls == 7
    assert record.runtime_metadata.elicitation_calls == (0 if action in {"unsupported", "off"} else 1)
    assert record.runtime_metadata.sample_budget == 13
    assert "option_" not in json.dumps(record.chief_editor_decision.model_dump(), ensure_ascii=False)
    assert any("继续" in item for item in record.chief_editor_decision.terminology_decisions)


def test_production_discussion_change_updates_matrix_used_by_fallback(tmp_path):
    discussion = [{
        "issue_id": "issue_placeholder",
        "speaker": "terminology_reviewer",
        "stance": "reconsider",
        "claim": "navigation context",
        "evidence": ["advances a step"],
        "proposed_action": "下一步",
        "confidence": 0.95,
        "position_changed": True,
    }]
    # Issue IDs are deterministic but source-derived; fill the production ID from the same findings.
    from council_of_translation.localization.clustering import cluster_findings

    issue = cluster_findings([
        FindingV2(agent_name="terminology_reviewer", source_span="Continue button", candidate_span="继续", issue_type="terminology", problem="wording choice", evidence="both preserve meaning", action="继续", finding_kind="choice", proposed_value="继续", confidence=0.8),
        FindingV2(agent_name="fluency_reviewer", source_span="Continue button", candidate_span="继续", issue_type="fluency", problem="wording choice", evidence="both preserve meaning", action="下一步", finding_kind="choice", proposed_value="下一步", confidence=0.8),
    ])[0]
    discussion[0]["issue_id"] = issue.issue_id
    telemetry = RuntimeTelemetry(sample_budget=10)
    record = run(run_structured_review(
        ReviewTaskV2(source_text="Continue", candidate_translation="继续", content_type="ui", briefing_mode="off"),
        ScriptedModelExecutor(_standard_script(discussion=discussion), telemetry),
        ScriptedUserInteractionGateway(supported=False, telemetry=telemetry),
        store=ReviewStore(tmp_path / "records", legacy_dir=tmp_path / "legacy"),
    ))

    assert record.discussion_rounds[0].turns[0].position_changed is True
    assert len({position.option_id for position in record.issue_clusters[0].positions}) == 1
    assert record.decision_trace.entries[0].decision == "下一步"


def test_production_genuine_tie_remains_human_review(tmp_path):
    reviews = [_review(), _review(), _review([_finding("继续"), _finding("下一步")]), _review(), _review(), _review()]
    telemetry = RuntimeTelemetry(sample_budget=10)
    record = run(run_structured_review(
        ReviewTaskV2(source_text="Continue", candidate_translation="继续", content_type="ui", briefing_mode="off"),
        ScriptedModelExecutor(reviews, telemetry),
        ScriptedUserInteractionGateway(supported=False, telemetry=telemetry),
        store=ReviewStore(tmp_path / "records", legacy_dir=tmp_path / "legacy"),
    ))
    assert record.status == "NEEDS_HUMAN_REVIEW"
    assert record.decision_trace.entries[0].outcome == "human_review"
    assert record.runtime_metadata.sampling_calls == 6
    assert record.runtime_metadata.elicitation_calls == 0


@pytest.mark.parametrize(("mode", "calls", "budget"), [("lightweight", 4, 6), ("standard", 6, 13), ("strict", 8, 18)])
def test_active_plan_budget_replaces_stale_telemetry_budget(mode, calls, budget, tmp_path):
    telemetry = RuntimeTelemetry(sample_budget=3)
    record = run(run_structured_review(
        ReviewTaskV2(source_text="Save", candidate_translation="保存", mode=mode, briefing_mode="off"),
        ScriptedModelExecutor([_review()] * calls, telemetry),
        ScriptedUserInteractionGateway(supported=True, telemetry=telemetry),
        store=ReviewStore(tmp_path / mode, legacy_dir=tmp_path / "legacy"),
    ))
    assert record.runtime_metadata.sample_budget == budget
    assert record.runtime_metadata.sampling_calls == calls
    assert record.runtime_metadata.elicitation_calls == 0
