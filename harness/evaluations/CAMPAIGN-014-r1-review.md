# CAMPAIGN-014-r1 Foreman Review

- Decision: `CHANGES_REQUESTED`
- Reviewed Worker report: `harness/reports/CAMPAIGN-014-r1-worker.md`
- Reviewed ledger: `harness/reports/CAMPAIGN-014-r1-ledger.md`
- Contract: `harness/contracts/CAMPAIGN-014-r1.md`
- Contract SHA-256:
  `4FBCF691DF9702587EC6A5D2F5FB1215D4440D3A6229ACBA1D4A969C7F09B2A0`
- Original baseline: `4f976c2764a463dceb403084fa3faead5300211e`
- Reviewed HEAD: `742128a1dfc2282d7aad4ee016d37ff94922c9ca`
- Review date: 2026-08-25 Asia/Shanghai

## Outcome

The Worker stop is procedurally correct, but CAMPAIGN-014 is not yet accepted. The seven
scoped PKG-080 through PKG-086 commits are preserved. PKG-087 cannot complete under r1
because `tests/unit/test_persistence_v2.py` was omitted from the exact allowlist even
though its two parameterized release assertions must follow the truthful V0.13.1 runtime
identifiers. A bounded r2 contract shall add only that missing path and finish the
already-authorized release migration.

## Independent evidence

- HEAD and the seven reported commits match; Git index is empty.
- The committed baseline-to-HEAD diff contains 21 paths, all inside the r1 allowlist,
  with `1167 insertions / 103 deletions`; `git diff --check` passes.
- All 14 r1 protected hashes match exactly.
- The PKG-087 intermediate is confined to the eight reported authorized paths. Its
  package/module/build identifiers are consistently `0.13.1` /
  `truthful-boundaries-council-v11.1`, and the canonical lock diff is limited to the
  editable root version and FastMCP upper bound.
- Independent focused replay produced exactly `31 passed, 3 failed`:
  - `test_new_write_persists_truthful_v0130_runtime_and_version_identifiers[full]`;
  - `test_new_write_persists_truthful_v0130_runtime_and_version_identifiers[metadata]`;
  - `test_server_info_and_versioned_defaults`.
- The first two failures compare correct V0.13.1 persistence output against stale
  V0.13.0/v11 constants in the omitted unit-test path. The third compares the same
  correct runtime identifiers against stale constants in an r1-authorized integration
  test.
- No production workaround is warranted. Making runtime identifiers conditional or
  retaining the old values would make persisted records and diagnostics untruthful.

## Required correction

CAMPAIGN-014-r2 shall:

- preserve all seven committed packages and the exact admitted PKG-087 intermediate;
- add only `tests/unit/test_persistence_v2.py` to the implementation/test allowlist;
- migrate its test name and four stale identifier assertions, and migrate the stale
  tool-surface assertions already authorized by r1;
- keep persistence semantics, history-mode coverage, public tools, schemas, budgets,
  concurrency, routing and every F-064 through F-070 behavior unchanged;
- complete PKG-087 as the eighth and only new Campaign commit; and
- run every skipped r1 final check, including full regression, exact 30/30 Golden,
  fresh artifacts, archive inspection and both installed-wheel FastMCP smokes.

No other source, test, dependency, workflow, schema, prompt or behavior change is
authorized.

## Acceptance state

- F-064 through F-070 remain planned pending complete r2 evidence and independent
  Foreman acceptance.
- Q-016 remains planned and cannot be issued before local acceptance and protected-main
  publication.
- No push, PR, release, deployment or live Goose/provider action is authorized by this
  review.
