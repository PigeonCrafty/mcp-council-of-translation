# CAMPAIGN-008-r1 Main Worker Ledger

## Control

- Role/mode: `WORKER / MAIN WORKER`, `STRICT_CAMPAIGN`
- Contract: `harness/contracts/CAMPAIGN-008-r1.md`
- Contract SHA-256: `3D477E8418B77A621EFEBB3BD496CD0508BCC9C39A22D833EFA79886A98EE366`
- Baseline: `c4d2e42f5bfee377cdbebaed776272cb996c679c`
- Package order: PKG-042 -> PKG-043 -> PKG-044 -> PKG-045 -> PKG-046
- Subagents: forbidden / 0
- Acceptance authority: Foreman only

## Admission

- Exact HEAD/subject and empty index: passed.
- Declared Foreman/user dirty set recorded and protected.
- Protected baseline SHA-256 snapshot recorded in the Worker report evidence set.
- Pinned uv 0.12.3 lock check and Python 3.12 locked dev sync: passed.
- Baseline compile: passed.
- Baseline complete suite: `246 passed in 5.50s`.

## Package state

| Package | State | Files/commit | Verification |
| --- | --- | --- | --- |
| PKG-042 | COMPLETE | `5cec253`; `models.py`, `compatibility.py`, `persistence.py`, `test_v24_models_persistence.py` | Focused `31 passed`; complete suite `250 passed`; `git diff --check` passed |
| PKG-043 | COMPLETE | `6d03558`; `value_metrics.py`, `orchestration.py`, two focused test files | Focused `9 passed`; complete suite `255 passed` |
| PKG-044 | COMPLETE | `6baa9fc`; `digest.py`, `orchestration.py`, focused/affected presentation tests | Focused `23 passed`; complete suite `258 passed`; clean target and hard cap passed |
| PKG-045 | COMPLETE | `f68969c`; `evaluation.py`, exact 18-case JSON corpus, aggregate regression tests | Focused `8 passed`; exact 18 cases; JSON-safe aggregate all metrics `1.0`; complete suite `261 passed` |
| PKG-046 | COMPLETE | `6e28c10`; version/schema/build, metadata role-ID allowlist, five-tool registration order, docs, tests, `uv.lock` | Pinned uv `0.12.3` refresh changed only root `0.9.0 -> 0.10.0`; focused `52 passed`, privacy rerun `23 passed`; complete suite `263 passed` |

## Integrated verification

- Final HEAD: `6e28c103f98a6b0481ab7d103580b83f8e6c4cfa`; five scoped package commits; index empty.
- Compile: `.venv\Scripts\python.exe -m compileall -q src tests` -> exit 0.
- Complete regression after final privacy correction: `263 passed in 3.61s`.
- Final named Campaign probes: `13 passed in 1.08s`; exact 18 golden cases and JSON-safe aggregate passed.
- Fresh artifacts: wheel SHA-256 `D46D5A9AA3E37D536CC2363477E0D9FDE149A2BD93DBE153F4D9694C04E91008`; sdist SHA-256 `A26D3ADBE62C303B6064E2D38F8580BC4D9A333406068BCC52D2D864B5884EA4`.
- Isolated wheel smoke: Python `3.12.9`, FastMCP `3.4.7`, exact ordered five tools called, version `0.10.0`, build `evidence-value-council-v8`, schema `2.4`.
- `uv.lock` SHA-256 `A783C2C5E8987BBCEC5A5917BD885B3DBEFF5F1BDB7CB032D476B01C0B0B1211`; baseline diff is only editable root version `0.9.0 -> 0.10.0`; revision remains 3.
- Baseline-to-HEAD scope and `git diff --check`: passed; all paths authorized.
- Protected SHA-256 values match admission; protected dirty/untracked set remains present and unstaged.
- Subagents: 0. Live Goose/provider/model calls: 0. Push/PR/release/deploy: 0.

## Incidents and deviations

- First PKG-042 focused run hit a pre-existing Windows permission error in the global pytest temp root. No product test failed; the unchanged command rerun with repository-local `--basetemp` passed. The self-improvement skill was consulted, but its `.learnings/` logging action was suppressed because the contract protects that path.
- PKG-043's first two focused assertions assumed all six lightweight roles were routed for UI; the frozen router correctly selected four. Assertions were corrected to the actual active-role plan, with no production behavior change.
- PKG-046's first release-focused assertion exposed the pre-existing FastMCP registration order (`get_server_info` first). Registration was moved without changing any tool signature or implementation so the actual order matches the frozen five-tool order; the focused rerun passed.
- First isolated current-FastMCP smoke used the historical `get_tools()` helper, which FastMCP 3.4.7 replaced with `list_tools()`. The installed wheel and dependency installation were healthy; the smoke harness was corrected and all five tool calls passed. A second fresh artifact build/isolated install after the final metadata allowlist correction also passed.
