# CAMPAIGN-015-r1 Main Worker Execution Ledger

Status: READY_FOR_REVIEW

## Authority

- HARNESS_ROLE: WORKER / MAIN WORKER
- HARNESS_MODE: STRICT_CAMPAIGN
- Contract: `harness/contracts/CAMPAIGN-015-r1.md`
- Contract SHA-256: `98B1AC4DBC7E8F2E7356293E9754BAACA12AF99E6B53145FDA16EEB196A6AE53` (verified)
- Required baseline / observed HEAD: `c7d788ca37ecb5d6bd3f1ebec01d48d5c7d52fb4`
- Admitted local `origin/main`: `dde2761469f5b5f6f8fd841ed4230ba4efe2827b`
- Subagents: forbidden; used 0
- Live Goose/provider/model calls: forbidden; used 0
- Remote Git/GitHub calls: forbidden; used 0

## Admission

- Git index: empty
- Tracked dirty set: exactly `harness/features.json`, `harness/plan.md`, `harness/progress.md`
- Starting-file hashes: all contract values matched
- Protected-asset hashes: all contract values matched
- Forbidden trees `.learnings/**`, `reviews/**`, and `myTest/**`: not read, traversed, copied, hashed, modified, or staged
- `python -m compileall src tests`: PASS
- First full-regression invocation: `.venv\Scripts\python.exe -m pytest -q --basetemp .tmp\campaign015-r1-worker\admission-pytest`
  - Result: environment/setup failure, `426 passed, 150 errors`; the authorized parent temp directory did not yet exist and pytest does not create nested basetemp parents.
  - Correction: created only `.tmp\campaign015-r1-worker`, then used a fresh basetemp.
- Admission rerun: `.venv\Scripts\python.exe -m pytest -q --basetemp .tmp\campaign015-r1-worker\admission-pytest-rerun`
  - Result: PASS, exactly `576 passed in 5.84s`.

## Protected Baseline Hashes

All starting-file and protected hashes enumerated in the frozen contract were verified before editing. Exact reconciliation will be repeated and recorded at handoff.

## Package Log

### PKG-088

- State: COMMITTED
- Inspection command typo: an initial `rg` named the nonexistent `src/council_of_translation/core/orchestration.py`; rerun used the actual `localization/orchestration.py`. A later combined `rg` likewise named a nonexistent `localization/routing.py`; the valid results were retained and routing inspection used `localization/roles.py`.
- Red command: `.venv\Scripts\python.exe -m pytest -q tests\integration\test_v132_continuation_evidence_gap.py --basetemp .tmp\campaign015-r1-worker\pkg088-red`
  - Result: expected FAIL, `1 failed in 0.35s`.
  - Assertion: child status was defective `COMPLETED`, expected `NEEDS_HUMAN_REVIEW` after the parent retained canonical `discussion_unavailable`.
- Production correction: continuation now recognizes only the exact `discussion_unavailable` warning or exact semicolon-delimited fallback code and retains the corresponding fail-closed fields.
- Green command: `.venv\Scripts\python.exe -m pytest -q tests\integration\test_v132_continuation_evidence_gap.py --basetemp .tmp\campaign015-r1-worker\pkg088-green`
  - Result: PASS, `1 passed in 0.26s`.
- Affected command: `.venv\Scripts\python.exe -m pytest -q tests\integration\test_v132_continuation_evidence_gap.py tests\integration\test_orchestration_v2.py tests\integration\test_v21_reconsideration.py tests\integration\test_v131_discussion_coherence.py tests\integration\test_r4_reviewer_coverage.py tests\integration\test_v26_decision_support.py tests\integration\test_v131_input_completeness.py tests\unit\test_decision_support.py --basetemp .tmp\campaign015-r1-worker\pkg088-affected`
  - Result: PASS, `73 passed in 1.97s`, zero skips/deselections/xfails.
- Package diff check: PASS.
- Commit: `d2d49ab` — `PKG-088 preserve continuation discussion evidence`
- Changed paths: `src/council_of_translation/localization/orchestration.py`, `tests/integration/test_v132_continuation_evidence_gap.py`
- First sandboxed `git add` attempt failed with `.git/index.lock: Permission denied`; the authorized local stage operation was rerun with filesystem escalation. No remote or network authority was used.

### PKG-089

- State: COMMITTED
- Focus command: `.venv\Scripts\python.exe -m pytest -q tests\integration\test_v132_continuation_evidence_gap.py --basetemp .tmp\campaign015-r1-worker\pkg089-focus`
  - Result: PASS, `2 passed in 0.27s`.
- Expanded affected command: `.venv\Scripts\python.exe -m pytest -q tests\integration\test_v132_continuation_evidence_gap.py tests\integration\test_orchestration_v2.py tests\integration\test_v21_reconsideration.py tests\integration\test_v131_discussion_coherence.py tests\integration\test_r4_reviewer_coverage.py tests\integration\test_v26_decision_support.py tests\integration\test_v131_input_completeness.py tests\unit\test_decision_support.py tests\integration\test_v12_verification_view.py tests\unit\test_verification_receipt.py tests\unit\test_persistence_v2.py --basetemp .tmp\campaign015-r1-worker\pkg089-affected`
  - Result: PASS, `228 passed in 2.23s`, zero skips/deselections/xfails.
- Evidence: parent bytes/model immutable; child linked; full/compact/phase/display/receipt terminal fields coherent; canonical receipt JSON equals text copy; receipt complete with no redactions; clean continuation does not acquire sticky discussion degradation; parent/child saves `2`, sampling prompts `7 + 1`, elicitation `0`, no retry.
- Package diff check: PASS.
- Commit: `16da96b` — `PKG-089 verify continuation terminal coherence`
- Changed path: `tests/integration/test_v132_continuation_evidence_gap.py`

### PKG-090

- State: GREEN, pending commit
- Version/build migration: package/module `0.13.2`; diagnostic build `truthful-boundaries-council-v11.2`; Schemas unchanged `2.6/1.1/2.1`.
- Provenance correction: the V0.13.1 stage report now distinguishes all six contract-frozen SHA roles and explicitly states that `9d23ed01...` is not the final protected-main runtime publication SHA.
- Lock tool: exact `uv 0.12.3 (507230998 2026-08-07 x86_64-pc-windows-msvc)` acquired with repository-local `UV_CACHE_DIR` and `UV_TOOL_DIR`.
- Lock command: `uvx --from uv==0.12.3 uv lock --refresh`
  - Result: resolved 78 packages; only editable root `0.13.1 -> 0.13.2`.
  - Before: 200959 bytes, SHA-256 `E7E4E44A19A3A7F1813EE3B5CFDC5814A70BF29C71CD5115582AF4E64A352E00`.
  - After: 200959 bytes, SHA-256 `8D6F90F994B44E4785B31965F8A5CFA7AD40F3D55D9A43F53D0A993F79EE66EF`.
  - Invariants: revision/package/upload-time `3/78/586`; dependency graph unchanged.
- Release matrix: `38 passed in 1.40s`, zero skips/deselections/xfails.
- Integrated affected matrix: `246 passed in 2.46s`, zero skips/deselections/xfails.
- Golden pytest: `4 passed in 1.16s`.
- Golden production aggregate: Schema `2.1`, exact `30/30`, `failed_case_ids=[]`; all inherited accuracy metrics plus decision-support/coherence metrics `1.0`; insufficient false-reassurance `0.0`.
- Final compile: PASS.
- Complete regression: `578 passed in 6.41s`, zero skips; greater than admitted 576.
- Dead-import scan: PASS, zero unused imports across 6 changed Python files.
- First invariant probe failed because the Worker temp script imported nonexistent `EVALUATOR_SCHEMA_VERSION`; corrected to validate the actual evaluator output. Rerun PASS: tools/routes/budgets/concurrency/version/build/Schemas/defaults `5/15/6-13-18/3-3/0.13.2/v11.2/2.6-1.1-2.1/frozen`.
- Fresh build: exact pinned uv; PASS. Upstream warning said repository-local uv cache was inside the source directory; archive member inspection proved no cache/temp asset was included.
- Artifact inspection first attempt failed because the Worker temp script assumed `Requires-Python` ordering `>=3.10`; actual canonical metadata is `<3.14,>=3.10`. Semantic check corrected and rerun PASS.
- Wheel: `council_of_translation-0.13.2-py3-none-any.whl`, 110425 bytes, SHA-256 `4BB74C181EE516E7E12C1BA25369649ED5AF070E507940D64FCB78D8936AEC8E`, 31 members.
- Sdist: `council_of_translation-0.13.2.tar.gz`, 103515 bytes, SHA-256 `28B77549974D410283D4CFA34380A7722547ED02B49A87FCCC79F82879CA881A`, 42 members.
- Archive audit: correct version/Python/FastMCP metadata; production package present; no Harness, audit, review, learning, user, test, Git or temp assets.
- FastMCP 2.13.0.2 / CPython 3.12.9 installed-wheel smoke: PASS from isolated `Lib/site-packages`; five tools called; frozen invariants, adversarial full/compact/phase/report/receipt path and clean control passed. Known upstream Authlib deprecation warning recorded.
- FastMCP 3.4.7 first smoke attempt failed in the Worker temp script because FastMCP 3 removed server-side `mcp.get_tools()`. The probe was corrected to use cross-version client `list_tools()`; rerun PASS from isolated `Lib/site-packages`, five tools called, adversarial and clean controls passed. The corrected probe was also rerun on FastMCP 2.13.0.2 and passed.
- Package diff and new-document whitespace checks: PASS.
- Commit: `c0f0d190ff5b5bc753f9dc743ce3a5743fe32bdf` — `PKG-090 release V0.13.2 terminal truthfulness closure`
- Changed paths: `AGENTS.md`, `README.md`, `docs/v0.13.1-stage-closure-report.md`, `docs/v0.13.2-terminal-truthfulness-closure.md`, `docs/v0.4-architecture.md`, `docs/v0.4-tool-contract.md`, `pyproject.toml`, `src/council_of_translation/__init__.py`, `tests/integration/test_tool_surface_v2.py`, `tests/integration/test_v10_release_contract.py`, `tests/unit/test_persistence_v2.py`, `uv.lock`.

## Final Reconciliation

- Final HEAD: `c0f0d190ff5b5bc753f9dc743ce3a5743fe32bdf`.
- Local `origin/main`: unchanged `dde2761469f5b5f6f8fd841ed4230ba4efe2827b`.
- Post-commit compile: PASS.
- Post-commit complete regression: `578 passed in 5.91s`.
- Baseline-to-final changed paths: exactly all 14 authorized paths; no outside path.
- Baseline-to-final `git diff --check`: PASS.
- Exact commit path audits: PASS for PKG-088, PKG-089 and PKG-090.
- Protected hashes: all 12 contract values MATCH.
- Contract hash recheck: `98B1AC4DBC7E8F2E7356293E9754BAACA12AF99E6B53145FDA16EEB196A6AE53`.
- Tracked dirty files remain exactly protected `harness/features.json`, `harness/plan.md`, `harness/progress.md`.
- Git index: empty.
- Required checks skipped: none.
- Subagents: 0.
- Successful local Git filesystem authority escalations: 6 (three stage and three commit cycles); authority expansion: 0.
- Dependency/environment operations: 7 (pinned uv acquisition, lock refresh, one build, two isolated venv creations, two exact FastMCP wheel installs); build invocations: 1.
- Live Goose/provider/model calls: 0. Remote Git/GitHub calls: 0. Push/PR/tag/release/publish/deploy calls: 0.
- Bounded temp cleanup: PASS; verified absolute target `C:\Users\GeZhu\MyMCP\mcp-council-of-translation\.tmp\campaign015-r1-worker`, removed recursively, and confirmed absent.
