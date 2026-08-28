import json
from datetime import datetime, timedelta, timezone

import pytest

from council_of_translation.localization.compatibility import ReviewRecordV1
from council_of_translation.localization.models import (
    ChiefEditorDecisionV2,
    CouncilPlan,
    ReviewRecordV2,
    ReviewTaskV2,
    RuntimeMetadata,
    UserDecision,
)
from council_of_translation.localization.persistence import (
    InvalidReviewIdError,
    MalformedReviewRecordError,
    ReviewRecordNotFoundError,
    ReviewPersistenceError,
    ReviewStore,
    build_review_id,
    default_reviews_dir,
)
from council_of_translation.localization.roles import build_council_plan
from council_of_translation.localization.verification import (
    build_verification_receipt,
    render_verification_report,
)


def _record(review_id: str, *, history_mode: str = "full") -> ReviewRecordV2:
    return ReviewRecordV2(
        review_id=review_id,
        task=ReviewTaskV2(
            source_text="SECRET SOURCE",
            candidate_translation="SECRET CANDIDATE",
            context="SECRET CONTEXT",
            audience="SECRET AUDIENCE",
            term_glossary="SECRET TB",
            style_guide="SECRET SG",
            project_rules="SECRET RULE",
            technical_constraints="SECRET CONSTRAINT",
            reference_translations="SECRET REFERENCE",
            known_exceptions="SECRET EXCEPTION",
            notes="SECRET NOTES",
            source_language="SECRET SOURCE LANGUAGE",
            target_language="SECRET TARGET LANGUAGE",
            content_type="SECRET CONTENT TYPE",
            history_mode=history_mode,
        ),
        runtime_metadata=RuntimeMetadata(
            fallbacks=["SECRET RUNTIME TEXT"],
            wall_clock_ms=321,
            sampling_wait_ms=654,
            independent_review_concurrency_limit=3,
            independent_review_peak_concurrency=2,
            independent_review_batch_count=3,
            independent_review_concurrency_disposition="configured",
        ),
        council_plan=CouncilPlan(
            content_type="SECRET PLAN CONTENT TYPE",
            active_role_ids=["SECRET ROLE TEXT"],
        ),
        independent_reviews=[{"model_text": "SECRET MODEL TEXT"}],
        user_decisions=[
            UserDecision(decision_id="d1", context="SECRET USER TEXT", elicitation_action="accept")
        ],
        chief_editor_decision=ChiefEditorDecisionV2(
            must_fix=["SECRET CHIEF TEXT"], decision_rationale="SECRET RATIONALE"
        ),
        policy_gate_result={"reason": "SECRET POLICY TEXT"},
        fallback_reason="SECRET FALLBACK TEXT",
        version_metadata={"package_version": "SECRET VERSION TEXT"},
    )


def test_ids_are_collision_resistant_and_lexically_sortable():
    instant = datetime(2026, 8, 11, 1, 2, 3, 4, tzinfo=timezone.utc)
    ids = {build_review_id(now=instant) for _ in range(2_000)}
    assert len(ids) == 2_000

    earlier = build_review_id(now=instant, suffix_factory=lambda: "ffffffffffff")
    later = build_review_id(now=instant + timedelta(microseconds=1), suffix_factory=lambda: "000000000000")
    assert earlier < later


def test_default_directory_honors_configuration(monkeypatch, tmp_path):
    configured = tmp_path / "configured"
    monkeypatch.setenv("COUNCIL_REVIEWS_DIR", str(configured))
    assert default_reviews_dir() == configured


def test_full_write_is_atomic_and_round_trips(monkeypatch, tmp_path):
    store = ReviewStore(tmp_path / "new", legacy_dir=tmp_path / "legacy")
    record = _record(build_review_id())
    observed = {}

    from council_of_translation.localization import persistence

    real_replace = persistence.os.replace

    def observing_replace(source, destination):
        observed["temporary_exists"] = source.exists()
        observed["destination_absent"] = not destination.exists()
        real_replace(source, destination)

    monkeypatch.setattr(persistence.os, "replace", observing_replace)
    path = store.save(record)

    assert path is not None
    assert observed == {"temporary_exists": True, "destination_absent": True}
    assert list(path.parent.glob("*.tmp")) == []
    loaded = store.load(record.review_id)
    assert isinstance(loaded, ReviewRecordV2)
    assert loaded.task.source_text == "SECRET SOURCE"
    assert loaded.schema_version == "2.6"
    assert loaded.runtime_metadata.wall_clock_ms == 321
    assert loaded.runtime_metadata.sampling_wait_ms == 654
    assert loaded.runtime_metadata.independent_review_peak_concurrency == 2


def test_metadata_write_uses_allowlist_and_remains_readable(tmp_path):
    store = ReviewStore(tmp_path / "new", legacy_dir=tmp_path / "legacy")
    record = _record(build_review_id())
    path = store.save(record, history_mode="metadata")
    assert path is not None

    serialized = path.read_text(encoding="utf-8")
    for secret in (
        "SECRET SOURCE",
        "SECRET CANDIDATE",
        "SECRET CONTEXT",
        "SECRET AUDIENCE",
        "SECRET TB",
        "SECRET SG",
        "SECRET RULE",
        "SECRET CONSTRAINT",
        "SECRET REFERENCE",
        "SECRET EXCEPTION",
        "SECRET NOTES",
        "SECRET MODEL TEXT",
        "SECRET USER TEXT",
        "SECRET CHIEF TEXT",
        "SECRET RATIONALE",
        "SECRET POLICY TEXT",
        "SECRET FALLBACK TEXT",
        "SECRET SOURCE LANGUAGE",
        "SECRET TARGET LANGUAGE",
        "SECRET CONTENT TYPE",
        "SECRET RUNTIME TEXT",
        "SECRET PLAN CONTENT TYPE",
        "SECRET ROLE TEXT",
        "SECRET VERSION TEXT",
    ):
        assert secret not in serialized

    loaded = store.load(record.review_id)
    assert isinstance(loaded, ReviewRecordV2)
    assert loaded.task.history_mode == "metadata"
    assert loaded.task.source_text == ""
    assert loaded.independent_reviews == []
    assert loaded.user_decisions == []
    assert loaded.schema_version == "2.6"
    assert loaded.runtime_metadata.wall_clock_ms == 321
    assert loaded.runtime_metadata.sampling_wait_ms == 654
    assert loaded.runtime_metadata.independent_review_concurrency_limit == 3
    assert loaded.runtime_metadata.independent_review_peak_concurrency == 2
    assert loaded.runtime_metadata.independent_review_batch_count == 3
    assert loaded.runtime_metadata.independent_review_concurrency_disposition == "configured"


@pytest.mark.parametrize("history_mode", ["full", "metadata"])
def test_v25_routing_provenance_round_trips_in_safe_structured_history(tmp_path, history_mode):
    store = ReviewStore(tmp_path / history_mode, include_legacy=False)
    record = _record(build_review_id(), history_mode=history_mode)
    record.council_plan = build_council_plan("standard", "legal_risk")

    path = store.save(record, history_mode=history_mode)
    payload = json.loads(path.read_text(encoding="utf-8"))
    assert payload["schema_version"] == "2.6"
    assert payload["council_plan"]["routing_profile"] == "route_legal_risk_standard_v1"
    assert payload["council_plan"]["routing_reason_codes"] == [
        "content_legal_risk",
        "mode_standard",
        "deterministic_preflight_coverage",
        "risk_panorama",
    ]
    loaded = store.load(record.review_id)
    assert loaded.council_plan.routing_profile == record.council_plan.routing_profile
    assert loaded.council_plan.routing_reason_codes == record.council_plan.routing_reason_codes
    if history_mode == "full":
        assert loaded.council_plan == record.council_plan
    else:
        assert loaded.council_plan.active_role_ids == []


@pytest.mark.parametrize("history_mode", ["full", "metadata"])
def test_new_write_persists_truthful_v0132_runtime_and_version_identifiers(tmp_path, history_mode):
    store = ReviewStore(tmp_path / "new", legacy_dir=tmp_path / "legacy")
    record = ReviewRecordV2(
        review_id=build_review_id(),
        task=ReviewTaskV2(source_text="Save", candidate_translation="保存", history_mode=history_mode),
    )
    path = store.save(record, history_mode=history_mode)

    payload = json.loads(path.read_text(encoding="utf-8"))
    expected = {
        "package_version": "0.13.2",
        "diagnostic_build": "truthful-boundaries-council-v11.2",
    }
    assert {key: payload["runtime_metadata"][key] for key in expected} == expected
    assert {key: payload["version_metadata"][key] for key in expected} == expected
    assert payload["version_metadata"]["record_schema"] == "2.6"

    loaded = store.load(record.review_id)
    assert loaded.runtime_metadata.package_version == "0.13.2"
    assert loaded.runtime_metadata.diagnostic_build == "truthful-boundaries-council-v11.2"
    assert loaded.version_metadata == {**expected, "record_schema": "2.6"}


def test_v21_metadata_redacts_compact_and_reconsideration_text(tmp_path):
    store = ReviewStore(tmp_path / "new", legacy_dir=tmp_path / "legacy")
    record = _record(build_review_id(), history_mode="metadata")
    record.degraded = True
    record.warnings = ["SECRET WARNING"]
    record.effective_task.audience = "SECRET EFFECTIVE AUDIENCE"
    record.effective_task.material_rule_context = ["SECRET DERIVED RULE"]
    record.deliberation_summary.final_outcome = "SECRET FINAL OUTCOME"
    record.reconsideration_provenance.requested_role_ids = ["SECRET ROLE ID"]
    path = store.save(record, history_mode="metadata")

    serialized = path.read_text(encoding="utf-8")
    assert "SECRET" not in serialized
    loaded = store.load(record.review_id)
    assert loaded.degraded is True
    assert loaded.warnings == []
    assert loaded.reconsideration_provenance.requested_role_ids == []


def test_v21_metadata_preserves_only_safe_reconsideration_role_provenance(tmp_path):
    store = ReviewStore(tmp_path / "new", legacy_dir=tmp_path / "legacy")
    record = _record(build_review_id(), history_mode="metadata")
    record.reconsideration_provenance.requested_role_ids = [
        "ux_copy_reviewer", "PRIVATE_USER_ROLE"
    ]
    record.reconsideration_provenance.completed_role_ids = ["ux_copy_reviewer"]
    path = store.save(record, history_mode="metadata")

    serialized = path.read_text(encoding="utf-8")
    assert "PRIVATE_USER_ROLE" not in serialized
    loaded = store.load(record.review_id)
    assert loaded.reconsideration_provenance.requested_role_ids == ["ux_copy_reviewer"]
    assert loaded.reconsideration_provenance.completed_role_ids == ["ux_copy_reviewer"]


def test_metadata_round_trip_preserves_safe_disposition_and_redacts_chief_prose(tmp_path):
    store = ReviewStore(tmp_path / "new", legacy_dir=tmp_path / "legacy")
    record = _record(build_review_id(), history_mode="metadata")
    record.status = "COMPLETED"
    record.chief_editor_decision = ChiefEditorDecisionV2(
        publishability="可发布",
        review_needed="否",
        decision_rationale="SECRET CHIEF RATIONALE",
        conflict_resolutions=["SECRET CHIEF PROSE"],
    )
    path = store.save(record, history_mode="metadata")

    serialized = path.read_text(encoding="utf-8")
    assert "SECRET" not in serialized
    loaded = store.load(record.review_id)
    assert loaded.status == "NEEDS_HUMAN_REVIEW"
    assert loaded.chief_editor_decision.publishability == "需人工复核"
    assert loaded.chief_editor_decision.review_needed == "是"
    assert loaded.chief_editor_decision.decision_rationale == ""
    listed = list(store.iter_records())
    assert [(item.status, item.chief_editor_decision.publishability, item.chief_editor_decision.review_needed) for item in listed] == [
        ("NEEDS_HUMAN_REVIEW", "需人工复核", "是")
    ]


def test_atomic_write_failure_is_normalized_without_host_path(monkeypatch, tmp_path):
    from council_of_translation.localization import persistence

    raw_path = str(tmp_path / "PRIVATE" / "record.json")

    def fail_replace(source, destination):
        raise OSError(f"cannot replace {raw_path}")

    monkeypatch.setattr(persistence.os, "replace", fail_replace)
    store = ReviewStore(tmp_path / "new", legacy_dir=tmp_path / "legacy")
    with pytest.raises(ReviewPersistenceError, match="review record write failed") as caught:
        store.save(_record(build_review_id()))
    assert raw_path not in str(caught.value)
    assert list((tmp_path / "new").glob("*.tmp")) == []


def test_off_mode_creates_no_directory_or_file(tmp_path):
    destination = tmp_path / "must-not-exist"
    store = ReviewStore(destination, legacy_dir=tmp_path / "legacy")
    result = store.save(_record(build_review_id()), history_mode="off")
    assert result is None
    assert not destination.exists()


def test_new_storage_wins_and_legacy_v1_is_fallback(tmp_path):
    new_dir = tmp_path / "new"
    legacy_dir = tmp_path / "legacy"
    new_dir.mkdir()
    legacy_dir.mkdir()
    legacy_id = "20260810_145151"
    legacy_payload = {"review_id": legacy_id, "task": {"marker": "legacy"}}
    (legacy_dir / f"{legacy_id}.json").write_text(json.dumps(legacy_payload), encoding="utf-8")
    store = ReviewStore(new_dir, legacy_dir=legacy_dir)

    loaded = store.load(legacy_id)
    assert isinstance(loaded, ReviewRecordV1)
    assert loaded.task["marker"] == "legacy"

    (new_dir / f"{legacy_id}.json").write_text(
        json.dumps({"review_id": legacy_id, "task": {"marker": "new"}}), encoding="utf-8"
    )
    assert store.load(legacy_id).task["marker"] == "new"


def test_malformed_records_raise_explicit_errors_without_legacy_fallback(tmp_path):
    new_dir = tmp_path / "new"
    legacy_dir = tmp_path / "legacy"
    new_dir.mkdir()
    legacy_dir.mkdir()
    review_id = "20260810_145151"
    (new_dir / f"{review_id}.json").write_text("not-json", encoding="utf-8")
    (legacy_dir / f"{review_id}.json").write_text(
        json.dumps({"review_id": review_id, "task": {"marker": "legacy"}}), encoding="utf-8"
    )

    with pytest.raises(MalformedReviewRecordError, match="malformed"):
        ReviewStore(new_dir, legacy_dir=legacy_dir).load(review_id)


def test_mismatched_id_invalid_id_and_missing_record_are_errors(tmp_path):
    store = ReviewStore(tmp_path / "new", legacy_dir=tmp_path / "legacy")
    review_id = build_review_id()
    store.storage_dir.mkdir()
    (store.storage_dir / f"{review_id}.json").write_text(
        json.dumps({"review_id": build_review_id(), "task": {}}), encoding="utf-8"
    )
    with pytest.raises(MalformedReviewRecordError, match="mismatched"):
        store.load(review_id)
    with pytest.raises(InvalidReviewIdError):
        store.load("../../reviews/secret")
    with pytest.raises(ReviewRecordNotFoundError):
        store.load("20260810_145152")


def test_v2_save_rejects_legacy_id(tmp_path):
    store = ReviewStore(tmp_path / "new", legacy_dir=tmp_path / "legacy")
    with pytest.raises(InvalidReviewIdError):
        store.save(_record("20260810_145151"))


def test_reader_accepts_frozen_eight_character_v2_suffix(tmp_path):
    store = ReviewStore(tmp_path / "new", legacy_dir=tmp_path / "legacy")
    review_id = "20260811T010203000004Z_ab12cd34"
    path = store.save(_record(review_id))
    assert path is not None
    assert store.load(review_id).review_id == review_id


def test_saving_readable_v20_model_writes_new_v26_schema(tmp_path):
    store = ReviewStore(tmp_path / "new", legacy_dir=tmp_path / "legacy")
    record = _record(build_review_id()).model_copy(update={"schema_version": "2.0"})
    path = store.save(record)

    payload = json.loads(path.read_text(encoding="utf-8"))
    assert payload["schema_version"] == "2.6"
    assert payload["version_metadata"]["record_schema"] == "2.6"
    assert store.load(record.review_id).schema_version == "2.6"


def test_metadata_receipt_uses_only_physically_retained_allowlist_fields(tmp_path):
    store = ReviewStore(tmp_path / "new", legacy_dir=tmp_path / "legacy")
    record = _record(build_review_id(), history_mode="metadata")
    record.council_plan = build_council_plan("standard", "legal_risk")
    record.status = "COMPLETED"
    record.degraded = True
    record.warnings = ["SECRET WARNING"]
    record.fallback_reason = "SECRET FALLBACK"
    record.chief_editor_decision = ChiefEditorDecisionV2(
        publishability="修改后可发布",
        review_needed="是",
        suggested_translation="SECRET TRANSLATION",
    )
    path = store.save(record, history_mode="metadata")
    loaded = store.load(record.review_id)

    receipt = build_verification_receipt(loaded)
    report = render_verification_report(receipt)
    unavailable = set(receipt["availability"]["not_recorded_fields"])

    assert receipt["record"]["history_mode"] == "metadata"
    assert receipt["routing"]["profile"] == "route_legal_risk_standard_v1"
    assert receipt["routing"]["active_role_ids"] is None
    assert receipt["reviewer_execution"]["samples"] is None
    assert receipt["preflight"] == {
        "blocking": None,
        "failed_check_count": None,
        "failed_blocking_check_count": None,
        "failed_blocking_check_kinds": None,
    }
    assert receipt["issues"] == {
        "cluster_count": None,
        "blocking_cluster_count": None,
        "severity_counts": None,
        "category_counts": None,
    }
    assert receipt["outcome"]["warning_count"] is None
    assert receipt["outcome"]["fallback_reason_code"] is None
    assert receipt["outcome"]["fallback_reason_redacted"] is None
    assert receipt["outcome"]["suggested_translation_present"] is None
    assert receipt["decision_support"] == loaded.decision_support.model_dump(mode="json")
    assert receipt["decision_support"]["level"] == "insufficient"
    assert "decision_support.level" not in unavailable
    assert all(value is None for value in receipt["coherence"].values())
    assert {
        "routing.active_role_ids", "reviewer_execution.samples",
        "preflight.blocking", "preflight.failed_check_count",
        "preflight.failed_blocking_check_count", "preflight.failed_blocking_check_kinds",
        "issues.cluster_count", "issues.blocking_cluster_count", "issues.severity_counts",
        "issues.category_counts", "outcome.warning_count", "outcome.fallback_reason_code",
        "outcome.fallback_reason_redacted", "outcome.suggested_translation_present",
        "coherence.expected_terminal_disposition", "coherence.terminal_disposition_occurrences",
        "coherence.terminal_disposition_is_last_report_line",
        "coherence.terminal_disposition_matches_structured",
    } <= unavailable
    assert receipt["availability"]["verification_complete"] is False
    assert receipt["availability"]["redacted_fields"] == []
    assert "SECRET" not in path.read_text(encoding="utf-8")
    assert "SECRET" not in str(receipt)
    assert "SECRET" not in report
