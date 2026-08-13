# Foreman Review: CAMPAIGN-007-r1

## Decision

`CHANGES_REQUESTED`

The bounded concurrent independent-review implementation is structurally sound, but the
V2.3 wall-clock contract is incomplete for continuation records and is finalized too
early for new-review records. A bounded r2 correction can satisfy the Campaign without
reworking accepted r1 package behavior.

## Control and scope

- Role: FOREMAN
- Mode: STRICT_CAMPAIGN
- Contract: `harness/contracts/CAMPAIGN-007-r1.md`
- Contract SHA-256:
  `A796CFF155AFC1BA0FDECBF5A33FFEA718D98F63F4C33FF335F931ABA8188F7A`
- Baseline: `f9651ed64daf86dd5fabac5e7437b9de8b3186bc`
- Worker final HEAD: `61252ae27823467d74c38efaa59aa1521b006752`
- Worker report/ledger: present and internally consistent
- Diff: 21 authorized committed files, 616 insertions and 75 deletions; no scope
  mismatch; `git diff --check` passed
- Protected assets: all ten contract hashes independently matched
- Git index: empty; admitted Foreman/user assets and required r1 reports preserved

## Independently accepted r1 evidence

- Complete source/test/doc diff inspected. Concurrency is confined to independent role
  sampling; no role, prompt, Policy Gate, presentation, budget or tool-count change was
  introduced.
- The correlated batch reserves the complete independent budget, caps concurrency at
  three, returns plan order, attempts once, isolates sibling exceptions and propagates
  outer cancellation.
- Configuration behavior is exact: missing -> `3/default`; valid 1/2/3 are honored;
  invalid values -> `1/invalid_fallback`.
- Fresh Foreman focused suite: `80 passed in 2.28s`.
- Fresh Foreman compile and full suite: `244 passed in 3.28s`.
- Fresh diagnostics: package/module `0.9.0`, build `bounded-parallel-council-v7`, schema
  `2.3`, default/max concurrency `3/3`, exact five tools and budgets 6/13/18.
- Worker artifact evidence is credible and mapped: fresh wheel/sdist, isolated Python
  3.12 and FastMCP 3.4.7 five-tool smoke, concurrent `3/2/6` and sequential `1/6/6`.
- Local timing evidence materially improves six-role delayed work while structural
  peak/barrier evidence, not timing alone, establishes concurrency.

These results preserve PKG-037, PKG-038, the compatibility/privacy portion of PKG-039,
PKG-040 diagnostics and the V0.9 packaging migration as accepted evidence for the r2
review unless the correction changes or invalidates them.

## Failed acceptance criterion

Campaign criterion 7 requires V2.3 records to report truthful end-to-end wall time.
Independent source inspection and a delayed continuation counterexample show:

```text
schema=2.3
sampling_calls=1
elapsed_ms=20
sampling_wait_ms=20
wall_clock_ms=0
independent_review_concurrency_disposition=legacy
```

`continue_structured_review()` never starts or finalizes a wall-clock timer. It creates a
new V2.3 child and performs reconsideration sampling, but snapshots a default-zero wall
value. It also resets independent-review concurrency provenance to the V2.3 model's
legacy default even though the child retains the parent's independent reviews and
coverage.

For normal and required-briefing early-return reviews, `wall_clock_ms` is captured before
process-digest/display construction and record finalization. The field therefore means
"time until adjudication" rather than the frozen end-to-end Core duration. Persistence
I/O need not be included because the record must contain its final value before the
single atomic save, but all in-memory record construction and rendering must be.

The dynamic assignment `telemetry.independent_review_wall_clock_ms` is not represented in
`RuntimeTelemetry.snapshot()` or `RuntimeMetadata`; it should be removed rather than
left as dead implied telemetry.

## Required correction

1. Time every record-producing Core path, including `continue_review`.
2. Finalize `wall_clock_ms` after in-memory digest/display/record construction and
   immediately before the one persistence save; update the record snapshot before save.
3. Preserve the parent's independent-review concurrency limit, peak, batch count and
   disposition in a continuation child, because the child retains those independent
   reviews/coverage. Continue to report only the child's own sampling/wall totals under
   existing continuation semantics.
4. Remove the unused dynamic independent-batch wall assignment unless a contracted,
   modeled field is added; r2 does not authorize a new field.
5. Add delayed counterexamples for normal, required-briefing early return and
   continuation records; assert nonzero/bounded wall values and continuation provenance.
6. Rerun focused telemetry/continuation/briefing/persistence tests, full 244+ suite,
   compile, diff/scope/hashes, and a fresh wheel plus isolated smoke because production
   orchestration changes.

No live Goose/provider call is required or authorized in r2. Q-011 remains a
post-acceptance and post-publication gate.

## Authority and remaining risk

- Foreman production edits: 0
- Live calls: 0
- External mutations: 0
- Subagents: 0
- Fresh build was not repeated after the Foreman cache-permission failure because the
  deterministic acceptance defect was already established; r2 must rebuild after the
  correction.
- Remaining external risk after r2 will still be real Goose/provider concurrency and
  rate-limit behavior.
