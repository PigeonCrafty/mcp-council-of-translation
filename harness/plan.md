# Council of Translation V0.6 Harness Plan

## Control

- Harness mode: `STRICT_CAMPAIGN`
- Foreman: Codex
- Main Worker: Codex Main Worker in a separate new conversation
- Active Campaign: `CAMPAIGN-003-r2` (`ACCEPTED / CLOSED`)
- Accepted implementation HEAD: `9dac21dd3cee9d9a299786e8cdec525f28a0c517`
- Product target: `0.6.0`
- Diagnostic build target: `guided-deliberation-v4`
- Acceptance authority: Foreman only

Repository artifacts are the source of truth. Conversation summaries do not override this plan, `features.json`, `progress.md`, or the active Campaign contract.

The Foreman and Main Worker are separate Codex conversations. The Worker must bootstrap exclusively from repository assets and must not assume access to the Foreman's conversation context.

The V0.4 and V0.5 sections below are accepted architectural history. The `Campaign 003: Guided Process-first Council` section is the authoritative delta for the active V0.6 target.

`CAMPAIGN-003-r1` produced the integrated V0.6 implementation and preserved evidence for all but one PKG-018 boundary. `CAMPAIGN-003-r2` corrected that boundary: auto-mode context is sufficient only when content type is recognized **and** at least two independent context categories are present. Independent review accepted the combined Campaign 003 implementation. Live Goose gates Q-008 and Q-009 remain separate post-publication validation.

## Product outcome

Upgrade Council of Translation from independent role reviews plus a coordinator summary into a Goose-first, review-only structured deliberation system that:

1. exposes translation blind spots from distinct professional roles;
2. groups reviewer findings around issues rather than personalities;
3. runs bounded, targeted cross-role discussion only where it adds value;
4. asks the user to decide among valid alternatives by default when Goose supports elicitation;
5. treats the user's choice as decisive among valid options;
6. falls back to constraint-aware Council adjudication when the user declines, cancels, or cannot interact;
7. reconsiders only affected roles after new user context or preference;
8. returns a compact chief-editor summary while persisting a full structured trace;
9. remains review-only and never edits translation files;
10. is testable without live Goose or live model calls.

## Frozen product decisions

### Target environment

- Goose Desktop and interactive Goose CLI are the primary clients.
- Generic MCP behavior is supported through graceful capability fallbacks, not at the expense of Goose usability.
- Non-interactive Goose CLI must not hang or fail merely because elicitation is unavailable.
- Council Core must not depend directly on Goose-specific Rust types or UI code.

### User interaction

- `interactive_mode="auto"` is the default for all review modes.
- Interaction occurs only when there is a meaningful choice among at least two valid alternatives or the user can provide material missing context.
- A review may surface at most three DecisionPoints, collected in one elicitation form when the client supports it.
- The default user authority is `decisive_within_valid_options`.
- User input is classified as `preference`, `context_update`, or explicit `policy_override`.
- A normal preference cannot override technical integrity, semantic correctness, an explicit hard TB/project rule, or a critical risk blocker.
- An explicit policy override must be labeled and preserved in the decision trace. It must never silently erase a technical-integrity failure.

### No literal majority voting

- Do not restore the legacy one-person-one-vote mechanism.
- The fallback is `council_adjudication`, based on a structured Position Matrix.
- Invalid options are removed by the Policy Gate before adjudication.
- Remaining positions use role relevance, evidence provenance, constraint tier, blocking status, and confidence; raw vote counts are not authoritative.
- If valid alternatives remain indistinguishable, return `review_needed="是"` rather than manufacture a majority.

### Output and trace

- Default `trace_level="summary"` returns a chief-editor overview, blind spots, consensus, material disagreements, user decisions, final disposition, and `review_id`.
- Full reviewer output, issue clusters, discussion turns, positions, user decisions, reconsiderations, and decision trace are persisted when `history_mode="full"`.
- Default `history_mode="full"` preserves current behavior.
- Do not place hidden chain-of-thought or unrestricted model reasoning in either summary or full trace. Persist structured claims, evidence, stance, proposed action, confidence, and position changes only.
- Full records are retrieved on demand through `view_review_record`; V0.4 does not require a custom MCP App or clickable UI.

### Compatibility

- Value and correctness take priority over preserving the V0.3 response shape.
- Existing V1 records remain readable. A missing `schema_version` means V1.
- V0.4 may expose a compact compatibility view for `reviews` and `conflict_reviews` when inexpensive, but must not weaken the V2 design to preserve aliases.
- Legacy debate/voting code is removed only after useful security and persistence tests are migrated.

## Public MCP surface

V0.4 should expose exactly these normal tools:

1. `review_translation(...)` — enhanced V2 orchestration.
2. `continue_review(review_id, user_decisions, ...)` — the only new public tool; resumes or revises a prior decision using linked immutable history.
3. `view_review_record(review_id, detail_level="full")` — enhanced V1/V2 reader.
4. `list_review_records(...)` — enhanced metadata listing.
5. `get_server_info()` — version and capability diagnostics.

Do not register legacy debate, voting, or generic personality Council tools.

## State machine

```text
RECEIVED
  -> NORMALIZED
  -> PREFLIGHTED
  -> PLANNED
  -> INDEPENDENT_REVIEWED
  -> CLUSTERED
  -> DISCUSSED | DISCUSSION_SKIPPED
  -> DECISION_POINTS_READY | NO_USER_DECISION_NEEDED
  -> USER_DECIDED | USER_DECLINED | USER_CANCELLED
     | INTERACTION_UNSUPPORTED | RETURNED_PENDING
  -> RECONSIDERED | RECONSIDERATION_SKIPPED
  -> POLICY_GATED
  -> ADJUDICATED
  -> COMPLETED | COMPLETED_WITH_FALLBACK | NEEDS_HUMAN_REVIEW
```

`continue_review` creates a new revision linked through `parent_review_id`; it does not mutate an already persisted parent record.

## Shared data contracts

Use Pydantic v2 models internally for V2 persisted and LLM-facing structures. Add Pydantic as a direct dependency if it becomes a direct API. Keep small V1 parsing adapters where needed. Invalid model output must normalize conservatively and must not become a hard constraint.

### FindingV2

Required semantic fields:

- `finding_id`
- `agent_name`
- `role_perspective`
- `source_span`
- `candidate_span`
- `issue_type`
- `severity`
- `constraint_tier`
- `blocking`
- `problem`
- `evidence`
- `evidence_type`
- `rule_refs`
- `action`
- `confidence`

The parser may accept legacy `span`, but V2 serialization must distinguish source and candidate anchors.

### RoleDefinition

Required fields:

- `id`, `display_name`, `role_type`
- `mission`, `scope`
- `must_check`, `must_not_decide`
- `evidence_policy`, `blocking_conditions`
- `applicable_modes`, `applicable_content_types`
- `discussion_policy`, `priority`
- `output_contract_version`, `prompt_version`

`chief_editor` is an `adjudicator`, not a ninth reviewer.

### PreflightResult

Contains typed checks with `check_id`, `kind`, `status`, `severity`, source/candidate evidence, and `blocking`. V0.4 deterministic blockers are limited to high-confidence technical integrity checks:

- named and braced placeholder parity;
- printf-style placeholder parity;
- explicit variable/command tokens;
- HTML/XML tag balance and required-tag parity;
- URL preservation;
- explicit do-not-translate literals supplied by the caller.

Numeric and Markdown differences are warnings/signals unless an explicit project constraint makes them hard.

### IssueCluster and Position Matrix

`IssueCluster` includes:

- stable `issue_id`, topic/category, source/candidate anchors;
- finding IDs and participant role IDs;
- candidate actions and structured positions;
- evidence and immutable hard constraints;
- severity, constraint tier, blocking state;
- consensus status and whether user input is needed.

Each `RolePosition` includes `role_id`, `stance`, `option_id`, claim, evidence, confidence, blocking status, and conditions. Allowed stances are `accept`, `accept_with_conditions`, `reject`, and `not_applicable`.

### Discussion and user decision

`DiscussionTurn` records only structured deliberation: speaker, target, stance (`support`, `challenge`, `qualify`, `reconsider`), claim, evidence, proposed action, confidence, and whether the position changed.

`DecisionPoint` contains stable option IDs, valid options, recommended option, reason user input is useful, and a fallback. At most three DecisionPoints are emitted per review.

`UserDecision` records selected option, authority mode, classification, optional context, elicitation action, and provenance.

### ReviewRecordV2

Required sections:

- `schema_version`, `review_id`, `parent_review_id`, timestamps;
- normalized task and input diagnostics;
- runtime metadata and CouncilPlan;
- preflight, independent reviews, issue clusters;
- discussion rounds, decision points, user decisions;
- reconsiderations, policy-gate result;
- chief-editor decision and decision trace;
- status, fallback reason, version metadata.

Use collision-resistant, lexically sortable review IDs such as UTC timestamp with microseconds plus a random suffix. The reader must accept legacy `YYYYMMDD_HHMMSS` IDs.

## Runtime abstraction

Council orchestration depends on two interfaces rather than FastMCP Context directly:

- `ModelExecutor.sample(...)`
- `UserInteractionGateway.capabilities()` and `elicit(...)`

FastMCP adapters wrap the current `ctx.sample` and `ctx.elicit` behavior. Test doubles support deterministic scripted responses, unsupported interaction, decline, cancel, malformed responses, and errors.

MCP/Goose payloads and all model outputs are untrusted data. Delimit them, cap their size, normalize them, and never allow reviewer output to create immutable project rules or deterministic blockers.

## Sampling and interaction budgets

- lightweight: maximum 6 model sampling calls;
- standard: maximum 10 model sampling calls;
- strict: maximum 14 model sampling calls;
- maximum one targeted discussion round;
- standard: at most one discussed issue and three participating roles;
- strict: at most two discussed issues and four participating roles;
- at most three DecisionPoints in one elicitation form;
- affected roles may reconsider in one batched call per role;
- no substantive conflict means no manufactured discussion.

Every record stores actual sampling, elicitation, latency, fallback, and parse-failure counts.

## Persistence

- Write new records to a stable per-user data directory, configurable with `COUNCIL_REVIEWS_DIR`.
- Use atomic writes.
- Read new storage first and optionally read the legacy working-directory `reviews/` path for V1 compatibility.
- `history_mode` values: `off`, `metadata`, `full`; default `full`.
- `metadata` must not persist source text, candidate translation, TB/SG packets, model text, or user free text.
- Tests inject a temporary storage directory and never write to the user's real Goose data directory.

## Suggested source layout

The Main Worker may refine names without changing boundaries, but `workflow.py` must stop owning parsing, orchestration, conflict detection, persistence, and IDs together.

```text
src/council_of_translation/localization/
  models.py
  roles.py
  preflight.py
  clustering.py
  deliberation.py
  policy.py
  runtime.py
  persistence.py
  orchestration.py
  prompt_builders.py
  compatibility.py
```

Avoid compatibility wrappers that merely duplicate the old monolith. Keep one authoritative implementation per responsibility.

## Quality gates

The Campaign is not ready for Foreman review until:

1. all existing relevant tests pass or are intentionally replaced with equivalent coverage;
2. V1 record reading, V2 full/metadata/off persistence, and collision-safe IDs are tested;
3. preflight blocker and warning behavior is tested with false-positive cases;
4. issue clustering is tested for same issue/different wording and different issue/same span;
5. no-conflict reviews skip discussion;
6. user accept, decline, cancel, unsupported, pending, and later `continue_review` are tested;
7. user preference cannot override an invalid technical option;
8. a context update triggers only affected-role reconsideration;
9. model call budgets are enforced in every mode;
10. default response is compact while full trace is retrievable;
11. no hidden reasoning is exposed;
12. Goose Desktop and interactive CLI flows are exercised when practical, with live-call counts disclosed;
13. repository instructions, review-only behavior, and output-mode rules remain intact;
14. authoritative docs match the implemented contract;
15. legacy code removal leaves no dead imports or obsolete registered tools.

## Non-goals

- General-purpose dynamic Councils.
- External Translation/TB MCP orchestration.
- Per-role model/provider routing.
- Role-specific Skills.
- Translation file editing or automatic application of fixes.
- Custom MCP App/UI in V0.4.
- Literal democratic majority voting.
- Unlimited debate rounds.
- Persisting or exposing unrestricted chain-of-thought.

## Campaign 002: Outcome-first Decision UX

### Acceptance state

The repository implementation is accepted at `ca3d24afdc8feaa65286b13c6118720809749436` by `harness/evaluations/CAMPAIGN-002-r3-review.md` and published on protected `main` through PR #3 at `daacdbfdd2d3710291c8d792040d08875396b8c5`. F-011 through F-016 are accepted. Two real Goose workflows independently verified explicit Council delegation and valid user-outcome selection with targeted reconsideration; Q-007 is accepted by `harness/evaluations/CAMPAIGN-002-q007-live-review.md`. Campaign 002 is closed.

### Why this Campaign exists

V0.4 has passed a real Goose end-to-end run. The live record `20260812T060954605875Z_1d988172bd1f` proves that sampling, six-role coverage, elicitation, reconsideration, adjudication, persistence, and full-trace retrieval work together. It also exposed a product-level weakness: the single Goose form rendered one submit button correctly, but the displayed choices were long overlapping reviewer actions rather than concise, mutually exclusive translation outcomes. Internal option IDs and dense descriptions made a successful interaction feel like a diagnostic dump.

V0.5 keeps the standard MCP elicitation form and improves the information architecture. It does not introduce a custom Goose UI.

### Frozen V0.5 decisions

- Keep exactly five public MCP tools and the review-only boundary.
- Keep `interactive_mode="auto"`, `decision_fallback="council_adjudication"`, `trace_level="summary"`, and `history_mode="full"` as defaults.
- Keep sampling budgets at lightweight 6, standard 10, and strict 14 for the first V0.5 implementation; improve targeting before expanding budgets.
- Present decisions as mutually exclusive candidate outcomes, not raw reviewer action strings.
- Retain one batched MCP form with one submit action. One button is expected client behavior; the Council must make the fields and choices readable.
- Always offer an explicit `暂不决定，由 Council 裁决` choice when user interaction is available.
- A valid user choice remains decisive among valid options and cannot bypass the Policy Gate or deterministic hard constraints.
- Reconsider only roles whose recorded position conflicts with the selected outcome or whose expertise is materially affected.
- If the budget prevents required reconsideration, report a truthful degraded result with explicit warnings rather than silently returning `COMPLETED`.
- The compact response leads with the effective task, a chief-editor deliberation digest, the decision outcome, and warnings; the full trace remains available through `view_review_record`.
- V2.1 records must read V1 and V2.0 history. Value and correctness continue to take priority over preserving obsolete response aliases.

### V2.1 data contract

#### FindingV2 additions

- `finding_kind`: `issue`, `choice`, or `affirmation`.
- `proposed_value`: the concrete target outcome, when the finding proposes a choice.
- Clean `affirmation` findings may support coverage and consensus but must not become issue clusters or DecisionPoints merely because they contain explanatory prose.
- Legacy V2.0 findings without these fields normalize conservatively as `issue` unless their stored structure proves otherwise.

#### Outcome-first clusters and decisions

- `IssueCluster` owns normalized candidate outcomes derived from distinct `proposed_value` values, the current candidate, and admissible Council proposals.
- Raw `action` remains reviewer advice and evidence; it is not itself a selectable option.
- Options with the same normalized outcome collapse into one option regardless of how many roles repeat them.
- If fewer than two materially distinct valid outcomes remain after the Policy Gate, do not create a DecisionPoint.
- The current candidate is represented explicitly when it is a valid alternative.

Each `DecisionOption` carries:

- stable internal `option_id`;
- machine-comparable `outcome_value`;
- concise user-facing `label` and `description`;
- supporting role IDs and a bounded support rationale;
- policy validity and invalidation reason where applicable.

Internal IDs remain in the trace and form value mapping but are not shown as user-facing option text.

#### User decision and delegation

- `UserDecision` distinguishes selecting an outcome from explicitly delegating to the Council.
- Delegation invokes the existing constraint-aware Position Matrix; it is not a majority vote and is not recorded as an interaction failure.
- Unsupported, declined, cancelled, malformed, and explicit delegation remain distinguishable in provenance and telemetry.

#### Compact response and status truthfulness

- Add a bounded `effective_task` snapshot that reports normalized content type, audience, mode, and material rule context actually used by the server.
- Add a bounded `deliberation_summary` containing consensus, material disagreement, evidence basis, selected/delegated outcome, and affected-role reconsideration.
- Add explicit `degraded` and `warnings` fields.
- Required post-decision work skipped for budget or runtime reasons yields `COMPLETED_WITH_FALLBACK` or `NEEDS_HUMAN_REVIEW`, according to integrity impact; it must not masquerade as an unqualified `COMPLETED` result.
- Chief-editor checklist items are deduplicated by normalized outcome and evidence target.

### Goose form presentation rules

- At most three DecisionPoints in one elicitation form.
- At most four user-facing choices per DecisionPoint, including the explicit Council-delegation choice.
- Labels should be short translation outcomes (target: at most 48 Unicode code points).
- Descriptions explain the tradeoff in plain language (target: at most 160 Unicode code points) and do not repeat full reviewer feedback.
- Field titles identify the decision topic; descriptions explain why user judgment is useful.
- Option ordering is deterministic: current candidate first when valid, then distinct alternatives by policy/relevance, then Council delegation last.
- The form result maps safely back to stable internal option IDs and rejects unknown or stale values.

### Targeted reconsideration policy

- A supporting role is not resampled solely because the user selected the outcome it already supports.
- Prefer dissenting roles whose position conflicts with the chosen outcome, followed by roles whose hard expertise is materially implicated.
- Respect role priority and remaining mode budget; do not manufacture reconsideration for unaffected roles.
- For the standard six-reviewer, one-chief-editor path, up to three truly affected roles can reconsider within the existing 10-call budget.
- Persist requested, completed, skipped, and failed reconsideration roles separately.

### Campaign package graph

1. `PKG-011` — V2.1 outcome-first domain models, compatibility, and persistence.
2. `PKG-012` — candidate outcome extraction, normalization, deduplication, and DecisionPoint eligibility.
3. `PKG-013` — Goose-readable batched elicitation form, stable value mapping, and explicit Council delegation.
4. `PKG-014` — position-aware targeted reconsideration, budget accounting, and truthful degraded statuses.
5. `PKG-015` — compact deliberation digest, effective-task visibility, warning surface, and chief-output deduplication.
6. `PKG-016` — V0.5 regression/evaluation corpus, migration tests, version/build metadata, and authoritative documentation.

Packages are executed sequentially under one Strict Campaign. Shared orchestration and model files are integration hotspots owned by the Main Worker; implementation subagents may receive only bounded, non-overlapping work or read-only assignments.

### V0.5 quality gates

1. A deterministic `Continue` / `继续` / `下一步` fixture renders genuine outcome choices rather than reviewer instructions.
2. Duplicate reviewer wording cannot multiply or duplicate options.
3. A clean affirmation does not manufacture an issue or user decision.
4. The current candidate, distinct valid alternatives, and Council delegation are mapped round-trip through the form without exposing internal IDs as labels.
5. Selecting an outcome resamples only contrary or materially affected roles; the standard reference flow fits the 10-call budget without `reconsideration_budget_unavailable`.
6. A forced insufficient-budget case returns explicit degraded status and warnings.
7. Compact output is bounded, non-duplicative, and explains Council reasoning without exposing hidden chain-of-thought.
8. V1 and V2.0 records remain readable; new full and metadata V2.1 records preserve the privacy contract.
9. All 117 accepted V0.4 tests plus focused V0.5 tests pass.
10. Exact five-tool introspection, review-only behavior, 6/10/14 budgets, package/module version `0.5.0`, and diagnostic build `outcome-first-decision-v3` are verified.
11. A fresh sdist and wheel are built from the V0.5 candidate using a repository-local cache/output path.
12. A pinned-commit Goose test prompt and expected evidence checklist are delivered even when Worker credentials do not permit a live provider call.

### V0.5 non-goals

- Custom MCP Apps, bespoke Goose widgets, or multiple submit buttons.
- General-purpose Councils or non-localization workflows.
- Majority voting or one-person-one-vote restoration.
- Per-role provider/model selection.
- Automatic translation editing or file mutation.
- Unlimited discussion/reconsideration rounds.
- Budget expansion before targeted selection is proven insufficient.
- Persisting or exposing hidden reasoning.

## Campaign 003: Guided Process-first Council

### Why this Campaign exists

V0.5 proves that normal Goose can execute the complete technical path: six-role sampling, structured findings, bounded discussion, readable outcome elicitation, explicit Council delegation, valid user authority, targeted reconsideration, evidence-weighted adjudication, compact output and full-trace retrieval. The two accepted live records are summarized in `harness/evaluations/CAMPAIGN-002-q007-live-review.md`.

The remaining product defect is information architecture. A source/target-only user must already know which domain, content type, audience, style and usage constraints matter. The Council then returns correct but dense structures whose verdict is easier to notice than the different professional perspectives that created value. Campaign 003 makes the process—not speed or the final answer—the primary experience.

### Product principle

The primary Council output is a structured expansion of the user's decision frame:

1. what the Council understood;
2. which assumptions it had to make;
3. what the user may not have considered;
4. what each professional lens noticed and why it matters;
5. where genuine consensus and disagreement exist;
6. which missing context could change the result;
7. how user input changed role positions;
8. the chief editor's synthesis and execution checklist, last.

The server exposes structured claims, evidence, questions, positions and changes. It must never request, persist or display hidden chain-of-thought.

### Guided session state machine

```text
RECEIVED
  -> NORMALIZED
  -> BRIEFING_SKIPPED | BRIEFING_REQUESTED
  -> BRIEFING_ACCEPTED | BRIEFING_DECLINED | BRIEFING_CANCELLED
     | BRIEFING_UNSUPPORTED | BRIEFING_MALFORMED
  -> BRIEF_CONFIRMED
  -> PREFLIGHTED
  -> PLANNED
  -> INDEPENDENT_REVIEWED
  -> BLIND_SPOTS_MAPPED
  -> CONTEXT_GAPS_READY | NO_CONTEXT_GAP_NEEDED
  -> CONTEXT_UPDATED | CONTEXT_GAP_DECLINED | CONTEXT_GAP_UNSUPPORTED
  -> CONTEXT_RECONSIDERED | CONTEXT_RECONSIDERATION_SKIPPED
  -> DISCUSSED | DISCUSSION_SKIPPED
  -> DECISION_POINTS_READY | NO_USER_DECISION_NEEDED
  -> USER_DECIDED | USER_DELEGATED | USER_DECLINED | USER_CANCELLED
     | INTERACTION_UNSUPPORTED | RETURNED_PENDING
  -> OUTCOME_RECONSIDERED | OUTCOME_RECONSIDERATION_SKIPPED
  -> POLICY_GATED
  -> ADJUDICATED
  -> PROCESS_DIGESTED
  -> COMPLETED | COMPLETED_WITH_FALLBACK | NEEDS_HUMAN_REVIEW
```

Briefing happens before reviewer sampling. At most one adaptive context-gap form may happen after independent review. The existing outcome decision form remains a separate checkpoint because new context can invalidate or reshape prior options.

### Pre-review Briefing Gate

`review_translation` adds `briefing_mode` with `auto` as the default and `always` / `off` as explicit alternatives. No new public tool is added.

`auto` requests a brief only when caller context is materially sparse. A normal source/target-only call is sparse. A call with a recognized content type plus useful audience/context/style/rule material skips redundant questions. The sufficiency rule is deterministic and tested; it does not spend a model call.

One flat MCP form collects no more than six primitive fields:

- domain;
- content location/type;
- audience;
- tone or communication goal;
- primary review focus;
- bounded usage context.

Every categorical field includes a concise `不确定，由 Council 推断` value. User briefing answers may replace defaults and inference, but cannot erase caller hard constraints, TB/SG authority or deterministic preflight facts. Field-level provenance distinguishes caller, user briefing, normalized alias and inferred assumption.

Declined, cancelled, unsupported and malformed briefing responses remain distinct. In `auto`, the review may continue with explicit assumptions and context confidence. In `always`, absence of an accepted brief stops before reviewer sampling with a truthful pre-review disposition. No path may fabricate user answers.

### Context normalization

Common caller phrases such as `UI button`, `button`, `error message`, `onboarding`, `subtitle`, `marketing copy`, `technical docs` and their normalized variants map predictably to supported content types or locations. Unknown values remain visible as assumptions rather than silently becoming an unexplained `unspecified` plan.

Precedence is frozen:

1. deterministic hard constraints and explicit caller rule packets;
2. accepted user briefing updates for mutable context/preferences;
3. explicit caller context fields;
4. normalized aliases;
5. bounded Council inference.

The effective brief is included in reviewer prompts, persisted under full history, and projected safely under metadata history without user free text.

### Adaptive material context gaps

Independent reviewer envelopes may add optional structured context gaps. A gap contains a bounded question, why the answer can change an outcome or professional judgment, affected role IDs, and safe answer guidance. It is advisory model evidence: it cannot create a hard constraint, blocker or policy override.

The Core deduplicates gaps and selects at most two using deterministic materiality and role-relevance rules. It elicits at most one flat follow-up form. Generic curiosity, repeated questions, questions already answered by the brief, and questions that cannot change any valid outcome are suppressed.

Accepted answers trigger only affected-role context reconsideration. Requested, completed, skipped and failed roles are separate from outcome reconsideration provenance. If the user declines or the client cannot elicit, the Council continues with explicit assumptions unless an existing integrity rule requires human review.

### Concise interaction information architecture

All three form families—briefing, context gap and outcome decision—share bounded presentation rules:

- flat primitive schemas only;
- at most six briefing fields, two context-gap fields and three outcome questions;
- deterministic titles, target maximum 48 Unicode code points;
- descriptions, target maximum 160 Unicode code points;
- no title repeated inside its description;
- no internal IDs, hashes, full reviewer prose or action instructions in user-facing values;
- one submit action per batched form is expected Goose behavior.

Decision titles derive from bounded source/candidate anchors and normalized issue category, for example `向导按钮译法` or `“Continue”按钮的处理方式`. They must not reuse an unbounded reviewer `problem` sentence as the title.

### Process-first digest

The default compact response adds a structured `process_digest` and a bounded `display_report`. The order is frozen:

1. `case_brief`;
2. `assumptions` and `context_confidence`;
3. `blind_spots`;
4. `role_lenses`;
5. `consensus`;
6. `minority_report`;
7. `material_disagreements`;
8. `context_gaps` and answers;
9. `user_decisions`;
10. `reconsideration_changes`;
11. `editor_synthesis`;
12. `execution_checklist` and final disposition.

The digest preserves all six distinct role lenses when they contain material non-duplicate information. It compresses repeated prose by normalized issue/evidence target, not by erasing minority views. A minority report states the strongest valid dissent and the condition under which it would become decisive. Blind spots and counterfactual conditions precede the verdict.

The Markdown `display_report` is derived deterministically from the structured digest and is safe for an outer agent to show directly. It remains review-only and must not contain a full replacement translation unless `output_mode=full_rewrite` was explicitly requested. Full raw reviewer records remain available through `view_review_record`.

### V2.2 records and phase trace

New V2.2 records add typed sections for:

- effective review brief and field provenance;
- briefing interaction and assumptions;
- structured context gaps and answers;
- context reconsideration provenance;
- phase trace and phase-specific telemetry;
- process-first digest.

Phase telemetry distinguishes briefing elicitation, context-gap elicitation and outcome elicitation. Metadata persistence retains only safe categorical/disposition/count fields and excludes source, target, form free text, user answers, role prose and derived display prose. V1, V2.0 and V2.1 remain readable.

### Sampling and interaction budgets

- lightweight: maximum 6 sampling calls;
- standard: maximum 13 sampling calls;
- strict: maximum 18 sampling calls;
- briefing forms consume no sampling calls;
- maximum one context-gap form with two questions;
- maximum one bounded discussion round;
- maximum one outcome form with three DecisionPoints;
- context and outcome reconsideration each target only materially affected roles;
- insufficient budget or failed required reconsideration is explicit and cannot report clean completion.

The standard deep reference path is six independent reviews, up to three context-affected role calls, one discussion call and up to three outcome-affected role calls: 13 total. Ordinary reviews need not consume the maximum.

### Campaign 003 package graph

1. `PKG-017` — V2.2 briefing/context-gap/process-digest models, compatibility and privacy-safe persistence.
2. `PKG-018` — deterministic context sufficiency, aliases, Briefing Gate, form mapping and field provenance.
3. `PKG-019` — reviewer context-gap contract, materiality aggregation, one follow-up form, affected-role context reconsideration and 6/13/18 accounting.
4. `PKG-020` — shared concise form information architecture and deterministic issue titles.
5. `PKG-021` — process-first digest, minority report, blind spots, phase trace and bounded display report.
6. `PKG-022` — V0.6 migration, full regression/evaluation corpus, exact identifiers, fresh packaging and authoritative documentation.

Packages execute in dependency order under one Strict Campaign. `models.py`, `orchestration.py`, `runtime.py` and `tools/review.py` are integration hotspots owned by the Main Worker. Subagents may receive only bounded non-overlapping packages or read-only assignments; they never own acceptance.

### Campaign 003 quality gates

1. A source/target-only normal Goose path requests a concise pre-review brief before the first sample.
2. Rich caller context skips redundant briefing in `auto`; `always` and `off` behave deterministically.
3. Briefing accept/decline/cancel/unsupported/malformed paths preserve truthful provenance and never fabricate user fields.
4. `UI button` and equivalent aliases route to `ui`; unknown values remain visible assumptions.
5. At most two material non-duplicate context gaps are elicited once; immaterial or answered questions are suppressed.
6. Context answers reconsider only affected roles and cannot become model-authored hard constraints.
7. Outcome decisions retain V0.5 user authority, Policy Gate behavior, delegation semantics and stable option mapping.
8. Briefing/context/decision titles and descriptions meet bounds and do not repeat reviewer prose or expose internal identifiers.
9. Process digest places blind spots, role lenses, minority report and disagreements before final synthesis; repeated content is semantically deduplicated.
10. Display report is bounded, review-only and contains no hidden reasoning or unauthorized full translation.
11. Full/metadata/off persistence preserves privacy; V1/V2.0/V2.1 records remain readable and new records write schema 2.2.
12. Lightweight/standard/strict never exceed 6/13/18; deep standard reference flow completes within 13 and insufficient paths degrade truthfully.
13. All 159 accepted V0.5 tests plus focused V0.6 regressions pass.
14. Exact five tools, defaults, package/module `0.6.0`, build `guided-deliberation-v4`, schema `2.2`, review-only boundary and fresh sdist/wheel smoke pass.
15. Pinned Goose recipes cover source/target-only briefing, optional material context follow-up, user selection and process-first output; Worker live calls remain optional and disclosed.

### V0.6 non-goals

- Custom MCP Apps, bespoke Goose widgets, control over Goose button/layout rendering or multiple submit buttons per form.
- General-purpose or dynamically invented Councils.
- Automatic translation application, file edits or translation memory ownership.
- Per-role provider/model routing.
- Majority voting or raw role-count authority.
- Unlimited questions, debate rounds, context reconsideration or outcome reconsideration.
- Persisting or displaying hidden chain-of-thought.
- Migrating this repository to an unreleased MCP SDK generation before current Goose compatibility is preserved by the runtime abstraction.
