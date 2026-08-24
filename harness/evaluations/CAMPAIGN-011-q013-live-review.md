# Foreman Live Review: CAMPAIGN-011 Q-013

## Decision

`CHANGES_REQUESTED`

The V0.11 live routing behavior is accepted as evidence, but Q-013 is not yet accepted.
Case A exposes a material dual-channel disposition mismatch: the persisted structured
chief says `修改后可发布` and `review_needed=否`, while the deterministically rendered
primary report says `需人工复核` and `需人工复核：是`. A structured consumer and a human
reader can therefore receive different release instructions from the same record.

## Control

- Role: `FOREMAN`
- Harness mode: `STRICT_CAMPAIGN`
- Gate: `Q-013` — Risk-sensitive panoramic routing live evidence
- Contract: `harness/contracts/CAMPAIGN-011-q013-live.md`
- Contract SHA-256:
  `1119EB0392C52D0A8F4444556B8A4C402837355AF89B01B49C398D2D7CCEC613`
- Published protected `main`: `938c3a4bb9f14c7688286b25eabd8aff9f18a09d`
- Published implementation: `7f7d050ad7cd5ef931b38eafd11f988619afced1`
- Package/build/schema: `0.11.0` / `risk-coherent-council-v9` / `2.5`
- Review date: 2026-08-24 Asia/Shanghai

## Evidence policy and handoff deviations

The user ran preparation and exactly one A/B/C review in normal Goose and reported no
retry. Goose's narrative did not expose the required structured fields for A/B and
reported non-canonical inferred fields for C, including names that do not exist in
Schema 2.5. Those statements are not used as telemetry evidence.

The Foreman located the exact three persisted full-history JSON records in the retained
`.tmp/q012` directory and independently loaded them through the V0.11 production
`ReviewStore`. Persisted records are authoritative. The directory name is a retained
environment-path deviation, not a record ambiguity: all three IDs, tasks, timestamps,
version/build/schema values and hashes are unique and match the issued cases. Raw records
remain ignored and are not copied into Harness, product code or tests.

The first independent product-load attempt reproduced the known global uv-cache access
failure. The identical read-only load/rerender check then passed with the repository
virtual environment. Per the protected-asset boundary, no `.learnings/**` file was
modified; this deviation is recorded here.

Goose-reported wall-clock prose is not treated as authoritative because it conflicts
with persisted telemetry: B was reported as 3,663 ms versus record `5,365 ms`; C was
reported as 10,970 ms versus record `19,742 ms`. The record values below are used.

## Shared admission and presentation evidence

- Preparation passed: package/module `0.11.0`, build `risk-coherent-council-v9`, schema
  `2.5`, budgets `6/13/18`, concurrency limit/max `3` and exactly five public tools.
- All three tasks use the issued content type, mode, `review_only`, interaction-off,
  briefing-off and full-history settings.
- Every reviewer sample is `structured_success`; every route has full coverage, zero
  unavailable samples, zero parse failures, zero elicitation and no degradation,
  warnings or fallback.
- Each report has exactly the five required headings in order, places the chief section
  last, remains below 3,200 code points and exposes no internal route, role or entity ID.
- Every structured `suggested_translation` is null.
- Production-model load and deterministic rerender are exact for all three records and
  leave both the model dump and raw bytes unchanged.

## Case A — routing accepted, disposition coherence failed

- Review ID: `20260824T034709461394Z_33b581b3d0b6`.
- Raw SHA-256:
  `30DF454664858CB34187FE7B8EF81B38E83D16474D3F887151DDF12BBC6B1B52`.
- Route: `route_legal_risk_standard_v1` with exact reasons
  `content_legal_risk`, `mode_standard`, `deterministic_preflight_coverage`,
  `risk_panorama`.
- Ordered roles: fidelity, terminology, product context, UX copy, risk ambiguity and
  fluency; successful/unavailable `6/0`, coverage `full`.
- Runtime: `7/13` sampling calls, zero elicitation, concurrency peak `3`, two batches,
  persisted wall clock `15,647 ms`.
- The primary report correctly preserves authorization weakening, location-precision
  reversal, selected-partner scope loss and withdrawal-right reversal without inventing
  a statute or giving legal advice.
- Failure: structured chief `修改后可发布 / 否` conflicts with the primary final line
  `需人工复核 / 是`.

Independent source inspection identifies the deterministic cause. `build_process_digest`
places the chief final disposition after all action lines. `_primary_checklist` stops once
six projected entries have been collected, so a long actionable case discards the final
disposition. `render_display_report` then sees no final line and inserts its safe fallback
`最终处置：需人工复核；需人工复核：是`. The fallback is conservative, but the two public
channels are not coherent.

## Case B — preserved accepted evidence

- Review ID: `20260824T034736890253Z_ee206d53abf7`.
- Raw SHA-256:
  `A8C5F6F1780B199FF88F1216E49C7645E2C62F31509130963094011567799D2F`.
- Route: `route_legal_risk_lightweight_v1` with exact focused-risk reasons.
- Ordered roles: fidelity, terminology, risk ambiguity and fluency; successful/unavailable
  `4/0`, coverage `full`.
- Runtime: exactly `4/6` samples, zero elicitation, persisted wall clock `5,365 ms`.
- Result: `COMPLETED`, `可发布 / 否`, no fabricated blocker, statute or legal advice;
  368-code-point five-section report and null suggested translation.

This case is accepted for reuse by the correction revision.

## Case C — preserved accepted evidence

- Review ID: `20260824T034809876049Z_c78aaf84819e`.
- Raw SHA-256:
  `E0F2D1711272FC32A5A652E390C36A5CB193CFA039F8696A00187E75EABCE35F`.
- Route: `route_legal_risk_strict_v1` with exact strict-risk reasons.
- Ordered roles: technical safety, fidelity, terminology, product context, UX copy,
  risk ambiguity and fluency; successful/unavailable `7/0`, coverage `full`.
- Runtime: `8/18` samples, zero elicitation, persisted wall clock `19,742 ms`.
- Deterministic preflight independently records three blocking failures for placeholder
  parity, explicit DNT preservation and `required_literal:{terms_url}`.
- The structured model preserves the placeholder loss and the distinct expansion from
  `for this request only` to `所有账户数据`; result is `NEEDS_HUMAN_REVIEW`, chief
  `需人工复核 / 是`, and suggested translation is null.

This case is accepted for reuse by the correction revision. Goose's non-canonical
`overall_quality_score`, `verdict`, alternate role IDs and similar inferred fields are
explicitly rejected and are not product evidence.

## Required correction

Issue `CAMPAIGN-011-r3` as a bounded patch:

1. preserve the canonical structured chief final disposition independently of the
   bounded action-item projection;
2. render that exact final disposition once and last even when more than six actionable
   entries exist;
3. retain existing safety behavior for pending, degraded and true human-review cases;
4. leave routing, roles, evidence, clustering, sampling, adjudication and Schema 2.5
   unchanged;
5. release the correction as V0.11.1, then rerun the normal-Goose Q-013 cases on the
   published build before accepting the gate.

Q-013 remains planned. Case B and C evidence, plus Case A routing/coverage evidence, are
preserved; only cross-channel disposition coherence and post-fix live confirmation remain.
