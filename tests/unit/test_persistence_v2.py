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
