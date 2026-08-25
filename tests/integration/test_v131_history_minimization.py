import json

from council_of_translation.localization.compatibility import ReviewRecordV1
from council_of_translation.localization.models import ReviewRecordV2, ReviewTaskV2
from council_of_translation.localization.orchestration import compact_review_response
from council_of_translation.presentation import structured_payload
import council_of_translation.tools.review as review_module


SENTINELS = ("PRIVATE_TASK_SENTINEL", "HOSTILE_REVIEW_SENTINEL", "SECRET_RATIONALE_SENTINEL")


class CountingStore:
    record = None
    loads = 0
    saves = 0

    def load(self, review_id):
        type(self).loads += 1
        assert self.record is not None
        assert review_id == self.record.review_id
        return self.record

    def save(self, *args, **kwargs):
        type(self).saves += 1
        raise AssertionError("history views must not save")


def _legacy_record():
    return ReviewRecordV1(
        review_id="legacy-summary-1",
        mode="standard",
        status="completed",
        task={"source_text": SENTINELS[0]},
        reviews=[{"role_feedback": SENTINELS[1]}],
        chief_editor_decision={
            "publishability": "需人工复核",
            "review_needed": "是",
            "decision_rationale": SENTINELS[2],
        },
        reviewer_outputs=[{"private": SENTINELS[1]}],
    )


def _install(monkeypatch, record):
    CountingStore.record = record
    CountingStore.loads = 0
    CountingStore.saves = 0
    monkeypatch.setattr(review_module, "ReviewStore", CountingStore)


def test_v1_summary_is_exact_six_field_privacy_projection(monkeypatch):
    record = _legacy_record()
    _install(monkeypatch, record)

    result = review_module.view_review_record.fn(record.review_id, "summary")
    payload = structured_payload(result)

    assert list(payload) == [
        "schema_version",
        "review_id",
        "mode",
        "status",
        "publishability",
        "review_needed",
    ]
    assert payload == {
        "schema_version": "1.0",
        "review_id": record.review_id,
        "mode": "standard",
        "status": "completed",
        "publishability": "需人工复核",
        "review_needed": "是",
    }
    rendered = json.dumps(payload, ensure_ascii=False) + result.content[0].text
    assert all(sentinel not in rendered for sentinel in SENTINELS)
    assert CountingStore.loads == 1
    assert CountingStore.saves == 0


def test_v1_full_remains_byte_compatible(monkeypatch):
    record = _legacy_record()
    expected = record.model_dump(mode="json")
    _install(monkeypatch, record)

    payload = structured_payload(review_module.view_review_record.fn(record.review_id, "full"))

    assert payload == expected
    assert json.dumps(payload, ensure_ascii=False, separators=(",", ":")) == json.dumps(
        expected, ensure_ascii=False, separators=(",", ":")
    )
    assert CountingStore.loads == 1
    assert CountingStore.saves == 0


def test_v1_verification_remains_canonical_and_private(monkeypatch):
    record = _legacy_record()
    _install(monkeypatch, record)

    result = review_module.view_review_record.fn(record.review_id, "verification")
    payload = structured_payload(result)

    assert list(payload) == ["review_id", "display_report", "verification_receipt"]
    assert payload["verification_receipt"]["receipt_schema_version"] == "1.1"
    rendered = json.dumps(payload, ensure_ascii=False) + result.content[0].text
    assert all(sentinel not in rendered for sentinel in SENTINELS)
    assert CountingStore.loads == 1
    assert CountingStore.saves == 0


def test_v2_summary_projection_is_unchanged(monkeypatch):
    record = ReviewRecordV2(
        review_id="current-summary-1",
        task=ReviewTaskV2(source_text="Save", candidate_translation="保存", briefing_mode="off"),
    )
    _install(monkeypatch, record)

    payload = structured_payload(review_module.view_review_record.fn(record.review_id, "summary"))

    assert payload == compact_review_response(record)
    assert CountingStore.loads == 1
    assert CountingStore.saves == 0
