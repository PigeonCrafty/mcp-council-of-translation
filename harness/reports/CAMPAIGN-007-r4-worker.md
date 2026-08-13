# CAMPAIGN-007-r4 Main Worker Report

## Status and authority

- Worker outcome: `BLOCKED`; Foreman acceptance, publication and Q-011 acceptance are
  not claimed.
- Role/mode: `WORKER / MAIN WORKER`, `STRICT_CAMPAIGN`.
- Contract: `harness/contracts/CAMPAIGN-007-r4.md`.
- Verified contract SHA-256:
  `38D15B4ADC36FEBF7D63FB6DB98DE05CE69A30BE06EC1BE2662437E5696C510D`.
- Exact admitted baseline/current HEAD:
  `11fb742cda602d33cb66550d0f3d665234bd4193`
  (`Accept bounded parallel Council V0.9`).
- Subagents: forbidden / 0. Campaign authority escalations: 0.
- Live Goose/provider/model calls: 0. Push/PR/release/deployment actions: 0.

## Admission

Admission passed before invoking the pinned toolchain:

- HEAD and subject matched exactly; zero commits followed the baseline; index was empty.
- The r4 contract hash and all 17 protected-asset hashes matched.
- The existing unstaged `uv.lock` exactly matched the admitted r3 intermediate SHA-256
  `94409C5B068B84B029A15F183C3BF028DE4C19E6DF65D3E6B4781F0BA93B442E`.
- The admitted intermediate had 78 packages, revision 1, zero `upload-time` entries,
  root version 0.9.0 and the declared 596/596 baseline diff.
- The protected Foreman/user dirty set was preserved.

## Pinned toolchain evidence

Both environment directories were dedicated repository-local paths:

- `UV_CACHE_DIR=.tmp/campaign007-r4-uv-cache`
- `UV_TOOL_DIR=.tmp/campaign007-r4-uv-tools`

The exact required bootstrap/invocation reported:

```text
uv tool run --from uv==0.12.3 uv --version
uv 0.12.3 (507230998 2026-08-07 x86_64-pc-windows-msvc)
Downloading uv (19.3MiB)
Installed 1 package in 20ms
```

The canonical regeneration command was then run with the same local directories:

```text
uv tool run --from uv==0.12.3 uv lock
Resolved 78 packages in 1ms
```

## Blocking result

Pinned uv 0.12.3 treated the revision-1 intermediate as current and made no file
change. Immediate baseline-to-worktree inspection remained:

- `uv.lock`: `596 insertions(+), 596 deletions(-)`;
- header revision: `1`, not required `3`;
- `upload-time` entries: `0`, not required `586`;
- package entries: 78; root entry: one;
- SHA-256 unchanged at
  `94409C5B068B84B029A15F183C3BF028DE4C19E6DF65D3E6B4781F0BA93B442E`.

The broad diff still contains the r3 format rewrite plus the root version change, so it
fails r4 acceptance criterion 2 and the explicit stop condition. The Worker did not
attempt uncontracted `--refresh`/`--upgrade` flags, manually restore or edit generated
content, stage the lock, or create a commit.

## Verification and skipped checks

Completed:

- exact baseline/subject/zero-commit/empty-index admission;
- exact r4 contract, admitted intermediate and 17 protected hashes;
- local-cache/local-tool bootstrap of exact uv 0.12.3;
- canonical pinned `uv lock` invocation;
- immediate baseline-to-worktree textual and lock-invariant audit.

Skipped because the exact-diff stop condition requires immediate `BLOCKED`:

- pinned `uv lock --check`;
- pinned `uv sync --locked --group dev`;
- pinned `uv run --frozen` compile and expected `246 passed` full suite;
- package/module/build/schema/five-tool/budget probes;
- the required commit, because staging is forbidden when the diff is not exact;
- fresh artifacts and live calls (not required by contract).

## Git state, external operations and remaining blocker

- Current HEAD remains the required baseline; commits created: 0; index remains empty.
- `uv.lock` remains the exact admitted unstaged r3 intermediate.
- No protected asset was edited, staged, deleted, moved or committed. This r4 report is
  required and intentionally uncommitted.
- External dependency operations: 1 pinned uv 0.12.3 download/install into the local
  tool directory. Dependency sync/install operations: 0. Live calls: 0.

Remaining blocker: direct canonical `uv lock` under the required pinned tool does not
upgrade an already-current revision-1 lock or recover removed artifact metadata. The
contract needs to authorize a deterministic baseline restoration before pinned
regeneration, or specify another exact uv operation that reconstructs revision 3 while
preserving the dependency graph. The Worker has no authority to infer that operation.
