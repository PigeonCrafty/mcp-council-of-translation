# Council of Translation Harness Progress

## Control

- Role: FOREMAN
- Mode: STRICT_CAMPAIGN
- Campaign: `CAMPAIGN-002-r3`
- Campaign state: `ACCEPTED / LIVE_VALIDATION_PENDING`
- Campaign root baseline: `824559afd68f170758837769b1d1d19df991db4b`
- Correction baseline: `f7a4f23865383d52dede37f95de091932918090c`
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

The Campaign starts from exact Git commit `824559afd68f170758837769b1d1d19df991db4b`. The following Foreman/user assets may be dirty and are protected. The Worker must preserve them and must not stage, edit, delete, move, or commit them:

- `mcp-council-of-translation-audit-and-upgrade-recommendations.md`
- `reviews/`
- `.learnings/`
- Foreman-owned `harness/plan.md`, `harness/features.json`, `harness/progress.md`, and all issued contracts/evaluations
- `myTest/` if it appears

The Worker may create only the active Campaign ledger and report under `harness/reports/`. Production, test, and documentation paths are limited by the active contract.

## Frozen V0.5 decisions

- Target package/module version: `0.5.0`; diagnostic build: `outcome-first-decision-v3`; record schema: `2.1`.
- Goose-first, review-only, exact five public tools, `interactive_mode=auto`, one standard batched elicitation form, and no custom MCP UI.
- User-facing choices are concise, mutually exclusive translation outcomes. Raw reviewer action prose remains evidence, not an option value.
- An explicit `暂不决定，由 Council 裁决` option is always available in interactive decisions.
- User choice is decisive only among Policy-Gate-valid options. Council fallback remains evidence-weighted adjudication rather than majority voting.
- Reconsider only contrary or materially affected roles. Preserve 6/10/14 budgets initially and make budget degradation truthful.
- Compact results expose effective task, bounded deliberation summary, decision, degraded state, and warnings; full structured trace remains on demand.
- V1 and V2.0 records remain readable. New V2.1 full and metadata persistence retain the established privacy contract.

## Campaign 002 disposition

- r1 and r2 Foreman decisions: `CHANGES_REQUESTED`; r3 Foreman decision: `ACCEPTED`.
- Accepted correction contract: `harness/contracts/CAMPAIGN-002-r3.md`
- Final implementation commit: `ca3d24afdc8feaa65286b13c6118720809749436`
- Foreman review: `harness/evaluations/CAMPAIGN-002-r3-review.md`
- Worker report: `harness/reports/CAMPAIGN-002-r3-worker.md`
- Preserved r2 report: `harness/reports/CAMPAIGN-002-r2-worker.md`
- Preserved r1 ledger/report: `harness/reports/CAMPAIGN-002-r1-ledger.md`, `harness/reports/CAMPAIGN-002-r1-worker.md`
- Prior accepted review: `harness/evaluations/CAMPAIGN-001-r5-review.md`
- Commit policy: scoped local commits required; no push, PR, release, deployment, credential, or Goose installation mutation

## Current risks

1. V0.5 live provider/Goose decision-form UX has not yet been exercised; Q-007 remains `pending_live_validation`.
2. The accepted implementation and Foreman-owned Campaign assets have not yet been pushed through the protected-branch workflow.
3. Q-003 remains partial because one V0.4 Goose interactive run does not establish both Desktop and CLI behavior.

## Next step

After user authorization, commit the Foreman-owned acceptance assets and push the accepted V0.5 history through the repository's protected-branch workflow. Then run a pinned-commit live Goose interaction test and review its evidence before marking Q-007 or the V0.5 release complete.
