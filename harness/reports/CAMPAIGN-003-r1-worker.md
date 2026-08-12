# CAMPAIGN-003-r1 Worker Report

## Disposition

`READY_FOR_REVIEW`

This is a Main Worker handoff, not Campaign acceptance. The Foreman retains independent
acceptance authority. No push, PR, release, deployment, credential request, Goose
mutation, or live model/provider call was performed.

## Authority and admission

- HARNESS_ROLE: WORKER / MAIN WORKER
- HARNESS_MODE: STRICT_CAMPAIGN
- Contract: `harness/contracts/CAMPAIGN-003-r1.md`
- Contract SHA-256: `6A1017CF7C8205CC1FB753EC747529B0BF7920676655A53314C8B71B29239A46`
- Exact admitted baseline: `fe4b55a6597d8ac18885c0faab14722f44588e12`
- Final HEAD: `3de6e5fafb0d6a0a4347b68469e99ce7ef8bc816`
- Admission index: empty; branch was `main...origin/main`.
- Admission compile: `python -m compileall -q src tests` -> exit 0,
  `COMPILE_OK`.
- Admission regression: `.venv\Scripts\python.exe -m pytest -q --basetemp
  .tmp\campaign003-r1-admission-2 -p no:cacheprovider` -> exit 0,
  `159 passed in 1.63s`.
- Existing dirty/untracked assets were inventoried before edits. All protected hashes
  matched, so the admission gate passed without repairing or rewriting repository state.

## Package execution matrix

| Package | Executor | Principal files | Commit | Focused verification |
| --- | --- | --- | --- | --- |
| PKG-017 | Main Worker | models, compatibility, persistence, V2.2 model/persistence tests | `f06e6e7be496a80f75826ef1827db2fd6770a0ae` | model/persistence suite: `28 passed in 0.30s` |
| PKG-018 | Main Worker | guided gate, orchestration, prompts, roles/runtime/tool, briefing tests | `2fc3a0239ba5e25890ec07f4e0e80f1e68bd2509` | briefing/role/runtime suite: `25 passed in 0.30s` |
| PKG-019 | Main Worker | context gaps, reconsideration, orchestration, prompts, tests | `193f6245fdc3625092c65202ee9c82664f4bf28b` | context/brief/model/role suite: `34 passed in 0.45s` |
| PKG-020 | Main Worker | shared flat forms, deterministic mappings, tests | `193f6245fdc3625092c65202ee9c82664f4bf28b` | briefing/context/form suite: `16 passed in 0.30s` |
| PKG-021 | Main Worker | digest, phase trace, orchestration, tests | `a874a6e9d18595da2449b668d8909b555cba7913` | digest/context/briefing suite: `17 passed in 0.32s` |
| PKG-022 | Main Worker | migration, version/build/tool schema, docs, integrated tests | `1fb8bcd6e9def5ebaade2773ce0ffff764297e1c`, `3de6e5fafb0d6a0a4347b68469e99ce7ef8bc816` | migration `16 passed in 1.12s`; metadata follow-up `9 passed in 0.30s` |

Subagents used: 0. Implementation followed the contract dependency order. PKG-019 and
PKG-020 share one scoped commit because they intentionally converge on the same form and
orchestration hotspots. Six total local commits were created, within the contract cap.

## Implemented contract surface

- Added schema V2.2 guided-session records with conservative V1/V2.0/V2.1 readers and
  authoritative V2.2 writes.
- Added the only authorized public argument: `briefing_mode=auto|always|off`, default
  `auto`, in the actual FastMCP/Pydantic schema. The public MCP surface remains exactly
  five tools.
- Added a deterministic, sampling-free Briefing Gate. Source/target-only `auto` asks one
  six-field form before sampling; rich context skips; `always` stops without sampling on
  non-accept; `off` records explicit assumptions. Answers have field provenance and feed
  the effective task, Council plan and reviewer prompts.
- Added bounded optional reviewer context gaps: invalid items are isolated; material,
  unanswered gaps are semantically deduplicated to at most two; one form is used; only
  affected roles are reconsidered, capped at three.
- Added flat, bounded, human-readable briefing/context/outcome forms with exact internal
  mappings and no exposed hashes, action prose or reviewer problem identifiers.
- Added the frozen process-first 12-section structured digest and deterministic Markdown
  report, six active-role lenses, minority counterfactual, blind-spots-before-verdict,
  bounded semantic deduplication, review-only output and an 8,000-code-point cap.
- Preserved V0.5 Policy Gate, outcome selection/delegation, suppression, normalized
  influence, coverage and continuation behavior. Sampling ceilings are now 6/13/18.
- Updated distribution/module version to `0.6.0`, diagnostic build to
  `guided-deliberation-v4`, schema to `2.2`, lock metadata and affected documentation.
- Metadata persistence retains only privacy-safe modes, counters and identifiers; it
  excludes briefing/context answers, reviewer/user/chief prose, display Markdown and
  phase summaries.

## Exact Core and schema evidence

The source/target-only Core probe produced: briefing before first sample; action
`accept`; asked fields `domain`, `content_type`, `audience`, `tone_goal`,
`primary_focus`, `usage_context`; `UI button` normalized to effective/plan content type
`ui`; context confidence `full`; six independent samples; one briefing call; status
`COMPLETED`; six role lenses; display length 830.

The actual briefing schema exposes the six human fields. Its content-type enum is:
`界面文案`, `营销文案`, `技术文档`, `法律或风险文案`,
`不确定，由 Council 推断`. A context-gap probe exposed one `context_1` string field,
title `补充背景 1`, maximum length 240. An outcome probe exposed one
`review_choice_1` field with title `“Continue” 的措辞结果` and values
`保留：继续`, `改为：下一步`, `暂不决定，由 Council 裁决`; exact mapping selected
`option_222222222222` with outcome `下一步` for `改为：下一步`.

The deep standard reference flow used exactly 13 samples in this order:

1. six independent reviews;
2. three context reconsiderations;
3. one discussion;
4. three outcome reconsiderations.

It recorded one context-gap interaction, one outcome interaction, three completed roles
in each reconsideration phase, a valid selected outcome, and the exact 13-phase trace:
`briefing`, `preflight`, `planning`, `independent_review`, `blind_spot_mapping`,
`context_gap`, `context_reconsideration`, `discussion`, `outcome_decision`,
`outcome_reconsideration`, `policy_gate`, `adjudication`, `digest_construction`.
Forced lightweight insufficiency remains at the six-sample ceiling and truthfully emits
skipped/failed provenance, warnings, degraded state and non-clean status.

The process digest/display uses this exact order: Case Brief; Assumptions & Context
Confidence; Blind Spots; Role Lenses; Consensus; Minority Report; Material
Disagreements; Context Gaps & Answers; User Decisions; Reconsideration Changes; Editor
Synthesis; Execution Checklist & Final Disposition. Hostile long prose and hidden-key
probes kept display at or below 8,000 code points, each role perspective at or below 240,
and excluded hidden reasoning and `suggested_translation` from review-only compact output.

## Verification evidence

- Package checks are listed in the matrix and detailed with exact commands/results in
  `harness/reports/CAMPAIGN-003-r1-ledger.md`.
- Integrated focused command:
  `.venv\Scripts\python.exe -m pytest -q tests\unit\test_v22_models_persistence.py
  tests\unit\test_v22_forms.py tests\integration\test_v22_briefing.py
  tests\integration\test_v22_context_gaps.py tests\integration\test_v22_digest.py
  tests\integration\test_orchestration_v2.py
  tests\integration\test_r3_outcome_suppression.py
  tests\integration\test_v21_elicitation.py
  tests\integration\test_v21_reconsideration.py
  tests\integration\test_tool_surface_v2.py --basetemp
  .tmp\campaign003-r1-focused -p no:cacheprovider` -> exit 0,
  `59 passed in 1.36s`.
- Final compile/full command: `python -m compileall src tests`, then
  `.venv\Scripts\python.exe -m pytest -q --basetemp
  .tmp\campaign003-r1-pytest-postbuild -p no:cacheprovider` -> both exit 0,
  `182 passed in 1.83s`.
- Fresh build: `$env:UV_CACHE_DIR='.tmp\campaign003-r1-uv-cache'; uv build --out-dir
  .tmp\campaign003-r1-dist` -> exit 0.
- Wheel: `council_of_translation-0.6.0-py3-none-any.whl`, 70,329 bytes,
  SHA-256 `C52779316470EA7F0F7AA59D83CAF4964B070CA31667B35065846257311790B9`.
- Sdist: `council_of_translation-0.6.0.tar.gz`, 63,926 bytes,
  SHA-256 `35CA90DBAE659844558EA6363E9CF0D2C1F12F6ABDA0FD05FCA45BE8A211983E`.
- A fresh repository-local Python 3.12 environment installed the wheel. Isolated
  `python -I` smoke output was:
  `{"wheel_version":"0.6.0","module_version":"0.6.0","build":"guided-deliberation-v4","schema":"2.2","tools":["continue_review","get_server_info","list_review_records","review_translation","view_review_record"],"briefing_default":"auto","budgets":{"lightweight":6,"standard":13,"strict":18},"guided_core":{"briefing_action":"accept","sampling_calls":6,"content_type":"ui","role_lenses":6,"display_length":830}}`.
- Public probes confirmed exactly five tools, actual enum/default, schema/build/version and
  6/13/18 budgets. Documentation assertion, obsolete identifier and public registration
  scans passed.
- `git diff --check fe4b55a6597d8ac18885c0faab14722f44588e12..HEAD` -> exit 0;
  staged diff empty; complete baseline-to-final diff inspected.

## Commit and changed-file audit

Chronological commits:

1. `f06e6e7be496a80f75826ef1827db2fd6770a0ae Add V2.2 guided session record models`
2. `2fc3a0239ba5e25890ec07f4e0e80f1e68bd2509 Add sampling-free review briefing gate`
3. `193f6245fdc3625092c65202ee9c82664f4bf28b Add guided context gaps and bounded forms`
4. `a874a6e9d18595da2449b668d8909b555cba7913 Add process-first review digest`
5. `1fb8bcd6e9def5ebaade2773ce0ffff764297e1c Migrate guided review contract to V0.6`
6. `3de6e5fafb0d6a0a4347b68469e99ce7ef8bc816 Retain safe guided metadata counts`

Baseline-to-final statistics: 34 files changed, 2,187 insertions, 159 deletions. Changed
files were limited to `AGENTS.md`, `README.md`, the two V0.4 docs, `pyproject.toml`,
`uv.lock`, authorized package modules under `src/council_of_translation/`, and authorized
unit/integration tests. The complete diff was inspected; allowed-path audit returned zero
disallowed paths. Neither Campaign report is committed.

## Protected state and privacy

Final protected hashes equal admission:

| Asset | Verified SHA-256 |
| --- | --- |
| `harness/plan.md` | `984F547FFDECBE02A8C7E16108BF743BD9935592DBC24F44CDBE45687E97AF9E` |
| `harness/features.json` | `D054BCB1DA0F85BA9AC8E9C96A0DC9256BE96417C190B31C8EF377A5C6776B8E` |
| `harness/progress.md` | `101B0E936093344D2FFAED334974105736BD175C32C8D715072A5EB18384E776` |
| `harness/contracts/CAMPAIGN-002-r3.md` | `1908786C679B8F3ACF67B5925CE0FBD407C0AD9A2B05DD682739903176F68007` |
| `harness/contracts/CAMPAIGN-003-r1.md` | `6A1017CF7C8205CC1FB753EC747529B0BF7920676655A53314C8B71B29239A46` |
| `harness/evaluations/CAMPAIGN-002-r3-review.md` | `8FCE03BACDAFBF6BE7B75DE1718236B0ACBDF073BE4714D752A643D1C9A810B7` |
| `harness/evaluations/CAMPAIGN-002-q007-live-review.md` | `6E70A3CB7D496CDC9ED9E61A9DA15B93102A75F7516AA72957D731B36954F273` |
| `harness/reports/CAMPAIGN-002-r3-worker.md` | `543755CA72C85D4E9AB234CA3E37405C14F33992429723C566CAB0339D6FD358` |
| `.learnings/LEARNINGS.md` | `22F939E6F980DF52487AAFE97EDCA9B90CF3931DDB7A31BF8A5BBB8F052E658F` |
| `.learnings/ERRORS.md` | `F99EB75886781958BF5AE6DCF844FD476CBCA45937896A25EE3B2E9D6CD34F0A` |
| audit Markdown | `B48073E063C4C9F34E0B6B4DAE94E80079EAAAD3B2F8E273DD60B2F25F6ABD76` |
| `reviews/20260810_145151.json` | `BA2607DEAF9BA440C514FB3D6E5AB34197EDEFA7CC04D9F83859A6EDE4E8FC73` (unchanged admission/final inventory) |

Final worktree dirt consists of the original protected Foreman/user assets plus this
Campaign's two permitted untracked report files. The Git index is empty. Evidence in
these reports contains no credentials, raw tokens, private review payloads, unnecessary
user/model prose or hidden reasoning.

## Deviations, retries, skips and remaining risk

- The first combined admission command's transport output was truncated; compile and
  full tests were rerun separately and produced the admitted evidence above.
- The first sandboxed `git add` was denied by `.git/index.lock`; 12 narrowly scoped Git
  authority escalations followed (six adds and six commits), with staged-name and cached
  diff checks before every commit. No protected asset entered the index.
- One intermediate post-PKG-018 full run reported `142 passed, 29 failed`; all failures
  were diagnosed as expected V0.6 fixture/budget migration points and were resolved by
  authorized integration changes without weakening prior behavior assertions.
- The first installed-wheel smoke used the development environment's FastMCP
  `get_tools()` helper; installed FastMCP 3.4.7 exposes `list_tools()`. The smoke was
  rerun through the installed public method and passed.
- One protected review hash command used a stale filename; the actual protected file was
  located read-only and its hash matched.
- Required checks skipped: none. `ruff` was unavailable, so the contract's dead-import
  check used a bounded AST import scan of changed production modules and found no unused
  imports.
- Live Goose/model/provider checks were intentionally not run (0 calls) because the
  contract makes them optional and prohibits requesting credentials. External mutations:
  0. A single allowed package-resolution operation downloaded five dependency artifacts
  to the repository-local uv cache for isolated wheel installation.
- Remaining risk: Foreman still needs independent acceptance and optional real Goose
  rendering validation. The fresh wheel resolved FastMCP 3.4.7 while the development
  environment has a different introspection helper; actual schema and Core behavior
  passed in both contexts.

## Pinned-commit Goose recipes for independent validation

Use the exact reviewed commit; these are instructions only and were not executed by the
Worker.

### Source/target-only briefing

Install/run:

```powershell
uvx --refresh --from git+https://github.com/PigeonCrafty/mcp-council-of-translation@3de6e5fafb0d6a0a4347b68469e99ce7ef8bc816 mcp_council_of_translation
```

Prompt:

> First call `get_server_info` and verify version 0.6.0, schema 2.2, build
> guided-deliberation-v4 and budgets 6/13/18. Then call `review_translation` with source
> `Save changes`, candidate `保存更改`, `briefing_mode=auto`, standard mode and full
> history, supplying no other context. Show me the elicitation before any reviewer
> sampling. Accept the briefing and identify the content as a UI button, adding concise
> domain/audience/tone/focus/usage context. Return the review result without applying an
> edit. Verify the process-first 12-section order, blind spots before verdict, six role
> lenses, status/telemetry and absence of a full replacement translation.

### Deep process session with optional context gap and valid outcome

Prompt:

> Call `review_translation` at the pinned 0.6.0 extension with source `Continue`,
> candidate `继续`, standard mode, `briefing_mode=always`, full history and no hard rule
> that preselects wording. Accept the briefing as UI button copy in a setup flow. If the
> Council exposes a material optional context-gap form, answer it concisely; do not ask
> the outer agent to invent a gap. If a valid outcome form is exposed, choose one of its
> displayed valid human-readable outcomes (do not supply an internal ID). Return the
> review-only result and inspect the phase trace, both reconsideration provenance blocks,
> exact outcome mapping, 13-call ceiling, degraded/warning truthfulness, process-first
> digest order, minority report, blind spots and final disposition. Do not apply edits.
