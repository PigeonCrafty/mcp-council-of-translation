# Campaign Foreman Review: CAMPAIGN-003-r1

## Control

- Role: FOREMAN
- Mode: STRICT_CAMPAIGN
- Decision: CHANGES_REQUESTED
- Contract: `harness/contracts/CAMPAIGN-003-r1.md`
- Campaign Worker report: `harness/reports/CAMPAIGN-003-r1-worker.md`
- Execution ledger: `harness/reports/CAMPAIGN-003-r1-ledger.md`
- Reviewed baseline/final state: `fe4b55a6597d8ac18885c0faab14722f44588e12..3de6e5fafb0d6a0a4347b68469e99ce7ef8bc816`

## Scope and repository review

- Complete baseline-to-final diff inspected: yes; 34 authorized files, 2,187 insertions and 159 deletions.
- Global boundary and non-goal compliance: pass; exact five tools, review-only behavior, no new dependency and no forbidden path in the six commits.
- User changes preserved: pass; all protected hashes matched the issued contract.
- Commit/worktree policy compliance: pass; six scoped commits, empty index, only protected Foreman/user assets and the two authorized r1 reports remain dirty/untracked.
- Required Worker capability and delegation-policy compliance: pass; Main Worker used no subagents and integrated in dependency order.
- External/destructive action compliance: pass; no push, PR, release, deployment, credential, Goose or provider mutation.
- Resume/retry and side-effect safety: pass; build/install reads were repository-local and no external write was reported.
- Sensitive evidence hygiene: pass; no credential, raw private payload or hidden reasoning was found in the reports or committed diff.

## Task graph review

| Package | Boundary/dependency review | Worker evidence | Foreman verification | Package result |
| --- | --- | --- | --- | --- |
| PKG-017 | V2.2 models/persistence stayed in scope | 29 focused passes and privacy probes | Models, compatibility and metadata projection inspected; focused/full suites passed | PASS |
| PKG-018 | Briefing gate stayed in scope, but its frozen sufficiency predicate is incomplete | 25 focused passes | Counterexample shows unknown content type plus three other fields skips briefing | FAIL |
| PKG-019 | Context gaps/reconsideration/budgets stayed in scope | 34 focused passes | Gap isolation, bounded form, affected-role and forced-insufficiency tests passed | PASS |
| PKG-020 | Shared form IA stayed in scope | 16 focused passes | Flat/bounded schemas and exact outcome mapping passed | PASS |
| PKG-021 | Digest/phase trace stayed in scope | 17 focused passes | Frozen 12-section order, six lenses, privacy and 13-call path passed | PASS |
| PKG-022 | Migration/build/docs stayed in scope | 182 full passes, build and wheel smoke | Version/tool/budget checks passed; Foreman fresh build produced 0.6.0 artifacts | PASS |

## Campaign acceptance review

| Criterion | Worker evidence | Foreman verification | Result |
| --- | --- | --- | --- |
| 1 | Source/target-only briefing ordered before sampling | Focused test rerun | PASS |
| 2 | Rich auto skip plus always/off matrix | Frozen rich-context predicate counterexample failed | FAIL |
| 3-11 | Interaction provenance, context gaps, Policy Gate and V0.5 invariants | Focused and full suites rerun; relevant diff inspected | PASS |
| 12-17 | Process digest, privacy, telemetry, budgets, compatibility and continuation | Focused/full suites and source inspection passed | PASS |
| 18-20 | Identifiers, complete regression, packaging, scope and hygiene | 182 passes, compile, diff/scope audit and fresh build passed | PASS |

## Independent integration verification

| Command/workflow | Result | Evidence path |
| --- | --- | --- |
| `python -m compileall -q src tests` | PASS | Foreman console, 2026-08-12 |
| Full pytest with isolated basetemp/cache disabled | PASS, `182 passed in 2.15s` | Foreman console, 2026-08-12 |
| Contract focused V2.2 suite | PASS, `59 passed in 1.62s` | Foreman console, 2026-08-12 |
| Baseline-to-final `git diff --check` and allowed-path audit | PASS, 34 changed / 0 disallowed | Foreman console, 2026-08-12 |
| Fresh `uv build` | PASS; fresh 0.6.0 wheel and sdist created | `.tmp/foreman-c003-dist/` (ephemeral) |
| Frozen sufficiency counterexample | FAIL: `unknown_plus_three True False` | Foreman console, 2026-08-12 |

The Foreman fresh wheel dependency installation did not finish promptly and was terminated; this does not create the Campaign failure, because the Worker's isolated wheel smoke is internally consistent and the independent source/full/build checks passed. The r2 correction must rerun the required package/full/build evidence.

## Delegation and integration audit

- Package/subagent/file/commit mapping reconciled: yes; no subagents.
- Frozen interface and dependency compliance: one semantic violation in PKG-018 only.
- Collision/conflict handling: pass; shared orchestration/form changes were integrated sequentially.
- Main Worker verification independently checked: yes; reported test counts, commits, boundaries and hashes reconcile.
- Ledger/report/repository consistency: pass.

## Findings

| Severity | Package/criterion | Finding and evidence | Required correction |
| --- | --- | --- | --- |
| Major | PKG-018 / criterion 2 | `context_is_sufficient()` returns `_provided_context_count(task) >= 3`. This lets `content_type=unspecified`, `context`, `audience`, and `term_glossary` count as rich and skip briefing. The frozen contract requires a recognized content type **and** at least two independent context categories. Foreman probe printed `unknown_plus_three True False`. | Implement the exact frozen predicate and add positive/negative counterexample tests. Do not alter public schema, forms or other accepted packages. |

## Preserved evidence

- Preserve r1 evidence for PKG-017, PKG-019, PKG-020, PKG-021 and PKG-022.
- Preserve all r1 boundary, privacy, five-tool, 6/13/18, digest, compatibility and packaging evidence.
- PKG-018 briefing ordering and action-matrix evidence remains useful, but its sufficiency evidence must be replaced by r2 tests.

## Decision rationale

The implementation is otherwise cohesive and well verified, but the failed predicate is a frozen product invariant: unknown content type must remain visible as uncertainty and must not silently bypass the user briefing merely because unrelated fields reach a numeric threshold. This is a bounded deterministic correction, so the decision is `CHANGES_REQUESTED`, not `BLOCKED`.

## User audit index

- Contract: `harness/contracts/CAMPAIGN-003-r1.md`
- Worker report and ledger: `harness/reports/CAMPAIGN-003-r1-worker.md`, `harness/reports/CAMPAIGN-003-r1-ledger.md`
- Baseline-to-final diff/commits: `fe4b55a..3de6e5f`, six commits
- Key verification artifacts: this review and r1 focused/full/build evidence
- Remaining risks or waivers: live Goose V0.6 rendering remains unverified; no acceptance waiver granted

## Next action

Execute only the bounded correction contract `harness/contracts/CAMPAIGN-003-r2.md` from exact baseline `3de6e5fafb0d6a0a4347b68469e99ce7ef8bc816`.
