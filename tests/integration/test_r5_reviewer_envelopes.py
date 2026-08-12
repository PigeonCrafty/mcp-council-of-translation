import asyncio
import json

import pytest

from council_of_translation.localization.models import ReviewTaskV2
from council_of_translation.localization.orchestration import compact_review_response, run_structured_review
from council_of_translation.localization.persistence import ReviewStore
from council_of_translation.localization.runtime import (
    RuntimeTelemetry,
    ScriptedModelExecutor,
    ScriptedUserInteractionGateway,
)


def run(coro):
    return asyncio.run(coro)


VALID_CLEAN = {"role_feedback": "checked", "findings": []}


def _workflow(payloads, tmp_path):
    telemetry = RuntimeTelemetry(sample_budget=10)
    record = run(
        run_structured_review(
            ReviewTaskV2(source_text="Save", candidate_translation="保存"),
            ScriptedModelExecutor([json.dumps(payload) for payload in payloads], telemetry),
            ScriptedUserInteractionGateway(telemetry=telemetry),
            store=ReviewStore(tmp_path / "records", legacy_dir=tmp_path / "legacy"),
        )
    )
    return record, compact_review_response(record)


def _assert_all_unavailable(record, compact, expected_error):
    assert record.status == compact["status"] == "NEEDS_HUMAN_REVIEW"
    assert record.chief_editor_decision.publishability == "需人工复核"
    assert record.chief_editor_decision.review_needed == "是"
    assert record.fallback_reason == compact["fallback_reason"] == "reviewer_coverage_none"
    assert record.runtime_metadata.reviewer_coverage == "none"
    assert record.runtime_metadata.reviewer_samples_successful == 0
    assert record.runtime_metadata.reviewer_samples_unavailable == 6
    assert record.runtime_metadata.sampling_calls == 6
    assert record.runtime_metadata.parse_failures == 6
    assert record.runtime_metadata.fallbacks.count(f"reviewer_{expected_error}") == 6
    assert record.runtime_metadata.fallbacks[-1] == "reviewer_coverage_none"
    assert compact["runtime_metadata"] == record.runtime_metadata.model_dump(mode="json")
    assert all(review["sample_status"] == "unavailable" for review in record.independent_reviews)
    assert all(review["sample_error"] == expected_error for review in record.independent_reviews)
    assert all(review["findings"] == [] for review in record.independent_reviews)


@pytest.mark.parametrize(
    ("case", "payload", "expected_error"),
    [
        ("empty_object", {}, "invalid_role_feedback"),
        ("wrong_feedback_type", {"role_feedback": 7, "findings": []}, "invalid_role_feedback"),
        ("missing_findings", {"role_feedback": "checked"}, "invalid_findings_container"),
        ("null_findings", {"role_feedback": "checked", "findings": None}, "invalid_findings_container"),
        ("string_findings", {"role_feedback": "checked", "findings": "none"}, "invalid_findings_container"),
        ("object_findings", {"role_feedback": "checked", "findings": {}}, "invalid_findings_container"),
        ("scalar_entry", {"role_feedback": "checked", "findings": [7]}, "invalid_finding_entry"),
        ("null_entry", {"role_feedback": "checked", "findings": [None]}, "invalid_finding_entry"),
        ("list_entry", {"role_feedback": "checked", "findings": [[]]}, "invalid_finding_entry"),
        ("inert_entry", {"role_feedback": "checked", "findings": [{}]}, "inert_finding"),
        (
            "bad_confidence",
            {"role_feedback": "checked", "findings": [{"problem": "bad", "action": "fix", "confidence": "abc"}]},
            "invalid_finding_value",
        ),
        (
            "scalar_rule_refs",
            {"role_feedback": "checked", "findings": [{"problem": "bad", "action": "fix", "rule_refs": 7}]},
            "invalid_finding_value",
        ),
        ("blank_clean", {"role_feedback": "  ", "findings": []}, "empty_reviewer_response"),
        (
            "too_many_findings",
            {
                "role_feedback": "checked",
                "findings": [{"problem": "issue", "action": "fix"} for _ in range(6)],
            },
            "too_many_findings",
        ),
    ],
)
def test_semantically_malformed_envelopes_are_unavailable_without_exceptions(
    case, payload, expected_error, tmp_path
):
    record, compact = _workflow([payload] * 6, tmp_path / case)
    _assert_all_unavailable(record, compact, expected_error)


def test_valid_findings_before_invalid_entry_are_discarded_with_unavailable_sample(tmp_path):
    valid_finding = {
        "source_span": "Save",
        "candidate_span": "保存",
        "issue_type": "terminology",
        "problem": "wording issue",
        "evidence": "observed wording",
        "action": "use 保存",
        "confidence": 0.8,
    }
    payload = {"role_feedback": "checked", "findings": [valid_finding, None]}
    record, compact = _workflow([payload] * 6, tmp_path)

    _assert_all_unavailable(record, compact, "invalid_finding_entry")
    assert record.issue_clusters == []


def test_one_malformed_envelope_among_valid_clean_reviewers_is_partial(tmp_path):
    record, compact = _workflow([{}, *[VALID_CLEAN for _ in range(5)]], tmp_path)

    assert record.status == "NEEDS_HUMAN_REVIEW"
    assert record.chief_editor_decision.publishability == "需人工复核"
    assert record.chief_editor_decision.review_needed == "是"
    assert record.fallback_reason == compact["fallback_reason"] == "reviewer_coverage_partial"
    assert record.runtime_metadata.reviewer_coverage == "partial"
    assert record.runtime_metadata.reviewer_samples_successful == 5
    assert record.runtime_metadata.reviewer_samples_unavailable == 1
    assert record.runtime_metadata.sampling_calls == 6
    assert record.runtime_metadata.parse_failures == 1
    assert "reviewer_invalid_role_feedback" in record.runtime_metadata.fallbacks
    assert record.runtime_metadata.fallbacks[-1] == "reviewer_coverage_partial"


def test_valid_structured_zero_findings_remain_full_clean_coverage(tmp_path):
    record, compact = _workflow([VALID_CLEAN] * 6, tmp_path)

    assert record.status == "COMPLETED"
    assert record.chief_editor_decision.publishability == "可发布"
    assert record.chief_editor_decision.review_needed == "否"
    assert record.fallback_reason == ""
    assert record.runtime_metadata.reviewer_coverage == "full"
    assert record.runtime_metadata.reviewer_samples_successful == 6
    assert record.runtime_metadata.reviewer_samples_unavailable == 0
    assert record.runtime_metadata.sampling_calls == 6
    assert record.runtime_metadata.parse_failures == 0
    assert record.runtime_metadata.fallbacks == []
    assert record.issue_clusters == record.discussion_rounds == record.decision_points == []
    assert all(review["sample_error"] == "" for review in record.independent_reviews)
    assert compact["runtime_metadata"]["reviewer_coverage"] == "full"


def test_empty_feedback_is_valid_when_a_valid_advisory_finding_remains(tmp_path):
    payload = {
        "role_feedback": "",
        "findings": [
            {
                "source_span": "Save",
                "candidate_span": "保存",
                "issue_type": "terminology",
                "problem": "wording issue",
                "evidence": "observed wording",
                "action": "use 保存",
                "blocking": True,
                "constraint_tier": "hard",
                "confidence": 0.8,
            }
        ],
    }
    record, _ = _workflow([payload] * 6, tmp_path)

    assert record.runtime_metadata.reviewer_coverage == "full"
    assert record.runtime_metadata.reviewer_samples_successful == 6
    assert record.runtime_metadata.parse_failures == 0
    assert record.issue_clusters
    assert all(
        position.evidence_origin == "model"
        and position.constraint_tier == "advisory"
        and position.blocking is False
        for cluster in record.issue_clusters
        for position in cluster.positions
    )
