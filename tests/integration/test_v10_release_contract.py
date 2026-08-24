import asyncio
import json

from council_of_translation import __diagnostic_build__, __schema_version__, __version__
from council_of_translation.localization.compatibility import parse_review_record
from council_of_translation.localization.models import (
    CouncilValueMetrics,
    ReviewRecordV2,
    ReviewTaskV2,
    RoleContribution,
)
from council_of_translation.localization.persistence import ReviewStore, build_review_id
from council_of_translation.server import mcp
from council_of_translation.tools.review import _server_info


def test_v011_identifiers_surface_and_frozen_runtime_limits(monkeypatch):
    monkeypatch.delenv("COUNCIL_REVIEW_CONCURRENCY", raising=False)
    assert (__version__, __diagnostic_build__, __schema_version__) == (
        "0.11.1", "risk-coherent-council-v9.1", "2.5"
    )
    info = _server_info()
    assert info["package_version"] == info["module_version"] == "0.11.1"
    assert info["diagnostic_build"] == "risk-coherent-council-v9.1"
    assert info["schema_version"] == "2.5"
    assert info["sample_budgets"] == {"lightweight": 6, "standard": 13, "strict": 18}
    assert info["independent_review_concurrency_limit"] == 3
    assert info["max_independent_review_concurrency"] == 3
    assert list(asyncio.run(mcp.get_tools())) == [
        "review_translation", "continue_review", "view_review_record",
        "list_review_records", "get_server_info",
    ]


def test_v25_full_and_metadata_writes_are_truthful_and_old_records_still_read(tmp_path):
    metrics = CouncilValueMetrics(
        role_contributions=[
            RoleContribution(role_id="fidelity_reviewer", contribution_kind="unique_material", unique_issue_count=1),
            RoleContribution(role_id="PRIVATE_ROLE_SENTINEL", contribution_kind="corroborating", corroborated_issue_count=1),
        ],
        unique_material_issue_count=1,
    )
    for mode in ("full", "metadata"):
        store = ReviewStore(tmp_path / mode, include_legacy=False)
        record = ReviewRecordV2(
            review_id=build_review_id(),
            task=ReviewTaskV2(source_text="PRIVATE", candidate_translation="保密", history_mode=mode),
            council_value_metrics=metrics,
        )
        path = store.save(record)
        payload = json.loads(path.read_text(encoding="utf-8"))
        assert payload["schema_version"] == "2.5"
        assert payload["version_metadata"] == {
            "package_version": "0.11.1",
            "diagnostic_build": "risk-coherent-council-v9.1",
            "record_schema": "2.5",
        }
        assert payload["council_value_metrics"]["unique_material_issue_count"] == 1
        if mode == "metadata":
            assert "PRIVATE" not in path.read_text(encoding="utf-8")
            assert payload["council_value_metrics"]["role_contributions"] == [{
                "role_id": "fidelity_reviewer",
                "contribution_kind": "unique_material",
                "unique_issue_count": 1,
                "corroborated_issue_count": 0,
                "material_finding_count": 0,
            }]

    for version in ("2.0", "2.1", "2.2", "2.3", "2.4"):
        historical = parse_review_record({
            "schema_version": version,
            "review_id": "20260811T010203000004Z_ab12cd34",
            "task": {},
        })
        assert historical.schema_version == version
        assert historical.council_value_metrics == CouncilValueMetrics()
