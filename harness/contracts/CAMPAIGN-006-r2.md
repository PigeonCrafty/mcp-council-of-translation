# Campaign Contract: CAMPAIGN-006-r2

## Control

- Role: MAIN WORKER
- Mode: STRICT_CAMPAIGN
- State: ASSIGNED
- Repository: `C:\Users\GeZhu\MyMCP\mcp-council-of-translation`
- Baseline commit: `403310ccdfcbb026bd2b375517d14dc927286604`
- Baseline subject: `Plan context-coherent Council V0.8`
- Product target: `0.8.0`
- Diagnostic build target: `context-coherent-council-v6`
- Required report: `harness/reports/CAMPAIGN-006-r2-worker.md`
- Required ledger: `harness/reports/CAMPAIGN-006-r2-ledger.md`
- Commit policy: three to five scoped local commits; no push, PR, release, deployment or branch-protection change
- Worktree: shared; Main Worker owns every authorized production path
- Subagents: forbidden because guided selection, orchestration, role routing and digest behavior are tightly coupled
- Acceptance authority: Foreman only

## Supersession and incorporated specification

This contract supersedes `CAMPAIGN-006-r1` for execution. PR #10 published the r1
Foreman assets and advanced protected `main`, so the r1 baseline is no longer the exact
shared-worktree HEAD. This is an administrative baseline correction, not a product
redesign.

Read `AGENTS.md`, `harness/plan.md`, `harness/features.json`,
`harness/progress.md`, this contract, `harness/contracts/CAMPAIGN-006-r1.md`,
`harness/evaluations/CAMPAIGN-005-q009-live-review.md` and
`harness/evaluations/CAMPAIGN-005-r1-review.md` completely before editing.

All frozen design, discretion, reserved decisions, allowed and forbidden paths,
authorized actions, package graph PKG-032 through PKG-036, acceptance criteria,
verification requirements and stop conditions in the exact r1 contract identified below
are incorporated into r2 unchanged. The only controlling substitutions are:

1. baseline and baseline subject are the r2 Control values above;
2. the required ledger/report use the r2 paths above;
3. every r1 verification command that compares from the old baseline compares from
   `403310ccdfcbb026bd2b375517d14dc927286604` instead;
4. r1 is immutable Foreman history and must not be executed, edited, staged or committed.

If r1 and r2 conflict on any of those four administrative fields, r2 controls. Otherwise
r1 controls. No production, test, documentation, package, dependency, schema, tool,
budget, role, interaction, persistence or acceptance requirement is relaxed.

## Frozen outcome summary

Deliver Council of Translation V0.8 as a context-first, relevant panoramic review:

- Standard and strict marketing use, in relative order, exactly the six relevant lenses
  `fidelity_reviewer`, `terminology_reviewer`, `product_context_reviewer`,
  `brand_voice_reviewer`, `risk_ambiguity_reviewer`, and `fluency_reviewer`.
- Brand-slogan-versus-functional-UI, binding glossary/reference, and meaning/routing/
  option/release-changing questions are deterministically eligible material context.
  Generic curiosity, unrelated trivia, duplicates and plainly answered questions remain
  bounded and suppressible.
- Selected material context is handled before discussion, DecisionPoint creation and
  outcome elicitation. Actual answers update the effective brief and reconsider only
  affected active roles within the existing cap.
- Assumption, decline, cancel, unsupported, malformed or error leaves material context
  unresolved, opens no outcome form, accepts no outcome, lowers confidence as needed,
  preserves the required confirmation, and returns conservative human-review status.
- Suppressed questions are not presented as user decisions. Primary text maps raw issue
  labels such as `ux`, removes doubled punctuation, preserves material evidence and
  conditions, keeps the verdict last, and remains within 3,200 code points.
- Raw V2.2 records remain the only telemetry truth; current role IDs, sample-status/
  coverage literals and executed call counts receive deterministic invariant tests.
- Package/module become `0.8.0`; build becomes `context-coherent-council-v6`; schema stays
  `2.2`; the exact five tools, review-only/default interaction behavior, compatibility,
  privacy, and budgets `6/13/18` remain.

The five sequential packages remain PKG-032 classification, PKG-033 context precedence
and conservative status, PKG-034 six-role marketing routing, PKG-035 presentation and
record invariants, and PKG-036 version/package/docs migration. Expected admission is
exactly `203 passed` plus successful compile.

## Admission gate

Before any edit:

1. verify exact HEAD and subject from Control;
2. verify the Git index is empty and only the declared Foreman/user dirt is present;
3. hash this contract, verify the incorporated r1 hash and every protected hash below;
4. run `python -m compileall -q src tests`;
5. run the full suite with repository-local basetemp and cache disabled; expect exactly
   `203 passed`;
6. reproduce the r1 deterministic counterexamples: three-role standard marketing,
   material brand/UI and glossary questions suppressed as `immaterial_gap`, unresolved
   context followed by outcome/clean publication, and raw presentation artifacts.

Stop `BLOCKED` on unexplained drift. Do not repair, stage, rewrite, delete, move or
commit protected assets.

| Protected asset | SHA-256 |
| --- | --- |
| `harness/plan.md` | `72F0367FE40AF040CBA613397EFF2823DF5AB621D2EE7A73B4382825EA51C8C7` |
| `harness/features.json` | `CFD4CF22032336B2DCCC27F5AB4BD6E2A4FD45351B4C8EE662209B44EAACC8B0` |
| `harness/progress.md` | `9DC1784899273F2DB05F79E87B6DBA3CF7ACA9B17D3C4923792430279069B010` |
| `harness/contracts/CAMPAIGN-006-r1.md` | `29580DBB99603BE6CFA04D62707074290076717850602E1825881AA4B889AA3F` |
| `harness/evaluations/CAMPAIGN-005-q009-live-review.md` | `99725BA7913EA7B8A75A1D1E9A2B52C152238BF1F582C644BE27DE970E06E54A` |
| `harness/evaluations/CAMPAIGN-005-r1-review.md` | `6DC51DA5B7955289D407BB53194F7EA100736BD324B087EBDAF89C64F86AD41C` |
| `harness/contracts/CAMPAIGN-005-r1.md` | `F47CC137CD6DF31C28E39519CCCF78DB3609C5D0EB3E71686AA1F62E27035E02` |
| `harness/reports/CAMPAIGN-005-r1-worker.md` | `41A7C37C3C71C9F2A066723635CB9836A77E544546FCCEB8E1E8296C35D40A93` |
| `.learnings/LEARNINGS.md` | `22F939E6F980DF52487AAFE97EDCA9B90CF3931DDB7A31BF8A5BBB8F052E658F` |
| `.learnings/ERRORS.md` | `F99EB75886781958BF5AE6DCF844FD476CBCA45937896A25EE3B2E9D6CD34F0A` |
| audit Markdown | `B48073E063C4C9F34E0B6B4DAE94E80079EAAAD3B2F8E273DD60B2F25F6ABD76` |

Preserve `.learnings/**`, `reviews/**`, the audit Markdown, every prior Harness artifact
and `myTest/**` if it appears. Only the r2 ledger/report may be created under Harness.

## Required verification and handoff

Execute every r1 package and acceptance check with the corrected baseline. In particular,
prove exact marketing role order, material-gap selection variants, all resolved and
unresolved interaction actions, zero outcome requests when unresolved, deep 13-call
budget behavior, clean/disputed/degraded/pending/adversarial rendering, literal V2.2
record invariants, exact five tools, versions/defaults/budgets, full suite, compile,
scope/diff/protected hashes, fresh artifacts and isolated current-FastMCP wheel calls.

Use `git diff --check 403310ccdfcbb026bd2b375517d14dc927286604..HEAD`
and audit every changed path against the r1 allowed-path list. Reuse the accepted FastMCP
2.13 dual-channel evidence as authorized by r1; do not claim live provider behavior.

Maintain `harness/reports/CAMPAIGN-006-r2-ledger.md` throughout execution and write
`harness/reports/CAMPAIGN-006-r2-worker.md`. Start the conversational handoff with exactly
`READY_FOR_REVIEW` or `BLOCKED`, then report contract hash, baseline/final HEAD,
package/commit/file mapping, before/after counterexamples, focused/full/build/wheel
results, protected hashes, index/worktree state, subagent/authority/live-call counts,
retries/deviations and remaining risks. Do not push or claim Campaign acceptance or
project completion.
