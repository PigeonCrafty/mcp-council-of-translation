import asyncio
import json

import pytest

from council_of_translation.localization.models import ReviewTaskV2
from council_of_translation.localization.orchestration import (
    compact_review_response,
    continue_structured_review,
    run_structured_review,
)
from council_of_translation.localization.persistence import ReviewStore
from council_of_translation.localization.runtime import (
    ModelExecutionResult,
    RuntimeTelemetry,
    ScriptedModelExecutor,
    ScriptedUserInteractionGateway,
)


def run(coro):
    return asyncio.run(coro)


STRUCTURED_CLEAN = json.dumps({"role_feedback": "checked", "findings": []})


def _run_workflow(script, tmp_path):
    telemetry = RuntimeTelemetry(sample_budget=10)
    return run(
        run_structured_review(
            ReviewTaskV2(source_text="Save", candidate_translation="保存"),
            ScriptedModelExecutor(script, telemetry),
            ScriptedUserInteractionGateway(telemetry=telemetry),
            store=ReviewStore(tmp_path / "records", legacy_dir=tmp_path / "legacy"),
        )
    )


def test_all_structured_clean_reviewers_remain_completed_and_distinct_from_unavailable(tmp_path):
    record = _run_workflow([STRUCTURED_CLEAN] * 6, tmp_path)
    compact = compact_review_response(record)

    assert record.status == "COMPLETED"
    assert record.chief_editor_decision.publishability == "可发布"
    assert record.chief_editor_decision.review_needed == "否"
    assert record.issue_clusters == record.discussion_rounds == record.decision_points == []
    assert record.fallback_reason == ""
    assert record.runtime_metadata.reviewer_coverage == "full"
    assert record.runtime_metadata.reviewer_samples_successful == 6
    assert record.runtime_metadata.reviewer_samples_unavailable == 0
    assert record.runtime_metadata.sampling_calls == 6
    assert all(review["sample_status"] == "structured_success" for review in record.independent_reviews)
    assert compact["runtime_metadata"]["reviewer_coverage"] == "full"


@pytest.mark.parametrize(
    ("case", "script", "parse_failures"),
    [
        (
            "reasoning_only",
            [ModelExecutionResult(status="malformed", error="reasoning-only content")] * 6,
            0,
        ),
        ("empty", [""] * 6, 0),
        ("transport_error", [RuntimeError("transport unavailable") for _ in range(6)], 0),
        ("invalid_json", ["not JSON"] * 6, 6),
    ],
)
def test_all_unavailable_reviewer_scenarios_require_human_review(case, script, parse_failures, tmp_path):
    record = _run_workflow(script, tmp_path / case)
    compact = compact_review_response(record)

    assert record.status == compact["status"] == "NEEDS_HUMAN_REVIEW"
    assert record.chief_editor_decision.publishability == compact["chief_editor"]["publishability"] == "需人工复核"
    assert record.chief_editor_decision.review_needed == compact["chief_editor"]["review_needed"] == "是"
    assert record.chief_editor_decision.suggested_translation is None
    assert record.fallback_reason == compact["fallback_reason"] == "reviewer_coverage_none"
    assert record.runtime_metadata.reviewer_coverage == "none"
    assert record.runtime_metadata.reviewer_samples_successful == 0
    assert record.runtime_metadata.reviewer_samples_unavailable == 6
    assert record.runtime_metadata.sampling_calls == 6
    assert record.runtime_metadata.parse_failures == parse_failures
    assert "reviewer_coverage_none" in record.runtime_metadata.fallbacks
    assert all(review["sample_status"] == "unavailable" for review in record.independent_reviews)
    assert compact["runtime_metadata"] == record.runtime_metadata.model_dump(mode="json")
    assert "0/6" in record.chief_editor_decision.review_reason


def test_partial_reviewer_coverage_is_explicit_and_conservatively_requires_review(tmp_path):
    record = _run_workflow(
        [STRUCTURED_CLEAN, *[RuntimeError("transport unavailable") for _ in range(5)]],
        tmp_path,
    )
    compact = compact_review_response(record)

    assert record.status == "NEEDS_HUMAN_REVIEW"
    assert record.chief_editor_decision.publishability == "需人工复核"
    assert record.chief_editor_decision.review_needed == "是"
    assert record.fallback_reason == "reviewer_coverage_partial"
    assert record.runtime_metadata.reviewer_coverage == "partial"
    assert record.runtime_metadata.reviewer_samples_successful == 1
    assert record.runtime_metadata.reviewer_samples_unavailable == 5
    assert record.runtime_metadata.sampling_calls == 6
    assert [review["sample_status"] for review in record.independent_reviews].count("structured_success") == 1
    assert compact["fallback_reason"] == "reviewer_coverage_partial"
    assert compact["runtime_metadata"]["reviewer_coverage"] == "partial"
    assert "1/6" in compact["chief_editor"]["review_reason"]


def test_continuation_preserves_partial_parent_coverage_and_cannot_clear_human_review(tmp_path):
    finding = lambda action: {
        "source_span": "Continue",
        "candidate_span": "继续",
        "issue_type": "terminology",
        "problem": "wording choice",
        "evidence": "observable wording evidence",
        "action": action,
        "confidence": 0.8,
    }
    parent_script = [
        RuntimeError("transport unavailable"),
        STRUCTURED_CLEAN,
        json.dumps({"role_feedback": "checked", "findings": [finding("继续")]}),
        STRUCTURED_CLEAN,
        STRUCTURED_CLEAN,
        json.dumps({"role_feedback": "checked", "findings": [finding("下一步")]}),
        json.dumps({"turns": []}),
    ]
    parent_telemetry = RuntimeTelemetry(sample_budget=10)
    store = ReviewStore(tmp_path / "records", legacy_dir=tmp_path / "legacy")
    parent = run(
        run_structured_review(
            ReviewTaskV2(
                source_text="Continue",
                candidate_translation="继续",
                content_type="ui",
                decision_fallback="return_pending",
            ),
            ScriptedModelExecutor(parent_script, parent_telemetry),
            ScriptedUserInteractionGateway(supported=False, telemetry=parent_telemetry),
            store=store,
        )
    )
    point = parent.decision_points[0]
    selected = point.options[0].option_id
    reconsideration = json.dumps(
        {
            "positions": [
                {
                    "issue_id": point.issue_id,
                    "stance": "accept",
                    "option_id": selected,
                    "claim": "selected valid action",
                    "confidence": 0.8,
                }
            ]
        }
    )
    child = run(
        continue_structured_review(
            parent,
            [{"decision_id": point.decision_id, "selected_option_id": selected}],
            ScriptedModelExecutor([reconsideration, reconsideration], RuntimeTelemetry(sample_budget=10)),
            store=store,
        )
    )

    assert parent.status == "RETURNED_PENDING"
    assert parent.runtime_metadata.reviewer_coverage == "partial"
    assert child.status == "NEEDS_HUMAN_REVIEW"
    assert child.chief_editor_decision.publishability == "需人工复核"
    assert child.chief_editor_decision.review_needed == "是"
    assert child.fallback_reason == "reviewer_coverage_partial"
    assert child.runtime_metadata.reviewer_coverage == "partial"
    assert child.runtime_metadata.reviewer_samples_successful == 5
    assert child.runtime_metadata.reviewer_samples_unavailable == 1
    assert child.runtime_metadata.sampling_calls == 2
