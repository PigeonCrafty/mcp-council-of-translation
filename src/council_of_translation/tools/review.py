import json
import logging
from importlib.metadata import PackageNotFoundError, version
from pathlib import Path

from fastmcp import Context

from council_of_translation import __version__
from council_of_translation.localization.roles import normalize_mode
from council_of_translation.localization.schemas import TranslationReviewTask
from council_of_translation.localization.workflow import run_translation_review
from council_of_translation.security import sanitize_text, validate_debate_id
from council_of_translation.server import mcp


MAX_REVIEW_FIELD_LENGTH = 12000
DIAGNOSTIC_BUILD = "review-result-self-identifying-v1"


def _installed_version() -> str:
    try:
        return version("Council-of-Translation")
    except PackageNotFoundError:
        return __version__


def _server_info() -> dict:
    return {
        "name": "Council-of-Translation",
        "package_version": _installed_version(),
        "module_version": __version__,
        "diagnostic_build": DIAGNOSTIC_BUILD,
        "review_fallback": "preserves unstructured reviewer output",
        "sampling_result_parsing": "extracts Goose SamplingResult.text",
    }


def _clean(value: str | None, max_length: int = MAX_REVIEW_FIELD_LENGTH) -> str:
    return sanitize_text(value or "", max_length=max_length)


def _build_task(
    source_text: str,
    candidate_translation: str,
    source_language: str,
    target_language: str,
    content_type: str,
    context: str,
    audience: str,
    mode: str,
    term_glossary: str,
    style_guide: str,
    project_rules: str,
    brand_guidelines: str,
    technical_constraints: str,
    reference_translations: str,
    known_exceptions: str,
    notes: str,
) -> TranslationReviewTask:
    return {
        "source_text": _clean(source_text),
        "candidate_translation": _clean(candidate_translation),
        "source_language": _clean(source_language or "auto", max_length=100),
        "target_language": _clean(target_language or "zh-CN", max_length=100),
        "content_type": _clean(content_type or "unspecified", max_length=200),
        "context": _clean(context),
        "audience": _clean(audience),
        "mode": normalize_mode(mode),
        "term_glossary": _clean(term_glossary),
        "style_guide": _clean(style_guide),
        "project_rules": _clean(project_rules),
        "brand_guidelines": _clean(brand_guidelines),
        "technical_constraints": _clean(technical_constraints),
        "reference_translations": _clean(reference_translations),
        "known_exceptions": _clean(known_exceptions),
        "notes": _clean(notes),
    }


@mcp.tool()
def get_server_info() -> dict:
    """
    Return diagnostic information for the running Council of Translation MCP server.

    Diagnostic-only tool. Do not call this for ordinary translation reviews; call
    review_translation directly. Use get_server_info only when checking whether the
    host is running a stale cached server.
    """
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
    term_glossary: str = "",
    style_guide: str = "",
    project_rules: str = "",
    brand_guidelines: str = "",
    technical_constraints: str = "",
    reference_translations: str = "",
    known_exceptions: str = "",
    notes: str = "",
) -> dict:
    """
    Review a candidate localization translation with role-specific reviewers and a chief editor.

    This tool is review-only: it returns structured findings and a recommended translation
    for the calling agent to apply. It does not modify files and does not replace the
    caller's translation skill, TB, SG, or project-rule retrieval.

    Args:
        source_text: Source text to review against.
        candidate_translation: Existing candidate translation to review.
        source_language: Source language code or name, e.g. en.
        target_language: Target locale/language, e.g. zh-CN.
        content_type: Content type such as ui, help, marketing, error, technical, legal-lite.
        context: Product/page/component context and neighboring meaning.
        audience: Target user group.
        mode: Review depth: lightweight, standard, or strict. Defaults to standard.
        term_glossary: Relevant TB entries for this segment, not necessarily the full TB.
        style_guide: Relevant SG rules for this segment.
        project_rules: Project-specific rules, forbidden wording, punctuation, naming, etc.
        brand_guidelines: Relevant brand voice rules.
        technical_constraints: Placeholders, markup, do-not-translate items, length limits, etc.
        reference_translations: Historical or neighboring translations relevant to this segment.
        known_exceptions: Known exceptions that should override normal reviewer preferences.
        notes: Additional caller notes.

    Returns:
        Structured review report with reviewer outputs, chief editor decision, and
        server_info diagnostics. This is the default tool for translation review.
    """
    if not _clean(source_text, max_length=1_000_000):
        return {"error": "source_text is required"}
    if not _clean(candidate_translation, max_length=1_000_000):
        return {"error": "candidate_translation is required"}

    task = _build_task(
        source_text=source_text,
        candidate_translation=candidate_translation,
        source_language=source_language,
        target_language=target_language,
        content_type=content_type,
        context=context,
        audience=audience,
        mode=mode,
        term_glossary=term_glossary,
        style_guide=style_guide,
        project_rules=project_rules,
        brand_guidelines=brand_guidelines,
        technical_constraints=technical_constraints,
        reference_translations=reference_translations,
        known_exceptions=known_exceptions,
        notes=notes,
    )

    record = await run_translation_review(task, ctx)
    record["server_info"] = _server_info()
    return record


@mcp.tool()
def list_review_records() -> dict:
    """
    List saved localization review records.

    Returns:
        Review IDs and summary metadata for records saved in the reviews directory.
    """
    reviews_dir = Path("reviews")
    if not reviews_dir.exists():
        return {"total_reviews": 0, "reviews": []}

    reviews = []
    for file_path in sorted(reviews_dir.glob("*.json"), reverse=True):
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                record = json.load(f)
            task = record.get("task", {})
            decision = record.get("chief_editor_decision", {})
            reviews.append(
                {
                    "review_id": record.get("review_id"),
                    "mode": record.get("mode"),
                    "source_text": task.get("source_text", "")[:120],
                    "candidate_translation": task.get("candidate_translation", "")[:120],
                    "publishability": decision.get("publishability"),
                    "review_needed": decision.get("review_needed"),
                }
            )
        except (json.JSONDecodeError, OSError) as e:
            logging.warning(f"Skipping invalid review record {file_path}: {e}")

    return {"total_reviews": len(reviews), "reviews": reviews}


@mcp.tool()
def view_review_record(review_id: str) -> dict:
    """
    View a saved localization review record by ID.

    Args:
        review_id: Review ID in YYYYMMDD_HHMMSS format.

    Returns:
        Complete review record including task input, reviewer findings, and chief editor decision.
    """
    if not validate_debate_id(review_id):
        return {"error": "Invalid review_id format. Expected: YYYYMMDD_HHMMSS"}

    reviews_dir = Path("reviews")
    file_path = reviews_dir / f"{review_id}.json"

    try:
        resolved_path = file_path.resolve()
        reviews_dir_resolved = reviews_dir.resolve()
        if not resolved_path.is_relative_to(reviews_dir_resolved):
            return {"error": "Invalid review_id: path traversal detected"}
    except (ValueError, OSError):
        return {"error": "Invalid review_id"}

    if not file_path.exists():
        return {"error": f"Review {review_id} not found"}

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError:
        return {"error": "Review record is corrupted"}
