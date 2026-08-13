# Campaign Contract: CAMPAIGN-006-r3

## Control

- Role: MAIN WORKER
- Mode: STRICT_CAMPAIGN
- State: ASSIGNED
- Repository: `C:\Users\GeZhu\MyMCP\mcp-council-of-translation`
- Baseline commit: `8ed8d866076acab9dc22a57c6fd31d4ff6792fe4`
- Baseline subject: `Release context-coherent Council 0.8.0`
- Product/build/schema: preserve `0.8.0` / `context-coherent-council-v6` / `2.2`
- Supersedes for execution: `CAMPAIGN-006-r2`
- Required report: `harness/reports/CAMPAIGN-006-r3-worker.md`
- Ledger: no new ledger required; preserve the r2 ledger
- Commit policy: exactly one scoped local commit; no push, PR, release or deployment
- Subagents: forbidden for this bounded correction
- Acceptance authority: Foreman only

Read `AGENTS.md`, this contract, `harness/contracts/CAMPAIGN-006-r2.md`,
`harness/evaluations/CAMPAIGN-006-r2-review.md`, the r2 Worker report/ledger,
`harness/plan.md`, `harness/features.json` and `harness/progress.md` completely before
editing.

## Preserved r2 evidence

Do not reimplement or redesign Campaign 006. PKG-033 through PKG-036 pass and are
preserved. PKG-032's material-impact grammar, two-question bound, semantic dedupe,
generic/immaterial suppression and active-role filtering also pass. The exact role
routing, phase precedence, conservative unresolved status, primary presentation,
V2.2 record invariants, version/tool/default/budget behavior, 217-test result, artifacts
and wheel smoke remain valid unless this correction invalidates them.

## Admission gate

Before editing:

1. verify exact HEAD and subject from Control;
2. verify an empty Git index and only declared Foreman/user/report dirt;
3. verify this contract and every protected hash below;
4. run `.venv\Scripts\python.exe -m compileall -q src tests`;
5. run the full suite with repository-local basetemp and cache disabled; expect exactly
   `217 passed`;
6. reproduce both failures without modifying production:
   - a binding official glossary/reference question is selected even when the caller
     already supplied `term_glossary` or `reference_translations`;
   - brand-slogan-versus-functional-UI is selected even when caller context and content
     type unambiguously establish one side.

Stop `BLOCKED` on unexplained drift. Do not edit, stage or commit protected assets.

| Protected asset | SHA-256 |
| --- | --- |
| `harness/plan.md` | `D87B68EC6C1AC483C08B71E926CCEFF4CCD763EC02A6DF192F20CAE072F1B14E` |
| `harness/features.json` | `86FD1BF14DB6A56C0B12FF77A1960C59CAB81F7781ACFFBBAFDDCDE57735B775` |
| `harness/progress.md` | `910686CFF3701A8C03ACC04AFDCC016805A3B1E8A7D8FE0C8D3E4139C4902D9A` |
| `harness/evaluations/CAMPAIGN-006-r2-review.md` | `623B092CE9AB4D89FD100DA0AC6EA269B078E575190D353DFADFC3E7A29D77DF` |
| `harness/contracts/CAMPAIGN-006-r2.md` | `70756EC6B7DA60086EA15E165EF4D21B81E359E32B3FA5FC886E47752ADF8CD2` |
| `harness/reports/CAMPAIGN-006-r2-worker.md` | `D15D85BD49241341FF0FE8859BE1ECA28782D17EB638B37B0F289361C84F73C3` |
| `harness/reports/CAMPAIGN-006-r2-ledger.md` | `512A85627AE1A7D70724839C6FE2926FEE0707570E761693D48152FC56EB780D` |
| `harness/contracts/CAMPAIGN-006-r1.md` | `29580DBB99603BE6CFA04D62707074290076717850602E1825881AA4B889AA3F` |
| `harness/evaluations/CAMPAIGN-005-q009-live-review.md` | `99725BA7913EA7B8A75A1D1E9A2B52C152238BF1F582C644BE27DE970E06E54A` |
| `.learnings/LEARNINGS.md` | `22F939E6F980DF52487AAFE97EDCA9B90CF3931DDB7A31BF8A5BBB8F052E658F` |
| `.learnings/ERRORS.md` | `F99EB75886781958BF5AE6DCF844FD476CBCA45937896A25EE3B2E9D6CD34F0A` |
| audit Markdown | `B48073E063C4C9F34E0B6B4DAE94E80079EAAAD3B2F8E273DD60B2F25F6ABD76` |

Preserve `.learnings/**`, `reviews/**`, the audit Markdown, all prior Harness artifacts,
r2 evidence and `myTest/**` if it appears. Only the r3 Worker report may be created under
Harness.

## Correction outcome

Make direct-answer classification aware of bounded caller context without changing
`ReviewBriefV2`, persisted schema or public arguments.

1. A question about an official, approved, binding or otherwise designated slogan/term
   glossary or reference is `already_answered` when the caller already supplied the
   relevant non-empty `term_glossary` or `reference_translations` packet.
2. A compound brand-slogan-versus-functional-UI question is `already_answered` only when
   caller-provided usage context plus normalized content type unambiguously establish one
   side.
3. `content_type=marketing` by itself is not an answer. A marketing/UI conflict such as
   marketing content plus “多步骤设置向导底部主操作按钮” remains unanswered/material
   and must still enter the existing conservative context-first flow.
4. An explicit clean marketing context such as “官网首页品牌宣传标语” and an explicit
   clean UI context under UI content type are answers. Missing, vague or mixed context
   is not.
5. Caller packets remain context, not deterministic hard rules or blockers. Do not parse
   their values for semantic correctness; presence is sufficient only for a question
   asking whether that packet/reference exists.

## Allowed paths

- `src/council_of_translation/localization/guided.py`
- `src/council_of_translation/localization/orchestration.py`
- `tests/integration/test_v08_context_classification.py`
- `tests/integration/test_v22_context_gaps.py`
- required `harness/reports/CAMPAIGN-006-r3-worker.md`

All other production, tests, package, documentation, Harness and user paths are
forbidden. No version, build, schema, role, prompt, budget, tool, dependency,
presentation, persistence or Policy Gate change is authorized.

## Acceptance criteria

1. Supplied `term_glossary` suppresses the corresponding official/binding glossary
   existence question with `reason="already_answered"`.
2. Supplied `reference_translations` suppresses a corresponding approved/reference
   existence question with the same provenance.
3. Explicit brand-slogan marketing usage and explicit functional-UI usage suppress the
   compound usage question.
4. Marketing-only, no-context, vague context and conflicting marketing-plus-UI-button
   cases continue selecting that material question.
5. No generic non-empty rule/context packet suppresses an unrelated question; duplicate,
   generic, immaterial, limit and active-role behavior remain unchanged.
6. Existing unresolved-action workflows still make zero outcome requests and require
   human review; a genuinely missing brand/UI or glossary gap remains before outcomes.
7. Exact six-role marketing routing, 13-call deep path, presentation invariants, literal
   record telemetry, version/build/schema, exact five tools and budgets 6/13/18 remain.
8. No accepted test is deleted or weakened; focused checks, compile, full suite,
   `git diff --check`, exact two-production/two-test maximum scope and protected hashes
   pass.

## Required verification

- Add a deterministic truth table for both caller packet types and brand/UI contexts,
  including all positive and negative cases above.
- Run the complete V0.8 classification and context-precedence suites plus the existing
  V2.2 context-gap suite.
- Re-run the exact six-role/deep-budget and presentation/runtime focused suites to prove
  preservation.
- Run compile and the entire suite using `.venv\Scripts\python.exe`, repository-local
  basetemp and disabled pytest cache.
- Run source exact-five-tool/version/schema/default/budget inspection.
- Run `git diff --check 8ed8d866076acab9dc22a57c6fd31d4ff6792fe4..HEAD`, exact allowed-path audit,
  protected-hash audit and empty-index check.

No fresh artifact build or wheel installation is required because r2 packaging evidence
is preserved and version/package/runtime adapter files are forbidden. Do not run live
Goose/provider/model calls.

## Stop conditions and handoff

Stop `BLOCKED` if the correction requires a schema/public-field change, parsing arbitrary
caller prose into hard rules, weakening the unresolved-context gate, touching an
unauthorized path or using external/live authority.

Write `harness/reports/CAMPAIGN-006-r3-worker.md`. Start the conversational handoff with
exactly `READY_FOR_REVIEW` or `BLOCKED`, then report contract hash, baseline/final HEAD,
the one commit and exact files, before/after truth table, focused/full results, preserved
invariants, hashes/index/worktree, authority/subagent/live-call counts and remaining
risks. Do not push or claim Campaign acceptance or project completion.
