# CAMPAIGN-013-r2 Main Worker Ledger

## Control

- HARNESS_ROLE: WORKER / MAIN WORKER
- HARNESS_MODE: STRICT_CAMPAIGN
- Campaign: `CAMPAIGN-013-r2`
- Contract: `harness/contracts/CAMPAIGN-013-r2.md`
- Contract SHA-256: `0FD5641A76FB859C14FB4D331B00E38931AEA98589C5D580F0E675DB4537B4E2`
- Original baseline: `44b1969677cd6b1fda63047ca514aede6609bdad`
- Revision baseline / admitted HEAD: `6a07f4ebc61146e60af8bb6e7456f2b144ce15a4`
- Preserved package commit: `6a07f4ebc61146e60af8bb6e7456f2b144ce15a4` (PKG-075)
- Executor: Codex Main Worker
- Subagents: 0

## Admission

- Read complete: pigeon-harness skill, common protocol, Worker protocol, `AGENTS.md`, Harness plan/features/progress, r1/r2 contracts, r1 Foreman review, r1 Worker report and r1 ledger.
- HEAD, local `origin/main`, empty index, preserved PKG-075 three-path commit, exact admitted PKG-076 intermediate hashes and every r2 protected hash: PASS.
- Dirty/untracked set: exactly the r2-admitted Foreman/user assets plus the exact PKG-076 intermediate; protected paths were not traversed where forbidden.
- `\.venv\Scripts\python.exe -m compileall -q src tests`: PASS.
- Initial basetemp attempt failed before product execution because `.tmp/campaign013-r2-worker` did not yet exist: 351 passed, 126 setup errors. The parent was created inside the contract-authorized temporary boundary and the exact command was rerun. The self-improvement logging target `.learnings/**` is protected and was not read or modified.
- `\.venv\Scripts\python.exe -m pytest -q --basetemp .tmp/campaign013-r2-worker/admission`: exact expected intermediate, `467 passed, 10 failed`.
- Expected failures: seven stale r3 fallback assertions, two downstream PKG-079 Schema assertions and one downstream PKG-077 metadata receipt assertion.

## Protected and authorized boundaries

- Preserved: all Foreman-owned Harness state, prior contracts/evaluations/reports, `.learnings/**`, `reviews/**`, `myTest/**`, audit Markdown and all other user assets.
- Authorized: inherited r1 paths, r2-only assertion migration in `tests/integration/test_r3_outcome_suppression.py` and `tests/integration/test_r3_workflow.py`, this ledger/report and `.tmp/campaign013-r2-worker/**`.
- Forbidden: live Goose/provider/model calls, remote mutation, push/PR/release/deploy, public-surface/routing/prompt/budget/concurrency changes.

## Package execution

| Package | Executor | State | Commit | Notes |
| --- | --- | --- | --- | --- |
| PKG-075 | prior Main Worker | preserved | `6a07f4ebc61146e60af8bb6e7456f2b144ce15a4` | Three-path committed classifier/model foundation preserved. |
| PKG-076 | Codex Main Worker | complete | `393b947` | Seven stale assertions migrated; 20/20 legacy tests pass; affected matrix `105 passed, 1 failed` only at downstream receipt; full `474 passed, 3 failed` only at contracted PKG-077/079 assertions. |
| PKG-077 | Codex Main Worker | complete | `613faee` | Receipt 1.1 exact projection/history availability plus one-line normal support presentation; focused `194 passed`; full `478 passed, 2 failed` only at downstream release Schema assertions. |
| PKG-078 | Codex Main Worker | complete | `2ed6973` | Prior 24 canonical hash preserved; six calibration cases appended; exact 30/30, prior eight metrics 1.0, two new accuracy/coherence metrics 1.0 and false-reassurance 0.0; mutation controls pass. |
| PKG-079 | Codex Main Worker | complete | `b01461b792ecb5eeda20229d47a404015ec6910c` | V0.13.0/build v11/Schema 2.6/receipt 1.1, operator docs and pinned uv 0.12.3 root-only lock refresh; release matrix 167 passed; full 480 passed. A final dead-import scan found two F401 imports; they were removed and the scoped commit was amended before handoff, then the focused 39-test set, compile and full 480-test suite passed again. |

### Exact package manifests

- PKG-075: `src/council_of_translation/localization/decision_support.py`, `src/council_of_translation/localization/models.py`, `tests/unit/test_decision_support.py`.
- PKG-076: `src/council_of_translation/localization/compatibility.py`, `decision_support.py`, `models.py`, `orchestration.py`, `persistence.py`; `tests/integration/test_orchestration_v2.py`, `test_r3_outcome_suppression.py`, `test_r3_workflow.py`, `test_r4_reviewer_coverage.py`, `test_v21_reconsideration.py`, `test_v22_briefing.py`, `test_v26_decision_support.py`; `tests/unit/test_decision_support.py`, `test_persistence_v2.py`, `test_v22_models_persistence.py`.
- PKG-077: `src/council_of_translation/localization/digest.py`, `orchestration.py`, `verification.py`; `tests/integration/test_tool_surface_v2.py`, `test_v24_presentation.py`, `test_v26_decision_support.py`; `tests/unit/test_persistence_v2.py`, `test_verification_receipt.py`.
- PKG-078: `src/council_of_translation/evaluation.py`, `tests/fixtures/v24_golden_corpus.json`, `tests/integration/test_v24_golden_corpus.py`.
- PKG-079: `AGENTS.md`, `README.md`, `docs/v0.4-architecture.md`, `docs/v0.4-tool-contract.md`, `pyproject.toml`, `src/council_of_translation/__init__.py`, `src/council_of_translation/localization/orchestration.py`, `tests/integration/test_tool_surface_v2.py`, `test_v08_presentation_invariants.py`, `test_v10_release_contract.py`, `tests/unit/test_decision_support.py`, `test_persistence_v2.py`, `uv.lock`.

### Command evidence

- Admission: `.venv\Scripts\python.exe -m compileall -q src tests` PASS; `.venv\Scripts\python.exe -m pytest -q --basetemp .tmp/campaign013-r2-worker/admission` reproduced `467 passed, 10 failed` after the bounded parent-directory correction.
- Package pytest invocations used only the named package-owned files/matrices above: PKG-076 legacy `20 passed`, affected `105 passed, 1 failed`, full `474 passed, 3 failed`; PKG-077 focused `194 passed`, full `478 passed, 2 failed`; PKG-078 exact runner `30/30`; PKG-079 release matrix `167 passed`.
- Final: classifier `29 passed`; affected matrix `330 passed`; purity `3 passed`; explicit delegation `1 passed`; post-cleanup focused `39 passed`; compile PASS; complete suite `480 passed in 4.78s`.
- Release: repository-local `UV_CACHE_DIR`/`UV_TOOL_DIR`; `uv tool run --from uv==0.12.3 uv lock --refresh`; pinned locked dev sync; pinned build; archive inspection; isolated CPython 3.12 wheel install/reinstall and five-tool smoke; pinned Ruff F401 scan `All checks passed!`.
- Git: per-package exact-path `git add`, four scoped r2 commits (PKG-079 amended only for its two dead-import removals), `git diff --check`, original/revision-baseline name/stat audits, per-commit `git show --name-only`, cached-diff/index checks and final status.

## Counts and deviations

- Authority escalations: 10 successful local Git operations (five exact-path stages and four commits plus the authorized PKG-079 amend); no product/external authority expansion
- Dependency/environment operations: 7 (repository-local pinned uv 0.12.3 acquisition/probe, canonical lock refresh, locked dev sync, isolated CPython 3.12 environment creation, initial wheel/FastMCP install, pinned Ruff acquisition and final wheel reinstall); build invocations: 2
- Live/provider/model calls: 0
- Remote mutations: 0
- Deviations: one corrected local basetemp-parent preparation error, one initially mistyped focused pytest node, one initially invalid multi-operation patch split into valid per-file patches, one initial sandbox-denied `git add` retried with the approved exact-path escalation, a `Get-FileHash -LiteralPath` wildcard error corrected with exact enumerated paths, two installed-wheel smoke harness compatibility/isolation corrections (`list_tools`, list payload and a fresh history directory), one relative smoke executable path error corrected with absolute resolved paths, and one metadata probe key typo corrected after enumerating the real keys. The fresh-build warning about the repository-local cache was closed by archive inspection: zero `.tmp`, `dist` or `build` entries. No production or protected-asset deviation occurred; `.learnings/**` remained unread and unchanged.

## Final verification and artifacts

- Final classifier truth table: `29 passed`.
- Final affected orchestration/persistence/presentation/verification/routing/tool/release matrix: `330 passed`.
- Retrieval purity: `3 passed`; explicit non-degraded delegation counterexample: `1 passed`.
- Final focused post-cleanup set: `39 passed`; `python -m compileall -q src tests`: PASS; full suite: `480 passed in 4.78s`.
- Golden: exact `30/30`; original 24 canonical hash `e8178a926eaf099998956e46e2f132f1c004f14ae5150d04477ac2fef181ba32`; eight inherited metrics `1.0`; support-level and outcome-coherence accuracy `1.0`; false reassurance `0.0`; mutation controls PASS; runtime totals 186 samples, 5 elicitations and budget 374 with zero display/routing sampling.
- Final wheel: `council_of_translation-0.13.0-py3-none-any.whl`, 108621 bytes, SHA-256 `1C851C3455CCEC156DFB86A17A8DB3C7C91A6AAF3205E855CA744269C68459E0`.
- Final sdist: `council_of_translation-0.13.0.tar.gz`, 101583 bytes, SHA-256 `DFB3A1E1508B634B4F0FC1499D0634104D503E2EDEDC66C3F713930D28A7F217`.
- Archive inspection: wheel 31 entries, sdist 42 entries, no temporary/build/dist entries; wheel metadata version 0.13.0; final dead import absent.
- Installed-wheel smoke: isolated CPython 3.12.9 and FastMCP 3.4.7, import from isolated `site-packages`, all five tools called, and clean/limited/insufficient/blocker coherence PASS.
- Exact bounded cleanup: resolved `.tmp/campaign013-r2-worker` against the repository root, verified the target did not escape it, removed it recursively, and confirmed `Test-Path=False` (`REMOVED=True`).
