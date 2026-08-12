# Foreman Review: CAMPAIGN-002-r3

## Control

- Role: FOREMAN
- Mode: STRICT_SEQUENTIAL
- Decision: ACCEPTED
- Contract: `harness/contracts/CAMPAIGN-002-r3.md`
- Worker report: `harness/reports/CAMPAIGN-002-r3-worker.md`
- Reviewed baseline/final state: `f7a4f23865383d52dede37f95de091932918090c..ca3d24afdc8feaa65286b13c6118720809749436`
- Review date: 2026-08-12 Asia/Shanghai

## Scope and repository review

- Allowed-file compliance: passed; exactly 11 authorized production, test, and documentation files changed.
- Non-goal compliance: passed; no public surface, dependency, schema/version/build, budget, provider, persistence, role, voting, custom UI, or review-only boundary changed.
- User changes preserved: passed; every protected asset and the r3 contract matched its issued SHA-256 before Foreman-owned acceptance updates.
- Commit/worktree compliance: passed; one scoped local commit, `ca3d24a`, and an empty index. Existing protected Harness/user dirt remains unstaged.
- Subagent policy: passed; the Worker used zero subagents as required.
- External/destructive action compliance: passed; no live call, push, PR, release, deployment, credential, Goose, or destructive mutation occurred.
- Sensitive evidence hygiene: passed; suppression provenance is allowlisted, bounded, content-free, and omitted from metadata history.

## Acceptance review

| Criterion | Worker evidence | Foreman verification | Result |
| --- | --- | --- | --- |
| 1 | Omitted classification/action probes | Independent Core probe produced zero DecisionPoints and zero elicitation; action prose did not enter selectable cluster structures | PASS |
| 2 | Issue/invalid/incomplete choice cases | Production tests and independent probes cover issue, invalid/missing kind, empty, non-string, and overlong proposals | PASS |
| 3 | Mixed valid choice control | Unit coverage retains current/proposed outcomes and excludes issue/affirmation advice | PASS |
| 4 | V1/V2.0 compatibility | Full compatibility suite remains green; no compatibility parser was changed | PASS |
| 5 | Repeated-anchor provenance | Independent production probe persisted only issue ID, decision ID, and `ambiguous_candidate_anchor`; compact result was degraded fallback | PASS |
| 6 | Missing-anchor provenance | Independent production probe persisted `missing_candidate_anchor` with the same truthful warning/status behavior | PASS |
| 7 | Protected-token control | Independent `{count}`-loss probe produced normal Policy Gate invalidation without suppression warning or runtime degradation | PASS |
| 8 | Bounded/private provenance | New tests enforce reason allowlist, ID shape, deduplication, cap of eight, content-free serialization, and metadata omission | PASS |
| 9 | Accepted r1/r2 behavior | Full suite passed 159 tests; focused suite passed 36; readable form, policy, continuation, privacy, and tool-surface regressions remain green | PASS |
| 10 | Integrated gates | Compile, fresh sdist/wheel, isolated wheel install/smoke, diff check, changed-file scope, and protected hashes passed | PASS |

## Independent verification

| Command/workflow | Result | Evidence |
| --- | --- | --- |
| `python -m compileall src tests` | PASS | exit 0 |
| `.venv\Scripts\python.exe -m pytest -q --basetemp .tmp\foreman-c002-r3-full -p no:cacheprovider` | PASS | 159 passed in 1.71s |
| Required focused suite | PASS | 36 passed in 1.06s |
| Foreman production Core probes | PASS | action non-promotion, missing/ambiguous suppression, and protected-token control printed `FOREMAN_PROBES_OK COMPLETED` |
| Repository-local-cache `uv build` | PASS | fresh `0.5.0` sdist and wheel built |
| Fresh isolated wheel installation | PASS | 70 packages installed with FastMCP 3.4.7 |
| Installed-wheel introspection | PASS | package/module `0.5.0`, build `outcome-first-decision-v3`, schema `2.1`, exactly the five expected tools, budgets 6/10/14 |
| `git diff --check f7a4f238..HEAD` | PASS | exit 0 |
| Protected-hash audit | PASS | all 14 issued hashes matched before acceptance-state edits |

The first isolated-venv attempt hit the known global uv-cache permission defect and passed after selecting a repository-local cache. Two initial smoke assertions also targeted non-contract implementation details: a non-public schema constant location and tool registration order. The corrected smoke checked the public server-info contract and exact five-tool set and passed. These were Foreman harness corrections, not product defects.

## Findings

No acceptance-blocking production finding remains.

## Preserved evidence

- All accepted r1/r2 model, persistence/privacy, readable form, local reconstruction, influence, reconsideration, compact-output, compatibility, tool-surface, version, and packaging evidence.
- r3 regression evidence for conservative outcome eligibility and truthful decision-suppression provenance.

## Decision rationale

r3 closes both defects identified in the r2 Foreman review without expanding scope. Only a validated `choice` with a bounded non-empty `proposed_value` can now create a proposal; raw action prose is never selectable. Missing or ambiguous replacement anchors leave privacy-safe suppression provenance and a truthful degraded compact result, while ordinary deterministic invalidation remains non-degraded. The complete diff, independent counterexamples, 159-test suite, fresh build, installed-wheel smoke, and protected-state audit all pass. The Campaign implementation is therefore accepted.

Live Goose/provider behavior was intentionally not exercised. This does not block repository acceptance, but Q-007 remains pending until the accepted commit is pushed and run through the real Goose interaction flow.

## User audit index

- Contract: `harness/contracts/CAMPAIGN-002-r3.md`
- Worker report: `harness/reports/CAMPAIGN-002-r3-worker.md`
- Baseline-to-final commit: `f7a4f23865383d52dede37f95de091932918090c..ca3d24afdc8feaa65286b13c6118720809749436`
- Foreman review: `harness/evaluations/CAMPAIGN-002-r3-review.md`
- Remaining risk: live Goose/provider decision-form UX is not yet validated for V0.5.

## Next action

Commit the Foreman-owned Campaign assets and accepted implementation history, push through the repository's protected-branch workflow, then run the pinned V0.5 Goose test and attach the result to Q-007. Do not claim release completion before that live evidence is reviewed.
