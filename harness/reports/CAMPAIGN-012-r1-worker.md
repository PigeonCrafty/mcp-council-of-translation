# CAMPAIGN-012-r1 Worker Report

## Terminal recommendation

`READY_FOR_REVIEW`

This is a Worker handoff only. Campaign acceptance and Q-014 authority remain with the Foreman.

## Control and admission

- Role/mode: `WORKER / MAIN WORKER`, `STRICT_CAMPAIGN`
- Contract: `harness/contracts/CAMPAIGN-012-r1.md`
- Contract SHA-256: `E4E1CAAFB5E6E08729B5E726C5144793D3BE7E029699AA24984F37E97D587548`
- Exact admission HEAD and `origin/main`: `6544d41d308f9ed7ab253dac5a70a94581cd04d8`
- Admission index: empty
- Admission product/source/test/package drift: none
- Admission compile: PASS
- Admission complete suite: `311 passed in 4.53s`
- Admitted tracked dirty Foreman assets: `harness/features.json`, `harness/plan.md`, `harness/progress.md`
- Admitted protected/user untracked assets: `.learnings/`, `reviews/`, the user audit report, active contract, and two contract-listed Foreman evaluations
- No forbidden directory or raw Q-012/Q-013 record was read, copied, modified, staged, deleted or committed.

## Package execution and commits

1. PKG-065 / F-053 — canonical current V2.5 receipt
   - Paths: `src/council_of_translation/localization/verification.py`; `tests/unit/test_verification_receipt.py`
   - Evidence: exact nested field shape; Q-013-shaped 7/13, 4/6 and 8/18 cases; deterministic five-section Markdown; strict code/privacy projection; zero executor/gateway/orchestration/save instrumentation; `7 passed`
   - Commit: `1b5de8194b952adf2e8c57ba78a30542a330dc2e`
2. PKG-066 / F-054 — metadata/historical availability and privacy
   - Paths: verification module; receipt unit tests; `tests/unit/test_persistence_v2.py`
   - Evidence: metadata physical allowlist; V1 and V2.0-V2.4 schema-aware matrices; model-fields-set protection against compatibility defaults; hostile role/code/path/prose redaction; `34 passed`
   - Commit: `a712d1d60af1d61c8823d2fd1fb6308b470d2455`
3. PKG-067 / F-055 — existing-tool verification view
   - Paths: `src/council_of_translation/tools/review.py`; tool-surface test; new integration test
   - Evidence: actual FastMCP invocation, exact `{review_id, display_report, verification_receipt}` wrapper, five Markdown headings, single load, no save, unchanged full/summary projections, exact five tools; focused `20 passed`, dependent matrix `54 passed`
   - Commit: `da4f9c466ebf497feefdc661b3e6bfda8e1a016b`
4. PKG-068 / F-056 — integrated/live-shaped evidence
   - Path: `tests/integration/test_v12_verification_view.py`
   - Evidence: clean/modified/blocker A/B/C; deliberate terminal mismatch reported without repair; unavailable reviewer; continuation parent; metadata and legacy; persistence bytes/counters/timestamps/report unchanged; affected matrix `72 passed`; Golden `24/24`
   - Commit: `340d70d2729569baa23937347e94f70beab5671e`
5. PKG-069 / F-057 — V0.12 release migration
   - Paths: `AGENTS.md`, `README.md`, both authorized docs, `pyproject.toml`, module identifiers, release/tool/persistence assertions, `uv.lock`
   - Evidence: `0.12.0`, build `verifiable-evidence-council-v10`, persisted Schema `2.5`, receipt Schema `1.0`; docs distinguish normal/full/summary/verification; release-focused `58 passed`; exact pinned lock/build/smoke
   - Commit: `06b0e378adc99826c48cd9fc7cc4337d8bc25367`

Final HEAD is `06b0e378adc99826c48cd9fc7cc4337d8bc25367`. There are exactly five baseline-to-final commits.

## Changed paths

Baseline-to-final changes are exactly these 14 authorized paths:

- `AGENTS.md`
- `README.md`
- `docs/v0.4-architecture.md`
- `docs/v0.4-tool-contract.md`
- `pyproject.toml`
- `src/council_of_translation/__init__.py`
- `src/council_of_translation/localization/verification.py`
- `src/council_of_translation/tools/review.py`
- `tests/integration/test_tool_surface_v2.py`
- `tests/integration/test_v10_release_contract.py`
- `tests/integration/test_v12_verification_view.py`
- `tests/unit/test_persistence_v2.py`
- `tests/unit/test_verification_receipt.py`
- `uv.lock`

Diff stat: 14 files, 1544 insertions, 29 deletions. The root lock semantic diff is exactly editable root version `0.11.1 -> 0.12.0`; revision `3`, 78 packages and 586 upload-time entries are unchanged.

## Campaign verification

- Final syntax: `.venv\Scripts\python.exe -m compileall -q src tests` -> PASS
- Final complete suite: `.venv\Scripts\python.exe -m pytest -q --basetemp=.tmp/campaign012-worker/final-after-commits` -> `334 passed in 3.86s`
- No test reduction from admitted `311`; no failures
- Exact Golden production runner: `24/24`, `failed_case_ids=[]`; all eight aggregate metrics are `1.0`; runtime sampling `148`, elicitation `4`, budget `296`, routing/display calls `0/0`
- Runtime identity probe: tools exactly `review_translation`, `continue_review`, `view_review_record`, `list_review_records`, `get_server_info`; package/module `0.12.0`; build `verifiable-evidence-council-v10`; persisted Schema `2.5`; receipt Schema `1.0`; defaults unchanged; budgets `6/13/18`; concurrency `3/3`
- Purity proof: verification retrieval has one record load, zero saves, zero sampling, zero elicitation, no record model mutation, no timestamp/counter/report change and byte-identical persisted JSON
- `git diff --check`: PASS
- Read-only AST dead-import scan over eight changed Python paths: PASS
- Baseline-to-final path/scope audit: PASS
- Final Git index: empty

## Fresh release artifacts

Built with exact `uv 0.12.3 (507230998 2026-08-07 x86_64-pc-windows-msvc)` using repository-local `UV_CACHE_DIR` and `UV_TOOL_DIR`:

- `council_of_translation-0.12.0-py3-none-any.whl` — 102026 bytes — SHA-256 `CF704CBDB6262BFAB8B81ECBD76B25FB9A786826ECE422867789ADBF0B0F1533`
- `council_of_translation-0.12.0.tar.gz` — 95611 bytes — SHA-256 `B2CF5AD5821E92D9E21DE21D8316961B735694DFEAA3585A26153C2960C79C22`

Archive inspection confirmed the verification module, 0.12.0 metadata, Python range and direct dependencies. Isolated installed-wheel smoke used CPython 3.12.9 and current FastMCP 3.4.7. Import origin was the isolated environment's `Lib/site-packages/council_of_translation/__init__.py`, not workspace `src`. It called all five tools and verified review/continuation error dual channels, list/info, and full/summary/verification history views; verification availability was complete.

## Protected reconciliation

Final hashes match the contract:

- Contract: `E4E1CAAFB5E6E08729B5E726C5144793D3BE7E029699AA24984F37E97D587548`
- `harness/features.json`: `EF72993996F07D1F85F50173BE67294D49ECA0DF480AFE018067C066750061C0`
- `harness/plan.md`: `0C7235BEAC53AA93817D6FDF9931B5769148BAEB91EE359AF1D0D37E58857FF8`
- `harness/progress.md`: `B94CB0B934C9D9BD967A9A9FF3D3F8C0BF09DA7F41BB9856049044EB166006D9`
- Q-013 archive/CI review: `03BA93961D64B09F652673C0B1754570BC372AE69943061FABBE6D4567BE5126`
- NEXT-CAMPAIGN assessment: `8DE8D6FEB40D4EA070E0D48B177F021DA5F4BC338ECE3559A41F330A5728DC0F`

The three admitted tracked Harness files remain dirty and protected. The active contract/evaluations and all user assets remain untracked and protected. This report and the ledger remain untracked and unstaged.

## Delegation, authority and external actions

- Subagents: `3`, all bounded read-only analyses; implementation-editing subagents: `0`
- Main Worker inspected and integrated every result
- Authority escalation requests: `9`; five were required Git commit writes, one was a failed network-install retry, and three guarded the local two-commit object rewrite (one approval timeout, one exact-HEAD guard stop, one successful rewrite)
- Dependency-operation invocations: `7`; exact uv acquisition/version check, lock refresh, build, venv creation and three isolated-install attempts
- Live Goose/provider/model calls: `0`
- Git pushes/PR updates/publication/releases/deployments: `0`
- Credential/Goose configuration changes: `0`

## Deviations, failures and resolution

- Admission temp creation initially used unsupported `New-Item -LiteralPath`; corrected to a validated fixed `-Path` before compile/tests.
- A read-only PowerShell multi-range printer had a singleton-array type error; replaced by direct file reads.
- A subagent guessed nonexistent test names in read-only search and found that repo-root `python -m build` is shadowed/unusable; no production effect, and the required fixed uv build succeeded.
- First Git commit attempt hit sandbox `.git/index.lock` denial; bounded Git escalations completed the required local commits.
- First isolated install timed out downloading `exceptiongroup`; escalated retry could not read the workspace wheel; a same-sandbox cached retry succeeded.
- First installed FastMCP 3.4.7 smoke used obsolete server `get_tools`; corrected only the temporary script to public `list_tools`, then passed.
- One read-only `python -c` probe used illegal inline `async def`; replaced by direct `asyncio.run`.
- Dead-import scan found two unused imports in the new integration test; they were removed and PKG-068/069 commit objects were locally rebuilt to preserve exact five-package commit scope. The first rewrite approval timed out; a second guard used an incorrect expanded hash and stopped before writes; the corrected guarded rewrite succeeded.
- The first final-index audit used PowerShell output truthiness instead of `$LASTEXITCODE` and falsely printed `index=NOT_EMPTY`; the corrected `git diff --cached --name-only` audit returned no paths and confirmed the index is empty.
- Self-improvement logging was redirected here because `.learnings/**` is a protected user asset and was neither read nor written.

## Skipped checks and risks

- Required checks skipped: none.
- Live Goose/provider/model validation, push, PR, publication, release and deployment were intentionally not run because the contract forbids them; live-call count is zero.
- The initial uv build warned that its repository-local cache could theoretically be included. Explicit wheel/sdist manifests showed no cache content, and isolated wheel behavior passed. The entire Worker temporary directory is removed before handoff.
- Remaining non-blocking gates: independent Foreman acceptance and any later Q-014 issuance/publication/live validation.
