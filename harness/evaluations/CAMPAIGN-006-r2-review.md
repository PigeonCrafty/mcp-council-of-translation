# Campaign Foreman Review: CAMPAIGN-006-r2

## Control

- Role: FOREMAN
- Mode: STRICT_CAMPAIGN
- Decision: `CHANGES_REQUESTED`
- Contract: `harness/contracts/CAMPAIGN-006-r2.md`
- Worker report: `harness/reports/CAMPAIGN-006-r2-worker.md`
- Execution ledger: `harness/reports/CAMPAIGN-006-r2-ledger.md`
- Reviewed baseline: `403310ccdfcbb026bd2b375517d14dc927286604`
- Reviewed final state: `8ed8d866076acab9dc22a57c6fd31d4ff6792fe4`
- Contract SHA-256: `70756EC6B7DA60086EA15E165EF4D21B81E359E32B3FA5FC886E47752ADF8CD2`

## Scope and repository review

- Complete baseline-to-final diff inspected: yes; 23 authorized paths, 629 insertions and 53 deletions.
- Commit/package mapping: `7f5a03c` PKG-032; `06aa90c` PKG-033/034; `8912cb9` PKG-035; `8ed8d86` PKG-036.
- Global boundary compliance: pass. No schema shape, public argument, sixth tool, dependency, budget, Policy Gate, history rewrite, live provider or Goose change.
- User and Foreman assets: all eleven protected hashes match; index is empty; only declared protected dirt and the required r2 report/ledger remain.
- Delegation: forbidden and correctly unused. Four local commits satisfy the three-to-five policy; no push, PR, release or deployment occurred.
- Worker retry and authority disclosures are consistent with the ledger and repository state; no sensitive values were persisted.

## Task graph review

| Package | Foreman verification | Result |
| --- | --- | --- |
| PKG-032 | Material brand/UI and official-glossary variants are selected, active affected roles are filtered and generic/duplicate/limit cases remain bounded. A missing direct-answer path is described below. | `CORRECTION_REQUIRED` |
| PKG-033 | Decline, cancel, unsupported, malformed, error and explicit assumption open no outcome form and produce conservative status; an actual answer precedes affected-role reconsideration and outcome. | `PASS / PRESERVED` |
| PKG-034 | Lightweight marketing remains three roles; standard/strict use the exact frozen six in order; independent deep-path evidence reaches 13/13 calls. | `PASS / PRESERVED` |
| PKG-035 | Suppressed questions no longer appear as completed interaction, unresolved material context is visible, standalone `ux` and doubled punctuation are normalized, and the verdict remains last. | `PASS / PRESERVED` |
| PKG-036 | Source diagnostics report 0.8.0/build v6/schema 2.2, exact five tools and budgets 6/13/18; documentation and artifact evidence are otherwise coherent. | `PASS / PRESERVED` |

## Campaign acceptance review

| Criterion | Foreman verification | Result |
| --- | --- | --- |
| 1–3 | Exact six-role routing and the two missing-context live shapes pass. | PASS |
| 4 | Audience/context examples are bounded, but already supplied glossary/reference and unambiguous brand/UI usage are not recognized as answers. | FAIL |
| 5–7 | Resolved/unresolved phase ordering, conservative status and valid answered continuation pass. | PASS |
| 8–9 | Primary rendering and literal V2.2 record invariants pass. | PASS |
| 10–12 | Version/tool/default/budget, 217-test, compile, scope, package and installed-wheel evidence pass. | PASS, preserved subject to correction integration |

## Independent integration verification

| Command/workflow | Result |
| --- | --- |
| Complete `git diff --stat/name-status/check 403310c..8ed8d86` and per-file production/test inspection | 23/23 authorized paths; diff check clean |
| Focused V0.8 context/routing/presentation/role suites | `24 passed` using system Python |
| `.venv\Scripts\python.exe -m compileall -q src tests` | passed |
| `.venv\Scripts\python.exe -m pytest -q -p no:cacheprovider --basetemp .tmp/foreman-c006-r2-full-venv` | `217 passed in 2.38s` |
| Source tool/version/role probe | exact five tools; 0.8.0/build v6/schema 2.2; marketing routes 3/6/6; budgets 6/13/18 |
| Caller-context counterexample probe | supplied `term_glossary` and explicit resolved brand usage both still selected as unanswered gaps |

The first full-suite attempt used system Python 3.13, which lacks `fastmcp`, and stopped during collection. The repository `.venv` contains FastMCP 2.13.0.2; the exact full rerun there passed. One diagnostic probe also tried to call the decorated `FunctionTool` as a plain function; the corrected probe used the project's `_server_info()` helper and `mcp.get_tools()`. These are Foreman environment/probe corrections, not product failures. `.learnings/**` was not modified because it is a protected user asset.

## Finding

| Severity | Package/criterion | Finding and evidence | Required correction |
| --- | --- | --- | --- |
| Major | PKG-032 / criterion 4 | `select_context_gaps()` receives only `ReviewBriefV2`; `_gap_is_answered()` checks audience, usage context, tone, domain and content type, but the brief does not contain `term_glossary` or `reference_translations`. Consequently a caller-provided binding glossary still triggers the question “是否存在官方批准且具有约束力的标语词表或参考译法？”. The unconditional compound-alternative return also re-asks “品牌标语还是功能按钮？” even when caller context unambiguously establishes brand-slogan usage. This contradicts the frozen requirement that plainly answered questions remain `already_answered`, and would add exactly the redundant interaction V0.8 is meant to remove. | Pass bounded caller context into selection or derive an equivalent internal answer packet. Recognize explicit supplied glossary/reference and unambiguous brand-versus-functional usage; do not treat `content_type=marketing` alone or conflicting marketing/UI context as an answer. Add direct counterexamples and rerun affected plus full suites. |

## Preserved evidence

- PKG-033 through PKG-036 implementation and focused evidence remain valid.
- PKG-032 material-impact grammar, dedupe, generic/immaterial/limit bounds and active-role filtering remain valid except for direct-answer recognition.
- Complete 23-path scope, four commits, all protected hashes, compile, 217-test regression, exact tool/version/schema/default/budget probes, deep 13-call path, fresh artifacts and current-FastMCP wheel evidence are preserved.
- The correction must not reopen role routing, status precedence, presentation, versioning, schema, tools, budgets, dependencies or packaging behavior.

## Decision rationale

Campaign 006 r2 fixes the original live failures and is technically strong, but one frozen acceptance condition is not met: context already provided by the caller can still produce a redundant material follow-up. Because the correction is deterministic, local to context answer recognition and independently testable without redesign, the proper decision is `CHANGES_REQUESTED`, not `BLOCKED`.

## Next action

Issue `CAMPAIGN-006-r3` from exact Worker HEAD `8ed8d866076acab9dc22a57c6fd31d4ff6792fe4`. Limit it to caller-context-aware `already_answered` recognition and focused/full regressions. Preserve all other r2 package evidence and prohibit live/provider/public/schema/version changes.
