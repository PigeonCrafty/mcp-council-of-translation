# Foreman Review: CAMPAIGN-007-r6

## Decision

`ACCEPTED`

CAMPAIGN-007-r6 removes the Windows short-timer assumption from the continuation timing
regression while preserving the test's original zero-wall protection and every
production invariant.

## Control and scope

- Contract SHA-256:
  `00A1B7FC7F0B8ED5C7252C5723BB5647F192C4DC2A827CCB7E05EC30F1D646A4`
- Baseline: `116f2297c035c006bbd0419e802691ec5f30c0c8`
- Accepted final HEAD: `516db0ea88ec69cdd7df5e3490eb8aa08b74eca3`
- Exactly one commit: `516db0e Stabilize continuation timing regression`
- Exact scope: `tests/integration/test_orchestration_v2.py`, 10 insertions and three
  deletions; no production, lock, workflow or dependency change
- Baseline-to-final scope/textual audit and `git diff --check`: passed

## Corrected evidence

- The test executor measures actual `perf_counter` elapsed time around its existing
  asynchronous delay instead of recording a fabricated 20ms.
- The semantic assertion is
  `0 < sampling_wait_ms <= wall_clock_ms < 2_000`.
- Exactly one sample, parent immutability, child linkage, persistence, schema, coverage,
  status and inherited concurrency provenance assertions remain unchanged.

## Independent Foreman verification

- Exact uv 0.12.3 lock check and locked Python 3.12 dev sync: passed.
- Named continuation test in twenty independent Windows/Python 3.12 processes with
  unique repository-local basetemps: `20/20 passed`.
- Timing-focused integration files: `23 passed in 1.07s`.
- Compile: passed.
- Complete suite: `246 passed in 3.91s`.
- Package/module 0.9.0, build `bounded-parallel-council-v7`, schema 2.3, exact five
  tools and budgets 6/13/18 remain unchanged.
- `uv.lock` remains exact at
  `1CED44E8A6D0F88691A83FFC5B214232CAAA6E437BA5EC8820B5EDADA5C65E9D`.
- All protected hashes matched; index empty; user assets preserved.

## Remaining gate

The correction requires a fresh six-job PR #15 run. Q-011 remains post-publication and
is not accepted by this test-only revision.

