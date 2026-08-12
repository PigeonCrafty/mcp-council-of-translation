# CAMPAIGN-002-r1 Execution Ledger

## Control

- Role: `WORKER / CODEX MAIN WORKER`
- Mode: `STRICT_CAMPAIGN`
- Contract: `harness/contracts/CAMPAIGN-002-r1.md`
- Contract SHA-256: `D58590B24E5CF2E4E7F7116F9E9F7B4D621009B6D3986CCA9A7784ECC1EC40BE`
- Baseline: `824559afd68f170758837769b1d1d19df991db4b`
- State: `READY_FOR_REVIEW`
- Acceptance authority: Foreman only

## Admission evidence

- `git rev-parse HEAD`: exact baseline; object type `commit`; subject `Record V0.4 test branch publication`.
- Staged changes: none.
- Tracked dirt: only protected `harness/plan.md`, `harness/features.json`, and `harness/progress.md`.
- Protected untracked roots: `.learnings/`, audit Markdown, `reviews/`, and issued CAMPAIGN-002 contract; `myTest/` absent.
- Contract and all protected hashes matched issuance values, including external live record `8F10CB...A16`.
- `python -m compileall src tests`: exit 0.
- `.venv\Scripts\python.exe -m pytest -q --basetemp .tmp\campaign002-r1-baseline -p no:cacheprovider`: exit 0; `117 passed in 1.48s`.

## Package ledger

| Package | Owner | State | Files | Verification | Commit | Risks/deviations |
| --- | --- | --- | --- | --- | --- | --- |
| PKG-011 | bounded subagent 1 + Main Worker integration | COMMITTED | `models.py`, `compatibility.py`, `persistence.py`, `test_models_v2.py`, `test_persistence_v2.py` | subagent focused `24 passed`; Main focused `24 passed`; Main full `122 passed`; scoped diff-check passed | `d8a5032` | later packages must populate new safe-default fields |
| PKG-012 | bounded subagent 2 (no patch) + Main Worker implementation | COMMITTED | `clustering.py`, `deliberation.py`, `policy.py`, `prompt_builders.py`, new `test_v21_outcomes.py` | focused `24 passed`; full `126 passed`; scoped diff-check passed | `560ec00` | V2.0 direct clustering compatibility retained only when no current candidate is supplied |
| PKG-013 | Main Worker | COMMITTED | `orchestration.py`; four updated integration tests; new `test_v21_elicitation.py` | focused `30 passed`; full `129 passed`; scoped diff-check passed | `1677936` | standard form maps safe values back to exact internal outcomes; delegation is form-only action |
| PKG-014 | Main Worker | COMMITTED | `orchestration.py`; two updated integration tests; new `test_v21_reconsideration.py` | focused `35 passed`; full `132 passed`; scoped diff-check passed | `7601d9c` | lightweight forced path intentionally degrades; standard reference remains within budget |
| PKG-015 | Main Worker | COMMITTED | `orchestration.py`, `policy.py`, new `test_v21_compact.py` | focused `26 passed`; full `135 passed`; scoped diff-check passed | `b312acf` | compact rule context reports presence/kind, never packet contents |
| PKG-016 | Main Worker + bounded subagent 3 read-only review | COMMITTED / VERIFIED | version/build sites, README/AGENTS/docs, bounded corrections and regression tests | final full `141 passed`; focused `74 passed`; compile/build/wheel/diff/hash checks pass | `d08e50d`, `5687208` | no live provider call; build output under ignored `.tmp/` |

## Delegations

1. PKG-011: bounded implementation of V2.1 models, migration, persistence, and focused tests. No Harness, integration-hotspot, Git, external, or acceptance authority.
2. PKG-012: bounded outcome extraction/normalization implementation assignment. It was interrupted after two timeboxes because no file changes were produced; Main Worker implemented the package. No files, Git state, protected assets, or external systems were changed by this subagent.
3. PKG-016: read-only contract/acceptance review. It found deterministic option validation, mixed affirmation, metadata provenance, exact continuation mapping, normalized effective-task, form/compact bounds, and logical continuation-budget gaps. Main Worker corrected each with deterministic regressions. Final pass reported no remaining acceptance blocker and made no files/Git/external changes.

## Events

- Admission gate completed with no deviations.
- PKG-011 delegated after admission; later packages not started.
- Two read-only discovery commands returned exit 1: one named a nonexistent integration-test path and one assumed an incorrect package directory. No writes resulted. The `self-improvement` skill normally requires an `.learnings/ERRORS.md` entry, but Campaign protection of `.learnings/**` takes precedence; the incidents are recorded here instead.
- PKG-011 bounded subagent changed exactly five authorized files and made no Git, Harness, protected-asset, or external changes. It reported focused `24 passed`, all-unit `75 passed`, a pre-final full-suite `121 passed`, `py_compile` and scoped diff-check success.
- Main Worker independently ran `.venv\Scripts\python.exe -m pytest -q tests/unit/test_models_v2.py tests/unit/test_persistence_v2.py --basetemp .tmp\campaign002-pkg011-main -p no:cacheprovider`: exit 0, `24 passed in 0.25s`.
- Main Worker independently ran `.venv\Scripts\python.exe -m pytest -q --basetemp .tmp\campaign002-pkg011-full -p no:cacheprovider`: exit 0, `122 passed in 1.47s`; scoped `git diff --check` also exited 0.
- PKG-011 scoped local commit created: `d8a5032 Add V2.1 review record models` (five authorized files only). Ledger remained uncommitted as required.
- First PKG-012 focused run exposed six regressions: legacy options without `outcome_value` became invalid and the new delegation pseudo-option polluted the accepted Position identity invariant. A second run exposed the remaining delegation identity regression. Main Worker restored legacy read/direct-call behavior and moved delegation responsibility to the PKG-013 form mapping, where it is an interaction action rather than a Position outcome.
- Final PKG-012 focused command `.venv\Scripts\python.exe -m pytest -q tests/unit/test_v21_outcomes.py tests/unit/test_clustering_v2.py tests/unit/test_deliberation_policy_v2.py tests/unit/test_r3_deliberation_policy.py --basetemp .tmp\campaign002-pkg012d -p no:cacheprovider`: exit 0, `24 passed in 0.16s`.
- Final PKG-012 full command `.venv\Scripts\python.exe -m pytest -q --basetemp .tmp\campaign002-pkg012-full2 -p no:cacheprovider`: exit 0, `126 passed in 1.55s`; scoped diff-check exited 0.
- PKG-012 scoped local commit created: `560ec00 Normalize outcome-first review choices` (five authorized files only).
- A malformed read-only `rg` regular expression returned exit 1 during PKG-013 test discovery; corrected immediately with two literal searches. No write resulted and `.learnings/**` remains untouched by Campaign protection.
- Initial PKG-013 focused run had one expected legacy fixture failure because it submitted an internal option ID instead of the new safe form value; corrected the fixture. Focused command `.venv\Scripts\python.exe -m pytest -q tests/integration/test_v21_elicitation.py tests/integration/test_tool_surface_v2.py tests/integration/test_orchestration_v2.py tests/integration/test_r3_workflow.py tests/unit/test_runtime_v2.py --basetemp .tmp\campaign002-pkg013c -p no:cacheprovider`: exit 0, `30 passed in 1.08s`.
- First PKG-013 full run exposed one remaining V0.4 continuation fixture that omitted explicit V2.1 choice fields. The fixture was migrated without weakening its partial-coverage assertion. Final full command `.venv\Scripts\python.exe -m pytest -q --basetemp .tmp\campaign002-pkg013-full2 -p no:cacheprovider`: exit 0, `129 passed in 1.66s`.
- PKG-013 scoped local commit created: `1677936 Add outcome-readable Council elicitation` (six authorized files only); scoped diff-check exited 0.
- Initial PKG-014 focused run produced three expected assertion failures because accepted fixtures still expected all supporting and dissenting roles to be resampled. Assertions were migrated to the frozen dissent-only behavior and exact lower call counts.
- PKG-014 focused command `.venv\Scripts\python.exe -m pytest -q tests/integration/test_v21_reconsideration.py tests/integration/test_orchestration_v2.py tests/integration/test_r4_reviewer_coverage.py tests/integration/test_r3_workflow.py tests/unit/test_deliberation_policy_v2.py --basetemp .tmp\campaign002-pkg014e -p no:cacheprovider`: exit 0, `35 passed in 0.40s`.
- PKG-014 full command `.venv\Scripts\python.exe -m pytest -q --basetemp .tmp\campaign002-pkg014-full -p no:cacheprovider`: exit 0, `132 passed in 1.88s`; scoped diff-check exited 0. Evidence includes standard 8-call success with no supporting-role resample, three-call affected-role cap, requested/completed/skipped/failed provenance, transport failure, and forced lightweight budget degradation with non-clean status.
- PKG-014 scoped local commit created: `7601d9c Target affected-role reconsideration` (four authorized files only).
- PKG-015 focused command `.venv\Scripts\python.exe -m pytest -q tests/unit/test_v21_compact.py tests/integration/test_orchestration_v2.py tests/integration/test_v21_reconsideration.py tests/unit/test_deliberation_policy_v2.py tests/unit/test_r3_deliberation_policy.py --basetemp .tmp\campaign002-pkg015b -p no:cacheprovider`: exit 0, `26 passed in 0.32s`.
- PKG-015 full command `.venv\Scripts\python.exe -m pytest -q --basetemp .tmp\campaign002-pkg015-full -p no:cacheprovider`: exit 0, `135 passed in 1.55s`; scoped diff-check exited 0. Compact/full parity fields, effective input presence without packet copying, bounded digest, warnings/degradation, retrieval hint, review-only rewrite exclusion, no hidden reasoning, and semantic checklist deduplication are directly asserted.
- PKG-015 scoped local commit created: `b312acf Surface compact Council decisions` (three authorized files only).
- PKG-016 version/docs plus audit-correction commit: `d08e50d Release outcome-first V0.5 contract`; final compact-bound follow-up: `5687208 Bound compact review output`. V0.5 identifiers are package/module `0.5.0`, schema `2.1`, diagnostic build `outcome-first-decision-v3`.
- PKG-016 prebuild full test after version edits: one failure because ignored editable `egg-info` still reported `0.4.0`; `_installed_version` now treats the executing module as authoritative when stale editable metadata disagrees. Full rerun passed `135`.
- First wheel smoke installed the wheel with `--no-deps` and failed deep import because FastMCP was absent. The dependency install then completed but the combined command timed out at 120 seconds after installation, before the smoke expression. Re-running the smoke expression succeeded. A final fresh environment with normal dependency resolution succeeded end-to-end.
- Required final compile `python -m compileall src tests`: exit 0.
- Required final full `.venv\Scripts\python.exe -m pytest -q --basetemp .tmp\campaign002-r1-pytest -p no:cacheprovider`: exit 0, `140 passed in 1.96s` before the final bounded-output regression; post-correction full `.venv\Scripts\python.exe -m pytest -q --basetemp .tmp\campaign002-r1-finalfull -p no:cacheprovider`: exit 0, `141 passed in 2.14s`.
- Required focused suite covering models/persistence/outcomes/form/reconsideration/compact/envelopes/coverage/tools: exit 0, `74 passed in 1.69s`; additional final correction focus: `23 passed in 0.30s`.
- Fresh build `$env:UV_CACHE_DIR='.tmp\campaign002-uv-cache'; uv build --out-dir .tmp\campaign002-dist`: exit 0; produced `council_of_translation-0.5.0.tar.gz` and `council_of_translation-0.5.0-py3-none-any.whl`. Rebuilt again after final correction: exit 0.
- Fresh wheel smoke in `.tmp\campaign002-wheel-smoke-postcommit`: exit 0; output `0.5.0 0.5.0 outcome-first-decision-v3 2.1 5`, with exact frozen tool order asserted.
- `git diff --check 824559afd68f170758837769b1d1d19df991db4b..HEAD`: exit 0. Final branch is ahead of `origin/main` by seven local commits, index empty, and only issued protected Harness/user assets plus this ledger/report remain outside commits.
- Final protected SHA-256 checks exactly matched issuance: plan `B7B6...F20`, features `6DC3...575`, progress `D0A5...CE3`, contract `D585...0BE`, prior review `1843...16B`, learnings `22F9...58F`/`F99E...F0A`, audit `B480...D76`, repository record `BA26...C73`, external live record `8F10...A16`.
- Live provider/Goose model calls: `0`. The issued external live record was read-only structural evidence only; no credentials or external state changes occurred.
