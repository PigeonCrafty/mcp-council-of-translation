# Foreman Review: CAMPAIGN-007-r2

## Decision

`ACCEPTED`

CAMPAIGN-007-r2 corrects the V2.3 record-finalization defect without changing the
accepted bounded-concurrency scheduler or any Council semantics. Combined r1+r2 evidence
satisfies F-035 through F-039. Publication and live Goose Q-011 remain separate gates.

## Control and scope

- Role/mode: FOREMAN / STRICT_CAMPAIGN
- r2 contract SHA-256:
  `612CC6F9C42B93956A1CCB4EC8ACE1B634F42AFE674B9EB48105CD76772D888D`
- r2 baseline: `61252ae27823467d74c38efaa59aa1521b006752`
- Accepted final HEAD: `e835566a2c8d60ba153b68175d19685cb96185fe`
- Exactly one r2 commit: `e835566 Finalize V2.3 record timing provenance`
- Exact r2 scope: orchestration plus three authorized integration tests; 127 insertions,
  six deletions; no unauthorized path; `git diff --check` passed
- r1 report/ledger and all eleven r2 protected hashes matched independently
- Git index empty; declared Foreman/user/report assets preserved

## Corrected counterexamples

- Normal review: a deterministic delayed final renderer is included in persisted
  `wall_clock_ms`; the stored value equals the returned record.
- Required-briefing nonaccept: the pending record has nonzero final wall time, zero
  sampling calls and unchanged `RETURNED_PENDING` semantics.
- Continuation: a delayed reconsideration produces nonzero wall and sampling-wait
  values, retains the child's own one-call total, and copies the parent's independent
  concurrency limit/peak/batch/disposition.
- Parent record bytes remain unchanged and each path performs one persistence save.
- The unmodeled dynamic `independent_review_wall_clock_ms` assignment is absent.

## Fresh Foreman verification

- Delayed counterexamples: `3 passed in 0.29s`.
- Risk-weighted concurrency/continuation/briefing/persistence/tool/context/presentation
  matrix: `83 passed in 2.52s`.
- Compile: passed.
- Complete suite: `246 passed in 3.37s`.
- Fresh local-cache wheel and sdist build: passed; wheel size 78,383 bytes, sdist size
  72,335 bytes. Build hashes differ from the Worker artifacts because Python archives
  contain build-time metadata; version/content verification and the Worker's isolated
  installed-wheel smoke are the acceptance evidence, not cross-run byte identity.
- Fresh source diagnostics: package/module `0.9.0`, build
  `bounded-parallel-council-v7`, schema `2.3`, concurrency default/max `3/3`, exact five
  tools, review-only and budgets 6/13/18.
- Worker installed-wheel evidence independently exercised all five tools on Python 3.12
  and FastMCP 3.4.7, including parent/continuation wall telemetry and preserved
  `3/3/2/configured` provenance.

## Campaign acceptance mapping

- F-035: accepted — only independent reviewers overlap, default maximum three; later
  phases remain ordered.
- F-036: accepted — full batch budget reservation, exact-once calls, role correlation,
  stable plan order and sibling failure isolation are proven.
- F-037: accepted — schema 2.3 distinguishes accumulated wait and finalized wall time,
  stores bounded concurrency facts and reads V1/V2.0–V2.2 conservatively.
- F-038: accepted — missing/1/2/3/invalid configuration behavior and sequential override
  are deterministic and exposed through existing diagnostics.
- F-039: accepted — V0.9.0/build v7/schema 2.3, exact five tools, unchanged budgets,
  documentation, fresh artifacts and installed-wheel behavior pass.

## Remaining gate and risk

Q-011 is not accepted by deterministic tests. The Worker observed that the in-memory
FastMCP sampling callback serialized provider callbacks even while the Core correctly
held three correlated tasks. Therefore the published build must be tested in normal
Goose at effective limits one and three. Acceptance requires no protocol failure or
coverage loss and a materially lower server-reported wall time at three; otherwise the
safe limit-one override remains available and the latency claim must be revised.

- Foreman live calls: 0
- Worker live calls: 0
- Subagents: 0
- External mutation in review: 0
- Push/PR/release/deployment: not performed
