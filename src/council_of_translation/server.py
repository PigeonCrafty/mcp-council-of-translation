from fastmcp import FastMCP

INSTRUCTIONS = """
Council of Translation is an MCP server for multi-agent localization translation review.

This server is review-only. It does not translate files, modify project content, or replace the caller's translation skill. A calling agent should provide the source text, candidate translation, and the relevant TB/SG/project-rule packet for the current segment. The server returns structured reviewer findings and a chief editor recommendation for the caller to apply.

## What it does
The workflow:
1. Accepts source text, candidate translation, content type, context, audience, terminology, style rules, project rules, and technical constraints
2. Routes the task through specialized localization reviewers
3. Produces structured review findings
4. Produces a chief editor decision with must-fix items, optional improvements, recommended_translation, rationale, and human-review guidance

**Key Feature**: Translation review decisions are traceable to role-specific findings rather than a generic self-check.

## When to use this server
Use Council of Translation when you need:
- Multi-role review of localized product copy
- Checks for fidelity, fluency, terminology, product context, UX, brand voice, placeholders, and risk
- A chief editor recommendation with rationale and optional alternatives
- Reusable translation review records that the caller can apply outside this MCP server

## Localization Roles
- Fidelity reviewer
- Fluency reviewer
- Terminology reviewer
- Product context reviewer
- UX copy reviewer
- Brand voice reviewer
- Technical safety reviewer
- Risk and ambiguity reviewer
- Chief editor

## Available Tools

### Translation Review Workflow
1. **review_translation(...)**
   - Main review-only tool
   - Default tool for translation quality review; call this directly for normal use
   - Requires source_text and candidate_translation
   - Accepts relevant term_glossary, style_guide, project_rules, brand_guidelines, technical_constraints, reference_translations, known_exceptions, and notes
   - Supports mode: lightweight, standard, strict
   - Uses MCP sampling internally to ask reviewer roles and chief_editor
   - Returns structured review report plus server_info diagnostics; the caller decides whether and how to apply recommendations

2. **get_server_info()**
   - Diagnostic-only tool for cache/version checks
   - Do not call before normal reviews; review_translation already includes server_info

3. **list_review_records()**
   - Lists saved localization review records from reviews/

4. **view_review_record(review_id)**
   - Retrieves a complete saved review record by ID

## Typical Usage Pattern

For a translation review:
1. The outer translation agent generates or receives a candidate translation
2. The outer agent retrieves only the relevant TB/SG/project rules for the current segment
3. Call review_translation(...)
4. Read reviews, chief_editor_decision, and optional server_info
5. The outer agent applies or ignores the recommendation according to project context

Use lightweight mode for low-risk short UI strings, standard mode for normal product localization, and strict mode for high-exposure or risky content.

## Important Notes
- This server depends on MCP sampling support from the host client.
- The server does not own full TB/SG context. The caller should pass the relevant rule packet.
- Explicit project rules, TB, SG, and known exceptions take priority over generic reviewer preferences.
- Review records are automatically saved to reviews/.
- The chief editor returns a recommendation, not a file modification.
"""

mcp = FastMCP(name="council-of-translation", instructions=INSTRUCTIONS)

from council_of_translation import tools  # noqa: F401, E402
from council_of_translation import prompts  # noqa: F401, E402


def main():
    mcp.run()

if __name__ == "__main__":
    main()
