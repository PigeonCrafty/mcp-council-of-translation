# Council of Translation Harness Progress

## Control

- Role: FOREMAN
- Mode: STRICT_CAMPAIGN
- Campaign: `CAMPAIGN-012`
- Campaign state: `PUBLISHED; Q-014_ISSUED`
- Active contract: none
- Accepted implementation: `e940044c5367ff2ef86e4c58bd75e1f85e4da4cf`
- Accepted review: `harness/evaluations/CAMPAIGN-012-r3-review.md`
- Accepted review SHA-256:
  `9948709C712A5F39738BA7DA13692CCD818C3E27C833D9571AC835B913956415`
- Accepted features: `57/57`
- Accepted quality gates: `13/14`; Q-014 issued
- Active post-publication gate: `Q-014`
- Live contract: `harness/contracts/CAMPAIGN-012-q014-live.md`
- Publication review: `harness/evaluations/CAMPAIGN-012-r3-publication-ci-review.md`
- Next Campaign assessment:
  `harness/evaluations/NEXT-CAMPAIGN-012-ASSESSMENT.md`
- Accepted correction contract: `harness/contracts/CAMPAIGN-011-r3.md`
- Correction contract SHA-256:
  `BA884359309326C179E5A42AF44D24872B960FD0D717130B59E88C534066C64A`
- Published protected `main`: `6c4366f7a43135388d0cf68655a6a3638d6bbe1b`
- Published product implementation: `213cce55bb21d6854f76e89bee33a4e9e2f9dd8c`
- Last updated: 2026-08-24 Asia/Shanghai
- Completion authority: Foreman only

## Campaign 012 assignment and r1 review

- Design assessment: `harness/evaluations/NEXT-CAMPAIGN-012-ASSESSMENT.md`.
- Parent implementation contract: `harness/contracts/CAMPAIGN-012-r1.md`.
- r1 decision: `CHANGES_REQUESTED` by
  `harness/evaluations/CAMPAIGN-012-r1-review.md`.
- r1 implementation HEAD: `06b0e378adc99826c48cd9fc7cc4337d8bc25367`.
- r2 decision: `CHANGES_REQUESTED` by
  `harness/evaluations/CAMPAIGN-012-r2-review.md`.
- r2 implementation HEAD: `5819a92e352c468021c3a8f30aa488508e4223f4`.
- Accepted bounded correction: `harness/contracts/CAMPAIGN-012-r3.md`.
- Product target: package/module `0.12.0`, build
  `verifiable-evidence-council-v10`, persisted Review Schema `2.5`, verification receipt
  schema `1.0`.
- Accepted features: F-053 through F-057 by combined CAMPAIGN-012-r1/r2/r3 evidence.
- Frozen tool change: add only `detail_level="verification"` to the existing
  `view_review_record`; the public tool count remains five.
- Frozen authority boundary: receipt projection is deterministic, privacy-safe,
  read-only and sampling-free; normal review reports, routing, Policy Gate, adjudication,
  persistence and budgets remain unchanged.
- Q-014 is issued after local acceptance and protected-main publication. It is a
  user-operated normal-Goose gate; the Main Worker is forbidden from live
  Goose/provider calls and cannot accept Q-014.

### r1 preserved evidence and correction boundary

- Exact five commits and 14 authorized implementation paths; index empty and protected
  user/Foreman assets preserved.
- Independent compile, `334 passed` full regression, `38 passed` focused receipt/tool
  matrix, Golden selection and `git diff --check` pass.
- Preserved product: package/module `0.12.0`, build
  `verifiable-evidence-council-v10`, persisted Schema `2.5`, receipt Schema `1.0`, exact
  five tools, budgets 6/13/18 and concurrency 3/3.
- Blocking privacy counterexample: a path-shaped hostile `parent_review_id` survives
  both receipt channels without redaction.
- Blocking boundedness counterexample: 100 duplicate active roles produce 100 sample
  rows and a renderer `ValueError`, so public verification retrieval is not total.
- Coherence counterexample: the expected disposition can occur once before a conflicting
  final disposition while `terminal_disposition_matches_structured` remains true.
- Display omission: serving module and Schema are structured but absent from primary
  Markdown despite the frozen record/serving-version requirement.
- r2 scope is only verification projection/rendering plus focused tests. No version,
  package, lock, orchestration, provider or public-surface change is authorized.

### r2 preserved evidence and remaining count boundary

- Parent-ID path/prose privacy, duplicate active-role redaction, exact ordered sample
  projection, terminal coherence and serving-version primary display all pass.
- Independent compile, `84 passed` focused matrix, `360 passed` full regression, Golden
  selection, five-tool/version/schema/budget/concurrency probes and `git diff --check`
  pass.
- Remaining failure: `10**3500` in a non-negative runtime field is emitted as 3,501
  digits and causes `ValueError: verification report exceeds hard cap`.
- Remaining static bound: oversized `independent_reviews` is fully iterated before its
  cardinality mismatch is rejected.
- r3 fixes only JSON-safe count limits and pre-iteration sample cardinality. All r2
  product and artifact evidence is preserved by the accepted final review.

### r3 acceptance

- Decision: `ACCEPTED` by `harness/evaluations/CAMPAIGN-012-r3-review.md`.
- Accepted implementation: `e940044c5367ff2ef86e4c58bd75e1f85e4da4cf`.
- Exact one-commit/three-path scope, 14 protected hashes, byte-identical lock and empty
  index pass.
- Independent evidence: compile, `165 passed` V0.12 matrix, `441 passed` full regression,
  Golden 24/24, JSON-safe count truth table, no-tail sample rejection and actual hostile
  FastMCP verification wrapper.
- Product remains 0.12.0/build v10, persisted Schema 2.5, receipt Schema 1.0, exact five
  tools, budgets 6/13/18 and concurrency 3/3.
- F-053 through F-057 are accepted and published through protected `main` by PR #26.
- Accepted implementation `e940044` maps tree-identically to published `213cce5`; the
  accepted archive maps tree-identically to published main `6c4366f`.
- PR and protected-main CI each passed Ubuntu/Windows Python 3.10/3.12/3.13.
- Q-014 is issued by `harness/contracts/CAMPAIGN-012-q014-live.md`; acceptance requires
  fresh normal-Goose A/B/C receipts and remains with the Foreman.

## Q-013 live review and r3 correction

- Q-013-r2 decision: `ACCEPTED` by
  `harness/evaluations/CAMPAIGN-011-q013-live-r2-review.md`.
- Fresh records A `20260824T055437150459Z_57eb0e6c7126`, B
  `20260824T055650352341Z_13adec94c680` and C
  `20260824T055754842258Z_76bfb2e3afd1` prove the exact standard/lightweight/strict routes.
- Runtime truth is A 7/13, B 4/6 and C 8/18 sampling/budget; all reviewer coverage is
  full, elicitation is zero, no reviewer is unavailable and no run is degraded.
- Structured chief and primary terminal are coherent exactly once and last: A
  `修改后可发布 / 否`, B `可发布 / 否`, C `需人工复核 / 是`.
- Goose narrative misstates some canonical reason codes, role/status names and B/C
  budgets; persisted full records are authoritative and pass the machine verifier.
- CAMPAIGN-011 is complete. All 52 features and all 13 quality gates are accepted.

- V0.11.1 publication decision: `PUBLISHED; Q-013-r2 ISSUED` by
  `harness/evaluations/CAMPAIGN-011-r3-publication-ci-review.md`.
- Protected-main PR #24 rebase-merged at `f64d86f`; all six required Ubuntu/Windows
  Python 3.10/3.12/3.13 checks passed.
- Accepted implementation `76921ec` maps tree-identically to published implementation
  `6d3a5b6`; accepted archive `428ce1e` maps tree-identically to published main `f64d86f`.
- Final normal-Goose contract is `harness/contracts/CAMPAIGN-011-q013-live-r2.md`.
  It requires fresh A/B/C records on V0.11.1/build v9.1 and exact primary/structured
  terminal coherence. Q-013 remains planned until Foreman accepts all three records.

- CAMPAIGN-011-r3 decision: `ACCEPTED` by
  `harness/evaluations/CAMPAIGN-011-r3-review.md` at
  `76921ecb69ec26f0034ec772433e102a3f7715bf`.
- Exact two-commit/11-path scope passed. V0.11.1/build v9.1 preserves Schema 2.5, exact
  five tools, all routing/adjudication invariants, budgets 6/13/18 and concurrency 3.
- Independent complete regression: 311 passed. Golden: 24/24 with all eight metrics 1.0.
  Lock changed only root 0.11.0 to 0.11.1 and retained revision/package/upload-time
  invariants 3/78/586. Fresh source and isolated-wheel probes passed.
- Rebuilding all three exact Q-013 records with the accepted production code yields
  canonical final dispositions once and last: A `修改后可发布 / 否`, B `可发布 / 否`, C
  `需人工复核 / 是`; raw records and structured objects remain unchanged.
- At r3 acceptance time V0.11.1 was local and Q-013 remained unaccepted; protected-main
  publication and fresh normal-Goose A/B/C validation have now completed successfully.

- Decision: `CHANGES_REQUESTED` by
  `harness/evaluations/CAMPAIGN-011-q013-live-review.md` (SHA-256
  `CA5E5098FC18B0C8C9949A6F499FA850EA581BC16EF158E566B2FAFBE4F21A7C`).
- Preparation and all three persisted records prove V0.11/build v9/Schema 2.5, exact
  legal-risk lightweight/standard/strict routes, ordered 4/6/7 roles, full structured
  coverage, bounded sampling, zero elicitation, no degradation and five-section reports.
- Preserved records: A `20260824T034709461394Z_33b581b3d0b6`, B
  `20260824T034736890253Z_ee206d53abf7`, C
  `20260824T034809876049Z_c78aaf84819e`; production load and rerender are exact and raw
  hashes are recorded in the review.
- B is a clean accepted control. C correctly retains deterministic `{terms_url}` blockers,
  the distinct authorization-scope expansion and required human review. Case A correctly
  exposes authorization, precision, partner-scope and withdrawal-right errors.
- Failed criterion: Case A's structured chief is `修改后可发布 / 否`, but its primary final
  line is `需人工复核 / 是`. Root cause is deterministic: the six-entry primary checklist
  cap discards the terminal disposition and activates the renderer's safety fallback.
- Goose narrative omitted required structured fields for A/B and invented non-canonical
  C fields; persisted JSON is the evidence authority. Reported external durations also
  conflict with record telemetry and are not accepted as timing truth.
- CAMPAIGN-011-r3 is issued at exact published-main baseline `938c3a4` to preserve the
  canonical final disposition outside the action cap and release V0.11.1/build v9.1.
  Routing, roles, structured adjudication, Schema 2.5, tools and budgets are frozen.

## Campaign 011 r1 review and r2 correction

- Final decision: `ACCEPTED` by
  `harness/evaluations/CAMPAIGN-011-r2-review.md`.
- Accepted implementation: `565e97d19efbbd7ff009f747a48979fceb002d11`.
- F-047 through F-052 are accepted by combined r1/r2 evidence.
- Independent final evidence: exact twelve-path/one-commit r2 correction; protected hashes;
  compile; 307 full passes; direct 4/6/7 route, version/schema/tool/budget/concurrency probes;
  exact 24/24 Golden with eight metrics at 1.0; pinned lock check; fresh wheel/sdist and
  wheel-origin registration smoke.
- Product: package/module `0.11.0`, build `risk-coherent-council-v9`, Schema `2.5`;
  exact five tools, review-only behavior, budgets 6/13/18 and concurrency controls retained.
- Publication and Q-013 normal-Goose risk-routing validation remain separate gates.

- r1 decision: `CHANGES_REQUESTED` by
  `harness/evaluations/CAMPAIGN-011-r1-review.md`.
- Preserved r1 implementation: five scoped commits through
  `1ae3a7419c1eaeb293a944a49d0873cdf95952e1` implement PKG-057 through PKG-061.
- Preserved evidence: focused package suites passed; Golden is exactly 24/24 with 148
  scripted samples, four elicitations, total budget 296 and all eight aggregate metrics
  at 1.0; the committed 15-path diff passes `git diff --check`.
- Independent reproduction: `19 passed, 3 failed`. One current-runtime test still asserts
  Schema 2.4 and was omitted from r1's allowed paths; two persistence tests still assert
  V0.10.2/build v8.2. These are stale release assertions, not routing failures.
- Active r2 scope: authorize only the omitted test plus existing PKG-062 release paths,
  finish the admitted unstaged release intermediate, update the root lock to 0.11.0 and
  complete regression/build/isolated-wheel evidence in one commit.
- At the r1 checkpoint F-047 through F-052 remained pending final Campaign acceptance;
  the final r2 decision above now accepts them. Q-013 remains post-publication planned.

### Original r1 assignment

- Goal: V0.11 risk-coherent panoramic routing without expanding the Council beyond
  translation QA.
- Trigger: standard `legal_risk` currently selects four roles and omits the existing
  product-context, UX-copy and risk-ambiguity perspectives.
- Frozen legal-risk portfolios: lightweight 4, standard 6, strict 7. Standard remains
  within the exact deepest-path budget `6+3+1+3=13`; strict remains within 18.
- F-047 through F-052 were the r1 plan: explicit routing profiles, risk-sensitive portfolios,
  Schema 2.5 provenance/compatibility, concise presentation, 24-case Golden corpus and
  V0.11 release migration.
- Frozen release: package/module `0.11.0`, build `risk-coherent-council-v9`, schema `2.5`.
- Preserved: exact five tools, review-only default, 6/13/18 budgets, concurrency 3,
  evidence hierarchy, user authority, no-vote adjudication, five-section report and all
  non-legal route portfolios.
- Admission evidence: compile passed and `294 passed` at exact baseline.
- Worker reports: `harness/reports/CAMPAIGN-011-r1-ledger.md` and
  `harness/reports/CAMPAIGN-011-r1-worker.md`, both untracked/unstaged.
- Worker may create at most three bounded subagents but owns integration and final
  verification. Live Goose/provider calls, push, PR, release and deployment are forbidden.
- Q-013 is planned as a separate post-publication normal-Goose risk-routing gate; no
  Worker or offline Campaign evidence can accept it.

## Campaign 011 publication and Q-013 issuance

- Publication decision: `PUBLISHED; Q-013 READY` by
  `harness/evaluations/CAMPAIGN-011-publication-ci-review.md`.
- PR #23 used protected `main` and rebase merge; published `main` is
  `938c3a4bb9f14c7688286b25eabd8aff9f18a09d`.
- Accepted implementation `565e97d` maps byte-for-byte to published implementation
  `7f7d050`; accepted archive `84ddf7b` maps byte-for-byte to published archive `938c3a4`.
- All six required Ubuntu/Windows Python 3.10/3.12/3.13 CI jobs passed before merge.
- Local `main` was reconciled to protected `origin/main`; tracked state is synchronized
  while existing untracked user assets remain untouched.
- Q-013 is issued by `harness/contracts/CAMPAIGN-011-q013-live.md`. It uses the unchanged
  normal-main Goose extension and three fresh conversations to prove legal-risk
  lightweight/standard/strict routing, live provider coverage and concise user value.

## Q-003 Desktop/CLI r1 review and r2 correction

- Final decision: `ACCEPTED` by
  `harness/evaluations/Q-003-desktop-cli-live-r2-review.md` (SHA-256
  `6757FDB858F46E9251050B4A285FC8D55353E4A14C3FEB296EC5D80FBD87DEA6`).
- CLI-r2 record `20260824T020404602512Z_8a7b36aca994` passed: exact V0.10.2/build
  v8.2/schema 2.4, explicit rich UI context, `briefing_mode=auto` skipped elicitation,
  six successful reviewers, full coverage, `6/13` calls, concurrency peak 3, clean
  completion, five-section 355-code-point report and null suggested translation.
- The r1 CLI pending record remains byte-identical and is retained as truthful evidence
  that native CLI elicitation is unavailable in this workflow; it is not counted as a
  successful review.
- Combined client boundary: Desktop supports native Briefing form round trip; interactive
  CLI supports the documented explicit-context fallback. Identical client widgets are
  not claimed.
- Q-003 is accepted. V0.10.2 now has 46/46 accepted feature items and 12/12 accepted
  quality gates.

- r1 decision: `CHANGES_REQUESTED` by
  `harness/evaluations/Q-003-desktop-cli-live-r1-review.md` (SHA-256
  `2625B52D58578B670600F1A032B4CB8864F338B6C578F0E32BDD9DDE235CEE73`).
- Desktop record `20260824T014417482642Z_da47683d8f04` is accepted for reuse: one
  accepted six-field briefing before sampling, six successful reviewers, full coverage,
  `6/13` calls, bounded concurrency, clean completion, five-section 346-code-point report
  and null suggested translation.
- CLI record `20260824T014635498220Z_cb108a4de83e` is a truthful negative result:
  briefing action `error`, zero samples, coverage `not_applicable`, `RETURNED_PENDING`,
  degraded warning and `briefing_error`; it does not satisfy r1.
- No screenshots were retained. User client attribution and record notes identify the
  runs, but r1's visual-evidence criterion remains unmet. Both records also landed in the
  retained `.tmp/q012` directory rather than the requested q003 directory.
- Root cause decision: r1 over-specified native form parity without prior CLI evidence.
  This is not currently classified as a Council orchestration defect: the server stopped
  before sampling and exposed missing coverage truthfully.
- Active correction: `harness/contracts/Q-003-desktop-cli-live-r2.md`. Preserve the
  accepted Desktop and pending CLI records, then run exactly one CLI explicit-context
  retry with `briefing_mode=auto`; no Desktop rerun or product change is authorized.
- Q-003 remains `partial_live_evidence`. If r2 succeeds, the Foreman may accept the gate
  as Desktop native elicitation plus truthful CLI explicit-context fallback, then
  design-freeze CAMPAIGN-011.

## Q-012 V0.10.2 final revalidation

- Decision: `ACCEPTED` by
  `harness/evaluations/CAMPAIGN-010-q012-live-review.md` (SHA-256
  `4B5AA1461D0C18C8C7A6A190ADDA1EAC3C7BAFAB95F87325C4A47C84F56D9717`).
- Admitted records: A `20260817T080941987242Z_0ad8595c0eb6`, B
  `20260817T081021025085Z_293aa64504ed`, C
  `20260817T081059106488Z_463c1303ed2b`.
- Shared pass: published V0.10.2/build v8.2/schema 2.4, exact signed inputs, concurrency
  `3/configured`, full planned-role coverage, no parse failures, degradation, warnings
  or fallback, five-section privacy-safe primary text and null `suggested_translation`.
- Case A: six marketing roles are grouped in one confirmation line; zero clusters,
  `6/13` calls and a 369-code-point report.
- Case B: deterministic `{count}` blockers remain auditable; primary text contains one
  placeholder repair and one distinct `cannot`/`可以` reversal repair, no execution-order
  repetition, `7/13` calls and truthful required human review.
- Case C: two full structured clusters remain intact while the shared scope repair is
  rendered once with its accuracy/privacy consequences; discussion value is zero,
  `5/13` calls and the report requires modification before publication.
- Independent production-model reload and rerender left all three persisted records
  byte-unchanged; focused presentation/value regressions passed `20 passed`.
- Operational deviation: Goose retained the prior `.tmp/q012` persistence directory
  instead of the newly requested `.tmp/q012-final`. Exact fresh IDs, hashes, signed
  inputs and version metadata make the records unambiguous, so this does not invalidate
  the live evidence.
- Q-012 is accepted and Campaign 010 is closed.

## Q-012 V0.10.1 revalidation

- Decision: `CHANGES_REQUESTED` by
  `harness/evaluations/CAMPAIGN-009-q012-live-review.md`.
- Admitted records: A `20260817T065433950821Z_5ca7ecf52b3a`, B
  `20260817T065512032949Z_e19fcdfc832c`, C
  `20260817T065532734548Z_0270f5294463`.
- Shared pass: published V0.10.1/build v8.1/schema 2.4, configured concurrency 3,
  phase/budget truth, full planned-role coverage, five-section privacy-safe primary
  report, null `suggested_translation`, no degradation or fallback.
- Case A: accepted; six marketing roles are grouped into one confirmation line and the
  369-code-point report is clean.
- Case B: safety outcome accepted, presentation rejected; `{count}` remains blocking and
  `cannot`/`可以` remains distinct, while three deterministic messages still appear as
  three primary must-fix items for one missing anchor.
- Case C: semantic outcome accepted, presentation rejected; the missing scope limitation
  is material and discussion value is truthfully zero, while one repair is repeated as
  two recommendations and two execution-order entries.
- Offline presentation/value tests remain green (`25 passed`) and therefore lack these
  live-shaped counterexamples.
- Active correction: `harness/contracts/CAMPAIGN-010-r1.md`; F-046 is planned.

## Campaign 010 r1 review

- Decision: `CHANGES_REQUESTED` by
  `harness/evaluations/CAMPAIGN-010-r1-review.md`.
- Preserved r1 evidence: deterministic `{count}` checks now render as one natural repair;
  raw check labels are hidden; distinct semantic safety remains; Case A, negative
  controls, complete structured records, V0.10.2 metadata, lock, docs, Golden 18/18,
  packaging invariants and `291 passed` remain valid.
- Exact live replay failure: Case B still renders two semantic-reversal recommendations;
  Case C still renders two recommendations plus two execution-order entries for one
  scope-restoration repair.
- Root cause: model-only grouping requires a non-empty replacement different from the
  current outcome, while admitted live `issue` findings have no `proposed_value` and
  their clusters carry only the current outcome.
- Active bounded correction: `harness/contracts/CAMPAIGN-010-r2.md`; version/build/schema
  remain `0.10.2` / `evidence-value-council-v8.2` / `2.4`.

## Campaign 010 r2 acceptance

- Decision: `ACCEPTED` by
  `harness/evaluations/CAMPAIGN-010-r2-review.md`.
- Accepted implementation HEAD: `f58306d0df42fc27d46dd5049348ccfce8a0f6f8`.
- F-046: accepted by combined r1/r2 evidence.
- Exact scope: one commit and three authorized renderer/test paths; protected assets and
  `uv.lock` are unchanged.
- Independent live-record replay: A 369 code points and unchanged; B 716 code points with
  exactly two repairs; C 1,056 code points with exactly one repair; all records remain
  byte-immutable through rendering.
- Independent verification: compile passed, `294 passed`, lock check passed, exact five
  tools, V0.10.2/build v8.2/schema 2.4, review-only, budgets 6/13/18 and concurrency 3.
- Fresh Foreman wheel/sdist build from final HEAD succeeded; Worker isolated FastMCP
  3.4.7 five-tool smoke remains supporting installed-artifact evidence.
- Publication: protected-main PR #20 merged at
  `2b4297d003a7ac4b69185200c8e2fd96dca738ce`; six PR checks and six post-merge `main`
  checks passed, and the published product tree matches accepted HEAD.
- Q-012 final A/B/C evidence is accepted; see
  `harness/evaluations/CAMPAIGN-010-q012-live-review.md`.

## Campaign 009 r1 review

- Decision: `CHANGES_REQUESTED` by
  `harness/evaluations/CAMPAIGN-009-r1-review.md`.
- Preserved evidence: V0.10.1/build v8.1/schema 2.4, exact five tools, budgets 6/13/18,
  complete `283 passed`, exact 18/18 Golden run, Case A grouped confirmation, Case B
  paraphrase value zero, one primary `{count}` work item, distinct semantic reversal,
  immutable full structured history, fresh package artifacts and lock integrity.
- r1 counterexample 1: existing `RolePosition.rule_refs=["TB-1"]` plus discussion
  `rule_ref:TB-1` is incorrectly reported as one new evidence item.
- r1 counterexample 2: a corroborated disputed issue can lose its material topic and
  render only an anchor-based “相关问题” label.
- Active correction: `CAMPAIGN-009-r2`; no version, schema, tool, prompt, authority,
  sampling, dependency, documentation or lock change is authorized.

## Campaign 009 r2 acceptance

- Decision: `ACCEPTED` by
  `harness/evaluations/CAMPAIGN-009-r2-review.md`.
- Accepted implementation HEAD: `4a3c692ad528db03e4f72a025d60c4eb775454f0`.
- F-045 is accepted by combined CAMPAIGN-009-r1/r2 evidence.
- Independent evidence: exact two-commit/four-path scope, ten protected hashes, compile,
  `286 passed` full, `50 passed` risk-weighted, exact typed-provenance and material-topic
  counterexamples, zero new sampling/elicitation call sites and unchanged structured
  projection inputs.
- Preserved evidence: V0.10.1/build v8.1/schema 2.4, exact five tools, budgets 6/13/18,
  A/B grouped output, exact 18/18 Golden run with 113 samples/four elicitations/eight
  metrics at 1.0, immutable full history and accepted r1 package/lock evidence.
- Publication status: protected-main PR #18 merged at
  `f3b232cb2f3c9500fed04d204ef6198f2ee49af4`; six required CI jobs passed.
- Q-012 status: `changes_requested` until post-publication normal-Goose A/B/C evidence is
  reviewed; local Campaign acceptance is not live-gate acceptance.

## Accepted state

- V0.4.0 is published on protected `main` at `824559afd68f170758837769b1d1d19df991db4b` through PR #2; the required main-branch checks passed.
- All ten V0.4 feature items F-001 through F-010 and local quality gates Q-001, Q-002, Q-004, Q-005, and Q-006 are accepted. The final independent review is `harness/evaluations/CAMPAIGN-001-r5-review.md`.
- The accepted automated baseline contains 117 passing tests, exact five-tool introspection, package/module version `0.4.0`, diagnostic build `structured-deliberation-v2`, review-only behavior, and 6/10/14 sampling budgets.
- The DeepSeek reasoning-first MCP sampling compatibility repair was validated by the user in normal Goose and is external to this repository Campaign.
- A real Goose end-to-end V0.4 run completed successfully and persisted record `20260812T060954605875Z_1d988172bd1f` with full six-role coverage, no reviewer parse failures, a DecisionPoint, elicitation acceptance, reconsideration, adjudication, and retrievable full trace.
- That live evidence satisfies one Goose interactive path but does not establish both Desktop and CLI behavior; Q-003 is therefore `partial_live_evidence`, not fully accepted.
- Campaign 002 V0.5 implementation is accepted at `ca3d24afdc8feaa65286b13c6118720809749436`; F-011 through F-016 are accepted by `CAMPAIGN-002-r3`.
- Independent r3 acceptance evidence includes compile success, 159 passing tests, 36 focused regressions, production counterexample probes, a fresh `0.5.0` sdist/wheel, and isolated FastMCP 3.4.7 wheel smoke.
- V0.5 is published on protected `main` through PR #3 at `daacdbfdd2d3710291c8d792040d08875396b8c5`; all six required Windows/Linux Python checks passed.
- Q-007 is accepted by `harness/evaluations/CAMPAIGN-002-q007-live-review.md`. Live record `20260812T084202537834Z_bebbb7a76fc3` verified explicit Council delegation; record `20260812T084744453115Z_3864366de2b0` verified a valid user outcome, three requested/completed affected-role reconsiderations, 10/10 sampling, clean completion, and final user authority.
- Campaign 002 is closed. V0.5 is the accepted functional foundation for Campaign 003 and must not be reimplemented or weakened.
- Campaign 003 V0.6 implementation is accepted at `9dac21dd3cee9d9a299786e8cdec525f28a0c517` by `harness/evaluations/CAMPAIGN-003-r2-review.md`. F-017 through F-022 are accepted. Independent final evidence includes the corrected deterministic briefing predicate, 11 focused passes, 184 full passes, a real Core briefing path, exact five-tool/version/schema/budget probes and fresh 0.6.0 artifacts.
- V0.6 is published on protected `main` through PR #5 at `b601cf93f452a8e574e3c15a4a9c236cf8142ce1`; all six required Windows/Linux Python checks passed.
- Q-008 is accepted and Q-009 is `changes_requested` by `harness/evaluations/CAMPAIGN-003-q008-q009-live-review.md`. Live record `20260812T113302675410Z_611c7d32146e` proved pre-sampling briefing and six-role process generation, but normal Goose initially displayed only diagnostic fields and required a second prompt to reveal a long repetitive `display_report`.

## Live V0.4 usability findings

The accepted live record is the primary counterexample for Campaign 002:

- The standard MCP client correctly rendered one batched form and one submit button; this is expected behavior and is not a protocol defect.
- Four choices were verbose, overlapping reviewer `action` strings rather than mutually exclusive translation outcomes such as keeping `继续` versus using `下一步`.
- Internal option identifiers and dense descriptions made the form difficult to scan.
- The selected option caused only three of four participant roles to reconsider because the standard 10-call budget was exhausted; `reconsideration_budget_unavailable` was stored while the review still appeared unqualified `COMPLETED`.
- The compact result did not make the effective normalized task, decision rationale, degraded reconsideration, or Council process sufficiently visible.
- The actual record normalized `content_type` to `unspecified` and `audience` to an empty value despite the outer test prompt describing UI context, so effective inputs must be visible in the compact result.
- A clean semantic affirmation was surfaced as an optional improvement, showing that positive confirmation and actionable issues need distinct representation.

## Protected baseline changes

Campaign 003 starts from exact Git commit `fe4b55a6597d8ac18885c0faab14722f44588e12`. The following Foreman/user assets may be dirty and are protected. The Worker must preserve them and must not stage, edit, delete, move, or commit them:

- `mcp-council-of-translation-audit-and-upgrade-recommendations.md`
- `reviews/`
- `.learnings/`
- Foreman-owned `harness/plan.md`, `harness/features.json`, `harness/progress.md`, and all issued contracts/evaluations
- `myTest/` if it appears

The Worker may create only the active Campaign ledger and report under `harness/reports/`. Production, test, and documentation paths are limited by the active contract.

## Frozen V0.6 decisions

- Target package/module version: `0.6.0`; diagnostic build: `guided-deliberation-v4`; write schema: `2.2`.
- Goose-first, review-only, exact five public tools, `interactive_mode=auto`, one standard batched elicitation form, and no custom MCP UI.
- `briefing_mode=auto` is added to `review_translation`; sparse source/target-only input elicits a guided brief before any reviewer sampling, while rich caller context skips redundant questions.
- The default presentation is process-first: case brief, assumptions, blind spots, role lenses, consensus, minority report and material disagreements precede user decisions and the final editor synthesis.
- User-facing choices remain concise, mutually exclusive translation outcomes. Raw reviewer action prose remains evidence, not an option value.
- An explicit `暂不决定，由 Council 裁决` option is always available in interactive decisions.
- User choice is decisive only among Policy-Gate-valid options. Council fallback remains evidence-weighted adjudication rather than majority voting.
- At most one adaptive context-gap follow-up form with two material questions may occur after independent review; it cannot create hard constraints by model assertion.
- Reconsider only contrary or materially affected roles. Sampling budgets are 6/13/18 for lightweight/standard/strict and all skipped/failed work remains truthful.
- Full structured trace remains on demand; no hidden chain-of-thought is requested, exposed or persisted.
- V1, V2.0 and V2.1 records remain readable. New V2.2 full and metadata persistence retain the established privacy contract.

## Campaign 003 acceptance

- r1 decision: `CHANGES_REQUESTED` by `harness/evaluations/CAMPAIGN-003-r1-review.md`
- Preserved r1 evidence: PKG-017 and PKG-019 through PKG-022; all five-tool, V2.2, privacy, process-digest, 6/13/18, compatibility and package-build evidence remains valid.
- r1 correction resolved by r2: PKG-018 auto sufficiency now requires a recognized content type plus at least two independent context categories; the former numeric-only threshold is covered by regression counterexamples.
- r2 decision: `ACCEPTED` by `harness/evaluations/CAMPAIGN-003-r2-review.md`
- Accepted contract: `harness/contracts/CAMPAIGN-003-r2.md`
- Main Worker: Codex in a separate new conversation
- Execution ledger: not required for this one-package correction
- Worker report: `harness/reports/CAMPAIGN-003-r2-worker.md`
- Accepted implementation HEAD: `9dac21dd3cee9d9a299786e8cdec525f28a0c517`
- Publication status: published through PR #5 at protected-main commit `b601cf93f452a8e574e3c15a4a9c236cf8142ce1`
- Live validation: Q-008 accepted; Q-009 changes requested and is the user-facing target of Campaign 004

## Frozen V0.7 presentation decisions

- Package/module target: `0.7.0`; diagnostic build: `concise-council-display-v5`; record schema remains `2.2`.
- Keep exactly five tools, review-only defaults, existing inputs, user authority, Policy Gate, 6/13/18 budgets and all V0.6 persistence compatibility.
- Use FastMCP dual-channel results: concise Markdown is primary MCP text content; the existing compact/full dictionary remains structured content.
- Apply primary text presentation to `review_translation`, `continue_review` and `view_review_record`; diagnostics/list tools remain structured utilities.
- Default human report is Chinese, process-first and five sections or fewer: review brief; professional lenses; consensus/disagreement/blind spots; decisions/reconsideration only when present; chief conclusion last.
- Preserve one concise lens for every active role. Target each lens at 120 characters and include an evidence anchor only when it adds distinct value.
- Clean six-role output targets 1,800 characters; every default report has a hard 3,200-code-point cap. Full evidence remains available through structured content and full record retrieval.
- Positive affirmations contribute to truthful consensus. Role count is coverage evidence, never voting authority.
- Empty context-gap, decision, reconsideration and minority sections are omitted or compressed into one short statement; material dissent, blockers, gaps, degradation and unavailable roles are never hidden.
- No internal IDs, English implementation headings, raw model prose, chain-of-thought or unnecessary Policy Gate counters appear in primary text.

## Campaign 004 assignment

- r1 decision: `CHANGES_REQUESTED` by `harness/evaluations/CAMPAIGN-004-r1-review.md`
- r1 implementation HEAD: `ff0e345ff174f1f39741bbb47979aa51e277ca52`
- Preserved r1 evidence: PKG-023 through PKG-025; PKG-026 field mapping/privacy/layering/bounds; PKG-027 public diagnostics, docs, fresh artifacts and FastMCP 2.13.0.2/3.4.7 dual-channel wheel smoke
- r1 independent verification: 19 authorized files, 14 protected hashes exact, compile pass and `196 passed`; two acceptance counterexamples reproduced
- Active correction contract: `harness/contracts/CAMPAIGN-004-r2.md`
- Main Worker: Codex in a separate new conversation
- r1 ledger/report: `harness/reports/CAMPAIGN-004-r1-ledger.md`, `harness/reports/CAMPAIGN-004-r1-worker.md`
- r2 report: `harness/reports/CAMPAIGN-004-r2-worker.md`; no new ledger required
- r2 scope: correct V0.7 metadata-only history identifiers and case-insensitive internal-ID sanitization only
- Commit policy: at most two scoped local commits; no push, PR, release, deployment, credentials or live provider calls
- Subagents: forbidden for the bounded correction
- r2 decision: `ACCEPTED` by `harness/evaluations/CAMPAIGN-004-r2-review.md`
- F-023 through F-027: accepted by `CAMPAIGN-004-r2`
- Independent r2 evidence: four authorized files, all protected hashes exact, compile pass, `27 passed` focused, `198 passed` full, real metadata/privacy probe, standalone-ID adversarial probe and exact FastMCP five-tool diagnostics
- Accepted Campaign 004 implementation: `3779a78a9788018082470408fdd4d87a042985dc`
- Publication mapping: protected-main PR #6 rebased the accepted implementation to equivalent commit `1e0d93af2462995274514a521f5286bfd978469f`; its tree is byte-for-byte identical to accepted HEAD `3779a78a9788018082470408fdd4d87a042985dc`.
- Archive state: Campaign contracts, Worker evidence, Foreman reviews and acceptance state are archived on protected `main` at `d71b23cd4968ad288f7f5d927fbbc76be7872624`; all six required Windows/Linux Python checks passed.

## Current risks

1. Q-009 remains `changes_requested` by `harness/evaluations/CAMPAIGN-005-q009-live-review.md`: Campaign 005 presentation reached Goose, but standard marketing coverage, material-context precedence and final disposition remain insufficient.
2. FastMCP 2.13 emits the previously disclosed upstream Authlib deprecation warning, although r1 compatibility smoke passed.
3. Goose's second audit answer misreported `sampling_calls` as 0; the persisted record proves 6/13 with full six-role coverage. This is outer-agent summarization error, not server execution failure.

## Campaign 005 assignment

- Contract: `harness/contracts/CAMPAIGN-005-r1.md`
- Target: package/module `0.7.1`; diagnostic build `concise-council-display-v5.1`
- Package graph: PKG-030 primary microcopy correction, then PKG-031 patch migration and evaluation
- Frozen boundary: deterministic primary presentation and version/docs/tests only; no Council logic, prompt, sampling, schema, tool or budget change
- Main Worker: Codex in a separate new conversation
- Subagents: forbidden for this tightly bounded two-package correction
- Commit policy: at most two scoped local commits; no push, PR, release, deployment, credentials or live provider calls
- Required report: `harness/reports/CAMPAIGN-005-r1-worker.md`; no ledger required

## Campaign 005 acceptance

- Decision: `ACCEPTED` by `harness/evaluations/CAMPAIGN-005-r1-review.md`
- Accepted implementation HEAD: `c8616eb66b49de4be00672e6439ad6b1ea468967`
- F-028 and F-029: accepted by `CAMPAIGN-005-r1`
- Independent evidence: exact 16-path scope, ten protected hashes, compile pass, `42 passed` focused, `203 passed` full, 539-code-point live-shaped primary report and unchanged structured evidence
- Package evidence: fresh 0.7.1 wheel/sdist and isolated FastMCP 3.4.7 exact-five-tool smoke passed
- Publication state: published through protected-main PR #8 at `e2e2ba34dc890591a66d60b86e1373eb0316e80b`; all six Windows/Linux Python checks passed
- Publication mapping: rebase commits `2580536` / `f34073f` / `e2e2ba3` preserve the exact accepted tree from local acceptance commit `cf375be`
- Live state: Q-009 remains `changes_requested` until the published commit passes normal-user Goose revalidation

## Campaign 005 live Q-009 result

- Published presentation correction: live-verified; first answer directly showed a concise Council process without procedural counters or redundant clean-role evidence
- Live counterexample: `bigger than bigger` → `比大更大` combined marketing with retained UI-button context
- Deterministic source finding: standard marketing currently activates only fidelity, terminology and fluency
- Context finding: two outcome-changing brand/usage questions were suppressed as `immaterial_gap`, after which wording selection proceeded and the chief returned an unqualified publishable disposition
- Goose audit limitation: its claimed raw values included invalid coverage/status/role IDs and impossible zero call counts; prose audit telemetry is rejected
- Gate decision: Q-009 remains `changes_requested`; Q-010 is planned for clean and deliberately mixed-context live evidence

## Campaign 006 assignment

- Active contract: `harness/contracts/CAMPAIGN-006-r3.md`
- r2 decision: `CHANGES_REQUESTED` by `harness/evaluations/CAMPAIGN-006-r2-review.md`
- r2 implementation HEAD: `8ed8d866076acab9dc22a57c6fd31d4ff6792fe4`
- Preserved r2 evidence: PKG-033 through PKG-036; PKG-032 material-impact grammar/bounds except caller-context-aware `already_answered`; exact 23-path scope, compile, 217 tests, six-role/deep-budget/presentation/runtime probes and fresh artifacts
- r3 correction: suppress official glossary/reference questions when the corresponding caller packet is already supplied; suppress brand-versus-functional questions only when caller usage is unambiguous, while preserving questions for missing or conflicting marketing/UI context
- r3 decision: `ACCEPTED` by `harness/evaluations/CAMPAIGN-006-r3-review.md`
- Accepted implementation HEAD: `f3e9bde1b74ff4591d91b66a38558b8bebe6efab`
- F-030 through F-034: accepted by `CAMPAIGN-006-r3`
- Independent final evidence: exact four-file/one-commit correction scope, all protected hashes exact, compile pass, 39 focused passes, 220 full passes, Chinese/English direct-answer truth table, exact five tools/version/schema/defaults/budgets and six-role marketing route
- Preserved r2 evidence: deep 13/13 call path, context-first conservative status, concise presentation, literal V2.2 invariants, fresh 0.8.0 artifacts and installed FastMCP 3.4.7 wheel behavior
- Publication: protected-main PR #11 merged at `1f8e6981b9fdef08f42a35fc52c7a216b123a94a`; all six required Windows/Linux Python checks passed
- Publication mapping: accepted implementation `f3e9bde1b74ff4591d91b66a38558b8bebe6efab` maps to rebased remote implementation `fbe0eb1de63b6d26b4ffbf96e5e05b76fe4b86f8`; accepted archive tree and published tree are exactly `f832035855fd60ff7f3bf0b0dea4caf17d4df877`
- Q-009: accepted by the clean V0.8 Goose first response, which directly showed six concise marketing lenses, consensus and a verdict-last disposition
- Q-010: accepted by `harness/evaluations/CAMPAIGN-006-q010-r2-live-review.md`; the off-mode mixed case visibly lowered context confidence, preserved two unanswered blind spots, omitted outcome selection and ended in required human review
- Structured-channel boundary: the server returns Markdown plus unchanged `structured_content`; Goose exposed only Markdown to its outer model and then reconstructed invalid literal fields, so those prose telemetry claims remain rejected
- Live latency finding: the off-mode six-role path took 15.31 seconds; independent role samples and context/outcome reconsiderations are sequential, and the prior mixed path required at least eight provider round trips, so provider sampling dominates local MCP processing
- Superseded contract: `harness/contracts/CAMPAIGN-006-r1.md`; PR #10 published its Foreman assets and thereby advanced `main`, so its earlier baseline must not be executed
- Target: package/module `0.8.0`; diagnostic build `context-coherent-council-v6`; schema remains `2.2`
- Package graph: PKG-032 context-gap classification; PKG-033 context precedence/status; PKG-034 marketing role routing; PKG-035 presentation/invariants; PKG-036 migration/build/docs
- Frozen marketing route: standard and strict use fidelity, terminology, product context, brand voice, risk/ambiguity and fluency; lightweight remains narrow
- Public invariants: exact five tools, review-only, current defaults and budgets 6/13/18
- Main Worker: Codex in a separate conversation; implementation subagents forbidden because the packages share guided/orchestration/role/digest boundaries
- Commit policy for r3: one scoped local commit; no push, PR, release, deployment, credentials or live provider calls
- Required report: `harness/reports/CAMPAIGN-006-r3-worker.md`; no new ledger required

## Campaign 007 acceptance

- r1 implementation HEAD: `61252ae27823467d74c38efaa59aa1521b006752`; r1 decision:
  `CHANGES_REQUESTED` by `harness/evaluations/CAMPAIGN-007-r1-review.md`
- r2 accepted HEAD: `e835566a2c8d60ba153b68175d19685cb96185fe`; decision:
  `ACCEPTED` by `harness/evaluations/CAMPAIGN-007-r2-review.md`
- F-035 through F-039: accepted by combined r1+r2 evidence
- Independent final evidence: exact four-file/one-commit r2 correction, three delayed
  counterexamples, 83 focused passes, 246 full passes, compile, protected hashes, fresh
  wheel/sdist and preserved installed FastMCP 3.4.7 five-tool behavior
- Product: package/module `0.9.0`, build `bounded-parallel-council-v7`, schema `2.3`;
  exact five tools, review-only and budgets 6/13/18 preserved
- Runtime: default independent-review concurrency 3; operator values 1/2/3; invalid
  values safely use sequential limit 1; later Council phases remain ordered
- Q-011: `ACCEPTED` by
  `harness/evaluations/CAMPAIGN-007-q011-live-review.md`; six normal-Goose records
  retained full coverage and clean protocol behavior, with sequential `1/1/6`, parallel
  `3/3/2`, and median wall time reduced from 16,363 ms to 5,712 ms (`65.09%`, `2.86x`)

## Campaign 008 review state

- r1 decision: `CHANGES_REQUESTED` by
  `harness/evaluations/CAMPAIGN-008-r1-review.md`
- r1 implementation HEAD: `6e28c103f98a6b0481ab7d103580b83f8e6c4cfa`
- Preserved r1 evidence: V2.4 models/compatibility/privacy, ordinary structured
  contribution and discussion deltas, five-section value-first layout, exact five tools,
  V0.10 identifiers, budgets/concurrency and fresh artifact behavior
- Independent r1 verification: compile passed; `263 passed` full; `13 passed` focused;
  exact authorized diff and empty index
- Reproduced defect: placeholder-loss preflight correctly blocks release but value
  metrics report zero material issues and confirmation-only coverage, producing a
  contradictory primary report
- Golden defect: all 18 case names exist, but fixture-authored `observed` dictionaries
  duplicate `expected` and no product path derives the observations
- Active correction contract: `harness/contracts/CAMPAIGN-008-r2.md`
- r2 scope: PKG-047 structured preflight contribution/deduplication/prose-fallback
  correction; PKG-048 executable offline 18-case corpus
- Q-012: remains planned and cannot begin before local acceptance and publication

### r2 review

- r2 decision: `CHANGES_REQUESTED` by
  `harness/evaluations/CAMPAIGN-008-r2-review.md`
- r2 implementation HEAD: `6464f96f681aa3531c14cd631689673561193027`
- Preserved r2 evidence: placeholder/markup deterministic contribution correction,
  unavailable precedence, prose-free compatibility fallback, executable 18-case Golden
  runner, real context/continuation authority paths, `269 passed` and fresh artifact
  behavior
- Fresh Foreman evidence: compile; `269 passed` full; `17 passed` focused; 18/18 corpus
  with 113 scripted samples and four scripted elicitations
- Remaining counterexamples: required literal plus matching model finding = two issues;
  numeric parity plus matching model finding = two issues; one missing URL = command and
  URL parity counted as two issues
- Active bounded correction: `harness/contracts/CAMPAIGN-008-r3.md`

### r3 review

- r3 decision: `CHANGES_REQUESTED` by
  `harness/evaluations/CAMPAIGN-008-r3-review.md`
- r3 implementation HEAD: `c3fcfec363878d069b64e15a65a364c7fd55468b`
- Preserved r3 evidence: complete deterministic preflight correlation matrix,
  non-overmerge for placeholder/URL and distinct literals, unavailable precedence,
  `276 passed`, executable Golden 18/18 and fresh artifact behavior
- Remaining regression: two model-only clusters from different issue families but the
  same source/candidate span are incorrectly merged into one corroborated issue
- Active minimal correction: `harness/contracts/CAMPAIGN-008-r4.md`

### r4 acceptance

- r4 decision: `ACCEPTED` by
  `harness/evaluations/CAMPAIGN-008-r4-review.md`
- Accepted implementation HEAD: `84c6c64d40836875cf6515a6bf0c615c9e5ea0c9`
- F-040 through F-044: accepted by combined Campaign 008 r1-r4 evidence
- Independent final evidence: exact two-path/one-commit correction, protected hashes,
  compile, `278 passed` full, `19 passed` focused, `30 passed` V2.4/Golden, `33 passed`
  public/compatibility selection and direct cross-family/same-family/mixed probes
- Golden evidence: exact 18/18 production execution, 113 scripted samples, four scripted
  elicitations and all eight aggregate metrics 1.0
- Product: package/module `0.10.0`, build `evidence-value-council-v8`, schema `2.4`,
  exact five tools, review-only, budgets 6/13/18 and concurrency controls preserved
- Fresh artifact evidence: wheel/sdist and isolated Python 3.12/FastMCP 3.4.7 smoke in
  `harness/reports/CAMPAIGN-008-r4-worker.md`
- Publication status: accepted at protected `main`
- Q-012: pending post-publication normal-Goose usefulness/non-repetition validation

### Publication and Q-012 issuance

- Protected-main publication: PR #17, merged 2026-08-14
- Published `main`: `e3d3de275915088c1430a243dfd9c2e410cbc58a`
- CI: all six required Linux/Windows Python 3.10/3.12/3.13 jobs passed
- Live protocol: `harness/contracts/CAMPAIGN-008-q012-live.md`
- Fixed runtime: one unchanged normal-main extension command, concurrency 3, dedicated
  `.tmp/q012` persistence and one provider/model/account
- Cases: clean confirmation compression; deterministic placeholder correlation plus
  semantic separation; panoramic privacy-copy value without repetitive padding
- Evidence status: awaiting three user-run normal-Goose review IDs

### Q-012 r1 configuration admission failure

- Initial A/B/C attempts: invalid; all returned `review record write failed` and no
  `review_id`
- Evidence directory after attempts: `.tmp/q012` absent
- Goose extension state: `envs: {}` with both variables represented as protected
  `env_keys`; concurrency reached Core as `3/configured`, but the required review path
  did not resolve
- Bounded diagnosis: the protected review-directory value is stale, empty or malformed;
  the strongest concrete hazard is r1's YAML-quoted path being copied into a Goose
  Desktop raw-value input, where the quotes become part of an invalid Windows path
- Corrected protocol: `harness/contracts/CAMPAIGN-008-q012-live-r2.md`
- Repository action: pre-created ignored `.tmp/q012` with inherited write permissions;
  no production, test, dependency, Git or GitHub change
- Gate state: Q-012 remains issued; no valid live case has yet been admitted

### Q-012 admissible Case B and decision

- Valid clean Case A: `20260814T082515308822Z_acd09409c766`, SHA-256
  `8CB528793F5D9F4F97B76822349E6EB1BAB88A3EE6097A4079ADBD9ADF1D81B3`
- Case A evidence: `COMPLETED`, six `structured_success`, full coverage, calls `6/13`,
  all six roles `confirmation_only`, no discussion, 467-code-point report and chief last
- Case A observation: correct and within target, but six identical confirmation lines can
  be grouped while still naming every role once; this alone is not a gate failure
- Valid record: `20260814T082144326698Z_eee1cf4ac053`
- Record SHA-256:
  `5CF9DB8EF84FFF5CE68876E0B0A0A80B54094A71FF1A74C1B4B62DDC91E3879A`
- Actual input: Case B `{count}` placeholder loss plus `cannot`/`可以` reversal
- Preserved live evidence: V0.10/schema 2.4, six `structured_success`, full coverage,
  calls `7/13`, truthful blocker and distinct reversal, no degradation or fallback
- Failed non-repetition: the 1,501-code-point primary report repeats the placeholder
  defect across value, roles, disagreement and three chief work items
- Failed discussion truth: six rephrased statements of existing placeholder/reversal/rule
  facts are reported as six new evidence items; no position changed and no issue resolved
- Outer Goose metric aliases are excluded; persisted Schema 2.4 JSON is authoritative
- Q-012 decision: `CHANGES_REQUESTED`; Case C stopped to avoid unnecessary live cost
- Review: `harness/evaluations/CAMPAIGN-008-q012-live-review.md`
- Active correction: `harness/contracts/CAMPAIGN-009-r1.md`

## Next step

Archive the accepted r1/r2/r3 contracts, reports, reviews and updated Foreman state;
publish V0.12 through protected `main` with all six required CI jobs green. After exact
published-version admission, issue Q-014 for normal-Goose verification-receipt evidence.
