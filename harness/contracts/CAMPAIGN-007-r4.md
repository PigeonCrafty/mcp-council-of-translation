# Campaign Contract: CAMPAIGN-007-r4

## Control

- Role: WORKER / MAIN WORKER
- Mode: STRICT_CAMPAIGN
- State: ASSIGNED
- Repository: `C:\Users\GeZhu\MyMCP\mcp-council-of-translation`
- Baseline commit: `11fb742cda602d33cb66550d0f3d665234bd4193`
- Baseline subject: `Accept bounded parallel Council V0.9`
- Corrects: `CAMPAIGN-007-r3`
- Required report: `harness/reports/CAMPAIGN-007-r4-worker.md`
- New ledger: not required
- Commit policy: exactly one lockfile-only local commit; no push, PR, release or deployment
- Subagents: forbidden
- Acceptance authority: Foreman only

## Bounded outcome

Finish the V0.9 lock correction with the exact uv version used by CI. Normalize the
known uncommitted r3 intermediate lock and commit only the expected editable-root version
change. Do not change source, tests, dependencies, workflows, documentation, Harness
state or user assets.

Read completely before acting: `AGENTS.md`, `harness/plan.md`,
`harness/features.json`, `harness/progress.md`, this contract, the r3 contract/report/
review, `harness/evaluations/CAMPAIGN-007-publication-ci-review.md`, and the accepted r1/
r2 contracts, reports and reviews.

## Admitted intermediate state

HEAD and index remain at the exact baseline with zero r3 commits. `uv.lock` is an
intentional unstaged r3 intermediate produced by ambient uv 0.6.13:

- SHA-256: `94409C5B068B84B029A15F183C3BF028DE4C19E6DF65D3E6B4781F0BA93B442E`
- diff: 596 insertions / 596 deletions
- header revision 1, no upload-time entries, root package already 0.9.0

Do not treat this exact declared intermediate as unexplained drift. Any other `uv.lock`
content or hash is a stop condition.

## Required correction and pinned toolchain

1. Set both `UV_CACHE_DIR` and `UV_TOOL_DIR` to dedicated directories under repository
   `.tmp/`; do not use either global user directory.
2. Bootstrap and invoke the actual lock generator only as
   `uv tool run --from uv==0.12.3 uv ...`. Capture `uv --version` from that invocation
   and require exact version `0.12.3` before regeneration.
3. Run its canonical `uv lock` against the repository. This is authorized to overwrite
   the admitted r3 intermediate `uv.lock`.
4. Inspect baseline-to-worktree diff before further action. It must be exactly one line:
   the root editable `council-of-translation` version `0.8.0` to `0.9.0`. Header must
   remain revision 3; all 586 upload-time entries, 78 packages, dependencies, resolved
   versions, sources, hashes and lock format must match the baseline.
5. Stop `BLOCKED` without staging if any other baseline-to-worktree difference remains.
6. Run lock check, locked sync, compile and full tests with the same pinned uv 0.12.3,
   then create exactly one commit containing only `uv.lock`.

## Allowed paths

- `uv.lock`
- required uncommitted `harness/reports/CAMPAIGN-007-r4-worker.md`

Every other path is forbidden. Stage and commit only `uv.lock`. Preserve and do not
stage the r3/r4 contracts, reports, Foreman evaluations/state, `.learnings/**`,
`reviews/**`, the audit Markdown or any other pre-existing asset.

## Protected assets

| Protected asset | SHA-256 |
| --- | --- |
| `harness/plan.md` | `B4D88434D189874CD119694AF2783AC7FAF75E9E640BCC9D674D71027588B120` |
| `harness/features.json` | `8345870B42EAADF7590A8C741864AF4264CA9B2BB2DFCFA8E47CFEDFC5BA2881` |
| `harness/progress.md` | `96613C30FC527A13D8C2F883F438F954473D71254B15AB63D9D8DC491CF1EFDB` |
| `harness/evaluations/CAMPAIGN-007-publication-ci-review.md` | `71C1C01047D7D979AA9417EC429D422664318843BF7862BA988B0B30562A85BA` |
| `harness/contracts/CAMPAIGN-007-r1.md` | `A796CFF155AFC1BA0FDECBF5A33FFEA718D98F63F4C33FF335F931ABA8188F7A` |
| `harness/contracts/CAMPAIGN-007-r2.md` | `612CC6F9C42B93956A1CCB4EC8ACE1B634F42AFE674B9EB48105CD76772D888D` |
| `harness/contracts/CAMPAIGN-007-r3.md` | `FF1EF1903B4B430CC984BEB685BFCE9AF1CB375B8E7800D3BA99C913ADC680A6` |
| `harness/reports/CAMPAIGN-007-r1-ledger.md` | `BFA401751BD6B61CAE75DF12D905057B64866D91C6F529ED987C923699E51FF9` |
| `harness/reports/CAMPAIGN-007-r1-worker.md` | `EFA4B4853D57AC5EDE3F163C6C6C7BA06538C7DD5F322D2B93CF3C35E1AEF920` |
| `harness/reports/CAMPAIGN-007-r2-worker.md` | `9DA0A982FC041797A2277B015C1A27C78457AC9042BEB9DA313E9F4E050D9E9C` |
| `harness/reports/CAMPAIGN-007-r3-worker.md` | `6B68558210075A01CA97E3E3782188EE2BD65727D5BAC999A71F36C499F23635` |
| `harness/evaluations/CAMPAIGN-007-r1-review.md` | `09CD71C517145213B5E811B393783A9CE86D8EB2920828F77D1E719C17023DF3` |
| `harness/evaluations/CAMPAIGN-007-r2-review.md` | `99E1ACDAFCA5CED0EFF9A316865DFBCE11E589885B2DBBEE210F2FAEBB20E61B` |
| `harness/evaluations/CAMPAIGN-007-r3-review.md` | `1460EED3DE0B7F196EB0A231B839CBF7D271C64033D583E075D7808E398A6200` |
| `.learnings/LEARNINGS.md` | `52DC1BA8043481911C0DEABB3AC882504D9CBE8BB63D60F391C188586A230DF0` |
| `.learnings/ERRORS.md` | `F99EB75886781958BF5AE6DCF844FD476CBCA45937896A25EE3B2E9D6CD34F0A` |
| audit Markdown | `B48073E063C4C9F34E0B6B4DAE94E80079EAAAD3B2F8E273DD60B2F25F6ABD76` |

## Acceptance criteria and verification

1. Pinned-generator output reports uv 0.12.3.
2. Baseline-to-final `uv.lock` diff is exactly one insertion and one deletion at the
   editable root version; revision 3, 586 upload-time entries and 78 package entries
   remain.
3. With the same local directories and pinned generator:
   `uv lock --check` and `uv sync --locked --group dev` pass.
4. Run `uv run --frozen python -m compileall -q src tests` and
   `uv run --frozen pytest -q` with the pinned generator. Expected full result:
   `246 passed`.
5. Package/module remain 0.9.0, diagnostic build remains
   `bounded-parallel-council-v7`, schema remains 2.3, exact five tools and budgets
   6/13/18 remain unchanged.
6. Exactly one new commit and one committed path. Baseline-to-HEAD `git diff --check`,
   name/status, textual diff, protected hashes and empty index pass.
7. No fresh artifact or live Goose/provider test is required. Record the one local
   pinned-uv download/install as an external dependency operation, not a live model call.

## Stop conditions and handoff

Stop `BLOCKED` on tool version mismatch, any final lock difference beyond the root
version, unauthorized path, protected hash/baseline drift, test failure or need for
production/workflow/dependency changes.

Write `harness/reports/CAMPAIGN-007-r4-worker.md`. Start the conversational handoff with
exactly `READY_FOR_REVIEW` or `BLOCKED`, then report contract hash, baseline/final HEAD,
commit/path/diff, pinned uv evidence, lock invariants, locked sync, compile/full suite,
package/tool invariants, protected hashes/index/worktree, and authority/external/live
counts. Do not push, update PR #15 or claim publication/Q-011/project completion.
