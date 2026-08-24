# Campaign Review: CAMPAIGN-012-r3

## Decision

`ACCEPTED`

CAMPAIGN-012-r3 closes the remaining hostile-count/cardinality boundary while preserving
all r1/r2 receipt, history, privacy, coherence, release and product invariants. Combined
CAMPAIGN-012-r1/r2/r3 evidence accepts F-053 through F-057 at final implementation HEAD
`e940044c5367ff2ef86e4c58bd75e1f85e4da4cf`.

## Control

- Role: `FOREMAN`
- Harness mode: `STRICT_CAMPAIGN`
- Contract: `harness/contracts/CAMPAIGN-012-r3.md`
- Contract SHA-256:
  `E6EF7A7CC8468124E85CAA87C649141D2947D25506F6A00C6901F94487928161`
- Baseline: `5819a92e352c468021c3a8f30aa488508e4223f4`
- Final HEAD: `e940044c5367ff2ef86e4c58bd75e1f85e4da4cf`
- Worker report: `harness/reports/CAMPAIGN-012-r3-worker.md`
- Commit: `e940044 fix: bound verification receipt counts`
- Scope: exactly three authorized paths; Git index empty

## Scope and integrity

- Baseline is an ancestor of final HEAD; the range contains exactly one commit.
- The complete diff changes only `verification.py` and the two authorized V0.12 receipt
  test files. No tool, model, persistence, orchestration, package, documentation,
  dependency or lock path changed.
- All 14 contract-protected hashes match exactly. Existing Foreman/user dirty and
  untracked assets remain preserved.
- `uv.lock` is byte-identical at baseline and final HEAD with Git blob
  `550b6c4393e998192973c28869c88c73c0a050d1`.
- Baseline-to-final `git diff --check` passes and the Git index is empty.

## Independent Foreman verification

- Compile passes.
- Complete V0.12 receipt/history/tool/release matrix:
  `165 passed in 1.55s`.
- Complete regression: `441 passed in 4.12s`.
- Golden selection: `4 passed`; Worker production evidence records exact 24/24 and all
  eight aggregate metrics at 1.0.
- Direct numeric truth table for `runtime.wall_clock_ms`:
  - `0` and `1` round-trip exactly;
  - `9_007_199_254_740_991` round-trips exactly;
  - `9_007_199_254_740_992` becomes null/redacted;
  - `10**3500` becomes null/redacted and renders in 1,130 code points without exposing
    the 3,501-digit decimal.
- The r2 privacy counterexample remains fixed: a path-shaped parent becomes null with
  `record.parent_review_id` redaction.
- The r2 role counterexample remains fixed: 100 duplicate roles produce null routing and
  samples and a 940-code-point report.
- The r2 terminal counterexample remains fixed: expected-once then conflicting-final
  yields occurrences 1, last false and matches false.
- Tests instrument an oversized sample-list subclass whose iterator raises; the receipt
  rejects cardinality before invoking that iterator.
- The integration matrix calls the registered FastMCP history tool with a 3,501-digit
  runtime integer plus 100 samples and receives the normal bounded dual-channel wrapper.

## Frozen public invariants

- Package/module: `0.12.0`.
- Diagnostic build: `verifiable-evidence-council-v10`.
- Persisted Review Schema: `2.5`; verification receipt Schema: `1.0`.
- Exact five public tools in the frozen order.
- Sample budgets: 6/13/18; concurrency default/max: 3/3.
- Normal review/continuation text, `full`/`summary` history, review-only authority,
  routing, sampling, adjudication and persistence remain unchanged.
- Verification retrieval remains one-load, zero-save, zero-sampling and zero-elicitation.

## Artifact evidence

The Worker produced fresh final-HEAD artifacts and inspected both archives:

- wheel: 102,217 bytes, SHA-256
  `0056CB7CB0E66B5642D19FACE263487DD50C257BD97FB354875ED1E33B3D9644`;
- sdist: 95,927 bytes, SHA-256
  `B1A79CA35C1B48F82689AA3F3174A5CA713421E2B6A28D6FB499578C2D096837`.

Its isolated CPython 3.12.9/FastMCP 3.4.7 smoke imported from site-packages, called all
five tools and passed safe/full/summary/verification plus hostile-count wrapper probes.
Foreman did not traverse the contract-forbidden historical `dist/**` directory.

## Acceptance and remaining gates

- F-053 through F-057: accepted by combined CAMPAIGN-012-r1/r2/r3 evidence.
- Local V0.12 implementation: accepted at
  `e940044c5367ff2ef86e4c58bd75e1f85e4da4cf`.
- Q-014 is not accepted. It remains a separate normal-Goose gate after protected-main
  publication of the accepted implementation and Foreman archive assets.
- No push, PR, publication, release, deployment, credential or live provider action was
  performed during this review.
