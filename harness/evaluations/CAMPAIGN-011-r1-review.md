# Campaign Review: CAMPAIGN-011-r1

## Decision

`CHANGES_REQUESTED`

CAMPAIGN-011-r1 is not accepted because PKG-062 is incomplete and the complete suite has
three failing release assertions. The Worker nevertheless obeyed the strict stop condition:
the only failure outside the r1 allowlist is a historical-named test that constructs a new
runtime record and still asserts Schema 2.4. Returning that new record as 2.4 would violate
the frozen V0.11 contract. This is a contract-scope omission, not a product-design blocker.

## Control

- Role: `FOREMAN`
- Harness mode: `STRICT_CAMPAIGN`
- Contract: `harness/contracts/CAMPAIGN-011-r1.md`
- Contract SHA-256:
  `9EB1317585B0BC999AA9615D37DAC86992EC31BCBD87B0FC45330DB9A39D83E0`
- Baseline: `610eae8e7c2df31fd9052b0ae76a2d718805f28d`
- Reviewed HEAD: `1ae3a7419c1eaeb293a944a49d0873cdf95952e1`
- Worker report: `harness/reports/CAMPAIGN-011-r1-worker.md`
- Ledger: `harness/reports/CAMPAIGN-011-r1-ledger.md`
- Index: empty

## Independent findings

- The five committed packages are five ordered, scoped commits over exactly 15 r1-authorized
  implementation/test/fixture paths. The baseline-to-HEAD diff is 805 insertions and 75
  deletions, and `git diff --check` passes.
- The implemented routing table matches the frozen 15-profile matrix. The legal-risk
  portfolios are exactly 4/6/7 roles and the accepted non-legal portfolios retain their
  existing order.
- New routing provenance is bounded by literal profile/reason vocabularies, defaults old
  plans conservatively, and is persisted without caller prose. No new role or tool was
  introduced.
- Primary rendering uses fixed natural-language route descriptions, sanitizes internal
  routing tokens and keeps whole high-value lines while retaining all five sections and the
  final disposition.
- Worker evidence for PKG-057 through PKG-061 is internally consistent: focused suites
  passed; the production Golden runner passed exactly 24/24 with 148 scripted sampling calls,
  four elicitations, aggregate budget 296 and all eight aggregate metrics at 1.0.
- Nine PKG-062 release files are present as an unstaged, index-clean intermediate. Their
  focused release tests pass 16/16. They have not been accepted or committed.

## Reproduced failure and root cause

The Foreman independently ran the legacy presentation and persistence release tests and
reproduced exactly `19 passed, 3 failed`:

1. `tests/integration/test_v08_presentation_invariants.py` expects `2.4` from a newly
   executed review; the truthful V0.11 result is `2.5`. This path was accidentally omitted
   from r1's exhaustive allowed-test list.
2. Two parametrized `tests/unit/test_persistence_v2.py` cases still expect package
   `0.10.2` and build `evidence-value-council-v8.2`; the truthful release values are
   `0.11.0` and `risk-coherent-council-v9`.

No reproduced failure concerns role selection, sampling, elicitation, budgets, evidence
aggregation, display grouping or record compatibility. The proper correction is to migrate
the stale assertions, not to regress production metadata.

## Preserved evidence and required correction

- PKG-057 through PKG-061 and commits `29e28d7`, `43c6613`, `cc2d4bd`, `fd5589b` and
  `1ae3a74` are preserved for r2 final acceptance; the Worker must not rewrite or squash them.
- F-047 through F-051 remain pending Campaign acceptance rather than individually accepted.
- PKG-062/F-052 remains incomplete.
- CAMPAIGN-011-r2 must authorize the one omitted integration-test path, the already allowed
  release/persistence paths and `uv.lock`; complete one release commit; then run the complete
  regression, pinned root-only lock refresh, fresh artifacts and isolated wheel smoke.
- Q-013 remains a separate post-publication live gate.

