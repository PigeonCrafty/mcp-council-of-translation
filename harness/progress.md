# Council of Translation Harness Progress

## Control

- Role: FOREMAN
- Mode: STRICT_CAMPAIGN
- Campaign: `CAMPAIGN-001-r5`
- Campaign state: `ACCEPTED / LIVE_VALIDATION_PENDING`
- Source baseline: `34d41946717f1993b8954260afc893737198a3bb`
- Last updated: 2026-08-12 Asia/Shanghai
- Completion authority: Foreman only

## Accepted state

- V0.3.0 remains the published remote baseline.
- The cumulative V0.4.0 implementation is locally accepted at `3267259d335b87424bc2d24adb08f94697c484ec`; `origin/main` remains unchanged and local `main` is eight commits ahead.
- Foreman baseline syntax check on 2026-08-11: `python -m compileall src tests` passed with exit code 0.
- The DeepSeek reasoning-first MCP sampling issue was fixed in the user's Goose installation and published separately to `aaif-goose/goose#11092`; that external Goose patch is not part of this repository Campaign.
- All ten V0.4 feature items and local automated quality gates Q-001, Q-002, Q-004, Q-005, and Q-006 are accepted by the Foreman.
- Campaign r1 was independently reviewed at short commit `8a2531e` and received `CHANGES_REQUESTED`; accepted package evidence is preserved in `harness/evaluations/CAMPAIGN-001-r1-review.md` but no overall V0.4 acceptance has been issued.
- The r2 correction attempt made no implementation changes and closed as `CHANGES_REQUESTED` because the Foreman supplied a nonexistent expanded SHA. The verified full candidate baseline is `8a2531e91a42a1523e83d374b84553907a5e3e94`.
- Campaign r3 repaired the option/form/discussion/policy-output/metadata paths at `d9eca22`, but Foreman review found two remaining untrusted-model gaps: duplicate same-role Positions multiply influence, and total reviewer sampling failure is misreported as a clean publishable review. r3 therefore closed as `CHANGES_REQUESTED`; passing evidence is preserved in `harness/evaluations/CAMPAIGN-001-r3-review.md`.
- Campaign r4 at `6978c7b` repaired both r3 defects and passed all 99 tests, but independent Foreman probes found that syntactically valid malformed reviewer envelopes (`{}`, non-list `findings`, invalid finding values) are still counted as full clean coverage or can raise an uncaught validation exception. r4 therefore closed as `CHANGES_REQUESTED`; its passing evidence is preserved in `harness/evaluations/CAMPAIGN-001-r4-review.md`.
- Campaign r5 at `3267259` closed the semantic reviewer-envelope gap. Foreman independently inspected all six changed paths, reran 117 tests, verified the malformed/mixed/clean Core matrix, and accepted r5. No further code correction revision is active.

## Protected baseline changes

The Main Worker must preserve and must not stage, edit, delete, move, or commit:

- `mcp-council-of-translation-audit-and-upgrade-recommendations.md`
- `reviews/`
- `.learnings/`
- Foreman-owned `harness/plan.md`, `harness/features.json`, `harness/progress.md`, and issued contracts

The Main Worker may create only the ledger and report paths authorized by the active contract under `harness/reports/`.

## Frozen decisions

- Goose-first execution target.
- Review-only boundary remains mandatory.
- Default interaction mode is `auto`.
- User choice is decisive among valid options.
- No literal majority voting; no-response fallback is constraint-aware Position Matrix adjudication.
- Maximum three DecisionPoints in one elicitation form.
- Full history is the default, but default tool output is a compact chief-editor summary.
- `continue_review` is the only new public MCP tool.
- Value takes priority over exact V0.3 response compatibility; V1 records remain readable.
- Custom MCP UI is outside V0.4.

## Active assignment

- Contract: none; `harness/contracts/CAMPAIGN-001-r5.md` is accepted
- Worker role: none
- Accepted Worker report: `harness/reports/CAMPAIGN-001-r5-worker.md`
- Prior execution ledger: `harness/reports/CAMPAIGN-001-r1-ledger.md`
- Foreman reviews: `harness/evaluations/CAMPAIGN-001-r1-review.md`, `harness/evaluations/CAMPAIGN-001-r2-review.md`, `harness/evaluations/CAMPAIGN-001-r3-review.md`, `harness/evaluations/CAMPAIGN-001-r4-review.md`, `harness/evaluations/CAMPAIGN-001-r5-review.md`

## Current risks

1. Live Goose/provider behavior for the accepted V0.4 flow remains unverified; Q-003 is pending.
2. The accepted commit is local and unpushed, so the remote git-pinned `uvx` command cannot consume it yet.
3. Host uv cache and default pytest temp roots retain access defects; the existing `.venv` runs the complete 117-test suite successfully.

## Next step

No r6 implementation assignment is required. When the user authorizes it, push the accepted commit, run Goose against the exact pinned SHA, and record Q-003 evidence before claiming release-level completion.
