import asyncio
import json

from council_of_translation.localization.clustering import cluster_findings
from council_of_translation.localization.deliberation import build_decision_points
from council_of_translation.localization.models import FindingV2, ReviewTaskV2
from council_of_translation.localization.orchestration import (
    compact_review_response,
    continue_structured_review,
    run_structured_review,
)
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


def _finding(agent, action):
    return {
        "agent_name": agent,
        "role_perspective": agent,
        "source_span": "Continue button",
        "candidate_span": "继续按钮",
        "issue_type": "terminology" if agent == "terminology_reviewer" else "fluency",
        "severity": "minor",
        "problem": "wording choice",
        "evidence": "both preserve meaning",
        "action": action,
        "confidence": 0.8,
    }


def _point():
    findings = [FindingV2.model_validate(_finding("terminology_reviewer", "继续")), FindingV2.model_validate(_finding("fluency_reviewer", "下一步"))]
    return build_decision_points(cluster_findings(findings))[0]


def _standard_script(with_reconsideration=True):
    reviews = [
        _review(),
        _review(),
        _review([_finding("terminology_reviewer", "继续")]),
        _review(),
        _review(),
        _review([_finding("fluency_reviewer", "下一步")]),
    ]
    discussion = json.dumps({"turns": []})
    if not with_reconsideration:
        return [*reviews, discussion]
    point = _point()
    selected = point.options[1].option_id
    reconsideration = json.dumps(
        {
            "positions": [
                {
                    "issue_id": point.issue_id,
                    "stance": "accept",
                    "option_id": selected,
                    "claim": "accept user-valid option",
                    "evidence": ["user preference"],
                    "confidence": 0.9,
                }
            ]
        }
    )
    return [*reviews, discussion, reconsideration, reconsideration]


def test_full_mocked_interactive_workflow_is_bounded_compact_and_persisted(tmp_path):
    point = _point()
    selected = point.options[1].option_id
    telemetry = RuntimeTelemetry(sample_budget=10)
    executor = ScriptedModelExecutor(_standard_script(), telemetry)
    gateway = ScriptedUserInteractionGateway(
        [ElicitationResult(action="accept", data={point.decision_id: selected})],
        telemetry=telemetry,
    )
    store = ReviewStore(tmp_path / "records", legacy_dir=tmp_path / "legacy")
    record = run(
        run_structured_review(
            ReviewTaskV2(source_text="Continue", candidate_translation="继续", content_type="ui"),
            executor,
            gateway,
            store=store,
        )
    )

    assert record.status == "COMPLETED"
    assert record.runtime_metadata.sampling_calls == 9
    assert record.runtime_metadata.elicitation_calls == 1
    assert record.runtime_metadata.sample_budget == 10
    assert len(record.discussion_rounds) == 1
    assert len(record.decision_points) == 1
    assert {item.role_id for item in record.reconsiderations} == {"terminology_reviewer", "fluency_reviewer"}
    assert record.chief_editor_decision.review_needed == "否"
    assert record.decision_trace.entries[0].outcome == "valid_user_choice"
    assert store.load(record.review_id).review_id == record.review_id

    compact = compact_review_response(record)
    assert compact["review_id"] == record.review_id
    assert "independent_reviews" not in compact
    assert "discussion_rounds" not in compact
    assert "reasoning" not in json.dumps(record.model_dump(mode="json"))


def test_unsupported_interaction_falls_back_explicitly_without_hanging(tmp_path):
    telemetry = RuntimeTelemetry(sample_budget=10)
    executor = ScriptedModelExecutor(_standard_script(with_reconsideration=False), telemetry)
    gateway = ScriptedUserInteractionGateway(supported=False, telemetry=telemetry)
    record = run(
        run_structured_review(
            ReviewTaskV2(source_text="Continue", candidate_translation="继续", content_type="ui"),
            executor,
            gateway,
            store=ReviewStore(tmp_path / "records", legacy_dir=tmp_path / "legacy"),
        )
    )
    assert record.status == "COMPLETED_WITH_FALLBACK"
    assert record.fallback_reason == "user_interaction_unsupported"
    assert record.runtime_metadata.sampling_calls == 7
    assert record.runtime_metadata.elicitation_calls == 0
    assert record.reconsiderations == []
    assert record.decision_trace.entries[0].outcome == "council_fallback"
    assert record.decision_trace.entries[0].selected_option_id in {
        option.option_id for option in record.decision_points[0].options
    }


def test_clean_translation_skips_conflict_discussion_and_interaction(tmp_path):
    telemetry = RuntimeTelemetry(sample_budget=10)
    executor = ScriptedModelExecutor([_review()] * 6, telemetry)
    gateway = ScriptedUserInteractionGateway(supported=True, telemetry=telemetry)
    record = run(
        run_structured_review(
            ReviewTaskV2(source_text="Save", candidate_translation="保存", content_type="ui"),
            executor,
            gateway,
            store=ReviewStore(tmp_path / "records", legacy_dir=tmp_path / "legacy"),
        )
    )
    assert record.status == "COMPLETED"
    assert record.issue_clusters == []
    assert record.discussion_rounds == []
    assert record.decision_points == []
    assert gateway.requests == []
    assert record.runtime_metadata.sampling_calls == 6
    assert record.runtime_metadata.elicitation_calls == 0


def test_return_pending_then_continue_creates_immutable_linked_revision(tmp_path):
    store = ReviewStore(tmp_path / "records", legacy_dir=tmp_path / "legacy")
    first_telemetry = RuntimeTelemetry(sample_budget=10)
    parent = run(
        run_structured_review(
            ReviewTaskV2(
                source_text="Continue",
                candidate_translation="继续",
                content_type="ui",
                decision_fallback="return_pending",
            ),
            ScriptedModelExecutor(_standard_script(with_reconsideration=False), first_telemetry),
            ScriptedUserInteractionGateway(supported=False, telemetry=first_telemetry),
            store=store,
        )
    )
    assert parent.status == "RETURNED_PENDING"
    assert parent.runtime_metadata.sampling_calls == 7
    assert parent.runtime_metadata.elicitation_calls == 0
    assert parent.runtime_metadata.sample_budget == 10
    assert compact_review_response(parent)["decision_points"] == [
        point.model_dump(mode="json") for point in parent.decision_points
    ]
    parent_path = store.path_for(parent.review_id)
    parent_bytes = parent_path.read_bytes()
    point = parent.decision_points[0]

    telemetry = RuntimeTelemetry(sample_budget=10)
    selected = point.options[0].option_id
    reconsideration = json.dumps(
        {"positions": [{"issue_id": point.issue_id, "stance": "accept", "option_id": selected, "claim": "accepted", "confidence": 0.8}]}
    )
    child = run(
        continue_structured_review(
            parent,
            [{"decision_id": point.decision_id, "selected_option_id": selected, "classification": "context_update", "context": "This is navigation."}],
            ScriptedModelExecutor([reconsideration, reconsideration], telemetry),
            store=store,
        )
    )
    assert child.parent_review_id == parent.review_id
    assert child.review_id != parent.review_id
    assert child.status == "COMPLETED"
    assert child.runtime_metadata.sampling_calls == 2
    assert child.runtime_metadata.elicitation_calls == 0
    assert child.runtime_metadata.sample_budget == 10
    assert {item.role_id for item in child.reconsiderations} == {"terminology_reviewer", "fluency_reviewer"}
    assert parent_path.read_bytes() == parent_bytes


def test_missing_placeholder_remains_blocked_without_decision_point(tmp_path):
    telemetry = RuntimeTelemetry(sample_budget=6)
    record = run(
        run_structured_review(
            ReviewTaskV2(source_text="Delete {count}", candidate_translation="删除", mode="lightweight"),
            ScriptedModelExecutor([_review()] * 4, telemetry),
            ScriptedUserInteractionGateway(supported=True, telemetry=telemetry),
            store=ReviewStore(tmp_path / "records", legacy_dir=tmp_path / "legacy"),
        )
    )
    assert record.preflight.blocking is True
    assert record.chief_editor_decision.must_fix
    assert record.decision_points == []
    assert record.status == "NEEDS_HUMAN_REVIEW"
