# CAMPAIGN-013-r2 Foreman Review

- Decision: `CHANGES_REQUESTED`
- Reviewed Worker report: `harness/reports/CAMPAIGN-013-r2-worker.md`
- Reviewed ledger: `harness/reports/CAMPAIGN-013-r2-ledger.md`
- Contract: `harness/contracts/CAMPAIGN-013-r2.md`
- Contract SHA-256:
  `0FD5641A76FB859C14FB4D331B00E38931AEA98589C5D580F0E675DB4537B4E2`
- Original baseline: `44b1969677cd6b1fda63047ca514aede6609bdad`
- r2 admission baseline: `6a07f4ebc61146e60af8bb6e7456f2b144ce15a4`
- Reviewed HEAD: `b01461b792ecb5eeda20229d47a404015ec6910c`
- Review date: 2026-08-25 Asia/Shanghai

## Outcome

The V0.13 product implementation is substantively complete and the five Campaign commits
are preserved. The Campaign is not yet accepted because one authoritative architecture
statement still identifies the verification wrapper as receipt Schema 1.0 even though the
implemented and frozen V0.13 contract is receipt Schema 1.1. This is a bounded release-
documentation defect, not a reason to reopen the decision-support design or production
implementation.

## Independent evidence

- Git HEAD is the reported `b01461b`; the index is empty and the original-baseline diff is
  exactly 32 r2-authorized paths with 1,395 insertions and 174 deletions.
- The r2 contract SHA-256 and all ten protected hashes match; the admitted Foreman/user
  dirty and untracked assets remain outside implementation scope.
- Independent full regression passed `480` tests. The independently selected classifier,
  legacy-migration, orchestration, receipt, presentation, Golden, tool-surface and release
  matrix passed `212` tests.
- The executable Golden corpus passed exactly `30/30`: all eight inherited metrics are
  `1.0`, decision-support accuracy and disposition coherence are `1.0`, and insufficient
  false reassurance is `0.0`.
- The lock remains revision 3 with 78 packages and 586 upload-time entries; its product
  drift is only the editable root version `0.12.1 -> 0.13.0`.
- A fresh Foreman build succeeded with pinned uv 0.12.3. Archive inspection found 31 wheel
  entries and 42 sdist entries with no temporary, build or dist paths. Hash differences
  from the Worker archives are attributable to non-reproducible archive metadata and do
  not alter installed content or acceptance semantics.
- Source, package metadata, README, tool-contract documentation and tests consistently
  identify package/module 0.13.0, build `calibrated-evidence-council-v11`, Review Schema
  2.6 and receipt Schema 1.1.
- `docs/v0.4-architecture.md` alone still says `receipt-schema 1.0 wrapper`. The filename
  is intentionally historical for path stability, but its content is authoritative for
  the current V0.13 architecture and therefore must say 1.1.

## Required correction

CAMPAIGN-013-r3 shall make one documentation-and-regression commit on top of `b01461b`:

1. Change the stale architecture statement from receipt Schema 1.0 to 1.1 without changing
   the surrounding retrieval, privacy or purity contract.
2. Extend the existing V0.13 release-contract test so this exact stale current-architecture
   wording cannot recur.
3. Change no production, schema, prompt, routing, adjudication, persistence, package,
   dependency, lock or public-tool file.
4. Re-run compile, the focused release contract, the complete regression and the final
   scope/protected-hash checks. Fresh package artifacts are not required because the r3
   paths are neither production nor packaged release inputs and fresh r2 Foreman build
   evidence already passed.

## Acceptance state

- F-059 through F-063 remain unaccepted until the bounded r3 correction passes independent
  Foreman review.
- Q-015 remains planned and cannot be issued before local acceptance and protected-main
  publication.
- No push, PR, release, deployment or live Goose/provider action is authorized by this
  review.
