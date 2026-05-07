from fastmcp import FastMCP

INSTRUCTIONS = """
Council of Translation is an MCP server for multi-agent localization translation review.

This repository is being adapted from a general council deliberation server into a localization-focused council. The inherited debate workflow is still present during the transition, but the product direction is to support structured translation tasks, reviewer agents, and chief editor decisions.

## What it does
The target workflow will:
1. Accept source text, candidate translation, content type, context, audience, terminology, and constraints
2. Route the task through specialized localization reviewers
3. Produce structured review findings, recommended revisions, and a chief editor decision

**Key Feature**: Translation decisions should be traceable to role-specific findings rather than a generic summary.

## When to use this server
Use Council of Translation when you need:
- Multi-role review of localized product copy
- Checks for fidelity, fluency, terminology, product context, UX, brand voice, placeholders, and risk
- A final editor decision with rationale and optional alternatives
- Reusable translation review records

## Target Localization Roles
- Fidelity reviewer
- Fluency reviewer
- Terminology reviewer
- Product context reviewer
- UX copy reviewer
- Brand voice reviewer
- Technical safety reviewer
- Risk and ambiguity reviewer
- Chief editor
- Optional draft translator

## Available Tools

### Transitional Debate Workflow (inherited, to be replaced)
1. **start_council_debate(prompt)** - Initiates a new debate on your topic
   - All 9 members each generate an opinion via LLM sampling
   - Returns formatted text showing ALL individual opinions with member names and perspectives
   - Each member's unique viewpoint is preserved and displayed separately

2. **conduct_voting()** - Members vote on opinions (must run after start_council_debate)
   - Each member votes for opinions aligning with their values
   - Members cannot vote for their own opinion
   - Returns detailed vote information including who voted for whom with reasoning
   - Agents can see individual voting decisions and rationale

3. **get_results()** - Generates final results (must run after conduct_voting)
   - **Shows ALL 9 individual opinions** from each council member with vote counts
   - Highlights winning opinion(s)
   - **Displays ALL individual votes**: see exactly who voted for whom
   - Includes detailed reasoning from each member explaining their vote
   - AI-synthesized summary incorporating all perspectives
   - Saves debate to history

### History & Status Tools
- **list_past_debates()** - View all historical debates with metadata
- **view_debate(debate_id)** - Retrieve complete data for a specific past debate
  - Includes all opinions, individual votes, and results
  - Full vote breakdown showing each member's vote and reasoning
- **get_current_debate_status()** - Check the status of the current active debate

## Typical Usage Pattern

For a new debate:
1. Call start_council_debate("Should we implement feature X?")
2. Call conduct_voting()
3. Call get_results()

To reference past debates:
1. Call list_past_debates() to see available debates
2. Call view_debate(debate_id) to see specific debate details

## Important Notes
- This is the first rename and cleanup step toward the localization council design in `mydocs/`
- Only one debate can be active at a time
- Must complete the full workflow (start → vote → results) before starting a new debate
- Each complete debate makes ~28 LLM calls (9 opinions + 9 votes + 9 reasoning + 1 synthesis)
- All debates are automatically saved to history when get_results() is called
- **Full voting transparency**: All individual votes and reasoning are visible to agents
  - See exactly which members voted for which opinions
  - Access each member's reasoning for their vote choice
- The council provides balanced perspectives, not definitive answers
- Results include both democratic voting outcomes and AI synthesis for comprehensive insight
"""

mcp = FastMCP(name="council-of-translation", instructions=INSTRUCTIONS)

from council_of_translation import tools  # noqa: F401, E402
from council_of_translation import prompts  # noqa: F401, E402


def main():
    mcp.run()

if __name__ == "__main__":
    main()
