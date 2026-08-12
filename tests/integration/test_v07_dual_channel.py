import asyncio

from fastmcp import Client

from council_of_translation.localization.models import ReviewRecordV2, ReviewTaskV2
from council_of_translation.server import mcp
import council_of_translation.tools.review as review_module


def _record(review_id: str, *, parent_review_id: str | None = None) -> ReviewRecordV2:
    return ReviewRecordV2(
        review_id=review_id,
        parent_review_id=parent_review_id,
        task=ReviewTaskV2(
            source_text="Save",
            candidate_translation="保存",
            briefing_mode="off",
        ),
        display_report="# 审校背景\n\n- 测试审校背景。\n\n## 主编结论\n\n- 最终处置：可发布。",
        status="COMPLETED",
    )


def test_actual_fastmcp_review_result_has_primary_text_and_structured_content(monkeypatch):
    record = _record("20260812T120000000000Z_aaaaaaaaaaaa")

    async def fake_run(*args, **kwargs):
        return record

    monkeypatch.setattr(review_module, "run_structured_review", fake_run)

    async def call():
        async with Client(mcp) as client:
            return await client.call_tool(
                "review_translation",
                {"source_text": "Save", "candidate_translation": "保存"},
            )

    result = asyncio.run(call())
    assert result.content[0].type == "text"
    assert result.content[0].text.startswith("# 审校背景")
    assert result.structured_content["review_id"] == record.review_id
    assert result.structured_content["display_report"] == record.display_report
    assert "process_digest" in result.structured_content
    assert "server_info" in result.structured_content


def test_actual_fastmcp_continuation_and_view_share_dual_channel(monkeypatch):
    parent = _record("20260812T120000000000Z_bbbbbbbbbbbb")
    child = _record(
        "20260812T120100000000Z_cccccccccccc",
        parent_review_id=parent.review_id,
    )

    class FakeStore:
        def load(self, review_id):
            assert review_id == parent.review_id
            return parent

    async def fake_continue(*args, **kwargs):
        return child

    monkeypatch.setattr(review_module, "ReviewStore", FakeStore)
    monkeypatch.setattr(review_module, "continue_structured_review", fake_continue)

    async def call():
        async with Client(mcp) as client:
            continuation = await client.call_tool(
                "continue_review",
                {"review_id": parent.review_id, "user_decisions": []},
            )
            viewed = await client.call_tool(
                "view_review_record",
                {"review_id": parent.review_id, "detail_level": "full"},
            )
            return continuation, viewed

    continuation, viewed = asyncio.run(call())
    assert continuation.content[0].text.startswith("# 审校背景")
    assert continuation.structured_content["parent_review_id"] == parent.review_id
    assert viewed.content[0].text.startswith("# 审校背景")
    assert viewed.structured_content["review_id"] == parent.review_id
    assert "independent_reviews" in viewed.structured_content


def test_actual_fastmcp_error_is_safe_in_both_channels():
    async def call():
        async with Client(mcp) as client:
            return await client.call_tool(
                "review_translation",
                {"source_text": "", "candidate_translation": "保存"},
            )

    result = asyncio.run(call())
    assert result.content[0].text == "# 审校未完成\n\n- source_text is required"
    assert result.structured_content == {"error": "source_text is required"}
