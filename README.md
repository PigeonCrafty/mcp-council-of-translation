# Council-of-Translation

Council-of-Translation is an MCP server for multi-agent localization translation review.

The project is being adapted from a general council-style deliberation server into a structured localization review workflow. The target design is defined in `docs/` and centers on:

- role-based translation review
- consistent structured inputs and outputs
- terminology, style, context, placeholder, and risk checks
- a chief editor agent that makes traceable review recommendations
- lightweight, standard, and strict review modes

## Product Direction

The localization council is designed to review candidate translations through specialized roles:

- fidelity reviewer
- fluency reviewer
- terminology reviewer
- product context reviewer
- UX copy reviewer
- brand voice reviewer
- technical safety reviewer
- risk and ambiguity reviewer
- chief editor

Council-of-Translation is review-only. It does not modify files, replace an outer translation skill, or own the full TB/SG/project-rule context. The calling agent should pass only the relevant rule packet for the current segment, then decide how to apply the returned recommendations.

## Main MCP Tools

- `review_translation(...)`: reviews a candidate translation and returns role-specific findings plus `chief_editor_decision.recommended_translation`.
- `list_review_records()`: lists saved review records.
- `view_review_record(review_id)`: returns a full saved review record.

Typical flow:

```text
outer translation skill produces candidate translation
-> outer agent retrieves relevant TB / SG / project rules
-> review_translation(...)
-> Council returns structured review report
-> outer agent applies or ignores recommendations
```

## Development

Install dependencies:

```bash
uv sync
```

Run the MCP server:

```bash
uv run council_of_translation
```

The package also provides the MCP-style command alias:

```bash
uv run mcp_council_of_translation
```

Run directly from GitHub:

```bash
uvx --from git+https://github.com/PigeonCrafty/Council-of-Translation mcp_council_of_translation
```

Run tests:

```bash
PYTHONPATH=src uv run pytest tests/
```

## Design Docs

The active product and role design lives in:

- `docs/localization-council-role-system-design.zh-CN.txt`
- `docs/localization-council-prompt-agent-spec.zh-CN.txt`
