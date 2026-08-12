# Campaign Contract: CAMPAIGN-004-r1

## Control

- Role: MAIN WORKER
- Mode: STRICT_CAMPAIGN
- State: ASSIGNED
- Repository: `C:\Users\GeZhu\MyMCP\mcp-council-of-translation`
- Baseline commit: `b601cf93f452a8e574e3c15a4a9c236cf8142ce1`
- Baseline subject: `Archive V0.6 Campaign acceptance`
- Execution environment: Codex Main Worker in a separate new conversation; product/provider identity grants no authority
- Required capabilities: Python 3.10-3.13, FastMCP/MCP content and structured-content return handling, deterministic report rendering, Pydantic schemas, async Core/tool tests, packaging and scoped local Git commits
- Execution ledger: `harness/reports/CAMPAIGN-004-r1-ledger.md`
- Worker report: `harness/reports/CAMPAIGN-004-r1-worker.md`
- Commit policy: no more than five scoped local commits; no push, PR, release, deployment or branch-protection change
- Worktree strategy: one shared worktree; Main Worker owns all presentation integration hotspots
- Subagent delegation: allowed, not required; maximum two bounded non-overlapping assignments
- Parallel delegation: only disjoint tests/docs after the dual-channel interface is frozen
- Acceptance authority: Foreman only

Read `AGENTS.md`, `harness/plan.md`, `harness/features.json`, `harness/progress.md`, this contract, `harness/evaluations/CAMPAIGN-003-r2-review.md`, and `harness/evaluations/CAMPAIGN-003-q008-q009-live-review.md` completely before editing. Repository assets override conversation memory.

## Admission gate

Before any edit:

1. verify exact HEAD and subject above;
2. verify the Git index is empty;
3. verify only the protected Foreman/user dirt below is present;
4. verify all listed hashes and hash this contract byte-for-byte;
5. run `python -m compileall -q src tests`;
6. run the full suite with repository-local basetemp and cache provider disabled; expected baseline is exactly `184 passed`;
7. inspect the installed FastMCP/MCP return APIs read-only and record the versions/signatures used.

Stop `BLOCKED` on unexplained drift. Do not repair, stage, rewrite, delete or move protected assets.

| Protected asset | SHA-256 |
| --- | --- |
| `harness/plan.md` | `96777F92C747EDA9A12CB10D8A0AB1E3F131C852E738A16D43A5BE13CE3071B4` |
| `harness/features.json` | `78B1B264F5E5F39E09445A94E4298A4F4E8DC5088999D89D975D651CB45CBAC2` |
| `harness/progress.md` | `0424A3529B410A2DBC0E1BE4D10A55D953785E687F70D9715C631CEE8538BE75` |
| `harness/evaluations/CAMPAIGN-003-q008-q009-live-review.md` | `6F3E0D30907F7A84B52449A1CD62572EBD121E43E50C04987B33928A5833CD31` |
| `harness/contracts/CAMPAIGN-003-r1.md` | `6A1017CF7C8205CC1FB753EC747529B0BF7920676655A53314C8B71B29239A46` |
| `harness/contracts/CAMPAIGN-003-r2.md` | `AA0C69FF175FC0D33C05156B7A0699EF5731B13FC76B4616282B279A9598461E` |
| `harness/evaluations/CAMPAIGN-003-r1-review.md` | `B2CC11664F70352F45998BCBA6EE42EB2BBA1E8BE94CACB4B470A0D112B32DB3` |
| `harness/evaluations/CAMPAIGN-003-r2-review.md` | `980F3E88ED8BD7AA49F22B39792C5A56C11610D481C5C822CA596093C6761C79` |
| `harness/reports/CAMPAIGN-003-r1-ledger.md` | `7641B0D4CD5121D2CEA635DDD10B43D174A3CDD781E853591E6C142BD6E063BE` |
| `harness/reports/CAMPAIGN-003-r1-worker.md` | `1267643257A87942D90E539830A3FB68E653A543B14A848CD525FD20E0782770` |
| `harness/reports/CAMPAIGN-003-r2-worker.md` | `D36A5AB2ED054F318DEDB6BBE388023BF8EABDC8F80AB2FFBE8E2C47B80B9783` |
| `.learnings/LEARNINGS.md` | `22F939E6F980DF52487AAFE97EDCA9B90CF3931DDB7A31BF8A5BBB8F052E658F` |
| `.learnings/ERRORS.md` | `F99EB75886781958BF5AE6DCF844FD476CBCA45937896A25EE3B2E9D6CD34F0A` |
| audit Markdown | `B48073E063C4C9F34E0B6B4DAE94E80079EAAAD3B2F8E273DD60B2F25F6ABD76` |

Preserve `.learnings/**`, `reviews/**`, the audit Markdown, `myTest/**` if present, every prior Harness artifact and all user files. Do not copy the raw live record into tests or reports. Only the required Campaign 004 ledger/report may be created under Harness.

## Campaign outcome

Deliver Council of Translation V0.7 as a concise process-first MCP experience. A normal Goose review must receive a short Chinese Council process as the tool's primary text content on the first tool result, while the existing structured compact/full data remains available as structured content for automation and audit.

The human report shows what the Council understood, one useful insight from every professional role, truthful positive consensus or disagreement, material blind spots and actual decisions/reconsideration, then the chief conclusion last. It avoids long repeated prose, empty sections, internal IDs and technical telemetry. Full evidence remains retrievable; review logic, user authority and privacy do not change.

## Context and accepted baseline

V0.6 is accepted and published. Q-008 passed: source/target-only auto briefing ran before sampling. Q-009 failed usability: Goose initially returned a diagnostic checklist even though the record contained `display_report`; a second prompt showed a repetitive 12-section report. The sanitized evidence and exact defect boundary are in `harness/evaluations/CAMPAIGN-003-q008-q009-live-review.md`.

Do not redesign the Council. Campaign 004 changes the transport/presentation layer and deterministic digest synthesis only.

## Frozen design

### Public MCP surface and dual-channel result

- Keep exactly these tools: `review_translation`, `continue_review`, `view_review_record`, `list_review_records`, `get_server_info`.
- Add no public argument or mode.
- `review_translation`, `continue_review` and `view_review_record` return a FastMCP-compatible dual-channel result:
  - first text content block: concise `display_report` plus at most one short review-ID/retrieval footer;
  - structured content: the same compact/full dictionary the tool would otherwise return, with all existing keys and server information preserved.
- `get_server_info` and `list_review_records` remain structured utilities; they need no human report wrapper.
- `trace_level=full` changes structured content detail, not the concise primary text.
- Error paths return a concise primary error message and equivalent safe structured error data without filesystem paths or secrets.
- Tool/server descriptions tell a normal outer agent to present primary Council text before optional diagnostics. Correctness is proven through actual MCP content blocks, not prompt text alone.

The locked development environment uses FastMCP 2.13.0.2, where `fastmcp.tools.tool.ToolResult` supports `content` and `structured_content`. The Worker may implement a small compatibility adapter or use an equivalent public/stable path, but must prove installed-wheel behavior under both 2.13.0.2 and the currently resolved FastMCP version. Do not pin a new version or add a dependency without stopping.

### Structured digest compatibility

- Keep `ProcessDigestV2` and its 12 fields/order for structured compatibility.
- New records continue to write schema `2.2`; old V1/V2.0/V2.1/V2.2 reads remain.
- Improve `consensus`, `role_lenses`, minority and blind-spot contents deterministically where required, but do not remove fields.
- `display_report` becomes an adaptive human projection rather than a literal 12-heading mirror.
- Metadata history continues to exclude display prose and user/model text.

### Human report contract

Use at most five Chinese sections in this order:

1. `审校背景`;
2. `专业视角`;
3. `共识、分歧与盲区`;
4. `你的决定与复议` only when a decision, delegation, context answer, requested reconsideration or material change exists;
5. `主编结论`, always last.

Rules:

- A clean six-role case targets at most 1,800 Unicode code points.
- Every default primary report is hard-capped at 3,200 Unicode code points, including footer.
- Use shallow bullets and no paragraph longer than 160 code points.
- Do not show English section headings, internal role IDs, decision/option/gap hashes, schema/build/version metadata, raw action instructions, unrestricted model prose, hidden reasoning, Position Matrix internals or Policy Gate counters.
- Keep status/degradation/warnings/coverage/human-review meaning visible in plain Chinese when material.
- Do not include a full replacement translation in `review_only`.
- Do not add a summarization sampling call.

### Role lenses

- Preserve exactly one visible lens for every active role, including truthful unavailable-role notices.
- Each lens targets 120 code points; one optional evidence anchor targets 80.
- Select the most material role-specific signal: blocker/major issue, concrete choice/condition, strongest affirmation, then availability notice.
- Compress boilerplate and repeated praise semantically, but preserve distinct role ownership and any material minority, condition or evidence target.
- Use human Chinese role names only in primary text.

### Positive consensus

- Consensus synthesis may use structured successful affirmation findings and bounded clean role feedback, not only issue clusters.
- If all successful active roles independently affirm no material blocker and share a concrete outcome, report a positive consensus such as support for keeping the candidate.
- If roles are clean but do not share a concrete semantic claim, say that no role found a release-blocking issue without inventing a common recommendation.
- Partial/none coverage cannot become positive consensus and must remain a blind spot/human-review condition.
- Role counts describe coverage only. They never feed Policy Gate/adjudication or become majority voting.
- The accepted live counterexample must not render `未形成需合并的实质共识项` when all six structured role responses affirm the candidate.

### Conditional detail and final conclusion

- Omit empty/no-op context-gap, user-decision and reconsideration headings.
- Include section 4 whenever user input or reconsideration materially happened, even if the outcome did not change.
- Surface strongest minority plus decisive condition only when a valid dissent exists; otherwise one short no-material-disagreement statement is sufficient.
- Main conclusion contains publishability, human-review need, up to three highest-priority actions and a retrieval hint/review ID footer.
- Final disposition remains the last substantive line.

### Presentation integrity

- Add unique sentinel tests proving `tone_goal` and `primary_focus` form titles, submitted keys, effective brief, reviewer prompt and full record remain correctly mapped and never transpose.
- Preserve true phase chronology in structured data; primary text may summarize only actual recorded phases.
- `view_review_record` must not accidentally expose full raw content as primary text. Its structured content follows requested detail level; its primary text remains the concise report for V2.2 and a bounded legacy summary for old records.
- Structured content remains JSON-safe and backward-compatible for normal callers.

### Version and invariants

- Package/module version: `0.7.0`.
- Diagnostic build: `concise-council-display-v5`.
- Schema: `2.2`.
- Defaults remain review-only, interactive auto, briefing auto, trace summary, history full and Council adjudication fallback.
- Sampling ceilings remain 6/13/18; presentation consumes zero sampling calls.
- User authority, Policy Gate, reviewer coverage, continuation immutability, privacy and no-file-edit boundary remain unchanged.

### Main Worker discretion

- Exact compatibility-adapter module/name and public import strategy for FastMCP result objects.
- Exact Chinese microcopy within frozen section, length, safety and ordering constraints.
- Deterministic sentence/semantic-key helpers for role compression and positive consensus.
- Internal test fixture organization and commit grouping up to five commits.

### Reserved decisions

- New tools, arguments or presentation modes.
- Custom MCP App/widget, provider-specific rendering or Goose fork changes.
- Schema migration, dependency pin/addition, budget changes or extra model calls.
- Removing structured fields, full retrieval, reviewer roles or material evidence.
- Changing review logic, Policy Gate, user authority, fallback or translation-application scope.

## Global boundaries

### Allowed paths

- `src/council_of_translation/__init__.py`
- `src/council_of_translation/server.py`
- `src/council_of_translation/tools/review.py`
- `src/council_of_translation/localization/digest.py`
- `src/council_of_translation/localization/orchestration.py`
- `src/council_of_translation/localization/models.py` only if a bounded presentation validator/helper is necessary; no schema field removal
- `src/council_of_translation/presentation.py` or one equivalent new small presentation adapter
- `tests/unit/**`, `tests/integration/**`, `tests/conftest.py`
- `pyproject.toml`, `uv.lock` only for 0.7.0 metadata; no dependency change
- `README.md`, `AGENTS.md`, `docs/v0.4-architecture.md`, `docs/v0.4-tool-contract.md`
- required new Campaign 004 ledger/report paths

### Forbidden paths and systems

- `harness/plan.md`, `harness/features.json`, `harness/progress.md`, all contracts/evaluations and prior reports
- `.learnings/**`, `reviews/**`, audit Markdown, `myTest/**`
- persistence, compatibility, runtime, roles, policy, preflight, clustering or deliberation production modules unless the Foreman issues a revision
- prompts for sampled reviewer reasoning except documentation-only presentation guidance; no reviewer contract redesign
- GitHub workflows/settings, branch protection, credentials, Goose installation/configuration and external providers
- production files outside allowed paths

### Authorized external/destructive actions

- No live Goose/model/provider calls and no credentials.
- Repository-local dependency reads/build/install for dual-version wheel smoke are allowed. Record network reads and avoid retry unless the first attempt's state is understood.
- Scoped local Git staging/commits are required. No push, PR, release, tag or deployment.

## Task graph

| Package | Observable outcome | Depends on | Allowed boundary | Acceptance and verification | Parallel-safe |
| --- | --- | --- | --- | --- | --- |
| PKG-023 | Primary Markdown content plus structured dictionary on three human-facing tools | none | presentation adapter, tools/review, server instructions, focused tool tests | actual MCP result has first text block and structured content; errors safe; five tools unchanged | no |
| PKG-024 | Adaptive <=5-section Chinese report with conditional sections and 1,800/3,200 budgets | PKG-023 | digest, orchestration, models only if necessary, focused renderer tests | clean/disputed/degraded/pending/continuation fixtures; conclusion last; no internal labels | no |
| PKG-025 | Truthful positive consensus and six concise distinct role lenses | PKG-024 | digest, orchestration, focused consensus/lens tests | live-shaped six affirmations yield positive consensus; minorities/coverage preserved; no voting influence | no |
| PKG-026 | Layered retrieval, field mapping, privacy and invariant regressions | PKG-023 through PKG-025 | tools/review, digest/orchestration, tests | tone/focus sentinels round-trip; view full text stays concise; structured full complete; privacy/review-only/degradation green | no |
| PKG-027 | V0.7 identifiers, docs, dual-FastMCP installed-wheel smoke and Goose recipe | all prior | version/build files, docs, integrated tests | 0.7.0/build/schema/tools/budgets exact; fresh artifacts; 2.13/current result shape; dead references; Q-009 recipe | no |

## Collision and integration map

| Hotspot | Required sequencing | Owner/check |
| --- | --- | --- |
| Tool return annotations/output schema and FastMCP adapter | Freeze PKG-023 before other packages rely on result shape | Main Worker; actual server tool-call probes in both FastMCP versions |
| `digest.py` role lenses, consensus and renderer | PKG-024 then PKG-025; no concurrent edits | Main Worker; clean/disputed/degraded fixture matrix |
| `orchestration.py` compact/full/continuation paths | Integrate after renderer and adapter interfaces freeze | Main Worker; full regression after each change |
| Existing tests calling decorated `.fn` directly | Preserve structured assertions through an explicit helper/result unwrap; do not weaken them | Main Worker; baseline assertion audit |
| Version/docs/package smoke | Only after behavior is stable | Main Worker; source-to-wheel contract scan |

## Campaign acceptance criteria

1. `review_translation`, `continue_review` and `view_review_record` produce primary text content and structured content through actual FastMCP calls.
2. Primary text equals the bounded `display_report` plus at most one short retrieval footer; structured content preserves expected compact/full keys.
3. Five or fewer Chinese sections render in frozen order and the final disposition is last.
4. Clean six-role output is <=1,800 code points in the reference fixture; every report/footer is <=3,200.
5. Every active role appears once with a distinct concise lens; unavailable roles appear truthfully.
6. Repeated affirmative prose is compressed without hiding material evidence, dissent, conditions or blockers.
7. Six affirmative structured role responses produce truthful positive consensus; partial coverage cannot.
8. Empty interaction sections are omitted; actual user/context/reconsideration activity is shown.
9. Primary text contains no English implementation headings, internal IDs/hashes, hidden reasoning, unnecessary telemetry or full replacement translation under review-only.
10. Degradation, warnings, fallback, coverage gaps and human-review requirements remain clearly visible.
11. Unique `TONE_SENTINEL` and `FOCUS_SENTINEL` values round-trip to the correct form fields, effective brief, prompts and full record.
12. Full and compact structured retrieval remain complete; metadata/off privacy and V1/V2.0/V2.1/V2.2 compatibility remain green.
13. User outcome authority, delegation, Policy Gate, normalized influence, continuation immutability and reviewer coverage behavior remain green.
14. Presentation adds zero sampling calls and all paths remain within 6/13/18.
15. Exactly five tools, defaults, package/module 0.7.0, build `concise-council-display-v5` and schema 2.2 are correct in source and installed wheels.
16. FastMCP 2.13.0.2 and the currently resolved install both expose first text content plus structured content without API/schema failure.
17. All 184 accepted V0.6 tests plus focused V0.7 tests pass without deleting or weakening useful assertions.
18. Compile, focused/full tests, fresh build, wheel smoke, diff/scope audit, protected hashes, dead-reference scan and repository hygiene pass.
19. Documentation describes primary text, structured content, layered detail, exact identifiers/tools/budgets and review-only behavior accurately.
20. A pinned normal-user Goose recipe validates Q-009 without asking for diagnostic fields or requiring a second `view_review_record` prompt.

## Required verification

At admission and final:

```powershell
python -m compileall -q src tests
.venv\Scripts\python.exe -m pytest -q --basetemp .tmp\campaign004-r1-full -p no:cacheprovider
```

Create focused evidence for:

- actual FastMCP call result content blocks and structured content for review, continuation and view;
- safe dual-channel error result;
- clean six-affirmation live-shaped fixture with positive consensus and <=1,800 report;
- disputed/minority, blocker, partial/none coverage, degraded/warning/fallback and returned-pending fixtures;
- conditional decision/context/reconsideration section presence/absence;
- six active roles once each, lens/evidence bounds and semantic repetition compression;
- Chinese headings, final disposition last, <=3,200 hostile prose cap and forbidden-token scan;
- review-only no replacement translation and no new samples;
- `TONE_SENTINEL` / `FOCUS_SENTINEL` schema-to-record-to-prompt round-trip;
- compact/full/metadata/off and continuation retrieval;
- V0.6 decision/delegation/Policy Gate/coverage regressions;
- exact tool/default/version/build/schema/budget introspection.

Run an exact Core/tool printed probe showing:

- primary content text preview and length;
- structured-content key set;
- section headings in order;
- six role labels with no internal IDs;
- positive consensus for the live-shaped clean fixture;
- sampling count unchanged;
- full retrieval structured evidence count while primary text remains concise.

Build fresh artifacts with repository-local cache/output. Install the wheel twice in fresh repository-local environments: once constrained to FastMCP 2.13.0.2 and once with the current dependency resolution. In each, invoke the registered tools through the server API and assert primary text plus structured content, exact five tools, 0.7.0, build/schema/defaults/budgets and no import/API error.

Then run:

- `git diff --check b601cf93f452a8e574e3c15a4a9c236cf8142ce1..HEAD`;
- baseline-to-final allowed-path and complete diff audit;
- no obsolete V0.6 identifiers in active source/docs/tests except explicit compatibility/history fixtures;
- dead import and tool registration scan;
- protected hashes, index emptiness and final worktree inventory.

Live calls are optional and credentials must not be requested. Deliver this normal-user recipe concept without a diagnostic checklist: source/candidate only, manually answer briefing, then ask for Council review; the first final answer must itself expose the concise process, six role lenses, truthful consensus/uncertainty and verdict last.

## Delegation protocol

- Maximum two subagents; delegation is allowed, not required.
- Only disjoint tests/docs or read-only review may be delegated after PKG-023 freezes the return shape.
- Main Worker personally owns/integrates `tools/review.py`, the presentation adapter, `digest.py` and final orchestration behavior.
- No concurrent edits to shared production files.
- Subagents never modify Harness, commit without an explicit disjoint assignment, or claim acceptance.
- Main Worker inspects every returned diff and reruns integrated tests.

## Stop conditions

Stop `BLOCKED` if baseline, contract/protected hashes or admission count differ; dual-channel results cannot be supported across required FastMCP versions without a dependency/API decision; the frozen report budget would hide material evidence; a schema/public-interface/review-logic change is required; or work needs credentials, live calls, external mutation or forbidden paths.

## Handoff

Maintain `harness/reports/CAMPAIGN-004-r1-ledger.md` and write `harness/reports/CAMPAIGN-004-r1-worker.md`. Start the chat handoff with exactly `READY_FOR_REVIEW` or `BLOCKED`, then report:

- contract hash, baseline/final HEAD and commits;
- package/file/verification matrix and any subagents;
- primary/structured result probes, clean/disputed/degraded report evidence and length bounds;
- full/focused test, build and both installed-wheel smoke results;
- skipped checks, retries, deviations, Git authority escalations and external/live-call counts;
- protected hashes, index/worktree state and remaining risks.

Do not push or claim Campaign acceptance/project completion.
