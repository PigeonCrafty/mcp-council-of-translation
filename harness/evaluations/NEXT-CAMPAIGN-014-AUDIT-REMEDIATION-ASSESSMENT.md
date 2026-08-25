# Next Campaign 014 Assessment — V0.13 Audit Remediation

## Foreman decision

```text
RECOMMEND CAMPAIGN-014
STATE: PLANNED; CONTRACT NOT ISSUED
TYPE: NARROW AUDIT REMEDIATION
RECOMMENDED TARGET: V0.13.1
```

The independent V0.13 audit is accepted as a blocker on ordinary feature expansion.
CAMPAIGN-014 should repair known completeness, deterministic-precision, robustness,
trace-consistency and retrieval-minimization defects before any broader product work.

Source audit:
`mcp-council-of-translation-v0.13-independent-audit.md`

Foreman response:
`harness/evaluations/CAMPAIGN-013-INDEPENDENT-AUDIT-FOREMAN-RESPONSE.md`

## Product boundary

- Keep exactly five public tools.
- Keep the server review-only; do not translate files or apply edits.
- Keep budgets `6/13/18` and concurrency `1..3` with default `3`.
- Keep current reviewer portfolios, Policy Gate and bounded user authority.
- Prefer Review Schema `2.6` and receipt Schema `1.1` unless a new persisted field is
  proven necessary; stable warning/fallback/availability fields should carry the fixes
  where possible.
- Recommended build identifier: `truthful-boundaries-council-v11.1`.
- No production implementation is authorized by this assessment.

## Planned feature packages

### PKG-080 / F-064 — Input completeness fail-closed

Convert known source/candidate truncation into an explicit incomplete-review state.

Acceptance essentials:

- source-only, candidate-only and dual truncation are visible in compact/full/
  verification channels;
- any truncation yields degraded execution, `decision_support=insufficient`,
  `NEEDS_HUMAN_REVIEW` and `需人工复核 / 是`;
- a clean prefix plus unsafe omitted suffix cannot receive a complete publishable
  disposition;
- no long-document chunking or synthesis is introduced.

### PKG-081 / F-065 — Deterministic scanner precision

Repair printf and URL-boundary false positives with a dedicated negative corpus.

Acceptance essentials:

- ordinary percentage prose and localized sentence punctuation around URLs do not
  produce deterministic blockers;
- valid printf placeholders, application variables, protected literals, slash commands
  and flags retain current protection;
- no model finding gains deterministic authority.

### PKG-082 / F-066 — Discussion envelope safe degradation

Introduce total, conservative validation for Targeted Discussion payloads.

Acceptance essentials:

- missing/null/string/scalar/malformed turns never escape as unhandled exceptions;
- the chosen policy is whole-envelope rejection;
- pre-discussion positions and findings remain authoritative;
- no invalid discussion can create a blocker, action or position change;
- bounded degraded/warning/phase provenance is persisted and surfaced.

### PKG-083 / F-067 — Post-discussion state coherence

Recompute role consensus after valid position updates and distinguish it from optional
user preference.

Acceptance essentials:

- final converged positions yield consensus in the cluster, digest, minority report,
  value metrics and decision support;
- stale pre-discussion disagreement cannot create a limitation or DecisionPoint;
- a DecisionPoint may remain only when multiple Policy-valid outcomes independently
  justify user choice;
- full structured evidence preserves before/after provenance.

### PKG-084 / F-068 — Legacy V1 summary minimization

Add a compact V1 summary projection.

Acceptance essentials:

- V1 summary exposes bounded record identity, mode, status, publishability and
  review-needed facts only;
- source/candidate/task text, reviewer/conflict prose and full chief rationale are absent;
- V1 full and verification retrieval remain compatible and pure;
- retrieval adds zero saves, sampling or elicitation.

### PKG-085 / F-069 — Truthful evaluation semantics and blind-set contract

Calibrate the evidence claims without changing production adjudication.

Acceptance essentials:

- overbroad metric names are versioned or renamed to state their actual predicates;
- the existing 30-case production-path corpus remains a regression asset, not a claim
  of blind defect-identity performance;
- a machine-readable blind-set schema defines issue family, bounded anchors, severity
  range, allowed alternatives and forbidden findings;
- independent curation and external scoring remain a later gate, not Worker-authored
  proof of its own accuracy.

### PKG-086 / F-070 — FastMCP compatibility contract

Investigate Goose/runtime requirements and make the declared range match evidence.

Acceptance essentials:

- preserve evidence that the locked floor `2.13.0.2` passes the six-job OS/Python matrix
  and that isolated FastMCP `3.4.7` wheel smoke passed;
- choose and document either a justified upper bound, a minimum/current/latest-
  compatible CI matrix, or both;
- do not remove FastMCP 2.x support without a caller/runtime compatibility reason;
- dependency and lock changes, if any, remain canonical and narrowly scoped.

## Ordered execution

1. Reproduce and freeze counterexamples for AUD-001 through AUD-005.
2. Implement PKG-080 first; no later package may weaken its fail-closed outcome.
3. Implement PKG-081 and PKG-082 as deterministic/robustness boundary repairs.
4. Implement PKG-083 and prove one source of post-discussion truth.
5. Implement PKG-084 and run privacy/purity compatibility tests.
6. Implement PKG-085; separate regression metrics from blind evaluation claims.
7. Perform PKG-086 compatibility investigation and apply only the justified result.
8. Run complete regression, exact Golden checks, fresh artifacts and isolated wheel
   smoke before Foreman review.
9. After independent Foreman acceptance, publish V0.13.1 through protected main and
   confirm CI; publication is allowed only to enable validation of the accepted repair.
10. Run the post-publication Q-016 external/normal-Goose remediation re-audit. Do not
    lift the feature-expansion block until it passes.

## Q-016 — External audit-remediation gate

Q-016 is planned, not issued. It should include:

- external reproduction of each original AUD-001 through AUD-005 counterexample;
- positive and negative deterministic scanner cases;
- malformed-discussion and resolved-consensus trace checks;
- V1 summary privacy/data-minimization inspection;
- a normal-Goose receipt proving truncation is visible and fail-closed;
- confirmation that metric wording no longer overclaims blind quality evidence;
- a recorded disposition for AUD-007 based on the implemented compatibility policy.

The gate passes only when all of the following are true:

- AUD-001 through AUD-005 are independently reproduced as closed;
- F-069's truthful metric semantics and blind-set schema/design contract are accepted;
- F-070 records an evidence-backed supported-range decision, even if that decision
  intentionally makes no dependency code change;
- no regression weakens deterministic authority, reviewer coverage truth, user
  authority, privacy or the review-only boundary.

Q-016 is post-publication because its normal-Goose case must exercise published bytes.
Protected-main publication does not itself accept Q-016 or authorize a new feature
Campaign.

## Explicit non-goals

- long-document chunking, overlap or cross-chunk synthesis;
- new reviewer roles, content types or routing portfolios;
- new providers, MCP tools or public arguments;
- translation generation, file editing, UI or deployment features;
- A2A orchestration, context-MCP coupling or multi-round peer debate;
- numeric confidence, voting or model-self-reported authority.

## Progress accounting

- Accepted product features before this plan: `63`.
- Newly planned remediation features: `7` (`F-064` through `F-070`).
- Portfolio after planning: `63 accepted / 70 total`; `7 not started`.
- Accepted quality gates before this plan: `15`.
- Newly planned gate: `Q-016`.
- Gate portfolio after planning: `15 accepted / 16 total`; `1 not started`.

No implementation, release, publication or live provider validation is completed by this
assessment.
