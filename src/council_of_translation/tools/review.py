"""Frozen five-tool MCP surface for Council of Translation V0.4."""

from __future__ import annotations

from importlib.metadata import PackageNotFoundError, version
from typing import Any

from fastmcp import Context

from council_of_translation import __version__
from council_of_translation.localization.compatibility import ReviewRecordV1
from council_of_translation.localization.models import InputDiagnostics, ReviewRecordV2, ReviewTaskV2
from council_of_translation.localization.orchestration import (
    compact_review_response,
    continue_structured_review,
    run_structured_review,
)
from council_of_translation.localization.persistence import ReviewPersistenceError, ReviewStore
from council_of_translation.localization.runtime import (
    FastMCPModelExecutor,
    FastMCPUserInteractionGateway,
    RuntimeTelemetry,
)
from council_of_translation.localization.roles import normalize_mode
from council_of_translation.security import sanitize_text
from council_of_translation.server import mcp


MAX_REVIEW_FIELD_LENGTH = 12_000
DIAGNOSTIC_BUILD = "structured-deliberation-v2"


def _installed_version() -> str:
    try:
        return version("Council-of-Translation")
    except PackageNotFoundError:
        return __version__


def _server_info() -> dict[str, Any]:
    return {
        "name": "Council-of-Translation",
        "package_version": _installed_version(),
        "module_version": __version__,
        "diagnostic_build": DIAGNOSTIC_BUILD,
        "schema_version": "2.0",
        "default_output_mode": "review_only",
        "default_interactive_mode": "auto",
        "default_trace_level": "summary",
        "default_history_mode": "full",
        "user_authority": "decisive_within_valid_options",
        "decision_fallback": "council_adjudication",
        "review_only": True,
        "sample_budgets": {"lightweight": 6, "standard": 10, "strict": 14},
        "max_decision_points": 3,
        "normal_tools": [
            "review_translation",
            "continue_review",
            "view_review_record",
            "list_review_records",
            "get_server_info",
        ],
    }


def _clean(value: str | None, max_length: int = MAX_REVIEW_FIELD_LENGTH) -> str:
    return sanitize_text(value or "", max_length=max_length)


def _clean_list(values: list[str] | None, *, maximum: int = 100) -> list[str]:
    return [_clean(str(value), max_length=500) for value in (values or [])[:maximum] if str(value).strip()]


def _task_and_diagnostics(
    *,
    source_text: str,
    candidate_translation: str,
    source_language: str,
    target_language: str,
    content_type: str,
    context: str,
    audience: str,
    mode: str,
    output_mode: str,
    interactive_mode: str,
    decision_fallback: str,
    trace_level: str,
    history_mode: str,
    term_glossary: str,
    style_guide: str,
    project_rules: str,
    brand_guidelines: str,
    technical_constraints: str,
    do_not_translate_literals: list[str] | None,
    hard_constraints: list[str] | None,
    reference_translations: str,
    known_exceptions: str,
    notes: str,
) -> tuple[ReviewTaskV2, InputDiagnostics]:
    if decision_fallback == "return_pending" and history_mode != "full":
        raise ValueError("decision_fallback=return_pending requires history_mode=full")
    clean_source = _clean(source_text)
    clean_candidate = _clean(candidate_translation)
    diagnostics = InputDiagnostics(
        source_original_length=len(source_text),
        source_reviewed_length=len(clean_source),
        source_truncated=len(source_text) > MAX_REVIEW_FIELD_LENGTH,
        candidate_original_length=len(candidate_translation),
        candidate_reviewed_length=len(clean_candidate),
        candidate_truncated=len(candidate_translation) > MAX_REVIEW_FIELD_LENGTH,
    )
    task = ReviewTaskV2.model_validate(
        {
            "source_text": clean_source,
            "candidate_translation": clean_candidate,
            "source_language": _clean(source_language or "auto", 100),
            "target_language": _clean(target_language or "zh-CN", 100),
            "content_type": _clean(content_type or "unspecified", 200),
            "context": _clean(context),
            "audience": _clean(audience),
            "mode": normalize_mode(mode),
            "output_mode": output_mode if output_mode in {"review_only", "with_snippets", "full_rewrite"} else "review_only",
            "interactive_mode": interactive_mode if interactive_mode in {"auto", "off", "required"} else "auto",
            "decision_fallback": decision_fallback if decision_fallback in {"council_adjudication", "return_pending"} else "council_adjudication",
            "trace_level": trace_level if trace_level in {"summary", "full"} else "summary",
            "history_mode": history_mode if history_mode in {"off", "metadata", "full"} else "full",
            "term_glossary": _clean(term_glossary),
            "style_guide": _clean(style_guide),
            "project_rules": _clean(project_rules),
            "brand_guidelines": _clean(brand_guidelines),
            "technical_constraints": _clean(technical_constraints),
            "do_not_translate_literals": _clean_list(do_not_translate_literals),
            "hard_constraints": _clean_list(hard_constraints, maximum=20),
            "reference_translations": _clean(reference_translations),
            "known_exceptions": _clean(known_exceptions),
            "notes": _clean(notes),
        }
    )
    return task, diagnostics


def _error(exc: Exception) -> dict[str, str]:
    return {"error": str(exc), "error_type": type(exc).__name__}


@mcp.tool()
def get_server_info() -> dict[str, Any]:
    """Return V0.4 version, capability, budget, and frozen-tool diagnostics."""
    return _server_info()


@mcp.tool()
async def review_translation(
    source_text: str,
    candidate_translation: str,
    ctx: Context,
    source_language: str = "auto",
    target_language: str = "zh-CN",
    content_type: str = "unspecified",
    context: str = "",
    audience: str = "",
    mode: str = "standard",
    output_mode: str = "review_only",
    interactive_mode: str = "auto",
    decision_fallback: str = "council_adjudication",
    trace_level: str = "summary",
    history_mode: str = "full",
    term_glossary: str = "",
    style_guide: str = "",
    project_rules: str = "",
    brand_guidelines: str = "",
    technical_constraints: str = "",
    do_not_translate_literals: list[str] | None = None,
    hard_constraints: list[str] | None = None,
    reference_translations: str = "",
    known_exceptions: str = "",
    notes: str = "",
) -> dict[str, Any]:
    """Review an existing translation through bounded structured deliberation.

    This is review-only: it never edits translation files. The default response
    is compact; full structured evidence is retrieved with view_review_record.
    A full suggested translation is permitted only when output_mode is explicitly
    full_rewrite, and is never emitted by the default review_only path.
    """
    if not source_text.strip():
        return {"error": "source_text is required"}
    if not candidate_translation.strip():
        return {"error": "candidate_translation is required"}
    try:
        task, diagnostics = _task_and_diagnostics(
            source_text=source_text,
            candidate_translation=candidate_translation,
            source_language=source_language,
            target_language=target_language,
            content_type=content_type,
            context=context,
            audience=audience,
            mode=mode,
            output_mode=output_mode,
            interactive_mode=interactive_mode,
            decision_fallback=decision_fallback,
            trace_level=trace_level,
            history_mode=history_mode,
            term_glossary=term_glossary,
            style_guide=style_guide,
            project_rules=project_rules,
            brand_guidelines=brand_guidelines,
            technical_constraints=technical_constraints,
            do_not_translate_literals=do_not_translate_literals,
            hard_constraints=hard_constraints,
            reference_translations=reference_translations,
            known_exceptions=known_exceptions,
            notes=notes,
        )
        budget = {"lightweight": 6, "standard": 10, "strict": 14}[task.mode]
        telemetry = RuntimeTelemetry(sample_budget=budget)
        record = await run_structured_review(
            task,
            FastMCPModelExecutor(ctx, telemetry),
            FastMCPUserInteractionGateway(ctx, telemetry),
            input_diagnostics=diagnostics,
        )
        response = record.model_dump(mode="json", exclude_none=True) if task.trace_level == "full" else compact_review_response(record)
        response["server_info"] = _server_info()
        return response
    except (ValueError, ReviewPersistenceError) as exc:
        return _error(exc)


@mcp.tool()
async def continue_review(
    review_id: str,
    user_decisions: list[dict[str, Any]],
    ctx: Context,
) -> dict[str, Any]:
    """Create an immutable linked revision using decisions for active DecisionPoints.

    Only roles affected by those decisions are reconsidered. Independent review
    and unaffected roles are not rerun.
    """
    store = ReviewStore()
    try:
        parent = store.load(review_id)
        if not isinstance(parent, ReviewRecordV2):
            return {"error": "continue_review requires a V2 review record"}
        telemetry = RuntimeTelemetry(sample_budget=parent.council_plan.sample_budget)
        child = await continue_structured_review(
            parent,
            user_decisions,
            FastMCPModelExecutor(ctx, telemetry),
            store=store,
        )
        response = compact_review_response(child)
        response["server_info"] = _server_info()
        return response
    except (ValueError, ReviewPersistenceError) as exc:
        return _error(exc)


@mcp.tool()
def view_review_record(review_id: str, detail_level: str = "full") -> dict[str, Any]:
    """Read a V1 or V2 record; use summary for a compact V2 projection."""
    try:
        record = ReviewStore().load(review_id)
        if isinstance(record, ReviewRecordV2) and detail_level == "summary":
            return compact_review_response(record)
        if detail_level not in {"full", "summary"}:
            return {"error": "detail_level must be full or summary"}
        return record.model_dump(mode="json")
    except ReviewPersistenceError as exc:
        return _error(exc)


@mcp.tool()
def list_review_records(limit: int = 50) -> dict[str, Any]:
    """List privacy-safe V1/V2 review metadata from new and legacy storage."""
    records: list[dict[str, Any]] = []
    try:
        for record in ReviewStore().iter_records():
            if isinstance(record, ReviewRecordV2):
                records.append(
                    {
                        "schema_version": "2.0",
                        "review_id": record.review_id,
                        "parent_review_id": record.parent_review_id,
                        "created_at": record.created_at.isoformat(),
                        "mode": record.task.mode,
                        "status": record.status,
                        "publishability": record.chief_editor_decision.publishability,
                        "review_needed": record.chief_editor_decision.review_needed,
                    }
                )
            elif isinstance(record, ReviewRecordV1):
                records.append(
                    {
                        "schema_version": "1.0",
                        "review_id": record.review_id,
                        "mode": record.mode,
                        "status": record.status,
                        "publishability": record.chief_editor_decision.get("publishability"),
                        "review_needed": record.chief_editor_decision.get("review_needed"),
                    }
                )
            if len(records) >= max(0, min(limit, 200)):
                break
        return {"total_reviews": len(records), "reviews": records}
    except ReviewPersistenceError as exc:
        return _error(exc)
