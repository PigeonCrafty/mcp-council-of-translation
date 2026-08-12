# Foreman Review: CAMPAIGN-002-r2

## Control

- Role: FOREMAN
- Mode: STRICT_SEQUENTIAL
- Decision: CHANGES_REQUESTED
- Contract: `harness/contracts/CAMPAIGN-002-r2.md`
- Worker report: `harness/reports/CAMPAIGN-002-r2-worker.md`
- Reviewed baseline/final state: `5687208aaeaaf3e6b00c192fb42596fb9b6cbf47..f7a4f23865383d52dede37f95de091932918090c`
- Review date: 2026-08-12 Asia/Shanghai

## Scope and repository review

- Allowed-file compliance: passed; exactly 13 authorized production/test/doc files changed.
- Non-goal compliance: passed; no surface, dependency, version, budget, provider, custom UI, voting, or review-only boundary change.
- User changes preserved: passed; all issued protected hashes match.
- Resume/retry and side-effect safety: passed; the disclosed local dependency-install retry was repository-local and no external side effect was repeated.
- Sensitive evidence hygiene: passed; no credential, raw token, or private record content was introduced.
- Diff/commit inspection: complete; two scoped commits, 242 insertions and 57 deletions, index empty.

## Acceptance review

| Criterion | Worker evidence | Foreman verification | Result |
| --- | --- | --- | --- |
| 1 | Exact readable schema | Pydantic enum independently equals `保留：继续`, `改为：下一步`, delegation; no hashes | PASS |
| 2 | Readable round trip | Mapping and selected internal ID tests inspected | PASS |
| 3 | Per-field/stale handling | Same value across fields and malformed cases pass | PASS |
| 4 | Long document | Independent 603-character probe retains local `继续`/`下一步` | PASS |
| 5 | Unrelated placeholder | Independent full-candidate reconstruction retains both options | PASS |
| 6 | Affected placeholder | Independent `{count}` probe produces zero DecisionPoints | PASS |
| 7 | Ambiguous anchor | Helper returns `ambiguous_candidate_anchor`, but the persisted result silently loses it and reports clean completion | FAIL |
| 8 | Empty/contradictory spans | Focused tests pass | PASS |
| 9 | Preserve r1 behavior | Full suite passes, but an uncovered unclassified/legacy finding path promotes raw `action` prose to outcomes | FAIL |
| 10 | Frozen identifiers/defaults | Independent introspection matches 0.5.0/schema 2.1/build/five tools/6-10-14 | PASS |
| 11 | Documentation | Readable/local reconstruction wording is correct, but the assertion that action is never selectable is false in production | FAIL |
| 12 | Integrated verification | Compile, 146 tests, fresh build and diff pass; required behavioral coverage is incomplete | FAIL |

## Independent verification

| Command/workflow | Result | Evidence |
| --- | --- | --- |
| `python -m compileall -q src tests` | PASS | exit 0 |
| `.venv\Scripts\python.exe -m pytest -q --basetemp .tmp\foreman-campaign002-r2-pytest -p no:cacheprovider` | PASS | 146 passed in 1.57s |
| `$env:UV_CACHE_DIR='.tmp\foreman-campaign002-r2-uv-cache'; uv build --out-dir .tmp\foreman-campaign002-r2-dist` | PASS | fresh 0.5.0 sdist and wheel |
| Exact five-tool/version/build/schema introspection | PASS | expected identifiers and order |
| Readable enum probe | PASS | exact three readable values |
| Long/unrelated/affected-placeholder probes | PASS | r1 defects closed |
| Two valid unclassified `issue` findings with action prose | FAIL | production creates one DecisionPoint with `改为：请结合…` action instructions |
| Repeated-anchor production workflow | FAIL | `decision_points=0`, `warnings=[]`, `degraded=false`, empty invalid/suppression provenance, status `COMPLETED` |
| `git diff --check 5687208..f7a4f23` | PASS | exit 0 |

## Findings

| Severity | Finding | Required correction |
| --- | --- | --- |
| HIGH | `clustering._model_cluster` falls back to `legacy_actions` whenever no concrete proposal exists. Because fresh untrusted reviewer output defaults missing/invalid classification to `finding_kind="issue"`, two such findings can recreate action-prose DecisionPoints. This contradicts the frozen plan, README, AGENTS, and r2 criterion 9. | In production normalization, only `finding_kind="choice"` with a non-empty valid `proposed_value` may create an outcome. `issue`, `affirmation`, invalid/missing classification, and `choice` without a valid proposal must never promote `action`. Preserve V2.0 record readability without reactivating legacy action selection. |
| MEDIUM | Missing/repeated-anchor rejection is explicit only inside `_reconstruct_candidate`; when validation removes the DecisionPoint, the persisted record loses the reason and may report unqualified `COMPLETED`. This does not satisfy criterion 7's explicit-result requirement or the Campaign's truthful-degradation principle. | Persist bounded content-free decision-suppression provenance for missing/ambiguous anchors and surface it in compact warnings/fallback status. Do not expose candidate text. A meaningful interaction suppressed for reconstruction uncertainty must not masquerade as clean completion. |
| MEDIUM | The 146-test suite does not cover either production counterexample. | Add direct Core regressions for missing/invalid classification, issue-only action prose, choice-without-proposal, and persisted missing/repeated-anchor suppression/status. |

## Decision rationale

r2 successfully fixes the three r1 defects and most of its evidence is accepted for reuse. Acceptance is withheld because the raw-action fallback recreates the exact UX failure Campaign 002 was designed to eliminate whenever a model omits new fields, a realistic untrusted-output condition. The silent anchor-suppression path also violates the explicit degradation contract. Both corrections are narrow and need no user choice, new authority, or architectural redesign, so the decision is `CHANGES_REQUESTED` rather than `BLOCKED`.

## Preserved evidence

- Human-readable Pydantic/FastMCP enum values and per-field mapping.
- Issue-local current outcome and long-document behavior.
- Full-candidate reconstruction and unrelated/affected-placeholder validation.
- Collision handling, delegation, stale/malformed response handling.
- All r1 accepted models, persistence/privacy, influence, reconsideration, compact-output, version/build/tool and packaging evidence.

## Next action

Execute `harness/contracts/CAMPAIGN-002-r3.md` from exact baseline `f7a4f23865383d52dede37f95de091932918090c`. Remove action-prose promotion, persist/surface bounded reconstruction suppression, add focused production regressions, rerun the full suite and fresh build, and stop without pushing.
