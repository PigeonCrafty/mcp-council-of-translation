# Campaign Contract: CAMPAIGN-013-r1

## Control

- Harness role: `MAIN WORKER`
- Harness mode: `STRICT_CAMPAIGN`
- Campaign: `CAMPAIGN-013-r1`
- State: `ASSIGNED`
- Repository: `C:\Users\GeZhu\MyMCP\mcp-council-of-translation`
- Baseline commit: `44b1969677cd6b1fda63047ca514aede6609bdad`
- Product target: `0.13.0`
- Diagnostic build target: `calibrated-evidence-council-v11`
- Persisted Review Schema target: `2.6`
- Verification receipt schema target: `1.1`
- Acceptance authority: Foreman only
- Execution ledger: `harness/reports/CAMPAIGN-013-r1-ledger.md`
- Worker report: `harness/reports/CAMPAIGN-013-r1-worker.md`
- Commit policy: exactly five scoped local commits, one for PKG-075 through PKG-079
- Worktree strategy: shared worktree; sequential production-package integration
- Subagent delegation: allowed, not required; maximum three bounded implementation or
  read-only assignments
- Parallel delegation: allowed only for disjoint read-only investigation or disjoint
  test/documentation paths; production files must not be edited concurrently

## Campaign outcome

Add a deterministic categorical assessment of how well the validated Council evidence
supports the actual chief disposition. New reviews expose `well_supported`,
`supported_with_limits`, or `insufficient` with bounded reason codes; old records expose
`not_recorded`. The assessment is not a translation-quality score and does not add model
calls, voting or authority.

## Context

CAMPAIGN-012 and Q-014-r2 are complete with 58/58 accepted features and 14/14 accepted
quality gates. V0.12.1 reliably exposes authoritative execution facts to normal Goose.
The remaining interpretation gap is that users must manually combine context confidence,
coverage, blockers, issue evidence, degradation and chief disposition to determine how
well the result is supported.

Design assessment:
`harness/evaluations/NEXT-CAMPAIGN-013-ASSESSMENT.md`.

## Admission and protected state

Start only if `HEAD` and `origin/main` both equal the exact baseline, the Git index is
empty, and no product/source/test/package diff exists against the baseline. The admitted
worktree deliberately contains Foreman-owned Campaign assets and pre-existing user
assets. Preserve them exactly.

Foreman-owned protected hashes:

| Path | SHA-256 |
| --- | --- |
| `harness/features.json` | `428D7946F5B87E5368D9006EC5C77586A3F3DFB609837B4B34CB9BC323B048D3` |
| `harness/plan.md` | `BF250DF4C2BFF92D2F4EC953C379968427595483F6781247AED8D09643FABB88` |
| `harness/progress.md` | `C28432706FE313A240B8A641DCA02A57443060EFA391E4BA198380CCF8345BFE` |
| `harness/evaluations/NEXT-CAMPAIGN-013-ASSESSMENT.md` | `60570A7A7A8476E8B74F1CF32EB3999229524B1778DFDE9DABCA6C4746A5EDFA` |
| `harness/evaluations/CAMPAIGN-012-q014-live-r2-review.md` | `6207A0DDC7798B61C8B2003FE492BE7312186FC0F781E397730C12293CC6EE6A` |

The launch prompt supplies the final contract SHA-256; verify it before edits. Do not
modify, stage or commit any Harness asset except the two required new Worker report
paths. Do not read, traverse, copy, hash, modify or stage `.learnings/**`, `reviews/**`,
`myTest/**`, the user audit report, or other user-owned untracked content. Do not use raw
live records or Goose prose as fixtures. Synthetic live-shaped records may use only the
bounded facts in accepted evaluations and this contract.

If admission differs, stop before edits with `BLOCKED` and report the exact mismatch.

Foreman issuance evidence on the exact baseline:

- `python -m compileall -q src tests`: passed.
- First repository-venv full run used the Windows system pytest temp root and produced
  `322 passed, 122 errors`; every error was setup-time `PermissionError` while scanning
  `C:\Users\GeZhu\AppData\Local\Temp\pytest-of-GeZhu`, not a product assertion.
- Bounded rerun with a fresh repository-local basetemp: `444 passed in 4.13s` on the
  existing repository venv. The Foreman-created basetemp was removed.
- GitHub issue admission: zero open issues.
- The failed command record is retained here because `.learnings/**` is protected.

## Frozen design

### Architecture and invariants

- Public MCP tools remain exactly five and in the existing order.
- Defaults remain review-only, interactive `auto`, briefing `auto`, trace `summary`,
  history `full`, and Council adjudication fallback.
- Sampling budgets remain 6/13/18; independent-review concurrency remains 1..3 with
  default and maximum 3.
- Routing profiles, role portfolios, reviewer prompts, deterministic preflight, issue
  identity/clustering, concrete outcome eligibility, user authority, Policy Gate,
  reconsideration targeting and normal provider behavior remain unchanged except the
  explicit one-way insufficient-evidence safety tightening below.
- Assessment is deterministic and sampling-free. It reads only validated structured
  trace data already present before digest/persistence and never reads free source,
  candidate, context, audience, note, reviewer-feedback or evidence prose.
- Reviewer/model numeric `confidence` is never aggregated, averaged, thresholded or
  exposed as the product assessment.
- New reviews write Schema 2.6 once; the assessment is computed after chief adjudication,
  before final status/digest/persistence, and does not add a second save.
- Normal primary text remains exactly five sections and at most 3,200 Unicode code
  points. The final disposition remains exactly once and last.

### Exact `DecisionSupportAssessment` contract

Schema 2.6 adds this field to `ReviewRecordV2` after `council_value_metrics` and before
`display_report`:

```text
decision_support:
  level: "well_supported" | "supported_with_limits" | "insufficient" | "not_recorded"
  support_target: "chief_disposition"
  basis_codes: list[DecisionSupportBasisCode]
  limitation_codes: list[DecisionSupportLimitationCode]
  assessment_basis: "deterministic_structured_trace_v1" | "not_recorded"
  outcome_coherent: boolean | null
```

Lists are unique, bounded to their complete vocabulary and serialized in the canonical
order below. Unknown values fail validation for new records and are conservatively
redacted/unrecorded in compatibility or hostile receipt paths.

`DecisionSupportBasisCode` canonical order:

1. `full_reviewer_coverage`
2. `clean_confirmation`
3. `structured_material_evidence`
4. `corroborated_material_evidence`
5. `deterministic_blocker`
6. `policy_gate_enforced`
7. `valid_user_decision`
8. `completed_reconsideration`
9. `council_adjudication`

`DecisionSupportLimitationCode` canonical order:

1. `minimal_context`
2. `partial_context`
3. `material_disagreement`
4. `council_fallback`
5. `reviewer_unavailable`
6. `partial_reviewer_coverage`
7. `no_reviewer_coverage`
8. `unresolved_material_context`
9. `pending_user_input`
10. `incomplete_reconsideration`
11. `degraded_execution`
12. `runtime_fallback`

`not_recorded` requires empty code lists, `assessment_basis="not_recorded"` and
`outcome_coherent=null`. New Schema 2.6 full/metadata records require
`assessment_basis="deterministic_structured_trace_v1"` and a boolean coherence result.

### Deterministic classification truth table

Apply this precedence without score arithmetic:

1. `insufficient` if any of these is true:
   - status is `RETURNED_PENDING` or required briefing/user input is pending;
   - a selected material context gap remains unanswered, assumed, declined, cancelled,
     unsupported, malformed or errored;
   - reviewer coverage is `partial` or `none`, or an active reviewer is unavailable;
   - a requested materially affected reconsideration failed, was skipped for budget, or
     did not complete;
   - `degraded=true`; or
   - a runtime fallback is recorded other than the explicit non-degraded
     `user_delegated_to_council` path.
2. Otherwise `well_supported` when a deterministic preflight/Policy Gate blocker
   coherently yields `需人工复核 / 是`, even if model findings also exist.
3. Otherwise `supported_with_limits` when at least one validated material issue,
   unresolved material disagreement, minimal/partial but non-material context limitation,
   or non-degraded Council delegation/fallback remains.
4. Otherwise `well_supported` for full structured clean/affirming coverage.
5. A valid user decision with full coverage, no unresolved material context, completed
   required reconsideration and no degradation is `well_supported` when the decision
   resolves the material choice; remaining material disagreement makes it
   `supported_with_limits`.
6. A full-coverage critical model-only issue that requires human review but lacks a
   deterministic blocker is `supported_with_limits`, not `insufficient`.

Canonical codes record every applicable structured basis/limitation without changing
the precedence result. `minimal_context` or `partial_context` alone limits support but
does not make it insufficient unless an actual material gap is unresolved.

### One-way safety tightening and coherence

- If the derived level is `insufficient` while chief output is more permissive than
  `需人工复核 / 是`, normalize only `publishability`, `review_needed` and a bounded
  canonical review reason to human review before status/digest/persistence.
- Never change `must_fix`, `should_fix`, optional improvements, terminology decisions,
  conflict resolutions, execution order, suggested translation or a recorded valid user
  choice.
- `well_supported` and `supported_with_limits` are descriptive and can never upgrade or
  downgrade chief output.
- For insufficient support, coherence is true only when final chief is
  `需人工复核 / 是` and status is `NEEDS_HUMAN_REVIEW` or `RETURNED_PENDING`.
- For the other current levels, coherence is true only when the canonical terminal line,
  structured chief and existing status rules agree. `not_recorded` uses null.
- A false coherence result must be visible in full/verification history and must not be
  silently rewritten during retrieval.

### Persistence and compatibility

- New full records persist the exact assessment. New metadata records retain only this
  content-free assessment object plus existing allowlisted metadata.
- V1 and V2.0 through V2.5 full/metadata records load with exact `not_recorded` semantics;
  compatibility defaults must not be presented as historical observations.
- Reading, listing or verification retrieval never computes and writes an assessment
  back into an old record.
- Schema 2.6 readers remain compatible with every currently supported historical schema;
  writers always write 2.6.

### Normal primary presentation

Add at most one line in `## 主编结论`, immediately before the terminal disposition:

- `well_supported`: begin `- 结论依据：充分；`
- `supported_with_limits`: begin `- 结论依据：有限制；`
- `insufficient`: begin `- 结论依据：不足；`
- `not_recorded`: omit the line from legacy-rendered normal reports

The suffix is deterministic, Chinese, derived from the highest-priority bounded reason
codes, at most 160 Unicode code points and contains no raw code, count padding, source,
candidate or model prose. It must make clear that the line supports the disposition, not
candidate correctness. Existing material work items, warnings, blind spots and role
coverage remain visible. Terminal disposition remains once and last.

### Verification receipt 1.1

Receipt 1.1 retains every 1.0 field unchanged and inserts this top-level object after
`outcome` and before `coherence`:

```text
decision_support:
  level: string | null
  support_target: "chief_disposition" | null
  basis_codes: list[string] | null
  limitation_codes: list[string] | null
  assessment_basis: string | null
  outcome_coherent: boolean | null
```

For current full and metadata Schema 2.6 records, it exactly matches the persisted
assessment. For historical records, values reflect `not_recorded` semantics and exact
dotted paths appear in `availability.not_recorded_fields`; no value is inferred.
Structured receipt and the compact text JSON remain exactly equal. Receipt projection
remains one load, zero saves, zero sampling, zero elicitation and no mutation. The
verification human text adds one bounded decision-support line without losing its five
headings or 3,200-code-point cap.

`get_server_info()` advertises Review Schema `2.6` and verification receipt Schema `1.1`.
Every other diagnostic/default/tool field remains unchanged except V0.13 identifiers.

### Main Worker implementation discretion

- Private module/function names and safe internal helper decomposition.
- Whether code enums are `Literal`, `Enum` or validated constants, provided JSON values,
  canonical order and rejection behavior exactly match this contract.
- Exact deterministic Chinese suffix wording within the frozen meaning and 160-code-point
  bound.
- Synthetic fixture builders and internal test parametrization.
- Whether the assessment module is new or implemented beside value metrics, provided
  package/file scope, phase order and independence are preserved.

### Decisions reserved for Foreman or user

- Any numeric score/probability, new level/code, changed precedence or bidirectional
  adjudication authority.
- Any sixth MCP tool, new role/prompt/provider/model call, budget, concurrency setting,
  dynamic routing or public parameter.
- Any expansion into file/batch translation, TM/TB/SG ownership or edit application.
- Q-015 issuance, live Goose/provider calls, publication, release, deployment and
  Campaign acceptance.

## Global boundaries

### Authorized production and package paths

- `src/council_of_translation/localization/decision_support.py` (new, optional location)
- `src/council_of_translation/localization/models.py`
- `src/council_of_translation/localization/orchestration.py`
- `src/council_of_translation/localization/digest.py`
- `src/council_of_translation/localization/persistence.py`
- `src/council_of_translation/localization/compatibility.py`
- `src/council_of_translation/localization/verification.py`
- `src/council_of_translation/localization/__init__.py`
- `src/council_of_translation/evaluation.py`
- `src/council_of_translation/tools/review.py`
- `src/council_of_translation/__init__.py`
- `tests/fixtures/v24_golden_corpus.json`
- `AGENTS.md`
- `README.md`
- `docs/v0.4-architecture.md`
- `docs/v0.4-tool-contract.md`
- `pyproject.toml`
- `uv.lock`

### Authorized test paths

- `tests/unit/test_decision_support.py` (new)
- `tests/integration/test_v26_decision_support.py` (new)
- `tests/unit/test_models_v2.py`
- `tests/unit/test_persistence_v2.py`
- `tests/unit/test_v22_models_persistence.py`
- `tests/unit/test_v24_models_persistence.py`
- `tests/unit/test_verification_receipt.py`
- `tests/integration/test_orchestration_v2.py`
- `tests/integration/test_r4_reviewer_coverage.py`
- `tests/integration/test_r5_reviewer_envelopes.py`
- `tests/integration/test_tool_surface_v2.py`
- `tests/integration/test_v07_dual_channel.py`
- `tests/integration/test_v08_context_precedence.py`
- `tests/integration/test_v08_presentation_invariants.py`
- `tests/integration/test_v10_release_contract.py`
- `tests/integration/test_v11_routing.py`
- `tests/integration/test_v12_verification_view.py`
- `tests/integration/test_v21_reconsideration.py`
- `tests/integration/test_v22_briefing.py`
- `tests/integration/test_v22_context_gaps.py`
- `tests/integration/test_v22_digest.py`
- `tests/integration/test_v24_golden_corpus.py`
- `tests/integration/test_v24_presentation.py`
- `tests/integration/test_v24_value_metrics.py`
- `tests/integration/test_v25_risk_routing.py`

### Authorized Worker evidence paths

- `harness/reports/CAMPAIGN-013-r1-ledger.md` (new, untracked/unstaged)
- `harness/reports/CAMPAIGN-013-r1-worker.md` (new, untracked/unstaged)
- `.tmp/campaign013-worker/**` for bounded temporary verification only; remove it before
  handoff

### Forbidden paths and systems

- Every path not explicitly authorized above
- All existing `harness/**` other than the two new Worker reports
- `.learnings/**`, `reviews/**`, `myTest/**`, the user audit report and all other
  user-owned untracked content
- Goose installation/configuration, provider/model/account settings and credentials
- GitHub, remote branches, PRs, releases, deployments and package publication

### Non-goals

- Numeric confidence, calibration percentages, scores or user-configurable thresholds
- Reviewer-confidence averaging, voting, role weighting or hidden reasoning
- New findings, issue families, fuzzy matching, roles, prompts or model calls
- New decision options or interaction forms
- Raw assessment codes in the normal Council report
- Translating files, applying edits or owning caller retrieval/memory

### Authorized external and cleanup actions

- Local dependency sync, test, build and isolated-wheel installation required below; use
  repository-local or exact OS temporary directories and never expose credentials.
- Install/use exact `uv 0.12.3` if unavailable. Record each dependency operation.
- Delete only Worker-created `.tmp/campaign013-worker/**` or exact ephemeral build/smoke
  directories after resolving and verifying their absolute paths. Do not clean unrelated
  caches or user directories.
- Local Git staging and exactly five local commits are required. No push or remote
  mutation is authorized.

## Task graph

| Package | Feature | Observable outcome | Depends on | Authorized boundary | Parallel-safe |
| --- | --- | --- | --- | --- | --- |
| PKG-075 | F-059 | Exact model/code vocabulary plus total deterministic classifier and truth-table unit evidence | none | models; optional decision-support module; new unit test | no |
| PKG-076 | F-060 | Phase-ordered integration, one-way tightening, persistence and historical/metadata compatibility | PKG-075 | orchestration, persistence, compatibility, model/persistence/integration tests | no |
| PKG-077 | F-061 | One-line normal presentation and matching receipt 1.1 structured/text projections | PKG-076 | digest, verification, review tool and presentation/receipt/tool tests | no |
| PKG-078 | F-062 | Exact 30-case executable Golden corpus and calibration/negative metrics | PKG-077 | evaluation, corpus and authorized integration tests only | no |
| PKG-079 | F-063 | V0.13 identifiers, docs, root-only lock, fresh artifacts and installed-wheel proof | PKG-078 | version/docs/package/lock and authorized release tests | no |

## Collision and integration map

| Packages/files at risk | Required sequencing | Integration check |
| --- | --- | --- |
| PKG-075/076 models and classifier integration | freeze model/codes first; orchestration only after classifier unit truth table passes | rerun both package suites after PKG-076 |
| PKG-076/077 orchestration, digest and receipt coherence | persist finalized assessment before rendering either channel | compare record/full/normal/receipt assessment and terminal outcome |
| PKG-077/079 review diagnostics and release tests | receipt 1.1 behavior before version migration | focused tool/receipt/release suite after each commit |
| PKG-078 corpus and runtime path | no production edits in PKG-078 | exact production runner, 30/30 and all metrics |
| `uv.lock` | PKG-079 only, exact pinned canonical refresh | root-only semantic diff and 3/78/586 invariants |

Main Worker owns every integration decision and must inspect each package diff before the
next package begins. Subagents may not edit overlapping paths or accept work.

## Package acceptance details

### PKG-075 — deterministic contract

- Direct truth-table tests cover every classification rule and precedence collision,
  including deterministic blocker plus model issue, unresolved context plus blocker,
  degraded clean review, non-degraded user delegation and valid user decision.
- Unknown/duplicate/out-of-order codes normalize or reject exactly as frozen; no prose or
  numeric confidence affects output.
- Classification is total, deterministic and adds zero executor/gateway calls.

### PKG-076 — coherence and compatibility

- All parent and continuation terminal paths persist exactly one Schema 2.6 assessment;
  one-way tightening occurs before status/digest/save and cannot erase checklist content.
- Partial/zero coverage, pending briefing/outcome, unresolved context and failed/budgeted
  reconsideration are insufficient and never publishable.
- Full-coverage deterministic blocker remains well supported while human review stays
  mandatory. Full-coverage critical model-only risk remains supported with limits.
- V1/V2.0-V2.5 full/metadata reads are not recorded; V2.6 metadata round-trips only safe
  assessment fields.

### PKG-077 — presentation and receipt

- Clean/edit/blocker/insufficient primary reports each render the correct one-line label;
  blocker wording explicitly supports the negative disposition rather than candidate
  correctness.
- Five headings, all existing material content, role accounting, 1,200 clean target,
  3,200 hard cap and one-last terminal disposition remain.
- Receipt 1.1 text JSON parses exactly equal to structured content; V1/V2.0-V2.5
  availability is truthful; retrieval remains pure.

### PKG-078 — executable evaluation

- Corpus contains exactly the prior 24 cases unchanged plus six named calibration cases
  executed through production orchestration; fixtures contain no `observed` data.
- Existing eight aggregate metrics remain exactly 1.0.
- New `decision_support_accuracy` and `support_disposition_coherence` are exactly 1.0;
  `insufficient_false_reassurance_rate` is exactly 0.0.
- Mutating any expected support level or permissive-insufficient outcome produces the
  expected failed case/property.

### PKG-079 — release migration

- Package/module become `0.13.0`, build becomes `calibrated-evidence-council-v11`, Review
  Schema becomes `2.6` and receipt Schema becomes `1.1`.
- `uv 0.12.3` canonical refresh changes only editable root version
  `0.12.1 -> 0.13.0`; lock revision 3, package count 78 and 586 upload-time entries remain.
- Docs distinguish context confidence, coverage, support level and publishability and
  explicitly reject numeric/model-self-confidence interpretations.

## Campaign acceptance criteria

1. F-059 through F-063 meet every feature/package criterion without modifying a frozen
   product invariant.
2. Every level and reason code matches the exact contract and precedence; no unbounded
   text or score is stored or rendered.
3. Insufficient evidence never produces a permissive terminal disposition; no other
   level changes chief authority.
4. Record, normal report, full/metadata history and receipt 1.1 remain mutually coherent,
   privacy-safe and historical-truthful.
5. Existing public tools, routing, sampling, issue identity, user decisions, Policy Gate,
   budgets, concurrency and review-only safety remain stable.
6. Exact 30-case Golden and complete source/artifact/installed-wheel evidence pass with
   no skipped required check.
7. Changes stay in the exact allowlist and are split across exactly five scoped commits.
8. Worker reports risks and evidence but makes no acceptance, publication, Q-015 or
   project-completion claim.

## Required Campaign verification

Run and report at minimum:

1. Admission compile and complete baseline suite with a unique repository-local
   basetemp; expected admitted baseline is exactly 444 passing tests.
2. PKG-075 complete direct classification truth table, code validation/order and
   no-confidence/no-prose counterexamples.
3. PKG-076 parent/continuation, coverage, context, pending, degraded, fallback,
   reconsideration, blocker and compatibility matrices.
4. PKG-077 five-section presentation, cap/privacy, dual-channel receipt equality,
   historical availability and retrieval-purity matrix.
5. PKG-078 exact 30/30 executable Golden corpus, all prior eight metrics, three new
   calibration metrics and mutation-detection tests.
6. Complete affected orchestration/persistence/presentation/verification/routing/tool/
   release invariant matrix.
7. Final `python -m compileall -q src tests` and complete suite with zero failures and no
   reduction from the 444-test admitted baseline.
8. Exact five-tool order; package/module/build, Schemas 2.6/1.1, defaults, budgets
   6/13/18, concurrency 3/3 and all 15 routing profiles.
9. Programmatic proof that assessment adds no sampling/elicitation, and verification
   retrieval remains one load, zero saves, zero execution and byte-immutable.
10. `git diff --check`, exact baseline-to-final path audit, dead-import scan, index empty
    and every protected hash exact.
11. Fresh wheel and sdist build plus archive inspection.
12. Isolated CPython 3.12/current FastMCP wheel-origin smoke calling all five tools and
    proving clean/limited/insufficient/blocker assessment coherence in installed code.

Use a unique repository-local basetemp/cache for the known Windows host temp permission
defect. Record deviations and bounded reruns. Do not hide, delete or weaken a failing
test to improve the count.

## Required evidence and handoff

- Maintain the ledger mapping every package to executor/subagent, files, commit,
  commands, results, deviations and integration state.
- Record baseline/final HEAD, exact five commits, changed-file list/stat and complete
  diff inspection.
- Record all subagents, authority/escalation requests, dependency operations, cleanup,
  live calls and external mutations, including zero counts.
- Record fresh artifact names, sizes and SHA-256 values and prove isolated imports came
  from site-packages rather than the workspace.
- Record skipped checks with consequences; required checks may not be silently skipped.
- Preserve secrets and user data; use only content-free synthetic sentinels in reports.
- Leave `harness/reports/CAMPAIGN-013-r1-ledger.md` and
  `harness/reports/CAMPAIGN-013-r1-worker.md` untracked and unstaged. Git index must be
  empty at handoff.

In chat, start with exactly `READY_FOR_REVIEW` or `BLOCKED`, then summarize report and
ledger paths, contract hash, baseline/final state, commits/files, package and Campaign
verification, artifacts, skipped checks, protected hashes, subagent/authority/dependency/
live-call counts and remaining risks or blockers. Stop after the handoff. Do not claim
Campaign acceptance or Q-015 completion.

## Stop conditions

Stop with `BLOCKED` rather than guessing if:

- baseline, index, contract hash or any protected asset differs;
- a frozen level/code, precedence, schema, receipt field or one-way authority rule would
  need to change;
- implementation needs any path outside the exact allowlist;
- assessment would require free-prose inference, numeric/model confidence, a new model
  call, role, tool, budget, interaction or dynamic routing;
- normal report/full/summary behavior, issue identity, user authority, Policy Gate,
  routing, sampling, persistence count, tool count, budgets or concurrency regress;
- privacy tests expose source/candidate/model prose, paths, secrets or internal IDs;
- lock regeneration changes anything beyond the exact root version or loses revision,
  package or upload-time invariants;
- a required check, build or installed-wheel smoke cannot establish the result; or
- work requires live Goose/provider/model calls, publication, push, PR, release,
  deployment, credentials, destructive cleanup or other unapproved authority.
