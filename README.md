# Council of Translation

Council of Translation V0.13.1 is a Goose-first, review-only MCP server for context-coherent localization QA. It reviews a source/candidate pair, returns a concise Council report as the primary MCP text, and retains the complete existing dictionary as structured content. It never translates files or applies edits: the caller supplies relevant terminology, style, project, and technical context and owns the final edit.

## Public MCP tools

The normal tool surface is frozen to exactly five tools:

- `review_translation(...)` starts a V2 review.
- `continue_review(review_id, user_decisions, ...)` creates a linked immutable revision and reconsiders only affected roles.
- `view_review_record(review_id, detail_level="full")` reads V2 records and legacy V1 records; `detail_level` accepts `full`, `summary`, or the opt-in `verification` evidence view.
- `list_review_records(...)` returns bounded, privacy-safe record metadata.
- `get_server_info()` reports version, defaults, budgets, and build diagnostics.

The defaults are `output_mode="review_only"`, `interactive_mode="auto"`, `briefing_mode="auto"`, `decision_fallback="council_adjudication"`, `trace_level="summary"`, and `history_mode="full"`. `briefing_mode` also accepts `always` and `off`. Only explicit `output_mode="full_rewrite"` permits a full suggested translation.

## Review flow

```text
sampling-free briefing gate
  -> deterministic preflight
  -> role-routed independent reviews (bounded concurrency, default 3)
  -> optional one-form context follow-up (maximum two questions)
  -> affected-role context reconsideration
  -> issue clustering
  -> optional single bounded discussion round
  -> optional one-form user decision (maximum three points)
  -> affected-role outcome reconsideration
  -> Policy Gate
  -> evidence-weighted chief-editor adjudication
  -> deterministic Council value projection
  -> process-first digest and bounded display report
```

User choices are decisive only among valid outcomes. Reviewers classify findings as issues, concrete choices, or affirmations; action prose remains advice and is never used as a selectable value. A DecisionPoint appears only when at least two materially distinct valid local outcomes remain. A consistent bounded `candidate_span` supplies the issue-local current outcome; the whole candidate document is never used as an option label. The single standard Goose form batches at most three questions and normally has one submit button for the entire batch. Each field exposes at most four readable enum values (for example `保留：继续`, `改为：下一步`, and `暂不决定，由 Council 裁决`) which map per field to exact internal options. Internal option IDs and hash surrogates are not displayed.

Explicit Council delegation is a valid choice, not an interaction failure: the existing evidence-weighted Position Matrix adjudicates that point. Unsupported, declined, cancelled, malformed, stale, and non-interactive paths remain distinct and terminate through explicit fallback or `RETURNED_PENDING`; they do not hang. Each proposed local replacement is applied only at one provable candidate anchor, then deterministic checks run against the reconstructed complete candidate. Missing or repeated anchors suppress the affected decision with content-free Policy Gate provenance, `decision_suppressed:<reason>` warning, and truthful degraded fallback status; unrelated protected material elsewhere is preserved. A normal deterministic rejection such as placeholder loss is not reported as runtime degradation. Choices cannot override placeholder or markup integrity, semantic correctness, deterministically checked caller hard rules, or critical blockers. `return_pending` requires `history_mode="full"`, and the compact pending response contains its DecisionPoints. Raw vote counts are never authoritative.

Within an issue, duplicate or synonymous proposals collapse to one outcome, and repeated findings do not multiply a reviewer's Position Matrix influence. Only roles contrary to the selected outcome (or materially affected by it) are reconsidered; supporting roles are not sampled merely for agreeing. Requested, completed, skipped, and failed roles are recorded separately. Missing budget or a reconsideration failure sets `degraded=true`, emits bounded warnings, and returns a non-clean status. Reviewer sampling coverage is explicit and semantic, not merely syntactic JSON decoding: success requires string `role_feedback`, list `findings`, and safely validated finding objects. Valid clean/affirming reviewers count as coverage without manufacturing issues or checklist work. Partial or zero coverage conservatively returns `NEEDS_HUMAN_REVIEW`.

Source/candidate-only calls in `briefing_mode=auto` request a concise background form before sampling; rich caller context skips it, `always` requires it, and `off` proceeds with explicit assumptions. Reviewer envelopes may propose bounded material context gaps. Core recognizes outcome-changing usage, brand/UI and binding glossary/reference questions, deduplicates them, asks at most two in one follow-up, and reconsiders only affected active roles after real answers. An assumption, decline, cancel, unsupported, malformed or error leaves selected material context unresolved: no outcome form opens, confidence falls, and the result requires human review. Briefing, context, and outcome interactions have separate telemetry, as do context and outcome reconsideration provenance.

Maximum sampling budgets are 6 calls for `lightweight`, 13 for `standard`, and 18 for `strict`. A deep standard path fits six independent reviews, three context reconsiderations, one discussion, and three outcome reconsiderations exactly within 13. Clean input does not manufacture discussion or DecisionPoints.

V0.11 routes through one of 15 fixed content/mode profiles. Existing non-legal portfolios remain frozen. Explicit `content_type="legal_risk"` selects exactly four reviewers in lightweight mode (fidelity, terminology, risk/ambiguity, fluency), six in standard mode (adding product-context and UX-copy), and seven in strict mode (adding technical safety). Routing uses only normalized content type and mode—never free source, candidate, context, audience, or notes prose—and adds no model or interaction calls. New records expose bounded `routing_profile` and `routing_reason_codes`; older V2 records receive conservative unrecorded-routing defaults.

Only the independent reviewer phase runs concurrently. `COUNCIL_REVIEW_CONCURRENCY`
accepts the literal values `1`, `2`, or `3`; missing configuration defaults to `3`,
while empty, non-numeric, or out-of-range values safely use sequential execution and
record `invalid_fallback`. The full independent role count is reserved against the
sampling budget before launch, every role is attempted exactly once, results are
correlated back to plan order, and all interaction, reconsideration, discussion,
Policy Gate, adjudication, digest, and persistence phases wait for the batch to settle.
`get_server_info()` exposes the effective limit, maximum `3`, and disposition without
exposing raw environment values.

## Persistence and privacy

Records use stable sortable V2 IDs and atomic writes under the platform data directory (or `COUNCIL_REVIEWS_DIR` when explicitly configured). `history_mode` supports:

- `full`: complete structured trace;
- `metadata`: allowlisted metadata only—no source, candidate, TB/SG packets, model/user/chief prose, or free text; safe status, publishability, and review-needed disposition are retained;
- `off`: no write.

New records use schema `2.6`. They retain bounded routing provenance, `council_value_metrics`, content-free wall-time and concurrency telemetry, and add a deterministic `decision_support` assessment for the chief disposition. Its categorical level is `well_supported`, `supported_with_limits`, or `insufficient`; it is not a probability, score, vote, or reviewer-confidence average. Context confidence describes the input brief, reviewer coverage describes which planned roles returned valid envelopes, decision support describes the structured basis for the current disposition, and publishability remains the chief editor's operational outcome. Only `insufficient` can tighten a permissive outcome to `需人工复核 / 是`; no level can relax Policy Gate, blockers or valid user authority. Readers also accept V2.5 through V2.0 and legacy V1 records, which expose decision support as `not_recorded` rather than inferring history.

`review_translation`, `continue_review`, and `view_review_record` return two MCP channels. The first text block has exactly five Chinese sections in this order: `审校背景`, `Council 新增视角`, `角色覆盖与分工`, `共识、分歧与盲区`, and `主编结论`. Unique material perspectives precede corroboration and confirmation-only coverage; every active role is accounted for once and confirmation-only roles share one coverage line. The primary-only human work-item projection joins deterministic checks and reviewer corroboration through bounded protected anchors plus check provenance, translates known check failures into natural Chinese, and groups model-only cross-category findings only when exact source/candidate anchors and the concrete replacement agree. Different literals, structural-loss families, semantic repairs and genuinely different replacement actions remain separate; distinct material consequences remain readable once. This projection never mutates the complete checklist, raw clusters, value metrics or other structured evidence. Discussion value appears only when a discussion occurred, and the final editor disposition remains last. Clean reference output targets 1,200 Unicode code points or fewer; every primary report is capped at 3,200. Canonical adjudication counters and redundant evidence for clean roles are omitted from primary text, while blockers, material evidence, minority conditions, context or coverage gaps, warnings and degradation remain visible. Optional role evidence is shown whole or omitted whole. The complete compact or full dictionary—including chief rationale, RoleLens evidence, `council_value_metrics`, structured `process_digest`, status, warnings and retrieval metadata—remains in structured content. `list_review_records` and `get_server_info` retain their structured-only responses.

Use `view_review_record(review_id, detail_level="full")` to inspect full structured evidence when `history_mode="full"`; no hidden chain-of-thought is requested or stored. The first normal review response is already suitable for user presentation, so a second history lookup is not required just to obtain the concise Council report.

Use `detail_level="verification"` only when a client needs a deterministic, privacy-safe technical receipt. It retains the canonical receipt with receipt schema `1.1` in structured content and appends the exact same compact, UTF-8-safe JSON object after the five-section Markdown and review footer in the first text block. Receipt 1.1 adds the exact recorded decision-support assessment; historical unavailable facts remain `null` with explicit availability provenance. Retrieval does not return raw record content, persist a receipt, sample reviewers, elicit input, or replace the normal process-first Council report.

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

For Q-010 after publication, replace `<reviewed-commit>` above with the exact accepted commit and run two pinned normal-user recipes. First, review a clean marketing slogan with explicit brand usage and any binding glossary/reference; expect the six marketing lenses in frozen order and a normal outcome only after context is sufficient. Second, deliberately combine marketing with functional-button context and omit whether the text is a slogan or UI action; expect the Council to ask that material question first, and if it remains unanswered, open no wording form and require human review. Audit literal structured JSON for role IDs, sample statuses, coverage and call counts; do not treat an outer agent's prose reconstruction as telemetry truth.

The pinned build reports version `0.13.1`, schema `2.6`, verification receipt schema `1.1`, evaluator schema `2.1`, diagnostic build `truthful-boundaries-council-v11.1`, and budgets 6/13/18. V0.13.1 treats input beyond the 12,000-character review prefix and unavailable discussion envelopes as incomplete evidence requiring human review; it also minimizes legacy V1 summaries without changing their full or verification views.
