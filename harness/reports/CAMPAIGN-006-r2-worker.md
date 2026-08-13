# CAMPAIGN-006-r2 Main Worker Report

## Terminal status

`READY_FOR_REVIEW`

This is a Worker handoff, not Campaign acceptance or project-completion authority.

## Control and admission

- Role: WORKER / MAIN WORKER
- Mode: STRICT_CAMPAIGN
- Contract: `harness/contracts/CAMPAIGN-006-r2.md`
- Contract SHA-256:
  `70756EC6B7DA60086EA15E165EF4D21B81E359E32B3FA5FC886E47752ADF8CD2`
- Exact admitted baseline: `403310ccdfcbb026bd2b375517d14dc927286604`
  (`Plan context-coherent Council V0.8`)
- Admission index: empty.
- Admission dirt: only the declared modified Foreman Harness files and untracked
  `.learnings/`, r2 contract, audit Markdown and `reviews/`; `myTest/` was absent.
- Admission protected hashes: all 11 exact, mismatch count 0.
- Admission compile: `python -m compileall -q src tests`, exit 0.
- Admission suite:
  `python -m pytest -q -p no:cacheprovider --basetemp .tmp/campaign006-r2-admission` —
  `203 passed in 2.47s`.
- The incorporated r1 contract and every resource required by r2 were read completely.
  CAMPAIGN-006-r1 was used only as the incorporated specification/history and was not
  executed as a separate Campaign.

## Before/after counterexamples

Before implementation, the deterministic probes reproduced all contracted failures:

- marketing used 3 roles in lightweight/standard and 5 in strict;
- the live brand-vs-UI question and binding official-glossary question selected zero
  gaps and were labeled `immaterial_gap`;
- declining context still allowed a second outcome request, an accepted outcome and a
  `COMPLETED`/publishable result;
- raw `ux`, composed `。；依据` punctuation and a suppressed-gap pseudo-decision appeared
  in primary text.

After implementation and focused probes:

- lightweight marketing remains the frozen 3; standard and strict marketing use exactly
  `fidelity_reviewer`, `terminology_reviewer`, `product_context_reviewer`,
  `brand_voice_reviewer`, `risk_ambiguity_reviewer`, `fluency_reviewer` in that order;
- brand/UI, binding-glossary, semantic/audience, routing and release-impact variants are
  material, while generic curiosity/importance remains suppressed; duplicate, answered,
  inactive-role and two-question bounds remain deterministic;
- decline/cancel/error/unsupported/malformed/explicit-assumption context outcomes make
  zero outcome requests and return truthful human-review degradation; a real answer
  triggers only affected active-role context reconsideration before the outcome phase;
- unresolved questions remain visible without pseudo-decisions, raw `ux` and composed
  punctuation are normalized, and material evidence/minority conditions remain visible;
- a literal V2.2 standard-marketing record proves six valid role IDs, six structured
  reviewer successes, full coverage, 6 sampling calls, zero elicitation and six role
  lenses.

## Packages, commits and files

Final HEAD is `8ed8d866076acab9dc22a57c6fd31d4ff6792fe4`. Four scoped local commits were created;
none was pushed:

1. PKG-032 — `7f5a03c3cfdd5816e6a2702621fe529ed4e4053e`
   `Classify material Council context gaps`
   - `localization/guided.py`, `prompt_builders.py`, `orchestration.py`
   - `tests/integration/test_v08_context_classification.py`
2. PKG-033/PKG-034 — `06aa90c7da30bb7ec1ea3a0c51578874c90ce6a0`
   `Enforce context-first marketing Council flow`
   - `localization/orchestration.py`, `roles.py`
   - `tests/integration/test_v08_context_precedence.py`,
     `test_v08_marketing_routing.py`, `tests/unit/test_roles_v2.py`
3. PKG-035 — `8912cb95891f9ca0700e501579d670a71e18aaef`
   `Present unresolved Council context truthfully`
   - `localization/digest.py`
   - context-precedence assertions and
     `tests/integration/test_v08_presentation_invariants.py`
4. PKG-036 — `8ed8d866076acab9dc22a57c6fd31d4ff6792fe4`
   `Release context-coherent Council 0.8.0`
   - package/module/runtime/persistence/tool/server version loci, `pyproject.toml`,
     `uv.lock`
   - `AGENTS.md`, `README.md`, architecture/tool-contract docs
   - affected tool-surface and persistence tests.

The complete baseline diff contains exactly 23 authorized paths: `AGENTS.md`,
`README.md`, two docs, `pyproject.toml`, `uv.lock`, ten source files under
`src/council_of_translation`, four new `test_v08_*` integration files and three affected
existing test files. Diff total: 629 insertions, 53 deletions. No Harness contract,
plan, feature, progress, evaluation, prior report, learning, review or audit asset was
included in a commit.

## Package and integrated verification

- PKG-032 focused final: `10 passed`.
- PKG-033/034 focused final: `30 passed`; includes all unresolved actions, real-answer
  precedence, exact routing matrix and the deep standard-marketing 13/13-call path
  (6 independent + 3 context reconsiderations + 1 discussion + 3 outcome
  reconsiderations).
- PKG-035 focused final: `24 passed`.
- Combined PKG-032 through PKG-035: `47 passed in 1.38s`.
- PKG-036 package/tool/persistence focused final: `34 passed`.
- Final compile: `python -m compileall -q src tests`, exit 0.
- Final full suite:
  `python -m pytest -q -p no:cacheprovider --basetemp .tmp/campaign006-r2-final-full` —
  `217 passed in 2.44s`.
- Source registered-tool probe: exact five public tools; package/module `0.8.0`;
  diagnostic build `context-coherent-council-v6`; schema `2.2`; review-only true;
  defaults `review_only/auto/auto/summary/full/council_adjudication`; budgets `6/13/18`;
  standard and strict marketing exact frozen six.
- `git diff --check 403310ccdfcbb026bd2b375517d14dc927286604..HEAD`: exit 0.
- Allowed-path audit: 23/23 authorized; mismatch count 0.

## Fresh build and isolated wheel smoke

- `uv build --out-dir .tmp/campaign006-r2-dist`: passed.
- Wheel:
  `council_of_translation-0.8.0-py3-none-any.whl`, SHA-256
  `BADAAF69C3C9335EBBEF3B5B6A7EA3BBBF57C236870767BA3928E60D0BA61A7D`.
- Sdist: `council_of_translation-0.8.0.tar.gz`, SHA-256
  `6838F8A2DA7A11856014031F309A2D20BDCE160D65583ED99641127BA6075614`.
- Fresh repository-local CPython 3.12.9 environment resolved 70 current packages and
  installed FastMCP 3.4.7 plus the wheel.
- Isolated `-I` import resolved from the environment's `site-packages`, not repository
  source.
- Registered `get_server_info` and `view_review_record` calls passed. The installed
  server exposed exactly five tools and the expected version/build/schema/defaults/
  budgets. An actual scripted standard-marketing review used the frozen six roles,
  produced six role lenses, 6/6 successful samples, full reviewer coverage, a
  575-code-point primary response and full structured history.
- FastMCP 2.13 dual-channel behavior is reused from the accepted r1 evidence as the
  contract authorizes; current-FastMCP 3.4.7 is independently proven above.

## Protected state and final Git state

All final protected SHA-256 values match the contract, mismatch count 0:

- plan `72F036...C8C7`; features `CFD4CF...C8B0`; progress `9DC178...B010`;
- r1 contract `29580D...AA3F`; q009 review `99725B...E54A`; Campaign-005 review
  `6DC51D...D41C`; Campaign-005 contract `F47CC1...5E02`; Campaign-005 Worker report
  `41A7C...A93`;
- learnings `22F939...658F` / `F99EB7...34F0`; audit Markdown `B48073...BD76`.

Final HEAD: `8ed8d866076acab9dc22a57c6fd31d4ff6792fe4`. Final index is empty. The only worktree
dirt is the original protected Foreman/user state plus the authorized untracked r2
contract, ledger and Worker report. Build/test artifacts are under ignored `.tmp/`.

## Skips, delegation, authority and deviations

- Skipped by prohibition: live Goose/provider/model calls, push, PR, release, deploy,
  credential changes and Goose modification.
- Subagents: 0; subagents were forbidden.
- Live Goose/provider/model calls: 0. All model behavior tests used deterministic local
  scripted executors.
- Sandbox authority escalations: 4 — fresh `uv build`, repository-local `uv venv`, wheel
  dependency install/current resolution, and read-only artifact hashing after Windows
  ACL denial. No credential or deployment authority was requested.
- Retry history:
  - focused failures in PKG-032/033/034 exposed deterministic vocabulary, accepted field
    semantics and route-isolation mistakes; each was corrected inside its package before
    commit and is detailed in the ledger;
  - one combined PKG-036 patch failed atomically on a stale context hunk, then succeeded
    when split by file;
  - the wheel product ran correctly, but two assertion drafts encoded incorrect public
    field/role/footer assumptions. A read-only diagnostic localized them; the corrected
    asserted smoke passed without product changes;
  - sandboxed artifact hashing hit Windows ACL denial and passed under approved read-only
    elevation.

## Remaining risks and Foreman launch prompt

No known contract blocker remains. No live provider behavior was tested by prohibition;
the fresh wheel used deterministic scripted reviewer envelopes. Foreman must independently
verify acceptance and may reject or issue a revision contract.

Suggested independent Foreman launch prompt:

> HARNESS_ROLE: FOREMAN  
> Use pigeon-harness to independently evaluate CAMPAIGN-006-r2 from baseline
> `403310ccdfcbb026bd2b375517d14dc927286604` through Worker HEAD
> `8ed8d866076acab9dc22a57c6fd31d4ff6792fe4`. Read
> `harness/contracts/CAMPAIGN-006-r2.md`,
> `harness/reports/CAMPAIGN-006-r2-ledger.md`, and
> `harness/reports/CAMPAIGN-006-r2-worker.md`; verify protected hashes, commits, exact
> routing/context precedence/presentation counterexamples, 217-test regression, fresh
> artifacts and isolated wheel evidence. Do not infer acceptance from the Worker report;
> issue the independent Campaign evaluation.
