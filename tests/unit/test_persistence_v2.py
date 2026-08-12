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
        runtime_metadata=RuntimeMetadata(fallbacks=["SECRET RUNTIME TEXT"]),
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
    assert loaded.schema_version == "2.2"


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
    assert loaded.schema_version == "2.2"


@pytest.mark.parametrize("history_mode", ["full", "metadata"])
def test_new_write_persists_truthful_v071_runtime_and_version_identifiers(tmp_path, history_mode):
    store = ReviewStore(tmp_path / "new", legacy_dir=tmp_path / "legacy")
    record = ReviewRecordV2(
        review_id=build_review_id(),
        task=ReviewTaskV2(source_text="Save", candidate_translation="保存", history_mode=history_mode),
    )
    path = store.save(record, history_mode=history_mode)

    payload = json.loads(path.read_text(encoding="utf-8"))
    expected = {
        "package_version": "0.8.0",
        "diagnostic_build": "context-coherent-council-v6",
    }
    assert {key: payload["runtime_metadata"][key] for key in expected} == expected
    assert {key: payload["version_metadata"][key] for key in expected} == expected
    assert payload["version_metadata"]["record_schema"] == "2.2"

    loaded = store.load(record.review_id)
    assert loaded.runtime_metadata.package_version == "0.8.0"
    assert loaded.runtime_metadata.diagnostic_build == "context-coherent-council-v6"
    assert loaded.version_metadata == {**expected, "record_schema": "2.2"}


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
    assert loaded.status == "COMPLETED"
    assert loaded.chief_editor_decision.publishability == "可发布"
    assert loaded.chief_editor_decision.review_needed == "否"
    assert loaded.chief_editor_decision.decision_rationale == ""
    listed = list(store.iter_records())
    assert [(item.status, item.chief_editor_decision.publishability, item.chief_editor_decision.review_needed) for item in listed] == [
        ("COMPLETED", "可发布", "否")
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


def test_saving_readable_v20_model_writes_new_v22_schema(tmp_path):
    store = ReviewStore(tmp_path / "new", legacy_dir=tmp_path / "legacy")
    record = _record(build_review_id()).model_copy(update={"schema_version": "2.0"})
    path = store.save(record)

    payload = json.loads(path.read_text(encoding="utf-8"))
    assert payload["schema_version"] == "2.2"
    assert payload["version_metadata"]["record_schema"] == "2.2"
    assert store.load(record.review_id).schema_version == "2.2"
