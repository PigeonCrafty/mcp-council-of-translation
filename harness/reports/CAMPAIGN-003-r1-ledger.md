# CAMPAIGN-003-r1 Main Worker Ledger

## Authority

- HARNESS_ROLE: WORKER / MAIN WORKER
- HARNESS_MODE: STRICT_CAMPAIGN
- Contract: `harness/contracts/CAMPAIGN-003-r1.md`
- Contract SHA-256: `6A1017CF7C8205CC1FB753EC747529B0BF7920676655A53314C8B71B29239A46`
- Exact baseline: `fe4b55a6597d8ac18885c0faab14722f44588e12`
- Subagent ceiling: 3; planned/used: 0
- External/live calls: prohibited; count: 0

## Admission gate

- HEAD: exact baseline; commit object; subject `Close V0.5 live validation`.
- Branch: `main...origin/main`; index empty.
- Protected dirty/untracked inventory: `harness/features.json`, `harness/plan.md`,
  `harness/progress.md`, `.learnings/`, `harness/contracts/CAMPAIGN-003-r1.md`,
  `mcp-council-of-translation-audit-and-upgrade-recommendations.md`, `reviews/`.
- Protected hashes: all matched the contract admission table.
- Compile: `python -m compileall -q src tests` -> `COMPILE_OK`.
- Full baseline: `.venv\Scripts\python.exe -m pytest -q --basetemp
  .tmp\campaign003-r1-admission-2 -p no:cacheprovider` -> `159 passed in 1.63s`.
- Admission disposition: PASS. No production or report file was changed before PASS.

## Authorized boundaries

Only contract-listed source, tests, version/build files, README/AGENTS/V0.4 docs and this
Campaign's two report assets. Five public tools remain frozen; the sole public argument
addition is `briefing_mode=auto|always|off`, default `auto`. Review-only, privacy,
Policy Gate, continuation and 6/13/18 ceilings remain binding.

## Package log

### PKG-017 — V2.2 models, compatibility and persistence

- Status: completed.
- Assignment: Main Worker, no delegation.
- Changed files: `localization/models.py`, `compatibility.py`, `persistence.py`,
  `tests/unit/test_models_v2.py`, `test_persistence_v2.py`, new
  `test_v22_models_persistence.py`.
- Final package replay command: `.venv\Scripts\python.exe -m pytest -q
  tests\unit\test_models_v2.py tests\unit\test_persistence_v2.py
  tests\unit\test_v22_models_persistence.py --basetemp
  .tmp\campaign003-r1-final-pkg017 -p no:cacheprovider` -> exit 0,
  `29 passed in 0.24s`; package completion was `28 passed in 0.30s` before the PKG-022 metadata
  addition: `29 passed in 0.24s`);
  `git diff --check` passed (only protected `features.json` line-ending warning).
- Notes: authoritative writes are schema 2.2; V1/V2.0/V2.1 readers remain; metadata
  persists safe modes/counts/confidence/provenance IDs while excluding brief answers,
  context answers, model/user/chief prose, display Markdown and phase summaries.
- Commit: `f06e6e7 Add V2.2 guided session record models`.

### PKG-018 — Briefing Gate

- Status: completed.
- Assignment: Main Worker, no delegation.
- Changed files: new `localization/guided.py`; `orchestration.py`, `prompt_builders.py`,
  `roles.py`, `runtime.py`, `tools/review.py`; new `test_v22_briefing.py`; budget
  expectation migrations in role/runtime tests (budget constants share these files).
- Final package replay command: `.venv\Scripts\python.exe -m pytest -q
  tests\integration\test_v22_briefing.py tests\unit\test_roles_v2.py
  tests\unit\test_runtime_v2.py --basetemp .tmp\campaign003-r1-final-pkg018 -p
  no:cacheprovider` -> exit 0, `25 passed in 0.25s`; source/target-only event trace
  asserted briefing before first sample; all
  accept/non-accept modes and `UI button` routing covered.
- Full interim suite: `142 passed, 29 failed`; failures were expected migration points
  where pre-V0.6 workflow fixtures had no briefing response or asserted old budgets/
  identifiers. They remain open for integrated migration, not treated as acceptance.
- Commit: `2fc3a02 Add sampling-free review briefing gate`.

### PKG-019 — Context gaps and budgets

- Status: completed.
- Assignment: Main Worker, no delegation.
- Changed files: `guided.py`, `orchestration.py`, `prompt_builders.py`,
  `deliberation.py`, budget migration assertion in `test_r3_workflow.py`, new
  `test_v22_context_gaps.py`.
- Final package replay command: `.venv\Scripts\python.exe -m pytest -q
  tests\integration\test_v22_context_gaps.py
  tests\integration\test_v22_briefing.py
  tests\unit\test_v22_models_persistence.py tests\unit\test_roles_v2.py
  tests\unit\test_runtime_v2.py --basetemp .tmp\campaign003-r1-final-pkg019-exact -p
  no:cacheprovider` -> exit 0, `34 passed in 0.32s`. Covered invalid-gap isolation,
  valid/duplicate/already-
  answered/generic/immaterial selection, two-question form, accepted affected-role-only
  reconsideration, decline/unsupported, separate provenance, and forced lightweight
  budget insufficiency at exactly six samples.
- Commit: `193f624 Add guided context gaps and bounded forms` (combined with PKG-020
  after sequential implementation because both modify the same hotspots).

### PKG-020 — Shared concise forms

- Status: completed.
- Assignment: Main Worker, no delegation.
- Changed files: `deliberation.py`, `orchestration.py`, new `test_v22_forms.py`.
- Final package replay command: `.venv\Scripts\python.exe -m pytest -q
  tests\unit\test_v22_forms.py tests\integration\test_v22_briefing.py
  tests\integration\test_v22_context_gaps.py --basetemp
  .tmp\campaign003-r1-final-pkg020 -p no:cacheprovider` -> exit 0,
  `16 passed in 0.27s`.
  All schema titles <=48, descriptions <=160, flat primitive fields, no hashed internal
  IDs, deterministic anchor/category outcome title, and exact selected outcome mapping.
- Commit: `193f624 Add guided context gaps and bounded forms`.

### PKG-021 — Process digest and phase trace

- Status: completed.
- Assignment: Main Worker, no delegation.
- Changed files: new `localization/digest.py`; `orchestration.py`; new
  `test_v22_digest.py`.
- Final package replay command: `.venv\Scripts\python.exe -m pytest -q
  tests\integration\test_v22_digest.py tests\integration\test_v22_context_gaps.py
  tests\integration\test_v22_briefing.py --basetemp .tmp\campaign003-r1-final-pkg021 -p
  no:cacheprovider` -> exit 0, `17 passed in 0.30s`. Verified frozen 12-section order,
  six active-role lenses, blind spots before
  verdict, minority counterfactual, semantic dedupe, hidden-key exclusion, <=8,000
  display, review-only compact output, exact 13-phase trace, and the deep standard
  6+3+1+3 sample order at exactly 13 calls.
- Commit: `a874a6e Add process-first review digest`.

### PKG-022 — Migration, integration, packaging and docs

- Status: completed.
- Assignment: Main Worker, no delegation.
- Changed files: package/module version and lock metadata; server/tool diagnostics and
  actual FastMCP `briefing_mode` enum schema; README/AGENTS/architecture/tool contract;
  accepted V0.5 workflow fixtures migrated with explicit `briefing_mode=off`; V2.2
  continuation/privacy/public-surface regressions.
- Final package replay command: `.venv\Scripts\python.exe -m pytest -q
  tests\integration\test_tool_surface_v2.py tests\integration\test_v22_briefing.py
  --basetemp .tmp\campaign003-r1-final-pkg022 -p no:cacheprovider` -> exit 0,
  focused migration suite `16 passed in 1.04s`; final full suite `182
  passed in 1.83s`; compile passed; docs/constants assertion scan passed; obsolete
  version/build/budget scan returned zero; AST import scan returned no unused imports.
- Commit: `1fb8bcd Migrate guided review contract to V0.6`.
- Final metadata count follow-up: metadata records retain safe context asked/answered
  counts after reload; focused `9 passed in 0.30s`, full `182 passed in 2.46s`; commit
  `3de6e5f Retain safe guided metadata counts` (sixth/final Campaign commit).

## Final integrated verification

- Final HEAD: `3de6e5fafb0d6a0a4347b68469e99ce7ef8bc816`.
- Commit count from baseline: 6.
- Exact final compile/full command:
  `python -m compileall src tests; .venv\Scripts\python.exe -m pytest -q
  --basetemp .tmp\campaign003-r1-pytest-postbuild -p no:cacheprovider` -> compile
  success; `182 passed in 1.83s`.
- Named focused integrated suite across V2.2 models/forms/briefing/context/digest,
  continuation, suppression, elicitation, reconsideration and tool surface -> `59
  passed in 1.36s`.
- Printed Core probe: auto brief action `accept`; six asked fields; briefing precedes
  sampling; effective/plan content type `ui`; confidence `full`; sampling 6;
  briefing calls 1; status `COMPLETED`; exact 13-phase order; six role lenses; display
  length 830. Public probe: exact five tools, actual enum `auto|always|off`, default
  `auto`, schema 2.2, build `guided-deliberation-v4`, budgets 6/13/18.
- Fresh build command: `$env:UV_CACHE_DIR='.tmp\campaign003-r1-uv-cache'; uv build
  --out-dir .tmp\campaign003-r1-dist` -> success.
- Artifacts: wheel 70,329 bytes, SHA-256
  `C52779316470EA7F0F7AA59D83CAF4964B070CA31667B35065846257311790B9`;
  sdist 63,926 bytes, SHA-256
  `35CA90DBAE659844558EA6363E9CF0D2C1F12F6ABDA0FD05FCA45BE8A211983E`.
- Fresh repository-local Python 3.12 venv installed the wheel. `python -I` smoke:
  distribution/module `0.6.0`, build/schema exact, exact five tools, briefing schema
  exact, budgets exact, guided Core briefing accepted with six samples/six lenses and
  display length 830.
- Baseline-to-final audit: 34 changed files, all matched allowed-path rules; disallowed
  count 0; `git diff --check <baseline>..HEAD` exit 0; index empty; complete six-commit
  diff inspected.
- Dead-reference scan: no `0.5.0`, `outcome-first-decision-v3`, or `6/10/14` in
  source/tests/docs/version files. `ruff` was unavailable; bounded AST import scan of
  changed production modules found no unused imports.
- Protected SHA-256 values all exactly match admission; final status contains only the
  original protected Foreman/user dirt plus this Campaign ledger/report.

## Deviations, skips, escalations and risks

- Admission compile/test was first invoked as one combined command, whose output was
  truncated by the tool transport. Both commands were rerun separately; evidence above.
- Skipped checks: none so far.
- Permission escalations: 12 scoped Git operations (six `git add`, six `git commit`)
  after the initial sandboxed stage was denied by `.git/index.lock`; every staged-name
  and cached-diff check excluded Harness/user assets.
- External calls: 0.
- Package installation network reads: one allowed isolated-wheel dependency resolution;
  five dependency artifacts were downloaded into the repository-local uv cache. No
  publish, deploy, credentials, Goose, model or provider call occurred.
- Deviations: first combined admission output was transport-truncated and rerun
  separately; first isolated smoke used the development FastMCP `get_tools()` API and
  failed under installed FastMCP 3.4.7, then passed using that version's public
  `list_tools()` introspection; one protected-review hash command used a stale filename
  and was rerun against actual `reviews/20260810_145151.json`.
- Skipped: live Goose/provider calls (contract prohibited/not required); `ruff` absent,
  replaced with AST import scan. No required compile/test/build/smoke/diff/hash check
  skipped.
- Remaining risks: live Goose/provider rendering remains for Foreman validation; fresh
  wheel resolved FastMCP 3.4.7 under the existing dependency range while the development
  environment exposes an older introspection method, though both actual schemas and
  guided Core paths passed. Campaign acceptance remains reserved for Foreman.
