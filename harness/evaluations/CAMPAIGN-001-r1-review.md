# Campaign Foreman Review: CAMPAIGN-001-r1

## Control

- Role: FOREMAN
- Mode: STRICT_CAMPAIGN
- Decision: CHANGES_REQUESTED
- Contract: `harness/contracts/CAMPAIGN-001-r1.md`
- Campaign Worker report: `harness/reports/CAMPAIGN-001-r1-worker.md`
- Execution ledger: `harness/reports/CAMPAIGN-001-r1-ledger.md`
- Reviewed baseline/final state: `34d41946717f1993b8954260afc893737198a3bb..8a2531e91fe3f823449b0fd1e8a0eef7fd857890`

## Scope and repository review

- Complete baseline-to-final diff inspected: yes; 45 changed paths and all current production modules, tests, docs, metadata, report, and ledger were reviewed.
- Global boundary and non-goal compliance: pass. The review-only boundary, five-tool limit, model-call limits, and no-majority decision remain intact.
- User changes preserved: pass. Protected asset hashes match the Worker ledger; `reviews/`, the audit, and other user artifacts were not staged.
- Commit/worktree policy compliance: pass. Five scoped local commits; `main` is five commits ahead of unchanged `origin/main`; no tracked changes remain.
- External/destructive action compliance: pass. No push, PR, release, deployment, credential change, Goose installation mutation, or user-data deletion was reported or observed.

## Task graph review

| Package | Boundary/dependency review | Worker evidence | Foreman verification | Package result |
| --- | --- | --- | --- | --- |
| PKG-001 | Models and V1 adapter stayed in scope | 17 model/persistence tests | Conservative normalization and V1/V2 parsing inspected and rerun | PASS |
| PKG-002 | Persistence stayed in scope | Atomic/privacy/ID tests | Full/off/privacy behavior passes, but metadata reload resets final disposition to model defaults | FAIL |
| PKG-003 | Role registry/plan stayed in scope | 10 role tests | Nine definitions, chief adjudicator, routing, and budgets verified | PASS |
| PKG-004 | Runtime port stayed independent of FastMCP Core | 5 runtime tests | FastMCP 2.13.0.2 `Context.sample` returns text-bearing content; adapters and scripts pass | PASS |
| PKG-005 | Preflight stayed deterministic | 10 preflight tests | Technical blockers and warning-only numeric/Markdown behavior verified | PASS |
| PKG-006 | Clustering stayed issue-centric | 5 clustering tests | Named-example rules are absent; regression cases pass | PASS |
| PKG-007 | Discussion is bounded | unit/integration traces | Turns are recorded but `position_changed=true` never changes the cluster Position Matrix, so deliberation cannot affect a decision | FAIL |
| PKG-008 | Policy/chief integration stayed in scope | policy tests | Production Position IDs do not match DecisionPoint option IDs; provenance/tier are not consumed; fallback cannot adjudicate | FAIL |
| PKG-009 | Interaction and fallback stayed in scope | scripted acceptance/unsupported tests | Generated form is an unexplained free-text field with no option enum; scripted tests bypass the human-facing schema | FAIL |
| PKG-010 | Migration/docs/tool surface stayed in scope | 71 locked tests, build, scan | Exact five tools/version/build pass, but docs claim fallback and evidence behavior not implemented by production | FAIL |

## Campaign acceptance review

| Criterion | Worker evidence | Foreman verification | Result |
| --- | --- | --- | --- |
| 1 | F-001..F-010 and Q evidence table | Several claimed behaviors are only unit-constructible and not reachable correctly through production | FAIL |
| 2 | Q-001..Q-006 table | Automated gates run, but Q-003 is skipped and Q-005 behavior alignment is false | FAIL |
| 3 | Mocked full default path | Real form contract is unusable and fallback Position Matrix has disjoint IDs | FAIL |
| 4 | Clean workflow test | Six calls, no discussion or DecisionPoints | PASS |
| 5 | Missing-placeholder test | Preflight blocker survives and no preference point is created | PASS |
| 6 | Scripted valid choice | Internal ID injection is decisive, but a user is not shown a selectable valid-ID schema | FAIL |
| 7 | Unsupported workflow test | Terminates, but default Council fallback always degrades to human review instead of adjudicating a non-tie | FAIL |
| 8 | Continuation integration test | Parent bytes unchanged; linked child; only participant roles resampled | PASS |
| 9 | Compact/full tests | Trace separation passes; chief conflict output remains opaque IDs and non-actionable topic strings | FAIL |
| 10 | Persistence tests | V1/full/off/privacy pass; metadata disposition becomes false defaults after reload | FAIL |
| 11 | Budget/point tests | Hard 6/10/14 budgets and three-point cap verified | PASS |
| 12 | Structured-output tests | Extra reasoning fields are discarded; no secrets observed | PASS |
| 13 | Tool introspection/docs | Exact tools pass; fallback/evidence docs overstate implementation | FAIL |
| 14 | 71-test suite | Green suite misses production ID/schema/disposition counterexamples | FAIL |
| 15 | Hashes/status | Protected assets preserved and commits scoped | PASS |

## Independent integration verification

| Command/workflow | Result | Evidence path |
| --- | --- | --- |
| `python -m compileall -q src tests` | PASS, exit 0 | Foreman command output |
| system Python pytest with workspace basetemp | PASS, `67 passed, 1 skipped` | FastMCP-only surface skipped because system Python lacks FastMCP |
| `.venv\\Scripts\\python.exe -m pytest ...` | PASS, `71 passed in 1.13s` | Existing locked virtual environment |
| FastMCP tool/version introspection | PASS, exact five tools; version 0.4.0; expected build | Foreman command output |
| production option identity counterexample | FAIL, Position/DecisionPoint ID intersection is empty | `option_*` differs by 12 vs 10 digest characters |
| default fallback counterexample | FAIL, selected `""`, basis `indistinguishable_valid_alternatives`, human review true for a non-tie | Foreman direct Core exercise |
| generated elicitation schema inspection | FAIL, one required plain string field; no question, description, enum, or option labels | Foreman `model_json_schema()` output |
| discussion position-change counterexample | FAIL, turn says changed while matrix remains unchanged | Foreman direct normalization exercise |
| metadata disposition round trip | FAIL, `可发布/否` reloads as `需人工复核/是` | Foreman temporary-store exercise |
| `git diff --check 34d4194..HEAD` | PASS | Foreman command output |

The literal `uv run` and `uv build` retries could not read the host uv user cache (`sdists-v9/.git`, access denied). The existing `.venv` independently ran all 71 tests, and the Worker's successful frozen suite/build evidence remains usable. This host permission issue is not a product failure.

## Delegation and integration audit

- Package/subagent/file/commit mapping reconciled: yes; report and ledger agree with the five commits and changed paths.
- Frozen interface and dependency compliance: mostly; public surface and budgets comply, but F-007/F-008/F-009 semantics do not.
- Collision/conflict handling: no unauthorized overlap or protected-file mutation observed.
- Main Worker verification independently checked: syntax, tests, tools, metadata, and the highest-risk orchestration paths were rerun.
- Ledger/report/repository consistency: pass, apart from conclusions invalidated by missing counterexample coverage.

## Findings

| Severity | Package/criterion | Finding and evidence | Required correction |
| --- | --- | --- | --- |
| Critical | PKG-008, criteria 3/7 | `clustering.py` creates 12-character Position option digests while `deliberation.py` creates 10-character DecisionPoint digests. No production position can match a valid option, so non-interactive Council adjudication cannot select a non-tied alternative. | Use one authoritative stable option identity from clustering through DecisionPoint, discussion, reconsideration, policy, and trace; add end-to-end fallback regression. |
| Critical | PKG-009, criteria 3/6 | `_interaction_form` uses `(str, ...)`, and the elicitation message is generic. The schema exposes only an opaque decision ID and free text; it does not show or constrain valid options. | Generate a FastMCP-compatible schema with per-question descriptions and valid-option enums, plus a readable batched message; test the actual JSON schema. |
| Major | PKG-007/008 | Discussion turns declaring a position change are persisted but never applied to `IssueCluster.positions`; downstream adjudication ignores the discussion. | Safely normalize valid position changes for the permitted issue/speaker/action and feed the updated matrix into later steps. |
| Major | PKG-008 | Matrix scoring uses role relevance, confidence, and evidence count only. Evidence origin/tier and rule provenance are discarded before policy despite frozen design and docs. | Carry conservative provenance/tier into positions and consume it without allowing model output to manufacture hard constraints or blockers. |
| Major | PKG-008/009 | Chief output uses issue topics and opaque option IDs; `terminology_decisions` is always empty. The compact result is not an execution-ready chief summary of the process. | Resolve selected IDs to labels/actions, populate relevant checklist sections, and summarize bases without hidden reasoning. |
| Major | PKG-002/criterion 10 | Metadata projection omits safe final disposition fields; reload/list returns Pydantic defaults instead of the actual result. | Persist allowlisted `publishability`/`review_needed` (and only safe non-prose metadata) and assert exact round trip/list values. |
| Medium | PKG-004/telemetry | Reused/default scripted telemetry may retain a standard sample-budget value for another mode. | Synchronize runtime metadata budget with the active CouncilPlan and test all three modes. |
| Medium | tool robustness | Atomic-write `OSError` is not normalized to `ReviewPersistenceError`, so public tools may leak an uncaught storage failure. | Wrap storage I/O failures in the persistence error contract and test a simulated failure. |

## Preserved evidence

- PKG-001 model/V1 parsing foundations.
- PKG-003 role registry and deterministic routing.
- PKG-004 runtime protocol and FastMCP text/elicitation transport adapters, subject to the form-schema correction.
- PKG-005 deterministic preflight.
- PKG-006 issue-centric clustering strategy, subject to option-ID integration changes.
- PKG-010 exact five-tool surface, package/build metadata, legacy removal, compile/build evidence.
- Continuation immutability/linked-history mechanics and privacy redaction tests.

## Decision rationale

The Campaign is structurally strong and the automated suite is healthy, but the central user-visible V0.4 promise is not yet reachable: the real form does not present selectable choices, and the configured no-response Council fallback cannot match any Position to any DecisionPoint. These are bounded integration defects, so the correct decision is `CHANGES_REQUESTED`, not `BLOCKED` or a redesign.

## User audit index

- Contract: `harness/contracts/CAMPAIGN-001-r1.md`
- Worker report and ledger: `harness/reports/CAMPAIGN-001-r1-worker.md`, `harness/reports/CAMPAIGN-001-r1-ledger.md`
- Baseline-to-final diff/commits: `34d4194..8a2531e`; five commits recorded above.
- Key verification artifacts: this review and Foreman command output; no user test fixture was modified.
- Remaining risks or waivers: live Goose/provider behavior remains deferred because the Worker environment had no configured DeepSeek key; FastMCP 2.13.0.2 interface was inspected locally. The previously fixed DeepSeek reasoning-first issue is not contradicted: the supported FastMCP sampling return has a `.text` field and that adapter test passes.

## Next action

- Execute the bounded Sequential correction contract `harness/contracts/CAMPAIGN-001-r2.md`.
- Do not rerun or rewrite unaffected architecture packages except where integration changes require regression verification.
