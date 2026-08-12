# Work Order: CAMPAIGN-001-r3

## Control

- Role: WORKER
- Mode: STRICT_SEQUENTIAL
- State: ASSIGNED
- Repository: `C:\Users\GeZhu\MyMCP\mcp-council-of-translation`
- Baseline commit: `8a2531e91a42a1523e83d374b84553907a5e3e94`
- Baseline verification: this exact object was resolved by the Foreman as a `commit`; subject `Normalize V0.4 source endings`
- Supersedes: `harness/contracts/CAMPAIGN-001-r2.md` only because its full SHA was transcribed incorrectly
- Prior reviews: `harness/evaluations/CAMPAIGN-001-r1-review.md`, `harness/evaluations/CAMPAIGN-001-r2-review.md`
- Dirty files to preserve: the audit markdown, `reviews/`, `myTest/`, `.learnings/`, and all Foreman-owned `harness/` assets except the authorized report path below
- Worker report path: `harness/reports/CAMPAIGN-001-r3-worker.md`
- Commit policy: required; create scoped local commit(s), do not push
- Subagent policy: no implementation subagents

## Goal

Make the integrated V0.4 interaction, deliberation, adjudication, compact-result, telemetry, and metadata paths genuinely usable without changing the frozen product boundary or public surface.

## Context

Read both prior Foreman reviews completely. The r2 Worker made no implementation changes; this r3 scope is technically identical to r2 and changes only the verified Git baseline and artifact revision. Preserve all r1 evidence for unaffected packages.

The defects to correct are: production Position/DecisionPoint option-ID divergence; an opaque unconstrained elicitation form; discussion changes not applied to the Position Matrix; incomplete provenance/tier use in adjudication; opaque chief results; metadata disposition loss; stale active sample-budget metadata; and unnormalized persistence I/O failures.

## Scope

### Allowed files or boundaries

- `src/council_of_translation/localization/models.py`
- `src/council_of_translation/localization/clustering.py`
- `src/council_of_translation/localization/deliberation.py`
- `src/council_of_translation/localization/policy.py`
- `src/council_of_translation/localization/orchestration.py`
- `src/council_of_translation/localization/persistence.py`
- `src/council_of_translation/localization/runtime.py`
- `src/council_of_translation/localization/prompt_builders.py` only for corrected structured discussion/reconsideration contracts
- `src/council_of_translation/tools/review.py` only for aligned compact output and error behavior
- focused files under `tests/unit/**` and `tests/integration/**`
- `README.md`, `docs/v0.4-architecture.md`, `docs/v0.4-tool-contract.md`, and `AGENTS.md` only to align demonstrated behavior
- `harness/reports/CAMPAIGN-001-r3-worker.md`

### Forbidden files or boundaries

- Public tools beyond the frozen five, or renamed tools/arguments
- Version, diagnostic build, default interaction/fallback/trace/history modes, 6/10/14 sampling budgets, or three-DecisionPoint limit
- Translation/file editing, majority voting, custom MCP UI, provider routing, external integrations, or unrelated refactors
- Audit, `reviews/`, `myTest/`, `.learnings/`, prior reports/ledger, and Foreman-owned plan/features/progress/contracts/evaluations
- Goose installation/configuration, credentials, GitHub, push, PR, release, deployment, or publication

### Non-goals

- Rewriting passing roles, preflight, compatibility, or server structure.
- General translation-quality tuning unrelated to failed r1 criteria.
- Live-provider work when credentials are unavailable.

## Acceptance criteria

1. One authoritative deterministic option identity is used from `IssueCluster.positions` and candidate actions through DecisionPoint, discussion, reconsideration, Policy Gate, chief decision, and trace. Production DecisionPoint options match their intended Positions.
2. Unsupported, declined, cancelled, and `interactive_mode=off` default `council_adjudication` workflows select a valid non-tied option through the Position Matrix, return `COMPLETED_WITH_FALLBACK`, and record the basis. A genuine tie/insufficient evidence still requires human review; `return_pending` remains unchanged.
3. The generated Pydantic/FastMCP form schema gives every point a readable question/option description and an enum restricted to valid option IDs. The single batched message maps IDs to readable labels/descriptions. Invalid or missing accepted data degrades safely.
4. A valid `position_changed=true` discussion turn may update only its allowed issue and participant role to an existing valid candidate option. Invalid issue/speaker/option or blocker/hard-constraint escalation is ignored. The updated matrix is consumed downstream and remains traceable.
5. Position Matrix adjudication observably consumes role relevance, evidence/provenance, constraint tier, blocking state, and confidence without raw majority voting. Model-origin data still cannot manufacture a hard constraint or deterministic blocker.
6. User choices remain decisive only among valid options and cannot erase deterministic blockers. DecisionTrace distinguishes valid user choice, Council fallback, and human-review outcomes without hidden reasoning.
7. Compact chief output resolves internal option IDs to user-facing actions, populates applicable terminology/conflict/checklist sections, and concisely summarizes the decision basis. Default `review_only` contains no `suggested_translation` and makes no edit claim.
8. Metadata history preserves true safe `status`, `publishability`, and `review_needed` values on reload/list while redacting source, candidate, TB/SG/rules, model prose, user free text, chief prose, and secrets.
9. Persistence write/replace failures are normalized under `ReviewPersistenceError` at the public boundary without leaking raw host paths or uncaught storage errors.
10. Runtime metadata records the active plan's exact budget for lightweight, standard, strict, and continuation paths; all call, elicitation, parse-failure, fallback, and latency counters remain bounded.
11. Supported DeepSeek-compatible sampling remains intact: FastMCP text-bearing results and raw JSON strings parse; malformed, reasoning-only, or empty content degrades conservatively. Do not add dependency on unsupported repr-only objects.
12. Exact five-tool introspection, version `0.4.0`, build `structured-deliberation-v2`, V1 reading, continuation immutability, history privacy modes, preflight blockers, clean-review skip behavior, review-only output, and 6/10/14 budgets remain green.
13. Authoritative docs describe only production-path-tested behavior; no fallback, evidence-hierarchy, or form-choice claim may rely only on hand-built unit objects.

## Required verification

```powershell
python -m compileall src tests
```

```powershell
.venv\Scripts\python.exe -m pytest -q --basetemp .tmp\campaign001-r3-pytest -p no:cacheprovider
```

Also record:

- a production-path regression proving Position/DecisionPoint ID intersection and expected non-tied unsupported fallback selection;
- `model_json_schema()` evidence for field descriptions and option enums, plus FastMCP 2.13 schema conversion when available;
- valid/rejected discussion before/after Position Matrix evidence;
- injected-temp full/metadata/off storage and exact disposition round trips;
- exact five-tool/version introspection;
- call/elicitation counts for clean, interactive accept, unsupported fallback, genuine tie, return pending, and continuation;
- `git diff --check 8a2531e91a42a1523e83d374b84553907a5e3e94..HEAD`, final changed-file list, and complete diff inspection;
- build verification when the existing environment permits it. If the known uv cache permission defect recurs, record it and preserve r1 build evidence without altering user cache permissions.

Live Goose/model execution is optional only if already configured. Disclose the exact live-call count, including zero.

## Required evidence

- Exact command results and exit statuses.
- Baseline/final commits, scoped commits, final status, and changed-file list.
- Before/after evidence for every failed r1 counterexample.
- Test names mapped to acceptance criteria.
- Protected asset and prior-report integrity confirmation.
- Authority escalation, external mutation, subagent, and live-model counts.

## Stop conditions

- Observed HEAD is not exactly `8a2531e91a42a1523e83d374b84553907a5e3e94` before edits, or protected state differs unexpectedly.
- Correct form elicitation requires a custom UI, new public tool, or client patch.
- Correct adjudication requires majority voting, higher budgets, weaker blockers, or changed user authority.
- Work requires credentials, Goose installation changes, push/PR/release, or any forbidden boundary.
- A frozen design assumption cannot be corrected within the authorized files.

## Handoff

Write `harness/reports/CAMPAIGN-001-r3-worker.md`. In chat, start with exactly one terminal status, `READY_FOR_REVIEW` or `BLOCKED`, then summarize report path, baseline/final state, commits/files, verification and skipped checks, authority/live-call/subagent counts, and remaining risks or blockers. Stop after that handoff. Do not mark features accepted or claim Campaign/project completion.
