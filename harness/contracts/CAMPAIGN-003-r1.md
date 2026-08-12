# Campaign Contract: CAMPAIGN-003-r1

## Control

- Role: MAIN WORKER
- Mode: STRICT_CAMPAIGN
- State: ASSIGNED
- Repository: `C:\Users\GeZhu\MyMCP\mcp-council-of-translation`
- Baseline commit: `fe4b55a6597d8ac18885c0faab14722f44588e12`
- Baseline subject: `Close V0.5 live validation`
- Parent Campaign: `CAMPAIGN-002` (`ACCEPTED / CLOSED`)
- Execution environment: Codex Main Worker in a separate new conversation; provider identity grants no authority
- Required Worker capabilities: Python 3.10-3.13 compatible implementation, Pydantic/FastMCP schema work, deterministic async Core tests, packaging, local Git commits, bounded internal subagent coordination
- Execution ledger path: `harness/reports/CAMPAIGN-003-r1-ledger.md`
- Campaign Worker report path: `harness/reports/CAMPAIGN-003-r1-worker.md`
- Commit policy: six or fewer scoped local package/integration commits required; no push, PR, release, deployment or branch-protection change
- Worktree strategy: one shared worktree; Main Worker owns integration hotspots
- Subagent delegation: allowed, not required; maximum three bounded subagents
- Parallel delegation: allowed only for disjoint files or read-only work after interfaces are frozen
- Acceptance authority: Foreman only

Read `AGENTS.md`, `harness/plan.md`, `harness/features.json`, `harness/progress.md`, this contract, `harness/evaluations/CAMPAIGN-002-r3-review.md`, and `harness/evaluations/CAMPAIGN-002-q007-live-review.md` completely before editing. Repository assets, not conversation memory, are authoritative.

## Admission gate

Before any edit:

1. verify exact HEAD `fe4b55a6597d8ac18885c0faab14722f44588e12` and subject;
2. verify index empty;
3. verify only the protected Foreman/user dirt described below is present;
4. verify all listed SHA-256 values;
5. run a fresh baseline compile and full test suite, expected `159 passed`;
6. record exact commands, exits and elapsed results in the ledger.

Stop `BLOCKED` on any unexplained mismatch. Do not repair, stage, rewrite or delete protected dirt.

| Protected asset | SHA-256 |
| --- | --- |
| `harness/plan.md` | `984F547FFDECBE02A8C7E16108BF743BD9935592DBC24F44CDBE45687E97AF9E` |
| `harness/features.json` | `D054BCB1DA0F85BA9AC8E9C96A0DC9256BE96417C190B31C8EF377A5C6776B8E` |
| `harness/progress.md` | `101B0E936093344D2FFAED334974105736BD175C32C8D715072A5EB18384E776` |
| `harness/contracts/CAMPAIGN-002-r3.md` | `1908786C679B8F3ACF67B5925CE0FBD407C0AD9A2B05DD682739903176F68007` |
| `harness/evaluations/CAMPAIGN-002-r3-review.md` | `8FCE03BACDAFBF6BE7B75DE1718236B0ACBDF073BE4714D752A643D1C9A810B7` |
| `harness/evaluations/CAMPAIGN-002-q007-live-review.md` | `6E70A3CB7D496CDC9ED9E61A9DA15B93102A75F7516AA72957D731B36954F273` |
| `harness/reports/CAMPAIGN-002-r3-worker.md` | `543755CA72C85D4E9AB234CA3E37405C14F33992429723C566CAB0339D6FD358` |
| `.learnings/LEARNINGS.md` | `22F939E6F980DF52487AAFE97EDCA9B90CF3931DDB7A31BF8A5BBB8F052E658F` |
| `.learnings/ERRORS.md` | `F99EB75886781958BF5AE6DCF844FD476CBCA45937896A25EE3B2E9D6CD34F0A` |
| audit markdown | `B48073E063C4C9F34E0B6B4DAE94E80079EAAAD3B2F8E273DD60B2F25F6ABD76` |

Hash this r1 contract on admission and preserve it byte-for-byte. Preserve `.learnings/**`, `reviews/**`, all prior Harness artifacts, the audit markdown and `myTest/` if present. Only the required Campaign 003 ledger and Worker report may be created under Harness.

## Campaign outcome

Deliver Council of Translation V0.6 as a Goose-first guided review session. A normal caller may provide only source and candidate translation; the same `review_translation` call then gathers missing high-value context before sampling, exposes bounded material context gaps when they could change the judgment, retains the user's decisive authority among valid outcomes, and returns a process-first digest that emphasizes blind spots and distinct professional perspectives before the final verdict.

The integrated result remains review-only, uses exactly five public MCP tools, preserves V0.5 correctness and privacy, writes schema 2.2, identifies as package/module `0.6.0` and build `guided-deliberation-v4`, and enforces 6/13/18 sampling ceilings.

## Context

V0.5 is functionally accepted and live-verified. Do not redesign its outcome identity, Policy Gate, user-delegation semantics, targeted outcome reconsideration, reviewer coverage rules or five-tool boundary. The product defect is experience: source/target-only callers lack guided context collection, form titles reuse dense reviewer problem prose, and the compact result makes the verdict easier to see than the Council's blind spots, minority views and role-specific evidence.

The target is not faster adjudication. The target is a bounded, auditable expansion of the user's decision frame without hidden chain-of-thought or duplicated prose.

## Frozen design

### Architecture and invariants

- Council Core remains independent of FastMCP `Context`. Runtime adapters own sampling and elicitation details.
- Keep exactly these tools and this order-insensitive set: `review_translation`, `continue_review`, `view_review_record`, `list_review_records`, `get_server_info`.
- `review_translation` adds one public argument: `briefing_mode: auto | always | off`, default `auto`. Do not add another tool or public mode argument.
- `interactive_mode=auto`, `output_mode=review_only`, `decision_fallback=council_adjudication`, `trace_level=summary` and `history_mode=full` remain defaults.
- Pre-review briefing occurs inside the existing tool call and before the first reviewer sample.
- At most one briefing form, one context-gap form and one outcome-decision form occur per initial review.
- All elicitation schemas are flat objects of primitive fields compatible with normal Goose; do not require a custom MCP App/UI.
- The client controls rendering. Production correctness is defined by schema values, bounds, mappings, actions and persisted provenance, not button count or layout.
- User briefing answers may update mutable context/preferences but cannot erase deterministic checks, caller hard constraints, TB/SG/project-rule authority or critical blockers.
- Model-authored context gaps are advisory only. They cannot create hard constraints, blockers or policy overrides.
- User outcome selection remains decisive only among Policy-Gate-valid outcomes.
- Council fallback remains evidence-weighted Position Matrix adjudication, never majority voting.
- Show structured claims, evidence, questions, stances and position changes; never request, persist or expose unrestricted reasoning or hidden chain-of-thought.
- No code path translates files, writes translation assets or claims edits were applied.

### Shared interfaces and data contracts

#### ReviewTask and public inputs

- Add normalized `briefing_mode` with conservative default `auto`.
- Preserve all V0.5 inputs and defaults.
- `auto` briefing sufficiency is deterministic and sampling-free. A source/target-only call is sparse. Rich context requires a recognized content type plus at least two independent categories among usage context/reference, audience, style/brand, and glossary/project/technical authority.
- `always` requests the brief even when context is rich; a non-accepted result stops before sampling with a truthful pending/pre-review disposition.
- `off` never requests a briefing and proceeds with explicit assumptions/context confidence.

#### ReviewBriefV2

Add a typed effective brief with bounded values for:

- domain;
- normalized content type/location;
- audience;
- tone/communication goal;
- primary review focus;
- usage context;
- assumptions;
- context confidence (`full`, `partial`, `minimal`);
- field-level provenance (`caller`, `user_briefing`, `normalized_alias`, `inferred_default`).

Precedence is deterministic: hard constraints/rule packets, accepted user briefing for mutable fields, explicit caller context, normalized aliases, bounded inference. A more recent user briefing answer may update mutable caller context but its provenance must remain explicit.

#### Briefing interaction

The briefing form has at most six fields. Categorical fields include a concise `不确定，由 Council 推断` value. Free text is bounded and optional. Titles target 48 characters; descriptions target 160 and do not repeat titles.

Persist requested/skipped, action (`accept`, `decline`, `cancel`, `unsupported`, `malformed`), asked fields and safe provenance. Full history may store bounded accepted answers; metadata history must not store free text or reconstruct answers.

In `auto`, non-accept may continue with explicit assumptions and context confidence. In `always`, non-accept returns before reviewer sampling with zero sampling calls and a clear retry hint. Never convert missing/malformed content into an accepted answer.

#### ContextGapV2

Reviewer envelopes may include an optional `context_gaps` list in addition to required `role_feedback` and `findings`. Each gap contains:

- stable ID generated by Core;
- bounded question;
- bounded materiality statement explaining what judgment/outcome could change;
- affected role IDs;
- source role/provenance;
- answered/suppressed disposition and bounded reason.

Invalid gap entries are discarded conservatively and counted, but they do not erase otherwise valid reviewer findings or mark a valid review envelope unavailable. Gaps cannot carry blocking or hard-constraint authority.

Core deduplicates and selects at most two unanswered material gaps. It suppresses repeated, already answered, generic-curiosity and non-outcome-changing questions. One flat follow-up form uses bounded string fields with an explicit Council-assumption value. Accepted answers update the brief and trigger only affected-role context reconsideration.

#### Separate reconsideration provenance

Persist context reconsideration and outcome reconsideration separately, each with requested/completed/skipped/failed role IDs and bounded change effects. Do not double count one call across phases. Roles are selected by material relevance and deterministic priority, not raw vote counts.

#### ProcessDigestV2 and display report

Add a typed process digest in this exact presentation order:

1. case brief;
2. assumptions and context confidence;
3. blind spots;
4. role lenses;
5. consensus;
6. minority report;
7. material disagreements;
8. context gaps and answers;
9. user decisions;
10. reconsideration changes;
11. editor synthesis;
12. execution checklist and final disposition.

Retain a material lens for every active reviewer role; semantic deduplication may compress repeated issue/evidence text but cannot erase a distinct minority perspective. A minority report states the strongest valid dissent plus the condition under which it would become decisive. Blind spots precede the verdict.

Return both structured `process_digest` and a deterministic bounded Markdown `display_report`. Cap list counts and item lengths at least as strictly as the existing compact contract; cap the complete display report at 8,000 Unicode code points. Review-only responses must not contain a full replacement translation. Do not rely on an outer model to invent missing sections.

#### Phase trace and telemetry

Add bounded phase records for briefing, preflight, planning, independent review, blind-spot mapping, context gap, context reconsideration, discussion, outcome decision, outcome reconsideration, Policy Gate, adjudication and digest construction. Phase summaries contain structured disposition/count facts, not hidden reasoning.

Telemetry distinguishes briefing, context-gap and outcome elicitation calls/actions. Sampling ceilings are lightweight 6, standard 13 and strict 18. Briefing and elicitation do not count as sampling. The deep standard reference path—6 reviewers, up to 3 context reconsiderations, 1 discussion and up to 3 outcome reconsiderations—must fit exactly within 13.

#### V2.2 persistence and compatibility

- New records write schema `2.2`.
- Read V1/no-version, V2.0 and V2.1 records conservatively.
- Full history stores the bounded guided trace.
- Metadata history is allowlist-based and excludes source, candidate, caller packets, briefing free text, context answers, model/user/chief prose, display Markdown and secrets while retaining safe status, counts, modes, confidence and review-needed disposition.
- Off writes nothing.

### Main Worker implementation discretion

- Exact class/helper/module names and whether small new localization modules improve ownership.
- Exact Chinese enum wording, provided meanings, bounds and Council-inference choices satisfy the contract.
- Deterministic context sufficiency scoring implementation and alias table details within frozen categories.
- Deterministic materiality/deduplication scoring for context gaps, provided acceptance counterexamples pass.
- Internal digest construction helpers and safe semantic-deduplication implementation.
- Package commit grouping, up to six scoped commits.

### Decisions reserved for Foreman or user

- Adding/removing public tools or adding another public mode argument.
- Changing review-only scope, user authority, majority-vote prohibition or Policy Gate precedence.
- Custom MCP UI/App, provider/model routing, automatic translation edits or external storage/services.
- More than one follow-up context form, more than two context questions or higher than 6/13/18 sampling budgets.
- Weakening V0.5 tests, persistence privacy or supported record compatibility.
- Moving to a new major MCP/FastMCP API that breaks the currently live Goose path.

## Global boundaries

### Allowed files and directories

- `src/council_of_translation/__init__.py`
- `src/council_of_translation/server.py`
- `src/council_of_translation/tools/review.py`
- `src/council_of_translation/localization/**`
- `tests/unit/**`, `tests/integration/**`, `tests/conftest.py`
- `pyproject.toml`, `uv.lock` only for version/build consistency; no new dependency without stopping
- `README.md`, `AGENTS.md`, `docs/v0.4-architecture.md`, `docs/v0.4-tool-contract.md`
- Required new Campaign ledger/report paths only under `harness/reports/`

### Forbidden files, directories and systems

- `harness/plan.md`, `harness/features.json`, `harness/progress.md`
- all contracts and evaluations, including this contract
- all prior reports/ledgers
- `.learnings/**`, `reviews/**`, audit markdown, `myTest/**`
- GitHub workflows, repository settings, branch protection, credentials, Goose installation/configuration, external provider settings
- production files outside the allowed paths

### Non-goals

- General-purpose Councils or dynamic role invention.
- Custom MCP Apps/widgets or control over Goose layout/buttons.
- Translation generation as the default, file application, TB/TM ownership or project-file editing.
- Per-role provider/model selection.
- Majority voting, unlimited debate/questions or unrestricted resampling.
- Streaming raw model reasoning or persisting chain-of-thought.
- Performance optimization that hides role perspectives or skips the guided experience.

### Authorized external or destructive actions

- None. No live model/Goose call is required. Do not request credentials.
- Repository-local package/dependency reads needed by `uv build` or isolated wheel installation are allowed; record network reads and retry only after verifying the first attempt did not mutate external state.
- Local Git staging/commits are required and must include only authorized production/test/doc files. No push, PR, release, tag or deployment.

## Task graph

| Package | Observable outcome | Depends on | Allowed boundary | Acceptance and verification | Parallel-safe |
| --- | --- | --- | --- | --- | --- |
| PKG-017 | V2.2 guided-session models, compatibility and privacy-safe persistence | none | models, compatibility, persistence, focused tests | V1/V2.0/V2.1 read; V2.2 full/metadata/off; malformed fields conservative; metadata leak probes pass | yes before integration hotspots change |
| PKG-018 | Sampling-free Briefing Gate, context aliases, form mapping and field provenance | PKG-017 | roles, runtime, orchestration, tools/review, prompt builders, focused tests | source/target-only asks before sample; rich/always/off and all actions pass; `UI button` routes to ui; no fabricated answers | no |
| PKG-019 | Material context gaps, one follow-up form, context reconsideration and 6/13/18 budgets | PKG-017, PKG-018 | models, runtime, orchestration, prompt builders, roles/deliberation, focused tests | max two gaps; invalid gaps isolated; answered/immaterial dedupe; affected roles only; deep standard <=13; truthful insufficiency | no |
| PKG-020 | Shared concise form IA and deterministic outcome titles | PKG-018, PKG-019 | orchestration/form helpers, models if required, focused tests | all three form families flat/bounded/non-repeating; no reviewer problem prose/IDs/action values; exact round trips | no |
| PKG-021 | Process-first digest, phase trace and bounded display report | PKG-017 through PKG-020 | orchestration, models, policy/clustering only if needed, tools/review, focused tests | frozen order, six lenses, blind spots/minority before verdict, semantic dedupe, <=8000 display, review-only/privacy | no |
| PKG-022 | V0.6 migration, integrated evaluation, packaging and docs | PKG-017 through PKG-021 | version/build files, all tests, README/AGENTS/docs | full regression, exact identifiers/tools/defaults/budgets, fresh artifacts/wheel smoke, dead-reference scan, pinned Goose recipes | no |

## Collision and integration map

| Packages/files at risk | Required sequencing or isolation | Integration owner/check |
| --- | --- | --- |
| PKG-017/018/019/021 `models.py` and record construction | Freeze V2.2 types first; Main Worker integrates all later model changes | Main Worker; full model/persistence tests after every dependent package |
| PKG-018/019/020/021 `orchestration.py` | Strict sequence; never delegate overlapping edits concurrently | Main Worker; inspect complete combined diff and run focused Core workflows |
| PKG-018/019 `runtime.py` and elicitation telemetry | Share one phase-aware interaction contract before context-gap work | Main Worker; accept/decline/cancel/unsupported/malformed matrix |
| PKG-018/020/022 `tools/review.py` and FastMCP schemas | Freeze public `briefing_mode` and five-tool surface in PKG-018; later packages may only implement frozen presentation/version | Main Worker; exact installed-wheel introspection |
| PKG-019/021 budgets and phase summaries | Digest consumes recorded phase facts and must not infer missing execution | Main Worker; deep reference and forced insufficiency probes |
| Documentation after code contracts | Documentation may be delegated read-only/draft only after integrated behavior is stable | Main Worker; final code-to-doc assertion scan |

## Campaign acceptance criteria

1. A `review_translation` call containing only source and candidate, with `briefing_mode=auto` and supported elicitation, requests one concise briefing before the first model sample.
2. Rich caller context skips briefing in auto; always requests it; off never requests it. Sufficiency is deterministic and sampling-free.
3. Briefing accept/decline/cancel/unsupported/malformed paths retain distinct provenance; auto continues with explicit assumptions where allowed, always stops before sampling on non-accept, and no path fabricates accepted fields.
4. Briefing answers reach the effective task, CouncilPlan routing and reviewer prompts with field provenance while deterministic/caller hard authority remains intact.
5. Common content aliases including `UI button` route correctly; unknown content is visible through assumptions/context confidence rather than silent unexplained normalization.
6. Valid reviewer envelopes may carry optional context gaps; invalid gaps are isolated without destroying valid findings or coverage.
7. Only material unanswered non-duplicate gaps survive, maximum two in one form. Generic, answered, repeated and non-decision-changing gaps produce no follow-up.
8. Accepted context answers reconsider only affected roles; context and outcome reconsideration provenance remain separate and bounded.
9. Context gaps and sampled answers cannot create deterministic hard constraints, blockers or policy overrides.
10. Briefing, context-gap and outcome forms are flat primitive schemas with bounded deterministic titles/descriptions, exact mappings, no repeated titles, no internal IDs/hashes/action prose and no unbounded reviewer problem title.
11. V0.5 outcome selection, explicit Council delegation, Policy Gate invalidation, suppression provenance, influence normalization, coverage semantics and continuation remain green.
12. Process digest and display report use the frozen process-first order, retain material role lenses/minority evidence, place blind spots before verdict and semantically deduplicate repeated prose.
13. Display report is <=8,000 Unicode code points, review-only, contains no hidden reasoning and contains no full suggested translation without explicit `full_rewrite`.
14. Phase trace and telemetry truthfully distinguish briefing, context-gap and outcome interactions plus both reconsideration phases.
15. Sampling ceilings are 6/13/18. A deep standard reference flow completes useful work within 13; forced insufficiency exposes skipped/failed provenance, warnings, degraded state and non-clean status.
16. New full records serialize schema 2.2; metadata/off privacy passes hostile free-text probes; V1/V2.0/V2.1 readers remain compatible.
17. Default output remains bounded and full trace remains retrievable. Exact public tool set remains five and `continue_review` creates linked immutable revisions.
18. Package/module version is `0.6.0`, diagnostic build `guided-deliberation-v4`, schema `2.2`, defaults and 6/13/18 budgets match source and installed wheel.
19. All 159 accepted V0.5 tests plus focused V0.6 tests pass without weakening or deleting useful assertions.
20. Compile, full/focused tests, fresh sdist/wheel, isolated wheel smoke, `git diff --check`, allowed-scope audit, dead-reference scan, protected hashes and repository hygiene pass.

## Required Campaign verification

At admission and final integrated state run:

```powershell
python -m compileall src tests
.venv\Scripts\python.exe -m pytest -q --basetemp .tmp\campaign003-r1-pytest -p no:cacheprovider
```

Create named focused suites and exact printed Core outputs for at least:

- source/target-only auto briefing before first sample;
- rich-context auto skip, always/off behavior;
- briefing accept/decline/cancel/unsupported/malformed matrix;
- `UI button` alias and unknown-content assumptions;
- accepted briefing precedence versus caller hard rules;
- valid, invalid, duplicate, answered and immaterial context gaps;
- one two-question follow-up and affected-role context reconsideration;
- context-gap decline/unsupported and budget insufficiency;
- existing outcome selection/delegation, affected placeholder and anchor-suppression controls;
- all three JSON form schemas with exact titles/descriptions/value bounds;
- process-first digest ordering, six material lenses, minority/counterfactual content and deduplication;
- hostile long prose, hidden-reasoning key, review-only and metadata privacy controls;
- V1/V2.0/V2.1 reads and V2.2 full/metadata/off round trips;
- 6/13/18 mode ceilings and deep standard reference call order/count;
- continuation from a V2.2 parent without mutating it.

Build fresh artifacts with a repository-local cache/output:

```powershell
$env:UV_CACHE_DIR='.tmp\campaign003-r1-uv-cache'
uv build --out-dir .tmp\campaign003-r1-dist
```

Install the fresh wheel into a new repository-local virtual environment and smoke with `-I`. Assert package/module `0.6.0`, build `guided-deliberation-v4`, schema `2.2`, exact five tools, defaults including `briefing_mode=auto`, budgets 6/13/18, and one deterministic source/target-only guided Core path.

Then run:

- `git diff --check fe4b55a6597d8ac18885c0faab14722f44588e12..HEAD`;
- baseline-to-final name/status and allowed-file audit;
- complete diff inspection, not statistical sampling;
- tracked/index status check;
- protected SHA-256 audit;
- dead imports, obsolete build/version/default strings and public-tool registration scan;
- documentation assertion scan against implemented constants and behavior.

Live Goose/provider calls are optional. If unavailable, do not request credentials. Deliver two pinned-commit test prompts: source/target-only briefing and process-first deep session with optional context gap plus valid user outcome.

## Delegation protocol

- Delegation is allowed, not required, with a maximum of three subagents.
- Main Worker may delegate PKG-017 before integration hotspots change, bounded disjoint test/doc work after interfaces freeze, or read-only review.
- Main Worker must personally own or integrate every change to `orchestration.py`, public tool schemas and the final package graph.
- Do not delegate overlapping files concurrently in the shared worktree.
- Give each subagent exact allowed paths, required evidence and a prohibition on Harness/acceptance edits.
- Inspect every returned diff, reconcile it in the ledger and rerun package checks after integration.
- Subagents cannot commit unless the Main Worker assigns a disjoint scoped commit and verifies it; they never stage protected assets.
- Subagent completion is internal evidence only. Main Worker remains accountable for all commits, combined behavior and the final report.

## Required evidence

- Package-to-subagent/files/commits/verification matrix, including direct execution when no subagent was used.
- Exact command, exit, test count and meaningful output for admission, each package and final integration.
- Baseline-to-final commit list, changed-file list, line statistics and complete diff inspection statement.
- Exact Core outputs for form schemas, event/call order, decisions, context gaps, digest order, telemetry, status/degradation and privacy projections.
- Build artifact names/sizes and installed-wheel smoke output.
- Deviations, retries, failure diagnoses, conflict resolutions, skipped checks and their consequences.
- Authority-escalation count, subagent count, live model/Goose call count and external mutation count.
- Evidence redaction statement. Do not persist credentials, raw tokens, local private review content or unnecessary user/model prose.

## Stop conditions

- HEAD, index, protected dirt, protected hash or 159-test admission differs.
- Current Goose/FastMCP cannot perform the frozen flat briefing/context/outcome elicitation paths without a custom client or new public tool.
- Satisfying the design requires another public mode/tool, dependency, provider behavior change, custom UI, persistence privacy weakening or automatic translation edits.
- A context gap cannot be represented without model-authored hard authority or unbounded/private prose.
- The deep standard path cannot fit 13 calls without skipping required frozen work or misreporting status.
- Process-first output cannot remain bounded without erasing distinct material role perspectives.
- A required package cannot be integrated or verified within authorized files.
- Work requires push, PR, release, deployment, credentials, Goose mutation, destructive action or user/Foreman redesign.

Stop `BLOCKED`; do not silently weaken the product principle, privacy, authority, compatibility or evidence requirements.

## Handoff

Write `harness/reports/CAMPAIGN-003-r1-ledger.md` and `harness/reports/CAMPAIGN-003-r1-worker.md`. In chat start with exactly `READY_FOR_REVIEW` or `BLOCKED`, then summarize:

- ledger and report paths;
- exact baseline/final SHA and local commits/files;
- package graph execution/delegation matrix;
- compile, focused, full, build and wheel evidence;
- briefing/context-gap/process-digest exact Core evidence;
- protected state and repository hygiene;
- skipped checks and remaining risk;
- subagent, authority escalation, live-call and external-mutation counts.

Do not push, open a PR, release, deploy, change Goose, request credentials or claim Campaign acceptance/project completion. Stop after the handoff.
