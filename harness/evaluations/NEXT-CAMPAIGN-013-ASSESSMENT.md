# Next Product Campaign Assessment: Calibrated Decision Support

- Assessment decision: `RECOMMEND CAMPAIGN-013 DESIGN`
- Proposed product release: `0.13.0`
- Proposed diagnostic build: `calibrated-evidence-council-v11`
- Proposed persisted Review Schema: `2.6`
- Proposed verification receipt schema: `1.1`
- Proposed feature packages: 5
- Proposed post-publication quality gate: `Q-015`
- Implementation authorization: issued separately by the versioned Campaign contract

## Executive assessment

V0.12.1 closes the client-verifiability gap: normal Goose can now expose the exact
canonical verification receipt without reconstructing fields. The product has 58/58
accepted features and 14/14 accepted quality gates, the complete baseline has 444 passing
tests, and GitHub has no open product issues as of this assessment.

The highest-value next gap is now interpretation, not collection. The record exposes
context confidence, reviewer coverage, deterministic blockers, issue evidence,
degradation, fallback and chief disposition, but a normal user still has to infer whether
the final disposition is strongly supported, supported with material limits, or based on
insufficient evidence. `context_confidence` describes the briefing, not the strength of
the final decision. Reviewer-provided numeric confidence is model self-report and must
not be averaged into a product score.

CAMPAIGN-013 should add a deterministic, categorical decision-support assessment derived
from the validated structured trace. It must explain why the disposition is supportable
without introducing probability, voting, model authority or false precision.

## Product outcome

Every new review records one bounded assessment with three user-meaningful levels:

- `well_supported`: the recorded evidence strongly supports the actual disposition;
- `supported_with_limits`: the disposition is usable, but rests on material model
  findings, disagreement, limited context or Council adjudication that the user should
  keep visible; and
- `insufficient`: missing context, incomplete coverage, pending interaction or degraded
  execution prevents a safe conclusion.

Historical records that did not record the assessment return `not_recorded`; readers do
not retroactively guess. The level describes support for the *disposition*, not whether
the candidate translation is good. A deterministic placeholder blocker can therefore
make `需人工复核` well supported.

## Frozen semantic boundary

The assessment is a deterministic projection from bounded structured facts only:
reviewer coverage and sample availability, unresolved material context, deterministic
preflight, validated issue clusters, Policy Gate result, user authority provenance,
reconsideration completion, degradation/fallback state and the final chief disposition.
It never reads free source/candidate/prose to classify support and never consumes reviewer
confidence values.

Precedence is conservative:

1. pending interaction, unresolved material context, partial/zero coverage, failed
   required reconsideration or degraded execution yields `insufficient`;
2. otherwise a deterministic blocker that coherently produces human review is
   `well_supported`;
3. otherwise material model-only issues, unresolved disagreement, limited but usable
   context, or non-degraded Council fallback yields `supported_with_limits`;
4. otherwise full clean coverage yields `well_supported`.

An `insufficient` assessment may only tighten an accidentally permissive chief result to
`需人工复核 / 是`; it can never upgrade publishability, override a blocker, create an
outcome or change a valid user choice. Other levels are descriptive only.

## Proposed feature packages

### PKG-075 / F-059: Deterministic decision-support contract

Add a bounded `DecisionSupportAssessment` to Schema 2.6 with exact level, canonical
basis codes, canonical limitation codes, a deterministic assessment-basis identifier and
an outcome-coherence flag. Define a total truth table for clean, edited, deterministic
blocker, critical model issue, unresolved-context, partial/zero coverage, pending,
degraded, fallback, user-choice and continuation paths.

### PKG-076 / F-060: Conservative coherence and compatibility

Integrate assessment after structured adjudication and before digest/persistence. Prove
that insufficient evidence can only tighten a permissive disposition, while blocker and
user-authority rules remain unchanged. V1 and V2.0-V2.5 records load with
`not_recorded`; metadata projections retain only bounded content-free assessment fields.

### PKG-077 / F-061: Concise calibrated presentation and receipt 1.1

Add one short `结论依据` line before the final disposition in the existing chief section.
The final disposition remains exactly once and last, the five-section report and 3,200
hard cap remain unchanged, and codes remain in structured history rather than cluttering
normal prose. Verification receipt 1.1 adds the same canonical assessment without
changing the five-tool surface or retrieval purity.

### PKG-078 / F-062: Thirty-case calibrated Golden evidence

Extend the executable 24-case corpus with six deterministic calibration cases: clean
full coverage, deterministic blocker, material model edits, unresolved material context,
partial coverage and a valid user decision with completed reconsideration. Preserve the
existing eight metrics at 1.0 and add exact support-level accuracy, zero false reassurance
for insufficient cases and blocker/disposition coherence.

### PKG-079 / F-063: V0.13 release and operator documentation

Migrate package/module/build identifiers, Schema 2.6 and receipt Schema 1.1; refresh only
editable-root lock metadata; build fresh wheel/sdist artifacts; and document the
difference among context confidence, reviewer coverage, decision support and final
publishability.

## Q-015 live gate

After protected-main publication, normal Goose should run three bounded cases with the
unchanged extension command:

1. a clean lightweight case: `well_supported`, full coverage and `可发布 / 否`;
2. a standard material-edit case: `supported_with_limits`, full coverage and
   `修改后可发布 / 否`; and
3. an unresolved-material-context case with interaction disabled: `insufficient` and
   `需人工复核 / 是`.

Each case must expose the same level and reason codes in normal report, full record and
verification receipt 1.1 without model reconstruction. Deterministic-blocker
`well_supported / 需人工复核` behavior is a mandatory local and installed-wheel gate; it
does not require a fourth live provider run.

## Explicit non-goals

- No numeric confidence, percentage, probability, score or threshold tuning.
- No averaging reviewer confidence, majority voting or role-authority weighting.
- No new reviewer, prompt-only self-evaluation, provider/model router or sampling call.
- No new public MCP tool, budget, concurrency or interaction.
- No file/batch translation, TM/TB/SG ownership or edit application.
- No change to issue clustering, concrete outcome eligibility or deterministic Policy
  Gate authority except the one-way insufficient-evidence safety tightening.
- No ordinary raw evidence dump or expansion beyond the existing report cap.

## Alternatives considered

Batch/cross-segment consistency and long-document chunking remain outer-agent workflow
responsibilities under the review-only product boundary. More roles increase cost without
answering whether evidence is sufficient. Dynamic provider routing would mix cost policy
with epistemic quality. Numeric confidence would look precise while depending on
uncalibrated model self-report. Deterministic categorical support is the smallest product
addition that helps users interpret the process they already see.

## Principal risks

1. Users may read `well_supported` as “translation is correct.” Presentation must say it
   supports the disposition, including a negative or human-review disposition.
2. A derived label can become a second adjudicator. Only `insufficient` may tighten, and
   no level may relax Policy Gate or human-review requirements.
3. Reason-code growth can leak prose or become unstable. Freeze a bounded vocabulary and
   project only structured facts.
4. Compatibility defaults can fabricate historical certainty. Pre-2.6 records must say
   `not_recorded`.
5. Another line can reintroduce verbosity. Keep it to one concise line before the final
   disposition and preserve all current caps.

## Readiness judgment

The Campaign is bounded, testable and aligned with the process-first product purpose.
It uses the trustworthy measurement/export layer completed by CAMPAIGN-012 and does not
expand into translation execution. The Foreman should freeze the exact categorical
contract and dispatch CAMPAIGN-013-r1 with five sequential packages plus Q-015 as a
separate post-publication live gate.
