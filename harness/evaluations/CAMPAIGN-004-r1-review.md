# Campaign Foreman Review: CAMPAIGN-004-r1

## Control

- Role: FOREMAN
- Mode: STRICT_CAMPAIGN
- Decision: `CHANGES_REQUESTED`
- Contract: `harness/contracts/CAMPAIGN-004-r1.md`
- Campaign Worker report: `harness/reports/CAMPAIGN-004-r1-worker.md`
- Execution ledger: `harness/reports/CAMPAIGN-004-r1-ledger.md`
- Reviewed baseline: `b601cf93f452a8e574e3c15a4a9c236cf8142ce1`
- Reviewed final state: `ff0e345ff174f1f39741bbb47979aa51e277ca52`
- Contract SHA-256: `8A77DDCEB46339632D12603D5AA62CA1C5E39FEED8A1B250161DEA2A0E8B7C03`
- Worker report SHA-256: `B72FFBDC1128FEBBD0749391C127DAFC7C13DA71B92EC0E65614A4E246A05063`
- Ledger SHA-256: `DA1E93244868D1B8ABDE32002346D72B87AE48C0B63EFED1957509550A26684B`

## Scope and repository review

- Complete baseline-to-final diff inspected: yes; 19 files, 760 insertions and 110 deletions.
- Global boundary and non-goal compliance: the committed diff stayed within the r1 allowlist; no new tool, public argument, dependency, schema or model call was added.
- User changes preserved: all fourteen protected hashes matched independently.
- Commit/worktree policy compliance: five scoped commits, empty index, only declared Foreman/user dirt and the two authorized Worker reports remain.
- Required Worker capability and delegation-policy compliance: Main Worker completed all packages directly; subagents 0 of 2 allowed.
- External/destructive action compliance: no live Goose/model/provider call, push, PR, release, deployment or credential action.
- Resume/retry and side-effect safety: reported failed test/build probes were local and corrected without repeated external side effects.
- Sensitive evidence hygiene: no raw live record, credentials, private paths or user/model corpus was added to the committed diff or reports.

## Task graph review

| Package | Boundary/dependency review | Worker evidence | Foreman verification | Package result |
| --- | --- | --- | --- | --- |
| PKG-023 | Adapter and three tool paths changed after the declared baseline | Actual FastMCP calls, 10 focused passes, dual-version wheel smoke | Source/diff inspected; actual tool tests and full suite passed | PASS |
| PKG-024 | Renderer followed PKG-023 and stayed in digest/orchestration/tests | Clean, disputed/degraded/pending and hostile probes | Renderer inspected; clean/five-section/final-line/length probes passed | PASS |
| PKG-025 | Consensus and lenses followed renderer interface | Six-affirmation and partial-coverage tests | Positive consensus and conservative partial coverage reproduced | PASS |
| PKG-026 | Integrity tests cover mapping, privacy and layered retrieval | 54 focused passes; sampling 6 to 6 | Tone/focus mapping and primary/structured paths passed, but internal-ID sanitizer has uncovered forms | PARTIAL |
| PKG-027 | Version/docs/build completed after behavior packages | 0.7.0 source/wheels and FastMCP 2.13/3.4.7 smoke | Public diagnostics pass, but metadata-history projection still emits V0.6 identifiers | FAIL |

## Campaign acceptance review

| Criterion | Foreman verification | Result |
| --- | --- | --- |
| 1-8 | Dual-channel tool calls, adaptive sections, length, lenses, consensus and conditional interactions pass | PASS |
| 9 | `cluster_deadbeef` and uppercase `POSITION_F00DBABE` survive `_human_line` into primary text | FAIL |
| 10-14 | Degradation, pending state, field sentinels, retrieval compatibility, authority and zero-sampling presentation pass | PASS |
| 15 | Public info and full-record defaults are V0.7, but metadata projection writes `0.6.0 / guided-deliberation-v4` | FAIL |
| 16-17 | Worker dual-wheel evidence is credible and fresh; independent 196-test suite passes | PASS |
| 18 | Compile/tests/diff/scope/protection pass; exact version scan fails in active metadata persistence | FAIL |
| 19-20 | Documentation and normal-user Goose recipe match the intended V0.7 surface | PASS, subject to correcting persisted metadata truth |

## Independent integration verification

| Command/workflow | Result |
| --- | --- |
| `git diff --name-status/stat/check b601cf9..ff0e345` | 19 authorized files; diff check passed |
| Contract and fourteen protected SHA-256 checks | exact; mismatch count 0 |
| `.venv\Scripts\python.exe -m pytest -q --basetemp .tmp\foreman-c004-full -p no:cacheprovider` | `196 passed in 2.56s` |
| `python -m compileall -q src tests` | passed |
| Maximal structured renderer plus dual-channel footer probe | 2,520/2,593 code points; final disposition retained in this reachable constructed case |
| Internal identifier adversarial probe | `cluster_deadbeef` and `POSITION_F00DBABE` leaked into primary text; `decision_DEADBEEF` alone was filtered |
| V0.7 metadata projection probe | record defaults were V0.7, but metadata projection returned V0.6 package/build twice |

The first metadata probe used an incomplete record fixture and failed Pydantic validation before exercising persistence. It was corrected by supplying the required `ReviewTaskV2`; the corrected probe produced the failure above. No product or protected asset was changed by either read-only probe.

## Delegation and integration audit

- Package/subagent/file/commit mapping reconciled: yes; the five commits map cleanly to PKG-023 through PKG-027.
- Frozen interface and dependency compliance: yes.
- Collision/conflict handling: no parallel or subagent collision occurred.
- Main Worker verification independently checked: full test, compile, scope, hashes, renderer, sanitizer and metadata projection were checked.
- Ledger/report/repository consistency: consistent except the report correctly disclosed the four stale persistence literals as a remaining risk; that risk is acceptance-blocking rather than waivable.

## Findings

| Severity | Package/criterion | Finding and evidence | Required correction |
| --- | --- | --- | --- |
| High | PKG-027 / criteria 15 and 18 | `_metadata_projection` in `localization/persistence.py` hard-codes `0.6.0` and `guided-deliberation-v4` in both `runtime_metadata` and `version_metadata`. New V0.7 metadata-history records therefore misidentify their producer. | Authorize and update only the V0.7 metadata projection; derive or centralize identifiers safely and add persisted-file regression coverage. Do not rewrite old records. |
| Medium | PKG-026 / criterion 9 | `_human_line` filters only lowercase `decision|option|issue|gap` identifiers. A direct renderer probe displayed `cluster_deadbeef` and `POSITION_F00DBABE`. | Use one case-insensitive bounded sanitizer covering all internal entity/hash families that can reach primary text; preserve ordinary source tokens and review ID footer; add adversarial tests across all rendered fields. |

## Preserved evidence

- PKG-023, PKG-024 and PKG-025 are accepted as package evidence.
- PKG-026 evidence for tone/focus mapping, privacy, layered retrieval, zero added sampling, warning/degradation visibility and report bounds remains valid.
- PKG-027 evidence for public version info, five tools, schema 2.2, 6/13/18 budgets, fresh artifacts, documentation and FastMCP 2.13.0.2/3.4.7 dual-channel behavior remains valid.
- The 196-test integrated baseline remains the admission expectation for the correction revision.

## Decision rationale

The principal V0.7 presentation architecture works and materially addresses the user's complaint. Acceptance is withheld because a newly written history mode reports a false product version and the primary-text sanitizer does not satisfy the frozen no-internal-ID contract. Both defects are deterministic, independently reproduced and bounded to two small surfaces. A correction revision can preserve all other package evidence.

## User audit index

- Contract: `harness/contracts/CAMPAIGN-004-r1.md`
- Worker report and ledger: `harness/reports/CAMPAIGN-004-r1-worker.md`, `harness/reports/CAMPAIGN-004-r1-ledger.md`
- Baseline-to-final commits: `eda3dee`, `1bbe03e`, `150408d`, `d47ddd9`, `ff0e345`
- Independent evidence: commands and counterexamples recorded above
- Remaining live risk: normal-user Goose Q-009 still requires post-acceptance validation; it is not the cause of this revision.

## Next action

Issue `CAMPAIGN-004-r2` at exact baseline `ff0e345ff174f1f39741bbb47979aa51e277ca52`, authorizing only the metadata version projection, primary-text identifier sanitizer, focused tests and necessary documentation correction. Preserve all r1 package evidence and do not rerun live Goose or provider calls.
