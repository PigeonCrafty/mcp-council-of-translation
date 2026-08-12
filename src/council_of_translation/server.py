from fastmcp import FastMCP


INSTRUCTIONS = """
Council of Translation V0.7.1 is a review-only MCP server for guided structured
localization translation QA. It never edits translation files and does not own
translation memory, terminology/style-guide retrieval, project context, or final
edit application; the calling agent supplies the relevant packet and applies the
chief-editor checklist.

The default workflow adds a sampling-free briefing gate before deterministic
technical preflight and role-routed independent review. Material missing context
may trigger one two-question follow-up and affected-role context reconsideration.
Outcome-centric clustering, at most one targeted discussion round, one batched
interaction for at most three valid choices, separate outcome reconsideration,
a Policy Gate, and evidence-weighted
chief-editor adjudication. Form fields show bounded outcome labels through safe
values and include explicit Council delegation. User choices are decisive only
among valid options. Technical
integrity, semantic correctness, explicit hard rules, and critical blockers are
not overridden by preference. Fallback adjudication uses a Position Matrix, not
literal majority voting.

Normal responses are compact and default to output_mode=review_only,
briefing_mode=auto, interactive_mode=auto, trace_level=summary, and history_mode=full. Full structured
records contain claims, evidence, positions, decisions, and changes—not hidden
reasoning—and are available through view_review_record. Compact responses expose
effective task context, a process-first digest, an adaptive Chinese display report
with at most five sections, degradation, and warnings. The final editor disposition
is always the last substantive line.

For review_translation, continue_review, and view_review_record, present the first
primary Council text block directly to the user before optional structured diagnostics.
It already contains six role lenses, consensus or uncertainty, material risks and the
final disposition without procedural adjudication counters or redundant clean-role
evidence; do not require a second history lookup merely to show the review. The same
result retains the complete compact or full dictionary as
structured content for programmatic consumers.

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
