# CAMPAIGN-006-r3 Main Worker Report

## Terminal status

`READY_FOR_REVIEW`

This is a Worker handoff. Campaign acceptance and project-completion authority remain
with the Foreman.

## Control and admission

- Role: WORKER / MAIN WORKER
- Mode: STRICT_CAMPAIGN
- Contract: `harness/contracts/CAMPAIGN-006-r3.md`
- Contract SHA-256:
  `1AA82AFAC5E8A9AFD01A1DD3D7457F58AF700ED1CF5D68B799E0688B67C9759A`
- Exact baseline: `8ed8d866076acab9dc22a57c6fd31d4ff6792fe4`
  (`Release context-coherent Council 0.8.0`)
- Admission HEAD/subject: exact; Git index empty.
- Admission worktree: only declared modified Foreman Harness files and untracked
  Foreman/user/r2-r3 Harness assets; `myTest/` was absent.
- Admission protected hashes: 12/12 exact, mismatch count 0.
- Admission compile:
  `.venv\Scripts\python.exe -m compileall -q src tests` — passed.
- Admission full suite:
  `.venv\Scripts\python.exe -m pytest -q -p no:cacheprovider --basetemp
  .tmp\campaign006-r3-admission` — `217 passed in 3.82s`.
- Completely read before editing: AGENTS.md, r3 contract, r2 contract, r2 Foreman review,
  r2 Worker report/ledger, plan, features and progress, plus the pigeon-harness skill,
  common protocol and Worker protocol.
- CAMPAIGN-006-r2 was treated only as reviewed history; its accepted evidence and
  artifacts were preserved.

## Bounded correction

The internal context-gap selector now receives the existing effective `ReviewTaskV2`
without adding a schema field or public argument.

- An official/approved/binding/designated glossary-existence question is
  `already_answered` only when `term_glossary` is non-empty.
- A corresponding approved-reference-existence question is `already_answered` only when
  `reference_translations` is non-empty.
- Packet values are not parsed for correctness and do not become hard rules or blockers.
- A compound brand-slogan-versus-functional-UI question is `already_answered` only when
  normalized content type and explicit usage context identify the same single side.
- Marketing type alone, an unspecified type, vague context, opposite-side context or
  mixed brand/UI context remains unanswered and enters the existing conservative flow.
- Existing audience/context/tone/domain/content direct-answer checks, semantic dedupe,
  active-role filtering, generic/immaterial suppression and two-question limit remain.

## Before/after truth table

The pre-edit deterministic probe reproduced all four positive failures: each row selected
one unanswered gap.

| Case | Before | After |
| --- | --- | --- |
| Official glossary question + non-empty `term_glossary` | selected / unanswered | suppressed / `already_answered` |
| Approved reference question + non-empty `reference_translations` | selected / unanswered | suppressed / `already_answered` |
| Marketing + `官网首页品牌宣传标语` | selected / unanswered | suppressed / `already_answered` |
| UI + `多步骤设置向导底部主操作按钮` | selected / unanswered | suppressed / `already_answered` |

The post-edit negative table remained conservative:

| Case | Result |
| --- | --- |
| Missing glossary/reference packet | selected / unanswered |
| Unrelated style-guide/project-rules packet | selected / unanswered |
| Glossary packet plus unrelated audience or semantic-correctness question | selected / unanswered |
| Marketing type with no context | selected / unanswered |
| Explicit brand context with unspecified type | selected / unanswered |
| Marketing with vague `官网首页` context | selected / unanswered |
| Marketing plus functional settings-button context | selected / unanswered |
| Mixed brand-slogan and functional-button context | selected / unanswered |
| UI plus brand-slogan context | selected / unanswered |

The Core integration regression additionally proves that a supplied glossary suppresses
the corresponding gap without opening a form, while the same missing glossary remains
unanswered; unsupported interaction then makes zero outcome requests and returns
`NEEDS_HUMAN_REVIEW`.

## Commit and exact files

- Final HEAD: `f3e9bde1b74ff4591d91b66a38558b8bebe6efab`
- Exactly one scoped local commit:
  `f3e9bde1b74ff4591d91b66a38558b8bebe6efab` —
  `Recognize caller-answered context gaps`
- Exact baseline-to-final scope: four authorized files, 160 insertions and 3 deletions:
  - `src/council_of_translation/localization/guided.py`
  - `src/council_of_translation/localization/orchestration.py`
  - `tests/integration/test_v08_context_classification.py`
  - `tests/integration/test_v22_context_gaps.py`
- Unauthorized changed paths: 0. Both allowed production files and both allowed test
  files were the complete implementation scope. No other production, test,
  documentation, package, dependency or Harness state file was changed by the commit.

## Verification

- First required classification/context-precedence/V2.2 context-gap run:
  `17 passed in 0.43s`.
- Preserved routing/deep-budget/presentation/runtime/tool-surface run:
  `22 passed in 1.46s`.
- Final combined focused run over all required suites:
  `39 passed in 1.23s`.
- Precommit compile and full suite: compile passed; `220 passed in 2.86s`.
- Postcommit final compile:
  `.venv\Scripts\python.exe -m compileall -q src tests` — passed.
- Postcommit final full suite:
  `.venv\Scripts\python.exe -m pytest -q -p no:cacheprovider --basetemp
  .tmp\campaign006-r3-final-full` — `220 passed in 2.27s`.
- Source inspection through registered FastMCP tools and `_server_info()`:
  exact five tools; package/module `0.8.0`; build `context-coherent-council-v6`; schema
  `2.2`; review-only; defaults
  `review_only/auto/auto/summary/full/council_adjudication`; budgets `6/13/18`.
- Standard and strict marketing routes remain the exact frozen six in order:
  fidelity, terminology, product context, brand voice, risk/ambiguity and fluency.
- `git diff --check 8ed8d866076acab9dc22a57c6fd31d4ff6792fe4..HEAD`:
  exit 0.
- Allowed-path audit: 4/4 exact, unexpected count 0, missing count 0.
- Final protected-hash audit: all 12 contract-listed assets exact, mismatch count 0;
  r3 contract hash also unchanged.
- Final Git index: empty.

## Preserved evidence and skipped checks

- Preserved r2 behaviors: unresolved decline/cancel/error/unsupported/malformed/
  explicit-assumption paths make zero outcome requests and require human review; actual
  answers retain affected-role precedence; exact marketing routing and deep 13-call path;
  primary presentation and literal V2.2 runtime invariants; exact five tools/version/
  schema/defaults/budgets.
- Fresh artifact build and wheel installation were not run because r3 explicitly says
  they are not required and forbids changes to packaging/runtime-adapter files. The r2
  artifact and current-FastMCP wheel evidence is preserved.
- Live Goose/provider/model calls were prohibited and not run. All behavioral probes used
  local deterministic data and scripted executors.

## Authority, delegation, deviations and risk

- Subagents: 0; forbidden by contract.
- Authority escalations: 1, limited to the contract-required local `git commit`.
- Live Goose/provider/model calls: 0.
- Pushes, PRs, releases, deployments, credentials and Goose modifications: 0.
- Test failures/retries: 0 after editing. No scope or design deviation occurred.
- Remaining risk: recognition intentionally uses a bounded phrase grammar. Equivalent
  caller wording outside that grammar remains conservatively unanswered rather than
  being guessed. No known contract blocker remains.

## Foreman launch prompt

> HARNESS_ROLE: FOREMAN  
> Use pigeon-harness in STRICT_CAMPAIGN mode.  
> Review `harness/reports/CAMPAIGN-006-r3-worker.md` against
> `harness/contracts/CAMPAIGN-006-r3.md` in
> `C:\Users\GeZhu\MyMCP\mcp-council-of-translation`.  
> Inspect the baseline `8ed8d866076acab9dc22a57c6fd31d4ff6792fe4` to final HEAD
> `f3e9bde1b74ff4591d91b66a38558b8bebe6efab` diff and verify independently.  
> Decide ACCEPTED, CHANGES_REQUESTED, or BLOCKED.
