# Council of Translation Harness Progress

## Control

- Role: FOREMAN
- Mode: STRICT_CAMPAIGN
- Campaign: `CAMPAIGN-007`
- Campaign state: `ACCEPTED / PUBLISHED / Q011_ACCEPTED / CLOSED`
- Campaign baseline: `641ef46b6fdde380463b40d39a654cf8eb1248c2`
- Last updated: 2026-08-13 Asia/Shanghai
- Completion authority: Foreman only

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

## Next step

CAMPAIGN-007 is closed at published `main`
`641ef46b6fdde380463b40d39a654cf8eb1248c2`. Retain default concurrency three and the
documented sequential override. Select the next product opportunity from user experience
or a new audit; no Campaign 007 Worker assignment remains active.
