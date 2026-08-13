import json

from council_of_translation.localization.compatibility import parse_review_record
from council_of_translation.localization.models import (
    BriefingInteraction,
    ContextGapV2,
    PhaseRecord,
    PhaseReconsiderationProvenance,
    PhaseTrace,
    ReviewBriefV2,
    ReviewRecordV2,
    ReviewTaskV2,
)
from council_of_translation.localization.persistence import ReviewStore, build_review_id


def _record(*, history_mode: str = "full") -> ReviewRecordV2:
    secret = "BRIEF-SECRET-回答"
    return ReviewRecordV2(
        review_id=build_review_id(),
        task=ReviewTaskV2(
            source_text="source secret",
            candidate_translation="candidate secret",
            context="caller secret",
            history_mode=history_mode,
            briefing_mode="always",
        ),
        effective_brief=ReviewBriefV2(
            content_type="ui",
            usage_context=secret,
            assumptions=["model secret"],
            context_confidence="partial",
            field_provenance={"content_type": "normalized_alias"},
        ),
        briefing_interaction=BriefingInteraction(
            requested=True,
            action="accept",
            asked_fields=["usage_context"],
            accepted_answers={"usage_context": secret},
            answer_provenance={"usage_context": "user_briefing"},
        ),
        context_gaps=[
            ContextGapV2(
                gap_id="gap_1",
                question="secret question",
                materiality="secret materiality",
                answer="secret answer",
                disposition="answered",
            )
        ],
        context_reconsideration_provenance=PhaseReconsiderationProvenance(
            requested_role_ids=["fidelity_reviewer"],
            completed_role_ids=["fidelity_reviewer"],
            change_effects=["secret effect"],
        ),
        phase_trace=PhaseTrace(
            phases=[PhaseRecord(phase="briefing", disposition="accept", counts={"asked": 1}, summary="secret summary")]
        ),
        display_report="secret markdown",
    )


def test_v23_is_authoritative_and_older_v2_records_remain_readable():
    assert _record().schema_version == "2.3"
    for version in ("2.0", "2.1", "2.2", "2.3"):
        payload = _record().model_dump(mode="json")
        payload["schema_version"] = version
        assert parse_review_record(payload).schema_version == version


def test_v22_runtime_metadata_loads_with_conservative_parallel_defaults():
    payload = _record().model_dump(mode="json")
    payload["schema_version"] = "2.2"
    for field in (
        "wall_clock_ms", "sampling_wait_ms", "independent_review_concurrency_limit",
        "independent_review_peak_concurrency", "independent_review_batch_count",
        "independent_review_concurrency_disposition",
    ):
        payload["runtime_metadata"].pop(field, None)
    loaded = parse_review_record(payload)
    assert loaded.schema_version == "2.2"
    assert loaded.runtime_metadata.wall_clock_ms == 0
    assert loaded.runtime_metadata.sampling_wait_ms == 0
    assert loaded.runtime_metadata.independent_review_concurrency_limit == 1
    assert loaded.runtime_metadata.independent_review_peak_concurrency == 0
    assert loaded.runtime_metadata.independent_review_batch_count == 0
    assert loaded.runtime_metadata.independent_review_concurrency_disposition == "legacy"


def test_guided_models_bound_malformed_and_hostile_values():
    brief = ReviewBriefV2(
        domain="x" * 500,
        assumptions=["y" * 500] * 20,
        field_provenance={"domain": "caller", "unknown": "caller"},
    )
    assert len(brief.domain) == 120
    assert len(brief.assumptions) == 1 and len(brief.assumptions[0]) == 240
    assert brief.field_provenance == {"domain": "caller"}
    invalid = ContextGapV2(gap_id="gap", question="", materiality="")
    assert invalid.disposition == "suppressed" and invalid.reason == "invalid_gap"


def test_v22_full_metadata_and_off_round_trips_are_privacy_safe(tmp_path):
    full_store = ReviewStore(tmp_path / "full", include_legacy=False)
    full = _record()
    full_path = full_store.save(full)
    assert full_path is not None
    assert full_store.load(full.review_id).schema_version == "2.3"
    assert "secret markdown" in full_path.read_text(encoding="utf-8")

    metadata_store = ReviewStore(tmp_path / "metadata", include_legacy=False)
    metadata = _record(history_mode="metadata")
    metadata_path = metadata_store.save(metadata)
    assert metadata_path is not None
    raw = metadata_path.read_text(encoding="utf-8")
    payload = json.loads(raw)
    assert payload["schema_version"] == "2.3"
    assert payload["runtime_metadata"]["independent_review_concurrency_limit"] == 1
    assert payload["runtime_metadata"]["independent_review_concurrency_disposition"] == "legacy"
    assert payload["effective_brief"] == {"content_type": "ui", "context_confidence": "partial"}
    assert payload["briefing_interaction"]["action"] == "accept"
    assert payload["context_gap_interaction"] == {
        "requested": False,
        "action": "skipped",
        "asked_count": 0,
        "answered_count": 0,
    }
    for secret in ("source secret", "candidate secret", "caller secret", "BRIEF-SECRET", "secret question", "secret answer", "secret effect", "secret markdown", "secret summary"):
        assert secret not in raw

    off = _record(history_mode="off")
    assert ReviewStore(tmp_path / "off", include_legacy=False).save(off) is None
    assert not (tmp_path / "off").exists()


def test_metadata_allowlist_normalizes_hostile_guided_labels(tmp_path):
    record = _record(history_mode="metadata")
    record.effective_brief.content_type = "SECRET-CONTENT-TYPE"
    record.briefing_interaction.asked_fields = ["SECRET-FIELD-NAME"]
    record.phase_trace.phases[0].disposition = "SECRET-PHASE-DISPOSITION"
    path = ReviewStore(tmp_path, include_legacy=False).save(record)
    raw = path.read_text(encoding="utf-8")
    payload = json.loads(raw)
    assert "SECRET" not in raw
    assert payload["effective_brief"]["content_type"] == "unspecified"
    assert payload["briefing_interaction"]["asked_fields"] == []
    assert payload["phase_trace"]["phases"][0]["disposition"] == "degraded"
