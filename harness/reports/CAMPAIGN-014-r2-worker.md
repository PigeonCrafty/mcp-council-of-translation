READY_FOR_REVIEW

# CAMPAIGN-014-r2 Main Worker Report

## Control and result

- Contract: `harness/contracts/CAMPAIGN-014-r2.md`
- Verified SHA-256: `6B0A2FB0D122F3E67F12D0A4FADAD2BC17BA93A62DBC7802C748F294EC0FB404`
- Original Campaign baseline: `4f976c2764a463dceb403084fa3faead5300211e`
- Exact revision baseline: `742128a1dfc2282d7aad4ee016d37ff94922c9ca`
- Final HEAD: `9d23ed01f94be2ef0c724b3e0a3e7e1beba75c09`
- Terminal result: READY_FOR_REVIEW. Acceptance remains with the Foreman.

Admission preserved all seven PKG-080 through PKG-086 commits and every byte of the
eight-file unstaged PKG-087 intermediate. Exact HEAD/governance ref/empty-index/commit
chain, all intermediate and protected hashes, compile and the expected focused
`31 passed, 3 failed` state were independently reproduced before edits.

## Campaign commits and scope

1. `ed1f1ec54b730f6a2bf44e73214d36c1e4ec55c8` — PKG-080 fail closed on incomplete review input
2. `2cad51702a77545a4e78419aac99142541f63261` — PKG-081 refine deterministic token scanning
3. `651d97f0d6ad8ce750f96a6a6c51ecbded29193a` — PKG-082 degrade malformed discussion safely
4. `0208badaeaab3f2eec05bd73f8bd8f404015d7dd` — PKG-083 align post-discussion consensus
5. `a523283efa5604dd49331118e941d68a7b851445` — PKG-084 minimize legacy history summaries
6. `5ba1db58ba0075d5f3eff7e3d96ab6ef77b949e9` — PKG-085 narrow evaluator claims
7. `742128a1dfc2282d7aad4ee016d37ff94922c9ca` — PKG-086 bound FastMCP compatibility
8. `9d23ed01f94be2ef0c724b3e0a3e7e1beba75c09` — PKG-087 release V0.13.1 audit remediation

The one r2 commit contains exactly the ten authorized PKG-087 paths: `AGENTS.md`,
`README.md`, the architecture/tool-contract docs, `pyproject.toml`, package `__init__`,
the release/tool-surface/persistence tests and `uv.lock`. The r2 correction itself changed
only stale version/build assertions in the two authorized test files. Original
baseline-to-final scope is exactly 29 authorized paths (`1198 insertions / 134 deletions`);
revision-baseline-to-final is exactly 10 paths (`31 / 31`). Full diff inspection and
`git diff --check` passed.

## Verification

- Focused recovery: exact `31 passed, 3 failed -> 34 passed`.
- Full recovery: exact `572 passed, 3 failed -> 575 passed`; final run
  `575 passed in 5.09s`, zero skips/deselections.
- Final compile: PASS. Integrated affected matrix: `371 passed in 2.74s`.
- Golden: Schema 2.1, exact 30/30, zero failed IDs; all contracted aggregate accuracies
  1.0, insufficient false reassurance 0.0; 186 scripted samples and 5 scripted
  elicitations within a 374-call aggregate budget.
- Invariants: ordered five tools; package/module/build `0.13.1` / `0.13.1` /
  `truthful-boundaries-council-v11.1`; Review/Receipt/Evaluator schemas `2.6/1.1/2.1`;
  frozen defaults; budgets 6/13/18; concurrency 3/3; all 15 routing profiles.
- Purity: no added sampling/elicitation/save/retry call site; V1/V2 history purity,
  privacy, immutability and one-save orchestration remain covered by the integrated/full
  suites. Static import-delta scan found only used `ValidationError`.

## Lock, artifacts and installed-wheel evidence

- Pinned uv: exact 0.12.3. Lock check and locked sync passed.
- Lock SHA-256: `E7E4E44A19A3A7F1813EE3B5CFDC5814A70BF29C71CD5115582AF4E64A352E00`;
  only root version/specifier changed; revision/packages/upload-times remain `3/78/586`.
- Wheel: `council_of_translation-0.13.1-py3-none-any.whl`, 110309 bytes,
  SHA-256 `4582ACDB48D5B6E5C008A0E9B11020B290D60C1C812A6A7F7A7328AC76F1CDB8`.
- Sdist: `council_of_translation-0.13.1.tar.gz`, 103191 bytes,
  SHA-256 `41863D980E3597078CD2B808742D632C62BAA122B0CD56CA0BBA0C1D04C8EE43`.
- Both archives have correct metadata/content and no temp/cache entries.
- Isolated CPython 3.12.9 smokes passed with exact FastMCP 2.13.0.2 and 3.4.7.
  Both imported the wheel from isolated `site-packages`, enumerated and called all five
  tools, and passed clean, truncation fail-closed, malformed-discussion degradation and
  minimized V1-summary checks.

## Reconciliation, deviations and risk

- All 13 r2 protected hashes and workflow hash match; Git index is empty. Both r1/r2
  repository-local Worker temp trees were safely removed. Reports remain untracked and
  unstaged. No protected/user asset was changed, staged, traversed or deleted.
- Required checks skipped: 0. New r2 subagents: 0; preserved r1 subagent assignments: 3.
- Authority expansions: 0; scoped sandbox Git-write approvals: 2.
- Live Goose/provider/model calls: 0; remote calls/mutations: 0; push/PR/publication/
  release/deployment: 0.
- Recorded deviations: one initial basetemp-parent setup error, one install-session
  evidence-capture rerun, and two temp smoke cross-version adapter corrections. Each was
  diagnosed and bounded; all final commands passed without product changes.
- Remaining risk: FastMCP 2.13.0.2 emits its known upstream Authlib deprecation warning.
  The two tested compatibility points pass; this is not a claim about every intervening
  FastMCP version. No Campaign, publication or Q-016 acceptance is claimed.
