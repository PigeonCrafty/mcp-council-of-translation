# Live Gate Review: CAMPAIGN-012 Q-014

## Decision

`CHANGES_REQUESTED`

V0.12.0 passed the translation-review, routing, coverage, budget, privacy-safe Markdown
and terminal-coherence portions of all three normal-Goose cases. It did not satisfy the
central Q-014 requirement that a normal Goose agent receive and reproduce the canonical
`verification_receipt` object without reconstruction. The failure is bounded to the
verification result's client-visible text transport and does not invalidate the accepted
receipt projector, persisted record, ordinary report or Council adjudication evidence.

## Evidence admitted

- Case A: `20260824T095456034110Z_514515745f1b`
- Case B: `20260824T095527488257Z_6de232ca08b6`
- Case C: `20260824T095612817693Z_6928cdb00539`
- Published server: package/module `0.12.0`, build
  `verifiable-evidence-council-v10`, record Schema `2.5`, receipt Schema `1.0`
- Runtime boundary: unchanged normal Goose extension and provider/model across cases
- Retry/provider failures: none reported

The final pasted Case C block repeated Case A's review ID and lightweight report. It is
not admitted as a distinct Case C result. The immediately preceding complete strict
submission for `20260824T095612817693Z_6928cdb00539` is admitted instead; it contains
the strict normal report and verification Markdown needed for the findings below.

## Passing evidence

### Case A — lightweight clean control

- Correct canonical route, reason codes and ordered four-role portfolio.
- Four structured successes, full coverage, zero unavailable reviewers.
- Calls/budget/elicitation are exactly `4/6/0`.
- No blockers, issues, degradation, warnings or fallback.
- Chief and terminal are exactly `可发布 / 否`, once, last and coherent.
- Verification availability reports complete with zero missing/redacted fields.

### Case B — standard material-edit disposition

- Correct standard legal-risk route, reason codes and ordered six-role portfolio.
- Six structured successes, full coverage, zero unavailable reviewers.
- Calls/budget/elicitation are exactly `7/13/0`.
- The normal report preserves precision, selected-partner scope and withdrawal-right
  reversal without inventing statutes or legal advice.
- Chief and terminal are exactly `修改后可发布 / 否`, once, last and coherent.
- Verification availability reports complete.

### Case C — strict blocker plus semantic issue

- Correct strict legal-risk route, reason codes and ordered seven-role portfolio.
- Seven structured successes, full coverage, zero unavailable reviewers.
- Calls/budget/elicitation are exactly `8/18/0`.
- Missing `{terms_url}` is a deterministic blocker through three recorded failed check
  kinds, while authorization-scope expansion remains a separate material issue.
- Chief and terminal are exactly `需人工复核 / 是`, once, last and coherent.
- Verification availability reports complete.

## Failed acceptance criterion

Normal Goose did not expose the MCP `structuredContent` object to the agent:

- Case A stated that no separate JSON node was available and returned only the Markdown
  projection, while incorrectly reporting `missing field: none`.
- Case C likewise returned only the Markdown projection and no canonical JSON object.
- Case B constructed a new JSON object from Markdown. Its top-level keys are
  `receipt_version`, `record_version`, `runtime_server_info`, `active_role_ids`,
  `sampling`, `calls`, `timing_ms`, `concurrency`, `process_status`, `chief_editor` and
  `terminal_disposition_check`. These are not the frozen canonical fields
  `receipt_schema_version`, `record`, `serving`, `routing.active_role_ids`,
  `reviewer_execution`, `runtime`, `outcome` and `coherence`.
- Case B also renamed `diagnostic_build` to `git_commit` and replaced the canonical
  availability lists with derived counts. Therefore its claimed JSON is a model-created
  reconstruction, not server evidence.

The implementation currently places the canonical receipt only in FastMCP
`structured_content`; its sole `TextContent` contains the human Markdown projection.
FastMCP in-process tests prove the structured channel exists, but normal Goose in this
environment supplies only the text channel to the model. Q-014 explicitly requires
normal-Goose access and therefore cannot accept an in-process-only channel.

## Required correction

Issue CAMPAIGN-012-r4 as a two-package patch release:

1. Keep the existing structured receipt byte/semantically unchanged, but append one
   compact, parseable, canonical JSON serialization of that exact object to the same
   verification `TextContent` after the human receipt. Do not rely on a second content
   block or client support for `structuredContent`.
2. Preserve the five verification headings by using a non-heading delimiter and fenced
   JSON. Preserve ordinary `review_translation`, `continue_review`, `full` and `summary`
   text byte-for-byte.
3. Bound the combined verification text independently, prove hostile receipt payloads
   remain privacy-safe and parseable, and prove the JSON text parses equal to
   `structured_content["verification_receipt"]`.
4. Release package/module `0.12.1` and build
   `verifiable-evidence-council-v10.1`; keep record Schema `2.5`, receipt Schema `1.0`,
   five tools, budgets 6/13/18 and concurrency behavior unchanged.

## Acceptance state

- F-053 through F-057 remain accepted; their deterministic server-side evidence is not
  invalidated.
- F-058 is added as the bounded normal-Goose text-channel receipt fallback and remains
  planned until CAMPAIGN-012-r4 passes Foreman review.
- Q-014 remains unaccepted and requires a fresh post-publication revalidation after the
  correction is accepted and published.
