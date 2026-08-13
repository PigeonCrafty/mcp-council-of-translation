# Campaign Contract: CAMPAIGN-007-r1

## Control

- Role: WORKER / MAIN WORKER
- Mode: STRICT_CAMPAIGN
- State: ASSIGNED
- Repository: `C:\Users\GeZhu\MyMCP\mcp-council-of-translation`
- Baseline commit: `f9651ed64daf86dd5fabac5e7437b9de8b3186bc`
- Baseline subject: `Accept final Q-010 live evidence`
- Dirty files to preserve: Foreman changes to `harness/plan.md`,
  `harness/features.json`, `harness/progress.md`, this untracked contract, and the
  user-owned `.learnings/**`, audit Markdown and `reviews/**`
- Execution environment: separate Codex Main Worker conversation; informational only
- Required Worker capabilities: Python 3.10–3.13 async implementation and testing,
  FastMCP tool inspection, package build and isolated wheel smoke
- Execution ledger path: `harness/reports/CAMPAIGN-007-r1-ledger.md`
- Campaign Worker report path: `harness/reports/CAMPAIGN-007-r1-worker.md`
- Product target: `0.9.0`
- Diagnostic build target: `bounded-parallel-council-v7`
- Write schema target: `2.3`
- Commit policy: four to six scoped local commits; no push, PR, release or deployment
- Worktree strategy: shared; Main Worker owns every authorized implementation path
- Subagent delegation: forbidden because runtime, orchestration, telemetry and schema
  interfaces overlap
- Parallel delegation: forbidden
- Acceptance authority: Foreman only

## Campaign outcome

Reduce normal six-role Council wall-clock latency by running only independent reviewer
sampling with a deterministic maximum concurrency of three, while preserving panoramic
coverage, phase ordering, sample budgets, role/result identity, failure isolation,
review-only behavior and the exact five-tool Goose surface.

## Context

Published V0.8 live evidence measured 15.31 seconds for a six-role non-interactive case.
The six initial reviewer samples are currently awaited one after another and dominate
local MCP work. The prior mixed interactive run added at least two sequential context
reconsiderations. Campaign 007 optimizes only the independent-review phase; it does not
make the whole deliberation graph concurrent.

Read completely before editing: `AGENTS.md`, `harness/plan.md`,
`harness/features.json`, `harness/progress.md`, this contract,
`harness/evaluations/CAMPAIGN-006-q010-r2-live-review.md`,
`harness/contracts/CAMPAIGN-006-r3.md`,
`harness/evaluations/CAMPAIGN-006-r3-review.md`, and
`harness/reports/CAMPAIGN-006-r3-worker.md`.

## Frozen design

### Architecture and invariants

1. Concurrency is confined to the independent-review phase after briefing, deterministic
   preflight and plan construction. Context gaps, context reconsideration, discussion,
   outcome interaction, outcome reconsideration, Policy Gate, adjudication, digest and
   persistence remain phase-ordered and non-overlapping.
2. Default independent-review concurrency is three. Read
   `COUNCIL_REVIEW_CONCURRENCY` once per new review; accept only literal `1`, `2`, or `3`.
   Missing configuration uses three. Invalid, empty or out-of-range configuration uses
   one and records a bounded content-free configuration/fallback disposition.
3. Effective concurrency never exceeds the active role count or three. A value of one
   reproduces sequential provider behavior without changing prompts, roles or results.
4. Reserve the full independent role count in `SampleBudget` before launching any role
   request. Do not let concurrent tasks call an unsafe check-then-increment budget path.
   If the full batch cannot be reserved, start no role call and fail conservatively.
5. Each provider request is attempted exactly once. Do not replay a concurrent failure
   sequentially: retries could duplicate cost, exceed budget, or hide a provider/client
   incompatibility.
6. Correlate each request and response with its originating role. Persist
   `independent_reviews`, findings and role lenses in `CouncilPlan.active_role_ids` order,
   never completion order. An exception, error, malformed result or cancellation for one
   role is normalized as that role's unavailable sample and cannot cancel siblings.
   External cancellation of the entire review may still propagate normally.
7. Preserve all V0.8 semantics: exact role routing, prompts/token caps, structured
   envelope validation, context-gap bounds, discussion, user authority, Policy Gate,
   status degradation, concise primary presentation, privacy modes and budgets 6/13/18.
8. Keep exactly five public MCP tools. Do not add a performance, batch, debug or raw-JSON
   tool and do not change Goose.

### Shared interfaces and data contracts

- Add a bounded async sampling-batch primitive owned by the runtime/orchestration layer.
  It receives role-correlated work in plan order, enforces the effective limit and
  returns correlated results in input order.
- `RuntimeMetadata` V2.3 must add bounded content-free fields for:
  `wall_clock_ms`, accumulated sampling wait, effective independent-review concurrency
  limit, observed peak concurrency, and independent-review batch/wave count. The Worker
  may choose exact Python field names, but documentation, tests and server diagnostics
  must use them consistently.
- Preserve existing `elapsed_ms` as a backward-compatible accumulated runtime metric; do
  not silently redefine it. `wall_clock_ms` is the new end-to-end Core duration.
- New records write schema `2.3`. Parsing and persistence must continue accepting V1 and
  V2.0, V2.1 and V2.2. Older records receive conservative defaults (no claimed
  parallelism) and are never rewritten merely by reading.
- `get_server_info()` reports the effective concurrency limit, maximum supported value,
  configuration disposition, package/module `0.9.0`, build
  `bounded-parallel-council-v7`, schema `2.3`, unchanged budgets and unchanged five-tool
  order.
- Metadata/history projections must retain only content-free concurrency facts. They
  must not persist prompts, completions, source/candidate text or environment values
  beyond the normalized disposition and effective integer.

### Main Worker implementation discretion

- Choose `asyncio` scheduling/semaphore structure, internal helper names, and exact
  telemetry field names.
- Add small internal dataclasses or protocols when they reduce correlation or
  cancellation risk.
- Adjust deterministic scripted test doubles to be concurrency-safe while retaining
  established sequential test semantics.
- Select a stable CI-safe delayed-executor duration and performance assertion, provided
  the structural concurrency/barrier evidence is the primary proof and the timing check
  is not unreasonably flaky.

### Decisions reserved for Foreman or user

- Raising maximum/default concurrency above three.
- Parallelizing context or outcome reconsideration, discussion or any interaction.
- Automatic retry/replay after a failed concurrent request.
- Provider-specific branches, per-role model routing, budget changes, new tools, custom
  Goose UI, or a change to review-only/user authority behavior.
- Accepting or publishing the implementation, and post-publication Q-011 live evidence.

## Global boundaries

### Allowed production, package and documentation paths

- `src/council_of_translation/__init__.py`
- `src/council_of_translation/server.py`
- `src/council_of_translation/tools/review.py`
- `src/council_of_translation/localization/runtime.py`
- `src/council_of_translation/localization/orchestration.py`
- `src/council_of_translation/localization/models.py`
- `src/council_of_translation/localization/compatibility.py`
- `src/council_of_translation/localization/persistence.py`
- `tests/**/*.py`, only where directly required for the contracted behavior/version
- `pyproject.toml`
- `README.md`
- `AGENTS.md`
- `docs/v0.4-architecture.md`
- `docs/v0.4-tool-contract.md`
- required Campaign ledger and Worker report only under `harness/reports/`

### Forbidden files, directories, and systems

- Foreman-owned `harness/plan.md`, `harness/features.json`, `harness/progress.md`, every
  contract and evaluation
- prior Worker reports/ledgers
- `.learnings/**`, `reviews/**`, audit Markdown and `myTest/**` if it appears
- roles, prompt builders/prompts, guided forms, clustering, deliberation/Policy Gate,
  digest/presentation and security production modules
- dependencies, tool count/names, sample budgets, role registry/routing, public output
  modes/default interaction modes, review-only authority or persistence privacy policy
- Goose installation/configuration, provider credentials, GitHub, remote branches,
  releases and deployments

### Non-goals

- Parallelizing the complete Council workflow.
- Reducing role count, prompt size or evidence depth to create an artificial speedup.
- Provider/model selection or per-role routing.
- Batch review of multiple translations.
- A custom queue, distributed worker service, global cross-review rate limiter or cache.
- Showing performance counters in the concise human-facing Council report.

### Authorized external or destructive actions

- No destructive or live provider/Goose actions.
- Local scoped Git staging and four to six commits are required.
- Fresh package build and a disposable isolated environment under the repository or OS
  temp directory are authorized. Public dependency resolution is allowed only if the
  isolated smoke cannot use already installed/cache-resolved dependencies; record its
  count and do not modify system or Goose environments.

## Admission gate and protected assets

Before editing:

1. verify exact HEAD/subject and empty Git index;
2. confirm only the declared Foreman/user dirt exists;
3. hash this contract and verify every protected hash below;
4. run `.venv\Scripts\python.exe -m compileall -q src tests`;
5. run the full suite with disabled pytest cache and repository-local basetemp; expect
   exactly `220 passed`;
6. record the current sequential six-role loop and telemetry semantics as the reproduced
   baseline.

Stop `BLOCKED` on unexplained drift. Never stage, rewrite, delete, move or commit a
protected asset.

| Protected asset | SHA-256 |
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

## Task graph

| Package | Observable outcome | Depends on | Allowed boundary | Acceptance and verification | Parallel-safe |
| --- | --- | --- | --- | --- | --- |
| PKG-037 | Bounded correlated sampling batch and safe config | none | runtime plus focused unit tests | limits 1/2/3, default/invalid dispositions, barrier proves real overlap, ordered results, sibling exception isolation | no |
| PKG-038 | Core uses concurrency only for independent roles | PKG-037 | orchestration plus focused integration tests | upfront budget reservation, exact once calls, stable role/evidence order, sequential override, no later-phase overlap | no |
| PKG-039 | V2.3 truthful telemetry and compatibility | PKG-038 | models, compatibility, persistence plus tests | wall/work durations and concurrency facts correct; V1/V2.0–2.2 load; metadata remains private | no |
| PKG-040 | FastMCP/config diagnostics and regression integration | PKG-039 | review tool/server plus integration tests | exact five tools; environment modes visible; dual channel, context and decision paths preserved | no |
| PKG-041 | V0.9 migration and installable artifacts | PKG-040 | version/package/docs and affected tests | 0.9.0/build v7/schema 2.3 everywhere; full suite, fresh artifacts, isolated current-FastMCP wheel smoke | no |

## Collision and integration map

| Packages/files at risk | Required sequencing or isolation | Integration owner/check |
| --- | --- | --- |
| PKG-037/038 runtime telemetry and scheduling | scheduler contract before orchestration use | Main Worker / focused async and budget suite |
| PKG-038/039 orchestration snapshot and schema | Core behavior before persisted field migration | Main Worker / round-trip full/metadata tests |
| PKG-039/040 version/schema diagnostics | one authoritative constants mapping | Main Worker / source and installed-wheel introspection |
| All packages/tests | single shared worktree, sequential commits | Main Worker / complete baseline-to-final diff and full suite |

## Campaign acceptance criteria

1. With six independent roles and effective concurrency three, structural test evidence
   shows actual overlap bounded at three and two waves/batches; effective one shows no
   overlap and established sequential behavior.
2. A delayed deterministic executor shows a material wall-clock reduction for limit
   three versus one. Use a generous CI-safe threshold backed by barrier/peak evidence;
   timing alone is not sufficient.
3. All six calls are made exactly once, correlated to the correct prompt/role and
   persisted in plan order even when completion order is reversed.
4. One role exception/error/malformed envelope does not cancel or contaminate siblings;
   coverage/status/warnings remain the established conservative partial-coverage result.
5. Budget is reserved before launch, exact call totals stay within 6/13/18, and no
   hidden retry or post-budget call occurs. The accepted deep standard path remains
   exactly 13 total calls.
6. Briefing occurs before any sampling; context interaction/reconsideration, discussion,
   outcome interaction/reconsideration, Policy Gate and adjudication cannot begin until
   the independent batch is fully settled.
7. V2.3 telemetry reports truthful wall time, accumulated sampling wait, configured
   effective limit, actual peak and batches. Content-free metadata projection preserves
   only allowed facts. Old records remain readable.
8. Invalid concurrency configuration safely uses one and is visible in server/record
   diagnostics; valid 1/2/3 values behave exactly as declared.
9. No Council semantic or presentation regression: standard marketing has the exact six
   accepted roles/lenses, mixed unresolved context still requires human review,
   review-only emits no full translation, and the verdict remains last.
10. Package/module `0.9.0`, build `bounded-parallel-council-v7`, schema `2.3`, exact five
    tools and budgets 6/13/18 agree across source, records, docs, fresh wheel and sdist.

## Required Campaign verification

- Run focused runtime concurrency/config tests, including gate/barrier, reversed
  completion, per-role exception, invalid configuration and sequential override.
- Run focused orchestration tests covering six-role clean, partial coverage, unresolved
  context, answered context, outcome/reconsideration and deep 13-call paths.
- Run V1/V2.0/V2.1/V2.2/V2.3 parsing, full/metadata/off persistence and privacy tests.
- Run primary presentation, dual-channel, exact tool surface, version/schema/default and
  budget suites.
- Run compile and the complete test suite with `.venv\Scripts\python.exe`, disabled
  pytest cache and repository-local basetemp.
- Build fresh wheel and sdist. Install the wheel into a disposable Python 3.12
  environment and call all five registered tools through current installed FastMCP.
  Exercise one six-role concurrent review with a deterministic delayed executor and one
  sequential override; verify source is imported from site-packages.
- Run `git diff --check f9651ed64daf86dd5fabac5e7437b9de8b3186bc..HEAD`, exact
  changed-path audit, protected-hash audit, dead-import scan and empty-index check.
- Do not run live Goose/provider/model calls. Q-011 is an independent post-publication
  Foreman gate.

## Delegation protocol

- Implementation subagents are forbidden. Execute packages sequentially.
- Main Worker owns every diff, integration decision, verification command and report.
- Do not delegate acceptance authority or edit Foreman state.

## Required evidence

- Package/commit/files/verification matrix in the ledger and Worker report.
- Before/after structural and timed concurrency probes, including observed peak, batches,
  completion order, persisted order and call count.
- Exact configuration truth table for missing, 1, 2, 3, empty, non-numeric and
  out-of-range values.
- Exact phase-order trace and deep-budget call sequence.
- Schema compatibility and privacy projection examples without source/model/user text.
- Exact full-suite, build, wheel hashes and isolated import/tool-call results.
- Baseline-to-final changed paths, diff inspection, protected hashes and repository state.
- Subagent count, approval/escalation count, external dependency actions, live-call
  count, skipped checks, retries/deviations and remaining risks.
- Redact credentials, tokens and unnecessary sensitive content; report redaction without
  exposing values.

## Stop conditions

- Baseline, index, dirty set, contract hash or protected hashes differ.
- FastMCP/Goose concurrency requires provider-specific code, a new tool, duplicate calls,
  automatic replay or concurrency above three.
- Correctness requires parallelizing a post-review phase, changing roles/prompts/budgets,
  weakening coverage/status behavior or altering concise presentation.
- Schema compatibility, deterministic correlation, exact-once budget behavior or
  failure isolation cannot be established.
- Work requires an unauthorized path, dependency, credential, live call, external
  mutation, destructive action, push, PR, release or deployment.

## Handoff

Maintain `harness/reports/CAMPAIGN-007-r1-ledger.md` during execution and write
`harness/reports/CAMPAIGN-007-r1-worker.md`. Start the conversational handoff with exactly
`READY_FOR_REVIEW` or `BLOCKED`, then summarize contract hash, baseline/final HEAD,
package/commit/file mapping, concurrency/config/phase/budget evidence, focused/full/build/
wheel results, protected hashes, index/worktree state, subagent/authority/external/live
counts, deviations/skips and remaining risks. Do not push or claim Campaign acceptance,
publication, Q-011 acceptance or project completion.
