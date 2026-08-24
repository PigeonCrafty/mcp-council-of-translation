# Campaign Contract: CAMPAIGN-011-r1

## Control

- Role: `WORKER / MAIN WORKER`
- Mode: `STRICT_CAMPAIGN`
- State: `ASSIGNED`
- Repository: `C:\Users\GeZhu\MyMCP\mcp-council-of-translation`
- Baseline commit: `610eae8e7c2df31fd9052b0ae76a2d718805f28d`
- Baseline subject: `Accept Q-003 Desktop and CLI evidence`
- Admission baseline: compile passes and exactly `294 passed`
- Dirty assets to preserve: Foreman-owned `harness/plan.md`, `harness/features.json`,
  `harness/progress.md`, this contract, user-owned `.learnings/**`, the independent audit
  Markdown and `reviews/**`
- Execution environment: provider-neutral Codex Main Worker in a separate conversation
- Required Worker capabilities: Python 3.12, uv, Git, pytest, package build and isolated
  FastMCP wheel smoke
- Execution ledger path: `harness/reports/CAMPAIGN-011-r1-ledger.md`
- Campaign Worker report path: `harness/reports/CAMPAIGN-011-r1-worker.md`
- Commit policy: required; one scoped local commit per completed package
- Worktree strategy: shared worktree, strict package sequencing
- Subagent delegation: allowed, maximum three bounded subagents
- Parallel delegation: read-only analysis may run in parallel; implementation parallelism
  is forbidden because the production packages share routing/model/release files

## Campaign outcome

Deliver V0.11 as a risk-coherent, still review-only Translation Council. When the caller
classifies content as `legal_risk`, the Council must expose the product, user-understanding
and risk blind spots that V0.10.2's four-role standard route can miss, without adding a
generic legal adviser, inventing laws, exceeding the accepted sampling budgets, bloating
the primary report or changing the five-tool surface.

## Context

All V0.10.2 feature items and all 12 historical quality gates are accepted. Q-012 Case C
and subsequent route inspection expose the next bounded product gap: `legal_risk` in
standard mode currently resolves to only technical, fidelity, terminology and fluency
because role applicability is intersected with mode defaults. The already-defined
`risk_ambiguity_reviewer` is omitted in standard mode, while product-context and UX-copy
are excluded from legal-risk content. That is inconsistent with the product purpose of
showing users material blind spots.

The accepted V0.10.2 implementation, output grouping, evidence hierarchy, Policy Gate,
user authority, concurrency and history are the baseline. Do not redesign them.

## Frozen design

### Architecture and invariants

1. Keep exactly these five public tools in this order:
   `review_translation`, `continue_review`, `view_review_record`,
   `list_review_records`, `get_server_info`.
2. Keep default `review_only`; only explicit `full_rewrite` may produce a complete
   `suggested_translation`.
3. Keep sample budgets `lightweight=6`, `standard=13`, `strict=18`; only independent
   reviewer calls are concurrent and the default/max configured concurrency remains 3.
4. Keep the evidence hierarchy, deterministic preflight, context/outcome interaction,
   reconsideration limits, one discussion round, Policy Gate, Position Matrix and no-vote
   authority model unchanged.
5. Standard routes must contain at most six independent reviewers so the accepted deepest
   path remains `6 independent + 3 context reconsideration + 1 discussion + 3 outcome
   reconsideration = 13`.
6. V0.11 writes Schema `2.5`, package/module `0.11.0` and diagnostic build
   `risk-coherent-council-v9`.
7. V1 and V2.0 through V2.4 records remain readable. Missing new routing fields receive
   explicit conservative compatibility defaults; historical records are never rewritten.
8. Routing provenance is deterministic and sampling-free. It cannot contain caller prose,
   model reasoning, credentials, paths or arbitrary role IDs.
9. Primary output remains exactly five sections, targets 1,200 Unicode code points for
   clean cases, is capped at 3,200, hides internal IDs and preserves the chief disposition
   last. Full structured evidence remains unchanged by display grouping.
10. No reviewer may invent statutes, jurisdictional obligations or legal advice. Explicit
    caller rules and supplied jurisdictional evidence remain authoritative; absent legal
    context must be stated as uncertainty rather than fabricated.

### Frozen routing portfolios

Routing order is authority-neutral presentation/execution order, never a vote weight.
Implement explicit deterministic profiles with these exact role IDs:

| Content | Lightweight | Standard | Strict |
| --- | --- | --- | --- |
| `unspecified` | technical, fidelity, terminology, fluency | technical, fidelity, terminology, product-context, UX-copy, fluency | all eight existing reviewers in priority order |
| `ui` | technical, fidelity, terminology, fluency | technical, fidelity, terminology, product-context, UX-copy, fluency | same six-role UI portfolio |
| `marketing` | fidelity, terminology, fluency | fidelity, terminology, product-context, brand-voice, risk-ambiguity, fluency | same six-role marketing portfolio |
| `technical_documentation` | technical, fidelity, terminology, fluency | technical, fidelity, terminology, product-context, fluency | same five-role technical-documentation portfolio |
| `legal_risk` | fidelity, terminology, risk-ambiguity, fluency | fidelity, terminology, product-context, UX-copy, risk-ambiguity, fluency | technical, fidelity, terminology, product-context, UX-copy, risk-ambiguity, fluency |

The table preserves every accepted non-legal portfolio. Legal-risk lightweight is focused
at four roles; standard is panoramic at six; strict adds the technical reviewer for seven.
Deterministic preflight always runs, including when the independent technical reviewer is
not in a legal-risk lightweight/standard portfolio.

### Shared interfaces and data contracts

1. Extend `CouncilPlan` with:
   - `routing_profile`: one bounded deterministic profile identifier;
   - `routing_reason_codes`: a bounded list of safe deterministic codes.
2. Profile identifiers are derived only from normalized content type and mode. Reason
   codes are limited to fixed vocabulary equivalent to content type, mode, preserved
   legacy portfolio, risk-focused/risk-panorama/risk-strict and deterministic-preflight
   coverage. Do not persist natural-language reasoning.
3. Schema 2.5 persistence and compact/full results expose the profile and codes in
   structured content. Primary Markdown may express the selected professional coverage
   in natural Chinese but must never print internal profile/reason/role IDs.
4. Align existing role metadata with the frozen profiles: product-context and UX-copy may
   apply to legal-risk; risk-ambiguity may apply in lightweight, standard and strict when
   selected by an explicit profile. Do not add another reviewer role.
5. Keep `ROLE_DEFINITIONS` at nine total entries: eight reviewers plus the chief editor.
6. Keep all routing functions deterministic, registry-backed and free of task-content
   keyword inference. `legal_risk` is selected by normalized caller/Briefing content type,
   not fuzzy scanning of source, candidate or context prose.

### Main Worker implementation discretion

- Internal helper names and the exact mapping data structure.
- Whether compatibility defaults use a named legacy profile or a bounded unknown profile,
  provided old records parse deterministically and do not claim new routing evidence.
- Test fixture organization and natural Chinese display wording within the frozen output
  contract.
- How to split focused tests among authorized existing files and the new V0.11 test file.

### Decisions reserved for Foreman or user

- Any new MCP tool or public tool signature change.
- Any new reviewer/adjudicator role.
- Any change to the frozen portfolios, budgets, concurrency, evidence hierarchy, user
  authority, review-only boundary or five-section report contract.
- Fuzzy risk inference, legal-advice behavior, live provider calls, release, push, PR or
  deployment.
- Acceptance of any package, Campaign, publication or Q-013 live gate.

## Global boundaries

### Allowed production and package paths

- `src/council_of_translation/__init__.py`
- `src/council_of_translation/evaluation.py`
- `src/council_of_translation/localization/models.py`
- `src/council_of_translation/localization/roles.py`
- `src/council_of_translation/localization/orchestration.py`
- `src/council_of_translation/localization/persistence.py`
- `src/council_of_translation/localization/compatibility.py`
- `src/council_of_translation/localization/digest.py`
- `src/council_of_translation/tools/review.py`
- `pyproject.toml`
- `uv.lock`

### Allowed tests and fixtures

- `tests/unit/test_roles_v2.py`
- `tests/unit/test_persistence_v2.py`
- `tests/unit/test_v24_value_metrics.py`
- `tests/unit/test_v22_models_persistence.py`
- `tests/integration/test_v11_routing.py` (new)
- `tests/integration/test_orchestration_v2.py`
- `tests/integration/test_parallel_orchestration.py`
- `tests/integration/test_v24_presentation.py`
- `tests/integration/test_v24_golden_corpus.py`
- `tests/integration/test_tool_surface_v2.py`
- `tests/integration/test_v10_release_contract.py`
- `tests/fixtures/v24_golden_corpus.json`

### Allowed documentation

- `README.md`
- `AGENTS.md`
- `docs/v0.4-architecture.md`
- `docs/v0.4-tool-contract.md`

Historical `v0.4-*` documentation filenames remain stable; update their authoritative
content to V0.11 rather than renaming them.

### Allowed Worker evidence paths

- `harness/reports/CAMPAIGN-011-r1-ledger.md`
- `harness/reports/CAMPAIGN-011-r1-worker.md`

The two report files must remain untracked and unstaged for Foreman review. The Worker may
not modify any other `harness/**` file.

### Forbidden files, directories and systems

- `.learnings/**`, `reviews/**`, `myTest/**`, `.tmp/**` except disposable ignored test,
  build and isolated-smoke directories created by the Worker
- all `harness/contracts/**`, `harness/evaluations/**`, `harness/plan.md`,
  `harness/features.json`, `harness/progress.md`
- raw Q-003/Q-012 records, screenshots, provider/session logs and user test output
- Goose installation/configuration, credentials, provider accounts and external services
- GitHub state, branches, PRs, releases, tags and deployments
- dependency additions or removals

### Non-goals

- General-purpose Council expansion
- Automatic legal or jurisdictional advice
- Confidence percentages or uncalibrated confidence redesign
- Replay/debug tooling
- Dynamic keyword-based role selection
- Role voting, role weights or majority rules
- New elicitation UI or native CLI form support
- Translation-file editing or automatic application of suggested fixes

### Authorized external or destructive actions

- Local dependency/build resolution only when required for package build or isolated wheel
  smoke; record command count and result.
- Local exact-path staging and commits for the six packages.
- Disposable ignored directories under `.tmp/` may be created and removed after resolving
  their absolute path inside this repository. Do not delete user-owned test or review data.
- No live Goose/provider/model call, network mutation, push, PR, release or deployment.

## Task graph

| Package | Observable outcome | Depends on | Allowed boundary | Acceptance and verification | Parallel-safe |
| --- | --- | --- | --- | --- | --- |
| `PKG-057` / F-047 | Explicit route profiles and Schema 2.5 CouncilPlan fields | none | models, roles, compatibility, focused unit tests | Exact 15-profile matrix, safe provenance validation, old-plan defaults and deterministic repeated construction | no |
| `PKG-058` / F-048 | Legal-risk 4/6/7 panoramic portfolios and bounded role instructions | PKG-057 | roles, orchestration-facing tests, new routing integration test | Exact legal portfolios/order, no new role, no invented-law permission, non-legal counterexamples unchanged | no |
| `PKG-059` / F-049 | Routing provenance survives orchestration, persistence and continuation within budgets | PKG-058 | orchestration, persistence, compatibility, models, relevant runtime tests | Standard deep path exactly 13, strict within 18, zero routing calls, V1/V2.0–2.4 compatibility and immutable parent/child provenance | no |
| `PKG-060` / F-050 | Concise risk-route primary presentation | PKG-059 | digest and presentation tests | Five sections, natural role coverage, privacy-safe IDs, material consequences retained, no repeated repair, clean <=1200 and hostile <=3200 | no |
| `PKG-061` / F-051 | 24-case executable Golden corpus | PKG-060 | evaluation runner, golden fixture/test, focused value tests | Original 18 unchanged plus exact six risk cases; 24/24 and every aggregate metric 1.0; budgets truthful | no |
| `PKG-062` / F-052 | V0.11 release migration and authoritative docs | PKG-061 | version/tool metadata, package, lock, docs, release tests | 0.11.0/build v9/schema 2.5, exact five tools, frozen defaults/budgets/concurrency, fresh artifacts and isolated wheel smoke | no |

## Collision and integration map

| Packages/files at risk | Required sequencing or isolation | Integration owner/check |
| --- | --- | --- |
| PKG-057/058 `roles.py` and routing tests | Finish and verify profile model before portfolio changes | Main Worker / exact matrix replay |
| PKG-057/059 models and compatibility | Schema fields before persistence/continuation work | Main Worker / old-record round trip |
| PKG-059/060 orchestration projection and digest | Persist final plan before presentation assertions | Main Worker / structured-object immutability |
| PKG-061/062 evaluation, version and docs | Golden passes before release migration | Main Worker / final installed artifact run |
| `uv.lock` | PKG-062 only; pinned canonical operation | Main Worker / exact one-root-version diff |

## Campaign acceptance criteria

1. Baseline admission is exact and all changed paths are authorized.
2. All six packages satisfy their individual acceptance criteria and are represented by
   scoped local commits.
3. Exact non-legal route portfolios remain unchanged; legal-risk routes are exactly 4/6/7
   in the frozen order.
4. CouncilPlan routing provenance is bounded, deterministic, JSON-safe, persisted and
   compatible without user or model prose.
5. Legal-risk standard includes product-context, UX-copy and risk-ambiguity within six
   independent calls; strict includes technical within seven.
6. Reviewer instructions forbid invented statutes/legal requirements and preserve caller
   evidence authority.
7. Sampling, reconsideration, discussion and budget invariants remain true; routing adds
   zero model and interaction calls.
8. Primary reports remain concise, five-section, privacy-safe and non-repetitive while
   preserving full structured role evidence and risk consequences.
9. Golden evaluation passes exactly 24/24 with all aggregate metrics at 1.0 and no
   fixture-authored observed data.
10. Package/module `0.11.0`, build `risk-coherent-council-v9`, schema `2.5`, exact five
    tools, defaults, budgets and concurrency are verified from a freshly built wheel.
11. Full compile and complete test suite pass; baseline-to-final `git diff --check`, scope,
    dead-import and repository hygiene checks pass.
12. No protected/user asset, raw live record, credential, Goose state or external GitHub
    state is read into product assets or mutated.

## Required Campaign verification

Run and record at minimum:

```powershell
python -m compileall src tests
python -m pytest -q --basetemp <unique-workspace-path>
python -m pytest -q tests/unit/test_roles_v2.py tests/integration/test_v11_routing.py
python -m pytest -q tests/integration/test_v24_golden_corpus.py tests/integration/test_v24_presentation.py
python -m pytest -q tests/unit/test_persistence_v2.py tests/unit/test_v22_models_persistence.py tests/integration/test_orchestration_v2.py
python -m pytest -q tests/integration/test_tool_surface_v2.py tests/integration/test_v10_release_contract.py
git diff --check 610eae8e7c2df31fd9052b0ae76a2d718805f28d..HEAD
```

Also provide deterministic probes for:

- all 15 content/mode profile combinations and exact ordered role IDs;
- legal-risk standard deepest path `6+3+1+3=13` and strict maximum within 18;
- zero additional sampling/elicitation from routing or display;
- V1 and V2.0–2.4 record compatibility plus Schema 2.5 round trip;
- primary/full structured preservation and internal-ID privacy;
- 24-case Golden aggregate JSON;
- exact public tool order and server diagnostics;
- fresh sdist/wheel, archive member inspection and isolated Python 3.12/FastMCP 3.4.7
  calls to all five tools.

For `uv.lock`, use exact uv `0.12.3` and a repository-local cache/tool directory. The only
accepted lock diff is the editable root version `0.10.2 -> 0.11.0`; preserve revision 3,
78 packages and 586 upload-time entries. If canonical regeneration produces any other
drift, stop without manual lock editing and report `BLOCKED`.

## Delegation protocol

- Main Worker may use at most three bounded subagents for disjoint read-only analysis,
  test design or implementation paths that do not overlap.
- Do not delegate Foreman asset edits, integration, Git staging/commits, final verification
  or acceptance authority.
- Do not concurrently edit overlapping files in this shared worktree.
- Main Worker must inspect every returned diff, rerun package checks on integrated state
  and record delegation/result/integration in the ledger.
- If no useful disjoint delegation exists, Main Worker may execute all packages directly.

## Required evidence

- Admission HEAD/status, admitted dirty paths and exact contract SHA-256.
- Package-to-files/commits/tests matrix and any subagent assignment/result.
- Exact route profile truth table and before/after legal-risk counterexample.
- Sampling/elicitation counts for standard deep and strict bounded paths.
- Compatibility, persistence and structured-object immutability evidence.
- Golden 24/24 aggregate and total scripted sampling/elicitation counts.
- Full compile/test results, fresh artifact names/sizes/SHA-256 and isolated smoke output.
- Baseline-to-final changed-file list, diff inspection, scope audit and `diff --check`.
- Protected/admitted asset reconciliation, Git index state, skipped checks and consequences.
- Counts of subagents, approval/escalation requests, dependency operations, live calls and
  external mutations.

## Stop conditions

- HEAD is not the exact baseline or admitted dirty paths overlap an authorized Worker path.
- Contract SHA-256 does not match the Foreman-provided value.
- Any package needs a seventh standard reviewer, a larger budget, new public tool, new
  role, fuzzy risk inference, legal-advice behavior or schema beyond 2.5.
- A non-legal accepted portfolio changes or the standard deep path exceeds 13.
- Old records cannot be read conservatively or routing provenance requires user/model
  prose.
- Required work touches a forbidden path, raw live record or protected user asset.
- Lock regeneration produces drift beyond the exact root version change.
- A required test/build/smoke cannot be completed without new dependency, credential,
  live provider, push, PR, release or deployment authority.

## Handoff

Write the specified ledger and Campaign Worker report. Leave both untracked and unstaged.
In chat, start with exactly one terminal status, `READY_FOR_REVIEW` or `BLOCKED`, then
summarize report and ledger paths, baseline/final HEAD, six commits/files, package and
Campaign verification, artifacts, skipped checks, subagent/authority/dependency/live-call
counts and remaining risks or blockers. Stop after that handoff. Do not claim Campaign,
feature, publication or Q-013 acceptance.
