# CAMPAIGN-012-r4 Execution Ledger

## Control

- HARNESS_ROLE: `WORKER / MAIN WORKER`
- HARNESS_MODE: `STRICT_CAMPAIGN`
- Contract: `harness/contracts/CAMPAIGN-012-r4.md`
- Contract SHA-256: `29A6453ECD30C15CF204DB5C1B4DA3019632F9CBFE8B8FD222AC0CA7356A0255`
- Baseline: `aceac3383b2a597bbf5414362d9b71ac6e601267`
- Delegation: forbidden; Campaign subagents `0`
- Acceptance authority: Foreman only

## Admission

- Required repository/Harness assets read completely.
- HEAD matched the exact baseline; Git index was empty.
- Non-recursive status showed only admitted Foreman/user dirt and the r4 contract.
- All 15 contract-listed protected hashes matched.
- `python -m compileall src tests`: PASS.
- Complete baseline suite: exact `441 passed in 4.31s`.
- Forbidden `.learnings/**`, `reviews/**`, `myTest/**`, `dist/**` and independent audit
  Markdown were not read, hashed or traversed.

## Package state

| Package | State | Subagent | Commit | Evidence |
| --- | --- | --- | --- | --- |
| PKG-073 | committed | none | `a2078a462fc6f9d23c1a01d1e4b338764301f6eb` | Baseline actual FastMCP text had 1 block / 838 code points / footer last / 0 canonical labels / 0 JSON fences. Affected compile PASS. Focused receipt, verification-view and dual-channel selection: 135 passed. Text-only A/B/C parsed equal to the structured receipt at 3,800 / 3,478 / 3,980 code points with modes standard/lightweight/strict, calls 7/4/8, budgets 13/6/18, exact dispositions, five headings and no reconstructed aliases. Staged scope was exactly five authorized files; staged diff check passed. |
| PKG-074 | committed | none | `46849c9198213ad6d1e9888e8a0503bb1bccc61c` | Version/module `0.12.1`; build `verifiable-evidence-council-v10.1`; docs describe the same-object compact text fallback. Exact uv `0.12.3` canonical refresh resolved 78 packages and changed only editable root `0.12.0 -> 0.12.1`; lock SHA-256 `6B5E166D19F9466209C793624D92DE1F33EB254417CD571F653DD0A8B8E932DF`, revision/package/upload-time `3/78/586`. Compile PASS; focused release/tool/persistence plus PKG-073 controls: 171 passed. Staged scope was exactly ten authorized files; staged diff check passed. |

## Corrected command issue

- The first focused run used a nested `--basetemp` whose parent directory did not yet
  exist. Pytest completed 133 tests successfully and raised two setup errors while
  creating that path. No product assertion failed. The parent was created explicitly;
  the unchanged selection then passed 135/135. The self-improvement workflow was
  consulted, but its normal `.learnings/ERRORS.md` target is contract-protected and was
  neither read nor written; this ledger is the authorized durable record.
- A stale-string scan initially passed a lookahead to default `rg`, which does not
  support lookaround. The corrected `rg --pcre2` invocation passed with no stale matches.
- The first archive metadata assertion expected the unnormalized Python-range ordering;
  inspection showed the valid normalized `Requires-Python: <3.14,>=3.10` in both
  archives. Exact version and dependency metadata then passed.
- The first isolated-wheel smoke attempted the source-test helper `mcp.get_tools()`,
  which is not exposed on the FastMCP 3.4.7 service object. The supported
  `Client.list_tools()` path then passed the complete five-tool smoke.
- The first local AST scan treated `from __future__ import annotations` as an ordinary
  unused import. Excluding `__future__` directives produced zero unused imports across
  all nine changed Python files.

## Final verification

- Final compile: PASS.
- Complete suite: `444 passed in 3.98s`; no failures or skips.
- Focused release/receipt/tool/persistence matrix: `171 passed in 1.35s`.
- Focused purity/privacy/overflow matrix: `4 passed in 0.96s`.
- Golden pytest: `4 passed`; exact production aggregate `24/24`, no failed IDs, all
  eight metrics `1.0`, sampling/elicitation/budget `148/4/296`, routing/display `0/0`.
- Normal primary compatibility: review, continuation, full, summary and error text
  matched exact frozen strings; list and diagnostics retained their structured paths;
  canonical label was absent from every normal/error primary result.
- Verification purity probe: one load, zero saves, zero model-executor construction,
  zero interaction-gateway construction and no record mutation.
- Actual baseline-to-HEAD scope: 15/15 authorized paths, no unexpected or missing path.
- `git diff --check`: PASS. AST scan: nine files, zero unused imports.
- Exact public identity: five tools; package/module `0.12.1`; build
  `verifiable-evidence-council-v10.1`; record/receipt schemas `2.5/1.0`; budgets
  `6/13/18`; concurrency default/max `3/3`.
- Repository-local `.tmp/campaign012-r4-worker` and generated root `build` were resolved
  inside the repository and removed after evidence capture; both are absent at handoff.

## Fresh artifacts and installed-wheel smoke

- Exact builder: `uv 0.12.3 (507230998 2026-08-07 x86_64-pc-windows-msvc)`.
- `council_of_translation-0.12.1-py3-none-any.whl`: 102,738 bytes; SHA-256
  `29D3907AC9B4F3C64245FEEE7487E93E55D98AD98F3D504CA214D2475B1C5B6A`.
- `council_of_translation-0.12.1.tar.gz`: 96,442 bytes; SHA-256
  `FADD8801EF3DD9C357D327E3AE10CFE79007A371944401A499B12AA36C2D7AB4`.
- Wheel/sdist archive inspection found the verification module, version `0.12.1`,
  normalized Python range, exact direct dependencies and zero `.tmp` members.
- Isolated CPython `3.12.9` / FastMCP `3.4.7` imported from `wheel-env/Lib/site-packages`,
  called all five tools, reported exact identity/budgets/concurrency, and proved the
  2,713-code-point text JSON parsed equal to the structured receipt with footer before
  JSON, exactly five headings and no source text.

## Final lock and protected reconciliation

- `uv lock --check` with exact uv `0.12.3`: PASS, 78 packages.
- Lock SHA-256/invariants:
  `6B5E166D19F9466209C793624D92DE1F33EB254417CD571F653DD0A8B8E932DF`;
  revision/package/upload-time `3/78/586`; baseline diff is exactly editable root
  `0.12.0 -> 0.12.1`.
- Contract and all 15 listed protected hashes matched their admission values.
- Final HEAD: `46849c9198213ad6d1e9888e8a0503bb1bccc61c`; Git index empty.

## External and authority counts

- Live Goose/provider/model calls: `0`
- Remote/GitHub calls: `0`
- Push/PR/release/publication/deployment calls: `0`
- Authority escalations: `4` (two exact staging operations and two local commits)
- Dependency operations: `6` (exact uv acquisition/version check, lock refresh, build,
  isolated venv, isolated install and final lock check)
