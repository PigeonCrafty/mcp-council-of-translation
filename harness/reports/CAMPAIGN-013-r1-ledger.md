# CAMPAIGN-013-r1 Execution Ledger

## Control

- HARNESS_ROLE: `WORKER / MAIN WORKER`
- HARNESS_MODE: `STRICT_CAMPAIGN`
- Contract: `harness/contracts/CAMPAIGN-013-r1.md`
- Contract SHA-256: `D11C672105A740BFD2413C9794878BF6BD1FB7011C3407406ED45B50B20A29B5`
- Baseline: `44b1969677cd6b1fda63047ca514aede6609bdad`
- Commit policy: exactly five scoped local commits, one per PKG-075 through PKG-079
- Acceptance authority: Foreman only

## Admission

- Required pigeon-harness skill, common/Worker protocols, repository instructions,
  contract, plan, features, progress, design assessment and prior live review were read.
- HEAD and local `origin/main` both matched the exact baseline.
- Git index was empty; the product/source/test/package diff against baseline was empty.
- Non-recursive status contained only the admitted three tracked Foreman Harness files
  and contract/user untracked assets.
- Contract SHA-256 and all five contract-listed protected hashes matched.
- `.venv\\Scripts\\python.exe -m compileall -q src tests`: PASS.
- Complete admission suite with repository-local basetemp: `444 passed in 4.27s`.
- Forbidden `.learnings/**`, `reviews/**`, `myTest/**`, user audit Markdown and other
  user-owned untracked content were not read, traversed, copied or hashed.

## Package state

| Package | State | Executor | Commit | Evidence |
| --- | --- | --- | --- | --- |
| PKG-075 | complete | Main Worker | `6a07f4e` | direct truth table `19 passed`; combined model suite `29 passed`; compile/diff checks PASS |
| PKG-076 | blocked, uncommitted | Main Worker | none | affected matrix `129 passed, 1 deselected`; full suite `10 failed, 467 passed`; 7 failures require changes to forbidden tests or violation of frozen safety rule |
| PKG-077 | not started | Main Worker | none | blocked by PKG-076 |
| PKG-078 | not started | Main Worker | none | blocked by PKG-076 |
| PKG-079 | not started | Main Worker | none | blocked by PKG-076 |

## Counts

- Campaign subagents created/used: `0`
- Authority escalations: `1` (local staging/commit only)
- Dependency operations: `0`
- Live Goose/provider/model calls: `0`
- Remote Git/GitHub calls: `0`
- Push/PR/release/publication/deployment calls: `0`

## Deviations and incidents

- A read-only `rg` command used the Unix-style path glob
  `src/council_of_translation/localization/*.py`; Windows rejected that one path
  argument with `os error 123`. No file changed. Subsequent searches use
  `-g "*.py"` against the directory. The self-improvement protocol was read after
  the error; its normal `.learnings/**` log is prohibited by this Campaign, so
  this ledger and the Worker report are the only incident records.
- The first ledger update patch expected a section that did not yet exist and was
  rejected without changing the file; this corrected append used the observed EOF.
- The first PKG-075 focused run exposed a test expectation typo
  (`none_reviewer_coverage` instead of the frozen `no_reviewer_coverage`); production
  behavior was correct. The assertion was corrected and the complete focused suite was
  rerun.
- The first PKG-076 affected matrix failed because direct classifier fixtures declared
  Schema 2.6 before finalization and legacy persistence fixtures reached the new writer
  with `not_recorded`. The fix keeps classifier fixtures provisional, makes the single
  finalizer own the 2.6 transition, and invokes it on write copies only; historical reads
  remain non-mutating and `not_recorded`.
- PKG-076 focused rerun: `129 passed, 1 deselected in 1.31s`. The one deselection is a
  verification-receipt assertion intentionally owned by downstream PKG-077.
- PKG-076 full regression: `10 failed, 467 passed in 4.76s`. Three failures are
  downstream schema/receipt expectations in authorized PKG-077/079 paths. Seven are
  frozen-behavior contradictions in forbidden paths:
  `tests/integration/test_r3_outcome_suppression.py` (3 failures) and
  `tests/integration/test_r3_workflow.py` (4 failures). They require
  `COMPLETED_WITH_FALLBACK` for degraded execution or non-delegation runtime fallback,
  while this contract requires `insufficient` and forbids a permissive terminal outcome.
  Editing those files is outside the exact allowlist; preserving their assertions would
  violate the classification and one-way safety rules. The Campaign therefore stopped
  BLOCKED without committing PKG-076.

## Handoff state

- Final committed HEAD: `6a07f4ebc61146e60af8bb6e7456f2b144ce15a4`
- Commits created: `1/5`; only PKG-075 is committed.
- Git index: empty.
- PKG-076 remains an explicitly reported uncommitted intermediate in authorized paths.
- Protected hashes at stop match admission exactly.
- Required PKG-077 through PKG-079 checks, final complete regression, release migration,
  fresh artifacts and isolated-wheel smoke were not run because the contractual stop
  condition was reached.
- Worker-created `.tmp/campaign013-worker` resolved to the exact repository-local
  authorized path and was removed; post-cleanup `Test-Path` returned `False`.
