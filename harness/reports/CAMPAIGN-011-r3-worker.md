# CAMPAIGN-011-r3 Worker Report

Status: `READY_FOR_REVIEW`

This report is a Main Worker handoff. It does not claim Campaign, Q-013, publication, feature, or project acceptance.

## Control and authority

- HARNESS_ROLE: `WORKER / MAIN WORKER`
- HARNESS_MODE: `STRICT_CAMPAIGN`
- Contract: `harness/contracts/CAMPAIGN-011-r3.md`
- Contract SHA-256: `BA884359309326C179E5A42AF44D24872B960FD0D717130B59E88C534066C64A`
- Exact baseline: `938c3a4bb9f14c7688286b25eabd8aff9f18a09d`
- Final HEAD: `76921ecb69ec26f0034ec772433e102a3f7715bf`
- Packages executed in order: `PKG-063 -> PKG-064`
- Subagents: `0`; the contract did not grant delegation authority.
- Acceptance authority: Foreman only.

## Admission and protected state

Admission passed before implementation:

- HEAD matched the exact baseline.
- Contract hash matched exactly.
- Git index was empty.
- `.venv\Scripts\python.exe -m compileall src tests` exited 0.
- `.venv\Scripts\python.exe -m pytest -q --basetemp=.tmp/campaign011-r3-admission` returned `307 passed in 4.17s`.
- The admitted dirty/untracked set was exactly the Foreman plan/progress, Q-013 Harness assets, protected user directories, and audit Markdown shown by `git status --short`.
- The parent bounded live review was the only prior evaluation read, as expressly permitted by the contract. Raw Q-012 records and model prose were not read or copied.

Admission and final protected hashes are identical:

| Protected path | SHA-256 |
| --- | --- |
| `harness/plan.md` | `D9B89B1294EFE5A833F52C4916B404902EF75B285200D6703A8E6196036AA63C` |
| `harness/progress.md` | `99181103B1D7137C568F388F5DEA11D079CB762ADB7780D2EE5A65D9CA20C6E0` |
| `harness/features.json` | `E36271A359B2004A77AA0D94B13A23DF96825BF9F591B07FAD2D9873177DD7AB` |
| `harness/contracts/CAMPAIGN-011-q013-live.md` | `1119EB0392C52D0A8F4444556B8A4C402837355AF89B01B49C398D2D7CCEC613` |
| `harness/contracts/CAMPAIGN-011-r3.md` | `BA884359309326C179E5A42AF44D24872B960FD0D717130B59E88C534066C64A` |
| `harness/evaluations/CAMPAIGN-011-publication-ci-review.md` | `C98647AAF24E4CAE3EE468371B6A55F493538986A2011EA678E20801F65A3C2D` |
| `harness/evaluations/CAMPAIGN-011-q013-live-review.md` | `CA5E5098FC18B0C8C9949A6F499FA850EA581BC16EF158E566B2FAFBE4F21A7C` |
| audit Markdown | `B48073E063C4C9F34E0B6B4DAE94E80079EAAAD3B2F8E273DD60B2F25F6ABD76` |

`.tmp/q012/`, `.learnings/`, and `reviews/` were confirmed present without traversal at admission and reconciliation. They were not read, copied, staged, or modified.

## PKG-063 — terminal disposition preservation

The baseline counterexample used a legal-risk-shaped digest with more than six actions. Its structured final was `修改后可发布 / 否`, but `_primary_checklist` dropped that line and the renderer emitted the conservative `需人工复核 / 是` fallback.

Implemented behavior:

- `build_process_digest` retains at most seven bounded digest action entries and always places the canonical chief final disposition in the eighth digest slot. The complete structured chief lists remain untouched.
- `_primary_checklist` separates all canonical `最终处置：...` entries from action projection, continues to project at most six actionable work items, deduplicates the terminal entry, and appends the last canonical terminal exactly once.
- No severity inference, Case A prose, verdict override, sampling, elicitation, structured mutation, or larger six-action primary cap was introduced.

Counterexamples in the new `tests/integration/test_v25_risk_routing.py` cover:

- more than six pre-final legal-risk actions with canonical `修改后可发布 / 否`;
- a true `需人工复核 / 是` long case;
- a clean `可发布 / 否` case;
- pending plus degraded warnings without release permission;
- exactly-once and last terminal placement through the 3,200-code-point bounding path;
- byte-equivalent digest, chief, clusters and metrics plus unchanged zero-call telemetry.

Package evidence:

- New counterexamples: `4 passed in 0.17s`.
- Affected presentation/live-shaped/new suite: `21 passed in 0.22s`.
- Routing plus Golden regression: `10 passed in 0.45s`.

Commit:

- `4fce7d639934db414e640337de9daa6d9b82d948 Preserve terminal Council disposition`
- Paths:
  - `src/council_of_translation/localization/digest.py`
  - `tests/integration/test_v25_risk_routing.py`
- Diff: `170 insertions, 1 deletion`.

## PKG-064 — V0.11.1 release migration

Migrated only package/module identifiers to `0.11.1` and diagnostic build to `risk-coherent-council-v9.1`. Schema remains `2.5`.

Canonical lock workflow used repository-local `UV_CACHE_DIR`/`UV_TOOL_DIR` and exact uv 0.12.3:

- `uv tool run --from uv==0.12.3 uv --version` -> `uv 0.12.3 (507230998 2026-08-07 x86_64-pc-windows-msvc)`.
- `uv tool run --from uv==0.12.3 uv lock --refresh` -> resolved 78 packages; root updated `0.11.0 -> 0.11.1`.
- Both required/final `uv ... lock --check` runs resolved 78 packages and exited 0.
- Final lock SHA-256: `427A96BA85ECE8A64DBC173676E1424460DF4329B956DE535AFEA35EC8D575AE`.
- Lock invariants: revision 3, 78 packages, 586 `upload-time` entries.
- Baseline lock diff is exactly the editable root version line. No dependency, source, hash, edge, metadata, or format drift exists.

Package evidence:

- Release/persistence/tool surface suite: `38 passed in 1.19s`.
- Affected presentation/routing/Golden suite: `31 passed in 0.51s`.
- Compile: exit 0.

Commit:

- `76921ecb69ec26f0034ec772433e102a3f7715bf Release risk-coherent Council 0.11.1`
- Paths:
  - `AGENTS.md`
  - `README.md`
  - `docs/v0.4-tool-contract.md`
  - `pyproject.toml`
  - `src/council_of_translation/__init__.py`
  - `tests/integration/test_tool_surface_v2.py`
  - `tests/integration/test_v10_release_contract.py`
  - `tests/unit/test_persistence_v2.py`
  - `uv.lock`
- Diff: `24 insertions, 24 deletions`.

## Final integrated verification

- Final compile: `.venv\Scripts\python.exe -m compileall src tests` -> exit 0.
- Final complete suite: `.venv\Scripts\python.exe -m pytest -q --basetemp=.tmp/campaign011-r3-final-full` -> `311 passed in 3.81s`.
- Exact Golden probe: `24/24`, no failed case IDs.
- Golden metrics, all `1.0`: critical issue recall, false-positive-free rate, contribution-kind accuracy, conflict detection accuracy, user authority accuracy, chief consistency rate, call-budget accuracy, discussion marginal-value accuracy.
- Golden runtime: 148 sampling calls, 4 elicitation calls, aggregate budget 296, zero routing calls and zero display calls.
- Frozen runtime probe: exact five tools; package/module `0.11.1`; build `risk-coherent-council-v9.1`; schema `2.5`; defaults `review_only/auto/auto/summary/full/council_adjudication`; budgets `6/13/18`; concurrency limit/max `3`.
- Long-list source-tree probe: canonical modified-publishable terminal appeared exactly once as the final report line; report length 209.
- `git diff --check 938c3a4bb9f14c7688286b25eabd8aff9f18a09d..HEAD` -> exit 0.
- Standard-library AST dead-import scan: zero unused imports in `digest.py` and the new test.
- Git index: empty.
- Exactly two commits since baseline.
- Baseline-to-final diff: 11 authorized paths, `194 insertions, 25 deletions`.

Exact baseline-to-final paths:

1. `AGENTS.md`
2. `README.md`
3. `docs/v0.4-tool-contract.md`
4. `pyproject.toml`
5. `src/council_of_translation/__init__.py`
6. `src/council_of_translation/localization/digest.py`
7. `tests/integration/test_tool_surface_v2.py`
8. `tests/integration/test_v10_release_contract.py`
9. `tests/integration/test_v25_risk_routing.py`
10. `tests/unit/test_persistence_v2.py`
11. `uv.lock`

## Fresh build and archive inspection

Build command:

`uv tool run --from uv==0.12.3 uv build --sdist --wheel --out-dir .tmp/campaign011-r3-dist-76921ec`

Results:

- `council_of_translation-0.11.1.tar.gz`: 88,924 bytes; SHA-256 `1A40B9756DAD06F4F9EBE5D6F6ECC919BC5B7953E8F924F8B1D94FF5856F5E54`.
- `council_of_translation-0.11.1-py3-none-any.whl`: 94,925 bytes; SHA-256 `B7929DDE8CA05E91D9D618C3FB99D8E3250923041136C0AE7D3293A5EF4E1713`.
- sdist: 40 entries; wheel: 29 entries.
- Both archives prove version `0.11.1`, build `risk-coherent-council-v9.1`, schema `2.5`, and the terminal-disposition source fix.
- Tests are not packaged by the project; this was explicitly verified. No `.tmp` content entered either archive despite uv's source-local-cache warning.

## Isolated wheel-origin FastMCP smoke

- Fresh environment: `.tmp/campaign011-r3-wheel-smoke-76921ec`.
- Runtime: Python `3.12.9`, FastMCP `3.4.7`.
- Import origin: isolated `Lib/site-packages/council_of_translation/__init__.py`, not the repository source tree.
- Fresh wheel installed successfully with pinned uv 0.12.3.
- Called all five tools through the in-process FastMCP Client: `review_translation`, `continue_review`, `view_review_record`, `list_review_records`, `get_server_info`.
- Review, continuation and view returned both primary text and structured content.
- The long checklist's structured chief remained `修改后可发布 / 否`; each structured `display_report` contained the same canonical terminal exactly once and as its last line.
- The existing permitted review-ID footer followed the report in FastMCP primary content; it did not alter `display_report` or chief coherence.
- Installed diagnostics verified version/build/schema, exact tools, defaults, budgets and concurrency.
- Model/orchestration functions were replaced in memory with bounded local records, so this smoke made zero live model/provider calls.

## Deviations, skipped checks, operations, and risks

- The first new-test run exposed the pre-existing eight-entry `ProcessDigestV2` bound. The correction stayed in the authorized direct caller: seven bounded digest actions plus one canonical final. The structured chief remains complete and unchanged.
- Ruff was not installed, and `.venv` also lacked pyflakes. No dependency was added; a bounded standard-library AST scan passed. The failed pyflakes command is recorded here because `.learnings/**` is protected and was not read or written.
- The first isolated smoke assertion treated the permitted review-ID footer as part of `display_report`. The corrected smoke separately verified the report terminal and footer and passed.
- uv warned that the repository-local cache was below the source directory. Archive inspection proved `.tmp` was excluded.
- Required checks skipped: none.
- Prohibited/not performed: live Goose/provider/model calls, raw record inspection, push, PR creation/update, publication, release, deployment, credential work and Goose/configuration changes.
- Subagents: `0`.
- Sandbox authority escalation requests: `4`, all approved and limited to two exact staging operations and two exact commits.
- Pinned uv/dependency operations: `7` (`--version`, refresh, two checks, build, isolated venv, isolated install).
- Live call count: `0`; remote/external state mutations: `0`.
- Remaining risk: contract prohibited post-fix normal-Goose Q-013 validation. Local production, Golden, packaging and FastMCP evidence is complete, but Foreman/user live revalidation remains a separate gate.

## Final Git state and Foreman handoff

- Final HEAD: `76921ecb69ec26f0034ec772433e102a3f7715bf`.
- Index: empty.
- Pre-existing protected plan/progress modifications and protected untracked assets remain in place.
- `harness/reports/CAMPAIGN-011-r3-ledger.md` and this report are untracked and unstaged.

Foreman should independently inspect the two commits and baseline-to-final diff, rerun the contract checks, verify both reports remain untracked/unstaged, and decide `ACCEPTED`, `CHANGES_REQUESTED`, or `BLOCKED` for CAMPAIGN-011-r3.
