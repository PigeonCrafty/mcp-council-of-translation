from fastmcp import FastMCP


INSTRUCTIONS = """
Council of Translation V0.5 is a review-only MCP server for structured
localization translation QA. It never edits translation files and does not own
translation memory, terminology/style-guide retrieval, project context, or final
edit application; the calling agent supplies the relevant packet and applies the
chief-editor checklist.

The default workflow performs deterministic technical preflight, role-routed
independent review, outcome-centric clustering, at most one targeted discussion
round, one batched user interaction for at most three meaningful valid choices,
contrary/affected-role reconsideration, a Policy Gate, and evidence-weighted
chief-editor adjudication. Form fields show bounded outcome labels through safe
values and include explicit Council delegation. User choices are decisive only
among valid options. Technical
integrity, semantic correctness, explicit hard rules, and critical blockers are
not overridden by preference. Fallback adjudication uses a Position Matrix, not
literal majority voting.

Normal responses are compact and default to output_mode=review_only,
interactive_mode=auto, trace_level=summary, and history_mode=full. Full structured
records contain claims, evidence, positions, decisions, and changes—not hidden
reasoning—and are available through view_review_record. Compact responses expose
effective task context, a bounded deliberation summary, degradation, and warnings.

The public tool surface is frozen to exactly:
1. review_translation — run a new review.
2. continue_review — create a linked immutable revision from user decisions.
3. view_review_record — retrieve V1/V2 full or summary history.
4. list_review_records — list privacy-safe metadata.
5. get_server_info — diagnose version, capabilities, and budgets.
"""


mcp = FastMCP(name="council-of-translation", instructions=INSTRUCTIONS)

from council_of_translation import tools  # noqa: F401, E402
from council_of_translation import prompts  # noqa: F401, E402


def main() -> None:
    mcp.run()


if __name__ == "__main__":
    main()
