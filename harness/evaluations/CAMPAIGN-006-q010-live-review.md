# Live Goose Review: CAMPAIGN-006 Q-010

## Control

- Role: FOREMAN
- Gate: `Q-010` context-coherent panoramic Council live evidence
- Decision: `PARTIAL_LIVE_EVIDENCE / REVALIDATION_REQUIRED`
- Tested published build: `1f8e6981b9fdef08f42a35fc52c7a216b123a94a`
- Clean review ID: `20260813T023927996099Z_db4c1f516512`
- Mixed review ID: `20260813T030002465017Z_4b6fcf69ea45`
- Evidence: user-supplied first primary reports, Goose follow-up prose audits, and independent source/schema inspection at protected-main `dcdb722b328f1dfbee697af480ee06d2d9fa50b1`

## Accepted clean live evidence

- Normal Goose loaded package/module `0.8.0`, build `context-coherent-council-v6` and schema `2.2` from the pinned published revision.
- The first primary response directly showed the Council rather than a diagnostic checklist.
- The clean marketing case displayed all six intended Chinese lenses: fidelity,
  terminology, product context, brand voice, risk/ambiguity and fluency.
- The caller's explicit brand usage, approved glossary and brand guidance produced no
  redundant context interaction in the primary report.
- The six perspectives converged on retaining `比大更大`; the report remained concise,
  omitted empty interaction sections and placed `可发布 / 否` last.
- This live evidence closes the presentation/usability intent previously tracked by
  Q-009. Q-009 can be accepted, while literal telemetry claims in the Goose follow-up
  remain inadmissible for Q-010.

## Invalid Goose telemetry reconstruction

Both follow-up answers claim to copy raw fields, but several values cannot be emitted or
loaded by V0.8:

1. Current role IDs are `terminology_reviewer`, `brand_voice_reviewer` and
   `fluency_reviewer`; the reported `terminology_consistency_manager`,
   `brand_tone_gatekeeper` and `naturalness_polisher` are not registered IDs.
2. `independent_reviews[].agent_name` stores the role ID, not the Chinese display name.
3. `sample_status` is `structured_success|unavailable`; reported `success` is invalid.
4. `reviewer_coverage` is `full|partial|none|not_applicable`; reported numeric `1.0` is
   invalid.
5. `ContextGapInteraction.action` is one of `accept|decline|cancel|unsupported|malformed|
   error|skipped`; reported `none` is invalid.
6. Runtime metadata exposes integer total and phase elicitation counts; the reported
   free-form object attributing six independent reviews as elicitation is not the schema.
7. `fallback_reason` is a bounded string in current records, not an absent/null semantic
   invented by the prose summary.

Therefore the role display and primary report are usable live evidence, but the claimed
raw telemetry fields are an outer-agent reconstruction and cannot satisfy literal Q-010
audit requirements.

## Mixed-case evidence and interaction mismatch

The mixed primary report proves that the server did detect the intended material gaps:

- it displays two context questions under `你的决定与复议`;
- both are marked `已回答` with concrete values copied from the original caller context;
- two background reconsideration effects are displayed;
- the Council then returns a conditional `修改后可发布` disposition.

Those visible facts directly contradict the follow-up claim that `context_gaps=[]`,
`requested=false`, `action=none`, and `sampling_calls=6`. Two completed background
reconsiderations require at least two additional samples after the six independent
reviews, so this path used at least eight samples, with a possible additional discussion
sample depending on the literal record.

The intended test answer was the exact assumption value `由 Council 按现有证据继续，不提供额外背景`.
Neither displayed answer equals that value. Goose or its host interaction layer instead
submitted ordinary non-empty strings derived from the original prompt. The server is
designed to treat an accepted non-assumption form value as a real answer, so it performed
context reconsideration and continued. This run did not exercise the unresolved-context
branch and therefore neither passes nor disproves it.

## Latency diagnosis

The dominant delay is live model sampling, not local MCP record lookup or deterministic
aggregation:

- the independent-review loop awaits six role samples sequentially;
- affected context reconsiderations are also awaited sequentially, up to three;
- an optional discussion sample and up to three outcome reconsiderations are additional
  sequential phases;
- Goose may then make diagnostic/history tool calls and generate its own prose audit,
  but those local tool reads are comparatively small.

Consequently the clean path waits for approximately six provider round trips. The mixed
path shown here waits for at least eight. End-to-end duration is therefore roughly the
sum of provider latencies, response generation and any user/host elicitation delay, not
the duration of one model request. The V0.8 implementation intentionally optimized
quality and panoramic coverage, not latency.

## Gate decision

- Q-009: `ACCEPTED` by the clean V0.8 first-response evidence.
- Q-010: `PARTIAL_LIVE_EVIDENCE`; clean marketing behavior and mixed-gap detection are
  live-proven, but the conservative unresolved path and literal record telemetry remain
  unverified because Goose auto-submitted different context answers and reconstructed
  invalid fields.
- No production-code defect is established by these two reports, so no implementation
  correction contract is issued yet.

## Required revalidation

Run the mixed case with `interactive_mode=off`. This deterministically prevents Goose
from auto-filling the context form. The literal server record must then show selected
unanswered material gaps, `context_gap_interaction.action="unsupported"`, zero outcome
elicitation, no user decisions, lowered confidence, warning/fallback
`material_context_unresolved`, status `NEEDS_HUMAN_REVIEW`, and chief human-review
disposition.

Request the full record as a JSON code block from `view_review_record(...,
detail_level="full")` and reject any answer that renames keys, translates IDs, converts
literal enums, or summarizes numeric fields. If Goose cannot return literal JSON, the
primary report plus a direct MCP client capture is required instead.
