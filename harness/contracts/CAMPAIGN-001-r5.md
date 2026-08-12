# Work Order: CAMPAIGN-001-r5

## Control

- Role: WORKER
- Mode: STRICT_SEQUENTIAL
- State: ASSIGNED
- Repository: `C:\Users\GeZhu\MyMCP\mcp-council-of-translation`
- Baseline commit: `6978c7b76cf7cb8868405a92e05b831deb9e4a09`
- Baseline verification: Foreman resolved this exact object as a `commit`; subject `Harden reviewer influence and coverage`
- Prior contract/review: `harness/contracts/CAMPAIGN-001-r4.md`, `harness/evaluations/CAMPAIGN-001-r4-review.md`
- Dirty files to preserve: audit markdown, `reviews/`, `myTest/` if it appears, `.learnings/`, and every Foreman-owned `harness/` asset except the authorized report below
- Worker report path: `harness/reports/CAMPAIGN-001-r5-worker.md`
- Commit policy: required; scoped local commit(s), no push
- Subagent policy: no subagents; this is one narrow parser/coverage correction

## Goal

Close the remaining reviewer-envelope integrity gap: syntactically valid but semantically malformed reviewer JSON must never count as successful clean coverage or escape as an uncaught validation exception.

## Context

Read the r4 Foreman review completely. Preserve both passing r4 repairs and every earlier passing behavior. Do not redesign influence normalization, role prompts, Position Matrix policy, interaction, persistence, public tools, budgets, providers, or the Council workflow.

## Scope

### Allowed files or boundaries

- `src/council_of_translation/localization/orchestration.py` for bounded reviewer-envelope/finding validation, coverage accounting, and normalized telemetry
- `src/council_of_translation/localization/models.py` only if a minimal internal validation/result type is demonstrably necessary
- focused tests under `tests/integration/**` and `tests/unit/**`
- `README.md`, `docs/v0.4-architecture.md`, `docs/v0.4-tool-contract.md`, and `AGENTS.md` only to make the demonstrated semantic validation policy precise
- `harness/reports/CAMPAIGN-001-r5-worker.md`

### Forbidden files or boundaries

- All other production modules, public tool names/arguments, dependencies, versions, diagnostic build, defaults, budgets, DecisionPoint limits, provider/Goose integration, or custom UI
- Retry/repair sampling, extra model calls, prompt redesign, majority voting, translation/file editing, or broad refactors
- Changes to r4 role-influence normalization except tests proving it remains intact
- Protected user/Harness assets, prior reports/evaluations/contracts, push/PR/release/deployment/credentials

### Non-goals

- Recovering malformed reviewer payloads through another model call.
- Live-provider tuning.
- Redesigning general Pydantic normalization outside the independent-review response boundary.

## Required semantic policy

- A reviewer sample is a structured success only when its decoded object contains both envelope keys: `role_feedback` is a string and `findings` is a list. A missing key or wrong container type is malformed.
- `findings: []` is valid zero-finding coverage only with non-whitespace `role_feedback`; do not require a finding to manufacture proof of work. An empty `role_feedback` is acceptable only when at least one valid finding remains.
- Missing `findings`, non-list `findings`, non-object entries, or entries that cannot be safely validated are malformed reviewer samples, not clean reviews.
- No Pydantic/model-output validation exception may escape the reviewer loop.
- A malformed sample contributes zero successful-reviewer coverage. It must produce bounded parse/fallback provenance and use the existing `partial`/`none` conservative disposition without adding calls.
- If valid findings precede a malformed entry, choose and document one deterministic conservative policy: either discard the sample's findings or retain only validated findings as advisory evidence while still marking the sample unavailable. In either case, malformed content cannot create blockers/hard rules or successful coverage.

## Acceptance criteria

1. Six `{}` reviewer responses result in `NEEDS_HUMAN_REVIEW`, `需人工复核/是`, coverage `none`, zero successful reviewers, six unavailable reviewers, and explicit bounded schema-failure provenance.
2. Missing `findings`, `findings: null`, string/object `findings`, scalar/null/list entries, and inert empty finding objects do not count as successful coverage or clean review.
3. Uncoercible fields such as `confidence: "abc"`, invalid container types such as scalar `rule_refs`, and other Pydantic validation failures never escape the Core workflow; they follow the same conservative unavailable policy.
4. One semantically malformed reviewer among otherwise valid structured reviewers produces `partial` coverage and the existing conservative human-review disposition, with no extra sampling calls.
5. Six valid structured zero-finding responses remain `COMPLETED`, `可发布/否`, full coverage, six successes, no manufactured issues/discussion/DecisionPoints, and no fallback.
6. Valid findings continue to normalize conservatively, remain model-origin/advisory/non-blocking, and participate in clustering and policy exactly as before.
7. Invalid JSON, runtime malformed/reasoning-only, empty text, and transport errors retain the r4 unavailable behavior and bounded telemetry.
8. Continuation preserves parent partial/none coverage and cannot clear human review.
9. The r4 one-versus-five duplicate-position scores and selection remain identical; all finding IDs remain in full trace.
10. All 99 existing tests, exact five tools, version/build, review-only boundary, V1/metadata privacy, persistence errors, option/form/discussion/reconsideration paths, continuation, and 6/10/14 budgets remain green.
11. Documentation distinguishes syntactic JSON decoding from a semantically valid reviewer envelope and makes no live Goose/provider claim.

## Required verification

```powershell
python -m compileall src tests
```

```powershell
.venv\Scripts\python.exe -m pytest -q --basetemp .tmp\campaign001-r5-pytest -p no:cacheprovider
```

Also record production-Core evidence for:

- all-six `{}`;
- missing/non-list/null `findings`;
- scalar/null/inert finding entries;
- an uncoercible confidence and invalid `rule_refs` container;
- one malformed plus otherwise valid samples;
- all-valid structured zero-finding control;
- r4 duplicate influence counterexample;
- exact compact/full coverage provenance, statuses, dispositions, sampling calls, and parse/fallback counts;
- exact five-tool/version/budget introspection;
- `git diff --check 6978c7b76cf7cb8868405a92e05b831deb9e4a09..HEAD`, changed-file list, complete diff inspection, and protected hashes.

The known uv build/cache limitation may reuse the disclosed r1/r3 evidence because r5 cannot change package structure or dependencies. Live Goose/model calls are optional only if already configured; disclose exact count.

## Required evidence

- Exact commands, exits, test counts, baseline/final SHA, commits, files, and clean status.
- Before/after outputs for the malformed-envelope counterexamples.
- Test-to-criterion map and preserved-r4 regression statement.
- Protected assets, escalation, subagent, external mutation, and live-call counts.

## Stop conditions

- Baseline/protected state differs.
- A correction requires retry calls, prompt/provider changes, a public-surface change, dependencies, or any forbidden boundary.
- Semantically valid zero-finding coverage cannot be preserved without a product decision.

## Handoff

Write `harness/reports/CAMPAIGN-001-r5-worker.md`. In chat, start with `READY_FOR_REVIEW` or `BLOCKED`, then report paths, baseline/final commits, files, verification/skips, counts, and risks. Stop. Do not push, mark acceptance, or claim completion.
