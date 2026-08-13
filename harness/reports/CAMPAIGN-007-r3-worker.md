# CAMPAIGN-007-r3 Main Worker Report

## Status and authority

- Worker outcome: `BLOCKED`; Foreman acceptance, publication and Q-011 acceptance are
  not claimed.
- Role/mode: `WORKER / MAIN WORKER`, `STRICT_CAMPAIGN`.
- Contract: `harness/contracts/CAMPAIGN-007-r3.md`.
- Verified contract SHA-256:
  `FF1EF1903B4B430CC984BEB685BFCE9AF1CB375B8E7800D3BA99C913ADC680A6`.
- Exact admitted baseline and current HEAD:
  `11fb742cda602d33cb66550d0f3d665234bd4193`
  (`Accept bounded parallel Council V0.9`).
- Implementation subagents: forbidden / 0 used.
- Campaign authority escalations: 0. Sandbox approval escalations: 0.
- Live Goose/provider/model calls: 0. Push/PR/release/deployment actions: 0.

## Admission and protected state

Before regeneration, the Main Worker completely read AGENTS, plan, features, progress,
the r3 contract, publication CI review, and the r1/r2 contracts, Foreman reviews and
Worker reports/ledger, plus the pigeon-harness common and Worker protocols. Admission
verified:

- exact HEAD and subject;
- empty Git index and zero commits after the required baseline;
- the declared protected Foreman/user dirty set only;
- exact r3 contract hash and all 14 protected-asset hashes (15 hashes including the
  contract);
- `pyproject.toml` version `0.9.0` and the stale root editable `uv.lock` entry at
  `0.8.0`.

The pre-change counterexample used only the repository-local cache
`.tmp/campaign007-r3-uv-cache`:

```text
uv lock --check
Resolved 78 packages in 8.00s
error: The lockfile at `uv.lock` needs to be updated, but `--locked` was provided.
```

## Canonical regeneration and blocking diff

With `UV_CACHE_DIR` set to the same repository-local directory, canonical `uv lock`
reported:

```text
Resolved 78 packages in 57ms
Updated council-of-translation v0.8.0 -> v0.9.0
```

The executing binary was `uv 0.6.13 (a0f5c7250 2025-04-07)`. Immediate textual audit
showed unauthorized lock-format drift in addition to the permitted root version change:

- `uv.lock`: `596 insertions(+), 596 deletions(-)`;
- lock header `revision = 3` changed to `revision = 1`;
- 586 existing `upload-time` metadata occurrences were removed and none were added;
- wheel/sdist lines throughout the resolved graph were rewritten;
- the permitted root editable package version changed from `0.8.0` to `0.9.0`;
- the package count remained 78 and the root editable entry remained unique.

This violates the contract's exact-diff requirement and its prohibition on changing
lock format or any metadata beyond the root project version. Per the explicit stop
condition, the generated `uv.lock` was not restored, manually edited, staged or
committed. No attempt was made to hide or normalize the drift.

## Verification and skipped checks

Completed:

- exact baseline/subject/index/dirty-set admission;
- contract and protected-hash admission: all exact;
- stale-lock `uv lock --check` counterexample with local cache: failed as expected;
- canonical `uv lock` with local cache: completed;
- immediate semantic/textual diff audit: failed the exact-diff gate;
- current commit count after baseline: 0;
- current Git index: empty.

Skipped because the contract requires an immediate `BLOCKED` stop after extra lock
drift:

- post-change `uv lock --check`;
- `uv sync --locked --group dev`;
- compile and the expected `246 passed` full suite;
- version/build/schema/five-tool/budget probes;
- local commit (required only when the diff is exact);
- fresh build (also not required by this contract).

## Current Git state and handoff risk

- Current HEAD remains the required baseline; no commit was created.
- Git index is empty.
- Modified paths are the admitted Foreman-owned `harness/plan.md` and
  `harness/progress.md`, plus the intentionally uncommitted generated `uv.lock` drift.
- Untracked protected assets remain `.learnings/`, `reviews/`, the audit Markdown, the
  r3 contract and publication review; this required Worker report is additionally
  untracked.
- No protected asset was edited, staged, deleted, moved or committed.
- External dependency actions: one canonical/local-cache lock resolution; dependency
  installation actions: 0; live/external service calls: 0.

Remaining blocker: the available canonical uv version rewrites lock revision and
artifact metadata. A Foreman-authorized next step must supply or approve a compatible uv
toolchain or revise the contract. The Worker has no authority to restore the generated
file, manually patch the lock, commit the broad rewrite or continue verification.
