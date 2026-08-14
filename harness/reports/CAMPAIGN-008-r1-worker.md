# CAMPAIGN-008-r1 Main Worker Report

## Terminal status

`READY_FOR_REVIEW`

This is a Worker handoff only. Campaign acceptance, publication, Q-012, and project completion remain Foreman authority.

## Control and admission

- HARNESS_ROLE: `WORKER / MAIN WORKER`
- HARNESS_MODE: `STRICT_CAMPAIGN`
- Contract: `harness/contracts/CAMPAIGN-008-r1.md`
- Contract SHA-256: `3D477E8418B77A621EFEBB3BD496CD0508BCC9C39A22D833EFA79886A98EE366` (matched before editing and at handoff)
- Exact baseline: `c4d2e42f5bfee377cdbebaed776272cb996c679c` (matched before editing)
- Admission index: empty
- Admission compile: passed
- Admission complete suite: `246 passed in 5.50s`
- Admission pinned tool/sync: uv `0.12.3`, lock check passed, Python 3.12 locked dev sync checked 72 packages
- Protected dirty/untracked assets admitted and left unstaged: `harness/plan.md`, `harness/features.json`, `harness/progress.md`, `.learnings/`, `reviews/`, the Campaign contract, and the audit report
- Authorized implementation boundary used: only `src/council_of_translation/**`, authorized tests/fixtures, `README.md`, `AGENTS.md`, the two authoritative docs, `pyproject.toml`, `uv.lock`, and the two current report paths

## Final Git state and commits

- Final HEAD: `6e28c103f98a6b0481ab7d103580b83f8e6c4cfa`
- Git index: empty
- Baseline-to-HEAD `git diff --check`: passed
- Baseline-to-HEAD scope audit: every changed path is authorized
- Local commits (not pushed):
  1. `5cec25348f6f2e3f86ee72dc223f7faaa5c75562` — PKG-042, V2.4 value models/compatibility/persistence and focused tests
  2. `6d03558696c310026de1c0485a092cc5a2c6e8ed` — PKG-043, deterministic role/discussion value metrics and zero-call/counterexample tests
  3. `6baa9fc6c648be638586d0f5e2abc7631a864f1c` — PKG-044, frozen five-section value-first presentation and affected tests
  4. `f68969c783b5726e382208c0253e4192847c51cc` — PKG-045, exact 18-case offline corpus and JSON-safe comparison library/tests
  5. `6e28c103f98a6b0481ab7d103580b83f8e6c4cfa` — PKG-046, V0.10/schema 2.4/build v8 migration, privacy allowlist, ordered five-tool registration, docs, lock and release tests

Changed implementation scope totals 31 paths: package/version and server/tool metadata; localization models, compatibility, persistence, orchestration, digest and new value metrics; offline evaluation library; authorized docs; focused unit/integration tests; the 18-case fixture; and the root lock version.

## Package verification

- PKG-042: focused models/persistence `31 passed in 0.37s`; complete regression `250 passed in 4.34s`.
- PKG-043: focused contribution/discussion and zero-extra-call probes `9 passed in 0.25s`; complete regression `255 passed in 4.42s`. Duplicate/rephrased same-role findings count once; rephrased discussion claims alone produce `none`; clean runtime path remained 4 routed calls/0 elicitation.
- PKG-044: focused/affected presentation probes `23 passed in 1.39s`; complete regression `258 passed in 3.70s`. Exact five headings/order, role accounting, unique-before-confirmation, minority/degradation visibility, discussion conditionality, clean <=1,200 and hard <=3,200 passed.
- PKG-045: exact corpus/aggregate probes `8 passed in 0.30s`; complete regression `261 passed in 4.42s`. All 18 audit cases are present; aggregate is JSON-safe and reports 1.0 for critical recall, false-positive-free, contribution-kind, conflict, user-authority, chief consistency, call budget, and discussion marginal-value comparisons.
- PKG-046: release/migration/tool/persistence focus `52 passed in 1.31s`; final metadata privacy focus `23 passed in 1.56s`; complete regression `263 passed in 3.61s`. Version `0.10.0`, build `evidence-value-council-v8`, schema `2.4`, exact ordered five tools, defaults, budgets 6/13/18, concurrency default/max 3/3, full/metadata writes and V1/V2.0-V2.3 reads passed.

## Integrated Campaign verification

- `python -m compileall src tests` and final `.venv\Scripts\python.exe -m compileall -q src tests`: exit 0.
- Final complete suite: `263 passed in 3.61s`.
- Final named Campaign probes: `13 passed in 1.08s`.
- Pinned lock command: repository-local `UV_CACHE_DIR`/`UV_TOOL_DIR`, `uvx --from uv==0.12.3 uv lock --refresh` -> 78 packages resolved; only editable root version changed `0.9.0 -> 0.10.0`; lock revision remains 3.
- Final `uv.lock` SHA-256: `A783C2C5E8987BBCEC5A5917BD885B3DBEFF5F1BDB7CB032D476B01C0B0B1211`.
- Fresh build with pinned uv 0.12.3:
  - wheel `council_of_translation-0.10.0-py3-none-any.whl`, SHA-256 `D46D5A9AA3E37D536CC2363477E0D9FDE149A2BD93DBE153F4D9694C04E91008`
  - sdist `council_of_translation-0.10.0.tar.gz`, SHA-256 `A26D3ADBE62C303B6064E2D38F8580BC4D9A333406068BCC52D2D864B5884EA4`
- Isolated installed-wheel smoke: Python `3.12.9`, current FastMCP `3.4.7`; called `review_translation`, `continue_review`, `view_review_record`, `list_review_records`, and `get_server_info`; exact order, `0.10.0`, build v8, schema 2.4, budgets and concurrency passed.

## Protected evidence

Final SHA-256 values equal the admission snapshot:

- `harness/plan.md`: `438CB74F084A63EE4FAA3ABE380F9BCE53C196B9DDEBE33CEDE8A4520A0AEFB4`
- `harness/features.json`: `A5E1A5030C9A307F4A3FE55682D9E5F49A6789C11D34C20F5A407084141DF984`
- `harness/progress.md`: `6EBFDC6E858969E2C1350636DF5BD7DFFB845DF7776EC7173DA661F01C6D81A6`
- Campaign contract: `3D477E8418B77A621EFEBB3BD496CD0508BCC9C39A22D833EFA79886A98EE366`
- Audit report: `B48073E063C4C9F34E0B6B4DAE94E80079EAAAD3B2F8E273DD60B2F25F6ABD76`
- `.learnings/LEARNINGS.md`: `52DC1BA8043481911C0DEABB3AC882504D9CBE8BB63D60F391C188586A230DF0A`
- `.learnings/ERRORS.md`: `F99EB75886781958BF5AE6DCF844FD476CBCA45937896A25EE3B2E9D6CD34F0A`

No protected asset was staged or committed. The final dirty/untracked protected set matches admission, with only the two authorized current report files added.

## Incidents, skipped checks and authority

- Incidents: global Windows pytest temp-root permission was avoided with repository-local `--basetemp`; two test assumptions were corrected to the frozen UI router's four active lightweight roles; FastMCP 3.4.7 wheel smoke uses `list_tools()` rather than its historical `get_tools()` helper. No product failure remains.
- The self-improvement skill was consulted for the temp-root failure, but its requested `.learnings/` write was skipped because the Campaign protects that path.
- Skipped by contract: live Goose/provider/model testing (Q-012), push, PR, release, deployment, publication and credential work.
- Subagents: `0` (forbidden).
- Live Goose/provider/model calls: `0`.
- Authority escalations: `12`, limited to scoped `git add`, `git commit`, and one commit amendment required for the five local package commits. No external-system authority was requested.
- External dependency operations: pinned uv 0.12.3 acquisition/use, locked admission sync, canonical lock refresh, and two isolated wheel installs; the second install used the repository-local cache. No provider endpoint was contacted.

## Remaining risks

- Q-012 live Goose/provider verification is intentionally unrun and remains a separate Foreman gate.
- The build backend warned that the repository-local uv cache sits under the source directory; build logs and artifact contents included only declared package files, and the build left no tracked changes.
- No Campaign acceptance or publication is asserted by this report.
