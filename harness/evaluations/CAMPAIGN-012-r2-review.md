# Campaign Review: CAMPAIGN-012-r2

## Decision

`CHANGES_REQUESTED`

The r2 implementation correctly fixes all three Foreman counterexamples named by its
parent review, but one remaining hostile-count path still violates the frozen r1
boundedness contract. A physically valid non-negative runtime integer can be thousands
of decimal digits long; the receipt accepts it, the Markdown renderer expands it, and
the public verification path can still raise the 3,200-code-point hard-cap exception.

## Control

- Role: `FOREMAN`
- Harness mode: `STRICT_CAMPAIGN`
- Contract: `harness/contracts/CAMPAIGN-012-r2.md`
- Contract SHA-256:
  `1B628133452A89F1BA4F47798F124B0E07C9E25E4B994C52834D65A1FAFCB615`
- Baseline: `06b0e378adc99826c48cd9fc7cc4337d8bc25367`
- Worker final HEAD: `5819a92e352c468021c3a8f30aa488508e4223f4`
- Worker report: `harness/reports/CAMPAIGN-012-r2-worker.md`
- Commits: `27777d1`, `5819a92`
- Scope: exactly three authorized paths; Git index empty

## Accepted r2 evidence to preserve

- Baseline ancestry, contract hash, exact two-commit order, three-path scope, protected
  hashes and byte-identical `uv.lock` all pass.
- Independent compile and focused receipt/history/tool/release matrix pass:
  `84 passed in 1.20s`.
- Independent complete regression passes: `360 passed in 3.92s`.
- Independent Golden selection passes: `4 passed`; the Worker establishes exact 24/24
  and all eight aggregate metrics at 1.0.
- Current/legacy/null parents round-trip; path, traversal, prose and overlong parent IDs
  become null with explicit redaction and no raw echo.
- Duplicate, oversized and invalid active-role lists now redact routing and samples; the
  original 100-role counterexample renders safely in 940 code points.
- Sample membership must exactly follow the validated active-role order.
- Terminal coherence truth table is correct:
  `(1,true,true)`, `(1,false,false)`, `(2,true,false)`, `(0,false,false)`.
- Primary Markdown exposes serving package/module/build/Schema, retains five headings
  and remains within the hard cap for the tested full/partial/redacted shapes.
- Package/module/build remain `0.12.0` / `0.12.0` /
  `verifiable-evidence-council-v10`; schemas remain record `2.5` and receipt `1.0`;
  exact five tools, budgets 6/13/18 and concurrency 3/3 remain frozen.
- Worker fresh artifact hashes and isolated CPython 3.12/FastMCP 3.4.7 smoke are
  preserved as r2 evidence.

## Remaining counterexample

`RuntimeMetadata.wall_clock_ms` and several call/timing fields are constrained only to a
non-negative Python integer. `_safe_count` likewise checks only type and sign. A parsed
or assigned value of `10**3500` therefore remains a 3,501-digit integer in the canonical
receipt. Independent Foreman execution produced:

```text
projected_digits = 3501
ValueError: verification report exceeds hard cap
```

This is not a hypothetical alias or model-output issue: the V2.5 domain model accepts
the value, JSON can represent it within the runtime parser's digit limit, and the
verification renderer interpolates it directly. It violates CAMPAIGN-012-r1's explicit
requirement that list/count bounds remain deterministic and CAMPAIGN-012-r2's objective
that hostile persisted values return a bounded receipt instead of a renderer exception.

Static inspection also shows `_sample_projection` builds an output row for every
`independent_reviews` member before discovering that the list cannot equal the bounded
active-role list. The resulting Markdown is now safe, but processing remains unbounded
relative to the finite role registry. This can be corrected in the same count-boundary
package by rejecting a length mismatch before iteration.

## Required r3 correction

1. Define one canonical non-negative JSON-safe integer bound of
   `9_007_199_254_740_991` (`2**53 - 1`) for every numeric receipt field projected
   through `_safe_count`.
2. Values from zero through that maximum round-trip exactly. Booleans, negative values
   and larger integers become null and add the exact field path to `redacted_fields`.
3. Reject independent-review list length mismatch before iterating or constructing
   projected rows; valid lists still preserve exact ordered samples.
4. Prove the actual history tool returns bounded primary and structured channels for a
   3,501-digit runtime integer and oversized sample list.
5. Preserve every r1/r2 field, privacy, history, coherence, display, purity, release and
   product invariant; do not change version, schemas, tools, lock or normal reports.

F-053 through F-057 and Q-014 remain unaccepted. CAMPAIGN-012-r3 is the minimal
count-boundary correction.

## Foreman environment note

An attempted broad listing of the historical top-level `dist/` directory encountered an
existing access denial on old V0.3 artifacts. It was not a required r2 source check and
does not contradict the Worker's fresh isolated artifact evidence. No historical
artifact, protected `.learnings/**` file or user asset was modified; this command-boundary
incident is recorded here under the self-improvement protocol.
