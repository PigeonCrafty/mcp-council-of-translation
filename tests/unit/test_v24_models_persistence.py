import json

from council_of_translation.localization.compatibility import parse_review_record
from council_of_translation.localization.models import (
    CouncilValueMetrics,
    ReviewRecordV2,
    ReviewTaskV2,
    RoleContribution,
)
from council_of_translation.localization.persistence import ReviewStore, build_review_id


def test_v24_value_metrics_are_bounded_and_role_ids_are_unique():
    metrics = CouncilValueMetrics(
        role_contributions=[
            RoleContribution(role_id="fidelity_reviewer", contribution_kind="unique_material"),
            RoleContribution(role_id="fidelity_reviewer", contribution_kind="corroborating"),
        ],
        unique_material_issue_count=1,
        discussion_marginal_value="material",
    )

    assert [item.role_id for item in metrics.role_contributions] == ["fidelity_reviewer"]
    assert metrics.metric_basis == "structured_findings_and_trace"


def test_v20_through_v23_read_with_conservative_value_defaults():
    for schema_version in ("2.0", "2.1", "2.2", "2.3"):
        record = parse_review_record(
            {
                "schema_version": schema_version,
                "review_id": "20260811T010203000004Z_ab12cd34",
                "task": {},
            }
        )
        assert isinstance(record, ReviewRecordV2)
        assert record.council_value_metrics == CouncilValueMetrics()


def test_v24_record_reads_explicit_value_metrics():
    record = parse_review_record(
        {
            "schema_version": "2.4",
            "review_id": "20260811T010203000004Z_ab12cd34",
            "task": {},
            "council_value_metrics": {
                "role_contributions": [
                    {
                        "role_id": "terminology_reviewer",
                        "contribution_kind": "corroborating",
                        "corroborated_issue_count": 2,
                        "material_finding_count": 2,
                    }
                ],
                "corroborated_issue_count": 2,
                "discussion_marginal_value": "none",
            },
        }
    )

    assert record.council_value_metrics.corroborated_issue_count == 2
    assert record.council_value_metrics.role_contributions[0].contribution_kind == "corroborating"


def test_metadata_projection_preserves_only_content_free_value_metrics(tmp_path):
    store = ReviewStore(tmp_path / "reviews", legacy_dir=tmp_path / "legacy")
    record = ReviewRecordV2(
        review_id=build_review_id(),
        task=ReviewTaskV2(
            source_text="SECRET SOURCE",
            candidate_translation="SECRET CANDIDATE",
            history_mode="metadata",
        ),
        council_value_metrics=CouncilValueMetrics(
            role_contributions=[
                RoleContribution(
                    role_id="fidelity_reviewer",
                    contribution_kind="unique_material",
                    unique_issue_count=1,
                    material_finding_count=1,
                )
            ],
            unique_material_issue_count=1,
        ),
    )

    path = store.save(record, history_mode="metadata")
    payload = json.loads(path.read_text(encoding="utf-8"))

    assert "SECRET" not in path.read_text(encoding="utf-8")
    assert payload["council_value_metrics"]["unique_material_issue_count"] == 1
    assert store.load(record.review_id).council_value_metrics.role_contributions[0].role_id == "fidelity_reviewer"
