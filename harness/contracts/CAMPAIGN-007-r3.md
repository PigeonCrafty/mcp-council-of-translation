# Campaign Contract: CAMPAIGN-007-r3

## Control

- Role: WORKER / MAIN WORKER
- Mode: STRICT_CAMPAIGN
- State: ASSIGNED
- Repository: `C:\Users\GeZhu\MyMCP\mcp-council-of-translation`
- Baseline commit: `11fb742cda602d33cb66550d0f3d665234bd4193`
- Baseline subject: `Accept bounded parallel Council V0.9`
- Supersedes for execution: none; r1+r2 implementation remains accepted
- Required report: `harness/reports/CAMPAIGN-007-r3-worker.md`
- New ledger: not required
- Commit policy: exactly one lockfile-only local commit; no push, PR, release or deployment
- Subagents: forbidden
- Acceptance authority: Foreman only

## Bounded outcome

Repair the V0.9 publication admission failure by synchronizing only the root project
metadata in `uv.lock` with the already accepted `pyproject.toml`. Do not change source,
tests, dependencies, workflows, documentation, Harness state or user assets.

Read completely before acting: `AGENTS.md`, `harness/plan.md`,
`harness/features.json`, `harness/progress.md`, this contract,
`harness/evaluations/CAMPAIGN-007-publication-ci-review.md`, and the r1/r2 contracts,
reviews and Worker reports.

## Required correction

1. Confirm `pyproject.toml` declares `0.9.0` and the root editable project entry in
   `uv.lock` declares `0.8.0`.
2. Run the canonical uv lock regeneration using a repository-local uv cache.
3. Inspect the semantic and textual lock diff before staging. The only permitted lock
   graph change is the root package version `0.8.0` to `0.9.0`. Package names,
   dependency edges, resolved versions, sources, hashes and lock format must not change.
4. If regeneration changes anything else, restore no files, make no commit and report
   `BLOCKED` with the diff. Do not manually edit generated lock content to hide drift.
5. If the diff is exact, run the same locked admission used by CI, compile and the full
   suite, then create one commit containing only `uv.lock`.

## Allowed paths

- `uv.lock`
- required uncommitted `harness/reports/CAMPAIGN-007-r3-worker.md`

Every other path is forbidden. Stage and commit only `uv.lock`. Do not stage the Worker
report, this contract, Foreman evaluations/state, `.learnings/**`, `reviews/**`, the
audit Markdown or any pre-existing dirty/untracked asset.

## Admission and protected assets

Before editing, verify exact HEAD/subject, empty index, declared dirty set and this
contract's SHA-256. Confirm the stale-lock counterexample with `uv lock --check` using a
repository-local cache. Do not use the user's global uv cache.

| Protected asset | SHA-256 |
| --- | --- |
| `harness/plan.md` | `59A52E7AE73EE1AFBCCB89A8BAA4F13795FCD098F65CF1BADFB7FA5A05152DCA` |
| `harness/features.json` | `8345870B42EAADF7590A8C741864AF4264CA9B2BB2DFCFA8E47CFEDFC5BA2881` |
| `harness/progress.md` | `CB43DF547CA8D1DD1A3E510E5B8D3BF722955C917B3201B40ED09745D5B21659` |
| `harness/evaluations/CAMPAIGN-007-publication-ci-review.md` | `71C1C01047D7D979AA9417EC429D422664318843BF7862BA988B0B30562A85BA` |
| `harness/contracts/CAMPAIGN-007-r1.md` | `A796CFF155AFC1BA0FDECBF5A33FFEA718D98F63F4C33FF335F931ABA8188F7A` |
| `harness/contracts/CAMPAIGN-007-r2.md` | `612CC6F9C42B93956A1CCB4EC8ACE1B634F42AFE674B9EB48105CD76772D888D` |
| `harness/reports/CAMPAIGN-007-r1-ledger.md` | `BFA401751BD6B61CAE75DF12D905057B64866D91C6F529ED987C923699E51FF9` |
| `harness/reports/CAMPAIGN-007-r1-worker.md` | `EFA4B4853D57AC5EDE3F163C6C6C7BA06538C7DD5F322D2B93CF3C35E1AEF920` |
| `harness/reports/CAMPAIGN-007-r2-worker.md` | `9DA0A982FC041797A2277B015C1A27C78457AC9042BEB9DA313E9F4E050D9E9C` |
| `harness/evaluations/CAMPAIGN-007-r1-review.md` | `09CD71C517145213B5E811B393783A9CE86D8EB2920828F77D1E719C17023DF3` |
| `harness/evaluations/CAMPAIGN-007-r2-review.md` | `99E1ACDAFCA5CED0EFF9A316865DFBCE11E589885B2DBBEE210F2FAEBB20E61B` |
| `.learnings/LEARNINGS.md` | `52DC1BA8043481911C0DEABB3AC882504D9CBE8BB63D60F391C188586A230DF0` |
| `.learnings/ERRORS.md` | `F99EB75886781958BF5AE6DCF844FD476CBCA45937896A25EE3B2E9D6CD34F0A` |
| audit Markdown | `B48073E063C4C9F34E0B6B4DAE94E80079EAAAD3B2F8E273DD60B2F25F6ABD76` |

## Acceptance criteria

1. `git diff 11fb742cda602d33cb66550d0f3d665234bd4193..HEAD -- uv.lock`
   contains only the root editable package version change from 0.8.0 to 0.9.0.
2. `uv lock --check` passes with a repository-local cache.
3. `uv sync --locked --group dev` passes with a repository-local cache.
4. `.venv\Scripts\python.exe -m compileall -q src tests` passes.
5. The complete suite passes with disabled pytest cache and repository-local basetemp;
   expected count is `246 passed`.
6. Source/package/module remain `0.9.0`, build remains
   `bounded-parallel-council-v7`, schema remains `2.3`, exact five tools and budgets
   6/13/18 remain unchanged.
7. Exactly one commit and one committed path; `git diff --check` passes, index is empty
   and every protected hash remains exact.

## Required verification

- Capture the failing pre-change `uv lock --check` counterexample.
- Regenerate and semantically audit `uv.lock`.
- Run post-change `uv lock --check` and `uv sync --locked --group dev` with
  `UV_CACHE_DIR` inside `.tmp/`.
- Run compile and the complete suite exactly as CI-equivalent local checks.
- Inspect the baseline-to-HEAD name/status and textual diff, commit count, index,
  worktree and all protected hashes.
- No fresh artifact build is required because source/package metadata is unchanged; do
  not perform live Goose/provider/model calls or any push/PR/release/deployment action.

## Stop conditions and handoff

Stop `BLOCKED` on any dependency graph drift, unauthorized path, baseline/hash drift,
test regression, external/live requirement or need to alter anything beyond `uv.lock`.

Write `harness/reports/CAMPAIGN-007-r3-worker.md`. Start the conversational handoff with
exactly `READY_FOR_REVIEW` or `BLOCKED`, then report contract hash, baseline/final HEAD,
the one commit and exact diff, before/after lock checks, locked sync, compile/full suite,
version/tool invariants, protected hashes/index/worktree and authority/external/live
counts. Do not push or claim publication, Q-011 acceptance or project completion.
