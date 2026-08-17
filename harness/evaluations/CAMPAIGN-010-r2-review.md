# Campaign Review: CAMPAIGN-010-r2

## Decision

`ACCEPTED`

The zero-proposal structural projection now works against the immutable normal-Goose
records that invalidated r1. It groups one human repair without mutating structured issue
identity, preserves distinct repairs and consequences, and passes all required negative
controls and frozen product invariants.

## Control

- Role: `FOREMAN`
- Harness mode: `STRICT_CAMPAIGN`
- Contract: `harness/contracts/CAMPAIGN-010-r2.md`
- Contract SHA-256:
  `2A1F01AA9E59527B8D822A893CD968EDD335F5C738EA70939455DABFA2F3D711`
- Baseline: `144ecebb6bfbd507ccdfb09a9b87efac3d59e9e1`
- Accepted HEAD: `f58306d0df42fc27d46dd5049348ccfce8a0f6f8`
- Commit: `f58306d Fix zero-proposal work item grouping`
- Worker report: `harness/reports/CAMPAIGN-010-r2-worker.md`
- Scope: exactly three authorized paths; index empty

## Diff and implementation review

- Baseline is an ancestor of accepted HEAD; complete diff is 210 insertions and 22
  deletions across `digest.py` and the two authorized integration tests.
- `git diff --check` passes and no version, docs, dependency, lock, prompt, role,
  clustering, metric, persistence, adjudication or public-tool path changed.
- The r2 fallback applies only to actionless/current-only model clusters. Source and
  candidate anchors must each be exact or directly nested, category families must
  differ, concrete non-current actions must not conflict, and every group member must be
  pairwise compatible. This avoids transitive broad-span merging.
- Concrete replacement identity from r1 retains priority. Structured clusters, metrics,
  digest and persisted full records are not mutated.
- Negative tests cover conflicting replacements, different protected literals,
  one-sided source/candidate relation, placeholder plus reversal in one sentence and
  incompatible actions on the same spans.

## Immutable live-record replay

The Foreman loaded the three accepted Schema 2.4 JSON files into `ReviewRecordV2` and
rendered them with the accepted HEAD:

- A: 369 code points, zero repair lines, one grouped six-role confirmation, unchanged
  from the accepted clean report.
- B: 716 code points, exactly two repair lines and zero execution-order lines. One line
  restores `{count}`; one line repairs the `cannot`/`可以` reversal while retaining the
  second bounded safety consequence.
- C: 1,056 code points, exactly one repair line and zero execution-order lines. The scope
  restoration is stated once and both accuracy and user-impact consequences remain.
- Each record's complete JSON-mode model dump is identical before and after rendering.

This directly closes both r1 counterexamples without treating old rendered text as a new
live Q-012 result.

## Independent verification

- Compile: passed.
- Complete suite: `294 passed in 3.95s`.
- `uv lock --check`: passed with 78 packages; SHA-256 remains
  `31F0173F9325A4CA1C5BF95BB281B75E00374C8A241A19DFC38AB39C95F5347D`.
- Diagnostics: package/module `0.10.2`, build `evidence-value-council-v8.2`, schema `2.4`,
  exact five tools, review-only, budgets 6/13/18 and concurrency default/max 3.
- All 13 protected hashes match; user and Foreman dirt remains unstaged.
- Fresh wheel and sdist build from accepted HEAD succeeded. Worker evidence additionally
  provides isolated Python 3.12.9/FastMCP 3.4.7 five-tool smoke and exact Golden 18/18
  with unchanged 113 scripted samples, four elicitations and eight metrics at 1.0.
- Required checks skipped: none. Live calls and external publication actions: none.

## Acceptance and remaining gate

Combined CAMPAIGN-010-r1/r2 evidence accepts F-046 and the V0.10.2 implementation. Q-012
is not accepted by this local replay: the accepted tree must first be published, then a
new normal-Goose A/B/C run must confirm provider-shaped output on that published build.
