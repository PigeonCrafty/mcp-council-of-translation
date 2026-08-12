# CAMPAIGN-004-r1 Main Worker Ledger

## Authority

- HARNESS_ROLE: WORKER / MAIN WORKER
- HARNESS_MODE: STRICT_CAMPAIGN
- Contract: `harness/contracts/CAMPAIGN-004-r1.md`
- Contract SHA-256: `8A77DDCEB46339632D12603D5AA62CA1C5E39FEED8A1B250161DEA2A0E8B7C03`
- Exact baseline: `b601cf93f452a8e574e3c15a4a9c236cf8142ce1`
- Baseline subject: `Archive V0.6 Campaign acceptance`
- Subagents allowed/used: 2 / 0
- Live Goose/model/provider calls: prohibited / 0

## Admission gate

- HEAD and subject: exact.
- Git index: empty.
- Protected dirty/untracked inventory: `harness/features.json`, `harness/plan.md`,
  `harness/progress.md`, `.learnings/`, `harness/contracts/CAMPAIGN-004-r1.md`,
  `harness/evaluations/CAMPAIGN-003-q008-q009-live-review.md`, audit Markdown,
  and `reviews/`. `myTest/` absent.
- Contract SHA-256 and all fourteen protected SHA-256 values: exact; mismatch count 0.
- Compile: `python -m compileall -q src tests` -> exit 0,
  `ADMISSION_COMPILE_OK`.
- Full baseline: `.venv\Scripts\python.exe -m pytest -q --basetemp
  .tmp\campaign004-r1-admission -p no:cacheprovider` -> exit 0,
  `184 passed in 2.02s`.
- Installed API inspection: FastMCP `2.13.0.2`, MCP `1.20.0`;
  `ToolResult(content, structured_content)` and MCP
  `CallToolResult(content, structuredContent, isError)` signatures present.
- Admission disposition: PASS. No repository file changed before PASS.

## Authorized boundaries

Only the source/test/version/doc paths listed by the contract plus this Campaign's ledger
and Worker report. Main Worker owns presentation adapter, `tools/review.py`, `digest.py`
and orchestration integration. Five tools, schema 2.2, review-only behavior, user
authority, privacy and 6/13/18 budgets remain frozen.

## Package log

### PKG-023 — dual-channel tool results

- Status: completed.
- Executor: Main Worker; no delegation.
- Files: new `src/council_of_translation/presentation.py`,
  `src/council_of_translation/tools/review.py`, `src/council_of_translation/server.py`,
  new `tests/integration/test_v07_dual_channel.py`, and the existing direct-call error
  assertion in `test_tool_surface_v2.py`.
- Result shape: `ToolResult` with first `TextContent` primary Markdown and unchanged
  JSON-safe dictionary in `structured_content`; safe errors use the same shape. Review,
  continuation and full/summary record view share the adapter; list/info remain dicts.
- Verification: `python -m compileall -q src tests` -> exit 0;
  focused actual FastMCP Client/tool surface suite -> `10 passed in 1.06s`;
  integrated full suite -> `187 passed in 2.03s`.
- Retry: first focused run was `3 failed, 7 passed` because tests used MCP wire alias
  `structuredContent` as a Python attribute; FastMCP Client exposes
  `structured_content`. Production dual-channel output was already present. Tests were
  corrected to the public Python attribute and passed.
- Commit: `eda3dee Add dual-channel Council tool results`.

### PKG-024 — adaptive concise report

- Status: completed.
- Executor: Main Worker; no delegation.
- Files: `localization/digest.py`, `localization/orchestration.py`, migrated structured
  compatibility assertion in `test_v22_digest.py`, and new
  `tests/unit/test_v07_report.py`.
- Behavior: persisted 12-field `ProcessDigestV2` order retained; adaptive human report
  now has four clean sections or a conditional fifth interaction section, Chinese
  headings, shallow bounded bullets, generic visible degradation and final disposition
  as the last substantive line. Clean reference <=1,800; all reports <=3,200.
- Verification: compile exit 0; focused clean/interaction/hostile/Core/dual-channel suite
  -> `9 passed in 1.39s`; full integrated suite -> `190 passed in 2.04s`.
- Warning retry: focused run surfaced a Pydantic instance `model_fields` deprecation;
  assertion changed to class access without weakening the frozen 12-field-order check.
- Commit: `1bbe03e Render concise adaptive Council reports`.

### PKG-025 — consensus and role lenses

- Status: completed.
- Executor: Main Worker; no delegation.
- Files: `localization/digest.py` and new
  `tests/integration/test_v07_consensus.py`.
- Behavior: role lenses deterministically select blocker/major, concrete choice,
  affirmation, other issue, clean role-specific duty check, then unavailable notice.
  Full-coverage affirmations may synthesize positive consensus from a shared concrete
  candidate outcome; partial coverage cannot. This synthesis never feeds adjudication.
- Core evidence: live-shaped six affirmations -> full coverage, six samples, six
  distinct lenses, all six Chinese labels exactly once, shared support for `继续`, clean
  report <=1,800; partial coverage -> no positive consensus, explicit blind spot and
  human review.
- Verification: compile exit 0; focused suite -> `8 passed in 0.23s`; integrated full
  suite -> `192 passed in 2.05s`.
- Commit: `150408d Synthesize truthful Council consensus`.

### PKG-026 — layered retrieval and integrity regressions

- Status: completed.
- Executor: Main Worker; no delegation.
- Files: primary-text safety/humanization refinements in `localization/digest.py` and new
  `tests/integration/test_v07_integrity.py`.
- Sentinel evidence: actual six-field schema titles map `tone_goal` to
  `TONE_SENTINEL_独立语气` and `primary_focus` to
  `FOCUS_SENTINEL_独立重点`; accepted answer keys, effective brief, all six reviewer
  prompts and reloaded full record retain the correct non-transposed values.
- Integrity evidence: disputed minority/decisive condition, blocker, delegation,
  reconsideration, pending, degradation and human-review conclusion all visible;
  internal IDs, role IDs and Policy Gate label hidden; full structured evidence remains
  complete while primary text excludes private raw source/target/reviewer content;
  presentation adds zero samples.
- Regression verification: focused layered suite across dual-channel, consensus,
  briefing, continuation, persistence/privacy, suppression and reconsideration ->
  `54 passed in 1.50s`; full integrated suite -> `196 passed in 2.17s`; compile exit 0.
- Commit: `d47ddd9 Harden concise Council presentation`.

### PKG-027 — V0.7 migration and package verification

- Status: completed.
- Executor: Main Worker; no delegation.
- Files: package/module/runtime/record version identifiers, diagnostic build, server
  guidance, focused server-info assertion, dependency-neutral package metadata and four
  authorized documentation assets.
- Identifiers: package/module `0.7.0`, diagnostic build
  `concise-council-display-v5`, schema `2.2`, five tools and 6/13/18 budgets unchanged.
- Documentation: primary text plus complete structured content, adaptive Chinese report
  order and bounds, layered evidence retrieval, review-only boundary, and normal-user
  Q-009 recipe without a diagnostic checklist or required second history call.
- Verification: compile exit 0; focused V0.7/tool/digest suite ->
  `22 passed in 1.31s`; integrated full suite -> `196 passed in 2.03s`.
- Dead-reference scan: only four frozen V0.6 strings remain in the forbidden
  persistence module's explicit metadata-history projection; no active V0.6 identifier
  remains in authorized source, tests, docs or package metadata.
- Fresh build: initial `.venv\Scripts\python.exe -m build` attempt failed before
  artifact creation because the existing development environment has no `build` module.
  No dependency was added. A new repository-local directory and `uv build` produced
  `council_of_translation-0.7.0-py3-none-any.whl` (73,858 bytes,
  SHA-256 `3158B12E1B7860EBE33636C0A10B6FE4A0C3A1B52B308FF46162E4CE7295EB14`)
  and sdist (67,243 bytes,
  SHA-256 `CED34829BF91F802775B06B805327AE66DD032E196A5D6C80F38299F050382FE`).
- Installed wheel, FastMCP 2.13.0.2 / MCP 1.29.0: exact five registered tools;
  successful review/continue/view calls returned primary text plus structured content;
  info/list calls succeeded; version/build/schema/defaults/budgets exact. Final output:
  `WHEEL_SMOKE_OK ... tools=5 primary_len=634 structured_keys=19`.
- Installed wheel, current FastMCP 3.4.7 / MCP 1.29.0: same checks and same final
  primary/structured metrics passed.
- 2.13 smoke retries: first script expected empty decisions to error, but the valid
  continuation succeeded; second used `count` instead of the documented
  `total_reviews` list key. Both were smoke-script assertions, not package failures;
  the corrected script passed without dependency reinstall or extra network read.
- Core/tool printed probe: primary length 779; headings `审校背景`, `专业视角`,
  `共识、分歧与盲区`, `主编结论`; six Chinese role labels once each; positive
  consensus supports `继续`; structured key set has 18 keys; sampling stayed 6 -> 6;
  full reload retained six finding records.
- Fixture matrix: disputed/degraded/pending report length 380 with five ordered sections,
  blocker/minority/decisive condition/context gap/delegation/reconsideration/degradation
  visible and internal IDs hidden; hostile report length 1,069 <=3,200 with disposition
  last. Clean primary is 779 <=1,800.
- Final verification: `196 passed in 2.12s`; compile exit 0; baseline-to-final
  `git diff --check` pass; 19 files and zero scope mismatches; dead-import AST scan pass;
  exactly five `@mcp.tool` registrations; index empty; protected mismatch count 0.
- Commit: `ff0e345 Release concise Council display contract`.

## Final evidence summary

- Final HEAD: `ff0e345ff174f1f39741bbb47979aa51e277ca52`.
- Commits: five, one per PKG-023 through PKG-027; no report/Harness/user asset staged.
- Final full regression: `196 passed in 2.12s`; admission was `184 passed in 2.02s`.
- Git authority escalations: 10, exactly one scoped `git add` and one local `git commit`
  per package. No push/tag/PR/release/deploy operation.
- Authorized dependency network operations: fresh `uv build` environment and two fresh
  wheel dependency resolutions. Live Goose/model/provider/external service calls: 0.
- Subagents: 0. Live checks skipped as prohibited/optional. `ruff` was not installed;
  a read-only AST unused-import scan over changed production Python passed instead.
- Self-improvement logging was suppressed because `.learnings/**` is protected; all
  command/test retries are recorded here and in the Worker report.
- Protected hashes: contract hash exact; fourteen listed protected assets exact; mismatch
  count 0. Original Foreman/user dirty inventory remains present and untouched.
