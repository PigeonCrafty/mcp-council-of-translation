# CAMPAIGN-006-r2 Main Worker Ledger

## Control

- Role: WORKER / MAIN WORKER
- Mode: STRICT_CAMPAIGN
- Contract: `harness/contracts/CAMPAIGN-006-r2.md`
- Contract SHA-256: `70756EC6B7DA60086EA15E165EF4D21B81E359E32B3FA5FC886E47752ADF8CD2`
- Baseline: `403310ccdfcbb026bd2b375517d14dc927286604`
- Subagents: forbidden / 0
- Live Goose/provider/model calls: 0

## Admission

- Exact HEAD and subject `Plan context-coherent Council V0.8`: pass.
- Git index: empty; declared Foreman/user dirt only.
- Incorporated r1 and all 11 protected hashes: exact; mismatch count 0.
- `python -m compileall -q src tests`: pass.
- Full baseline: `203 passed in 2.47s`.
- Deterministic counterexamples reproduced before edits:
  - lightweight/standard marketing: 3 roles; strict: 5 roles;
  - brand/UI and official-glossary variants: 0 selected, both `immaterial_gap`;
  - declined selected context: two forms, one accepted outcome, `COMPLETED`;
  - raw `ux`, `。；依据`, and suppressed pseudo-decision all visible.

## Package state

| Package | State | Files | Verification | Commit |
| --- | --- | --- | --- | --- |
| PKG-032 | MAIN_WORKER_VERIFIED | guided, prompt, orchestration, classification test | `10 passed` | `7f5a03c3cfdd5816e6a2702621fe529ed4e4053e` |
| PKG-033 | MAIN_WORKER_VERIFIED | orchestration, precedence workflow test | included in `30 passed`; all unresolved actions and actual-answer order | `06aa90c7da30bb7ec1ea3a0c51578874c90ce6a0` |
| PKG-034 | MAIN_WORKER_VERIFIED | roles, routing/budget tests | included in `30 passed`; exact six and deep 13/13 | `06aa90c7da30bb7ec1ea3a0c51578874c90ce6a0` |
| PKG-035 | MAIN_WORKER_VERIFIED | digest, presentation/record tests | `24 passed`; combined PKG-032–035 `47 passed` | `8912cb95891f9ca0700e501579d670a71e18aaef` |
| PKG-036 | MAIN_WORKER_VERIFIED | version loci, docs, package tests | `34 passed`; compile; full `217 passed` | `8ed8d866076acab9dc22a57c6fd31d4ff6792fe4` |

## Incidents and deviations

- PKG-032 first focused run: `4 passed, 6 failed`. Three failures exposed missing
  compatibility terms (`受众`, `交互`, `风险`); one new assertion incorrectly expected
  a nonexistent `selected` persisted disposition; downstream failures were consequences
  of the same selection miss. Corrected the deterministic vocabulary and assertion
  without changing schema or accepting generic importance prose.
- PKG-033 first focused run: `15 passed, 2 failed`. One new assertion used the wrong
  existing phase name; one conflicted with the accepted `answered_count` meaning of
  submitted form fields. Restored that count while deriving material resolution only
  from real non-assumption answers and `ContextGapV2.disposition`.
- PKG-034 first focused run: `26 passed, 4 failed`. Making brand/risk globally standard
  expanded the unspecified default route from six to eight and broke accepted budget
  fixtures. Reverted global applicability and implemented the frozen six only in the
  standard/strict marketing selector; UI/docs/unspecified routing remains unchanged.
- PKG-036's first combined documentation/version patch did not apply because the
  `server.py` context had drifted from the patch hunk. `apply_patch` failed atomically;
  no partial edit occurred. The patch was split by file and applied successfully.
- Fresh build completed and produced both 0.8.0 artifacts. Sandboxed `Get-FileHash`
  could not read their Windows ACLs; the same read-only hash command was rerun with
  approved elevation and succeeded.
- The first isolated-wheel assertion used a nonexistent aggregate `defaults` key in
  `get_server_info`; inspection showed the accepted top-level `default_*` fields. The
  next assertion used role names without the accepted `_reviewer` suffix and treated
  the permitted review-ID footer as the final substantive verdict. A diagnostic run
  localized both test-script assumptions. The corrected assertion run passed without
  product changes.

## Integrated verification

- `python -m compileall -q src tests`: pass after implementation.
- `python -m pytest -q -p no:cacheprovider --basetemp .tmp/campaign006-r2-final-full`:
  `217 passed in 2.44s`.
- Source registered-tool probe: exact five tools, package/module `0.8.0`, build
  `context-coherent-council-v6`, schema `2.2`, review-only defaults and budgets
  `6/13/18`: pass.
- `uv build --out-dir .tmp/campaign006-r2-dist`: pass; fresh wheel and sdist created.
- Isolated current-resolution wheel environment: CPython 3.12.9, FastMCP 3.4.7;
  installed import came from the environment's `site-packages`. Registered
  `get_server_info` and `view_review_record` calls passed. The actual scripted standard
  marketing record had the frozen six roles, six role lenses, 6/6 successful samples,
  full coverage, a 575-code-point primary response and full structured history.
- Artifact SHA-256: wheel
  `BADAAF69C3C9335EBBEF3B5B6A7EA3BBBF57C236870767BA3928E60D0BA61A7D`;
  sdist `6838F8A2DA7A11856014031F309A2D20BDCE160D65583ED99641127BA6075614`.
- `git diff --check 403310ccdfcbb026bd2b375517d14dc927286604..HEAD`: exit 0.
- Baseline diff: 23 authorized paths, 629 insertions, 53 deletions; unauthorized path
  mismatch count 0. Git index remains empty.
- Final protected-hash comparison: all 11 exact; mismatch count 0. Contract hash remains
  `70756EC6B7DA60086EA15E165EF4D21B81E359E32B3FA5FC886E47752ADF8CD2`.

## Authority and external activity

- Subagents: 0 (forbidden by contract).
- Sandbox authority escalations: 4, limited to the repository-local fresh build,
  repository-local uv environment creation/install using shared caches, and read-only
  artifact hashing.
- Live Goose/provider/model calls: 0.
- Pushes, PRs, releases, deployments, credentials and Goose modifications: 0.
