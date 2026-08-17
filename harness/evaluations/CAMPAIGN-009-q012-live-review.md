# Live Goose Review: CAMPAIGN-009 Q-012 V0.10.1 Revalidation

## Decision

`CHANGES_REQUESTED`

All three normal-Goose records are admissible and prove that V0.10.1 is transport-safe,
budget-safe, concurrency-compatible and semantically conservative. Case A passes. Cases
B and C expose one bounded remaining defect: the structured evidence is correct, but the
primary chief section still maps one human repair to several repeated work items when
live model spans or deterministic messages differ syntactically.

## Control

- Role: `FOREMAN`
- Harness mode: `STRICT_CAMPAIGN`
- Gate: `Q-012` value-first Council live usefulness and non-repetition evidence
- Protocol: `harness/contracts/CAMPAIGN-009-q012-live.md`
- Published product commit: `f3b232cb2f3c9500fed04d204ef6198f2ee49af4`
- Published archive commit: `9cd0f317ca6ecedef3477ac322c73189d430ded8`
- Package/build/schema: `0.10.1` / `evidence-value-council-v8.1` / `2.4`
- Case A: `20260817T065433950821Z_5ca7ecf52b3a`, SHA-256
  `3652A7F55AEB1C25BAA34905C2E922957C6B184A58DF80CC513A5B1D20820F41`
- Case B: `20260817T065512032949Z_e19fcdfc832c`, SHA-256
  `80C7A47D1B0330A40A824B47C718A92B9C84C399FB548D9EA60E90320CDC5CEF`
- Case C: `20260817T065532734548Z_0270f5294463`, SHA-256
  `07EB4B9E331B188B035D3397F6C2E418F8CDF3AB2E6872E8236EE914F773857B`
- Evidence authority: the three persisted JSON files under `.tmp/q012`

## Shared admission and safety evidence

- Every record has the required package/build/schema and exact common review settings.
- Concurrency is `3/configured`; observed peaks are three and batch counts are two.
- Sampling is A `6/13`, B `7/13`, C `5/13`; no elicitation, retry or hidden budget
  overrun is present.
- Planned-role coverage is full in every case; successful/unavailable counts are A
  `6/0`, B `6/0`, C `4/0`.
- Parse failures, degradation, warnings and fallback are absent.
- `review_only` is preserved and every `suggested_translation` is null.
- Primary text has exactly the required five sections, ends with chief disposition and
  contains no internal issue/cluster/position/decision/option/gap identifier.
- Wall times are A 6,094 ms, B 11,579 ms and C 8,226 ms; accumulated sampling wait may
  exceed wall time because independent reviews overlap as designed.

## Case A — accepted

Six marketing roles completed and all six are `confirmation_only`. There are no clusters
or discussion turns. The 369-code-point report groups all six role names into exactly one
confirmation line, reports no false issue and ends in unqualified publishability. Case A
satisfies its protocol criteria.

## Case B — semantic safety passes, primary work-item identity fails

The deterministic placeholder checks remain critical blockers. Six reviewers complete,
the `cannot` to `可以` reversal remains visible as a separate critical semantic defect,
discussion adds zero evidence and changes no position, and the chief requires human
review. These safety outcomes pass.

The full record correctly preserves eight auditable clusters: three deterministic
preflight clusters, three reviewer cluster families for the missing `{count}` anchor and
two reviewer cluster families for the semantic reversal. Primary rendering may not
mutate those facts. It must, however, project them into human work items.

That projection still fails. The chief presents these three implementation messages as
three separate must-fix entries for the same `{count}` repair:

1. `explicit do-not-translate literal missing`
2. `explicit caller hard constraint violated`
3. `missing=['{count}']; extra=[]`

The coverage line also exposes `required_literal:{count}` as an implementation-oriented
anchor label. This violates the Case B requirement that deterministic and reviewer
evidence form one logical issue and one primary work item. The distinct semantic reversal
must remain a second work item.

## Case C — semantic value passes, non-repetition fails

The omitted `only ... while the app is open` scope is material and visible before the
chief. One fidelity cluster and one terminology/fluency cluster preserve distinct
structured category identity on the same bounded source/candidate spans. Discussion
adds zero evidence and changes no position, no unsupported statute or hidden reasoning
appears, and the chief correctly requires modification before publication.

The primary chief section nevertheless repeats the same repair twice under `建议修复`
and twice under `执行顺序`. Keeping two full structured clusters is intentional; asking
the user to perform the same wording repair four times is not. The primary projection
must state the repair once while retaining materially distinct accuracy, user-understanding
or risk consequences in bounded supporting text.

## Independent regression evidence

The existing relevant offline suite passes `25 passed` across live-shaped V0.10.1,
V2.4 presentation and value-metric tests. This confirms a regression-coverage gap rather
than a pre-existing red suite: current fixtures use syntactically cooperative chief
messages and do not reproduce the admitted live span/message variants.

## Required correction

Issue CAMPAIGN-010-r1 as a presentation-only V0.10.2 correction:

1. Build a bounded primary-only human work-item identity from existing structured
   anchors and deterministic provenance, including protected-token extraction from
   required-literal/DNT/preflight checks.
2. Collapse all primary chief entries for one repair even when generic deterministic
   messages omit the literal; render natural user language instead of check telemetry.
3. Keep distinct repairs separate and retain materially distinct consequences once.
4. Preserve clusters, findings, metrics, full history, Policy Gate, sampling, prompts,
   roles, routing, schema, tools, budgets and concurrency byte-for-byte where applicable.
5. Add sanitized live-shaped B and C counterexamples without committing raw live records.

Q-012 remains `CHANGES_REQUESTED`. No Goose reply text is needed because all required
evidence is present in the persisted records.
