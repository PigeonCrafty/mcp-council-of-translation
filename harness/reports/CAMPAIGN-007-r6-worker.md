# CAMPAIGN-007-r6 Main Worker Report

## Status and authority

- Worker outcome: `READY_FOR_REVIEW`; Foreman acceptance, publication and Q-011
  acceptance are not claimed.
- Role/mode: `WORKER / MAIN WORKER`, `STRICT_CAMPAIGN`.
- Contract: `harness/contracts/CAMPAIGN-007-r6.md`.
- Verified contract SHA-256:
  `00A1B7FC7F0B8ED5C7252C5723BB5647F192C4DC2A827CCB7E05EC30F1D646A4`.
- Exact admitted baseline:
  `116f2297c035c006bbd0419e802691ec5f30c0c8`
  (`Accept V0.9 lock publication fix`).
- Final HEAD: `516db0ea88ec69cdd7df5e3490eb8aa08b74eca3`.
- Subagents: forbidden / 0. Campaign authority escalations: 0.
- Live Goose/provider/model calls: 0. Push/PR/release/deployment actions: 0.

## Admission and boundaries

Admission passed before editing:

- exact HEAD/subject, zero post-baseline commits and empty index;
- exact r6 contract SHA-256 and baseline test SHA-256
  `FB5A0F980CEE9BE5B64278EF0FD7FD89766D3C6714AB6217E27C919CBFF5601B`;
- all 15 protected hashes exact, including production orchestration/runtime, `uv.lock`,
  `pyproject.toml`, CI workflow, accepted r5 evidence and user assets;
- only the declared Foreman/user dirty set was present and preserved.

The authorized implementation boundary was only
`tests/integration/test_orchestration_v2.py`; this required r6 report is intentionally
uncommitted. No production, lock, dependency, workflow, documentation or Harness-state
file was changed.

## Test-only correction

`DelayedContinuationExecutor.sample()` now:

1. captures `perf_counter()` immediately before the existing
   `await asyncio.sleep(0.02)`;
2. measures elapsed milliseconds after the await;
3. records the bounded positive integer duration in the existing `RuntimeEvent`.

The fixed `sampling_wait_ms == 20` and `15 <= wall_clock_ms` assertions were replaced by
the required semantic relation:

```text
0 < sampling_wait_ms <= wall_clock_ms < 2_000
```

The existing asynchronous delay and exactly-one-call assertion remain. Parent byte
immutability, child linkage, persistence, concurrency provenance, coverage, status,
schema and all other assertions in the test were unchanged.

## Pinned environment and verification

All environment commands used repository-local
`.tmp/campaign007-r6-uv-cache` and `.tmp/campaign007-r6-uv-tools` with exact
`uv 0.12.3 (507230998 2026-08-07 x86_64-pc-windows-msvc)`.

- `uv lock --check`: passed, 78 packages.
- `uv sync --locked --group dev --python 3.12`: passed/checked 72 packages.
- Runtime interpreter: Python 3.12.9 on Windows.
- Corrected named continuation test: 20 independent invocations, each with a unique
  repository-local `--basetemp`; `20/20` passed. Individual runs completed in
  0.21–0.43 seconds.
- Timing-focused files (`test_orchestration_v2.py`,
  `test_parallel_orchestration.py`, `test_v22_briefing.py`):
  `23 passed in 1.11s`.
- `python -m compileall -q src tests`: passed.
- Complete suite with disabled pytest cache and repository-local basetemp:
  `246 passed in 4.37s`.
- Public invariants: distribution/package `0.9.0`, module `0.9.0`, diagnostic build
  `bounded-parallel-council-v7`, schema `2.3`, exact five tools and budgets `6/13/18`.
- `uv.lock` SHA-256 remained exact:
  `1CED44E8A6D0F88691A83FFC5B214232CAAA6E437BA5EC8820B5EDADA5C65E9D`.

No required check was skipped. Artifact build and live calls were not required and were
not performed.

## Commit, scope and final Git state

Exactly one local test-only commit was created:

- `516db0ea88ec69cdd7df5e3490eb8aa08b74eca3` —
  `Stabilize continuation timing regression`

The baseline-to-HEAD committed scope is exactly one authorized path:
`tests/integration/test_orchestration_v2.py`, with 10 insertions and 3 deletions.
The final test SHA-256 is
`02CC3FFFAE04E9532E07E810AB67D33BBCC1237C4D910229D75B86B0DD546804`.
Textual scope inspection and `git diff --check` passed. The Git index is empty and all
15 protected hashes remain exact.

The remaining worktree dirt is exactly the admitted Foreman/user state plus this
required untracked r6 Worker report. No protected asset was staged or committed.

## Operations, deviations and remaining risk

- External dependency operations: one pinned uv 0.12.3 download/install into the
  repository-local tool directory. The locked sync performed no dependency upgrade.
- Initial sandboxed `git add` failed because `.git/index.lock` was not writable. The
  exact authorized staging command and commit were rerun with narrow filesystem
  elevation. Sandbox elevations: 2; Campaign authority escalations: 0.
- No implementation deviation occurred. No production clock monkeypatch, platform
  skip, retry, loosened upper bound, production change, lock/workflow/dependency change,
  push or PR #15 update occurred.
- Remaining external risk is the independent PR #15 CI rerun and post-publication
  normal-Goose Q-011 evidence, both outside Worker authority.
