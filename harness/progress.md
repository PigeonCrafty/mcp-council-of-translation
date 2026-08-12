# Council of Translation Harness Progress

## Control

- Role: FOREMAN
- Mode: STRICT_CAMPAIGN
- Campaign: `CAMPAIGN-003-r2`
- Campaign state: `ACCEPTED / CLOSED`
- Accepted implementation HEAD: `9dac21dd3cee9d9a299786e8cdec525f28a0c517`
- Last updated: 2026-08-12 Asia/Shanghai
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
- Publication status: local only; not yet pushed after Campaign acceptance
- Remaining validation: Q-008 source/target-only live Goose briefing and Q-009 process-first digest usability

## Current risks

1. Multiple elicitation checkpoints must remain bounded and must not make ordinary source/target-only reviews feel like a questionnaire maze.
2. Goose controls actual form rendering, so production schemas and display text must be independently verified without assuming a custom client UI.
3. Adaptive context-gap reconsideration can consume the expanded standard budget; deterministic tests prove the 13-call reference path, while live Goose/provider behavior remains to be observed.
4. Process visibility must expose structured claims and evidence without turning into duplicated reviewer prose or hidden chain-of-thought.

## Next step

Commit the Foreman-owned Campaign 003 acceptance assets, publish the accepted commits through the protected-main workflow, then run pinned-commit Goose tests for Q-008 and Q-009. Do not mark either live gate accepted without inspecting real persisted records and user-visible interaction evidence.
