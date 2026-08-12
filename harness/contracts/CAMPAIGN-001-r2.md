# Work Order: CAMPAIGN-001-r2

## Control

- Role: WORKER
- Mode: STRICT_SEQUENTIAL
- State: ASSIGNED
- Repository: `C:\Users\GeZhu\MyMCP\mcp-council-of-translation`
- Baseline commit: `8a2531e91fe3f823449b0fd1e8a0eef7fd857890`
- Prior contract/review: `harness/contracts/CAMPAIGN-001-r1.md`, `harness/evaluations/CAMPAIGN-001-r1-review.md`
- Dirty files to preserve: the audit markdown, `reviews/`, `myTest/`, `.learnings/`, and all Foreman-owned `harness/` assets except the authorized report path below
- Worker report path: `harness/reports/CAMPAIGN-001-r2-worker.md`
- Commit policy: required; create scoped local commit(s), do not push
- Subagent policy: no implementation subagents; this is a bounded correction revision

## Goal

Make the integrated V0.4 interaction/deliberation/adjudication path genuinely usable: a human can see and select valid options in one Goose/FastMCP form, discussions can safely update affected positions, non-interactive fallback can adjudicate a non-tied Position Matrix, the compact chief result is actionable, and metadata history preserves its true safe disposition.

## Context

The r1 structure and most foundation packages are preserved. Read the r1 Foreman review completely before editing. The primary defects are production option-ID divergence, an unconstrained/opaque elicitation schema, trace-only discussion changes, incomplete evidence/tier use in policy, opaque chief output, and metadata disposition loss. The exact five-tool surface, version/build identifiers, review-only boundary, defaults, budgets, V1 reading, and privacy guarantees are frozen.

## Scope

### Allowed files or boundaries

- `src/council_of_translation/localization/models.py`
- `src/council_of_translation/localization/clustering.py`
- `src/council_of_translation/localization/deliberation.py`
- `src/council_of_translation/localization/policy.py`
- `src/council_of_translation/localization/orchestration.py`
- `src/council_of_translation/localization/persistence.py`
- `src/council_of_translation/localization/runtime.py`
- `src/council_of_translation/localization/prompt_builders.py` only when required for the corrected structured discussion contract
- `src/council_of_translation/tools/review.py` only for aligned compact/tool error behavior
- focused files under `tests/unit/**` and `tests/integration/**`
- `README.md`, `docs/v0.4-architecture.md`, `docs/v0.4-tool-contract.md`, and `AGENTS.md` only to align authoritative behavior after implementation
- `harness/reports/CAMPAIGN-001-r2-worker.md`

### Forbidden files or boundaries

- Public tools beyond the frozen five, or any renamed tool/argument without stopping
- Version, diagnostic build, default interaction/fallback/trace/history modes, 6/10/14 sampling budgets, or three-DecisionPoint limit
- Translation/file editing, majority voting, custom MCP UI, provider routing, or external integrations
- Audit, `reviews/`, `myTest/`, `.learnings/`, r1 report/ledger, Foreman plan/features/progress/contracts/evaluations
- Goose installation/configuration, credentials, GitHub, push, PR, release, deployment, or package publication

### Non-goals

- Rewriting already-passing roles, preflight, compatibility, or public server structure.
- General translation-quality prompt tuning unrelated to the failed criteria.
- Preserving opaque internal option IDs in user-facing summaries.
- Adding live-provider requirements when credentials are unavailable.

## Acceptance criteria

1. One authoritative deterministic option-ID function/representation is used from `IssueCluster.positions` and candidate actions through `DecisionPoint`, discussion/reconsideration, Policy Gate, chief decision, and trace. Every production DecisionPoint option has the intended matching Position(s).
2. A non-interactive/unsupported/declined/cancelled default `council_adjudication` workflow with unequal valid evidence selects a valid option through the Position Matrix, returns `COMPLETED_WITH_FALLBACK`, and records the basis. A genuine evidence tie or insufficient evidence still returns human review. `return_pending` remains unchanged.
3. The dynamically generated Pydantic/FastMCP form schema contains, for every point, a readable question/option description and an enum limited to valid option IDs. The batched elicitation message also gives the user a readable mapping from IDs to labels/descriptions. Invalid/missing accepted form data normalizes safely.
4. A valid discussion turn with `position_changed=true` can update only the declared allowed issue and participant role, and only to an existing valid candidate action/option. Invalid speakers, issues, options, or attempts to create blockers/hard constraints are ignored. The updated matrix is used downstream and the structured turn remains traceable.
5. Position Matrix adjudication observably consumes role relevance, evidence/provenance, constraint tier, blocking state, and confidence without raw majority voting. Model-origin output remains unable to manufacture a hard constraint or deterministic blocker. Add focused precedence and tie regressions.
6. User choices remain decisive only among valid options and cannot erase a deterministic blocker. DecisionTrace distinguishes valid user choice, Council fallback, and human-review outcomes without persisting hidden reasoning.
7. The compact chief result resolves selected option IDs to user-facing actions/labels, populates applicable checklist sections including terminology/conflict decisions, and summarizes the decision basis concisely. Default `review_only` still has no `suggested_translation`; no file-edit claim is introduced.
8. Metadata history preserves the true safe `status`, `publishability`, and `review_needed` values on reload/list while continuing to redact source, candidate, TB/SG/rules, model prose, user free text, chief prose, and other secrets.
9. Persistence write/replace failures are normalized under `ReviewPersistenceError` at the public boundary; no raw host path or uncaught storage exception is returned.
10. Runtime metadata records the active plan's exact sample budget in lightweight, standard, strict, and continuation paths. Sampling, elicitation, parse-failure, fallback, and latency behavior remains bounded.
11. Existing DeepSeek-compatible supported sampling remains intact: FastMCP text-bearing responses and raw string JSON both parse; malformed/reasoning-only/empty content degrades conservatively without contaminating findings. Do not depend on a repr-only object unless supported by the actual FastMCP interface.
12. Exact five-tool introspection, version `0.4.0`, build `structured-deliberation-v2`, V1 reading, continuation immutability, history privacy modes, preflight blockers, clean-review skip behavior, review-only output, and 6/10/14 budgets all remain green.
13. Authoritative docs describe only behavior demonstrated by production-path tests. No claim of fallback adjudication, evidence hierarchy, or form choice may rely solely on hand-constructed unit objects.

## Required verification

Run fresh with workspace-local temp roots:

```powershell
python -m compileall src tests
```

```powershell
.venv\Scripts\python.exe -m pytest -q --basetemp .tmp\campaign001-r2-pytest -p no:cacheprovider
```

Also record:

- focused regression proving production Position IDs intersect DecisionPoint IDs and a non-tied unsupported fallback selects the expected option;
- `model_json_schema()` evidence showing per-field descriptions and valid-option enums, plus FastMCP 2.13 schema conversion if available;
- discussion-before/after Position Matrix evidence for valid and rejected changes;
- metadata full/metadata/off and exact disposition round trips in injected temporary storage;
- exact five-tool/version introspection;
- call/elicitation counts for clean, interactive-accept, unsupported-fallback, genuine-tie, return-pending, and continuation paths;
- `git diff --check 8a2531e..HEAD`, final changed-file list, and full diff inspection;
- build verification when the existing environment permits it. If the known host uv cache permission error recurs, record it and rely on the preserved r1 build evidence; do not alter user cache permissions.

Live Goose/model execution is optional only if already configured and must not trigger credential or installation changes. Disclose exact live call count, including zero.

## Required evidence

- Exact command results and exit status.
- Baseline/final commits, scoped commit list, final status, and changed-file list.
- Before/after evidence for every failed r1 counterexample.
- Test names mapped to each acceptance criterion.
- Confirmation that protected assets and r1 reports remain unchanged.
- Authority escalation, external mutation, subagent, and live-model counts.

## Stop conditions

- Baseline/protected changes differ from this contract.
- Correct form elicitation requires a custom UI, additional public tool, or a client-specific patch.
- Correct adjudication requires majority voting, higher budgets, weakening deterministic blockers, or changing user authority.
- The corrections require provider credentials, Goose installation changes, push/PR/release, or any forbidden boundary.
- A frozen r1 design assumption is invalid and cannot be corrected within these files.

## Handoff

Write `harness/reports/CAMPAIGN-001-r2-worker.md`. In chat, start with exactly one terminal status, `READY_FOR_REVIEW` or `BLOCKED`, then summarize the report path, baseline/final state, commits/files, verification and skipped checks, authority/live-call/subagent counts, and remaining risks or blockers. Stop after that handoff. Do not mark features accepted or claim Campaign/project completion.
