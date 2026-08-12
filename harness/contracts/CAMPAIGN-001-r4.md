# Work Order: CAMPAIGN-001-r4

## Control

- Role: WORKER
- Mode: STRICT_SEQUENTIAL
- State: ASSIGNED
- Repository: `C:\Users\GeZhu\MyMCP\mcp-council-of-translation`
- Baseline commit: `d9eca22bd8c2d2cb040e51c5a1e469a292d3d2ea`
- Baseline verification: Foreman resolved this exact object as a `commit`; subject `Fix V0.4 deliberation and interaction paths`
- Prior contract/review: `harness/contracts/CAMPAIGN-001-r3.md`, `harness/evaluations/CAMPAIGN-001-r3-review.md`
- Dirty files to preserve: audit markdown, `reviews/`, `myTest/`, `.learnings/`, and every Foreman-owned `harness/` asset except the authorized report below
- Worker report path: `harness/reports/CAMPAIGN-001-r4-worker.md`
- Commit policy: required; scoped local commit(s), no push
- Subagent policy: no subagents; this is a narrow two-defect correction

## Goal

Close the final two untrusted-model integrity gaps: a reviewer cannot multiply its Position Matrix influence by repeating findings, and unavailable reviewer sampling can never masquerade as a clean publishable Council review.

## Context

Read the r3 Foreman review completely. Preserve all passing r3 behavior and evidence. Do not redesign option identity, form elicitation, discussion/reconsideration safety, chief output, persistence, public tools, budgets, or product defaults.

## Scope

### Allowed files or boundaries

- `src/council_of_translation/localization/clustering.py`
- `src/council_of_translation/localization/deliberation.py` and/or `policy.py` only for per-role Position normalization/scoring
- `src/council_of_translation/localization/models.py` only if a small structured coverage/normalization field is necessary
- `src/council_of_translation/localization/orchestration.py` for reviewer coverage and conservative final status
- focused tests under `tests/unit/**` and `tests/integration/**`
- `README.md`, `docs/v0.4-architecture.md`, `docs/v0.4-tool-contract.md`, and `AGENTS.md` only to align demonstrated coverage/fallback behavior
- `harness/reports/CAMPAIGN-001-r4-worker.md`

### Forbidden files or boundaries

- All other production modules, public tool names/arguments, dependencies, versions, diagnostic build, defaults, budgets, DecisionPoint limits, provider/Goose integration, or custom UI
- Majority voting, extra sampling/retry calls, translation/file editing, or broad refactors
- Protected user/Harness assets, prior reports/evaluations/contracts, push/PR/release/deployment/credentials

### Non-goals

- Live provider tuning or retry policy.
- Changing the eight reviewer roles or Council routing.
- Reworking already-accepted r3 features.

## Acceptance criteria

1. Within one issue, one reviewer has at most one unit of total Position Matrix influence. Repeating an identical finding one to five times must produce the same option scores and selection as one finding.
2. If one reviewer supplies multiple distinct candidate actions for the same issue, its fixed total role influence is normalized deterministically across those actions or conservatively treated as ambiguous; it must not receive multiple full role weights. Full findings remain available in trace even if matrix rows are normalized.
3. Cross-role evidence weighting still uses relevance, provenance, tier, blocking state, evidence/rule references, and confidence; a trusted stronger position can beat multiple weaker roles without literal majority voting. Genuine normalized ties still require human review.
4. Independent reviewer sampling coverage distinguishes structured successful responses (including valid JSON with zero findings) from transport error, empty/reasoning-only content, and JSON parse failure.
5. If zero active reviewers return a structured successful response, final output must be `NEEDS_HUMAN_REVIEW`, `publishability=需人工复核`, `review_needed=是`, with explicit bounded fallback/coverage provenance. It must not claim a clean Council review or include a suggested translation.
6. Partial reviewer unavailability is explicitly surfaced in compact/full output through bounded status/fallback/runtime metadata. It must not be silently indistinguishable from full Council coverage. Choose a deterministic documented partial-coverage policy without adding model calls; deterministic preflight blockers continue to dominate.
7. A fully successful clean review whose reviewers return valid structured JSON with no findings remains `COMPLETED`, does not manufacture issues/discussion/DecisionPoints, and is distinguishable from unavailable sampling.
8. Error, malformed, reasoning-only, empty-text, and invalid-JSON reviewer scenarios are production-path tested. Mixed success/failure and all-success controls are included.
9. The duplicate-position production counterexample from the r3 Foreman review is a regression test: five repeated fluency findings cannot overrule a higher-relevance terminology position merely through repetition.
10. All 90 existing tests, exact five tools, version/build, option/form/discussion/reconsideration behavior, review-only boundary, V1/metadata privacy, persistence errors, continuation, and 6/10/14 budgets remain green.
11. Docs state the reviewer-coverage policy and one-role influence normalization precisely, without claiming live Goose/provider verification.

## Required verification

```powershell
python -m compileall src tests
```

```powershell
.venv\Scripts\python.exe -m pytest -q --basetemp .tmp\campaign001-r4-pytest -p no:cacheprovider
```

Also record:

- production clustering→DecisionPoint→policy evidence comparing one versus five identical same-role findings;
- one-role/multiple-distinct-actions normalization evidence;
- full Core workflows for all structured-clean, all reasoning-only, all empty, all transport-error, all invalid-JSON, and mixed availability;
- exact compact/full coverage provenance and status/disposition for those workflows;
- exact five-tool/version/budget introspection;
- `git diff --check d9eca22bd8c2d2cb040e51c5a1e469a292d3d2ea..HEAD`, changed-file list, complete diff inspection, and protected hashes.

The known uv build/cache limitation may reuse the disclosed r1/r3 evidence because r4 must not alter package structure or dependencies. Live Goose/model calls are optional only if already configured; disclose exact count.

## Required evidence

- Exact commands, exits, test counts, baseline/final SHA, commits, files, and clean status.
- Before/after outputs for both r3 Foreman counterexamples.
- Test-to-criterion map and preserved-r3 regression statement.
- Protected assets, escalation, subagent, external mutation, and live-call counts.

## Stop conditions

- Baseline/protected state differs.
- A correction requires extra model calls, new public surface, changed user authority, majority voting, dependencies, provider work, or any forbidden boundary.
- Correct partial-coverage handling requires a product decision outside the deterministic conservative policy above.

## Handoff

Write `harness/reports/CAMPAIGN-001-r4-worker.md`. In chat, start with `READY_FOR_REVIEW` or `BLOCKED`, then report paths, baseline/final commits, files, verification/skips, counts, and risks. Stop. Do not push, mark acceptance, or claim completion.
