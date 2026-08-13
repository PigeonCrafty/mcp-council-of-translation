# Foreman Publication Review: CAMPAIGN-007

## Decision

`CHANGES_REQUESTED`

CAMPAIGN-007-r2 remains `ACCEPTED` for implementation. Publication PR #15 is not
acceptable yet because all six required Windows/Linux CI jobs stop at the locked
environment admission step before compile or tests.

## Exact failure

- PR: `https://github.com/PigeonCrafty/mcp-council-of-translation/pull/15`
- Failed workflow run: `31668117294`
- Failing command: `uv sync --locked --group dev`
- Root cause: `pyproject.toml` declares package version `0.9.0`, while the root package
  entry in `uv.lock` still declares `0.8.0`.
- Independent local reproduction with a repository-local cache: `uv lock --check`
  resolves the project and then rejects the stale lockfile.
- The failure is identical across the six Python/OS matrix jobs and occurs before any
  production test. It does not invalidate the accepted scheduler, telemetry or record
  finalization evidence.

## Required correction

Issue CAMPAIGN-007-r3 as a lockfile-only work order. Regenerate `uv.lock` from the
already accepted `pyproject.toml`; accept only the expected root-project metadata change.
Any dependency addition, removal or version/source change is a stop condition. Re-run
the exact locked sync plus compile/full suite before Foreman updates PR #15.

Q-011 remains pending until the corrected publication passes CI and the exact published
commit is exercised in normal Goose.

