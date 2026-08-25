# CAMPAIGN-013-r1 Foreman Review

- Decision: `CHANGES_REQUESTED`
- Reviewed Worker report: `harness/reports/CAMPAIGN-013-r1-worker.md`
- Reviewed ledger: `harness/reports/CAMPAIGN-013-r1-ledger.md`
- Contract: `harness/contracts/CAMPAIGN-013-r1.md`
- Contract SHA-256:
  `D11C672105A740BFD2413C9794878BF6BD1FB7011C3407406ED45B50B20A29B5`
- Baseline: `44b1969677cd6b1fda63047ca514aede6609bdad`
- Reviewed HEAD: `6a07f4ebc61146e60af8bb6e7456f2b144ce15a4`
- Review date: 2026-08-24 Asia/Shanghai

## Outcome

The Worker stop is procedurally correct, but the Campaign is not accepted. PKG-075 is a
valid scoped foundation and should be preserved. PKG-076 cannot complete under r1 because
two legacy regression files omitted from the allowlist still assert the superseded
permissive fallback status. A bounded r2 contract must authorize those assertions to be
migrated; production must not be weakened to satisfy them.

## Independent evidence

- Git HEAD is the reported `6a07f4e`; index is empty; the single commit contains only
  `decision_support.py`, `models.py` and `test_decision_support.py`.
- The contract SHA-256 and all five reported protected hashes match.
- Baseline-to-HEAD scope is exactly the three PKG-075 paths.
- The uncommitted PKG-076 intermediate is confined to the reported authorized production
  and test paths, plus its authorized new V2.6 integration test.
- Independent PKG-075 classifier/model replay passed `39` tests.
- Independent full replay of the PKG-076 intermediate produced the same result:
  `467 passed, 10 failed`.
- Seven failures are exact status assertions in:
  - `tests/integration/test_r3_outcome_suppression.py` (3 failures); and
  - `tests/integration/test_r3_workflow.py` (4 failures).
- Those cases retain `degraded`, warnings, fallback reason, Council selection and
  persistence provenance but now correctly end in `NEEDS_HUMAN_REVIEW` because the
  evidence is `insufficient`.
- The other three failures are unfinished downstream Schema 2.6, receipt 1.1 and release
  expectations in paths already authorized for PKG-077/PKG-079.

## Semantic ruling

The frozen safety rule remains authoritative:

1. `degraded=true` is `insufficient`.
2. Any recorded runtime fallback other than explicit, non-degraded
   `user_delegated_to_council` is `insufficient`.
3. `unsupported`, `decline`, `cancel`, interaction `off`, ambiguous anchor and missing
   anchor therefore cannot retain a permissive terminal disposition.
4. The outcome trace and Council-selected option may remain recorded, but they are not a
   release authorization; chief disposition must be `需人工复核 / 是` and status must be
   `NEEDS_HUMAN_REVIEW`.
5. Explicit non-degraded user delegation remains the only
   `COMPLETED_WITH_FALLBACK` exemption and is `supported_with_limits`.

This is an intentional V0.13 safety migration. The two old files protect historical V0.5
behavior, not a still-valid V0.13 invariant. Changing production to keep their old status
would violate the Campaign truth table and create false reassurance.

## Required correction

CAMPAIGN-013-r2 shall:

- preserve commit `6a07f4e` as PKG-075;
- admit and finish the reported PKG-076 intermediate;
- add only the two legacy regression files above to the authorized test scope;
- migrate their terminal assertions while strengthening checks for support level, chief
  disposition and retained degradation/fallback provenance;
- complete PKG-077 through PKG-079 and every original final acceptance check; and
- create four additional scoped commits, preserving five total Campaign package commits.

No level, code, precedence, public tool, model call, budget, concurrency rule or product
authority changes are authorized.

## Acceptance state

- F-059 through F-063 remain unaccepted pending complete r2 evidence.
- Q-015 remains planned and cannot be issued before local acceptance and protected-main
  publication.
- No push, PR, release, deployment or live Goose/provider action is authorized by this
  review.
