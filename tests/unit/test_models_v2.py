from datetime import datetime, timezone

import pytest
from pydantic import ValidationError

from council_of_translation.localization.compatibility import ReviewRecordV1, parse_review_record
from council_of_translation.localization.models import (
    DecisionOption,
    DecisionPoint,
    FindingV2,
    PreflightCheck,
    PreflightResult,
    ReviewRecordV2,
    ReviewTaskV2,
    RolePosition,
)


def test_sampled_finding_cannot_create_hard_constraint_or_blocker():
    finding = FindingV2.model_validate(
        {
            "finding_id": "f-1",
            "agent_name": "reviewer",
            "role_perspective": "test",
            "span": "{count}",
            "issue_type": "invented",
            "severity": "catastrophic",
            "constraint_tier": "hard",
            "blocking": True,
            "problem": "claim",
            "evidence_origin": "model",
        }
    )

    assert finding.source_span == "{count}"
    assert finding.candidate_span == "{count}"
    assert finding.issue_type == "other"
    assert finding.severity == "minor"
    assert finding.constraint_tier == "advisory"
    assert finding.blocking is False
    assert finding.finding_kind == "issue"
    assert finding.proposed_value == ""


def test_v21_finding_classification_and_proposal_are_conservative():
    affirmation = FindingV2.model_validate(
        {"finding_kind": "affirmation", "proposed_value": 42, "blocking": True, "constraint_tier": "hard"}
    )
    assert affirmation.finding_kind == "affirmation"
    assert affirmation.proposed_value == ""
    assert affirmation.blocking is False
    assert affirmation.constraint_tier == "advisory"


def test_v21_option_and_decision_fields_are_bounded_and_safe():
    option = DecisionOption(
        option_id="internal",
        outcome_value="下一步",
        label="界" * 60,
        description="d" * 200,
        support_role_ids=["ux", "ux", "fidelity"],
        support_rationale="r" * 300,
        policy_basis=["hard_constraint", "hard_constraint"],
        is_current_candidate=True,
    )
    assert option.outcome_value == "下一步"
    assert len(option.label) == 48
    assert len(option.description) == 160
    assert option.support_role_ids == ["ux", "fidelity"]
    assert len(option.support_rationale) == 240


def test_deterministic_preflight_can_create_blocker():
    result = PreflightResult(
        checks=[
            PreflightCheck(
                check_id="placeholder-1",
                kind="placeholder_parity",
                status="fail",
                severity="critical",
                blocking=True,
            )
        ]
    )
    assert result.blocking is True


def test_invalid_position_stance_is_conservative():
    position = RolePosition.model_validate({"role_id": "r", "stance": "veto", "blocking": True})
    assert position.stance == "not_applicable"
    assert position.blocking is False


def test_decision_point_drops_invalid_recommendation():
    point = DecisionPoint.model_validate(
        {
            "decision_id": "d-1",
            "issue_id": "i-1",
            "question": "Choose",
            "options": [{"option_id": "a", "label": "A", "valid": False}],
            "recommended_option_id": "a",
            "fallback_option_id": "a",
        }
    )
    assert point.recommended_option_id == ""
    assert point.fallback_option_id == ""


def test_missing_schema_version_is_v1():
    parsed = parse_review_record({"review_id": "20260810_145151", "task": {}})
    assert isinstance(parsed, ReviewRecordV1)
    assert parsed.schema_version == "1.0"


def test_minimal_v2_record_validates_and_caps_decisions():
    record = ReviewRecordV2(
        review_id="20260811T010203000004Z_ab12cd34",
        created_at=datetime.now(timezone.utc),
        task=ReviewTaskV2(source_text="Save", candidate_translation="保存"),
        decision_points=[
            DecisionPoint(decision_id=f"d-{i}", issue_id=f"i-{i}", question="q") for i in range(5)
        ],
    )
    assert record.schema_version == "2.2"
    assert len(record.decision_points) == 3


def test_v20_record_and_findings_remain_readable_without_gaining_choice_authority():
    parsed = parse_review_record(
        {
            "schema_version": "2.0",
            "review_id": "20260811T010203000004Z_ab12cd34",
            "task": {},
            "independent_reviews": [{"findings": [{"action": "Use Next", "blocking": True}]}],
        }
    )
    assert isinstance(parsed, ReviewRecordV2)
    assert parsed.schema_version == "2.0"
    migrated = FindingV2.model_validate(parsed.independent_reviews[0]["findings"][0])
    assert migrated.finding_kind == "issue"
    assert migrated.proposed_value == ""
    assert migrated.blocking is False


def test_malformed_or_unknown_record_does_not_parse_as_success():
    with pytest.raises(ValueError):
        parse_review_record([])
    with pytest.raises(ValueError):
        parse_review_record({"schema_version": "99", "review_id": "x"})
    with pytest.raises(ValidationError):
        parse_review_record({"schema_version": "2.0"})
