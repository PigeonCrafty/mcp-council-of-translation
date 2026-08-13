# CAMPAIGN-007-r1 Main Worker Report

## Status and authority

- Worker outcome: `READY_FOR_REVIEW` (Foreman acceptance not claimed).
- Role/mode: `WORKER / MAIN WORKER`, `STRICT_CAMPAIGN`.
- Contract: `harness/contracts/CAMPAIGN-007-r1.md`.
- Verified contract SHA-256:
  `A796CFF155AFC1BA0FDECBF5A33FFEA718D98F63F4C33FF335F931ABA8188F7A`.
- Exact admitted baseline:
  `f9651ed64daf86dd5fabac5e7437b9de8b3186bc` (`Accept final Q-010 live evidence`).
- Final HEAD: `61252ae27823467d74c38efaa59aa1521b006752`.
- Implementation subagents: forbidden / 0 used.
- Campaign authority escalations: 0. Live Goose/provider/model calls: 0.
- No push, PR, release, deploy, credential request, or Goose modification occurred.

## Admission and boundaries

Admission passed before production edits: exact HEAD, empty index, exact contract hash,
only the declared Foreman/user dirty set, all 10 protected hashes, compile, and the exact
baseline suite result `220 passed in 2.54s`. The reproduced baseline six-role marketing
loop was sequential: peak 1, six calls, start/completion order 0..5, accumulated
`elapsed_ms=196`, observed wall about 195 ms, with no wall/concurrency/batch telemetry.

Implementation stayed within the contract's runtime, orchestration, model,
compatibility, persistence, review/server, version/package/documentation and directly
affected test paths. Protected Harness state, prior reports/evaluations, `.learnings/`,
`reviews/`, the audit Markdown and any user assets were neither staged nor committed.
Only the required r1 ledger and this report were created under `harness/reports/`.

## Package and commit matrix

| Package | Commit | Changed scope | Package verification |
| --- | --- | --- | --- |
| PKG-037 | `707b6f2fa1d4658c825e86c1d9664ba5a112bf03` | `localization/runtime.py`, `tests/unit/test_runtime_concurrency.py` | `17 passed in 0.51s` |
| PKG-038 | `eea1e09ccd490f4970988d883b70398cccbc5f9b` | `localization/orchestration.py`, `tests/integration/test_parallel_orchestration.py` | `22 passed in 1.00s`; broad integration/runtime `150 passed in 2.80s` |
| PKG-039 | `93c4510d80973c96e0e0f53412d0343c85f75e4f` | models, runtime, orchestration, compatibility, persistence and migration/integration tests | `53 passed in 1.21s`; full `236 passed in 3.07s` |
| PKG-040 | `189944c708514385e1d7a4485aa9329268c1761b` | review diagnostics plus tool/config and parallel integration tests | `45 passed in 2.13s` |
| PKG-041 | `61252ae27823467d74c38efaa59aa1521b006752` | authoritative version/build/schema constants, package/server/tools, docs and affected tests | compile pass; `61 passed in 1.95s`; full `244 passed in 3.21s` |

The baseline-to-final committed diff contains 21 authorized files with 616 insertions
and 75 deletions. `git diff --check` passed.

## Implemented behavior

- `COUNCIL_REVIEW_CONCURRENCY` is read once per new review. Missing uses `3/default`;
  only literal `1`, `2`, and `3` are configured; all other supplied values safely use
  `1/invalid_fallback`.
- A semaphore-bounded correlated batch reserves all independent-role budget before
  launch, attempts every provider request exactly once, isolates sibling exceptions,
  propagates outer cancellation, and restores input/plan order after completion.
- Only independent reviewers overlap. Briefing completes before launch; context
  interaction/reconsideration, discussion, outcome interaction/reconsideration, Policy
  Gate, adjudication, digest and persistence remain ordered after full batch settlement.
- Schema 2.3 persists bounded content-free `wall_clock_ms`, accumulated
  `sampling_wait_ms`, effective limit, observed peak, batch count and configuration
  disposition. V1 and V2.0/V2.1/V2.2 remain readable with conservative legacy defaults.
- Metadata projection retains normalized concurrency facts but not prompts, completions,
  source/candidate text, user/model/chief prose, secrets, or raw environment values.
- `get_server_info()` reports effective/max concurrency, disposition, version `0.9.0`,
  build `bounded-parallel-council-v7`, schema `2.3`, budgets 6/13/18 and the unchanged
  five-tool diagnostic order.

## Structural, timing, phase and budget evidence

Exact configuration probe:

| Input | Effective | Disposition |
| --- | ---: | --- |
| missing | 3 | `default` |
| `1` | 1 | `configured` |
| `2` | 2 | `configured` |
| `3` | 3 | `configured` |
| empty | 1 | `invalid_fallback` |
| non-numeric | 1 | `invalid_fallback` |
| `0` | 1 | `invalid_fallback` |
| `4` | 1 | `invalid_fallback` |

Delayed six-role Core probe:

| Limit | Observed wall | Record wall | Sampling wait | Peak | Batches | Calls |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 3 | 52 ms | 43 ms | 36 ms | 3 | 2 | 6 |
| 1 | 161 ms | 153 ms | 36 ms | 1 | 6 | 6 |

At limit 3, completion order was deliberately different from plan order, while the
persisted records remained exactly:
`fidelity_reviewer, terminology_reviewer, product_context_reviewer,
brand_voice_reviewer, risk_ambiguity_reviewer, fluency_reviewer`. Limit 1 preserved the
same order without overlap. The observed limit-3 wall time was about 68% lower; bounded
peak/barrier and exact-call assertions are the primary evidence, not timing alone.

The deep standard regression passed with exactly 13 calls in this sampling sequence:
`INDEPENDENT x6 -> CONTEXT_RECONSIDERATION x3 -> DISCUSSION x1 ->
OUTCOME_RECONSIDERATION x3`. Context and outcome elicitation each occurred once outside
the sampling budget. Budgets remain exactly 6/13/18. Partial and failed-role coverage
remained conservative and no failed request was replayed.

## Campaign verification

- Runtime concurrency/config, barriers, reverse completion, exceptions, invalid config,
  sequential override and tool diagnostics:
  `30 passed in 2.25s`.
- Clean/partial coverage, unresolved and answered context, decisions/reconsideration and
  deep 13-call orchestration:
  `25 passed in 0.47s`.
- V1/V2.0/V2.1/V2.2/V2.3 parse, full/metadata/off persistence and privacy/security:
  `34 passed in 0.28s`.
- Primary presentation, dual channel, exact tools, version/schema/defaults and budgets:
  `34 passed in 1.13s`.
- Final compile command:
  `.venv\Scripts\python.exe -m compileall -q src tests` — pass.
- Final full command:
  `$env:PYTHONPATH='src'; .venv\Scripts\python.exe -m pytest -q -p no:cacheprovider --basetemp=.tmp\pytest-campaign007-final`
  — `244 passed in 3.30s`.
- Final baseline-to-HEAD `git diff --check` — pass.
- Read-only AST import/name audit across every changed production Python module:
  `DEAD_IMPORT_CANDIDATES 0`.

## Fresh artifacts and isolated wheel smoke

`uv build --out-dir .tmp/campaign007-r1-dist` produced:

- wheel `council_of_translation-0.9.0-py3-none-any.whl`, 78,323 bytes,
  SHA-256 `1460F2593BAF162EC40AD05786B7C55DDDBD777CE863F1F43B295C918A572AEC`;
- sdist `council_of_translation-0.9.0.tar.gz`, 72,294 bytes,
  SHA-256 `A32EB2DEA9313A3CD55F323EDB0D8ABC91CCE52581CAF18F16B4D194BF9EC230`.

A disposable CPython 3.12 environment installed that exact wheel with the current
resolved FastMCP 3.4.7. `python -I` imported
`...campaign007-r1-wheel-env\Lib\site-packages\council_of_translation\__init__.py`,
and distribution/module introspection both returned `0.9.0`. Installed diagnostics were
build `bounded-parallel-council-v7`, schema `2.3`, effective/max concurrency `3/3`, and
budgets 6/13/18. The installed Core produced peak/batches/calls `3/2/6` and `1/6/6`.
All five registered tools were invoked through the current FastMCP client; review,
continue and view returned primary text plus structured content, continuation linked its
parent, view retrieved the full record, and listing returned stored records.

One isolated uv dependency resolution/install was performed as explicitly authorized;
no live model/provider/Goose request occurred.

## Protected hashes and final Git state

All protected values remained exact after implementation:

| Asset | SHA-256 |
| --- | --- |
| `harness/plan.md` | `75832D233A283489A59C14A6433E12C0B4A7916C1D6F955BEA9AEBB381C87887` |
| `harness/features.json` | `92CC65FFE0A799C4A4525BDADA733CAE6A11599C863E7F016F344820D808FF18` |
| `harness/progress.md` | `4E998697C0BC7E60592334B1875C5003E0521C6EA8EDF7499B98DACFF3E8CA05` |
| `harness/evaluations/CAMPAIGN-006-q010-r2-live-review.md` | `601A1162FD02A578EAA86CE7E92A2F2DC3C9C88AC0B428976BEE63310ACCD8A3` |
| `harness/contracts/CAMPAIGN-006-r3.md` | `1AA82AFAC5E8A9AFD01A1DD3D7457F58AF700ED1CF5D68B799E0688B67C9759A` |
| `harness/evaluations/CAMPAIGN-006-r3-review.md` | `F2144B2AD8AFEA5015E3F2FCB7DF12FB8E69107F961190B6AB017A8938FE50E9` |
| `harness/reports/CAMPAIGN-006-r3-worker.md` | `FC01B5C0163E505BC32D626EE8007D3CB0BB89610DD17CCB0768E4B56A54B45D` |
| `.learnings/LEARNINGS.md` | `52DC1BA8043481911C0DEABB3AC882504D9CBE8BB63D60F391C188586A230DF0` |
| `.learnings/ERRORS.md` | `F99EB75886781958BF5AE6DCF844FD476CBCA45937896A25EE3B2E9D6CD34F0A` |
| audit Markdown | `B48073E063C4C9F34E0B6B4DAE94E80079EAAAD3B2F8E273DD60B2F25F6ABD76` |

Final Git index: empty. Final committed HEAD: `61252ae27823467d74c38efaa59aa1521b006752`.
The remaining dirty/untracked state is exactly the admitted protected Foreman/user set
plus `harness/reports/CAMPAIGN-007-r1-ledger.md` and this Worker report; neither report is
staged or committed.

## Deviations, skipped checks and risks

- The first PKG-040 broad command accidentally used system Python and stopped at
  collection because FastMCP was absent; the repository `.venv` rerun is the reported
  verification.
- Two new-test expectation defects were corrected during package work: the integration
  prompt marker and the location of invalid-config provenance. Two expected V2.2
  new-write assertions were migrated while explicit old-read coverage was retained.
- Fresh build/install initially lacked sandbox access to the uv user cache and was rerun
  with narrow filesystem elevation. The first isolated smoke used the older FastMCP
  enumeration method; it was adapted to current `list_tools()` and passed without a
  product change.
- Ruff and pyflakes were unavailable in the existing environment. Dependencies were not
  changed; the required dead-import scan was completed with a read-only AST binding
  check across all changed production modules and found zero candidates.
- Skipped by contract: live Goose/provider/model performance verification, publication,
  push, PR, release and deployment. Q-011 live evidence remains Foreman/post-publication
  work.
- Remaining risk: deterministic local delays establish scheduling and a material local
  speedup, but real provider latency/rate limiting remains unmeasured because live calls
  were forbidden. No acceptance or project-completion claim is made.
