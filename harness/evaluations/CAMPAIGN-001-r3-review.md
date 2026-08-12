# Foreman Review: CAMPAIGN-001-r3

## Control

- Role: FOREMAN
- Mode: STRICT_SEQUENTIAL
- Decision: CHANGES_REQUESTED
- Contract: `harness/contracts/CAMPAIGN-001-r3.md`
- Worker report: `harness/reports/CAMPAIGN-001-r3-worker.md`
- Reviewed baseline/final state: `8a2531e91a42a1523e83d374b84553907a5e3e94..d9eca22bd8c2d2cb040e51c5a1e469a292d3d2ea`

## Scope and repository review

- Allowed-file compliance: pass. The commit changes exactly 16 authorized production/test/doc paths; the Worker report is the only additional Harness asset.
- Non-goal compliance: pass. Five-tool surface, review-only boundary, version/build, defaults, budgets, and three-point limit remain frozen. No provider routing, majority-vote feature, UI, or translation editing was added.
- User changes preserved: pass. Protected hashes independently match the Worker report. `myTest/` remains absent.
- Diff/commit inspection: complete baseline-to-HEAD diff inspected. One scoped local commit, `d9eca22`; tracked worktree and index are clean; no push.
- Delegation/external compliance: no implementation subagent; one read-only documentation reader is compatible with the contract. No external mutation or live model call.

## Acceptance review

| Criterion | Worker evidence | Foreman verification | Result |
| --- | --- | --- | --- |
| 1 | Shared 12-hex option identity and production regression | Clustering, DecisionPoints, discussion, reconsideration, trace, and fallback share matching IDs | PASS |
| 2 | Unsupported/decline/cancel/off and tie tests | Production workflows select non-tied fallback and retain genuine human-review ties | PASS |
| 3 | Pydantic/FastMCP schema tests | Field descriptions, exact enums, and readable batched mapping independently inspected | PASS |
| 4 | Safe discussion tests | Only existing issue/role/action rows update; model/advisory/non-blocking normalization is enforced | PASS |
| 5 | Evidence-weighted matrix tests | Provenance/tier/relevance/evidence/blocking/confidence are used, but duplicate findings from one role are summed as repeated independent Positions and can decide the outcome by count | FAIL |
| 6 | Trace outcome tests | User choice, Council fallback, and human review are distinguished; deterministic blockers remain separate | PASS |
| 7 | Chief-output regressions | User-facing actions replace opaque IDs; checklist/terminology/conflict fields are populated; review-only boundary remains | PASS |
| 8 | Metadata round trip/redaction | Safe disposition round-trips; prose/secrets remain excluded | PASS |
| 9 | Injected replace failures | Write failures normalize to path-redacted `ReviewPersistenceError` and public tools catch it | PASS |
| 10 | Mode/continuation telemetry tests | Active 6/10/14 budget and bounded counts verified | PASS |
| 11 | Adapter malformed/reasoning-only test | Adapter rejects unsafe content, but an all-malformed Council is then treated as a clean review and returns `COMPLETED`/publishable instead of conservative human review | FAIL |
| 12 | Full suite/introspection | Compile passes; 90 tests pass; exact tools/version/build/V1/continuation/privacy/preflight/budgets remain green | PASS |
| 13 | Documentation review | Docs align with implemented r3 happy/fallback paths, but do not disclose the unsafe all-reviewer-unavailable outcome | FAIL |

## Independent verification

| Command/workflow | Result | Evidence path |
| --- | --- | --- |
| `python -m compileall -q src tests` | PASS, exit 0 | Foreman command output |
| `.venv\\Scripts\\python.exe -m pytest -q --basetemp .tmp\\foreman-r3-full -p no:cacheprovider` | PASS, `90 passed in 2.08s` | Foreman command output |
| FastMCP tool/version introspection | PASS; exact five tools, 0.4.0, `structured-deliberation-v2`, 6/10/14 | Foreman command output |
| Protected hash comparison | PASS; reported r3-start hashes match | Foreman command output |
| `git diff --check <r3-baseline>..HEAD` | PASS | Foreman command output |
| Duplicate-role production matrix | FAIL; six rows/two unique roles, five identical fluency rows select B over one higher-relevance terminology row | Foreman direct clustering→DecisionPoint→policy exercise |
| All reasoning-only reviewer samples | FAIL; six `sample_malformed` events and six unavailable feedback entries still produce `COMPLETED` and publishable/no-review disposition | Foreman direct Core workflow |
| Malicious reconsideration provenance escalation | PASS; caller/hard/blocking claims normalize to model/advisory/non-blocking with empty rule refs | Foreman direct `_reconsider` exercise |
| Two-point partial scripted form defense | PASS with disclosure; missing accepted field becomes malformed and Council fallback completes, although the synthetic fallback reason remains `user_interaction_accept`; real FastMCP schema requires all fields | Foreman direct workflow |

The known host uv-cache permission defect and absent `build` module prevented a fresh r3 package build. This is an allowed disclosed omission under the contract; r1 build evidence remains valid because r3 adds no package/module/dependency entry. Live Goose/provider behavior remains unverified.

## Findings

| Severity | Finding | Required correction |
| --- | --- | --- |
| Major | `_matrix_choice` sums every `RolePosition`. One untrusted reviewer may emit up to five duplicate findings for one issue, multiplying its own role weight five times. The production counterexample lets five identical fluency rows overrule one higher-relevance terminology row, making repeated row count authoritative. | Normalize/cap total influence per `(issue, role)` before scoring. Identical duplicate findings must not change the outcome versus one copy; multiple distinct options from one role need deterministic conservative normalization. |
| Critical | `_sample_json` correctly marks reasoning-only/empty/error responses unavailable, but `run_structured_review` does not distinguish zero successful structured reviews from six successful clean reviews. With every active reviewer unavailable it returns `COMPLETED` and publishable/no-review. | Track independent-review coverage. All active reviewer samples unavailable must force `NEEDS_HUMAN_REVIEW`, `publishability=需人工复核`, explicit fallback/coverage provenance, and no false clean conclusion. Partial unavailability must be explicitly surfaced; successful structured empty findings must remain distinguishable from transport/parse failure. |

## Preserved evidence

- All r1 package evidence previously preserved.
- r3 criteria 1–4 and 6–10, 12 implementation and tests.
- Exact five-tool surface/version/build metadata, option identity, form schema, safe discussion/reconsideration, chief output, metadata privacy, persistence error normalization, telemetry budgets, and continuation behavior.
- The complete 90-test green suite remains regression evidence, but r4 must add the two missing counterexamples and rerun the full suite.

## Decision rationale

The r3 implementation successfully repairs the original option-ID, form, discussion, policy-output, metadata, and write-error defects. It cannot be accepted because two untrusted-model failure modes still violate frozen invariants: repeated findings can self-amplify one role into a count-based decision, and total reviewer sampling failure is misreported as a clean publishable review. Both are bounded corrections within existing architecture, so the correct decision is `CHANGES_REQUESTED`, not `BLOCKED`.

## Next action

- Execute `harness/contracts/CAMPAIGN-001-r4.md` from verified baseline `d9eca22bd8c2d2cb040e51c5a1e469a292d3d2ea`.
