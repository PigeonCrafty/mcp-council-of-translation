# Campaign Contract: CAMPAIGN-007-r6

## Control

- Role: WORKER / MAIN WORKER
- Mode: STRICT_CAMPAIGN
- State: ASSIGNED
- Repository: `C:\Users\GeZhu\MyMCP\mcp-council-of-translation`
- Baseline commit: `116f2297c035c006bbd0419e802691ec5f30c0c8`
- Baseline subject: `Accept V0.9 lock publication fix`
- Corrects: PR #15 CI round 2 timing-test failure
- Required report: `harness/reports/CAMPAIGN-007-r6-worker.md`
- New ledger: not required
- Commit policy: exactly one test-only local commit; no push, PR, release or deployment
- Subagents: forbidden
- Acceptance authority: Foreman only

## Bounded outcome

Remove the Windows scheduler assumption from the continuation timing regression test
without weakening its zero-wall protection or changing any production behavior.

Read completely before acting: `AGENTS.md`, `harness/plan.md`,
`harness/features.json`, `harness/progress.md`, this contract,
`harness/evaluations/CAMPAIGN-007-publication-ci-r2-review.md`, and the r2/r5 contracts,
reports and Foreman reviews.

## Required test correction

In `tests/integration/test_orchestration_v2.py` only:

1. Make `DelayedContinuationExecutor.sample()` measure its actual elapsed wait with
   `perf_counter` around the existing `await asyncio.sleep(0.02)` and record that bounded
   integer duration in `RuntimeEvent`, rather than fabricating constant `20`.
2. Preserve exactly one executor call and the asynchronous delay.
3. Replace the fixed assertions `sampling_wait_ms == 20` and
   `15 <= wall_clock_ms` with the semantic invariant:
   `0 < sampling_wait_ms <= wall_clock_ms < 2_000`.
4. Keep all parent immutability, child linkage, persistence, concurrency provenance,
   coverage, status and schema assertions unchanged.
5. Do not monkeypatch production clocks, loosen the upper bound, skip by platform,
   retry production operations, or change production source.

The baseline test SHA-256 is
`FB5A0F980CEE9BE5B64278EF0FD7FD89766D3C6714AB6217E27C919CBFF5601B`.

## Allowed paths

- `tests/integration/test_orchestration_v2.py`
- required uncommitted `harness/reports/CAMPAIGN-007-r6-worker.md`

Every other path is forbidden. Stage and commit only the test file. Preserve all
Foreman, user and report assets.

## Protected assets

| Protected asset | SHA-256 |
| --- | --- |
| `harness/plan.md` | `1BB454D8A42B4434B9CCF987F06D0674DE79CB986AC4D14FA8F8B617B9D50D83` |
| `harness/features.json` | `8345870B42EAADF7590A8C741864AF4264CA9B2BB2DFCFA8E47CFEDFC5BA2881` |
| `harness/progress.md` | `1FED1ABFACF278DDF49F428480EE25215E1C14AB37C0EF49E9CD3974A70CF86E` |
| r5 Foreman review | `80DBF65AA14C799F73013B9DDB17D4803F4D37B51126EDE4D3550DD019145084` |
| CI round-2 review | `CFDF297B1B7FAA869CB01E0B9C08D57BDB5182A1A883A018159DE29AFEB0CE78` |
| r5 contract | `F344D16FA84B32C275DCB55EF7D0B6769CE540CE374B6DED9F46E5E2FDE9B6C2` |
| r5 Worker report | `C2D5099C4166FE7A285F51E4B6328D8B17645D3ED0DF499D6BACD11A9E0286BF` |
| `uv.lock` | `1CED44E8A6D0F88691A83FFC5B214232CAAA6E437BA5EC8820B5EDADA5C65E9D` |
| `pyproject.toml` | `1D9E228DE87EC14CE1824911E5898E9230B6252D8DE6BDD9E17CB24FED260626` |
| `.github/workflows/ci.yml` | `0B37598E7D53D27B04E5524BAA4D46A2AB69D5E2607A5FF9F0437512CF8EF645` |
| production orchestration | `A72A6D08A4872D116ED830B4A99788194E0C8300A9F2BD697EA74E64D59FDC7B` |
| production runtime | `4AB8AF8F457033440C97784F8A7307B7477358C94B3F24EFFE3BE56ED54D85B3` |
| `.learnings/LEARNINGS.md` | `52DC1BA8043481911C0DEABB3AC882504D9CBE8BB63D60F391C188586A230DF0` |
| `.learnings/ERRORS.md` | `F99EB75886781958BF5AE6DCF844FD476CBCA45937896A25EE3B2E9D6CD34F0A` |
| audit Markdown | `B48073E063C4C9F34E0B6B4DAE94E80079EAAAD3B2F8E273DD60B2F25F6ABD76` |

## Required verification

Use CI-pinned uv 0.12.3 with repository-local `UV_CACHE_DIR` and `UV_TOOL_DIR`.

1. Confirm exact uv 0.12.3 and `uv lock --check`.
2. Synchronize the locked dev environment for Python 3.12.
3. Run the corrected named test at least twenty independent times on Windows, each with
   a unique repository-local `--basetemp`; require 20/20 pass. On another OS, run it at
   least five times and disclose the limitation.
4. Run the timing-focused files:
   `test_orchestration_v2.py`, `test_parallel_orchestration.py`, and
   `test_v22_briefing.py`.
5. Run compile and the complete suite with disabled pytest cache and repository-local
   basetemp; expect `246 passed`.
6. Verify package/module 0.9.0, build `bounded-parallel-council-v7`, schema 2.3, exact
   five tools, budgets 6/13/18 and exact lock hash.
7. Create exactly one commit containing only the authorized test file. Run baseline-to-
   HEAD scope/textual audit, `git diff --check`, protected hashes and empty-index check.

No live Goose/provider/model call, dependency upgrade, artifact build, push, PR update,
release or deployment is authorized.

## Stop conditions and handoff

Stop `BLOCKED` if the semantic relation fails, production needs modification, another
test must be weakened, the exact scope/hashes drift or any required check fails.

Write `harness/reports/CAMPAIGN-007-r6-worker.md`. Start the conversational handoff with
exactly `READY_FOR_REVIEW` or `BLOCKED`, then report contract hash, baseline/final HEAD,
commit/diff/scope, measured-duration change, repeated Python 3.12 result, focused/full
verification, public invariants, protected hashes/index/worktree and authority/external/
live counts. Do not push or claim publication, Q-011 acceptance or project completion.
