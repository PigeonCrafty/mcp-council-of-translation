# CAMPAIGN-008-r2 Main Worker Report

## Terminal status

READY_FOR_REVIEW

This is a Worker handoff only. Campaign acceptance and Q-012 acceptance remain with the
Foreman.

## Control and admission

- Role/mode: `WORKER / MAIN WORKER`, `STRICT_CAMPAIGN`.
- Contract: `harness/contracts/CAMPAIGN-008-r2.md`.
- Contract SHA-256: `9F01492711FDCA0CCF27D74851E8A3FDB26DA6454524CC4DAA799FA48E1201BB`.
- Exact admitted baseline: `6e28c103f98a6b0481ab7d103580b83f8e6c4cfa`, subject
  `Release V0.10 evidence value contract`.
- Admission index: empty. Declared Foreman/user dirty and untracked assets were recorded
  and protected.
- Admission compile: passed.
- Admission complete regression: `263 passed in 3.41s`.
- Subagents were forbidden and none were used.

## Scoped commits and paths

Exactly two local commits were created, one per package:

1. `c4c8fc616afedf9977c314e93e721d346367dd27` —
   `Fix deterministic Council value accounting`
2. `6464f96f681aa3531c14cd631689673561193027` —
   `Execute V2.4 offline golden corpus`

Baseline-to-final implementation/test paths are exactly:

- `src/council_of_translation/localization/value_metrics.py`
- `src/council_of_translation/localization/digest.py`
- `src/council_of_translation/evaluation.py`
- `tests/fixtures/v24_golden_corpus.json`
- `tests/unit/test_v24_value_metrics.py`
- `tests/integration/test_v24_value_metrics.py`
- `tests/integration/test_v24_golden_corpus.py`

This report is the only additional r2 Harness asset and is intentionally uncommitted.
No plan, features, progress, contract, evaluation, r1 report/ledger, `.learnings/`,
`reviews/`, audit Markdown, package metadata, dependency, lock, prompt, role, Policy Gate,
schema or public-tool path was staged or committed.

## PKG-047 — structured preflight contribution integrity

- Blocking and warning preflight clusters now remain structured material when their
  registered participant role is active, even with no model `finding_ids`.
- Correlation uses only bounded structured category/token identities. It does not read
  issue prose, perform fuzzy matching, call a model, introduce weights or multiply
  same-role authority.
- Equivalent preflight and model placeholder/markup evidence contributes once while both
  clusters and evidence sources remain in the full record.
- `unavailable` remains the highest role classification, while its deterministic issue
  remains counted and visible.
- Missing-metrics compatibility rendering no longer infers unique/corroborating or
  unavailable contribution from role prose. Existing material lens evidence remains
  displayable without being converted into a structured contribution claim.

Named evidence:

- Focused final suite:
  `tests/unit/test_v24_value_metrics.py`,
  `tests/integration/test_v24_value_metrics.py`,
  `tests/integration/test_v24_presentation.py`, plus affected compatibility presentation
  tests: `20 passed in 0.26s`.
- Package complete regression: `268 passed in 3.36s`.
- Later integrated focused suite: `17 passed in 0.49s`.
- Later complete regressions: `269 passed in 4.00s`, `269 passed in 3.52s`,
  `269 passed in 3.60s`, and final post-amend `269 passed in 3.67s`.

Reproduced before/after counterexample, `Delete {count} files` -> `删除文件`:

- Accepted r1 Foreman reproduction before r2: chief correctly returned
  `NEEDS_HUMAN_REVIEW`, but technical contribution was `confirmation_only`,
  `unique_material_issue_count=0`, `confirmation_only_role_count=6`, and primary text
  said `未发现新增实质问题；6 个角色完成确认性覆盖` before disclosing the blocker.
- After r2, preflight-only production orchestration: technical contribution
  `unique_material`, `unique_issue_count=1`, aggregate
  `unique_material_issue_count=1`, `confirmation_only_role_count=5`, chief
  `publishability=需人工复核`, `review_needed=是`, status `NEEDS_HUMAN_REVIEW`; primary
  material evidence is present and `未发现新增实质问题` is absent.
- After r2, preflight plus two duplicate model findings: full record retains two clusters,
  but technical and aggregate issue counts remain exactly one.
- After r2, failed technical sampling: technical contribution is truthfully
  `unavailable` with `unique_issue_count=1`; aggregate issue count remains one,
  unavailable count is one, and the false-clean primary line remains absent.
- Each after-path used six standard sampling attempts and zero elicitations; metrics and
  presentation added no calls.

## PKG-048 — executable 18-case Golden Corpus

- The fixture retains exactly the 18 frozen case IDs and declarative expected outcomes;
  it contains no `observed` object.
- `evaluate_golden_cases()` now runs `run_structured_review()` with prompt-aware scripted
  model/user gateways, so observations traverse production preflight, envelope
  validation, clustering, context/outcome forms, Policy Gate, adjudication, chief and
  Council value metrics.
- Case 16 accepts a real context form and performs affected-role context reconsideration.
- Case 17 creates two valid outcomes plus an option rejected by the deterministic
  `forbidden_literal` rule, returns pending, proves the invalid preference is rejected by
  real `continue_structured_review()`, then completes a valid continuation record.
- Negative probes mutate one expected outcome, the placeholder scenario input and the
  clean scenario reviewer envelope, rerunning production behavior each time. No observed
  dictionary is hand-edited.

Final single-corpus execution:

- `18/18` passed; failed cases `[]`.
- Critical recall, false-positive-free rate, contribution classification, conflict
  detection, user authority, chief consistency, call-budget accuracy and discussion
  marginal-value accuracy: all `1.0`.
- Aggregate runtime: `113` scripted sampling calls and `4` scripted elicitations across
  18 cases; each scenario matched its declared baseline and stayed within 6/13/18.
- Case 17: invalid continuation preference rejected, valid continuation completed,
  standard budget `9/13`.
- Focused executable-corpus suite: `4 passed in 0.41s`; integrated Campaign focus:
  `17 passed in 0.49s`.

## Integrated verification

- Final HEAD: `6464f96f681aa3531c14cd631689673561193027`.
- Final compile: `.venv\Scripts\python.exe -m compileall -q src tests` -> exit 0.
- Invariant suite covering V1/V2.0-V2.3 reads, V2.4 full/metadata persistence,
  presentation, five tools, version/build/schema, budgets and concurrency:
  `83 passed in 2.20s`.
- Final complete suite: `269 passed in 3.67s`.
- Baseline-to-HEAD `git diff --check`: passed.
- Exact-path scope audit: passed; seven changed paths, all authorized.
- AST dead-import scan of all three changed production modules: `DEAD_IMPORTS=NONE`.
- Fixture runtime proof: `rg '"observed"' tests/fixtures/v24_golden_corpus.json` returned no
  matches; runner directly imports/calls production orchestration.
- Fresh `uv build` succeeded:
  - wheel `council_of_translation-0.10.0-py3-none-any.whl`, SHA-256
    `6364CE1E86CE37457B2C7F56334F4FC92068A4451D9EFE4E4C4BB9ABAA4130EC`
  - sdist `council_of_translation-0.10.0.tar.gz`, SHA-256
    `B0AF5F30E902F13E4B2CFECA8A57E11921AB85173CCF87845CAB9CDF0A17BBC1`
- Isolated wheel smoke: Python `3.12.9`, FastMCP `3.4.7`, installed distribution/module
  `0.10.0`, build `evidence-value-council-v8`, schema `2.4`; all five tools were listed in
  frozen order and called. The scripted placeholder review used `6` sampling attempts,
  `0` elicitations, classified the unavailable technical role truthfully, retained one
  material issue and omitted the false-clean line.
- Temporary pytest, build, artifact and wheel-smoke directories were removed after
  evidence capture.

## Preserved invariants and protected assets

- Exact five public tools; no public parameters added.
- Package/module `0.10.0`, build `evidence-value-council-v8`, schema `2.4`.
- Review-only behavior, prompts, role routing, Policy Gate, user authority, history
  evidence, 6/13/18 budgets and concurrency controls unchanged.
- r1 accepted persistence, ordinary model contribution, discussion trace-delta,
  five-section presentation, minority/degradation and 3,200-code-point evidence remains
  green.
- Protected SHA-256 values matched at admission and final handoff:
  - `harness/plan.md`: `D1782282422F656AAE4F9405988547E6ED220A72287F1CBA0ECF4DB1015492D1`
  - `harness/features.json`: `A5E1A5030C9A307F4A3FE55682D9E5F49A6789C11D34C20F5A407084141DF984`
  - `harness/progress.md`: `CBD623C7C0E45FA80164D51F737A2C3D5ACAFF8AE99E350D6CF5729E956892A3`
  - r1 contract: `3D477E8418B77A621EFEBB3BD496CD0508BCC9C39A22D833EFA79886A98EE366`
  - r1 Foreman review: `D85B7C35026C394001C7C17DE5FCE591128D917BB1961FA67ADED19E88FE3292`
  - r1 Worker report: `412A1E032B919289630EAE58A386B45EF5869B10C91C9FEC76C78313DC8AA37F`
  - r1 ledger: `26AD64BE56B776B9EECD07F927C116E9B360746194D1CE026E3AEE0295A5068A`
  - `.learnings/LEARNINGS.md`: `52DC1BA8043481911C0DEABB3AC882504D9CBE8BB63D60F391C188586A230DF0`
  - `.learnings/ERRORS.md`: `F99EB75886781958BF5AE6DCF844FD476CBCA45937896A25EE3B2E9D6CD34F0A`
  - audit Markdown: `B48073E063C4C9F34E0B6B4DAE94E80079EAAAD3B2F8E273DD60B2F25F6ABD76`
- Final Git index is empty. Final worktree contains only the admitted modified
  `harness/features.json`, `harness/plan.md`, `harness/progress.md`; admitted untracked
  `.learnings/`, r1/r2 contracts, r1 evaluation/report/ledger, audit Markdown,
  `reviews/`; and this required untracked r2 Worker report.

## Commands, deviations, authority and skipped checks

- Principal commands: `python -m compileall -q src tests`; focused and complete `pytest`
  invocations with repository-local `--basetemp`; inline production counterexamples;
  executable-corpus aggregate; `git diff --check`; exact-path and AST import scans;
  `uv build`; isolated `uv venv` plus offline `uv pip install`; in-memory FastMCP client
  calls for all five tools.
- The first focused implementation pass exposed the HTML closing tag as both command and
  tag preflight evidence; bounded structured tag-name correlation fixed the duplicate.
  Compatibility presentation regressions then required preserving explicit legacy lens
  evidence without converting prose into contribution classifications.
- `python -m build` was unavailable. The required fresh artifact build used the existing
  repository release tool, `uv build`, without dependency or lock changes.
- Initial non-elevated Git index write and user uv-cache read were denied by the sandbox.
  Ten bounded elevated tool invocations were used: four commit/amend operations, two
  fresh build cache reads, two isolated offline install/cache reads, and two artifact
  hash/cleanup operations. The second build/smoke cycle regenerated evidence after the
  final deterministic-evaluator amendment. No other authority was requested.
- The first wheel-smoke assertion incorrectly assumed the user's existing history was
  empty; it was corrected to validate the returned integer/shape without altering or
  deleting that protected history. All five calls then passed.
- The self-improvement skill was consulted after failed commands, but its requested
  `.learnings/` write was skipped because the Campaign explicitly protects that path.
- No required verification was skipped. Live Goose/provider/model checks were prohibited
  and therefore not run. No network provider call, push, PR operation, release, deploy or
  credential action occurred.
- Counts: subagents `0`; live Goose/provider/model calls `0`; provider/network model calls
  `0`; pushes/PRs/releases/deployments `0`.

## Remaining risks

- The golden runner intentionally uses deterministic scripted gateways. It proves the
  production orchestration and authority boundaries offline, but does not measure live
  model response quality; live calls were contractually forbidden.
- Structured issue correlation is deliberately exact and bounded. Semantically similar
  prose with no shared protected token remains separate rather than introducing the
  forbidden fuzzy/prose heuristic.
