# CAMPAIGN-007-r5 Main Worker Report

## Status and authority

- Worker outcome: `READY_FOR_REVIEW`; Foreman acceptance, publication and Q-011
  acceptance are not claimed.
- Role/mode: `WORKER / MAIN WORKER`, `STRICT_CAMPAIGN`.
- Contract: `harness/contracts/CAMPAIGN-007-r5.md`.
- Verified contract SHA-256:
  `F344D16FA84B32C275DCB55EF7D0B6769CE540CE374B6DED9F46E5E2FDE9B6C2`.
- Exact admitted baseline:
  `11fb742cda602d33cb66550d0f3d665234bd4193`
  (`Accept bounded parallel Council V0.9`).
- Final HEAD: `28817d6ea7a0d547ae89579d4597cea0fbae0b2b`.
- Subagents: forbidden / 0. Campaign authority escalations: 0.
- Live Goose/provider/model calls: 0. Push/PR/release/deployment actions: 0.

## Admission and boundaries

Admission passed before refresh:

- exact HEAD/subject, zero post-baseline commits and empty index;
- exact r5 contract hash and all 20 protected-asset hashes;
- exact admitted unstaged `uv.lock` SHA-256
  `94409C5B068B84B029A15F183C3BF028DE4C19E6DF65D3E6B4781F0BA93B442E`;
- admitted intermediate invariants: revision 1, zero upload-time entries, 78 packages,
  one root entry at version 0.9.0 and the declared 596/596 baseline diff;
- only the declared Foreman/user/r3/r4 dirty assets were present and preserved.

The authorized implementation boundary was only `uv.lock`; this required r5 Worker
report is intentionally uncommitted. No source, test, dependency declaration, workflow,
documentation, Harness state or user asset was changed.

## Pinned refresh and exact lock evidence

Dedicated repository-local paths were used throughout:

- `UV_CACHE_DIR=.tmp/campaign007-r5-uv-cache`
- `UV_TOOL_DIR=.tmp/campaign007-r5-uv-tools`

Pinned generator evidence:

```text
uv tool run --from uv==0.12.3 uv --version
uv 0.12.3 (507230998 2026-08-07 x86_64-pc-windows-msvc)
```

The one authorized refresh command completed:

```text
uv tool run --from uv==0.12.3 uv lock --refresh
Resolved 78 packages in 10.45s
```

Before sync or staging, the resulting `uv.lock` SHA-256 was exactly:

`1CED44E8A6D0F88691A83FFC5B214232CAAA6E437BA5EC8820B5EDADA5C65E9D`

Baseline-to-worktree inspection was exactly one insertion and one deletion:

```diff
 name = "council-of-translation"
-version = "0.8.0"
+version = "0.9.0"
 source = { editable = "." }
```

Lock invariants passed: revision 3, 586 `upload-time` entries, 78 package entries and
one editable root entry. No dependency version, edge, source, hash or lock-format drift
remained. `git diff --check` passed.

## Verification

Every required verification used the same pinned uv 0.12.3 and local directories:

- `uv lock --check`: passed; final repeat resolved 78 packages in 0.99 ms.
- `uv sync --locked --group dev`: passed; local editable installation synchronized from
  0.4.0 to 0.9.0.
- `uv run --frozen python -m compileall -q src tests`: passed.
- `uv run --frozen pytest -q -p no:cacheprovider` with repository-local basetemp:
  `246 passed in 3.69s`.
- Runtime invariants: distribution/package `0.9.0`, module `0.9.0`, diagnostic build
  `bounded-parallel-council-v7`, schema `2.3`, exact tools
  `continue_review`, `get_server_info`, `list_review_records`, `review_translation`,
  `view_review_record`, and budgets `6/13/18`.

No required check was skipped. Fresh artifacts and live calls were not required and
were not performed.

## Commit and final Git state

Exactly one local commit was created:

- `28817d6ea7a0d547ae89579d4597cea0fbae0b2b` —
  `Refresh V0.9 root lock metadata`

The commit contains only `uv.lock` with one insertion and one deletion. Final
baseline-to-HEAD name/status, numstat, textual diff and `git diff --check` all passed.
The target lock hash remains exact. The Git index is empty. All 20 protected hashes
remain exact.

Remaining worktree dirt is the admitted Foreman/user state plus the untracked r3/r4/r5
contracts/reviews/reports; no protected asset was staged or committed. This r5 report is
the only newly created r5 report asset and remains untracked as required.

## Operations, deviations and risk

- External dependency operations: 1 pinned uv 0.12.3 download/install into the local
  tool directory. The locked sync changed only the disposable/repository virtual
  environment, not the dependency graph.
- First sandboxed `git add -- uv.lock` failed because `.git/index.lock` was not writable.
  The exact staging operation and subsequent commit were rerun with narrow filesystem
  elevation. Sandbox escalations: 2; Campaign authority escalation: 0.
- No implementation deviation occurred. No manual edit, Git restore, `--upgrade`, other
  lock operation, push or PR #15 update occurred.
- Remaining external risk is publication CI and later normal-Goose Q-011 evidence,
  both reserved to the Foreman/post-publication process.
