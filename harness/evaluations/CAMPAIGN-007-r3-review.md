# Foreman Review: CAMPAIGN-007-r3

## Decision

`CHANGES_REQUESTED`

The Worker correctly stopped at the contract's lock-format drift condition and made no
commit. The implementation is not defective; the r3 contract failed to pin the lock
generator to the CI toolchain.

## Independent diagnosis

- Baseline/current HEAD remained
  `11fb742cda602d33cb66550d0f3d665234bd4193`; index remained empty.
- The Worker used the available system `uv 0.6.13`, which downgraded lock revision 3 to
  revision 1 and removed upload-time metadata while updating the root version.
- CI explicitly installs `uv 0.12.3`; the repository's revision-3 lock was created and
  maintained by the newer format.
- Foreman reproduced the correction in an isolated `.tmp` project restored from the
  exact baseline. `uv 0.12.3` resolved the same 78 packages and changed exactly one
  line: the editable root package version `0.8.0` to `0.9.0`. Lock revision, artifact
  metadata, dependencies, sources and hashes remained unchanged.

## Required revision

CAMPAIGN-007-r4 must pin both the executable and caches: invoke `uv 0.12.3` through a
repository-local `UV_TOOL_DIR` and `UV_CACHE_DIR`, normalize the existing uncommitted r3
intermediate lock, require the exact one-line baseline-to-final diff, and run locked
sync/compile/full tests with that same uv version. No production or dependency change is
authorized.

The r3 Worker report is accepted as truthful blocked evidence. F-035 through F-039 and
the r2 implementation acceptance remain unchanged; publication PR #15 and Q-011 remain
pending.

