"""FastMCP-compatible dual-channel presentation for human-facing tools."""

from __future__ import annotations

from typing import Any

from fastmcp.tools.tool import ToolResult
from mcp.types import TextContent

from council_of_translation.localization.verification import (
    append_canonical_receipt_json,
    is_canonical_verification_receipt,
)


MAX_PRIMARY_TEXT = 3_200


def _bounded(value: Any, maximum: int) -> str:
    text = str(value or "").strip()
    return text if len(text) <= maximum else text[: maximum - 1].rstrip() + "…"


def primary_text_for_payload(payload: dict[str, Any]) -> str:
    """Return bounded human text without exposing raw structured record content."""
    if payload.get("error"):
        message = _bounded(payload.get("error"), 240) or "未知错误"
        return f"# 审校未完成\n\n- {message}"

    report = str(payload.get("display_report") or "").strip()
    review_id = _bounded(payload.get("review_id"), 96)
    if not report:
        status = _bounded(payload.get("status"), 80) or "已读取"
        report = (
            "# 审校记录\n\n"
            "- 这是旧版或精简记录；完整结构化内容仍在本次工具结果中。\n\n"
            f"## 主编结论\n\n- 状态：{status}"
        )

    footer = (
        f"\n\n审校记录：{review_id}；可用 view_review_record 获取结构化证据。"
        if review_id else ""
    )
    available = MAX_PRIMARY_TEXT - len(footer)
    if len(report) > available:
        report = report[: max(0, available - 1)].rstrip() + "…"
    return report + footer


def dual_channel_result(payload: dict[str, Any]) -> ToolResult:
    """Expose primary Markdown and the unchanged JSON-safe dictionary together."""
    primary_text = primary_text_for_payload(payload)
    receipt = payload.get("verification_receipt")
    if is_canonical_verification_receipt(receipt):
        primary_text = append_canonical_receipt_json(primary_text, receipt)
    return ToolResult(
        content=[TextContent(type="text", text=primary_text)],
        structured_content=payload,
    )


def structured_payload(result: ToolResult | dict[str, Any]) -> dict[str, Any]:
    """Unwrap results for internal callers and backwards-compatible assertions."""
    if isinstance(result, dict):
        return result
    return result.structured_content or {}
