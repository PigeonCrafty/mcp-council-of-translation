# Campaign Contract: CAMPAIGN-011-r3

## Control

- Harness role: `MAIN WORKER`
- Harness mode: `STRICT_CAMPAIGN`
- Campaign: `CAMPAIGN-011-r3`
- Baseline: `938c3a4bb9f14c7688286b25eabd8aff9f18a09d`
- Parent live review: `harness/evaluations/CAMPAIGN-011-q013-live-review.md`
- Parent decision: `CHANGES_REQUESTED`
- Product target: `0.11.1`
- Diagnostic build target: `risk-coherent-council-v9.1`
- Schema: frozen at `2.5`
- Acceptance authority: Foreman only

## Objective

Correct the V0.11 primary/structured disposition divergence exposed by Q-013 Case A.
The primary action projection may remain bounded, but it must never discard or replace
the canonical chief final disposition merely because more than six action lines precede
it. Deliver a narrowly scoped V0.11.1 patch without changing Council decisions, routing,
sampling, evidence or public tools.

## Admitted state and evidence boundary

Start only if `HEAD` is exactly the baseline above and the Git index is empty. The
worktree contains Foreman/user-owned modified, untracked and ignored evidence assets.
Record their admission hashes and preserve them byte-for-byte. In particular:

- do not modify `harness/plan.md`, `harness/progress.md`, `harness/features.json`, any
  existing contract, evaluation, report or ledger;
- do not read, copy, stage or modify `.tmp/q012/**`, `reviews/**`, `.learnings/**` or the
  user audit report;
- do not treat Goose narrative prose or raw live model prose as a test fixture;
- the Worker may read the parent live review, which contains the bounded counterexample
  and authoritative hashes without raw record content.

If the baseline, index or protected assets do not match admission, stop and report
`BLOCKED` before editing.

## Frozen design

- Exact five tools and all public signatures remain unchanged.
- Defaults remain `review_only`, interactive `auto`, briefing `auto`, trace `summary`,
  history `full` and Council adjudication fallback.
- Budgets remain `6/13/18`; concurrency remains bounded at `1..3`, default/max `3`.
- All 15 routing profiles and legal-risk 4/6/7 role portfolios remain unchanged.
- Schema remains `2.5`; old-record readability remains unchanged.
- Structured chief decisions, Policy Gate results, issue clusters, value metrics and
  persisted evidence must not be mutated to match presentation.
- Primary output remains exactly five sections, chief disposition last, clean target
  1,200 Unicode code points and hard cap 3,200.
- `review_only` must not emit a full replacement translation.

## Work packages

### PKG-063 — terminal disposition preservation

Observable result: `_primary_checklist` or its direct caller bounds actionable work while
preserving the canonical `最终处置：...；需人工复核：...` entry exactly once and last.

Authorized paths:

- `src/council_of_translation/localization/digest.py`
- `tests/integration/test_v24_presentation.py`
- `tests/integration/test_v101_live_shaped_value.py`
- `tests/integration/test_v25_risk_routing.py`

Required counterexamples:

1. A legal-risk-shaped digest with more than six pre-final action entries and chief
   `修改后可发布 / 否` renders that exact final disposition, not the human-review fallback.
2. A true human-review case with more than six entries remains `需人工复核 / 是`.
3. A clean publishable case remains unchanged.
4. Pending/degraded warnings remain visible and never turn into release permission.
5. Final disposition appears exactly once, is the last report line and survives the
   3,200-code-point bounding path.
6. Structured digest, chief, clusters and metrics remain byte-equivalent before/after
   rendering; rendering adds zero sampling and elicitation.

Do not solve this by raising the global six-line cap until the final happens to fit, by
hard-coding Case A prose, by inferring a new verdict from severity, or by mutating the
structured chief.

### PKG-064 — V0.11.1 release migration

After PKG-063 passes, migrate only release identifiers to package/module `0.11.1` and
diagnostic build `risk-coherent-council-v9.1`. Schema and behavior outside the correction
remain frozen.

Additional authorized paths:

- `AGENTS.md`
- `README.md`
- `docs/v0.4-architecture.md`
- `docs/v0.4-tool-contract.md`
- `pyproject.toml`
- `uv.lock`
- `src/council_of_translation/__init__.py`
- `src/council_of_translation/tools/review.py`
- `tests/integration/test_tool_surface_v2.py`
- `tests/integration/test_v08_presentation_invariants.py`
- `tests/integration/test_v10_release_contract.py`
- `tests/unit/test_persistence_v2.py`

Use the repository's pinned uv version and canonical lock workflow. The final `uv.lock`
diff must change only the editable root version `0.11.0 -> 0.11.1`; retain revision 3,
package count and upload-time metadata. Stop rather than manually rewriting lock content
or accepting unrelated format drift.

## Verification

Run and report at minimum:

1. admission compile and complete test count at the exact baseline;
2. focused PKG-063 counterexamples, including long-list and 3,200-boundary cases;
3. affected presentation, routing, persistence, tool-surface and release suites;
4. exact 24/24 Golden corpus with all eight aggregate metrics at 1.0;
5. final `python -m compileall src tests` and complete test suite;
6. exact five tools, version/build/schema, defaults, budgets and concurrency probes;
7. `git diff --check`, exact authorized-path audit, dead-import scan and empty index;
8. fresh sdist/wheel build and archive inspection;
9. isolated Python 3.12/FastMCP 3.4.7 wheel-origin smoke calling all five tools and
   checking dual-channel output plus the long-checklist terminal disposition.

Use a repository-local cache/basetemp if the known host uv/pytest permission defect
appears. Record the original failure and bounded rerun; do not hide either.

## Commits and handoff

- Create exactly two scoped local commits, one per package, after that package passes.
- Do not push, open/update a PR, publish, release, deploy, modify Goose/provider settings
  or make live model calls.
- Do not claim Campaign or Q-013 acceptance.
- Write `harness/reports/CAMPAIGN-011-r3-ledger.md` and
  `harness/reports/CAMPAIGN-011-r3-worker.md`; leave both untracked and unstaged.
- The final report must state baseline/final HEAD, commits, exact paths, test/build/smoke
  evidence, lock invariants, protected hashes, skipped checks, subagents, authority and
  external/live-call counts, and remaining risks.

Stop with `BLOCKED` if the correction requires changes outside the authorized paths,
changes structured adjudication rather than presentation, causes extra sampling or
elicitation, cannot preserve the terminal disposition under the hard cap, or produces
unrelated lock drift.
