# CAMPAIGN-007-r2 Main Worker Report

## Status and authority

- Worker outcome: `READY_FOR_REVIEW`; Foreman acceptance is not claimed.
- Role/mode: `WORKER / MAIN WORKER`, `STRICT_CAMPAIGN`.
- Contract: `harness/contracts/CAMPAIGN-007-r2.md`.
- Contract SHA-256:
  `612CC6F9C42B93956A1CCB4EC8ACE1B634F42AFE674B9EB48105CD76772D888D`.
- Exact admitted baseline:
  `61252ae27823467d74c38efaa59aa1521b006752` (`Release bounded parallel Council V0.9`).
- Final HEAD: `e835566a2c8d60ba153b68175d19685cb96185fe`.
- Implementation subagents: forbidden / 0 used.
- Campaign authority escalations: 0. Live Goose/provider/model calls: 0.
- No push, PR, release, deployment, credential request or Goose change occurred.

## Admission and protected state

Before editing, the Main Worker completely read the r2 contract, r1 Foreman review,
r1 contract/report/ledger, AGENTS, plan, features and progress plus the pigeon-harness
common and Worker protocols. Admission verified the exact HEAD and subject, empty Git
index, expected Foreman/user dirty set, exact r2 contract hash and all 11 protected
hashes. Baseline compile passed and the full suite was exactly `244 passed in 3.56s`.

The authorized correction boundary was only:

- `src/council_of_translation/localization/orchestration.py`
- `tests/integration/test_parallel_orchestration.py`
- `tests/integration/test_orchestration_v2.py`
- `tests/integration/test_v22_briefing.py`
- this required, uncommitted Worker report

The r1 ledger and report, Foreman Harness state, evaluations, contracts, `.learnings/`,
`reviews/` and audit Markdown were not edited, staged or committed.

## Before/after counterexamples

A deterministic 30 ms final-render delay and a 20 ms continuation sample reproduced
the accepted r1 defect before implementation:

| Path | Before | After |
| --- | --- | --- |
| Normal new review | `wall_clock_ms=1` despite 30 ms late render | `wall_clock_ms=33` |
| Required-briefing early return | `wall_clock_ms=0`, sampling 0, `RETURNED_PENDING` | `wall_clock_ms=32`, sampling 0, same status |
| Continuation | `wall=0`, `sampling_wait=20`, calls 1, provenance `1/0/0/legacy` | `wall=17`, `sampling_wait=20`, calls 1, provenance `3/1/2/default` |
| Continuation parent | provenance `3/1/2/default` | unchanged and byte-immutable |

Values are milliseconds. The delayed regression bounds are intentionally generous
(`20..1999` for final-render paths and `15..1999` for continuation) so structural late
finalization, rather than fragile timing precision, is the assertion.

## Correction and commit

Exactly one scoped local commit was created:

- `e835566a2c8d60ba153b68175d19685cb96185fe` —
  `Finalize V2.3 record timing provenance`

The implementation:

1. finalizes new-review and required-briefing `wall_clock_ms` after phase/digest/display/
   record construction and refreshes the record runtime snapshot immediately before its
   existing single save;
2. starts the continuation timer before continuation work and finalizes/refreshed its
   child snapshot after phase trace and display, immediately before its existing save;
3. copies the parent's independent-review limit, peak, batch count and configuration
   disposition into the child telemetry while retaining the child's own sampling,
   elicitation, accumulated wait and wall duration;
4. removes the unmodeled `telemetry.independent_review_wall_clock_ms` assignment;
5. adds deterministic late-render and delayed-continuation assertions, including stored
   round trips and parent immutability.

No second save, schema/public field, scheduler, environment rule, retry, tool, version,
budget, role, prompt, decision, persistence-policy, documentation or presentation change
was introduced. The committed diff is four authorized files, 127 insertions and six
deletions; `git diff --check` passed.

## Verification

- Three delayed telemetry counterexamples:
  `3 passed in 0.38s`.
- Runtime concurrency plus the complete modified orchestration/briefing files:
  `34 passed in 1.41s`.
- r1 runtime, concurrency, continuation, briefing, V1/V2 persistence/privacy,
  dual-channel, exact tool surface, V0.8 semantic/context/marketing and presentation
  regression matrix:
  `121 passed in 2.57s`.
- Pre-commit full suite: `246 passed in 3.21s`.
- Final compile:
  `.venv\Scripts\python.exe -m compileall -q src tests` — pass.
- Final full suite with disabled pytest cache and repository basetemp:
  `$env:PYTHONPATH='src'; .venv\Scripts\python.exe -m pytest -q -p no:cacheprovider --basetemp=.tmp\pytest-campaign007-r2-final`
  — `246 passed in 3.26s`.
- Baseline-to-final diff check — pass.
- Exact allowed-path audit — four paths above, pass.
- Unmodeled dynamic assignment scan — absent.
- Read-only AST dead-import scan of changed production code:
  `DEAD_IMPORT_CANDIDATES 0`.
- Git index — empty.

The accepted r1 configuration truth table, peak/batch ordering, exact-once calls,
failure isolation, cancellation, no replay, 6/13/18 budgets, deep 13-call sequence,
context/outcome ordering, Policy Gate, review-only presentation, V1/V2.0–2.2 reads,
schema 2.3 privacy, version/build and exact five-tool diagnostics remain green.

## Fresh artifacts and installed-wheel smoke

`uv build --out-dir .tmp/campaign007-r2-dist` produced:

- `council_of_translation-0.9.0-py3-none-any.whl`, 78,383 bytes,
  SHA-256 `2EF24AD76875542D21FA8D540B5FFD4DF8D549E0CCF8428A8EA99EDAB831B7C2`;
- `council_of_translation-0.9.0.tar.gz`, 72,325 bytes,
  SHA-256 `05497FA79FAAF2FCA11093C90B0996EBEDE6BF7A07310A364D6D320B5E745120`.

A fresh disposable CPython 3.12 environment installed that exact wheel with current
FastMCP 3.4.7. Isolated `python -I` imported from
`.tmp/campaign007-r2-wheel-env/Lib/site-packages`, and distribution introspection
returned `0.9.0`.

All five registered tools were called through the FastMCP client. Diagnostics reported
version `0.9.0`, build `bounded-parallel-council-v7`, schema `2.3` and budgets 6/13/18.
The actual tool-created parent was schema 2.3, `RETURNED_PENDING`, `wall=46`, seven
sampling calls, accumulated sampling wait 86, and independent provenance
`3/3/2/configured`. The actual continuation child was schema 2.3, linked to the parent,
`wall=20`, one sampling call, accumulated wait 18, and the same `3/3/2/configured`
provenance. Primary text plus structured content, full view and list all succeeded.

The in-memory FastMCP sampling callback itself observed peak one while the Core batch
reported three active correlated tasks; current FastMCP serializes this test callback.
This does not alter the accepted Core scheduler evidence and is disclosed for the
post-publication Q-011 provider test.

One isolated uv dependency resolution/install was performed; no live provider/model or
Goose action occurred.

## Protected hashes and final Git state

| Protected asset | Final SHA-256 |
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

Final HEAD is `e835566a2c8d60ba153b68175d19685cb96185fe`; exactly one commit follows the
contract baseline. The index is empty. The remaining worktree dirt is the admitted
Foreman/user set plus this required untracked r2 report. No protected asset is staged.

## Deviations, skipped checks and remaining risk

- No implementation deviation from the r2 correction boundary occurred.
- Sandbox filesystem elevation was used only for the required local Git write, uv cache
  access and artifact hashing; it did not expand Campaign authority.
- Skipped because forbidden: live Goose/provider/model validation, push, PR, release,
  deployment and Q-011 acceptance.
- Remaining external risk: actual Goose/provider overlap, latency and rate-limit behavior
  remain unmeasured. The installed in-memory FastMCP handler serialized callbacks, so
  Q-011 remains the independent post-publication compatibility/latency gate.
- No Campaign acceptance, publication, Q-011 acceptance or project-completion claim is
  made.
