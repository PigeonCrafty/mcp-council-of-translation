# Foreman Review: CAMPAIGN-001-r4

## Control

- Role: FOREMAN
- Mode: STRICT_SEQUENTIAL
- Decision: CHANGES_REQUESTED
- Contract: `harness/contracts/CAMPAIGN-001-r4.md`
- Worker report: `harness/reports/CAMPAIGN-001-r4-worker.md`
- Reviewed baseline/final state: `d9eca22bd8c2d2cb040e51c5a1e469a292d3d2ea..6978c7b76cf7cb8868405a92e05b831deb9e4a09`

## Scope and repository review

- Allowed-file compliance: pass. The commit changes exactly ten authorized production/test/doc paths; the Worker report is the only additional r4 Harness asset.
- Baseline and commit ancestry: pass. The contracted baseline exists, is the sole parent of `6978c7b`, and HEAD equals the reported final SHA.
- Non-goal compliance: pass. Five-tool surface, version/build, review-only boundary, defaults, budgets, provider integration, and three-point limit remain frozen. No retries or extra model calls were added.
- User changes preserved: pass. All reported protected hashes independently match; `myTest/` remains absent.
- Repository state: tracked worktree and index are clean; `main` is seven local commits ahead of unchanged `origin/main`; no push.
- Delegation/external compliance: zero subagents, external mutations, and live Goose/model calls.

## Acceptance review

| Criterion | Foreman verification | Result |
| --- | --- | --- |
| 1 | One versus five identical same-role findings produce two matrix rows, identical scores, and the same selection while all finding IDs remain in trace | PASS |
| 2 | Distinct actions from one role share a normalized fixed budget and a genuine equal-evidence tie requests human review | PASS |
| 3 | Relevance, provenance, tier, evidence/rule references, blocking state, stance, and confidence remain in pre-normalization scoring; repetition is not a vote | PASS |
| 4 | Transport/error, empty, reasoning-only status, and invalid JSON are distinguished, but syntactically valid malformed reviewer envelopes are counted as structured successes | FAIL |
| 5 | Zero transport/parse successes returns `NEEDS_HUMAN_REVIEW`, `需人工复核/是`, explicit `reviewer_coverage_none`, and no suggested translation | PASS |
| 6 | Partial transport/parse coverage is explicit and conservative; continuation cannot clear it | PASS |
| 7 | Six valid `{role_feedback, findings: []}` responses remain clean, but `{}`, `findings: null`, string findings, and scalar finding entries also falsely return the same clean `COMPLETED` result | FAIL |
| 8 | Worker tests cover runtime malformed status, empty text, errors, invalid JSON, mixed availability, and clean control, but not malformed JSON object schemas; an uncoercible finding can escape as a Pydantic exception | FAIL |
| 9 | The exact duplicate-position counterexample is repaired in production and regression-tested | PASS |
| 10 | Compile, all 99 tests, exact five tools, 0.4.0/build, option/form/discussion/reconsideration, privacy, persistence, continuation, and budgets remain green | PASS |
| 11 | Docs correctly describe influence normalization, but overclaim that malformed output is unavailable and cannot be interpreted as clean | FAIL |

## Independent verification

| Command/workflow | Result |
| --- | --- |
| `python -m compileall src tests` | PASS, exit 0 |
| `.venv\Scripts\python.exe -m pytest -q --basetemp .tmp\foreman-campaign001-r4 -p no:cacheprovider` | PASS, `99 passed in 1.54s` |
| Focused r4 plus tool-surface suite | PASS, `16 passed in 0.92s` |
| `git diff --check <r4-baseline>..<r4-final>` | PASS, no output |
| Changed-path and complete diff inspection | PASS; ten paths, all authorized |
| Protected hash comparison | PASS; every reported hash matches |
| Empty JSON object repeated for all six reviewers | FAIL; `COMPLETED`, `full`, six successes, `可发布` |
| `findings` as string or `null`, and scalar finding entries | FAIL; each is counted as full structured coverage and returns clean `COMPLETED` |
| Finding with `confidence: "abc"` | FAIL; uncaught `ValidationError` aborts the workflow |
| Valid structured zero-finding control | PASS; `COMPLETED`, full coverage, no manufactured issues |

The allowed r1/r3 package-build evidence remains applicable because r4 changes no package structure or dependency. Live Goose/provider behavior remains unverified and was optional under the r4 contract.

## Findings

| Severity | Finding | Required correction |
| --- | --- | --- |
| Critical | Reviewer coverage is based only on successful JSON-object decoding. Objects that do not satisfy the reviewer response contract (`{}`, missing/non-list `findings`, or non-object finding entries) are counted as successful clean reviews. Six such responses produce `COMPLETED`, full coverage, and `可发布`. | Add bounded semantic validation for the reviewer envelope and finding entries. Only an actual structured reviewer response may increment successful coverage. Malformed object schemas must be unavailable, surface parse/fallback provenance, and force the existing partial/none human-review policy without extra calls. |
| Major | A syntactically valid object containing an uncoercible finding value can raise `ValidationError` out of `_review_findings`, aborting the whole review instead of degrading conservatively. | Catch and normalize per-sample schema/validation failure. Preserve any explicitly chosen safe evidence behavior, but never count that sample as successful coverage or let validation escape. |

## Preserved evidence

- r4 fully repairs the two r3 defects: duplicate same-role influence and transport/parse coverage collapse.
- All r1/r3 passing implementation, package, persistence, privacy, interaction, option identity, policy, and tool-surface evidence remains preserved.
- The complete 99-test suite is green. r5 is a narrow semantic-envelope correction and must not reopen influence normalization or any other V0.4 feature.

## Decision rationale

`CHANGES_REQUESTED` is required because malformed model output can still masquerade as unanimous clean coverage, which is the same safety invariant r4 was intended to close. This is not a blocker: the defect is isolated to reviewer-envelope validation and coverage accounting, with no product decision, provider change, retry, or public API change needed.

## Next action

- Execute `harness/contracts/CAMPAIGN-001-r5.md` from exact baseline `6978c7b76cf7cb8868405a92e05b831deb9e4a09`.
