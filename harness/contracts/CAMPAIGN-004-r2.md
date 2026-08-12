# Campaign Contract: CAMPAIGN-004-r2

## Control

- Role: MAIN WORKER
- Mode: STRICT_CAMPAIGN
- State: ASSIGNED
- Repository: `C:\Users\GeZhu\MyMCP\mcp-council-of-translation`
- Baseline commit: `ff0e345ff174f1f39741bbb47979aa51e277ca52`
- Baseline subject: `Release concise Council display contract`
- Prior contract: `harness/contracts/CAMPAIGN-004-r1.md`
- Prior review: `harness/evaluations/CAMPAIGN-004-r1-review.md`
- Required report: `harness/reports/CAMPAIGN-004-r2-worker.md`
- New ledger: not required; preserve the r1 ledger unchanged
- Commit policy: one or two scoped local commits; no push, PR, release, deployment or branch-protection change
- Subagents: forbidden; this is a bounded correction
- Acceptance authority: Foreman only

Read `AGENTS.md`, `harness/plan.md`, `harness/features.json`, `harness/progress.md`, this contract, the r1 contract/report/ledger and r1 Foreman review completely before editing. Repository assets override conversation memory.

## Admission gate

Before any edit:

1. verify exact HEAD and subject above;
2. verify the Git index is empty;
3. verify only the declared Foreman/user/r1 evidence dirt is present;
4. verify this contract and every protected hash below byte-for-byte;
5. run `python -m compileall -q src tests`;
6. run the full suite with repository-local basetemp and cache disabled; expected admission is exactly `196 passed`;
7. reproduce both r1 Foreman counterexamples before changing code.

Stop `BLOCKED` on unexplained drift. Do not repair, stage, rewrite, delete, move or commit protected assets.

| Protected asset | SHA-256 |
| --- | --- |
| `harness/plan.md` | `0040EDBD2B7F0C43E7232020054E77F6A13DE0E87A2719D51734150A6F0C0488` |
| `harness/features.json` | `64FF41F3DCF43F4226031560935F0F4D8F66B1606D66825234771647320F47D1` |
| `harness/progress.md` | `6DF4D0C6FA9439028448464E8AE48FC509E2B98CE293A96A3CEDBAA13D719302` |
| `harness/evaluations/CAMPAIGN-004-r1-review.md` | `71A76DAB54D57B2A77589056204F7986264C4D5EE1CCE6E5EBFB5A4F38BCA092` |
| `harness/contracts/CAMPAIGN-004-r1.md` | `8A77DDCEB46339632D12603D5AA62CA1C5E39FEED8A1B250161DEA2A0E8B7C03` |
| `harness/reports/CAMPAIGN-004-r1-worker.md` | `B72FFBDC1128FEBBD0749391C127DAFC7C13DA71B92EC0E65614A4E246A05063` |
| `harness/reports/CAMPAIGN-004-r1-ledger.md` | `DA1E93244868D1B8ABDE32002346D72B87AE48C0B63EFED1957509550A26684B` |
| `harness/evaluations/CAMPAIGN-003-q008-q009-live-review.md` | `6F3E0D30907F7A84B52449A1CD62572EBD121E43E50C04987B33928A5833CD31` |
| `.learnings/LEARNINGS.md` | `22F939E6F980DF52487AAFE97EDCA9B90CF3931DDB7A31BF8A5BBB8F052E658F` |
| `.learnings/ERRORS.md` | `F99EB75886781958BF5AE6DCF844FD476CBCA45937896A25EE3B2E9D6CD34F0A` |
| audit Markdown | `B48073E063C4C9F34E0B6B4DAE94E80079EAAAD3B2F8E273DD60B2F25F6ABD76` |

Preserve `.learnings/**`, `reviews/**`, the audit Markdown, `myTest/**` if present, every prior Harness asset and all user files. Only the required r2 Worker report may be created under Harness.

## Preserved r1 evidence

Do not redesign or reimplement accepted r1 behavior. The following evidence remains valid unless the correction changes it:

- PKG-023 dual-channel results on three human-facing tools and exact five-tool surface;
- PKG-024 adaptive Chinese renderer, section order and 1,800/3,200 bounds;
- PKG-025 six distinct lenses and truthful positive consensus;
- PKG-026 tone/focus round-trip, layered retrieval, privacy, review-only, degradation and zero additional sampling;
- PKG-027 public V0.7 diagnostics, schema 2.2, budgets 6/13/18, docs, artifacts and FastMCP 2.13.0.2/3.4.7 compatibility.

## Correction outcome

Make new V0.7 metadata-only history truthful and make every user-facing primary Council report reject internal entity/hash identifiers independent of case or rendered field. Preserve normal translation tokens, placeholders and the explicitly permitted review-ID footer. Do not rewrite existing history files.

## Frozen correction design

### PKG-028: truthful V0.7 metadata projection

- Replace the four active V0.6 literals in `_metadata_projection` for newly written metadata records.
- Both `runtime_metadata` and `version_metadata` must report package `0.7.0` and diagnostic build `concise-council-display-v5`; schema remains `2.2`.
- Prefer a single local source of truth or existing validated V0.7 record metadata instead of duplicating four drifting literals, while preserving the metadata privacy allowlist.
- `history_mode=full` and `off`, legacy reads, file naming, atomic writes and existing records do not change.
- Add a real save/read-JSON regression for `history_mode=metadata`; do not test only the private helper.

### PKG-029: unified primary-text internal-ID sanitizer

- Apply one deterministic, bounded sanitizer to every string that can reach `display_report` primary text: background, role perspective/evidence, consensus, disagreements, blind spots, minority/condition, interaction, editor synthesis and checklist.
- Matching is case-insensitive and covers at least `issue_`, `cluster_`, `position_`, `decision_`, `option_`, and `gap_` followed by identifier/hash characters.
- Sanitization must also prevent raw role IDs and the established implementation labels already forbidden by r1.
- Do not erase ordinary words containing those substrings, legitimate source/candidate tokens, placeholders such as `{count}`, or the review ID shown by the presentation footer.
- Preserve material warnings, blockers, minority conditions, degradation and the final disposition.
- Add adversarial tests that place mixed-case internal identifiers in every rendered field family and assert none survives.

## Allowed paths

- `src/council_of_translation/localization/persistence.py`
- `src/council_of_translation/localization/digest.py`
- `tests/unit/test_persistence_v2.py`
- `tests/unit/test_v07_report.py`
- `tests/integration/test_v07_integrity.py`
- `tests/integration/test_v07_dual_channel.py` only if the footer/non-regression boundary needs a direct assertion
- required new `harness/reports/CAMPAIGN-004-r2-worker.md`

## Forbidden paths and non-goals

- All other production, test, documentation, package and configuration files.
- All Foreman assets, prior contracts/evaluations/reports/ledgers and user assets.
- No tool, argument, schema, dependency, version, build, budget, sampling, role, prompt, adjudication, policy, elicitation, persistence format or privacy-allowlist redesign.
- No rewrite/migration of existing record files.
- No live Goose/model/provider call, credential, network-dependent compatibility rerun, push, PR, tag, release or deployment.

## Acceptance criteria

1. A newly saved `history_mode=metadata` V2.2 JSON file reports `0.7.0` and `concise-council-display-v5` in both runtime and version metadata.
2. Metadata projection still excludes source text, candidate translation, user answers, model prose, findings, display report, warnings and fallback text.
3. Full/off history modes and V1/V2.0/V2.1/V2.2 reads remain unchanged.
4. Mixed/lower/upper-case internal IDs for all six named families are absent from every primary report section and the dual-channel first text block.
5. Ordinary source/candidate tokens, `{count}`, material blocker/minority/degradation language and the permitted review-ID footer remain visible.
6. Final disposition remains the last substantive report line and primary content remains <=3,200 code points.
7. The public surface remains exactly five tools; package/module 0.7.0, build `concise-council-display-v5`, schema 2.2 and budgets 6/13/18 remain exact.
8. Presentation adds no sampling and structured content remains complete.
9. All 196 r1 tests plus new focused regressions pass; no useful assertion is deleted or weakened.
10. Compile, diff/scope check, fresh 0.7.0 artifact build, isolated current-environment wheel smoke, protected hashes and repository hygiene pass.

## Required verification

- Reproduce before/after:
  - metadata projection returns V0.6 before and V0.7 after;
  - `cluster_deadbeef` and `POSITION_F00DBABE` appear before and are absent after.
- Run focused persistence/report/integrity/dual-channel tests.
- Run `python -m compileall -q src tests`.
- Run the complete suite with repository-local basetemp and cache disabled.
- Run `git diff --check ff0e345ff174f1f39741bbb47979aa51e277ca52..HEAD` and an exact allowed-path audit.
- Build a fresh wheel/sdist in repository-local ignored output, install the wheel in one fresh repository-local environment using the current resolved FastMCP, and smoke the metadata JSON plus primary/structured result. Reuse r1 evidence for FastMCP 2.13; no network-dependent second compatibility environment is required.
- Recheck all protected hashes and ensure the index is empty.

If a build or environment operation fails, diagnose once and record the consequence. Do not change dependencies or expand scope to repair the host.

## Handoff

Write `harness/reports/CAMPAIGN-004-r2-worker.md`. Start the conversational handoff with exactly `READY_FOR_REVIEW` or `BLOCKED`, then report contract hash, baseline/final HEAD, commits/files, both counterexample outcomes, focused/full/build/wheel results, protected hashes, index/worktree state, authority escalations, live/external call counts, deviations and remaining risks. Do not push or claim Campaign acceptance/project completion.
