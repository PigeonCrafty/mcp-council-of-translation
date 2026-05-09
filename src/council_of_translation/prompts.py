from council_of_translation.server import mcp

@mcp.prompt()
def review_translation_prompt(
    source_text: str,
    candidate_translation: str,
    target_language: str = "zh-CN",
    mode: str = "standard",
) -> str:
    """
    Prepare a Council of Translation review for a candidate translation.

    Args:
        source_text: Source text.
        candidate_translation: Candidate translation to review.
        target_language: Target locale/language.
        mode: Review depth: lightweight, standard, or strict.
    """
    return f"""Call review_translation with this candidate translation.

source_text:
{source_text}

candidate_translation:
{candidate_translation}

target_language:
{target_language}

mode:
{mode}

Before calling the tool, include any relevant TB, SG, project rules, placeholders, do-not-translate items, context, and known exceptions you have for this segment."""


@mcp.prompt()
def strict_translation_review_prompt(source_text: str, candidate_translation: str) -> str:
    """
    Prepare a strict Council review for high-risk or high-visibility localized text.

    Args:
        source_text: Source text.
        candidate_translation: Candidate translation to review.
    """
    return f"""Call review_translation in strict mode for this high-risk or high-visibility text.

source_text:
{source_text}

candidate_translation:
{candidate_translation}

mode:
strict

Pass all relevant context, TB/SG/project rules, brand guidelines, technical constraints, reference translations, and known exceptions. The Council should return review findings and a chief editor recommendation only; the caller applies any changes."""


@mcp.prompt()
def council_help() -> str:
    """
    Learn how to use the Council of Translation server.
    """
    return """Council of Translation is a review-only MCP server for localization QA.

Main tool:
- review_translation(...)

Required:
- source_text
- candidate_translation

Recommended context:
- content_type
- context
- audience
- term_glossary
- style_guide
- project_rules
- brand_guidelines
- technical_constraints
- reference_translations
- known_exceptions

Modes:
- lightweight: short low-risk strings
- standard: normal product localization
- strict: high-risk or high-visibility content

Output modes:
- review_only: default; final review advice only, no full rewritten translation
- with_snippets: includes limited local examples
- full_rewrite: only when explicitly requested

The server returns reviewer findings, chief_editor_decision.recommended_translation, and server_info. The calling agent remains responsible for applying changes.

Diagnostic note:
- get_server_info() is only for cache/version debugging. Do not call it before ordinary reviews; review_translation already includes server_info."""

