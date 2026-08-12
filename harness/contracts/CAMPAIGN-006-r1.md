# Campaign Contract: CAMPAIGN-006-r1

## Control

- Role: MAIN WORKER
- Mode: STRICT_CAMPAIGN
- State: ASSIGNED
- Repository: `C:\Users\GeZhu\MyMCP\mcp-council-of-translation`
- Baseline commit: `755aea681b64283a4cb369817d17b3e52c0973a0`
- Baseline subject: `Record V0.7.1 publication state`
- Product target: `0.8.0`
- Diagnostic build target: `context-coherent-council-v6`
- Required report: `harness/reports/CAMPAIGN-006-r1-worker.md`
- Required ledger: `harness/reports/CAMPAIGN-006-r1-ledger.md`
- Commit policy: three to five scoped local commits; no push, PR, release, deployment or branch-protection change
- Worktree: shared; Main Worker owns every authorized production path
- Subagents: forbidden because guided selection, orchestration, role routing and digest behavior are tightly coupled
- Acceptance authority: Foreman only

Read `AGENTS.md`, `harness/plan.md`, `harness/features.json`, `harness/progress.md`, this contract, `harness/evaluations/CAMPAIGN-005-q009-live-review.md` and `harness/evaluations/CAMPAIGN-005-r1-review.md` completely before editing.

## Admission gate

Before any edit:

1. verify exact HEAD and subject above;
2. verify the Git index is empty and only the declared Foreman/user dirt is present;
3. verify this contract plus every protected hash below;
4. run `python -m compileall -q src tests`;
5. run the full suite with repository-local basetemp and cache disabled; expected admission is exactly `203 passed`;
6. reproduce with deterministic fixtures:
   - standard marketing activates only three roles;
   - a brand-slogan-versus-functional-UI question and binding slogan-glossary question can be suppressed as `immaterial_gap`;
   - unresolved material context can be followed by an outcome form and an unqualified publishable disposition;
   - primary text can expose raw `ux`, `。；依据`, and suppressed questions as completed interaction content.

Stop `BLOCKED` on unexplained drift. Do not repair, stage, rewrite, delete, move or commit protected assets.

| Protected asset | SHA-256 |
| --- | --- |
| `harness/plan.md` | `FF508A3B0E87647B372C63D3C30448ABC4989E6D86C1466FE500334E4064212A` |
| `harness/features.json` | `9D147458DFA2E114E639E81A52CD84F2C48DD5AF2F9808DF4C9C04E07129DD0B` |
| `harness/progress.md` | `D37EDA7159962453AE19E2D796F09F62DD6099C8B768504683E3A1C80FB98DAB` |
| `harness/evaluations/CAMPAIGN-005-q009-live-review.md` | `99725BA7913EA7B8A75A1D1E9A2B52C152238BF1F582C644BE27DE970E06E54A` |
| `harness/evaluations/CAMPAIGN-005-r1-review.md` | `6DC51DA5B7955289D407BB53194F7EA100736BD324B087EBDAF89C64F86AD41C` |
| `harness/contracts/CAMPAIGN-005-r1.md` | `F47CC137CD6DF31C28E39519CCCF78DB3609C5D0EB3E71686AA1F62E27035E02` |
| `harness/reports/CAMPAIGN-005-r1-worker.md` | `41A7C37C3C71C9F2A066723635CB9836A77E544546FCCEB8E1E8296C35D40A93` |
| `.learnings/LEARNINGS.md` | `22F939E6F980DF52487AAFE97EDCA9B90CF3931DDB7A31BF8A5BBB8F052E658F` |
| `.learnings/ERRORS.md` | `F99EB75886781958BF5AE6DCF844FD476CBCA45937896A25EE3B2E9D6CD34F0A` |
| audit Markdown | `B48073E063C4C9F34E0B6B4DAE94E80079EAAAD3B2F8E273DD60B2F25F6ABD76` |

Preserve `.learnings/**`, `reviews/**`, the audit Markdown, every prior Harness artifact and `myTest/**` if it appears. Do not open or copy raw user records from the platform data directory. Only the required Campaign 006 ledger/report may be created under Harness.

## Campaign outcome

Deliver Council of Translation V0.8 as a context-first, relevant panoramic review. In default standard marketing work, the user sees six genuinely relevant lenses. Questions that determine whether text is a brand slogan, functional UI copy or governed by an official glossary are resolved before wording outcomes. If material context remains unresolved, the Council reports uncertainty and requires human review instead of manufacturing a clean publishable decision.

## Frozen design

### Relevant marketing Council

- Standard marketing active roles, in order, are exactly:
  1. `fidelity_reviewer`
  2. `terminology_reviewer`
  3. `product_context_reviewer`
  4. `brand_voice_reviewer`
  5. `risk_ambiguity_reviewer`
  6. `fluency_reviewer`
- Strict marketing contains the same six roles in the same relative order. It may not silently lose a standard lens.
- Lightweight marketing remains the existing deliberately narrow fast path unless a current invariant requires a bounded correction.
- Do not add technical or UX roles to marketing merely to reach six. The six roles above are the frozen relevant set.
- Standard budget remains 13. The deep path must fit six independent reviews, at most three context reconsiderations, one discussion and at most three outcome reconsiderations.

### Material context classification

- Keep `ContextGapV2` and record schema 2.2 unchanged.
- Context gaps remain reviewer suggestions, not hard constraints or blockers.
- Selection may inspect both bounded `question` and `materiality` through a deterministic impact grammar. It must recognize at least:
  - brand slogan versus functional/UI usage;
  - official, approved or binding slogan/term glossary/reference;
  - usage, audience or product context that changes meaning, role routing, option validity, release decision or recommended outcome.
- A non-empty model assertion alone is insufficient. Generic curiosity and unrelated product trivia remain suppressible.
- Direct questions whose answer is plainly present may remain `already_answered`; compound alternatives such as “品牌标语还是功能按钮” are not answered merely because some context string exists.
- Stable semantic dedupe, two-question cap, source/affected-role provenance and bounded strings remain.
- Prompt wording may use a small canonical impact vocabulary while legacy/free prose remains conservatively readable.
- Filter affected roles to registered active roles before reconsideration; invalid or unrelated IDs cannot crash the run or consume calls.

### Context precedence and status truth

- Selected material context is elicited before context reconsideration, discussion, DecisionPoint creation and outcome elicitation.
- A real non-assumption answer updates effective context, records provenance and reconsiders only affected active roles within the existing three-call phase cap.
- The explicit assumption value, decline, cancel, unsupported, malformed or error leaves the selected material context unresolved.
- When any selected material context remains unresolved:
  - do not open an outcome form in that run;
  - do not create a valid user outcome decision;
  - lower `effective_brief.context_confidence` from `full` when necessary;
  - preserve the unanswered question as a blind spot/required confirmation;
  - set bounded warning/fallback provenance such as `material_context_unresolved`;
  - return `NEEDS_HUMAN_REVIEW`, `publishability="需人工复核"`, and `review_needed="是"`.
- An actual answer may continue to discussion/outcome selection. A valid user choice remains decisive only among Policy-Gate-valid options.
- Immaterial, duplicate and already-answered suppressions alone do not degrade or require review.

### Presentation and audit integrity

- Suppressed immaterial/duplicate/already-answered questions do not appear under `你的决定与复议` as if the user handled them.
- Unresolved selected material context appears in the blind-spot or required-confirmation presentation before the final disposition.
- Map bounded issue labels including standalone `ux` to natural Chinese such as `用户体验` without erasing ordinary embedded tokens.
- Normalize punctuation so renderer composition cannot emit `。；依据`, `；；`, or equivalent doubled separators.
- Preserve the accepted concise primary report, conditional material evidence, internal-ID sanitizer, <=3,200 hard cap and verdict-last rule.
- Literal V2.2 record fields remain the only audit truth. Add deterministic invariant tests for current role IDs, `structured_success|unavailable`, coverage literals and executed call counts. Do not add an audit snapshot, duplicate telemetry, sixth tool or primary diagnostic section.
- The Goose follow-up's impossible zero-call/old-ID prose is external evidence quality, not a production fixture to reproduce as a server payload.

### Version and compatibility

- Package/module version: `0.8.0`.
- Diagnostic build: `context-coherent-council-v6`.
- Record schema remains `2.2`; no historical record rewrite.
- Exactly five public tools, review-only default, interactive/briefing auto, trace summary, history full, Council adjudication fallback and budgets 6/13/18 remain.
- V1, V2.0, V2.1 and V2.2 reads remain compatible; full/metadata/off privacy behavior remains.
- Presentation and context classification add no model calls. Only the already bounded reviewer/context/discussion/outcome phases may sample.

## Main Worker discretion

- Exact helper names and internal impact vocabulary.
- Whether context-resolution state is derived locally or represented by one non-persisted internal helper.
- Test fixture organization and exact natural Chinese microcopy with equivalent meaning.
- Three to five commits, provided package dependency order is preserved behaviorally.

## Reserved decisions

- New tools, public arguments, schema fields/version, dependencies, widgets or Goose changes.
- New sampling phase, model-based briefing classifier, budget increase or unlimited roles/questions.
- Changing user authority, Policy Gate hierarchy, review-only boundary, persistence privacy or historical records.
- Broad role redesign outside marketing standard/strict applicability.
- Treating reviewer context prose as a deterministic hard rule.

## Allowed paths

Production:

- `src/council_of_translation/localization/guided.py`
- `src/council_of_translation/localization/prompt_builders.py`
- `src/council_of_translation/localization/roles.py`
- `src/council_of_translation/localization/orchestration.py`
- `src/council_of_translation/localization/digest.py`
- `src/council_of_translation/localization/models.py` only for 0.8.0/build defaults; no model-field/schema shape change
- `src/council_of_translation/localization/persistence.py` only for current version identifiers
- `src/council_of_translation/tools/review.py` only for version/build descriptions and unchanged tool diagnostics
- `src/council_of_translation/__init__.py`
- `src/council_of_translation/server.py` only for V0.8 wording

Tests:

- `tests/unit/test_roles_v2.py`
- `tests/unit/test_v07_report.py`
- `tests/unit/test_persistence_v2.py`
- `tests/unit/test_v22_forms.py`
- `tests/unit/test_v22_models_persistence.py`
- `tests/integration/test_tool_surface_v2.py`
- `tests/integration/test_v071_live_presentation.py`
- `tests/integration/test_v07_integrity.py`
- `tests/integration/test_v22_briefing.py`
- `tests/integration/test_v22_context_gaps.py`
- `tests/integration/test_v22_digest.py`
- `tests/integration/test_v21_reconsideration.py`
- one or more focused new files matching `tests/integration/test_v08_*.py`

Package/docs:

- `pyproject.toml`, `uv.lock` only for package version; no dependency change
- `README.md`, `AGENTS.md`, `docs/v0.4-architecture.md`, `docs/v0.4-tool-contract.md`
- required `harness/reports/CAMPAIGN-006-r1-ledger.md`
- required `harness/reports/CAMPAIGN-006-r1-worker.md`

## Forbidden paths and systems

- All other production/tests/config/docs and every Foreman/user asset.
- GitHub settings/workflows, Goose installation/configuration, credentials and external providers.
- Live user record storage, live Goose/model/provider calls, push, PR, tag, release or deployment.

## Authorized actions

- Repository-local read/test/build/install operations.
- One fresh 0.8.0 sdist/wheel build and one repository-local current-FastMCP isolated wheel smoke.
- Exact-path local staging and three to five scoped local commits.
- Retry a failed repository-local build/test once after diagnosis; record every failure and correction in the ledger/report.

## Task graph

| Package | Observable outcome | Depends on | Main boundary | Verification |
| --- | --- | --- | --- | --- |
| PKG-032 | Live-shaped brand/UI and official-glossary questions classify as material without promoting model prose to a hard rule | none | guided, reviewer prompt, focused tests | counterexamples selected; generic/answered/duplicate/invalid remain bounded |
| PKG-033 | Unresolved material context blocks outcome interaction and produces conservative status; actual answers continue in phase order | PKG-032 | orchestration, guided, integration tests | all interaction actions, phase order, confidence, warnings/status and budget probes |
| PKG-034 | Standard/strict marketing use the exact six relevant lenses | PKG-033 | roles and routing/integration tests | exact role IDs/order, 6 base calls, deep 13-call budget path |
| PKG-035 | Context-first report is natural and raw record facts remain internally consistent | PKG-032–034 | digest plus focused presentation/invariant tests | no suppressed pseudo-decision, raw `ux`, doubled punctuation or verdict displacement |
| PKG-036 | V0.8 identifiers/docs/packages are truthful | PKG-035 | version loci, docs, build/smoke | full suite, exact five tools/schema/defaults/budgets, fresh artifacts and pinned recipes |

Packages are sequential and not parallel-safe.

## Acceptance criteria

1. Exact standard marketing role list is the frozen six and yields six role lenses with full successful coverage.
2. Strict marketing is a superset containing the same six in relative order; lightweight behavior and budgets remain bounded.
3. The two sanitized live questions are selected as material across realistic materiality prose variants and appear before any outcome form.
4. Direct answered, duplicate, generic, unrelated/immaterial, invalid and over-limit gaps remain safely bounded with truthful provenance.
5. Actual context answers update the brief and reconsider only affected active roles before discussion/outcome; total calls never exceed mode budget.
6. Assumption, decline, cancel, unsupported, malformed and error cases produce no outcome elicitation, no accepted outcome, lowered confidence, visible required confirmation and conservative human-review status.
7. A fully answered context case can proceed to valid user selection and clean completion when all other gates pass.
8. Primary text contains no suppressed pseudo-decision, standalone raw `ux`, `。；依据`, internal IDs or procedural counters; material evidence/conditions remain and verdict is last within 3,200 code points.
9. Raw V2.2 record invariants use current role IDs, valid sample/coverage literals and call counts consistent with executed phases; structured chief/role evidence and privacy remain.
10. Package/module 0.8.0, build `context-coherent-council-v6`, schema 2.2, exact five tools, defaults and budgets 6/13/18 pass in source and installed wheel.
11. All 203 accepted tests plus focused regressions pass without deletion or weakening; compile, diff, scope, protected hashes and index/worktree hygiene pass.
12. Fresh sdist/wheel and isolated current-FastMCP tool calls pass; docs provide pinned clean-marketing and mixed-context post-publication recipes.

## Required verification

- Deterministic before/after reproduction for the four live counterexamples.
- Role routing unit matrix for lightweight/standard/strict marketing plus existing UI/docs routes.
- Context-gap selection matrix including prose variants, compound alternative, direct answered question, generic curiosity, duplicate, invalid ID, question cap and immaterial trivia.
- Core phase-order workflows for actual answer and every unresolved action; assert gateway request ordering and zero outcome requests when unresolved.
- Deep standard marketing budget workflow reaching 13 without overflow.
- Clean/disputed/degraded/pending/adversarial primary render probes plus raw record invariant checks.
- Focused allowed suites, `python -m compileall -q src tests`, then full pytest with repository-local basetemp/cache disabled.
- Exact five-tool FastMCP call and server-info check.
- `git diff --check 755aea681b64283a4cb369817d17b3e52c0973a0..HEAD` and exact allowed-path audit.
- Fresh repository-local 0.8.0 build; install wheel in one fresh repository-local environment with current dependency resolution and call registered tools.
- Recheck every protected hash and empty index.

Reuse accepted FastMCP 2.13 dual-channel evidence because no adapter/result-shape change is authorized. Do not claim live provider behavior.

## Stop conditions

Stop `BLOCKED` if baseline/protected/admission evidence differs; the frozen six-role marketing route cannot fit the 13-call deep path; context precedence requires a new schema/public argument/model phase; valid user authority or Policy Gate would need weakening; unresolved material context cannot be represented truthfully with existing V2.2 fields; or any live/external/destructive authority is required.

## Handoff

Maintain `harness/reports/CAMPAIGN-006-r1-ledger.md` throughout execution and write `harness/reports/CAMPAIGN-006-r1-worker.md`. Start the conversational handoff with exactly `READY_FOR_REVIEW` or `BLOCKED`, then report contract hash, baseline/final HEAD, package/commit/file mapping, before/after counterexamples, focused/full/build/wheel results, protected hashes, index/worktree state, subagent/authority/live-call counts, retries/deviations and remaining risks. Do not push or claim Campaign acceptance/project completion.
