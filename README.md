# Council of Translation

Council of Translation V0.5 is a Goose-first, review-only MCP server for structured localization QA. It reviews a source/candidate pair, returns a compact chief-editor decision, and stores a retrievable structured trace. It never translates files or applies edits: the caller supplies relevant terminology, style, project, and technical context and owns the final edit.

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

User choices are decisive only among valid outcomes. Reviewers classify findings as issues, concrete choices, or affirmations; action prose remains advice and is never used as a selectable value. A DecisionPoint appears only when at least two materially distinct valid local outcomes remain. A consistent bounded `candidate_span` supplies the issue-local current outcome; the whole candidate document is never used as an option label. The single standard Goose form batches at most three questions and normally has one submit button for the entire batch. Each field exposes at most four readable enum values (for example `保留：继续`, `改为：下一步`, and `暂不决定，由 Council 裁决`) which map per field to exact internal options. Internal option IDs and hash surrogates are not displayed.

Explicit Council delegation is a valid choice, not an interaction failure: the existing evidence-weighted Position Matrix adjudicates that point. Unsupported, declined, cancelled, malformed, stale, and non-interactive paths remain distinct and terminate through explicit fallback or `RETURNED_PENDING`; they do not hang. Each proposed local replacement is applied only at one provable candidate anchor, then deterministic checks run against the reconstructed complete candidate. Missing or repeated anchors are rejected conservatively; unrelated protected material elsewhere is preserved. Choices cannot override placeholder or markup integrity, semantic correctness, deterministically checked caller hard rules, or critical blockers. `return_pending` requires `history_mode="full"`, and the compact pending response contains its DecisionPoints. Raw vote counts are never authoritative.

Within an issue, duplicate or synonymous proposals collapse to one outcome, and repeated findings do not multiply a reviewer's Position Matrix influence. Only roles contrary to the selected outcome (or materially affected by it) are reconsidered; supporting roles are not sampled merely for agreeing. Requested, completed, skipped, and failed roles are recorded separately. Missing budget or a reconsideration failure sets `degraded=true`, emits bounded warnings, and returns a non-clean status. Reviewer sampling coverage is explicit and semantic, not merely syntactic JSON decoding: success requires string `role_feedback`, list `findings`, and safely validated finding objects. Valid clean/affirming reviewers count as coverage without manufacturing issues or checklist work. Partial or zero coverage conservatively returns `NEEDS_HUMAN_REVIEW`.

Maximum sampling budgets are 6 calls for `lightweight`, 10 for `standard`, and 14 for `strict`. Clean input does not manufacture discussion or DecisionPoints.

## Persistence and privacy

Records use stable sortable V2 IDs and atomic writes under the platform data directory (or `COUNCIL_REVIEWS_DIR` when explicitly configured). `history_mode` supports:

- `full`: complete structured trace;
- `metadata`: allowlisted metadata only—no source, candidate, TB/SG packets, model/user/chief prose, or free text; safe status, publishability, and review-needed disposition are retained;
- `off`: no write.

New records use schema `2.1`. Readers also accept V2.0 and legacy V1 JSON records; missing `schema_version` is interpreted as V1.

The compact response includes `effective_task`, `deliberation_summary`, `degraded`, `warnings`, the review ID, and a retrieval hint. Use `view_review_record(review_id, detail_level="full")` to inspect full structured evidence when `history_mode="full"`; no hidden chain-of-thought is requested or stored.

## Development

```powershell
uv sync --locked --group dev
uv run council_of_translation
python -m compileall src tests
$env:PYTHONPATH='src'; python -m pytest -q
```

The package also exposes the `mcp_council_of_translation` command alias. See the [architecture](docs/v0.4-architecture.md) and [tool and data contract](docs/v0.4-tool-contract.md).

For a fresh Goose test, pin the reviewed local commit so cached installs cannot mask the build under test:

```powershell
uvx --refresh --from git+https://github.com/PigeonCrafty/mcp-council-of-translation@<reviewed-commit> mcp_council_of_translation
```

Call `get_server_info()` and verify version `0.5.0`, schema `2.1`, and diagnostic build `outcome-first-decision-v3` before interpreting the result.
