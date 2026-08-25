# CAMPAIGN-014-r1 Main Worker Ledger

## Control

- HARNESS_ROLE: WORKER / MAIN WORKER
- HARNESS_MODE: STRICT_CAMPAIGN
- Contract: `harness/contracts/CAMPAIGN-014-r1.md`
- Contract SHA-256: `4FBCF691DF9702587EC6A5D2F5FB1215D4440D3A6229ACBA1D4A969C7F09B2A0`
- Local implementation baseline: `4f976c2764a463dceb403084fa3faead5300211e`
- Equivalent published product tree: `95d90cf383d045778ce61afaa50dbcec199579ce`
- Admitted local governance ref: `bcdb0e2bc282e907e975b43882906872913f6bec`
- Executor: Codex Main Worker

## Admission

- Complete pigeon-harness skill/common/Worker protocol and 603-line contract read: PASS.
- Relevant AGENTS, plan/progress/features state and the two authoritative Campaign-014 design evaluations read as repository truth.
- HEAD, origin/main governance ref, empty index, published-product-tree equivalence, contract hash, protected hashes and workflow hash: PASS.
- Admitted dirty/untracked state recorded and preserved; forbidden user directories were not traversed.
- `.venv\Scripts\python.exe -m compileall -q src tests`: PASS.
- `.venv\Scripts\python.exe -m pytest -q --basetemp .tmp/campaign014-r1-worker/admission`: exact `480 passed in 4.67s`.

## Package graph

| Package | Executor | State | Files/commit | Verification/deviations |
| --- | --- | --- | --- | --- |
| PKG-080 | Main Worker | committed | `ed1f1ec54b730f6a2bf44e73214d36c1e4ec55c8`; `review.py`, `orchestration.py`, `digest.py`, new input-completeness integration test | truncation focused 7 passed; affected matrix 194 passed. First combined patch failed atomically on context mismatch; first focused run was 1 failed/6 passed because the numeric fixture lacked a word boundary, then fixture correction passed. |
| PKG-081 | bounded implementation subagent + Main integration | committed | `2cad51702a77545a4e78419aac99142541f63261`; `preflight.py`, `test_preflight_v2.py` | Main focused matrix 76 passed. Subagent first had one extraneous `{URL}` wrapper expectation and one PowerShell `$s` probe expansion; corrected bounded reruns passed. |
| PKG-082 | Main Worker; read-only subagent analysis | committed | `651d97f0d6ad8ce750f96a6a6c51ecbded29193a`; `deliberation.py`, `orchestration.py`, two unit tests, new discussion integration test | 45 focused passed; 71 affected passed. One combined patch failed atomically on a whitespace/context mismatch. First sandboxed Git write failed on `.git/index.lock`; approved local Git-write rerun committed exactly five paths. |
| PKG-083 | Main Worker; read-only subagent analysis | committed | `0208badaeaab3f2eec05bd73f8bd8f404015d7dd`; `deliberation.py`, `value_metrics.py`, discussion/value tests | 103 focused/affected passed. Production convergence, genuine split, retained Policy-valid DecisionPoint, once-per-role change and coherent digest/minority/support assertions passed. |
| PKG-084 | Main Worker; read-only subagent analysis | committed | `a523283efa5604dd49331118e941d68a7b851445`; `review.py`, new history-minimization integration test | System-Python command failed at collection because FastMCP was absent; project-venv first run was 31 passed/1 failed due test key typo `receipt_schema`; corrected rerun 32 passed. |
| PKG-085 | Main Worker | committed | `5ba1db58ba0075d5f3eff7e3d96ab6ef77b949e9`; evaluator, Golden fixture/tests, blind schema, remediation doc | 13 focused passed; direct evaluator result `2.1 30/30`, both renamed aggregate metrics 1.0, 186 samples/5 elicitations. A first bulk rewrite one-liner failed with a quoting syntax error before writing; an apply-patch-created bounded temp script performed the exact migration and was deleted. |
| PKG-086 | Main Worker | committed | `742128a1dfc2282d7aad4ee016d37ff94922c9ca`; `pyproject.toml`, release test, remediation doc | 3 focused passed; `uv.lock` byte-unchanged in this package. |
| PKG-087 | Main Worker | BLOCKED, uncommitted intermediate | authorized edits in `__init__.py`, `pyproject.toml`, `uv.lock`, `AGENTS.md`, `README.md`, architecture/tool docs, release test | Pinned uv 0.12.3 lock refresh succeeded with exact root version/specifier-only diff and 3/78/586 invariants; locked sync succeeded. Compile passed, but complete suite was `572 passed, 3 failed in 6.05s`. Two failures require changing forbidden `tests/unit/test_persistence_v2.py`; contract stop condition invoked. No PKG-087 commit/build/wheel smoke. |

## Pre-change reproductions

- AUD-001: 12,001-character source/candidate inputs were sampled as apparently complete and could return `COMPLETED` / `可发布`; reviewed length included a synthetic marker.
- AUD-002: ordinary percentage prose generated printf blockers and URL sentence punctuation generated URL blockers.
- AUD-003: malformed discussion containers either escaped as exceptions or became completed empty rounds; mixed valid/invalid turns partially applied, with no truthful discussion degradation.
- AUD-004: final positions converged to one option while cluster/digest/minority/support remained disputed; metrics simultaneously claimed resolution.
- AUD-005: V1 summary equaled the full legacy dump and exposed hostile task/reviewer/chief prose.

## Blocker evidence

- Final compile command: `.venv\Scripts\python.exe -m compileall -q src tests` — PASS.
- Final attempted full suite: `.venv\Scripts\python.exe -m pytest -q --basetemp .tmp/campaign014-r1-worker/pkg087-full -p no:cacheprovider` — FAIL, `3 failed, 572 passed in 6.05s`.
- Authorized failure: `tests/integration/test_tool_surface_v2.py::test_server_info_and_versioned_defaults` retains 0.13.0 and may be corrected inside the allowlist.
- Forbidden-path failures: both parameterizations of `tests/unit/test_persistence_v2.py::test_new_write_persists_truthful_v0130_runtime_and_version_identifiers` retain 0.13.0 / `calibrated-evidence-council-v11`. `tests/unit/test_persistence_v2.py` is absent from the exact authorized test list.
- Stop condition: a required full-regression correction needs a forbidden path. No conditional production behavior, test bypass, or partial PKG-087 commit was attempted.
- Current HEAD: `742128a1dfc2282d7aad4ee016d37ff94922c9ca`; index empty; authorized PKG-087 work remains unstaged.
- Current lock SHA-256: `E7E4E44A19A3A7F1813EE3B5CFDC5814A70BF29C71CD5115582AF4E64A352E00`; diff is only root `0.13.0 -> 0.13.1` and FastMCP specifier `>=2.13.0.2 -> >=2.13.0.2,<4`.

## Counts

- Subagent assignments: 3 authorized bounded assignments.
  - `receipt_shape_analysis` / Averroes: bounded PKG-081 implementation in `preflight.py` and `test_preflight_v2.py`; no staging/commit.
  - `release_test_analysis` / Volta: read-only AUD-003/AUD-004 and PKG-082/083 analysis; no edits/staging/commit.
  - `tool_surface_analysis` / Einstein: read-only AUD-005 and PKG-084 analysis; no edits/staging/commit.
- Contract-scope authority expansions: 0. Local Git-write sandbox approvals: 7 successful; one initial unapproved sandbox write failed harmlessly.
- Dependency operations: pinned uv 0.12.3 acquisition (two invocations because the first download exceeded the initial yield), one lock refresh and one locked sync.
- Builds: one editable locked-sync build; fresh wheel/sdist builds skipped after blocker.
- Live Goose/provider/model calls: 0.
- Remote mutations: 0.
- Push/PR/publication/release/deployment operations: 0.
