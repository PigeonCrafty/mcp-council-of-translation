import asyncio
from copy import deepcopy

from fastmcp import Client

from council_of_translation.localization.models import (
    ChiefEditorDecisionV2,
    ReviewRecordV2,
    ReviewTaskV2,
)
from council_of_translation.localization.orchestration import compact_review_response
from council_of_translation.presentation import structured_payload
from council_of_translation.server import mcp
from council_of_translation.tools import review as review_module


def _record() -> ReviewRecordV2:
    record = ReviewRecordV2(
        schema_version="2.5",
        review_id="20260824T020304000005Z_ab12cd34",
        task=ReviewTaskV2(
            source_text="Save",
            candidate_translation="保存",
            content_type="ui",
            history_mode="full",
        ),
        chief_editor_decision=ChiefEditorDecisionV2(
            publishability="可发布",
            review_needed="否",
        ),
        status="COMPLETED",
        display_report=(
            "# 审校背景\n\n- 当前译文通过审校。\n\n"
            "## 主编结论\n\n- 最终处置：可发布；需人工复核：否"
        ),
    )
    # A persisted full record physically contains every modeled field, including
    # empty lists and zero counters. Revalidation reproduces that loaded shape.
    return ReviewRecordV2.model_validate(record.model_dump(mode="json"))


def test_actual_registered_verification_view_has_exact_dual_channel_wrapper(monkeypatch):
    record = _record()
    before = deepcopy(record.model_dump(mode="json"))
    calls = {"load": 0, "save": 0}

    class FakeStore:
        def load(self, review_id):
            calls["load"] += 1
            assert review_id == record.review_id
            return record

        def save(self, *args, **kwargs):
            calls["save"] += 1
            raise AssertionError("verification retrieval must not save")

    monkeypatch.setattr(review_module, "ReviewStore", FakeStore)

    async def call():
        async with Client(mcp) as client:
            return await client.call_tool(
                "view_review_record",
                {"review_id": record.review_id, "detail_level": "verification"},
            )

    result = asyncio.run(call())
    payload = result.structured_content

    assert list(payload) == ["review_id", "display_report", "verification_receipt"]
    assert payload["review_id"] == record.review_id
    assert payload["verification_receipt"]["review_id"] == record.review_id
    assert payload["verification_receipt"]["availability"]["verification_complete"] is True
    assert result.content[0].text.startswith("# Council 验证回执")
    assert [line for line in payload["display_report"].splitlines() if line.startswith("#")] == [
        "# Council 验证回执",
        "## 记录与路由",
        "## 覆盖与调用",
        "## 风险与裁决",
        "## 一致性与可用性",
    ]
    assert result.content[0].text.endswith(
        f"审校记录：{record.review_id}；可用 view_review_record 获取结构化证据。"
    )
    assert "source_text" not in str(payload)
    assert "candidate_translation" not in str(payload)
    assert calls == {"load": 1, "save": 0}
    assert record.model_dump(mode="json") == before


def test_existing_full_and_summary_payloads_remain_exact(monkeypatch):
    record = _record()

    class FakeStore:
        def load(self, review_id):
            assert review_id == record.review_id
            return record

    monkeypatch.setattr(review_module, "ReviewStore", FakeStore)

    full = structured_payload(review_module.view_review_record.fn(record.review_id, "full"))
    summary = structured_payload(review_module.view_review_record.fn(record.review_id, "summary"))

    assert full == record.model_dump(mode="json")
    assert summary == compact_review_response(record)


def test_direct_invalid_detail_level_keeps_bounded_truthful_error(monkeypatch):
    record = _record()

    class FakeStore:
        def load(self, review_id):
            return record

    monkeypatch.setattr(review_module, "ReviewStore", FakeStore)

    payload = structured_payload(
        review_module.view_review_record.fn(record.review_id, "PRIVATE invalid detail")
    )

    assert payload == {"error": "detail_level must be full, summary, or verification"}
    assert "PRIVATE" not in str(payload)
