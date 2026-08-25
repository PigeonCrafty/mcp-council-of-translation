# Live Gate Review: CAMPAIGN-013 Q-015

## Decision

`ACCEPTED`

Three fresh user-operated normal-Goose records satisfy the calibrated decision-support
contract on published V0.13. The clean case is well supported, the material-edit case is
supported with bounded limits, and the unresolved-context case is correctly classified
as insufficient and transferred to human review. This accepts Q-015 and completes
CAMPAIGN-013 with all 63 features and all 15 quality gates accepted.

## Control

- Role: `FOREMAN`
- Harness mode: `STRICT_CAMPAIGN`
- Contract: `harness/contracts/CAMPAIGN-013-q015-live.md`
- Contract SHA-256:
  `74C4179BA020629D9F34966B0756FFB3547D29710A01A0A820B779A38788EC99`
- Published V0.13 product `main`: `95d90cf383d045778ce61afaa50dbcec199579ce`
- Q-015 issuance archive `main`: `3cbfc539d010474710a270e91f6696f9e59535c7`
- Package/module: `0.13.0`
- Diagnostic build: `calibrated-evidence-council-v11`
- Persisted/receipt Schemas: `2.6` / `1.1`
- Evidence source: three fresh user-operated normal-Goose conversations
- Review date: 2026-08-25 Asia/Shanghai

## Admitted records and label reconciliation

| Canonical case | Review ID | Route | Coverage | Calls/budget | Decision support | Outcome |
| --- | --- | --- | --- | --- | --- | --- |
| A | `20260825T054541425417Z_82948e153def` | legal-risk lightweight | full, 4/4 | 4/6 | `well_supported` | 可发布 / 否 |
| B | `20260825T054611911676Z_93268941479c` | legal-risk standard | full, 6/6 | 7/13 | `supported_with_limits` | 修改后可发布 / 否 |
| C | `20260825T054626792852Z_2e49a2805b07` | legal-risk standard | full, 6/6 | 7/13 | `insufficient` | 需人工复核 / 是 |

The conversational return packet placed the unresolved-context record under the `B`
heading and the material-edit record under the `C` heading. Their source/candidate
descriptions, route, findings, support level and terminal outcome uniquely identify the
intended cases, so the Foreman normalized the labels without rerunning either record.
The three review IDs are distinct and no retry was reported. This is an audit-level
handoff ordering defect, not a server or acceptance defect.

## Admission and shared contract

- The single admission response reports package/module 0.13.0, build v11, persisted
  Schema 2.6, receipt Schema 1.1, detail levels full/summary/verification, budgets
  6/13/18, concurrency 3/3 and exactly five public tools.
- Every receipt reports matching record and serving identity, receipt Schema 1.1 and
  the exact canonical top-level field order including `decision_support` between
  `outcome` and `coherence`.
- Every `decision_support` object has exactly the frozen fields. All target
  `chief_disposition`, use `deterministic_structured_trace_v1`, and report
  `outcome_coherent=true`.
- All normal reports retain exactly five ordered sections, one natural `结论依据` line
  before one terminal disposition, no raw support codes and no full replacement
  translation.
- All receipts are complete with empty missing/redacted lists and no source, candidate,
  reviewer/evidence prose, credentials, filesystem path, environment value, suggested
  translation text or internal issue ID.
- The full-view structured `decision_support` was not exposed by the client in all three
  conversations. The contract expressly permits the literal `not exposed by client`;
  the canonical verification JSON remains the evidence authority.

## Case A — clean and well supported

- The lightweight legal-risk route activates the required ordered fidelity,
  terminology, risk-ambiguity and fluency roles; all four are `structured_success`.
- Coverage/success/unavailable is full/4/0. Runtime is exactly four sampling calls,
  budget six and zero elicitation.
- Preflight is nonblocking; issue, warning, fallback and degradation counts are zero.
- The outcome is `COMPLETED`, `可发布 / 否`, with no suggested translation.
- Support is `well_supported` with basis codes `full_reviewer_coverage` and
  `clean_confirmation`, no limitation codes and a coherent chief disposition.
- The primary report says `结论依据：充分` while explicitly stating that full coverage
  does not mean the translation is necessarily correct.

## Case B — material edits with bounded limits

- The standard legal-risk route activates the required six ordered roles; all six are
  `structured_success`, coverage is full and unavailable is zero.
- Runtime is seven sampling calls within budget 13 with zero elicitation. Preflight is
  correctly nonblocking and seven material issue clusters remain visible.
- The report preserves the precise/approximate-location reversal, selected-partner
  scope loss, authorization weakening and withdrawal-right reversal without inventing
  statutes or providing legal advice.
- The outcome is `COMPLETED`, `修改后可发布 / 否`, with no suggested translation.
- Support is `supported_with_limits`; its bounded evidence includes full coverage,
  structured and corroborated material evidence, while `material_disagreement` remains
  an explicit limitation.
- The primary report says `结论依据：有限制` and the terminal outcome remains coherent.

## Case C — unresolved context and insufficient evidence

- The standard legal-risk route completes all six required samples with full coverage,
  budget 13 and zero elicitation because interaction is off.
- Two material questions about the concrete country, region, jurisdiction or approved
  terminology remain visibly unanswered. No user answer is fabricated.
- The record truthfully reports partial context, one warning, degraded execution and
  fallback `material_context_unresolved`.
- The outcome is `NEEDS_HUMAN_REVIEW`, `需人工复核 / 是`, with no suggested translation.
- Support is `insufficient`; limitations include `partial_context`,
  `material_disagreement`, `unresolved_material_context`, `degraded_execution` and
  `runtime_fallback`. The chief disposition remains coherent.
- The primary report says `结论依据：不足` and limits the available evidence to transfer
  for human review.

## Completion

- Q-015: accepted.
- CAMPAIGN-013: complete.
- Published V0.13 milestone: 63/63 features and 15/15 quality gates accepted.
- No corrective V0.13 revision or Goose rerun is required.
- The next action is a new product-Campaign assessment; no new implementation scope is
  implicitly authorized by this acceptance.
