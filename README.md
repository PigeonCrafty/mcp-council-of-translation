# Council-of-Translation

Council-of-Translation is an MCP server for multi-agent localization translation review.

The project is being adapted from a general council-style deliberation server into a structured localization workflow. The target design is defined in `mydocs/` and centers on:

- role-based translation review
- consistent structured inputs and outputs
- terminology, style, context, placeholder, and risk checks
- a chief editor agent that makes traceable final translation decisions
- lightweight, standard, and strict review modes

## Product Direction

The localization council is designed to review or generate translations through specialized roles:

- fidelity reviewer
- fluency reviewer
- terminology reviewer
- product context reviewer
- UX copy reviewer
- brand voice reviewer
- technical safety reviewer
- risk and ambiguity reviewer
- chief editor
- optional draft translator

The next implementation steps should replace the inherited generic debate and voting workflow with translation-specific tasks, schemas, prompts, and orchestration.

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

- `mydocs/localization-council-role-system-design.zh-CN.txt`
- `mydocs/localization-council-prompt-agent-spec.zh-CN.txt`
