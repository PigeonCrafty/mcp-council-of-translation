BLOCKED

# CAMPAIGN-014-r1 Main Worker Report

## Control and terminal state

- Contract: `harness/contracts/CAMPAIGN-014-r1.md`
- Verified SHA-256: `4FBCF691DF9702587EC6A5D2F5FB1215D4440D3A6229ACBA1D4A969C7F09B2A0`
- Exact admitted baseline: `4f976c2764a463dceb403084fa3faead5300211e`
- Equivalent published product tree: `95d90cf383d045778ce61afaa50dbcec199579ce`
- Admitted governance ref: `bcdb0e2bc282e907e975b43882906872913f6bec`
- Current/final committed HEAD: `742128a1dfc2282d7aad4ee016d37ff94922c9ca`
- Terminal state: BLOCKED during PKG-087. The required eight-commit history and complete passing verification cannot be produced within the exact path allowlist.

Admission passed before edits: exact HEAD/ref/hash, empty index, admitted dirty/untracked set, published-product equivalence, all protected hashes, compile, and exactly `480 passed in 4.67s`.

## Scoped commits and paths

1. `ed1f1ec54b730f6a2bf44e73214d36c1e4ec55c8` — PKG-080 fail closed on incomplete review input
   - `src/council_of_translation/tools/review.py`
   - `src/council_of_translation/localization/orchestration.py`
   - `src/council_of_translation/localization/digest.py`
   - `tests/integration/test_v131_input_completeness.py`
2. `2cad51702a77545a4e78419aac99142541f63261` — PKG-081 refine deterministic token scanning
   - `src/council_of_translation/localization/preflight.py`
   - `tests/unit/test_preflight_v2.py`
3. `651d97f0d6ad8ce750f96a6a6c51ecbded29193a` — PKG-082 degrade malformed discussion safely
   - `src/council_of_translation/localization/deliberation.py`
   - `src/council_of_translation/localization/orchestration.py`
   - `tests/unit/test_deliberation_policy_v2.py`
   - `tests/unit/test_r3_deliberation_policy.py`
   - `tests/integration/test_v131_discussion_coherence.py`
4. `0208badaeaab3f2eec05bd73f8bd8f404015d7dd` — PKG-083 align post-discussion consensus
   - `src/council_of_translation/localization/deliberation.py`
   - `src/council_of_translation/localization/value_metrics.py`
   - `tests/unit/test_r3_deliberation_policy.py`
   - `tests/unit/test_v24_value_metrics.py`
   - `tests/integration/test_v131_discussion_coherence.py`
5. `a523283efa5604dd49331118e941d68a7b851445` — PKG-084 minimize legacy history summaries
   - `src/council_of_translation/tools/review.py`
   - `tests/integration/test_v131_history_minimization.py`
6. `5ba1db58ba0075d5f3eff7e3d96ab6ef77b949e9` — PKG-085 narrow evaluator claims
   - `src/council_of_translation/evaluation.py`
   - `tests/fixtures/v24_golden_corpus.json`
   - `tests/integration/test_v24_golden_corpus.py`
   - `tests/integration/test_v131_evaluation_contract.py`
   - `docs/blind-evaluation-set.schema.json`
   - `docs/v0.13.1-audit-remediation.md`
7. `742128a1dfc2282d7aad4ee016d37ff94922c9ca` — PKG-086 bound FastMCP compatibility
   - `pyproject.toml`
   - `tests/integration/test_v10_release_contract.py`
   - `docs/v0.13.1-audit-remediation.md`

PKG-087 has no commit. Its authorized unstaged intermediate changes `AGENTS.md`, `README.md`, `docs/v0.4-architecture.md`, `docs/v0.4-tool-contract.md`, `pyproject.toml`, `src/council_of_translation/__init__.py`, `tests/integration/test_v10_release_contract.py`, and `uv.lock`. The index is empty. Existing Foreman/user dirty assets remain separate and unchanged.

## Package verification

- PKG-080: truncation focused `7 passed`; affected matrix `194 passed`.
- PKG-081: scanner positive/negative corpus `76 passed`.
- PKG-082: strict malformed discussion matrix `45 passed`; affected discussion/orchestration matrix `71 passed`; exactly one discussion sample and no retry in production counterexamples.
- PKG-083: consensus/digest/metrics/decision-support matrix `103 passed`; convergence and genuine split controls passed.
- PKG-084: V1 full/summary/verification and V2 purity matrix `32 passed`; one load, zero saves, no sampling/elicitation.
- PKG-085: evaluator/schema matrix `13 passed`; direct offline result Schema `2.1`, `30/30`, `critical_presence_contract_accuracy=1.0`, `clean_case_no_cluster_accuracy=1.0`, 186 sampling calls and 5 elicitation calls. JSON Schema 2020-12 positive/negative validation passed.
- PKG-086: release specifier matrix `3 passed`; `uv.lock` remained unchanged for this package.
- PKG-087: pinned `uv 0.12.3` reported `uv 0.12.3 (507230998 2026-08-07 x86_64-pc-windows-msvc)`; `lock --refresh` resolved 78 packages and changed only the editable root version/specifier; locked sync succeeded. Compile passed. Complete regression failed with `3 failed, 572 passed in 6.05s`.

## Blocking defect

The V0.13.1 production identifiers correctly make three stale release assertions fail. One is in authorized `tests/integration/test_tool_surface_v2.py`. The other two are the `full` and `metadata` parameterizations in `tests/unit/test_persistence_v2.py`, which still require package `0.13.0` and build `calibrated-evidence-council-v11`.

`tests/unit/test_persistence_v2.py` is not in CAMPAIGN-014-r1's exact authorized test paths. The contract explicitly says to stop rather than edit a required unlisted path. A production-only workaround would make version metadata caller-dependent and violate the frozen architecture, so none was attempted. Foreman revision must authorize that test path (and the already-listed tool-surface assertion) before PKG-087 can be completed.

## Lock, artifacts and smokes

- Uncommitted canonical lock SHA-256: `E7E4E44A19A3A7F1813EE3B5CFDC5814A70BF29C71CD5115582AF4E64A352E00`.
- Lock invariants: revision 3; 78 packages; 586 upload-time entries.
- Lock diff: only editable root `0.13.0 -> 0.13.1` and root FastMCP specifier `>=2.13.0.2 -> >=2.13.0.2,<4`.
- Fresh wheel/sdist, archive inspection, artifact names/sizes/SHA-256, and both exact FastMCP 2.13.0.2/3.4.7 installed-wheel smokes were not run after the mandatory stop condition. There are therefore no V0.13.1 artifact hashes or wheel-smoke claims.

## Protected reconciliation and hygiene

All 14 contract-pinned protected hashes still match admission:

- `harness/features.json`: `25DCB7F95F27571276EB991522B05C8298990E7C31CBD6A919E4A48323130EAC`
- `harness/plan.md`: `7D55DBA8494ADED34294B081009A66DD048F1FD70ECB911A8628F3E3F6D77AE8`
- `harness/progress.md`: `2E3318B30CC4E53D72D8067D76B6AB5F767459AC27141CDBD1AA3E242D821017`
- independent audit: `0B608DF956448C92AC4112452709129FB45B27478C0F571118660DAA89FBA179`
- prior audit report: `B48073E063C4C9F34E0B6B4DAE94E80079EAAAD3B2F8E273DD60B2F25F6ABD76`
- Foreman response: `7440C47877D2C76313F1848ABCF65269A1A8FD089CE4A3FE9AA4793907903CD4`
- Campaign assessment: `A7D4F770C6F7660964CB926F44A62D3F540F0A3B43C388E1D64B886B900A1529`
- stage report: `DA03138EB0E07F27C1FFEF1F1BA044DB13D590427BC7F8EA3CB53D26168C6C94`
- r3 contract: `473A2DD662297B4061336DC49B7558CFE2054AEAB55F5622750DFAF586EAFC63`
- r3 review: `D33EEFE60F1F23B5574F9B17725C6080B17002137D5E2DFB1B3B0DCE0DABFC05`
- r3 publication-CI review: `6DB2A06357647346B80521EEEAAB0114AE887E0918C80498509C1A21EA9958E9`
- Q-015 contract: `74C4179BA020629D9F34966B0756FFB3547D29710A01A0A820B779A38788EC99`
- Q-015 review: `9675941275A44C11188E794A0908CB7ACF1A3F9AC32377803CCD92598E1AD54B`
- `.github/workflows/ci.yml`: `0B37598E7D53D27B04E5524BAA4D46A2AB69D5E2607A5FF9F0437512CF8EF645`

No protected or user asset was staged or committed. Git index is empty.

Worker temporary basetemps and the repository-local uv cache/tool directory remain because the Campaign stopped before final cleanup. They are confined to `.tmp/campaign014-r1-worker/**`; no admitted asset was deleted or traversed.

## Deviations, calls and remaining risk

- Skipped required checks: final passing full suite, final integrated invariant/dead-import/diff audit, fresh artifact build/archive inspection, both installed-wheel smokes, artifact hashes, final temporary cleanup, and the eighth commit.
- Subagent assignments: 3 — Averroes/`receipt_shape_analysis` implemented bounded PKG-081; Volta/`release_test_analysis` performed read-only PKG-082/083 analysis; Einstein/`tool_surface_analysis` performed read-only PKG-084 analysis. Main Worker inspected/integrated all returned work.
- Contract-scope authority expansions: 0. Sandbox approvals: 7 successful scoped local Git writes; one initial sandboxed Git write failed without changing the index.
- Dependency operations: pinned uv acquisition, canonical lock refresh, locked sync; one editable package build. No dependency graph drift beyond the authorized root specifier.
- Live Goose/provider/model calls: 0. Remote Git/GitHub calls or mutations: 0. Push/PR/publication/release/deploy: 0.
- Remaining blocker: authorize `tests/unit/test_persistence_v2.py` for the two stale V0.13 release assertions, then finish PKG-087 and every skipped verification. No Campaign, publication, Q-016, or project acceptance is claimed.
