# CAMPAIGN-001-r1 Execution Ledger

## Control and authority

- Role: `WORKER / MAIN WORKER`
- Mode: `STRICT_CAMPAIGN`
- Contract: `harness/contracts/CAMPAIGN-001-r1.md`
- Baseline: `34d41946717f1993b8954260afc893737198a3bb`
- Final HEAD: `8a2531e91a42a1523e83d374b84553907a5e3e94`
- Acceptance authority: Foreman only; no feature was marked complete or accepted.
- Subagents: 4 bounded assignments; 3 disjoint implementers and 1 read-only PKG-010 documentation reader.
- Escalated tool calls: 22 (uv cache/locked-environment operations and scoped Git staging/commits only).
- External dependency/network operations: two `uvx --from uv@latest` invocations during lock recovery. Frozen uv runs used the locked/cache environment. No application service or model call succeeded.
- Live Goose workflows: 0.

## Baseline and protected state

Observed branch was `main`; both `HEAD` and `origin/main` were the baseline commit. Baseline dirty state consisted only of protected untracked `.learnings/`, `harness/`, the audit Markdown, and `reviews/`; `myTest/` was absent. The final status is `main...origin/main [ahead 5]` with the same protected untracked roots plus the two authorized report files inside `harness/reports/`.

Protected hashes were unchanged at final inspection:

| Path | SHA-256 / state |
| --- | --- |
| `.learnings/LEARNINGS.md` | `ACB976291B8937E5B0AEB8F953C85706FDBB3DD83E26C7E4E7D64D3E4253C0E0` |
| `harness/contracts/CAMPAIGN-001-r1.md` | `4496301B81901040C82FACA7386D4AA2930FFBEE2A5322329AC940C4B3505DEE` |
| `harness/features.json` | `968D658FBB3BA80E68AF8E6E514222B5FDE74E6F4E6708B488FC3804A248F189` |
| `harness/plan.md` | `0E5707BB5D53DBAC3E9A5D81307AC03EA807DA516E941B2C0F26611BA4B80D35` |
| `harness/progress.md` | `896D02F56205BA183476FC2D2D1A98ED4E638F99765C4D7293DAF73CDC090F6D` |
| audit Markdown | `B48073E063C4C9F34E0B6B4DAE94E80079EAAAD3B2F8E273DD60B2F25F6ABD76` |
| `reviews/20260810_145151.json` | `BA2607DEAF9BA440C514FB3D6E5AB34197EDEFA7CC04D9F83859A6EDE4E8FC73` |
| `myTest/` | absent |

## Package and delegation ledger

| Package | Owner | Files/outcome | Verification evidence | Result |
| --- | --- | --- | --- | --- |
| PKG-001 | Main Worker | `models.py`, `compatibility.py`, direct Pydantic metadata | focused models `7 passed`; final models+persistence `17 passed` | Main Worker verified |
| PKG-002 | `pkg_002_persistence`; Main Worker inspected/integrated | `persistence.py`, `test_persistence_v2.py` | subagent `10 passed`; final combined `17 passed` | Main Worker verified |
| PKG-003 | `pkg_003_roles`; Main Worker inspected/integrated | executable roles/plan and tests | subagent `10 passed`; final roles+runtime `15 passed` | Main Worker verified |
| PKG-004 | `pkg_004_runtime`; Main Worker inspected/integrated | runtime protocols, FastMCP adapters, scripted doubles, telemetry | subagent `5 passed`; final roles+runtime `15 passed`; real FastMCP signatures/tool use exercised | Main Worker verified |
| PKG-005 | Main Worker | deterministic preflight and tests | final core group included all preflight tests; `33 passed` | Main Worker verified |
| PKG-006 | Main Worker | general issue normalization/clustering | final core group `33 passed`; no named-case references | Main Worker verified |
| PKG-007 | Main Worker | bounded discussion, budgets, Position Matrix | final core group `33 passed`; 6/10/14 and one-round/participant limits asserted | Main Worker verified |
| PKG-008 | Main Worker | Policy Gate, chief decision, orchestration, compact/full trace | mocked interactive record: 9 samples, 1 elicitation; compact/full evidence captured | Main Worker verified |
| PKG-009 | Main Worker | default interaction, fallback/pending, continuation/reconsideration | fallback 7/0; clean 6/0; continuation 2 affected-role calls; immutable parent asserted | Main Worker verified |
| PKG-010 | Main Worker; `pkg_010_docs_reader` read-only | exact tools, migration/deletion, docs, security tests, final validation | locked full `71 passed`; focused tool surface `4 passed`; build and dead-reference scan passed | Main Worker verified; no acceptance claim |

Subagent boundaries/results:

- `pkg_002_persistence`: only persistence production/test files; no commit; reported one temp-root permission incident, rerun passed with injected basetemp.
- `pkg_003_roles`: only role production/test files; no commit.
- `pkg_004_runtime`: only runtime production/test files; no commit; kept Core independent of FastMCP imports.
- `pkg_010_docs_reader`: read-only comparison of docs/tool/runtime/frozen contract. It found pending-history, deterministic-hard-rule, full-trace wording, enum clarity, and maximum-budget issues. Main Worker corrected code/docs and reran tests. No files were edited by this subagent.

## Commits

| Commit | Scope |
| --- | --- |
| `f2ecb47` | Add structured deliberation domain models |
| `1dc2d4e` | Build deliberation foundations |
| `23e9869` | Complete structured review workflow and legacy migration |
| `8a65721` | Document the V0.4 review contract |
| `8a2531e` | Normalize three source endings found by final diff check |

No push, PR, release, deployment, or external mutation was performed.

## Verification commands and exact results

| Phase | Exact command | Exit/result |
| --- | --- | --- |
| Baseline | `python -m compileall src tests` | 0; passed |
| Baseline | `$env:PYTHONPATH='src'; python -m pytest -q` | 0; `21 passed in 0.05s` |
| PKG-001 | `$env:PYTHONPATH='src'; python -m pytest -q tests/unit/test_models_v2.py` | 0; `7 passed` |
| Foundations | focused persistence, roles, runtime, preflight, clustering, deliberation commands | 0; package results shown above |
| Intermediate integration | `$env:PYTHONPATH='src'; python -m pytest -q --basetemp .tmp/campaign001-mainworker-pytest` | 0; `79 passed` before legacy-test replacement |
| Reader fix first pass | focused preflight/deliberation/orchestration pytest command | 1; `27 passed, 1 failed` because the test fixture omitted `category=language_choice` after the new eligibility gate |
| Reader fix rerun | same focused command with fresh workspace basetemp | 0; `28 passed` |
| Final required compile | `python -m compileall src tests` | 0; all source/test trees listed without errors |
| Final required pytest, literal contract command | `$env:PYTHONPATH='src'; python -m pytest -q` | 1; `53 passed, 1 skipped, 14 errors`, all fixture setup errors from host `pytest-of-GeZhu` `PermissionError` |
| Final direct rerun | `$env:PYTHONPATH='src'; python -m pytest -q --basetemp .tmp\campaign001-final-direct` | 0; `67 passed, 1 skipped in 0.31s`; skip is FastMCP absent from system Python |
| Final locked suite | `uv run --frozen python -m pytest -q --basetemp .tmp\campaign001-final-locked` | 0; `71 passed, 1 warning in 1.09s` |
| Models/persistence | `$env:PYTHONPATH='src'; python -m pytest -q tests\unit\test_models_v2.py tests\unit\test_persistence_v2.py --basetemp .tmp\campaign001-final-model-persistence` | 0; `17 passed` |
| Roles/runtime | `$env:PYTHONPATH='src'; python -m pytest -q tests\unit\test_roles_v2.py tests\unit\test_runtime_v2.py --basetemp .tmp\campaign001-final-roles-runtime` | 0; `15 passed` |
| Core/integration | `$env:PYTHONPATH='src'; python -m pytest -q tests\unit\test_preflight_v2.py tests\unit\test_clustering_v2.py tests\unit\test_deliberation_policy_v2.py tests\integration\test_orchestration_v2.py --basetemp .tmp\campaign001-final-core` | 0; `33 passed` |
| Tool surface | `uv run --frozen python -m pytest -q tests\integration\test_tool_surface_v2.py --basetemp .tmp\campaign001-final-tool-surface` | 0; `4 passed, 1 warning` |
| Metadata/tools | locked `python -c` importing distribution/module/server and awaiting `mcp.get_tools()` | 0; distribution/module `0.4.0`, build `structured-deliberation-v2`, exact five tools |
| Build | `uv build --out-dir .tmp\campaign001-build` | 0; built `council_of_translation-0.4.0.tar.gz` and `council_of_translation-0.4.0-py3-none-any.whl` |
| Dead references | `rg` scan for deleted workflow/schema/debate/voting/history/results/member/state imports | 0 normalized result; `NO_DEAD_REFERENCES` |
| Final diff | `git diff 34d4194..HEAD --check` | 0 after whitespace commit |
| Protected files | `Get-FileHash ... -Algorithm SHA256` | 0; all hashes identical to baseline |
| Goose capability | `goose --version` / `goose run --help` | 0; Goose `1.45.0`, stdio extension and run options present |
| Goose provider | `goose info --check` | 1 before model invocation; configured provider missing `DEEPSEEK_API_KEY`; also log-directory permission warning |

The locked pytest warnings were only `PytestCacheWarning` for the pre-existing inaccessible repository `.pytest_cache`; tests themselves all passed.

## Representative integration evidence

The sanitized mocked standard/UI workflow persisted record `20260811T102352400105Z_f35791d30a7c` with status `COMPLETED`, 9/10 samples, one accepted elicitation, one material disagreement, no must-fix items, and a traceable valid user decision. The compact projection omitted independent reviews and discussion turns. Loading the corresponding full record exposed all required sections: task/diagnostics/runtime/plan/preflight/independent reviews/clusters/discussion/DecisionPoints/user decisions/reconsiderations/Policy Gate/chief decision/DecisionTrace/version metadata. No hidden reasoning field appeared.

## Incidents, deviations, skipped checks, and risks

- `uv lock` initially failed because the sandbox could not access the user uv cache. Authorized retry with local uv 0.6.13 downgraded lock format; a current uv check was run, then Main Worker reconstructed the baseline revision-3 lock and retained only intentional V0.4 dependency/version lines. Final frozen tests/build passed.
- Default pytest temp-root discovery is inaccessible on this host. Every Campaign suite was rerun with a fresh workspace `--basetemp`; the literal required command and error are retained above.
- `.learnings/` was not updated for these incidents because the Campaign protects it; this ledger is the authorized record.
- Live Goose interactive acceptance and unsupported/decline fallback workflows were skipped: `goose info --check` proved the configured provider lacks `DEEPSEEK_API_KEY`. No credential/configuration change was authorized, and no provider/model call occurred.
- Goose Desktop GUI was not launched; real FastMCP registration/signatures and scripted interactive/fallback paths were verified instead.
- Tests inject storage roots; production default storage was intentionally not written. Non-Windows default-directory branches remain unexercised locally.
- Free-form TB/SG/project text remains authoritative reviewer context but cannot become a deterministic blocker by model assertion. Machine-enforced caller constraints are documented as `numeric_parity`, `markdown_parity`, `required_literal:<text>`, and `forbidden_literal:<text>`.

## Final repository state

- `HEAD`: `8a2531e91a42a1523e83d374b84553907a5e3e94`
- `origin/main`: `34d41946717f1993b8954260afc893737198a3bb`
- Ahead by five local commits; no staged or unstaged tracked changes.
- Baseline-to-final: 45 files changed, 3994 insertions, 4463 deletions.
- Dirty paths are protected untracked roots and the two authorized Harness reports only.
