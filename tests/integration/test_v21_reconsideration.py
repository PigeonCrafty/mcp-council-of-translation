import asyncio
import json

from council_of_translation.localization.models import (
    FindingV2,
    IssueCluster,
    ReviewTaskV2,
    RolePosition,
    UserDecision,
    option_id_for_action,
)
from council_of_translation.localization.orchestration import _reconsider
from council_of_translation.localization.orchestration import (
    _form_mapping,
    run_structured_review,
)
from council_of_translation.localization.deliberation import SampleBudget
from council_of_translation.localization.persistence import ReviewStore
from council_of_translation.localization.runtime import (
    ElicitationResult,
    RuntimeTelemetry,
    ScriptedModelExecutor,
    ScriptedUserInteractionGateway,
)
from council_of_translation.localization.clustering import cluster_findings
from council_of_translation.localization.deliberation import build_decision_points


def run(coro):
    return asyncio.run(coro)


def _cluster() -> IssueCluster:
    issue_id = "issue_reconsider"
    selected = option_id_for_action(issue_id, "下一步")
    current = option_id_for_action(issue_id, "继续")
    return IssueCluster(
        issue_id=issue_id,
        topic="button outcome",
        category="language_choice",
        participant_role_ids=[
            "technical_safety_reviewer",
            "terminology_reviewer",
            "product_context_reviewer",
            "ux_copy_reviewer",
            "fluency_reviewer",
        ],
        candidate_actions=["继续", "下一步"],
        positions=[
            RolePosition(role_id="technical_safety_reviewer", stance="accept", option_id=current, confidence=0.9),
            RolePosition(role_id="terminology_reviewer", stance="accept", option_id=current, confidence=0.9),
            RolePosition(role_id="product_context_reviewer", stance="accept", option_id=current, confidence=0.9),
            RolePosition(role_id="ux_copy_reviewer", stance="accept", option_id=current, confidence=0.9),
            RolePosition(role_id="fluency_reviewer", stance="accept", option_id=selected, confidence=0.9),
        ],
        needs_user_input=True,
        consensus_status="disputed",
    )


def _decision(cluster: IssueCluster) -> UserDecision:
    return UserDecision(
        decision_id="decision_reconsider",
        selected_option_id=option_id_for_action(cluster.issue_id, "下一步"),
        selected_outcome_value="下一步",
        elicitation_action="accept",
    )


def _successful_response(cluster: IssueCluster) -> str:
    return json.dumps({
        "positions": [{
            "issue_id": cluster.issue_id,
            "stance": "accept",
            "option_id": option_id_for_action(cluster.issue_id, "下一步"),
            "claim": "accept selected outcome",
            "confidence": 0.8,
        }]
    })


def test_only_dissenters_are_requested_and_three_call_cap_is_explicit():
    cluster = _cluster()
    telemetry = RuntimeTelemetry(sample_budget=10)
    budget = SampleBudget("standard", used=7)
    results, provenance, warnings = run(_reconsider(
        ReviewTaskV2(),
        [cluster],
        [_decision(cluster)],
        ScriptedModelExecutor([_successful_response(cluster)] * 3, telemetry),
        telemetry,
        budget,
    ))
    assert "fluency_reviewer" not in provenance.requested_role_ids
    assert len(provenance.requested_role_ids) == 4
    assert len(provenance.completed_role_ids) == 3
    assert len(provenance.skipped_role_ids) == 1
    assert telemetry.sampling_calls == 3
    assert any(item.status == "skipped" for item in results)
    assert any("reconsideration_skipped_limit" in warning for warning in warnings)


def test_reconsideration_transport_failure_is_failed_not_completed():
    cluster = _cluster()
    cluster.participant_role_ids = ["terminology_reviewer", "fluency_reviewer"]
    cluster.positions = [
        position for position in cluster.positions
        if position.role_id in cluster.participant_role_ids
    ]
    telemetry = RuntimeTelemetry(sample_budget=10)
    results, provenance, warnings = run(_reconsider(
        ReviewTaskV2(),
        [cluster],
        [_decision(cluster)],
        ScriptedModelExecutor([RuntimeError("transport unavailable")], telemetry),
        telemetry,
        SampleBudget("standard", used=7),
    ))
    assert provenance.requested_role_ids == ["terminology_reviewer"]
    assert provenance.completed_role_ids == []
    assert provenance.failed_role_ids == ["terminology_reviewer"]
    assert results[0].status == "failed"
    assert warnings == ["reconsideration_failed:terminology_reviewer"]


def test_forced_lightweight_budget_shortfall_returns_truthful_degradation(tmp_path):
    roles = [
        "technical_safety_reviewer",
        "fidelity_reviewer",
        "terminology_reviewer",
        "fluency_reviewer",
    ]
    findings = [
        FindingV2(
            agent_name=role,
            source_span="Continue",
            candidate_span="继续",
            issue_type="ux",
            severity="minor",
            finding_kind="choice",
            proposed_value="下一步" if role == "fluency_reviewer" else "继续",
            problem="wording choice",
            evidence="UI context",
            confidence=0.8,
        )
        for role in roles
    ]
    point = build_decision_points(
        cluster_findings(findings)
    )[0]
    selected_value = next(
        value for value, option in _form_mapping(point).items()
        if option is not None and option.outcome_value == "下一步"
    )
    reviews = [
        json.dumps({"role_feedback": "checked", "findings": [finding.model_dump(mode="json")]})
        for finding in findings
    ]
    reconsideration_cluster = cluster_findings(findings)[0]
    reconsideration = _successful_response(reconsideration_cluster)
    telemetry = RuntimeTelemetry(sample_budget=6)
    record = run(run_structured_review(
        ReviewTaskV2(
            source_text="Continue",
            candidate_translation="继续",
            content_type="ui",
            mode="lightweight",
            briefing_mode="off",
        ),
        ScriptedModelExecutor([*reviews, RuntimeError("reconsideration transport"), reconsideration], telemetry),
        ScriptedUserInteractionGateway([
            ElicitationResult(action="accept", data={"review_choice_1": selected_value})
        ], telemetry=telemetry),
        store=ReviewStore(tmp_path / "records", legacy_dir=tmp_path / "legacy"),
    ))
    assert record.runtime_metadata.sampling_calls == 6
    assert record.degraded is True
    assert record.status == "NEEDS_HUMAN_REVIEW"
    assert record.decision_support.level == "insufficient"
    assert record.decision_support.outcome_coherent is True
    assert len(record.reconsideration_provenance.requested_role_ids) == 3
    assert len(record.reconsideration_provenance.completed_role_ids) == 1
    assert len(record.reconsideration_provenance.skipped_role_ids) == 1
    assert len(record.reconsideration_provenance.failed_role_ids) == 1
    assert "reconsideration_degraded" in record.fallback_reason
    assert record.warnings
