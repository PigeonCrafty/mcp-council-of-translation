# Campaign Contract: CAMPAIGN-014-r1

## Control

- Harness role: `WORKER / CAMPAIGN MAIN WORKER`
- Harness mode: `STRICT_CAMPAIGN`
- Campaign: `CAMPAIGN-014-r1`
- State: `ASSIGNED`
- Repository: `C:\Users\GeZhu\MyMCP\mcp-council-of-translation`
- Exact local implementation baseline: `4f976c2764a463dceb403084fa3faead5300211e`
- Equivalent published product tree: `95d90cf383d045778ce61afaa50dbcec199579ce`
- Admitted local `origin/main` governance ref: `bcdb0e2bc282e907e975b43882906872913f6bec`
- Product target: `0.13.1`
- Diagnostic build target: `truthful-boundaries-council-v11.1`
- Persisted Review Schema target: `2.6` unchanged
- Verification receipt Schema target: `1.1` unchanged
- Offline Golden evaluator Schema target: `2.1`
- Acceptance authority: Foreman only
- Execution ledger: `harness/reports/CAMPAIGN-014-r1-ledger.md`
- Worker report: `harness/reports/CAMPAIGN-014-r1-worker.md`
- Commit policy: exactly eight scoped local commits, one for PKG-080 through PKG-087
- Worktree strategy: shared worktree; sequential integration of overlapping production
  packages
- Subagent delegation: allowed, not required; maximum three bounded implementation or
  read-only assignments
- Parallel delegation: allowed only for disjoint read-only investigation or disjoint
  file ownership; no concurrent edits to shared production, fixture, package or docs
  paths

## Campaign outcome

Release a narrow V0.13.1 audit remediation that fails closed on incomplete input,
eliminates confirmed deterministic scanner false positives, safely degrades malformed
discussion, keeps post-discussion state coherent, minimizes legacy V1 summaries,
truthfully names offline evaluation evidence and bounds declared FastMCP compatibility.
The Campaign adds no product capability beyond correcting these boundaries.

## Context and authority

The independent audit at
`mcp-council-of-translation-v0.13-independent-audit.md` returned `BLOCK NEXT CAMPAIGN`.
Foreman independently reproduced AUD-001 through AUD-005, accepted AUD-006 as an
evaluation-contract defect, and partially accepted AUD-007 as compatibility governance.

Authoritative design assets:

- `harness/evaluations/CAMPAIGN-013-INDEPENDENT-AUDIT-FOREMAN-RESPONSE.md`
- `harness/evaluations/NEXT-CAMPAIGN-014-AUDIT-REMEDIATION-ASSESSMENT.md`

This contract supersedes conversation summaries for implementation scope. It does not
accept work, publish V0.13.1, issue Q-016 or lift the feature-expansion block.

## Admission and protected state

Start only when all admission facts hold:

1. `HEAD` is exactly `4f976c2764a463dceb403084fa3faead5300211e`.
2. The Git index is empty, verified by the exit code of `git diff --cached --quiet`.
3. The local product tree at HEAD is byte-equivalent to published product commit
   `95d90cf383d045778ce61afaa50dbcec199579ce` for `src/**`, `tests/**`, `AGENTS.md`,
   `README.md`, `docs/v0.4-architecture.md`, `docs/v0.4-tool-contract.md`,
   `pyproject.toml`, `uv.lock` and `.github/workflows/ci.yml`.
4. The admitted local `origin/main` ref is
   `bcdb0e2bc282e907e975b43882906872913f6bec`. Do not fetch or mutate remote state.
5. Every protected hash below matches exactly.
6. The SHA-256 of this contract matches the launch prompt.
7. `python -m compileall -q src tests` passes and the complete suite passes exactly
   `480` tests using a unique repository-local basetemp.

Foreman admission evidence on 2026-08-25 Asia/Shanghai:

- repository `.venv` CPython 3.12.9;
- compile passed;
- complete regression: `480 passed in 4.60s`;
- the verified repository-local admission basetemp was removed;
- no production/source/test/package diff exists between local HEAD and the published
  product tree.

### Protected hashes

| Path | SHA-256 |
| --- | --- |
| `harness/features.json` | `25DCB7F95F27571276EB991522B05C8298990E7C31CBD6A919E4A48323130EAC` |
| `harness/plan.md` | `7D55DBA8494ADED34294B081009A66DD048F1FD70ECB911A8628F3E3F6D77AE8` |
| `harness/progress.md` | `2E3318B30CC4E53D72D8067D76B6AB5F767459AC27141CDBD1AA3E242D821017` |
| `mcp-council-of-translation-v0.13-independent-audit.md` | `0B608DF956448C92AC4112452709129FB45B27478C0F571118660DAA89FBA179` |
| `mcp-council-of-translation-audit-and-upgrade-recommendations.md` | `B48073E063C4C9F34E0B6B4DAE94E80079EAAAD3B2F8E273DD60B2F25F6ABD76` |
| `harness/evaluations/CAMPAIGN-013-INDEPENDENT-AUDIT-FOREMAN-RESPONSE.md` | `7440C47877D2C76313F1848ABCF65269A1A8FD089CE4A3FE9AA4793907903CD4` |
| `harness/evaluations/NEXT-CAMPAIGN-014-AUDIT-REMEDIATION-ASSESSMENT.md` | `A7D4F770C6F7660964CB926F44A62D3F540F0A3B43C388E1D64B886B900A1529` |
| `docs/v0.13-stage-development-report.md` | `DA03138EB0E07F27C1FFEF1F1BA044DB13D590427BC7F8EA3CB53D26168C6C94` |
| `harness/contracts/CAMPAIGN-013-r3.md` | `473A2DD662297B4061336DC49B7558CFE2054AEAB55F5622750DFAF586EAFC63` |
| `harness/evaluations/CAMPAIGN-013-r3-review.md` | `D33EEFE60F1F23B5574F9B17725C6080B17002137D5E2DFB1B3B0DCE0DABFC05` |
| `harness/evaluations/CAMPAIGN-013-r3-publication-ci-review.md` | `6DB2A06357647346B80521EEEAAB0114AE887E0918C80498509C1A21EA9958E9` |
| `harness/contracts/CAMPAIGN-013-q015-live.md` | `74C4179BA020629D9F34966B0756FFB3547D29710A01A0A820B779A38788EC99` |
| `harness/evaluations/CAMPAIGN-013-q015-live-review.md` | `9675941275A44C11188E794A0908CB7ACF1A3F9AC32377803CCD92598E1AD54B` |
| `.github/workflows/ci.yml` | `0B37598E7D53D27B04E5524BAA4D46A2AB69D5E2607A5FF9F0437512CF8EF645` |

Existing Foreman/user dirty and untracked assets are admitted. Preserve them exactly.
Do not read, traverse, copy, hash, modify, delete or stage `.learnings/**`, `reviews/**`
or `myTest/**`. Do not modify or stage any Harness path except the two new report paths
authorized by this contract. Do not use raw audit prose, raw Goose records or user data
as test fixtures; use bounded synthetic counterexamples stated in this contract.

If any admission fact differs, stop before edits with `BLOCKED` and report the exact
mismatch.

## Frozen architecture and invariants

### Stable product boundary

- Public MCP tools remain exactly five and in their current order.
- The server remains review-only and never translates files or applies edits.
- Defaults remain output `review_only`, interactive `auto`, briefing `auto`, trace
  `summary`, history `full` and Council adjudication fallback.
- Sampling budgets remain `6/13/18`; independent-review concurrency remains `1..3` with
  default and maximum `3`.
- Reviewer roles, routing portfolios, prompt authority, evidence hierarchy, Policy Gate,
  bounded user authority, reconsideration targeting and one-save persistence remain
  unchanged except the explicit corrections below.
- Review Schema stays `2.6`; verification receipt Schema stays `1.1`. Historical readers
  remain compatible with V1 and V2.0 through V2.5.
- The primary report retains exactly five sections and the canonical disposition exactly
  once and last. The 3,200-code-point cap and review-only rewrite boundary remain.
- No remediation adds a model, sampling, elicitation, retry, persistence or public tool
  call beyond the existing path.

### AUD-001 / F-064 — fail-closed incomplete input

- Keep the current 12,000-caller-character bound; do not implement chunking.
- `InputDiagnostics.*_original_length` records the original caller string length.
  `*_reviewed_length` records retained caller characters and excludes any synthetic
  truncation marker; it is never greater than 12,000.
- Source-only, candidate-only and dual truncation may still run the bounded Council, but
  the result is explicitly incomplete.
- Every truncated review must include canonical warning `input_truncated` plus
  `source_input_truncated` and/or `candidate_input_truncated` as applicable, set
  `degraded=true`, include `input_truncated` in bounded fallback provenance, classify
  decision support as `insufficient`, set status `NEEDS_HUMAN_REVIEW`, and set chief
  disposition `需人工复核 / 是`.
- The normal report must state deterministically that only a bounded prefix was reviewed
  and that the result is not complete-text publication permission. The compact response
  exposes this through display, warnings, fallback, degraded status and decision
  support; the full record retains exact diagnostics.
- Verification receipt 1.1 must remain schema-compatible and must not imply a complete
  review. A pure truncation case exposes fallback `input_truncated`, degraded true,
  insufficient support and the human-review disposition in both text and canonical JSON.
- Briefing-return, interactive, noninteractive, deterministic-blocker, model-issue,
  persistence-history and continuation paths cannot relax or erase the incomplete-input
  safety state.
- A clean prefix with an unsafe omitted suffix is a regression fixture for completeness,
  not a request to inspect or infer the omitted suffix.

### AUD-002 / F-065 — deterministic scanner precision

- Ordinary percentage prose such as `100% safe`, `50% discount`, `25% off` and
  `100% satisfied` is not a printf placeholder.
- Bare percent-plus-space-plus-letter ambiguity (`% s`, `% d`, `% o`) is treated as
  prose; protected printf tokens remain unambiguous forms such as `%s`, `%d`, `%2$s`,
  `%02d`, `%.2f` and `%%`.
- URL identity excludes sentence-final ASCII and Chinese punctuation. Tests cover `.`,
  `,`, `;`, `:`, `!`, `?`, `。`, `，`, `；`, `：`, `！`, `？` and closing punctuation
  around a URL. Balanced URL-internal syntax must not be stripped blindly.
- Existing protection for braced placeholders, variables, tags, commands, flags,
  do-not-translate literals, explicit hard constraints, numeric and Markdown signals
  remains unchanged.
- Deterministic checks stay higher-authority than model findings; the repair improves
  recognition precision and does not demote a valid blocker.

### AUD-003 / F-066 — whole-envelope discussion degradation

- Targeted Discussion remains at most one sampled JSON result. It is a single-sample
  simulated cross-role deliberation, not independent reviewers replying to one another.
- A valid discussion envelope is an object with an explicitly present list-valued
  `turns`; an explicit empty list is valid.
- Missing/null/string/scalar `turns`, any non-object entry, model-validation failure,
  unknown issue, unknown participant role, invalid stance/confidence or an invalid
  declared position change makes the whole envelope unavailable. Do not partially apply
  earlier turns.
- On invalid discussion: preserve the complete pre-discussion clusters and Position
  Matrix, add no blocker/action/evidence/position change, issue no retry or hidden call,
  and continue safely with canonical `discussion_unavailable` warning/fallback and a
  degraded discussion phase trace.
- Existing V0.13 support rules then make the outcome `insufficient` and human-review-
  required because execution degraded. This is evidence insufficiency, not a new
  deterministic translation blocker.
- Invalid JSON/model execution errors follow the same bounded path and cannot escape as
  an unhandled public-tool exception.

### AUD-004 / F-067 — post-discussion state coherence

- After every valid applied position change, recompute role consensus from final
  nonempty option IDs for material participant positions: zero options is
  `insufficient_evidence`, one is `consensus`, and more than one is `disputed`.
- Role consensus and user-choice usefulness remain separate. Do not automatically clear
  `needs_user_input` merely because roles converge; it continues to represent multiple
  bounded candidate outcomes that still must pass existing outcome validation and the
  Policy Gate.
- Digest, deliberation summary, minority report, decision-support limitations and
  Council value metrics must consume the same post-discussion consensus truth.
- A DecisionPoint may remain after role convergence only because multiple independently
  valid bounded outcomes justify user preference. Stale pre-discussion disagreement may
  not create a DecisionPoint or `material_disagreement` limitation.
- Preserve pre/post position and discussion provenance; do not rewrite Round 1 evidence.

### AUD-005 / F-068 — privacy-minimized V1 summary

- `view_review_record(detail_level="summary")` for V1 returns exactly these top-level
  fields: `schema_version`, `review_id`, `mode`, `status`, `publishability`,
  `review_needed`.
- It excludes the task, source/candidate, reviewer and conflict prose, full chief object,
  rationale and any unbounded legacy content.
- V1 `full`, V1 `verification`, V2 `full|summary|verification`, list and error behavior
  remain unchanged.
- Retrieval remains one load, zero saves, zero sampling, zero elicitation and no record
  mutation.

### AUD-006 / F-069 — truthful evaluator semantics

- Bump only the offline Golden evaluator envelope from Schema `2.0` to `2.1`; this is not
  an MCP record or receipt schema change.
- Rename fixture/observation property `critical_issue_recalled` to
  `critical_or_blocking_cluster_present`.
- Rename fixture/observation property `false_positive_free` to
  `clean_case_has_no_clusters`. For non-clean cases its expected and observed value is
  `null`/not applicable, not automatically true.
- Replace aggregate `critical_issue_recall` with
  `critical_presence_contract_accuracy`, measured as exact expected/observed presence
  agreement across the corpus.
- Replace aggregate `false_positive_free_rate` with
  `clean_case_no_cluster_accuracy`, measured only across clean cases.
- The old overclaiming aggregate keys are absent from Schema 2.1 output. Documentation
  explicitly states that these metrics do not prove defect-identity recall, span recall,
  severity calibration or general false-positive performance.
- Keep exactly 30 existing Golden scenarios. Preserve each case ID, category, task,
  reviewer envelopes, discussion/interaction inputs and expected semantic values; only
  the frozen property-name/not-applicable migration is allowed. All other inherited and
  calibration metrics remain at their accepted targets.
- Add `docs/blind-evaluation-set.schema.json` as a valid JSON Schema 2020-12 contract.
  It must require a set identifier, independent-curation provenance and cases containing
  source/candidate, expected issue family, bounded source/candidate anchors, accepted
  severity range, allowed alternative interpretations and forbidden findings.
- Do not create or score a purportedly independent blind corpus in this Campaign. The
  schema is a later external-evaluation handoff, not Worker-authored proof of accuracy.

### AUD-007 / F-070 — bounded FastMCP compatibility

- Freeze declared dependency compatibility to `fastmcp>=2.13.0.2,<4`; retain the tested
  2.x floor and exclude unsupported future major 4.
- Keep the six-job protected CI workflow byte-identical. It continues to validate the
  locked FastMCP 2.13.0.2 environment on Windows/Ubuntu and Python 3.10/3.12/3.13.
- Fresh isolated wheel evidence must separately validate exact FastMCP 2.13.0.2 and exact
  3.4.7 on CPython 3.12. Do not describe this as proof of every intermediate version.
- The canonical lock remains on FastMCP 2.13.0.2; only the root project version and root
  FastMCP specifier may change. Lock revision 3, 78 packages and 586 upload-time entries
  remain exact.

### Main Worker implementation discretion

- Private helper/module names and internal decomposition within the exact allowlist.
- Regex/parser implementation details that satisfy every positive/negative example.
- Deterministic Chinese truncation sentence within the frozen meaning and existing cap.
- Test parametrization, synthetic fixtures and repository-local temp/cache names.
- The exact JSON Schema descriptions and `$defs` organization, provided the required
  fields and independent-curation boundary are machine-enforced.

### Decisions reserved for Foreman or user

- Rejecting oversized input instead of the frozen bounded-prefix fail-closed path.
- Long-document chunking, new stored/receipt schemas, new public fields or a sixth tool.
- Partial acceptance of a malformed discussion envelope or any automatic retry.
- Redefining role consensus, user authority, DecisionPoint eligibility or Policy Gate.
- A different evaluator metric meaning, a Worker-authored blind benchmark, or a FastMCP
  range other than `>=2.13.0.2,<4`.
- Any role, route, prompt, provider, model call, budget, concurrency, default or output-
  mode change.
- Live Goose/provider validation, Q-016 issuance, acceptance, publication, push, PR,
  release, deployment or feature-expansion unblock.

## Global boundaries

### Authorized production, package and documentation paths

- `src/council_of_translation/tools/review.py`
- `src/council_of_translation/localization/preflight.py`
- `src/council_of_translation/localization/deliberation.py`
- `src/council_of_translation/localization/orchestration.py`
- `src/council_of_translation/localization/decision_support.py`
- `src/council_of_translation/localization/digest.py`
- `src/council_of_translation/localization/value_metrics.py`
- `src/council_of_translation/localization/verification.py`
- `src/council_of_translation/evaluation.py`
- `src/council_of_translation/__init__.py`
- `AGENTS.md`
- `README.md`
- `docs/v0.4-architecture.md`
- `docs/v0.4-tool-contract.md`
- `docs/blind-evaluation-set.schema.json` (new)
- `docs/v0.13.1-audit-remediation.md` (new)
- `pyproject.toml`
- `uv.lock`

### Authorized test and fixture paths

- `tests/fixtures/v24_golden_corpus.json`
- `tests/unit/test_preflight_v2.py`
- `tests/unit/test_deliberation_policy_v2.py`
- `tests/unit/test_r3_deliberation_policy.py`
- `tests/unit/test_v24_value_metrics.py`
- `tests/unit/test_decision_support.py`
- `tests/unit/test_verification_receipt.py`
- `tests/integration/test_orchestration_v2.py`
- `tests/integration/test_tool_surface_v2.py`
- `tests/integration/test_v07_dual_channel.py`
- `tests/integration/test_v12_verification_view.py`
- `tests/integration/test_v24_golden_corpus.py`
- `tests/integration/test_v24_presentation.py`
- `tests/integration/test_v26_decision_support.py`
- `tests/integration/test_v10_release_contract.py`
- `tests/integration/test_v131_input_completeness.py` (new)
- `tests/integration/test_v131_discussion_coherence.py` (new)
- `tests/integration/test_v131_history_minimization.py` (new)
- `tests/integration/test_v131_evaluation_contract.py` (new)

### Authorized Worker evidence paths

- `harness/reports/CAMPAIGN-014-r1-ledger.md` (new, untracked and unstaged)
- `harness/reports/CAMPAIGN-014-r1-worker.md` (new, untracked and unstaged)

Any other source, test, fixture, documentation, package, dependency, workflow, Harness,
user or external path is forbidden. Stop rather than edit a required unlisted path.

### Non-goals

- No chunking, overlap, cross-chunk synthesis or long-document architecture.
- No new reviewer, content type, routing profile, provider or generic adaptive Council.
- No translation generation, file editing, UI, A2A or context-MCP coupling.
- No multi-round or independently sampled peer debate.
- No numeric quality/confidence score, majority vote or model-self-reported authority.
- No expansion of the Golden corpus beyond the existing 30 scenarios.
- No actual independent blind corpus or production-quality claim.
- No CI workflow change or new required status context.

### Authorized external and destructive actions

- No live Goose/provider/model call, remote Git/GitHub mutation, push, PR, release,
  publication or deployment.
- Local dependency resolution/install is allowed only for locked sync, pinned `uv
  0.12.3`, fresh builds and the two exact isolated FastMCP smoke environments.
- Local Git staging/commits are allowed only for exact authorized paths and exact package
  commits. No reset, checkout overwrite, force operation, history rewrite or broad clean.
- Worker-created repository-local basetemps, build dirs and isolated environments may be
  removed only after resolving and verifying their absolute paths are inside the
  repository and recording creation/cleanup in the ledger. Never delete admitted assets.
- On native Windows, keep local Git operations sandboxed. No remote Git HTTPS operation
  is authorized; if a future Foreman revision authorizes one, it must use
  `require_escalated` outside the sandbox as required by the user.

## Task graph

| Package | Observable outcome | Depends on | Allowed boundary | Package verification | Parallel-safe |
| --- | --- | --- | --- | --- | --- |
| PKG-080 / F-064 | Truncated input is visibly incomplete and always fail-closed | none | review/orchestration/decision-support/digest/verification plus focused tests | source/candidate/both, briefing, blocker, persistence, continuation and receipt counterexamples | no |
| PKG-081 / F-065 | Percentage prose and URL punctuation stop causing deterministic false blockers | none | preflight plus focused unit/integration tests | complete negative corpus and preserved positive protected-token corpus | yes, only with disjoint files |
| PKG-082 / F-066 | Every malformed discussion envelope safely degrades without applying turns | none | deliberation/orchestration plus focused tests | all wrong-shape/invalid-reference/model-error cases and zero hidden retry | no |
| PKG-083 / F-067 | Final Position Matrix, consensus, digest, metrics and support agree | PKG-082 | deliberation/orchestration/digest/value metrics/decision support plus focused tests | converged/unresolved/valid-choice controls through production orchestration | no |
| PKG-084 / F-068 | V1 summary is bounded and privacy-minimized | none | review tool plus history/dual-channel tests | exact six-field V1 summary, full/verification/V2 purity and zero side effects | yes, only with disjoint files |
| PKG-085 / F-069 | Evaluator Schema 2.1 states only measured predicates and exports a blind-set schema | PKG-080 through PKG-084 | evaluation, existing fixture, Golden tests and new schema/docs | exact 30/30, renamed semantics, non-clean nulls, schema positive/negative checks | no |
| PKG-086 / F-070 | FastMCP supported range is bounded to tested majors | none | pyproject, lock-related test/docs only; final lock update occurs in PKG-087 | specifier assertion and pre-release isolated 2.13.0.2/3.4.7 import/tool probes | yes for read-only investigation only |
| PKG-087 | V0.13.1 release identifiers, docs, canonical lock and artifacts are coherent | PKG-080 through PKG-086 | release identifiers/docs/tests/uv.lock and all integrated authorized paths | full matrix, 30/30, schemas, lock, artifacts and two installed-wheel smokes | no |

## Collision and integration map

| Packages/files at risk | Required sequencing or isolation | Integration owner/check |
| --- | --- | --- |
| PKG-080/082/083 share orchestration and decision support | Execute in numeric order in the shared worktree; no parallel edits | Main Worker / combined fail-closed and discussion matrix |
| PKG-082/083 share deliberation tests and consensus state | PKG-082 must be committed before PKG-083 | Main Worker / baseline-to-final semantic diff |
| PKG-080/083/085 affect production orchestration Golden outcomes | Run the full Golden runner only after all three integrate | Main Worker / exact 30-case property audit |
| PKG-084 and PKG-080 share public history/compact behavior | Integrate PKG-080 first if both touch review tool tests | Main Worker / V1/V2/full/summary/verification matrix |
| PKG-086/087 share pyproject, docs and lock | PKG-086 freezes the specifier decision; PKG-087 alone performs final canonical lock/version migration | Main Worker / exact lock diff |
| All packages may touch release documentation | Final documentation reconciliation belongs only to PKG-087 | Main Worker / stale-term/version scan |

## Package acceptance details

### PKG-080

- Reproduce the accepted AUD-001 counterexample before edits.
- Test source-only, candidate-only and dual truncation at exact boundary and boundary+1.
- Test a clean retained prefix with a critical omitted suffix and prove no complete
  publication claim.
- Prove full, compact, metadata/history, verification and continuation truth.
- Prove no added sampling, elicitation, retry or save.

### PKG-081

- Negative cases include every percentage and URL-punctuation example frozen above,
  parenthesized URLs and Chinese punctuation.
- Positive cases include `%s`, `%d`, `%2$s`, `%02d`, `%.2f`, `%%`, `{name}`, `${APP}`,
  `/help`, `--force`, tags, DNT and required/forbidden literals.
- A scanner repair may not convert an existing deterministic blocker into model advice.

### PKG-082

- Test missing, null, string and scalar `turns`; lists containing string/integer/null;
  missing issue/speaker; unknown issue/role; invalid stance/confidence; invalid proposed
  action; parse failure and executor error.
- Any invalid entry rejects all turns in that envelope. A valid empty list is not a
  failure.
- The review completes safely as degraded/human-review-required without a new blocker.

### PKG-083

- A valid discussion that converges all material participant options yields consensus,
  increments resolved-discussion metrics once and disappears from material disagreement.
- A genuine remaining split stays disputed.
- A converged language-choice issue may retain a DecisionPoint only when two or more
  outcome candidates survive existing validation and Policy Gate.
- No role is counted twice and repeated evidence does not gain authority.

### PKG-084

- Assert exact key order and exact six-field set for V1 summary.
- Use hostile legacy prose sentinels and prove none reaches summary text or structured
  content.
- Prove V1 full remains byte-compatible and verification remains canonical/privacy-safe.

### PKG-085

- Migrate only the two overclaiming property names/semantics and evaluator envelope
  version. Do not silently retain misleading aliases in Schema 2.1 output.
- Prove all 30 case inputs and non-renamed semantic expectations remain unchanged by a
  canonical projection/hash independent of the renamed keys.
- Aggregate targets remain 1.0, and mutations of critical presence, clean-case clusters,
  support level and call budget fail the expected case/property.
- Validate the JSON Schema itself and at least one synthetic conforming and one rejected
  document without adding a runtime dependency.

### PKG-086

- Change the declared dependency specifier only as frozen. Do not refresh the lock in
  this package.
- Record why `<4` is an evidence boundary, not proof of every 2.x/3.x release.
- Keep `.github/workflows/ci.yml` byte-identical.

### PKG-087

- Package/module become `0.13.1`; build becomes
  `truthful-boundaries-council-v11.1`; Review Schema remains `2.6`; receipt Schema remains
  `1.1`; evaluator Schema becomes `2.1`.
- Pinned `uv 0.12.3` canonical lock refresh changes only editable root version
  `0.13.0 -> 0.13.1` and root FastMCP specifier to `>=2.13.0.2,<4`; resolved FastMCP
  stays 2.13.0.2 and lock invariants remain 3/78/586.
- Documentation describes truncation fail-closed behavior, deterministic scanner
  boundaries, whole-envelope discussion degradation, post-discussion consensus,
  minimized V1 summary, evaluator limitations, blind-set handoff and tested FastMCP
  points.
- Targeted Discussion is named single-sample simulated cross-role deliberation without
  implying Round 1 independence.

## Campaign acceptance criteria

1. F-064 through F-070 meet every frozen criterion and AUD-001 through AUD-005 are closed
   by production-path counterexamples.
2. No truncated review or invalid discussion can produce a permissive terminal outcome;
   the result remains useful but explicitly incomplete/insufficient.
3. Valid deterministic tokens remain protected while every frozen percentage/URL
   negative case is blocker-free.
4. Final role positions, consensus, DecisionPoints, digest, metrics and decision support
   are mutually coherent.
5. V1 summary is exactly minimized without changing any other history channel.
6. Evaluator Schema 2.1 makes no defect-identity/general-false-positive claim and the
   blind-set asset is only a schema for independent future curation.
7. FastMCP declaration is exactly `>=2.13.0.2,<4`, both tested points pass installed-
   wheel smoke, and the six-job workflow remains byte-identical.
8. Public tools/defaults, roles/routes, budgets, concurrency, schemas 2.6/1.1, Policy
   Gate, bounded user authority, privacy, persistence count and review-only boundary do
   not regress.
9. Exact 30-case Golden, complete regression, fresh artifacts and installed-wheel
   evidence pass with no skipped required check.
10. The complete diff stays in the exact allowlist and is represented by exactly eight
    scoped local commits; protected assets and index reconcile exactly.
11. Worker reports evidence and risk without claiming acceptance, publication, Q-016 or
    project completion.

## Required Campaign verification

Run and record at minimum:

1. Admission compile and complete suite with a unique repository-local basetemp; require
   exactly `480 passed` before edits.
2. Pre-change reproductions for all five production defects with exact observed failure
   behavior.
3. PKG-080 full input-completeness matrix including briefing, continuation, persistence,
   compact and canonical receipt channels.
4. PKG-081 positive/negative scanner corpus with exact preflight check kinds and blocker
   counts.
5. PKG-082 malformed-envelope matrix and no-retry/no-hidden-call telemetry.
6. PKG-083 production discussion convergence, genuine split and Policy-valid user-choice
   counterexamples.
7. PKG-084 V1 full/summary/verification privacy and retrieval-purity matrix.
8. PKG-085 exact 30/30 evaluator Schema 2.1 run, renamed metric formulas, canonical
   preservation proof, mutation controls and blind-schema validation.
9. Integrated affected orchestration, decision-support, presentation, verification,
   persistence, Golden, tool-surface and release matrix.
10. Final `python -m compileall -q src tests` and complete suite with zero failures and at
    least the 480 admitted tests; report exact total and duration.
11. Exact five-tool order; package/module/build `0.13.1`/v11.1; Review/Receipt/Evaluator
    Schemas `2.6`/`1.1`/`2.1`; defaults; budgets `6/13/18`; concurrency `3/3`; all 15
    routing profiles.
12. Programmatic proof that the repairs add no model/sampling/elicitation/retry and no
    extra persistence save; history retrieval remains pure and records immutable.
13. `git diff --check`, exact baseline-to-final path audit, dead-import scan, protected-
    hash reconciliation, workflow hash, empty index and temporary-asset cleanup.
14. Fresh wheel and sdist build with archive inspection and SHA-256/size evidence.
15. Two isolated CPython 3.12 wheel-origin smokes: exact FastMCP 2.13.0.2 and exact
    FastMCP 3.4.7. Each imports from isolated `site-packages`, calls all five tools, and
    proves one clean case plus truncation/discussion/V1-summary behavior relevant to its
    surface.

Use unique repository-local basetemps/caches for the known Windows host-temp permission
boundary. A failed command must be recorded with diagnosis and bounded rerun; do not hide
or weaken failures. Prior V0.13 artifact hashes or CI results do not substitute for fresh
V0.13.1 evidence.

## Execution, delegation and commits

Execute packages in dependency order. PKG-081 and read-only PKG-086 investigation may
run beside disjoint work, but Main Worker owns integration and must inspect every diff.

Create exactly one local commit per package with these subjects or clear equivalents:

1. `PKG-080 fail closed on incomplete review input`
2. `PKG-081 refine deterministic token scanning`
3. `PKG-082 degrade malformed discussion safely`
4. `PKG-083 align post-discussion consensus`
5. `PKG-084 minimize legacy summary retrieval`
6. `PKG-085 calibrate evaluation evidence semantics`
7. `PKG-086 bound FastMCP compatibility`
8. `PKG-087 release V0.13.1 audit remediation`

Before every commit, inspect exact staged names and staged diff. Never stage reports,
ledgers, Harness state, audit files, protected assets, user assets or temporary output.
The Git index must be empty at handoff.

Subagents have no acceptance authority. Main Worker records every assignment, files,
result, integration and verification in the ledger. If subagents are not used, record
zero and execute directly.

## Required evidence and handoff

Maintain:

- `harness/reports/CAMPAIGN-014-r1-ledger.md`
- `harness/reports/CAMPAIGN-014-r1-worker.md`

Both remain untracked and unstaged. The ledger maps each package to executor/subagent,
files, commit, commands, results, deviations and integration status.

The Worker report must include:

- terminal status and contract SHA-256;
- baseline/final HEAD and exact eight commits;
- baseline-to-final changed-file list/stat and complete diff inspection;
- package-by-package counterexamples and verification;
- exact final compile/full-suite/Golden/metric results;
- schema/tool/default/budget/concurrency/routing invariants;
- lock diff and 3/78/586 counts;
- fresh artifact names, sizes and SHA-256 values;
- both isolated FastMCP versions and proof of wheel-origin imports/tool calls;
- protected-hash/workflow reconciliation, index state and cleanup;
- every subagent, authority escalation, dependency operation, build, live call, remote
  mutation and skipped required check, including explicit zero counts;
- remaining risks or blockers without claiming acceptance.

In chat, start with exactly `READY_FOR_REVIEW` or `BLOCKED`, then summarize report and
ledger paths, contract hash, baseline/final state, commits/files, package/Campaign
verification, artifacts, skipped checks, protected hashes, subagent/authority/dependency/
live-call counts and remaining risk. Stop after handoff.

## Stop conditions

Return `BLOCKED` before guessing if:

- baseline, index, local governance ref, contract hash, workflow hash or any protected
  asset differs;
- a required fix needs a path outside the exact allowlist;
- truncation cannot remain fail-closed without chunking, rejection or a schema change;
- discussion safety would require partial malformed-envelope acceptance, retry or loss
  of valid Round 1 evidence;
- consensus and DecisionPoint semantics cannot be separated as frozen;
- V1 summary minimization changes full/verification/V2 behavior;
- evaluator migration cannot preserve the exact 30 scenario inputs and non-renamed
  expected semantics;
- FastMCP 2.13.0.2 or 3.4.7 installed-wheel evidence fails, or canonical lock generation
  drifts beyond the exact root version/specifier and 3/78/586 invariants;
- any public tool, role, route, prompt, budget, concurrency, schema 2.6/1.1, Policy Gate,
  user authority, privacy, persistence or review-only invariant regresses;
- a required test/build/archive/smoke cannot establish the result;
- work requires live Goose/provider/model calls, remote Git/GitHub mutation, push, PR,
  publication, release, deployment, credentials, destructive cleanup or broader user
  authority.

Only Foreman may revise this contract, accept the Campaign, authorize protected-main
publication, issue Q-016 or lift the next-feature block.
