# CAMPAIGN-004-r1 Main Worker Report

## Terminal disposition

`READY_FOR_REVIEW`

This is a Worker handoff only. It does not claim Campaign acceptance or project
completion.

## Authority and admission

- HARNESS_ROLE: WORKER / MAIN WORKER
- HARNESS_MODE: STRICT_CAMPAIGN
- Contract: `harness/contracts/CAMPAIGN-004-r1.md`
- Contract SHA-256:
  `8A77DDCEB46339632D12603D5AA62CA1C5E39FEED8A1B250161DEA2A0E8B7C03`
- Exact baseline: `b601cf93f452a8e574e3c15a4a9c236cf8142ce1`
  (`Archive V0.6 Campaign acceptance`)
- Admission: exact HEAD and contract hash, empty index, fourteen protected hashes exact,
  expected protected dirty/untracked inventory only, compile pass, and exactly
  `184 passed in 2.02s`.
- Final HEAD: `ff0e345ff174f1f39741bbb47979aa51e277ca52`.

## Commits and implementation scope

1. `eda3dee7e0b2b597153c7f64f07a6b2b5899561c` — Add dual-channel Council tool results
2. `1bbe03eda0c324bf26e41149e0d8eca5ac6fabbd` — Render concise adaptive Council reports
3. `150408d6ab78670e6b5cf0f44d8fb2928aa36656` — Synthesize truthful Council consensus
4. `d47ddd90d11560669153907775db95804753cab4` — Harden concise Council presentation
5. `ff0e345ff174f1f39741bbb47979aa51e277ca52` — Release concise Council display contract

Baseline-to-final changed exactly 19 authorized files:

- Production: `presentation.py`, `server.py`, `tools/review.py`, `digest.py`,
  `orchestration.py`, `models.py`, and `__init__.py`.
- Tests: `test_v07_dual_channel.py`, `test_v07_consensus.py`,
  `test_v07_integrity.py`, `test_v07_report.py`, plus bounded migrations in
  `test_v22_digest.py` and `test_tool_surface_v2.py`.
- Package/docs: `pyproject.toml`, `uv.lock`, `README.md`, `AGENTS.md`, architecture and
  tool-contract docs.

No forbidden production module, prior Harness artifact, `.learnings/**`, `reviews/**`,
audit Markdown or user asset was edited, staged, deleted, moved or committed.

## Package and observable-result matrix

| Package | Result | Focused evidence | Commit |
| --- | --- | --- | --- |
| PKG-023 | Three human-facing tools return first text content plus unchanged structured dictionary; safe errors use the same shape; exactly five tools retained | 10 passed; actual FastMCP Client calls | `eda3dee` |
| PKG-024 | Adaptive Chinese report with four clean sections or conditional fifth interaction section; verdict last; 1,800/3,200 bounds | 9 passed; full 190 | `1bbe03e` |
| PKG-025 | Six distinct concise lenses and full-coverage positive consensus; partial coverage remains conservative; no vote/adjudication effect | 8 passed; full 192 | `150408d` |
| PKG-026 | Tone/focus sentinel round-trip, layered retrieval, privacy, blocker/minority/pending/degraded visibility, internal-ID redaction and zero added samples | 54 passed; full 196 | `d47ddd9` |
| PKG-027 | Version 0.7.0, build `concise-council-display-v5`, docs, fresh artifacts and dual-FastMCP wheel validation | 22 passed; final full 196 | `ff0e345` |

Schema remains 2.2, public surface remains five tools, default remains review-only, and
sampling budgets remain 6/13/18.

## Primary/structured and report evidence

The exact Core/tool printed probe produced:

- Primary preview began `## 审校背景`; length 779 Unicode code points.
- Structured keys: `blind_spots`, `chief_editor`, `consensus`, `degraded`,
  `deliberation_summary`, `display_report`, `effective_task`, `fallback_reason`,
  `material_disagreements`, `parent_review_id`, `process_digest`, `retrieval_hint`,
  `review_id`, `runtime_metadata`, `schema_version`, `status`, `user_decisions`,
  `warnings`.
- Heading order: 审校背景 -> 专业视角 -> 共识、分歧与盲区 -> 主编结论.
- Six labels appeared exactly once with no internal role IDs: 技术与占位符审校员、
  忠实度审校员、术语与一致性管理员、产品语境审校员、用户体验文案审校员、
  自然度润色员.
- Positive consensus: all professional perspectives supported retaining `继续`.
- Sampling remained 6 before and after presentation; full reload retained six findings.

Fixture evidence:

- Clean report: 779 <=1,800, four sections, disposition last.
- Disputed/degraded/pending report: length 380, five sections; blocker, minority view,
  decisive condition, context gap, delegation, reconsideration, degradation and pending
  status visible; Policy Gate/internal option/role identifiers hidden; disposition last.
- Hostile long-prose report: length 1,069 <=3,200; degradation visible and disposition
  last. A separate oversized dual-channel payload test enforces the absolute 3,200 cap
  while retaining full structured evidence.
- Unique `TONE_SENTINEL` and `FOCUS_SENTINEL` values passed schema title, accepted-form,
  effective brief, all six reviewer prompts and persisted full-record checks without
  transposition.

## Verification

- Admission compile: pass.
- Admission full suite: `184 passed in 2.02s`.
- PKG focused/full progression: 10/187, 9/190, 8/192, 54/196, 22/196 passed.
- Final `python -m compileall -q src tests`: pass.
- Final full command:
  `.venv\Scripts\python.exe -m pytest -q --basetemp .tmp\campaign004-r1-full -p no:cacheprovider`
  -> `196 passed in 2.12s`.
- `git diff --check b601cf93f452a8e574e3c15a4a9c236cf8142ce1..HEAD`: pass.
- Baseline-to-final audit: 19 files, zero unauthorized paths.
- Changed-production AST unused-import scan: pass. (`ruff` unavailable, so no ruff
  invocation was claimed.)
- Tool registration scan: exactly five `@mcp.tool` decorators; tool-surface tests pass.
- Obsolete identifier scan: active authorized source/tests/docs/package metadata clean.
  Four V0.6 literals remain only in the contract-forbidden persistence history projection
  and were treated as explicit history-boundary exceptions; that module was not edited.

## Fresh artifacts and installed-wheel smoke

Repository-local `uv build` produced:

- `council_of_translation-0.7.0-py3-none-any.whl` — 73,858 bytes — SHA-256
  `3158B12E1B7860EBE33636C0A10B6FE4A0C3A1B52B308FF46162E4CE7295EB14`
- `council_of_translation-0.7.0.tar.gz` — 67,243 bytes — SHA-256
  `CED34829BF91F802775B06B805327AE66DD032E196A5D6C80F38299F050382FE`

Each wheel environment used isolated `-I` Python and a repository-local review store.
Both invoked all five registered tools through a FastMCP Client. Successful review,
continuation and full view returned first primary text plus structured content; info and
list calls succeeded. Both asserted five tools, package/module 0.7.0, build
`concise-council-display-v5`, schema 2.2, review-only/default modes and 6/13/18 budgets.

- FastMCP 2.13.0.2 / MCP 1.29.0:
  `WHEEL_SMOKE_OK ... tools=5 primary_len=634 structured_keys=19`.
- Current FastMCP 3.4.7 / MCP 1.29.0:
  `WHEEL_SMOKE_OK ... tools=5 primary_len=634 structured_keys=19`.

The 2.13 environment emitted Authlib's upstream deprecation warning only; no import,
schema, API or tool-call error remained.

## Retries, deviations, authority and skipped checks

- PKG-023: one multi-file patch was rejected atomically due to a mismatched test context;
  no file changed. First focused run was `3 failed, 7 passed` because the tests used the
  wire alias `structuredContent` instead of FastMCP Client's Python attribute
  `structured_content`; corrected public-API assertions passed.
- PKG-024: a Pydantic deprecation warning was removed by accessing class
  `model_fields`; the exact 12-field assertion was retained.
- Build: the first `.venv ... -m build` command failed before artifact creation because
  `build` is absent. No dependency was changed; a fresh separate `uv build` succeeded.
- Wheel smoke: the first script incorrectly expected empty continuation decisions to
  error, while the tool legally created a child; the second used `count` instead of
  `total_reviews`. Corrected assertions passed without reinstalling dependencies.
- Self-improvement logging was not written because `.learnings/**` is protected; all
  incidents are recorded here and in the ledger.
- Subagents: 0 of 2 allowed.
- Git authority escalations: 10 (one exact-path `git add` and one local `git commit` for
  each package). No other authority escalation.
- Authorized repository-local dependency operations: one successful build resolution
  and two wheel-environment resolutions. No credentials requested.
- Live Goose/model/provider/external service calls: 0. Live validation was optional and
  explicitly prohibited for this Worker; therefore skipped.
- No push, PR, tag, release, deploy or Goose installation/configuration change.

## Protection and final Git state

- Contract SHA-256 remains exact.
- All fourteen contract-listed protected SHA-256 values remain exact; mismatch count 0.
- Index is empty.
- Final tracked dirty files are exactly the original Foreman assets:
  `harness/features.json`, `harness/plan.md`, `harness/progress.md`.
- Final untracked protected/user assets remain `.learnings/`, the Campaign contract,
  prior live review, audit Markdown and `reviews/`; `myTest/` remains absent.
- New allowed untracked Worker assets are this report and
  `harness/reports/CAMPAIGN-004-r1-ledger.md`.

## Remaining risks

- No live Goose/provider behavior is claimed; Foreman may independently execute the
  documented normal-user Q-009 recipe.
- FastMCP 2.13.0.2 emits an upstream Authlib deprecation warning, but dual-channel calls
  pass.
- The four explicit V0.6 persistence-history literals are outside this contract's
  allowed boundary and remain untouched; source/tool/package V0.7 diagnostics and both
  installed wheels are exact.
