# Council of Translation

Council of Translation V0.4 is a Goose-first, review-only MCP server for structured localization QA. It reviews a source/candidate pair, returns a compact chief-editor decision, and stores a retrievable structured trace. It never translates files or applies edits: the caller supplies relevant terminology, style, project, and technical context and owns the final edit.

## Public MCP tools

The normal tool surface is frozen to exactly five tools:

- `review_translation(...)` starts a V2 review.
- `continue_review(review_id, user_decisions, ...)` creates a linked immutable revision and reconsiders only affected roles.
- `view_review_record(review_id, detail_level="full")` reads V2 records and legacy V1 records.
- `list_review_records(...)` returns bounded, privacy-safe record metadata.
- `get_server_info()` reports version, defaults, budgets, and build diagnostics.

The defaults are `output_mode="review_only"`, `interactive_mode="auto"`, `decision_fallback="council_adjudication"`, `trace_level="summary"`, and `history_mode="full"`. Only explicit `output_mode="full_rewrite"` permits a full suggested translation.

## Review flow

```text
deterministic preflight
  -> role-routed independent reviews
  -> issue clustering
  -> optional single bounded discussion round
  -> optional one-form user decision (maximum three points)
  -> affected-role reconsideration
  -> Policy Gate
  -> evidence-weighted chief-editor adjudication
```

User choices are decisive only among valid options. They cannot override placeholder or markup integrity, semantic correctness, deterministically checked caller hard rules, or critical blockers. Unsupported, declined, cancelled, malformed, and non-interactive elicitation paths terminate through explicit fallback or `RETURNED_PENDING`; they do not hang. `return_pending` requires `history_mode="full"`, and the compact pending response contains its DecisionPoints. Fallback uses an evidence-weighted Position Matrix, never raw vote counts.

Maximum sampling budgets are 6 calls for `lightweight`, 10 for `standard`, and 14 for `strict`. Clean input does not manufacture discussion or DecisionPoints.

## Persistence and privacy

Records use stable sortable V2 IDs and atomic writes under the platform data directory (or `COUNCIL_REVIEWS_DIR` when explicitly configured). `history_mode` supports:

- `full`: complete structured trace;
- `metadata`: allowlisted metadata only—no source, candidate, TB/SG packets, model text, or user free text;
- `off`: no write.

Readers check V2 storage first and can read legacy V1 JSON records. Missing `schema_version` is interpreted as V1.

## Development

```powershell
uv sync --locked --group dev
uv run council_of_translation
python -m compileall src tests
$env:PYTHONPATH='src'; python -m pytest -q
```

The package also exposes the `mcp_council_of_translation` command alias. See [V0.4 architecture](docs/v0.4-architecture.md) and [tool and data contract](docs/v0.4-tool-contract.md).
