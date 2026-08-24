# Campaign Contract: CAMPAIGN-012-r4

## Control

- Harness role: `WORKER / CAMPAIGN MAIN WORKER`
- Harness mode: `STRICT_CAMPAIGN`
- Campaign: `CAMPAIGN-012-r4`
- State: `ASSIGNED`
- Repository: `C:\Users\GeZhu\MyMCP\mcp-council-of-translation`
- Exact baseline: `aceac3383b2a597bbf5414362d9b71ac6e601267`
- Parent live contract: `harness/contracts/CAMPAIGN-012-q014-live.md`
- Foreman live review: `harness/evaluations/CAMPAIGN-012-q014-live-review.md`
- Required ledger: `harness/reports/CAMPAIGN-012-r4-ledger.md`
- Required Worker report: `harness/reports/CAMPAIGN-012-r4-worker.md`
- Target package/module: `0.12.1`
- Target diagnostic build: `verifiable-evidence-council-v10.1`
- Persisted record Schema: `2.5` unchanged
- Verification receipt Schema: `1.0` unchanged
- Acceptance authority: Foreman only
- Subagent delegation: forbidden; the correction is small and shares presentation files

## Incident and objective

Published V0.12.0 correctly returns a FastMCP `ToolResult` whose
`structured_content.verification_receipt` is canonical. Its only `TextContent`, however,
contains the human Markdown receipt. Normal Goose in Q-014 exposed only that text to the
agent. Case A and C could not return JSON; Case B reconstructed a noncanonical object,
renaming and reshaping the frozen schema. In-process FastMCP dual-channel evidence is
therefore insufficient for the required normal-Goose handoff.

Implement one bounded compatibility fallback: for
`view_review_record(detail_level="verification")` only, append one compact canonical
JSON serialization of the exact `verification_receipt` to the same first
`TextContent`. Keep the structured channel unchanged. Release this correction as
V0.12.1 without changing the receipt schema, record schema, public tool count, Council
behavior or ordinary reports.

## Frozen design

The verification `TextContent` must be exactly:

1. the existing verification primary Markdown, including its existing review footer;
2. two newlines;
3. the literal non-heading label `Canonical verification_receipt JSON:`;
4. a fenced `json` block containing one compact JSON object; and
5. no prose after the closing fence.

The compact object must be serialized directly from the same in-memory receipt object
assigned to `structured_content["verification_receipt"]`, using UTF-8-safe JSON with no
ASCII escaping and compact separators. Preserve insertion order; do not sort, rename,
flatten, alias, summarize or derive fields. Parsing the fenced text must produce an
object equal to the structured receipt.

Keep the existing verification report headings exactly: `# Council 验证回执`, then
`## 记录与路由`, `## 覆盖与调用`, `## 风险与裁决`, `## 一致性与可用性`. The JSON
label is deliberately not a Markdown heading.

Freeze a combined verification-text hard cap of 12,000 Unicode code points. Canonical
JSON must never be truncated. Existing receipt validation/redaction must keep valid,
legacy, metadata and hostile receipts within the cap. If an impossible internal payload
would exceed the cap, return a bounded privacy-safe tool error rather than malformed or
partial JSON; do not mutate or save the record.

The fallback applies only when the payload contains a valid
`verification_receipt`. Ordinary review, continuation, full history, summary, list,
diagnostic and error primary text remain byte-compatible with the baseline.

## Work packages

### PKG-073 — Normal-Goose canonical text fallback

Outcome: one text-only MCP consumer can copy the canonical receipt without inspecting
`structuredContent` or reconstructing Markdown.

Authorized production paths:

- `src/council_of_translation/presentation.py`
- `src/council_of_translation/tools/review.py`
- `src/council_of_translation/localization/verification.py`

Authorized test paths:

- `tests/integration/test_v12_verification_view.py`
- `tests/integration/test_v07_dual_channel.py`
- `tests/unit/test_verification_receipt.py`

Acceptance criteria:

1. Actual registered FastMCP verification calls return one first `TextContent` with the
   unchanged Markdown receipt/footer and exactly one canonical fenced JSON object.
2. The fenced JSON parses equal to
   `result.structured_content["verification_receipt"]`; exact canonical field names,
   ordered lists, enums, nulls, counts and availability lists are preserved.
3. A Goose-shaped text-only test proves A/B/C receipts expose the canonical object
   without reading `structured_content`.
4. The baseline B-style reconstructed aliases (`receipt_version`, `calls`,
   `chief_editor`, `terminal_disposition_check`, `git_commit`) are absent unless they
   legitimately occur as data values; the server emits only frozen receipt Schema 1.0
   names.
5. Full/metadata/legacy/unavailable/continuation/hostile receipts remain privacy-safe,
   parseable and at most 12,000 code points. No raw source, candidate, reviewer/evidence
   prose, paths, credentials, environment values or internal issue IDs escape.
6. Verification retrieval remains one load, zero saves, zero sampling, zero elicitation
   and no record mutation.
7. Existing `review_translation`, `continue_review`, `view_review_record(full|summary)`,
   list, diagnostic and error text assertions remain byte-equivalent.

### PKG-074 — V0.12.1 release migration and documentation

Depends on PKG-073.

Outcome: package, docs, tests, lock and fresh artifacts truthfully identify the bounded
compatibility correction.

Authorized paths:

- `AGENTS.md`
- `README.md`
- `docs/v0.4-architecture.md`
- `docs/v0.4-tool-contract.md`
- `pyproject.toml`
- `src/council_of_translation/__init__.py`
- `tests/integration/test_tool_surface_v2.py`
- `tests/integration/test_v10_release_contract.py`
- `tests/unit/test_persistence_v2.py`
- `uv.lock`

Acceptance criteria:

1. Package/module version is `0.12.1`; diagnostic build is
   `verifiable-evidence-council-v10.1`.
2. Persisted Schema remains `2.5`, receipt Schema remains `1.0`, public tools remain
   exactly five, defaults remain review-only/auto/auto/summary/full, budgets remain
   6/13/18 and concurrency remains bounded 1..3 with default/max 3.
3. Documentation states that verification retains structured content and also embeds
   its exact compact canonical receipt in the same text channel for clients that ignore
   MCP structured content. Normal callers still call `review_translation` directly.
4. `uv.lock` changes only the editable root version from 0.12.0 to 0.12.1; lock revision
   3, package count 78 and 586 upload-time entries remain unchanged.
5. Fresh wheel and sdist are built, inspected and smoke-tested from an isolated Python
   3.12/FastMCP 3.4.7 environment. All five tools must be called; verification text and
   structured receipt equality must be proven from the installed wheel.

## Authorized complete path set

The Worker may modify only:

- `AGENTS.md`
- `README.md`
- `docs/v0.4-architecture.md`
- `docs/v0.4-tool-contract.md`
- `pyproject.toml`
- `src/council_of_translation/__init__.py`
- `src/council_of_translation/presentation.py`
- `src/council_of_translation/tools/review.py`
- `src/council_of_translation/localization/verification.py`
- `tests/integration/test_v07_dual_channel.py`
- `tests/integration/test_v12_verification_view.py`
- `tests/integration/test_tool_surface_v2.py`
- `tests/integration/test_v10_release_contract.py`
- `tests/unit/test_persistence_v2.py`
- `tests/unit/test_verification_receipt.py`
- `uv.lock`
- `harness/reports/CAMPAIGN-012-r4-ledger.md` (new, untracked/unstaged)
- `harness/reports/CAMPAIGN-012-r4-worker.md` (new, untracked/unstaged)

Any other implementation, test, documentation, dependency, workflow or Harness path is
forbidden. Stop on a required out-of-scope path rather than editing it.

## Frozen non-goals

- No new MCP tool, parameter, reviewer, route, prompt, sampling, elicitation or model
  call.
- No receipt Schema 1.1 or persisted Schema migration.
- No change to canonical receipt keys or semantics.
- No change to normal five-section Council reports, decision authority, Policy Gate,
  outcome/reconsideration behavior, persistence paths or history defaults.
- No second content block as the only fallback; Q-014 proved the client may expose only
  the first text block.
- No pretty-printed/unbounded JSON, raw full-record dump or source/candidate leakage.
- No Goose/provider/model configuration or installation change.
- No live Goose/provider/model call, push, PR, release, publication or deployment.
- No edits or traversal under `.learnings/**`, `reviews/**`, `myTest/**`, `dist/**` or
  the independent audit Markdown.

## Protected admitted state

At admission, the following Foreman assets must match exactly:

| Path | SHA-256 |
| --- | --- |
| `harness/features.json` | `50E1A1B10E0A273809F1D0CD689C57F038B73045F78138B1A4BDBF5C0ECA44DC` |
| `harness/plan.md` | `8F8D46C5ADD70E6B2259EC005EC60C7618653A8410AC14BF24ADB18804ABCDFF` |
| `harness/progress.md` | `73921F878FE5719F219B0F21A116EAB189FAF13AD44C556E763E28EEE1BFEE48` |
| `harness/contracts/CAMPAIGN-012-q014-live.md` | `87369C91AE827C7B64E8956F3CB627ABF87D7B1300AE0764658760D6D8E2B864` |
| `harness/evaluations/CAMPAIGN-012-q014-live-review.md` | `3431A480D126A596C137C08E8728227340754DAED9EC0E0D64DA84F9FB694AAD` |
| `harness/evaluations/CAMPAIGN-012-r3-publication-ci-review.md` | `CFEA7631F560AB776F5B1E08C36DF3ED75066F3E48BA601DAC923E0F27ECDC99` |
| `harness/contracts/CAMPAIGN-012-r1.md` | `E4E1CAAFB5E6E08729B5E726C5144793D3BE7E029699AA24984F37E97D587548` |
| `harness/contracts/CAMPAIGN-012-r2.md` | `1B628133452A89F1BA4F47798F124B0E07C9E25E4B994C52834D65A1FAFCB615` |
| `harness/contracts/CAMPAIGN-012-r3.md` | `E6EF7A7CC8468124E85CAA87C649141D2947D25506F6A00C6901F94487928161` |
| `harness/evaluations/CAMPAIGN-012-r1-review.md` | `F0E3F8BB0A8D16EF51602F0352C9703646658BC2993A39BB6F1AFB064A08CEA8` |
| `harness/evaluations/CAMPAIGN-012-r2-review.md` | `FD74C91C3275FDE662A49D2DAB31051876F7718857DA7239DF0376BE23B08009` |
| `harness/evaluations/CAMPAIGN-012-r3-review.md` | `9948709C712A5F39738BA7DA13692CCD818C3E27C833D9571AC835B913956415` |
| `harness/reports/CAMPAIGN-012-r1-worker.md` | `43966E75BF6348B3B144ECA8BC517516DCC499AF9238B7288B8306B7F3760ECB` |
| `harness/reports/CAMPAIGN-012-r2-worker.md` | `54746D80619E5E4C35A69CA514381F0EBECF3E6E52B0D4050024B44BCB412A44` |
| `harness/reports/CAMPAIGN-012-r3-worker.md` | `BBFA01ABAE507C7DBD1D89A93E96BBD571E934DA754BE1489C908944333652D8` |

The untracked `.learnings/**`, `reviews/**` and independent audit Markdown are user
assets. Preserve them without reading, hashing, staging or modifying them.

## Admission

Before edits:

1. Confirm exact HEAD `aceac3383b2a597bbf5414362d9b71ac6e601267` and empty index.
2. Confirm only the admitted Foreman/user dirt plus this contract exists outside tracked
   baseline state.
3. Verify every protected hash above and the SHA-256 of this contract.
4. Run `python -m compileall src tests`.
5. Run the complete existing suite and require exactly `441 passed`.
6. Record admission evidence before changing any authorized file.

Stop on baseline/hash/index drift, an unexplained test result, or a required forbidden
path.

## Execution and commits

Execute PKG-073 then PKG-074. Use exactly one scoped local commit per package. Do not
stage reports, ledgers, Foreman assets or user assets. Local Git operations only; no
remote operation is authorized. Inspect each staged name list and diff before commit.

Use repository-local temporary/cache directories when dependency tooling cannot use the
host cache. Temporary build and environment assets must be removed before handoff.

## Required verification

After PKG-073:

- compile affected production/tests;
- run all verification-view, dual-channel and receipt unit/integration tests;
- run explicit text-only A/B/C projections and canonical JSON equality checks;
- run privacy, hostile size, legacy/metadata, no-side-effect and normal-text
  compatibility controls.

After PKG-074 and at final HEAD:

1. `python -m compileall src tests`.
2. Complete test suite; no failure or skip beyond an existing explicitly justified
   environment skip.
3. Focused V0.12/V0.12.1 verification, dual-channel, release, tool-surface, persistence,
   privacy and Golden selections.
4. Exact five tools; package/module 0.12.1; build v10.1; record Schema 2.5; receipt
   Schema 1.0; defaults; budgets 6/13/18; concurrency 3/3.
5. Byte-compatibility probes for normal review, continuation, full, summary, list,
   diagnostic and error primary text.
6. One-load/zero-save/zero-sampling/zero-elicitation proof for verification retrieval.
7. Fresh wheel/sdist, archive inspection and isolated CPython 3.12/FastMCP 3.4.7 wheel
   smoke calling all five tools and proving text JSON equals structured receipt.
8. `git diff --check`, exact authorized-path audit, dead-import scan, lock invariant
   audit, protected-hash reconciliation, empty index and temporary-asset cleanup.

No prior artifact hash substitutes for the fresh V0.12.1 artifacts.

## Stop conditions

Return `BLOCKED` without guessing if exact baseline/protected hashes fail; normal Goose
would still need structuredContent to access canonical fields; preserving JSON equality
requires a receipt schema change; combined text cannot be bounded without truncation;
normal tool text changes; lock regeneration drifts beyond the root version; a required
path is unauthorized; or any live/remote/external mutation becomes necessary.

## Worker deliverables

Create but do not stage:

- `harness/reports/CAMPAIGN-012-r4-ledger.md`
- `harness/reports/CAMPAIGN-012-r4-worker.md`

The report must start with exactly `READY_FOR_REVIEW` or `BLOCKED` and include contract
hash, baseline/final HEAD, commits/path scope, package evidence, complete regression,
text-only A/B/C evidence, compatibility/privacy/purity evidence, artifact hashes, lock
invariants, protected-hash reconciliation, skipped checks, subagent count, authority and
dependency operations, live/remote call counts and remaining risks. Do not claim
Campaign acceptance, Q-014 acceptance, publication or project completion.
