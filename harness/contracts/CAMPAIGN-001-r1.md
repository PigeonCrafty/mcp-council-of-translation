# Campaign Contract: CAMPAIGN-001-r1

## Control

- Role: WORKER / MAIN WORKER
- Assigned worker platform: Codex in a separate new conversation from the Foreman
- Mode: STRICT_CAMPAIGN
- State: ASSIGNED
- Repository: `C:\Users\GeZhu\MyMCP\mcp-council-of-translation`
- Baseline commit: `34d41946717f1993b8954260afc893737198a3bb`
- Dirty files to preserve: `mcp-council-of-translation-audit-and-upgrade-recommendations.md`, `reviews/`, `.learnings/`, Foreman control assets under `harness/` except the authorized report and ledger paths
- Execution ledger path: `harness/reports/CAMPAIGN-001-r1-ledger.md`
- Campaign Worker report path: `harness/reports/CAMPAIGN-001-r1-worker.md`
- Commit policy: required; create scoped local commits, do not push
- Worktree strategy: shared worktree only for this revision; isolated worktrees are forbidden because Foreman control assets are part of the protected dirty baseline
- Subagent delegation: allowed only for the packages below
- Parallel delegation: allowed only for read-only analysis or disjoint implementation boundaries explicitly marked parallel-safe

## Campaign outcome

Deliver Council of Translation V0.4 as a Goose-first, review-only structured deliberation system with deterministic preflight, executable roles, issue-centric bounded discussion, default user decisions, safe fallback adjudication, targeted reconsideration, compact output, full trace persistence, V1 record reading, and evidence-backed tests and documentation.

## Context

The V0.3 workflow performs independent sequential role sampling, heuristic conflict detection, optional coordinator review, chief-editor synthesis, and relative-path JSON persistence. The approved V0.4 design is frozen in `harness/plan.md`; machine-readable acceptance truth is `harness/features.json`; current state is `harness/progress.md`.

Read all three files, `AGENTS.md`, the independent audit report, and this contract before changing production files. Conversation history is not required and does not override these artifacts.

This Campaign is assigned to a new Codex conversation. Do not assume access to the Foreman's chat context, transient plans, or tool outputs; reconstruct the assignment only from repository artifacts and fresh baseline inspection.

## Frozen design

### Architecture and invariants

- Preserve the review-only boundary and existing output-mode rules.
- Use the state machine, public tool surface, data contracts, runtime abstraction, persistence rules, budgets, and non-goals from `harness/plan.md`.
- Internal V2 domain and persisted models use Pydantic v2 with conservative normalization at model-output boundaries.
- Council Core depends on `ModelExecutor` and `UserInteractionGateway`, not FastMCP Context.
- Hard constraints originate only from caller inputs, explicit project/TB/SG packets, deterministic preflight, and explicit confirmed policy overrides.
- LLM reviewer or discussion output is untrusted evidence and cannot create deterministic blockers.
- Default user authority is `decisive_within_valid_options`.
- No literal majority voting. Fallback is Position Matrix plus Policy Gate plus chief-editor adjudication.
- At most one targeted discussion round and three batched DecisionPoints.
- Full structured trace is persisted by default; normal tool response remains compact.
- Full traces contain no hidden chain-of-thought.
- Continuations create immutable linked revisions.
- New writes use stable configurable user storage and atomic writes; legacy working-directory records remain readable.

### Shared interfaces and data contracts

- Implement the contracts under `Shared data contracts` in `harness/plan.md`.
- `review_translation` adds or normalizes at least: `interactive_mode`, `decision_fallback`, `trace_level`, and `history_mode` while preserving required source/candidate inputs.
- `continue_review` accepts a review ID and structured user decisions, loads the parent, validates choices against active DecisionPoints, runs only required reconsideration/policy/adjudication steps, and writes a new linked record.
- `view_review_record` supports V1/V2 and an explicit detail level without returning a false success for malformed records.
- Runtime metadata reports sampling calls, elicitation calls/actions, parse failures, fallbacks, elapsed time, and version identifiers.
- Project version becomes `0.4.0`; diagnostic build becomes `structured-deliberation-v2` only when the integrated contract is actually implemented.

### Main Worker implementation discretion

- Exact module and class names within the suggested source layout.
- Whether V1 compatibility uses adapters or discriminated model parsing.
- Exact prompt wording, provided role boundaries, structured output contracts, security delimiters, and acceptance behavior remain intact.
- Exact deterministic placeholder regexes and parsers, provided false-positive regression cases exist.
- Exact Position Matrix representation, provided it is not raw majority voting and preserves evidence hierarchy.
- Subagent count and package assignment within the authority rules.
- Number and grouping of scoped local commits.

### Decisions reserved for Foreman or user

- Adding public MCP tools beyond `continue_review`.
- Restoring literal majority voting.
- Changing the review-only product boundary.
- Increasing model-call or DecisionPoint budgets.
- Adding a custom MCP App/UI.
- Removing V1 record reading.
- Changing default user authority, interactive mode, trace level, or history mode.
- Adding external MCP integrations, provider/model routing, or translation editing.
- Pushing branches, opening PRs, releases, deployments, destructive cleanup, or changing external Goose installations.

## Global boundaries

### Allowed files, directories, or systems

- `src/council_of_translation/**`
- `tests/**`
- `docs/**`
- `README.md`
- `AGENTS.md` only for concise authoritative V0.4 operational updates after implementation
- `pyproject.toml`, `uv.lock`
- obsolete legacy source files listed in the audit, but only in PKG-010 after dependency and test migration
- `harness/reports/CAMPAIGN-001-r1-ledger.md`
- `harness/reports/CAMPAIGN-001-r1-worker.md`

### Forbidden files, directories, or systems

- `mcp-council-of-translation-audit-and-upgrade-recommendations.md`
- `reviews/**`
- `myTest/**`
- `.learnings/**`
- Foreman-owned `harness/plan.md`, `harness/features.json`, `harness/progress.md`, `harness/contracts/**`, and `harness/evaluations/**`
- Goose source/installations outside this repository
- GitHub, releases, package registries, deployments, or external services except read-only documentation lookup

### Non-goals

- All non-goals in `harness/plan.md`.
- Opportunistic formatting, renaming, dependency upgrades, or refactors unrelated to V0.4.
- Live translation quality tuning beyond the accepted corpus and bounded Goose validation.
- Self-acceptance or marking `features.json` complete.

### Authorized external or destructive actions

- No push, PR, release, deployment, external mutation, or deletion of user data.
- Scoped deletion of obsolete tracked legacy code is authorized only in PKG-010 after tests/imports prove it is unused and replacement security coverage exists.
- Dependency resolution and read-only official documentation lookup are allowed when required; record network calls and lockfile changes.
- Up to four live Goose review workflows are authorized for final integration validation if credentials/configuration already exist. Do not expose secrets. Record provider/model, mode, call count, record ID, outcome, and any skipped live checks.

## Task graph

| Package | Observable outcome | Depends on | Allowed boundary | Acceptance and verification | Parallel-safe |
| --- | --- | --- | --- | --- | --- |
| PKG-001 | V2 models and V1 compatibility foundation | none | localization model/schema/compatibility modules, focused tests, direct model dependency | Validate all frozen data contracts; V1 fixture parses; invalid LLM values fall back safely; no blocker escalation | no; freezes shared interfaces |
| PKG-002 | Stable IDs, diagnostics and full/metadata/off persistence | PKG-001 | persistence, security, review history tools, focused tests | Atomic temp-dir tests; collision test; legacy ID/path read; metadata redaction; no writes to real user directory | yes after PKG-001; do not edit shared orchestration |
| PKG-003 | Executable RoleDefinition and deterministic CouncilPlan | PKG-001 | roles, role prompts, package-specific tests/docs | Role scope/evidence/blockers validate; chief is adjudicator; mode/content plans tested | yes after PKG-001 |
| PKG-004 | Runtime interfaces and FastMCP/test adapters | PKG-001 | runtime module and package-specific tests | Sampling and elicitation success/error/unsupported/decline/cancel are scripted and normalized; Core interface contains no FastMCP type | yes after PKG-001 |
| PKG-005 | Conservative deterministic preflight | PKG-001 | preflight module and package-specific corpus/tests | Required technical checks and false-positive warnings pass; sampled text cannot create blocker | yes after PKG-001 |
| PKG-006 | General issue normalization and clustering | PKG-001, PKG-005 | clustering module and package-specific tests | Remove production named-keyword conflict rules; same/different issue regression cases; immutable constraint propagation | no; consume frozen findings/preflight |
| PKG-007 | Bounded targeted discussion and Position Matrix | PKG-003, PKG-004, PKG-006 | deliberation prompts/module and focused tests | Relevant roles only; no-conflict skip; structured trace; one round; mode budgets; no hidden reasoning | no |
| PKG-008 | Policy Gate, chief adjudication, compact response and full trace | PKG-001, PKG-005, PKG-006, PKG-007 | policy/adjudication/orchestration and focused tests | Invalid options excluded; no raw majority; traceable decisions; compact summary; full retrievable record; conservative fallbacks | no; Main Worker owns shared integration files |
| PKG-009 | Default interaction, continuation and affected-role reconsideration | PKG-002, PKG-004, PKG-007, PKG-008 | review tools, interaction/reconsideration modules, focused integration tests | Auto/default, one form/up to three points, decisive valid user choice, fallback/pending, immutable continuation, affected roles only | no; Main Worker owns public tool surface |
| PKG-010 | Integrated validation, docs, migration and legacy removal | PKG-002 through PKG-009 | tests, golden corpus, authoritative docs, obsolete tracked legacy files | Full quality gates; exact tool list; no dead imports; old useful security tests migrated; live Goose checks within authority; repo hygiene clean except protected files | no |

## Collision and integration map

| Packages/files at risk | Required sequencing or isolation | Integration owner/check |
| --- | --- | --- |
| Shared V2 model definitions | PKG-001 completes before dependent implementation | Main Worker verifies every dependent import and schema test |
| `workflow.py` / orchestration | Main Worker exclusively integrates PKG-006 through PKG-009; subagents must not concurrently edit it | Baseline-to-final diff plus integration tests |
| `tools/review.py`, server instructions and public schemas | Main Worker exclusively integrates PKG-008/009/010 | Tool introspection and Goose calls |
| `prompt_builders.py` | Sequence role, discussion and adjudication changes or use isolated worktrees | Prompt contract tests and security delimiter inspection |
| Existing monolithic unit test file | New package tests should use separate files; Main Worker reconciles necessary shared edits | Full test suite and changed-file review |
| `pyproject.toml` / `uv.lock` | Main Worker owns dependency changes after model/runtime choice is final | Lock consistency and clean install/test |
| Legacy deletion and security tests | PKG-010 only after replacement persistence/security tests pass | Import scan, compile, full tests |

## Campaign acceptance criteria

1. Every `F-001` through `F-010` criterion has concrete evidence in the Worker report, without being marked accepted.
2. Every `Q-001` through `Q-006` quality gate is implemented and evidenced or the Worker returns `BLOCKED`.
3. The default Goose path performs independent review, issue clustering, bounded discussion, one batched user interaction when warranted, targeted reconsideration, policy gating, and chief adjudication.
4. A clean translation does not manufacture conflict, discussion, DecisionPoints, or excess sampling.
5. A missing placeholder remains blocked even when the user prefers the invalid option or multiple roles support it.
6. A user choice among valid alternatives is decisive and traceable.
7. Unsupported, declined, cancelled, malformed, and non-interactive elicitation paths terminate safely and explicitly.
8. `continue_review` creates a linked immutable revision and does not rerun unaffected roles.
9. Default output is compact enough for Goose while the full structured trace is available from history.
10. V1 records remain readable, V2 persistence honors privacy modes, and tests never write to the user's real review directory.
11. Model-call budgets and at-most-three DecisionPoints are enforced and recorded.
12. No unrestricted reasoning/chain-of-thought, secret, or sensitive metadata is introduced into output, logs, fixtures, or commits.
13. The public MCP surface contains only the five frozen normal tools, and docs match actual behavior.
14. All relevant automated checks pass on the integrated tree, with pre-existing warnings separated from failures.
15. Protected user files remain unmodified and excluded from commits.

## Required Campaign verification

Run fresh on the integrated state and record exact output/exit status:

```powershell
python -m compileall src tests
```

```powershell
$env:PYTHONPATH='src'; python -m pytest -q
```

If pytest cannot run, execute the AGENTS.md lightweight harness and explicitly record the coverage gap. Also run:

- package/build metadata verification for version `0.4.0`;
- MCP tool introspection proving the exact public tool surface;
- temp-directory persistence and V1/V2 fixture tests;
- call-budget assertions for lightweight, standard and strict;
- at least one full mocked interactive workflow and one fallback workflow;
- import/dead-reference scan after legacy deletion;
- up to four authorized live Goose workflows when practical: at minimum one interactive acceptance and one unsupported/decline/fallback path, with no secrets captured.

## Delegation protocol

- Main Worker may create subagents only for listed packages and within their boundaries.
- Give each subagent a bounded assignment; do not delegate acceptance authority.
- Do not concurrently edit overlapping files in one worktree.
- PKG-002, PKG-003, PKG-004 and PKG-005 may run in parallel only after PKG-001 interfaces are integrated, only with disjoint files/tests, and only in the shared worktree without overlapping edits.
- Main Worker exclusively owns shared orchestration, public tool registration, dependency/lock changes, final docs reconciliation, legacy deletion, and integration commits.
- Inspect every returned diff and rerun package checks on the integrated state.
- Record delegation, result, integration, verification and blockers in the ledger.
- Main Worker remains accountable for the final diff, combined behavior and report.

## Required evidence

- Package-to-subagent/files/commits/verification matrix.
- Exact command results and exit status.
- Baseline-to-final changed-file list and complete Main Worker diff inspection.
- Model-call and elicitation counts for mocked and live workflows.
- Representative compact response and corresponding full persisted trace, sanitized of user secrets.
- V1/V2 persistence fixtures and metadata-redaction evidence.
- Deviations, conflict resolutions, skipped checks and consequences.
- Fresh Campaign-level integration evidence.

## Stop conditions

- Baseline or protected changes differ from this contract.
- A frozen design, interface, dependency or ownership assumption is false.
- Goose/FastMCP cannot support the required default interaction plus fallback without a public contract change.
- Correctness requires literal majority voting, more public tools, larger budgets, custom UI, or removal of the review-only boundary.
- Work requires credential changes, pushes, PRs, releases, deployments, destructive user-data changes, or unapproved external mutation.
- Required behavior cannot be integrated or verified within the contract.
- A Worker believes compatibility demands weakening a V2 feature; stop and report the exact trade-off rather than silently preserving V1.

## Handoff

Write the specified ledger and Campaign Worker report. In chat, start with exactly one terminal status, `READY_FOR_REVIEW` or `BLOCKED`, then summarize report and ledger paths, baseline/final state, commits/files, package and Campaign verification, skipped checks, subagent/authority/live-call counts, and remaining risks or blockers. Stop after that handoff. Do not return only the status word. Do not mark features accepted or claim project completion.
