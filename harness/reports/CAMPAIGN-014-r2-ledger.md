# CAMPAIGN-014-r2 Main Worker Ledger

## Control

- HARNESS_ROLE: WORKER / MAIN WORKER
- HARNESS_MODE: STRICT_CAMPAIGN
- Contract: `harness/contracts/CAMPAIGN-014-r2.md`
- Contract SHA-256: `6B0A2FB0D122F3E67F12D0A4FADAD2BC17BA93A62DBC7802C748F294EC0FB404`
- Original Campaign baseline: `4f976c2764a463dceb403084fa3faead5300211e`
- Revision baseline: `742128a1dfc2282d7aad4ee016d37ff94922c9ca`
- Final HEAD: `9d23ed01f94be2ef0c724b3e0a3e7e1beba75c09`
- Executor: Codex Main Worker; no new r2 subagent assignment

## Admission

- Pigeon-harness skill, common protocol, Worker protocol, r2 contract, parent r1 contract,
  r1 Foreman review, r1 Worker report/ledger, AGENTS and required Harness state read: PASS.
- HEAD, `origin/main` governance ref `bcdb0e2bc282e907e975b43882906872913f6bec`,
  exact seven-commit chain, empty index, 21-path committed r1 diff and contract hash: PASS.
- All eight admitted unstaged PKG-087 intermediate hashes: exact match.
- All 13 r2 protected hashes, including workflow: exact match.
- Compile: PASS.
- First focused invocation used a nested basetemp before creating its parent and produced
  `1 failed, 13 passed, 20 errors`; this was a Windows test-runner setup error. After the
  allowed repository-local parent was created, the bounded identical rerun reproduced
  exactly `31 passed, 3 failed in 1.33s`, with only the contracted stale assertions.

## Bounded correction and commit

- `tests/unit/test_persistence_v2.py`: renamed the V0.13.0-specific test and changed only
  four package/build assertions for both `full` and `metadata` to V0.13.1/v11.1.
- `tests/integration/test_tool_surface_v2.py`: changed only package/module/build
  expectations to V0.13.1/v11.1.
- Focused recovery: exact `34 passed in 1.15s`.
- Pre-commit compile: PASS; full suite: `575 passed in 5.20s`.
- Staged names and complete staged diff inspected: exactly ten authorized paths,
  `31 insertions / 31 deletions`; staged `git diff --check`: PASS.
- Commit: `9d23ed01f94be2ef0c724b3e0a3e7e1beba75c09` —
  `PKG-087 release V0.13.1 audit remediation`.

## Final verification

- Compile: PASS.
- Complete regression: `575 passed in 5.09s`, zero failures/skips/deselections.
- Integrated affected matrix: `371 passed in 2.74s`.
- Golden tests: `4 passed`; direct evaluator: Schema 2.1, exact `30/30`, no failed IDs.
- Golden metrics: critical-presence, clean-case-no-cluster, contribution kind, conflict,
  user authority, chief consistency, call budget, discussion value, decision support and
  support/disposition coherence all `1.0`; insufficient false reassurance `0.0`.
- Golden runtime: 186 scripted sampling calls, 5 scripted elicitations, budget 374,
  routing/display calls 0, 30 result rows.
- Direct invariants: exact ordered five tools; package/module `0.13.1`; build
  `truthful-boundaries-council-v11.1`; schemas Review/Receipt/Evaluator `2.6/1.1/2.1`;
  defaults review_only/auto/auto/council_adjudication/summary/full; budgets 6/13/18;
  concurrency 3/3; 15 routing profiles.
- Original baseline-to-final: exactly 29 authorized paths, 1198 insertions/134 deletions.
- Revision baseline-to-final: exactly ten authorized PKG-087 paths.
- `git diff --check` original baseline-to-final: PASS.
- Static import/call-site audit: the only added production import is `ValidationError`,
  used by `deliberation.py`; no added `.sample(`, `.elicit(`, `.save(` or retry call site.
  The integrated history tests also prove one-load/zero-save retrieval and immutability.

## Lock, build and archives

- Pinned tool: `uv 0.12.3 (507230998 2026-08-07 x86_64-pc-windows-msvc)`.
- `uv lock --check`: 78 packages; `uv sync --locked --all-groups`: PASS.
- Lock SHA-256: `E7E4E44A19A3A7F1813EE3B5CFDC5814A70BF29C71CD5115582AF4E64A352E00`.
- Lock invariants: revision/package/upload-time `3/78/586`; delta only root version
  `0.13.0 -> 0.13.1` and root FastMCP specifier `>=2.13.0.2 -> >=2.13.0.2,<4`.
- Fresh wheel: `council_of_translation-0.13.1-py3-none-any.whl`, 110309 bytes,
  SHA-256 `4582ACDB48D5B6E5C008A0E9B11020B290D60C1C812A6A7F7A7328AC76F1CDB8`.
- Fresh sdist: `council_of_translation-0.13.1.tar.gz`, 103191 bytes,
  SHA-256 `41863D980E3597078CD2B808742D632C62BAA122B0CD56CA0BBA0C1D04C8EE43`.
- Archive inspection: wheel 31 entries, sdist 42 entries, correct 0.13.1 metadata,
  FastMCP `<4,>=2.13.0.2`, required package/pyproject files present, zero `.tmp` or
  Campaign cache entries.

## Installed-wheel smokes

- CPython 3.12.9 + exact FastMCP 2.13.0.2: PASS from isolated `site-packages`.
- CPython 3.12.9 + exact FastMCP 3.4.7: PASS from isolated `site-packages`.
- Each enumerated the exact five tools and called all five; each proved clean completion
  with six samples, truncation `NEEDS_HUMAN_REVIEW`/insufficient/`input_truncated`,
  malformed discussion `NEEDS_HUMAN_REVIEW`/`discussion_unavailable` with seven calls
  and no retry, and exact six-field V1 summary.
- First smoke attempts exposed two temporary harness API differences: omitted `None`
  fields on FastMCP 2 and `list_tools`/plain decorated functions on FastMCP 3. The temp
  smoke was made version-neutral and bounded reruns passed. FastMCP 2 emitted the known
  upstream Authlib deprecation warning.
- The first pair of isolated install commands exceeded the initial result window while
  the wrapper failed to retain session IDs; idempotent exact reruns established exit 0.

## Hygiene and counts

- Final protected reconciliation: all 13 r2 hashes exact; workflow exact.
- Git index: empty. Protected Foreman/user dirty and untracked assets remain unstaged.
- Resolved repository-local `.tmp/campaign014-r1-worker` and
  `.tmp/campaign014-r2-worker` were verified inside the repository and removed; `build`
  was absent. No admitted asset was removed or traversed.
- New r2 subagents: 0. Preserved r1 Campaign assignments: 3.
- Contract-scope authority expansions: 0. Sandbox authority escalations: 2, limited to
  exact `git add` and `git commit` writes.
- Dependency operations: one pinned uv acquisition, lock check, locked sync, two CPython
  3.12 venv creations and two exact-version installed-wheel environments; no unauthorized
  dependency graph change.
- Fresh distribution builds: 1. Installed-wheel smokes: 2 successful final runs.
- Live Goose/provider/model calls: 0. Remote Git/GitHub calls or mutations: 0.
- Push/PR/publication/release/deployment: 0. Skipped required checks: 0.
