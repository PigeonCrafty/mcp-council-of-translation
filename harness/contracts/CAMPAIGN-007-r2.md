# Campaign Contract: CAMPAIGN-007-r2

## Control

- Role: WORKER / MAIN WORKER
- Mode: STRICT_CAMPAIGN
- State: ASSIGNED
- Repository: `C:\Users\GeZhu\MyMCP\mcp-council-of-translation`
- Baseline commit: `61252ae27823467d74c38efaa59aa1521b006752`
- Baseline subject: `Release bounded parallel Council V0.9`
- Supersedes for execution: `CAMPAIGN-007-r1`
- Required report: `harness/reports/CAMPAIGN-007-r2-worker.md`
- New ledger: not required; preserve the r1 ledger unchanged
- Commit policy: exactly one scoped local commit; no push, PR, release or deployment
- Subagents: forbidden
- Acceptance authority: Foreman only

## Bounded correction outcome

Complete the already implemented V2.3 telemetry contract by finalizing truthful
wall-clock duration for every record-producing Core path and preserving the originating
independent-review concurrency provenance in continuation children. Do not redesign or
expand the accepted r1 bounded-concurrency implementation.

Read completely before editing: `AGENTS.md`, `harness/plan.md`,
`harness/features.json`, `harness/progress.md`, this contract,
`harness/contracts/CAMPAIGN-007-r1.md`,
`harness/evaluations/CAMPAIGN-007-r1-review.md`,
`harness/reports/CAMPAIGN-007-r1-worker.md`, and
`harness/reports/CAMPAIGN-007-r1-ledger.md`.

## Accepted r1 evidence to preserve

- Bounded correlated batch, configuration truth table and exact-once calls.
- Independent-review-only concurrency, limit/peak/batch telemetry and deterministic
  role ordering.
- Upfront budget reservation, sibling failure isolation, outer cancellation and no
  replay.
- Exact deep 13-call path, role coverage/status behavior, context/outcome ordering,
  Policy Gate, review-only and concise presentation.
- V1/V2.0/V2.1/V2.2 compatibility, V2.3 full/metadata/off persistence privacy.
- Package/module `0.9.0`, build `bounded-parallel-council-v7`, schema `2.3`, exact five
  tools, budgets 6/13/18 and artifact/install behavior.

## Required correction

1. Start a wall-clock timer in `continue_structured_review()` before continuation work.
   Finalize the child record's `wall_clock_ms` after all in-memory phase trace, digest,
   display and record construction, immediately before the single persistence save.
2. For both normal new reviews and the required-briefing early-return path, finalize
   `wall_clock_ms` at the same late boundary and update the record's runtime snapshot
   before save. Persistence I/O itself need not be included; do not add a second write.
3. A continuation child retains its parent's `independent_reviews` and coverage, so copy
   these four parent provenance fields into the child's runtime metadata:
   independent-review concurrency limit, peak, batch count and disposition. Continue to
   report the child's own sampling, elicitation, accumulated wait and wall duration under
   existing continuation semantics.
4. Remove the unmodeled dynamic assignment
   `telemetry.independent_review_wall_clock_ms`; r2 does not authorize a new field.
5. Add deterministic delayed tests showing nonzero and bounded `wall_clock_ms` for:
   normal new review, required-briefing early return, and continuation with sampling.
   Assert continuation provenance equals the parent and the child remains schema 2.3.
6. Do not change concurrency scheduling, environment semantics, retry behavior, schema,
   public diagnostics, versions, tools, budgets, roles, prompts, decisions, presentation,
   persistence policy or documentation.

## Allowed paths

- `src/council_of_translation/localization/orchestration.py`
- `tests/integration/test_parallel_orchestration.py`
- `tests/integration/test_orchestration_v2.py`
- `tests/integration/test_v22_briefing.py`
- required `harness/reports/CAMPAIGN-007-r2-worker.md`

Every other production, test, package, documentation, dependency, Harness and user path
is forbidden. Do not stage or commit any report or protected asset.

## Admission and protected assets

Before editing, verify exact HEAD/subject, empty index, declared dirty set, contract hash
and all hashes below. Run compile and the full suite; expect exactly `244 passed`. Stop
`BLOCKED` on unexplained drift.

| Protected asset | SHA-256 |
| --- | --- |
| `harness/plan.md` | `EFE9E14272605B9CADE534383E6CB04E4B0D4194F77B401B0A3F933CC3E0F5BB` |
| `harness/features.json` | `92CC65FFE0A799C4A4525BDADA733CAE6A11599C863E7F016F344820D808FF18` |
| `harness/progress.md` | `C7BF8EE19EA85E85D5C3CD375B2C818BA5A44F06AA660E353576C550B8DA4B69` |
| `harness/contracts/CAMPAIGN-007-r1.md` | `A796CFF155AFC1BA0FDECBF5A33FFEA718D98F63F4C33FF335F931ABA8188F7A` |
| `harness/reports/CAMPAIGN-007-r1-ledger.md` | `BFA401751BD6B61CAE75DF12D905057B64866D91C6F529ED987C923699E51FF9` |
| `harness/reports/CAMPAIGN-007-r1-worker.md` | `EFA4B4853D57AC5EDE3F163C6C6C7BA06538C7DD5F322D2B93CF3C35E1AEF920` |
| `harness/evaluations/CAMPAIGN-007-r1-review.md` | `09CD71C517145213B5E811B393783A9CE86D8EB2920828F77D1E719C17023DF3` |
| `harness/evaluations/CAMPAIGN-006-q010-r2-live-review.md` | `601A1162FD02A578EAA86CE7E92A2F2DC3C9C88AC0B428976BEE63310ACCD8A3` |
| `.learnings/LEARNINGS.md` | `52DC1BA8043481911C0DEABB3AC882504D9CBE8BB63D60F391C188586A230DF0` |
| `.learnings/ERRORS.md` | `F99EB75886781958BF5AE6DCF844FD476CBCA45937896A25EE3B2E9D6CD34F0A` |
| audit Markdown | `B48073E063C4C9F34E0B6B4DAE94E80079EAAAD3B2F8E273DD60B2F25F6ABD76` |

## Acceptance criteria

1. A delayed normal review persists schema 2.3 with `wall_clock_ms` covering in-memory
   finalization and no regression to accumulated `elapsed_ms`/`sampling_wait_ms`.
2. A delayed required-briefing early return persists a truthful nonzero wall time, zero
   sampling calls and unchanged pending/human-review behavior.
3. A delayed continuation child with one or more sampling calls persists nonzero wall and
   sampling-wait values, retains its own call totals, and copies the parent's four
   independent-review concurrency provenance fields instead of `legacy` defaults.
4. No path performs a second save or claims persistence duration; parent records remain
   immutable and child linkage/status/digest/display remain correct.
5. The dead dynamic batch-wall assignment is absent. No new schema or public field is
   introduced.
6. r1 focused concurrency/config/order/failure/budget/context/presentation/persistence/
   tool/version checks and the complete suite remain green.
7. Fresh 0.9.0 wheel/sdist and an isolated current-FastMCP smoke exercise one new review
   and one continuation, verifying truthful wall/provenance plus exact five tools.
8. Exact allowed scope, protected hashes, `git diff --check`, dead-import scan and empty
   index pass.

## Required verification

- Add and run the three delayed telemetry counterexamples.
- Run r1 runtime concurrency, parallel orchestration, continuation, briefing,
  persistence/privacy, dual-channel, tool-surface, V0.8 semantic and presentation suites.
- Run `.venv\Scripts\python.exe -m compileall -q src tests` and the full suite with
  disabled pytest cache and repository-local basetemp.
- Build fresh wheel/sdist and run an isolated installed-wheel smoke through current
  FastMCP for review, continuation, view, list and diagnostics. Verify import from the
  isolated environment.
- Run `git diff --check 61252ae27823467d74c38efaa59aa1521b006752..HEAD`, exact
  allowed-path audit, protected-hash audit, dead-import scan and empty-index check.
- No live Goose/provider/model calls. No push, PR, release, deployment or Goose change.

## Stop conditions and handoff

Stop `BLOCKED` if correction requires a schema/public-field change, second persistence
write, scheduler/provider change, unauthorized path, live/external action or cannot
preserve r1 evidence.

Write `harness/reports/CAMPAIGN-007-r2-worker.md`. Start the conversational handoff with
exactly `READY_FOR_REVIEW` or `BLOCKED`, then report contract hash, baseline/final HEAD,
the one commit and exact paths, before/after counterexamples, focused/full/build/wheel
results, preserved r1 invariants, hashes/index/worktree, subagent/authority/external/live
counts and remaining risks. Do not push or claim Campaign acceptance, publication,
Q-011 acceptance or project completion.
