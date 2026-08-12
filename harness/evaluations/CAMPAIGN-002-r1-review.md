# Campaign Foreman Review: CAMPAIGN-002-r1

## Control

- Role: FOREMAN
- Mode: STRICT_CAMPAIGN
- Decision: CHANGES_REQUESTED
- Contract: `harness/contracts/CAMPAIGN-002-r1.md`
- Campaign Worker report: `harness/reports/CAMPAIGN-002-r1-worker.md`
- Execution ledger: `harness/reports/CAMPAIGN-002-r1-ledger.md`
- Reviewed baseline/final state: `824559afd68f170758837769b1d1d19df991db4b..5687208aaeaaf3e6b00c192fb42596fb9b6cbf47`
- Review date: 2026-08-12 Asia/Shanghai

## Scope and repository review

- Complete baseline-to-final diff inspected: yes; 28 committed files, 1,562 insertions, 148 deletions, seven scoped commits.
- Global boundary and non-goal compliance: passed. Exact five tools, review-only behavior, no custom MCP UI, no majority voting, and 6/10/14 budgets are preserved.
- User changes preserved: passed. Issued plan/features/progress/contract, `.learnings/`, audit markdown, and review records match protected hashes.
- Commit/worktree policy compliance: passed. Index is empty; implementation changes are committed; only declared Foreman/user assets and required reports remain dirty/untracked.
- Required Worker capability and delegation-policy compliance: passed. Three bounded subagents were disclosed; no overlapping concurrent production edit was found.
- External/destructive action compliance: passed. No push, PR, release, deployment, credential, Goose installation, or live-model mutation occurred.

## Task graph review

| Package | Boundary/dependency review | Worker evidence | Foreman verification | Package result |
| --- | --- | --- | --- | --- |
| PKG-011 | Models/compatibility/persistence stayed in scope | focused 24; full 122 | Diff and V1/V2.0/V2.1 privacy tests inspected; full suite passed | PASS; evidence preserved |
| PKG-012 | Outcome normalization stayed in scope, but the current-outcome interface is wrong for document-sized candidates | focused 24; full 126 | Independent long-document and local-anchor probes fail | FAIL |
| PKG-013 | Standard elicitation adapter stayed in scope, but emitted enum values are opaque hashes | focused 30; full 129 | Exact FastMCP/Pydantic schema inspected; enum is `choice_<hash>`/`delegate_<hash>` | FAIL |
| PKG-014 | Reconsideration/status changes stayed in scope | focused 35; full 132 | Selection, cap, provenance, failure and degradation code/tests inspected; full suite passed | PASS; evidence preserved |
| PKG-015 | Compact-output changes stayed in scope | focused 26; full 135 | Bounds, privacy, deduplication, effective-task and warning paths inspected; full suite passed | PASS; evidence preserved |
| PKG-016 | Version/docs/build changes stayed in scope | full 141; fresh build/wheel smoke | Foreman compile, 141-test run, fresh sdist/wheel and tool introspection passed; UX docs inherit PKG-013 claim defect | PASS except affected UX wording/tests |

## Campaign acceptance review

| Criterion | Worker evidence | Foreman verification | Result |
| --- | --- | --- | --- |
| 1 | Synthetic `Continue` fixture | Works only when the entire candidate is the local span; fails for normal document candidates | FAIL |
| 2 | Duplicate proposal tests | Normalization/influence tests pass | PASS |
| 3 | Affirmation tests | Clean and mixed affirmation tests pass | PASS |
| 4 | Current candidate and no-point tests | Current candidate is incorrectly the whole `task.candidate_translation` | FAIL |
| 5 | Bounded form tests | Counts/bounds pass, but actual enum choices are opaque hashes | FAIL |
| 6 | Mapping/stale tests | Internal round trip is safe; user-facing values are not readable | FAIL |
| 7 | Delegation/failure tests | Provenance paths pass, subject to readable-value correction | PASS with integration dependency |
| 8 | User authority | Policy Matrix and valid-choice path pass | PASS with option-validity dependency |
| 9 | Targeted reconsideration/budget | Reference flow uses eight calls and supporting role is not resampled | PASS |
| 10 | Degraded reconsideration | Forced budget/runtime tests pass | PASS |
| 11 | Compact output | Required fields and bounds pass | PASS |
| 12 | Chief output cleanup | Deduplication and affirmation behavior pass | PASS |
| 13 | Persistence/privacy/migration | Tests and source inspection pass | PASS |
| 14 | Accepted regressions | Full 141-test suite passes | PASS |
| 15 | Tools/defaults/version/build | Independent introspection matches frozen contract | PASS |
| 16 | Compile/tests/build/diff | Independent compile, 141 tests, fresh sdist/wheel, diff check pass | PASS |
| 17 | Documentation | Documents opaque values as if they were readable; must be corrected with implementation | FAIL |

## Independent integration verification

| Command/workflow | Result | Evidence |
| --- | --- | --- |
| `python -m compileall -q src tests` | PASS | exit 0 |
| `.venv\Scripts\python.exe -m pytest -q --basetemp .tmp\foreman-campaign002-r1-pytest -p no:cacheprovider` | PASS | 141 passed in 1.69s |
| `$env:UV_CACHE_DIR='.tmp\foreman-campaign002-uv-cache'; uv build --out-dir .tmp\foreman-campaign002-dist` | PASS | fresh 0.5.0 sdist and wheel |
| `_server_info()` plus `mcp.get_tools()` | PASS | 0.5.0 / `outcome-first-decision-v3` / schema 2.1 / exact five tools |
| `git diff --check 824559a..5687208` | PASS | exit 0 |
| Exact emitted schema for `继续` versus `下一步` | FAIL | enum values are `choice_f08fa884c58d`, `choice_99ab5485672e`, `delegate_e2f76c056b55`; readable outcomes exist only in the description |
| Long-document current-outcome probe | FAIL | a 603-character candidate yields `candidate_actions=['下一步']` and zero DecisionPoints |
| Local replacement with unrelated `{name}` probe | FAIL | valid local choice exists before Policy Gate and is removed after comparing the whole source against the isolated string `下一步` |

One Foreman read-only `rg` command failed because of a malformed quoted regex. It caused no writes and was replaced by literal/targeted inspection. `.learnings/` remained protected; this review is the durable incident record.

## Delegation and integration audit

- Package/subagent/file/commit mapping reconciled: yes.
- Frozen interface and dependency compliance: package order and shared-file integration were respected, but the PKG-012 current-outcome interface did not model issue-local replacement.
- Collision/conflict handling: no repository collision found.
- Main Worker verification independently checked: package counts reconcile; final tests/build reproduced.
- Ledger/report/repository consistency: consistent.

## Findings

| Severity | Package/criterion | Finding and evidence | Required correction |
| --- | --- | --- | --- |
| HIGH | PKG-013 / criteria 5, 6, 17 | `_interaction_form` uses `Literal` values from `_safe_form_value`; the actual schema enum is opaque hashes. Standard enum clients can therefore present the same unreadable tokens that V0.5 was intended to remove. Tests explicitly require the hashes instead of testing readable enum values. | Make each emitted enum value itself concise and human-readable while retaining a server-side, per-field mapping to stable internal option IDs. Do not rely on prose descriptions to relabel opaque enums. Preserve safe stale/unknown rejection. |
| HIGH | PKG-012 / criteria 1, 4 | `run_structured_review` passes the entire candidate translation to `cluster_findings`, and `_model_cluster` treats it as the current issue outcome. A candidate longer than 500 characters is discarded; shorter documents expose the whole translation as one option. | Derive the current outcome from the issue-local `candidate_span` using a deterministic conservative rule. Full-task candidate text may be used only to reconstruct/validate a proposed local replacement, never as the displayed local outcome. |
| HIGH | PKG-012/013 integration / criteria 1, 8 | `_validate_outcome_options` runs full-source preflight against each isolated local outcome. An unrelated placeholder elsewhere in the document invalidates an otherwise safe `继续`/`下一步` choice. | Reconstruct the complete candidate translation by applying the local outcome to an unambiguous candidate anchor, then run deterministic preflight/hard constraints on the reconstructed full candidate. Ambiguous/missing anchors must degrade conservatively and explicitly. |
| MEDIUM | Tests/docs / criteria 16, 17 | Existing tests are green because they only use a one-token whole candidate and assert `choice_`/`delegate_` enums. README/AGENTS repeat the opaque-value claim. | Add long-document, unrelated-placeholder, ambiguous-anchor, and exact readable-enum regressions; update authoritative wording. |

## Preserved evidence

- PKG-011 V2.1 models, V1/V2.0 reading, full/metadata/off persistence, atomic writes, and metadata privacy.
- PKG-012 proposal deduplication, one-role influence, affirmation classification, and no-choice/no-DecisionPoint behavior, except current-outcome derivation and option validation.
- PKG-014 targeted contrary-role reconsideration, three-role cap, sampling accounting, provenance, and truthful degradation.
- PKG-015 effective-task snapshot, deliberation digest, warning surface, bounded compact output, and chief checklist deduplication.
- PKG-016 exact version/build/tool/default/budget metadata and package build mechanics, excluding affected form documentation/tests.
- All accepted V0.4 regression evidence remains valid.

## Decision rationale

The implementation is healthy at the unit/build/repository level and most V0.5 architecture is sound. Acceptance is withheld because the three failed paths are the central user value of Campaign 002: readable Goose decisions and correct issue-local outcome handling. These are bounded corrections and do not require redesign, new authority, or user input, so the correct decision is `CHANGES_REQUESTED`, not `BLOCKED`.

## User audit index

- Contract: `harness/contracts/CAMPAIGN-002-r1.md`
- Worker report and ledger: `harness/reports/CAMPAIGN-002-r1-worker.md`, `harness/reports/CAMPAIGN-002-r1-ledger.md`
- Baseline-to-final diff: `824559afd68f170758837769b1d1d19df991db4b..5687208aaeaaf3e6b00c192fb42596fb9b6cbf47`
- Key verification: full suite, fresh package build, schema dump, long-candidate probe, and local-placeholder probe recorded above.
- Remaining risk: live Goose rendering remains unverified until a corrected readable schema is accepted and pushed for a pinned test.

## Next action

Execute the bounded correction contract `harness/contracts/CAMPAIGN-002-r2.md`. Preserve accepted package evidence, correct only the issue-local outcome/form/validation slice, run the full integrated suite and fresh build, and return for independent review without pushing.
