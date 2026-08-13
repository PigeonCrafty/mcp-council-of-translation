# CAMPAIGN-007-r1 Main Worker Ledger

## Control

- Role: WORKER / MAIN WORKER
- Mode: STRICT_CAMPAIGN
- Contract: `harness/contracts/CAMPAIGN-007-r1.md`
- Contract SHA-256: `A796CFF155AFC1BA0FDECBF5A33FFEA718D98F63F4C33FF335F931ABA8188F7A`
- Baseline: `f9651ed64daf86dd5fabac5e7437b9de8b3186bc`
- Subagents: forbidden / 0
- Live Goose/provider/model calls: 0

## Admission

- Exact HEAD/subject and empty index: pass.
- Declared Foreman/user dirt only; `myTest/` absent.
- Contract and all 10 protected hashes: exact; mismatch count 0.
- `.venv\Scripts\python.exe -m compileall -q src tests`: pass.
- Full baseline: `220 passed in 2.54s`.
- Reproduced baseline: six independent marketing roles ran sequentially with peak 1,
  start/completion order 0..5, 6 calls, accumulated `elapsed_ms=196`, and about 195ms
  observed batch wall time. No wall/concurrency/batch telemetry fields existed.

## Package state

| Package | State | Files | Verification | Commit |
| --- | --- | --- | --- | --- |
| PKG-037 | MAIN_WORKER_VERIFIED | runtime, concurrency unit test | `17 passed in 0.51s` | `707b6f2` |
| PKG-038 | MAIN_WORKER_VERIFIED | orchestration, parallel integration test | `22 passed`; integration+runtime `150 passed` | `eea1e09` |
| PKG-039 | MAIN_WORKER_VERIFIED | models, runtime, orchestration, compatibility, persistence, migration tests | `53 passed`; full `236 passed` | `93c4510` |
| PKG-040 | MAIN_WORKER_VERIFIED | review diagnostics, tool/config and parallel integration tests | `45 passed in 2.13s` | `189944c` |
| PKG-041 | MAIN_WORKER_VERIFIED | version constants, package, server/tool wording, docs, affected tests | focused `61 passed`; full `244 passed`; fresh sdist/wheel and isolated smoke pass | `61252ae` |

## Campaign verification

- Runtime/config/tool diagnostics: `30 passed in 2.25s`.
- Six-role orchestration, clean/partial/context/decision/reconsideration/deep paths:
  `25 passed in 0.47s`.
- V1/V2.0/V2.1/V2.2/V2.3 compatibility, full/metadata/off persistence and privacy:
  `34 passed in 0.28s`.
- Presentation, dual channel, exact tool surface, version/default/budget regressions:
  `34 passed in 1.13s`.
- Final compile: `.venv\Scripts\python.exe -m compileall -q src tests` passed.
- Changed-source AST dead-import scan: `DEAD_IMPORT_CANDIDATES 0`.
- Final full suite with disabled cache/repository basetemp: `244 passed in 3.30s`.
- Baseline-to-final `git diff --check`: pass; 21 authorized files,
  `616 insertions(+), 75 deletions(-)`.

## Structural, timing, phase and budget evidence

- Exact config table: missing -> `3/default`; `1`, `2`, `3` -> same integer and
  `configured`; empty, non-numeric, `0`, and `4` -> `1/invalid_fallback`.
- Delayed Core probe at limit 3: observed wall 52 ms, record wall 43 ms, accumulated
  sampling wait 36 ms, peak 3, 2 batches, 6 exact-once calls. Completion order differed
  from plan order; persisted order was the six-role plan order.
- Same probe at limit 1: observed wall 161 ms, record wall 153 ms, peak 1, 6 batches,
  6 exact-once calls and sequential/persisted plan order. The limit-3 observation was
  about 68% lower wall time than limit 1; structural peak/barrier assertions remain the
  primary evidence.
- Deep standard phase assertion passed with exactly:
  `INDEPENDENT x6 -> CONTEXT_RECONSIDERATION x3 -> DISCUSSION x1 -> OUTCOME_RECONSIDERATION x3`.
  Sampling calls equaled the 13-call standard budget. The accepted six-role plan and
  later phase trace remained ordered; lightweight/standard/strict budgets remain
  6/13/18.

## Artifacts and isolated wheel smoke

- Fresh wheel: `council_of_translation-0.9.0-py3-none-any.whl`, 78,323 bytes,
  SHA-256 `1460F2593BAF162EC40AD05786B7C55DDDBD777CE863F1F43B295C918A572AEC`.
- Fresh sdist: `council_of_translation-0.9.0.tar.gz`, 72,294 bytes,
  SHA-256 `A32EB2DEA9313A3CD55F323EDB0D8ABC91CCE52581CAF18F16B4D194BF9EC230`.
- Disposable CPython 3.12 environment installed the wheel with current resolved
  FastMCP 3.4.7. Isolated `-I` import resolved to that environment's `site-packages`.
- Installed package/module `0.9.0`, build `bounded-parallel-council-v7`, schema `2.3`,
  concurrency effective/max `3/3`, budgets 6/13/18 and exact five tools were observed.
- All five registered tools were called through the current FastMCP client. Primary
  text and structured content were both present; continuation parent linkage, full view,
  and listing passed. Installed Core probes reported peak/batches/calls `3/2/6` and
  `1/6/6` for parallel and sequential modes.

## Protected state

- Contract hash remained
  `A796CFF155AFC1BA0FDECBF5A33FFEA718D98F63F4C33FF335F931ABA8188F7A`.
- All 10 protected asset hashes matched the contract after implementation.
- Final index is empty. The final dirty/untracked set is the admitted Foreman/user set
  plus only this Campaign ledger and Worker report. No protected asset was staged or
  committed.

## Incidents, deviations and authority

- PKG-038 first focused run: `18 passed, 4 failed`. The new integration executor looked
  for a nonexistent `Role ID:` prompt marker, so its own role lookup raised before call
  accounting. The batch correctly isolated those exceptions. The test was corrected to
  use the existing JSON role-definition `"id"` marker; production scheduling was not
  changed for this test defect.
- PKG-039 first focused run: `51 passed, 1 failed`. One accepted model test still
  asserted the former authoritative write schema `2.2`; it was migrated to `2.3` and
  augmented with explicit V2.2 conservative-default coverage.
- PKG-039 first full migration run: `234 passed, 2 failed`. The continuation and literal
  runtime invariant tests likewise asserted the old write schema. Their new-write
  expectations were migrated to `2.3`; backward-read coverage remains explicit.
- PKG-040 first broad focused command used the system Python instead of the repository
  virtual environment; collection stopped because that interpreter has no FastMCP. No
  product assertions ran. Verification was immediately moved back to `.venv`.
- PKG-040 first `.venv` focused run: `44 passed, 1 failed`. The new assertion looked for
  operator-config provenance in the product `fallback_reason`; the implementation
  intentionally records this content-free diagnostic in `runtime_metadata.fallbacks`
  and its dedicated disposition field. The test was corrected to the contracted record
  diagnostic without degrading an otherwise successful review.
- Fresh build and isolated-environment commands initially lacked sandbox access to the
  user uv cache; the exact authorized commands were rerun with filesystem elevation.
- The first isolated smoke used the older FastMCP `get_tools()` enumeration method.
  Current FastMCP 3.4.7 exposes `list_tools()`; the smoke script was adapted and the
  complete run passed. Product/package code was not changed for this harness script.
- Ruff and pyflakes are not installed in the repository environment; no dependency was
  added. The required dead-import audit used a read-only AST name-binding scan across
  every changed production Python module and found zero candidates.
- Campaign authority escalations: 0. Sandbox filesystem elevations were limited to
  required local Git writes, uv cache access and artifact hashing.
- External dependency actions: 1 isolated uv resolution/install; live Goose/provider/
  model calls: 0. Subagents: 0. Push/PR/release/deploy: 0.
