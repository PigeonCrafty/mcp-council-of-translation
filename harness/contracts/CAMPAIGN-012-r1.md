# Campaign Contract: CAMPAIGN-012-r1

## Control

- Harness role: `MAIN WORKER`
- Harness mode: `STRICT_CAMPAIGN`
- Campaign: `CAMPAIGN-012-r1`
- State: `ASSIGNED`
- Repository: `C:\Users\GeZhu\MyMCP\mcp-council-of-translation`
- Baseline commit: `6544d41d308f9ed7ab253dac5a70a94581cd04d8`
- Product target: `0.12.0`
- Diagnostic build target: `verifiable-evidence-council-v10`
- Persisted Review Schema: frozen at `2.5`
- Verification receipt schema: `1.0`
- Acceptance authority: Foreman only
- Execution ledger: `harness/reports/CAMPAIGN-012-r1-ledger.md`
- Worker report: `harness/reports/CAMPAIGN-012-r1-worker.md`
- Commit policy: exactly five scoped local commits, one for PKG-065 through PKG-069
- Worktree strategy: shared worktree; sequential package integration
- Subagent delegation: allowed, not required; maximum three bounded implementation or
  read-only assignments
- Parallel delegation: allowed only for disjoint read-only investigation or disjoint
  test/doc paths; production files must not be edited concurrently

## Campaign outcome

Add an opt-in, client-neutral verification receipt to the existing
`view_review_record` tool. A caller can request `detail_level="verification"` and receive
a compact deterministic Markdown receipt plus the matching canonical structured receipt,
without relying on Goose or another outer model to rename or reconstruct execution facts.
The normal Council report remains concise and unchanged.

## Context

CAMPAIGN-011 and Q-013 are complete with 52/52 accepted features and 13/13 accepted
quality gates. Q-013 persisted records correctly held routing, role coverage, sampling,
budget and chief disposition, but Goose's surrounding narrative renamed roles/statuses
and misstated some budgets. Persisted records are authoritative. This Campaign adds a
safe projection of that authority; it does not change Council reasoning.

Design assessment:
`harness/evaluations/NEXT-CAMPAIGN-012-ASSESSMENT.md`.

## Admission and protected state

Start only if `HEAD` and `origin/main` both equal the exact baseline, the Git index is
empty, and no product/source/test/package diff exists against the baseline. The admitted
worktree deliberately contains Foreman-owned Campaign assets and pre-existing user
assets. Preserve them exactly.

Foreman-owned protected hashes:

| Path | SHA-256 |
| --- | --- |
| `harness/features.json` | `EF72993996F07D1F85F50173BE67294D49ECA0DF480AFE018067C066750061C0` |
| `harness/plan.md` | `0C7235BEAC53AA93817D6FDF9931B5769148BAEB91EE359AF1D0D37E58857FF8` |
| `harness/progress.md` | `B94CB0B934C9D9BD967A9A9FF3D3F8C0BF09DA7F41BB9856049044EB166006D9` |
| `harness/evaluations/CAMPAIGN-011-q013-archive-ci-review.md` | `03BA93961D64B09F652673C0B1754570BC372AE69943061FABBE6D4567BE5126` |
| `harness/evaluations/NEXT-CAMPAIGN-012-ASSESSMENT.md` | `8DE8D6FEB40D4EA070E0D48B177F021DA5F4BC338ECE3559A41F330A5728DC0F` |

The launch prompt supplies the final contract SHA-256; verify it before edits. Do not
modify, stage or commit any Harness asset except the two required new report paths. Do
not read, traverse, copy, hash, modify or stage `.learnings/**`, `reviews/**`,
`.tmp/q012/**`, the user audit report, or other user-owned untracked content. Do not use
raw Q-012/Q-013 records or Goose prose as fixtures. Synthetic live-shaped records may be
constructed only from the bounded facts in accepted evaluations and this contract.

If admission differs, stop before edits with `BLOCKED` and report the exact mismatch.

Foreman issuance evidence on the exact baseline:

- `python -m compileall src tests`: passed.
- System Python 3.13 test attempt: collection stopped because that interpreter does not
  have `fastmcp`; this is an environment mismatch, not baseline product evidence.
- First repository `.venv` attempt: correctly collected 311 tests but the specified
  nested basetemp parent had not been created, producing fixture setup errors.
- Corrected repository `.venv` run after explicitly creating the isolated parent:
  `311 passed in 3.80s` on Python 3.12.9/FastMCP 2.13.0.2.
- The Foreman removed only the exact temporary directory it created. `.learnings/**` is
  protected, so the two failed command records are retained here instead of being written
  into the self-improvement log.

## Frozen design

### Architecture and invariants

- The public MCP surface remains exactly five tools in the existing order.
- `view_review_record` keeps its existing parameters and adds only the accepted value
  `verification` for `detail_level`; `full` and `summary` outputs remain behaviorally and
  structurally unchanged.
- `review_translation` and `continue_review` primary and structured outputs remain
  unchanged except additive current-server version/build diagnostics required by the
  V0.12 release.
- Receipt construction is a pure, deterministic projection from one loaded persisted
  record plus the current `_server_info()` identity. It performs exactly one record load,
  zero saves, zero sampling, zero elicitation and no orchestration/adjudication call.
- Persisted Review Schema remains `2.5`. Receipt protocol `1.0` is a derived view and is
  never written back into review history.
- Defaults remain review-only, interactive `auto`, briefing `auto`, trace `summary`,
  history `full`, and Council adjudication fallback. Budgets remain 6/13/18 and review
  concurrency remains 1..3 with default/max 3.
- All routing profiles, roles, prompts, preflight rules, issue clustering, value metrics,
  Policy Gate, chief adjudication, decision authority and normal five-section report
  behavior remain unchanged.

### Exact tool payload

For `detail_level="verification"`, `view_review_record` returns one `ToolResult` whose
structured content is exactly this wrapper shape:

```json
{
  "review_id": "<same review id>",
  "display_report": "<deterministic verification Markdown>",
  "verification_receipt": { "<canonical receipt below>": "..." }
}
```

Do not include the raw full record, source, candidate, model prose or evidence prose in
this wrapper. The existing `dual_channel_result` presents `display_report` as primary
text and may append its established review-ID footer. Invalid detail levels return the
existing bounded error shape with the truthful message:
`detail_level must be full, summary, or verification`.

`get_server_info()` adds only:

```json
{
  "verification_receipt_schema_version": "1.0",
  "review_record_detail_levels": ["full", "summary", "verification"]
}
```

All existing server-info fields remain unchanged apart from the V0.12 package/build
identifiers.

### Canonical `verification_receipt` field contract

The canonical JSON object has these exact keys and nesting. `T | null` means JSON null,
never a guessed compatibility default. Arrays preserve recorded order unless explicitly
stated as sorted.

```text
receipt_schema_version: "1.0"
review_id: string
record:
  schema_version: string
  history_mode: "full" | "metadata" | "legacy"
  parent_review_id: string | null
  recorded_package_version: string | null
  recorded_diagnostic_build: string | null
serving:
  package_version: string
  module_version: string
  diagnostic_build: string
  schema_version: string
routing:
  mode: string | null
  content_type: string | null
  profile: string | null
  reason_codes: list[string] | null
  active_role_ids: list[string] | null
reviewer_execution:
  samples: list[{role_id: string, sample_status: "structured_success" | "unavailable" | null}] | null
  coverage: "full" | "partial" | "none" | "not_applicable" | null
  successful_count: integer | null
  unavailable_count: integer | null
runtime:
  sampling_calls_total: integer | null
  sample_budget_total: integer | null
  elicitation_calls_total: integer | null
  briefing_elicitation_calls: integer | null
  context_gap_elicitation_calls: integer | null
  outcome_elicitation_calls: integer | null
  wall_clock_ms: integer | null
  sampling_wait_ms: integer | null
  independent_review_concurrency_limit: integer | null
  independent_review_peak_concurrency: integer | null
  independent_review_batch_count: integer | null
  independent_review_concurrency_disposition: string | null
preflight:
  blocking: boolean | null
  failed_check_count: integer | null
  failed_blocking_check_count: integer | null
  failed_blocking_check_kinds: list[string] | null
issues:
  cluster_count: integer | null
  blocking_cluster_count: integer | null
  severity_counts: {critical: integer, major: integer, minor: integer, preference: integer} | null
  category_counts: object[string, integer] | null
outcome:
  status: string | null
  degraded: boolean | null
  warning_count: integer | null
  fallback_reason_code: string | null
  fallback_reason_redacted: boolean | null
  publishability: "可发布" | "修改后可发布" | "需人工复核" | null
  review_needed: "是" | "否" | null
  suggested_translation_present: boolean | null
coherence:
  expected_terminal_disposition: string | null
  terminal_disposition_occurrences: integer | null
  terminal_disposition_is_last_report_line: boolean | null
  terminal_disposition_matches_structured: boolean | null
availability:
  verification_complete: boolean
  not_recorded_fields: list[string]
  redacted_fields: list[string]
```

`expected_terminal_disposition` is the exact Markdown line
`- 最终处置：{publishability}；需人工复核：{review_needed}`. Coherence is descriptive;
the projector must report a mismatch and must never rewrite the record or chief outcome.

### Availability and privacy rules

- For a full current V2.5 record, all applicable fields above are populated from recorded
  values. Empty recorded fallback reason is the exact empty string, not null.
- For `history_mode="metadata"`, only fields physically retained by the existing
  metadata allowlist may be populated. Omitted active roles, samples, preflight, issues,
  warning text/count, fallback reason, suggested-translation presence, and display-report
  coherence are null and their exact dotted paths appear in sorted
  `availability.not_recorded_fields`.
- V1 returns `history_mode="legacy"`; only physically recorded review ID, mode, status
  and chief fields may be projected. All other absent facts are null and enumerated.
- V2.0 through V2.4 availability is schema-aware. In particular, routing provenance is
  not recorded before 2.5, concurrency/timing provenance is not recorded before 2.3,
  and compatibility-model defaults must not be reported as historical observations.
- `verification_complete` is true only when every field required for a full record of
  that schema is recorded and no value required by the receipt was redacted.
- Role IDs must be registry-backed. Routing/reason/status/concurrency/preflight/category
  codes must come from bounded existing enums/allowlists or a strict identifier allowlist.
  Unknown or prose-shaped values are omitted/null, their dotted path is added to sorted
  `redacted_fields`, and no raw value survives either channel.
- `fallback_reason_code` may expose only an empty string or a bounded code matching
  `^[a-z0-9][a-z0-9_:-]{0,79}$`; other content is null and redacted.
- `category_counts` uses bounded known issue families with unknown safe values collapsed
  to `other`; keys are deterministically sorted.
- `failed_blocking_check_kinds` is unique and sorted. It includes kind codes only, never
  source/candidate evidence, required literals, messages or paths.
- The receipt must never contain task source/candidate/context/audience, glossary/style/
  rule packets, reviewer feedback/findings/evidence/action text, cluster topic/spans,
  DecisionPoint/option/issue/claim IDs, user answers, suggested translation text,
  warnings text, filesystem paths, environment values or secrets.

### Primary Markdown contract

Render primary Markdown only from the canonical receipt, with these five headings in
this exact order:

1. `# Council 验证回执`
2. `## 记录与路由`
3. `## 覆盖与调用`
4. `## 风险与裁决`
5. `## 一致性与可用性`

Show canonical enum/code values in backticks. The primary text must include record and
serving versions, route and ordered roles when available, reviewer success/unavailable/
coverage, calls/budget/elicitation, server wall/sampling wait/concurrency, preflight and
issue counts, canonical status/degradation, chief outcome and terminal coherence. For
partial receipts, visibly state the count of unavailable and redacted fields. Target at
most 2,400 Unicode code points and never exceed the existing 3,200 primary hard cap. It
must not invent a human-friendly alias that replaces a canonical value.

### Main Worker implementation discretion

- Internal class/function names and private helper decomposition inside the new
  verification module.
- Exact safe-code allowlist representation and deterministic Markdown punctuation.
- Test fixture builders using synthetic, content-free live-shaped records.
- Whether receipt models use Pydantic models or typed immutable mappings, provided the
  exact JSON field contract and validation behavior above hold.

### Decisions reserved for Foreman or user

- Any sixth MCP tool, persisted Schema 2.6 migration, ordinary-report expansion, receipt
  fingerprint, raw evidence exposure, new role/model/provider, new budget, fuzzy matching,
  routing/adjudication change or product-scope expansion.
- Q-014 issuance, live Goose calls, publication, release, deployment and Campaign
  acceptance.

## Global boundaries

### Authorized production and package paths

- `src/council_of_translation/localization/verification.py` (new)
- `src/council_of_translation/tools/review.py`
- `src/council_of_translation/__init__.py`
- `AGENTS.md`
- `README.md`
- `docs/v0.4-architecture.md`
- `docs/v0.4-tool-contract.md`
- `pyproject.toml`
- `uv.lock`

### Authorized test paths

- `tests/unit/test_verification_receipt.py` (new)
- `tests/integration/test_v12_verification_view.py` (new)
- `tests/integration/test_v07_dual_channel.py`
- `tests/integration/test_tool_surface_v2.py`
- `tests/integration/test_v08_presentation_invariants.py`
- `tests/integration/test_v10_release_contract.py`
- `tests/integration/test_v24_golden_corpus.py`
- `tests/integration/test_v25_risk_routing.py`
- `tests/unit/test_persistence_v2.py`

### Authorized Worker evidence paths

- `harness/reports/CAMPAIGN-012-r1-ledger.md` (new, untracked/unstaged)
- `harness/reports/CAMPAIGN-012-r1-worker.md` (new, untracked/unstaged)
- `.tmp/campaign012-worker/**` for bounded temporary verification only; remove it before
  handoff

### Forbidden paths and systems

- Every path not explicitly authorized above
- All existing `harness/**` other than the two new Worker reports
- `.learnings/**`, `reviews/**`, `.tmp/q012/**`, `myTest/**` and the user audit report
- Goose installation/configuration, provider/model/account settings and credentials
- GitHub, remote branches, PRs, releases, deployments and package publication

### Non-goals

- Translating files, batch ingestion, TM/TB/SG ownership or applying edits
- New reviewer roles, prompts, sampling, elicitation, discussion or decision behavior
- Fuzzy issue matching, confidence scoring or legal advice
- Adding receipt data to the normal `review_translation` primary report
- Persisting the receipt or modifying existing record bytes

### Authorized external and cleanup actions

- Local dependency sync, test, build and isolated-wheel installation required by the
  verification section; use repository-local or exact OS temporary directories and never
  expose credentials.
- Install/use exact `uv 0.12.3` if unavailable. Record each dependency operation.
- Delete only Worker-created `.tmp/campaign012-worker/**` or exact ephemeral build/smoke
  directories after resolving and verifying their absolute paths. Do not clean unrelated
  caches or user directories.
- Local Git staging and exactly five local commits are required. No push or other remote
  mutation is authorized.

## Task graph

| Package | Feature | Observable outcome | Depends on | Authorized boundary | Parallel-safe |
| --- | --- | --- | --- | --- | --- |
| PKG-065 | F-053 | Canonical receipt models/projector expose the exact full-V2.5 field contract and pure side-effect-free projection | none | new verification module; new unit test | no |
| PKG-066 | F-054 | Metadata, V1 and V2.0-V2.4 availability plus hostile-value privacy controls are truthful | PKG-065 | verification module; unit test; persistence test | no |
| PKG-067 | F-055 | Existing history tool returns matching verification primary/structured channels; full/summary and normal review paths are unchanged | PKG-066 | review tool; new verification integration test; dual-channel/tool-surface tests | no |
| PKG-068 | F-056 | Live-shaped A/B/C, continuation, negative, Golden and invariant evidence closes coherence and compatibility risk | PKG-067 | authorized test paths only | no |
| PKG-069 | F-057 | V0.12 identifiers/docs/lock/artifacts and isolated-wheel behavior are complete | PKG-068 | authorized release/docs/package paths and release tests | no |

## Collision and integration map

| Packages/files at risk | Required sequencing | Integration check |
| --- | --- | --- |
| PKG-065/066 `verification.py` and unit tests | strictly sequential; PKG-066 extends accepted PKG-065 contract | rerun both package suites after PKG-066 |
| PKG-067/069 `tools/review.py` and tool-surface tests | PKG-067 behavior before PKG-069 identifier migration | focused tool tests after each commit |
| PKG-068 and all prior tests | no production edits in PKG-068 | full affected matrix and Golden after commit |
| `uv.lock` | PKG-069 only, exact pinned canonical refresh | root-only semantic diff and lock invariants |

Main Worker owns every integration decision and must inspect each package diff before the
next package begins. Subagents may not edit overlapping paths or accept work.

## Package acceptance details

### PKG-065 — canonical receipt

- Full V2.5 synthetic A/B/C shapes reproduce exact ordered route/role values, 7/13,
  4/6 and 8/18 total calls/budgets, zero elicitation, full coverage and their canonical
  chief outcomes without aliases.
- Receipt rendering from the same record is deterministic and record bytes/models remain
  equivalent before/after projection.
- Unit instrumentation proves zero executor/gateway/orchestration/store-save activity.

### PKG-066 — privacy and historical truth

- V1, metadata, and every V2.0-V2.4 compatibility case has an explicit expected
  availability matrix; no defaulted routing/timing/value is presented as recorded.
- Private sentinels in every forbidden prose/path field are absent from canonical JSON
  serialization and Markdown.
- Unknown role/code/prose-shaped fallback values are redacted without exceptions or raw
  echo. Output size and list/count bounds remain deterministic.

### PKG-067 — existing-tool dual channel

- Actual registered FastMCP tool invocation returns the exact wrapper, receipt and five
  Markdown headings for `verification`.
- Existing `full` and `summary` structured outputs compare equal to pre-feature expected
  projections; normal review/continuation primary text is unchanged.
- Tool registration stays exactly five and schema advertises the additive detail level
  through its description/diagnostics without changing required parameters.

### PKG-068 — integrated evidence

- Synthetic Q-013-shaped clean/edit/blocker cases verify primary/structured values and
  terminal coherence, including a deliberate mismatch that is reported but not repaired.
- Unavailable reviewer, metadata, legacy, continuation and hostile-record controls pass.
- Exact 24/24 Golden corpus remains intact with all existing aggregate metrics at 1.0.
- Receipt retrieval does not change sampling/elicitation counters, record timestamps,
  persistence bytes or normal report text.

### PKG-069 — release migration

- Package/module become `0.12.0`, build becomes `verifiable-evidence-council-v10`,
  persisted schema stays `2.5`, receipt schema is `1.0`.
- `uv 0.12.3` canonical refresh changes only the editable root version
  `0.11.1 -> 0.12.0`; lock revision 3, package count 78 and 586 upload-time entries remain.
- Docs distinguish normal/summary/full/verification views and state that the receipt is
  opt-in technical evidence, not a replacement for the process-first report.

## Campaign acceptance criteria

1. F-053 through F-057 meet every feature and package criterion without modifying a
   frozen product invariant.
2. Receipt field names/types/nesting and availability semantics match this contract
   exactly; no alias-only compatibility layer is accepted.
3. Both receipt channels are privacy-safe, bounded, deterministic and mutually coherent.
4. Existing public tools, full/summary behavior, normal primary reports, persistence,
   routing, sampling, adjudication and review-only safety remain unchanged.
5. All product/test/docs/lock changes are within the exact allowlist and split across
   exactly five scoped commits.
6. Fresh source, artifact and isolated installed-wheel evidence passes with no skipped
   required check.
7. Worker reports risks and evidence but makes no acceptance, Q-014 or project-completion
   claim.

## Required Campaign verification

Run and report at minimum:

1. Admission: `python -m compileall src tests` and the complete baseline test suite;
   expected admitted baseline is 311 passing tests. If it differs, diagnose and stop on
   unexplained drift before implementation.
2. Focused unit receipt tests after PKG-065 and combined historical/privacy tests after
   PKG-066.
3. Actual FastMCP dual-channel/tool-registration integration tests after PKG-067.
4. PKG-068 live-shaped A/B/C, mismatch, metadata, V1, V2.0-V2.5, hostile prose,
   unavailable reviewer, continuation and no-side-effect probes.
5. Exact 24/24 executable Golden corpus and all existing eight aggregate metrics at 1.0.
6. Complete affected tool/persistence/presentation/routing/release invariant matrix.
7. Final `python -m compileall src tests` and complete test suite with zero failures and
   no reduction from the 311-test admitted baseline.
8. Exact five-tool order; package/module/build, Schema 2.5, receipt Schema 1.0, defaults,
   budgets 6/13/18 and concurrency 3/3 probes.
9. Programmatic proof that verification retrieval performs one load, zero saves, zero
   sampling, zero elicitation and no record mutation.
10. `git diff --check`, exact baseline-to-final path audit, dead-import scan, index empty
    and all protected hashes exact.
11. Fresh wheel and sdist build plus archive inspection.
12. Isolated CPython 3.12/current FastMCP wheel-origin smoke that calls all five tools and
    verifies normal dual channels plus full/summary/verification history behavior from
    the installed wheel.

Use a unique repository-local basetemp/cache if the known Windows host temp permission
defect occurs. Record the original failure and bounded rerun. Do not hide, delete or
weaken a failing test to improve the count.

## Required evidence and handoff

- Maintain the required ledger mapping every package to executor/subagent, files, commit,
  commands, results, deviations and integration state.
- Record baseline/final HEAD, exact five commits, changed-file list/stat and complete diff
  inspection.
- Record all subagents, authority/escalation requests, dependency operations, cleanup,
  live calls and external mutations, including zero counts.
- Record fresh artifact names, sizes and SHA-256 values and prove isolated imports came
  from site-packages rather than the workspace.
- Record skipped checks with consequences; required checks may not be silently skipped.
- Preserve secrets and user data; use only content-free synthetic sentinels in reports.
- Leave `harness/reports/CAMPAIGN-012-r1-ledger.md` and
  `harness/reports/CAMPAIGN-012-r1-worker.md` untracked and unstaged. The Git index must be
  empty at handoff.

In chat, start with exactly `READY_FOR_REVIEW` or `BLOCKED`, then summarize report and
ledger paths, contract hash, baseline/final state, commits/files, package and Campaign
verification, artifacts, skipped checks, protected hashes, subagent/authority/dependency/
live-call counts and remaining risks or blockers. Stop after the handoff. Do not claim
Campaign acceptance or Q-014 completion.

## Stop conditions

Stop with `BLOCKED` rather than guessing if:

- baseline, index, contract hash or any protected asset differs;
- a required field cannot be derived truthfully without raw-file access, persistence
  migration or compatibility-default inference;
- the exact receipt contract requires a field/type/name/nesting change;
- implementation needs any path outside the allowlist;
- normal reports/full/summary outputs, routing, sampling, Policy Gate, chief decision,
  persistence bytes, tool count, budgets or concurrency would change;
- privacy tests reveal source/candidate/model prose, paths, secrets or internal issue IDs;
- lock regeneration changes anything beyond the exact root version or loses revision,
  package or upload-time invariants;
- a required check, build or installed-wheel smoke cannot establish the result; or
- work requires live Goose/provider/model calls, publication, push, PR, release,
  deployment, credentials, destructive cleanup or other unapproved authority.
