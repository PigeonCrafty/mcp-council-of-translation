# Council of Translation V0.10 Harness Plan

## Control

- Harness mode: `STRICT_CAMPAIGN`
- Foreman: Codex
- Main Worker: Codex Main Worker in a separate new conversation
- Active Campaign: `CAMPAIGN-009-r2` (`ACCEPTED / PUBLISHED`)
- Source baseline: `62f2ee9bf1860f80281afbbad53734db5f700205`
- Product target: `0.10.1`
- Diagnostic build target: `evidence-value-council-v8.1`
- Acceptance authority: Foreman only

Repository artifacts are the source of truth. Conversation summaries do not override this plan, `features.json`, `progress.md`, or the active Campaign contract.

CAMPAIGN-009-r1 reached the intended Q-012 A/B outcome but independent Foreman review
found two bounded counterexamples: an already-present typed rule reference can be counted
as new discussion evidence, and a corroborated material disagreement can be replaced by
an unintelligible anchor-only summary. CAMPAIGN-009-r2 corrects only those boundaries;
the V0.10.1 migration, Golden evidence, full-record preservation and A/B improvements are
retained.

CAMPAIGN-009-r2 is accepted at
`4a3c692ad528db03e4f72a025d60c4eb775454f0`. Typed rule/constraint provenance now
canonicalizes before novelty comparison, and grouped corroboration states the material
topic once before suppressing repetition. Independent Foreman evidence includes 286 full
passes, 50 focused passes, exact counterexamples, preserved A/B behavior and frozen
version/tool/schema/budget invariants. Publication and normal-Goose Q-012 revalidation
remain separate gates.

The Foreman and Main Worker are separate Codex conversations. The Worker must bootstrap exclusively from repository assets and must not assume access to the Foreman's conversation context.

The V0.4, V0.5 and Campaign 003 sections below are accepted architectural history. `Campaign 004: Concise Primary Council Presentation` is the authoritative delta for the active V0.7 target.

`CAMPAIGN-003-r1` produced the integrated V0.6 implementation and preserved evidence for all but one PKG-018 boundary. `CAMPAIGN-003-r2` corrected that boundary: auto-mode context is sufficient only when content type is recognized **and** at least two independent context categories are present. Independent review accepted the combined Campaign 003 implementation. Live Goose gates Q-008 and Q-009 remain separate post-publication validation.

Published V0.6 live evidence accepted Q-008 but returned a diagnostic checklist instead of the Council process until the user explicitly requested `display_report`. Campaign 004 is the authoritative V0.7 delta: make a short, readable Council process the primary MCP content while preserving full structured evidence separately.

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

## Campaign 004: Concise Primary Council Presentation

### Live counterexample

Published V0.6 record `20260812T113302675410Z_611c7d32146e` contains a complete six-role process and 12-part digest. Normal Goose nevertheless answered with version fields, call counts and schema checks because the tool exposed one large dictionary and left the outer agent to choose what mattered. A second explicit retrieval prompt showed the process, but it was long, repetitive, mixed English/internal labels with Chinese prose, and reported no consensus despite six affirmative role findings.

Campaign 004 treats this as a presentation-contract defect, not a missing-review defect. The Council must remain structurally rich while its default human surface becomes short, layered and difficult for an outer agent to overlook.

### Dual-channel MCP result

FastMCP 2.13 supports a tool result containing both primary content blocks and structured content. V0.7 uses that protocol shape:

```text
MCP result
  content[0].text       = concise user-facing Council Markdown
  structuredContent    = existing compact or full structured dictionary
```

`review_translation`, `continue_review` and `view_review_record` use this dual channel. `get_server_info` and `list_review_records` remain structured utilities. No sixth tool or new public mode argument is added.

Primary text is the normal human answer. Structured content preserves review ID, status, effective task, digest, runtime facts, warnings and retrieval fields for agents and automation. Tool/server descriptions explicitly instruct normal callers to show the primary Council text before optional diagnostics, but correctness never depends only on prompt wording.

### Adaptive human report

The persisted 12-field `process_digest` remains the machine-readable source. The default `display_report` no longer mirrors all 12 fields mechanically. It renders at most five Chinese sections:

1. `审校背景` — language, content/use, audience, confidence and only material assumptions;
2. `专业视角` — one short distinct line for every active role;
3. `共识、分歧与盲区` — positive consensus, material disagreement, minority condition, unanswered gaps or coverage limits;
4. `你的决定与复议` — included only when a user decision, delegation, context answer or position change actually occurred;
5. `主编结论` — publishability, human-review need and a short action checklist, always last.

Clean/simple reports target 1,800 Unicode code points. Every default report is capped at 3,200. Each role lens targets 120 characters; optional evidence anchors target 80. The renderer uses shallow bullets, Chinese labels and no internal role IDs. Empty/no-op sections are omitted rather than producing repeated `未触发` paragraphs. A material blocker, minority, unanswered gap, unavailable role, warning or degradation may never be omitted to satisfy a length target.

### Role-lens compression

Every active reviewer remains visible because the product value is the professional frame, not merely the verdict. Deterministic compression selects the most material role-specific signal in this order:

1. critical/major issue or hard/preflight evidence relevant to the role;
2. concrete choice or materially distinct condition;
3. strongest bounded affirmation/evidence;
4. truthful unavailable-role notice.

Repeated generic praise is shortened, but role ownership is preserved. The renderer must not use a new model call, invent missing evidence, or substitute a generic MQM label for the role's actual perspective.

### Truthful positive consensus

Consensus is not limited to issue clusters. Structured successful affirmations and clean role feedback may establish a positive statement such as `六个专业视角均未发现阻碍发布的问题；共同支持保留“继续”`. This is coverage/evidence synthesis, not majority voting and not a Policy Gate input.

The renderer must distinguish:

- positive consensus;
- no material issue but insufficient evidence for a shared semantic claim;
- genuine disagreement;
- unavailable or partial coverage.

It must never display `未形成实质共识` merely because affirmations were excluded from issue clustering when the role evidence clearly shares a conclusion.

### Presentation integrity

- Preserve review-only: no full replacement translation in default content.
- Hide hashes, option/decision IDs, internal role IDs, raw action prose, schema/build metadata and Policy Gate counters from primary text.
- Keep warnings, degradation, fallback, coverage gaps and human-review requirements visible in plain language.
- Use unique sentinel tests to prove briefing `tone_goal` and `primary_focus` labels round-trip to the correct stored fields.
- Preserve the true phase order; do not ask the outer agent to reconstruct chronology from prose.
- Full `view_review_record` structured content remains complete; its primary text stays concise unless the caller explicitly asks the outer agent to enumerate raw evidence.

### Version and compatibility

- Package/module: `0.7.0`.
- Diagnostic build: `concise-council-display-v5`.
- Record schema remains `2.2`; no persistence migration is justified by presentation-only changes.
- Exact five tools and all V0.6 inputs/defaults remain.
- Sampling budgets remain 6/13/18; presentation uses zero model samples.
- Fresh installed-wheel tests must cover the locked FastMCP 2.13 behavior and the currently resolved FastMCP release behavior.

### Campaign 004 package graph

1. `PKG-023` — dual-channel primary MCP text plus structured content for review, continuation and record viewing.
2. `PKG-024` — adaptive five-section Chinese report, conditional sections and 1,800/3,200 character budgets.
3. `PKG-025` — positive consensus synthesis and concise distinct six-role lenses.
4. `PKG-026` — presentation integrity, briefing field round-trip, errors/degradation/privacy and layered retrieval regressions.
5. `PKG-027` — V0.7 identifiers, dual-version FastMCP packaging smoke, documentation and normal-user Goose recipe.

Packages execute in dependency order. `digest.py`, `orchestration.py` and `tools/review.py` are integration hotspots owned by the Main Worker. Subagents may work only on disjoint tests/docs after the output interface is frozen.

### Campaign 004 quality gates

1. A normal tool call exposes the concise Markdown as `content[0].text` and the complete dictionary as structured content.
2. Review, continuation and record-view tools share the same presentation adapter without changing the five-tool set.
3. Clean six-role output is readable in five or fewer Chinese sections, targets 1,800 characters and never exceeds 3,200.
4. Every active role retains one distinct practical lens; repetitive praise is compressed.
5. Six affirmative roles produce truthful positive consensus rather than `未形成需合并的实质共识项`.
6. Material minority, disagreement, blockers, gaps, warnings, degraded execution and unavailable coverage remain visible.
7. Empty decision/context/reconsideration sections do not consume separate headings.
8. Final disposition and action checklist appear last; internal telemetry and identifiers do not appear in primary text.
9. `tone_goal` and `primary_focus` round-trip independently through real form schemas and Core persistence.
10. Compact/full/metadata/off history, review-only, user authority, Policy Gate, V1/V2.0/V2.1 reads and V2.2 writes remain green.
11. No presentation path adds sampling calls or exceeds 6/13/18.
12. Exact five tools, package/module 0.7.0, build `concise-council-display-v5`, schema 2.2 and defaults pass in source and fresh wheel.
13. All 184 accepted V0.6 tests plus focused V0.7 regressions pass without weakening useful assertions.
14. A normal-user Goose recipe asks for review rather than diagnostics and defines Q-009 evidence: primary process visible in the first answer, concise role lenses, truthful consensus and verdict last.

### Campaign 004 r1 review and bounded correction

Independent Foreman review of r1 is `CHANGES_REQUESTED` in
`harness/evaluations/CAMPAIGN-004-r1-review.md`. The dual-channel transport,
adaptive report, role lenses, positive consensus, field mapping, limits, public
diagnostics and dual-FastMCP package behavior are preserved evidence. Two deterministic
defects remain:

1. metadata-only history projection still writes V0.6 package/build identifiers for
   newly produced V0.7 records;
2. primary-text sanitization filters only some lowercase internal identifier families,
   so cluster/position and case variants can remain visible.

`CAMPAIGN-004-r2` is a two-surface correction. It may update the metadata projection,
the primary-text sanitizer, focused regressions and strictly necessary documentation.
It must not redesign the report, change the five-tool surface, schema, budgets,
adjudication, reviewer behavior, persistence privacy allowlist or legacy records.

### Campaign 004 acceptance

`CAMPAIGN-004-r2` is accepted by
`harness/evaluations/CAMPAIGN-004-r2-review.md` at
`3779a78a9788018082470408fdd4d87a042985dc`. F-023 through F-027 are accepted.
Independent final evidence includes 198 full passes, 27 focused passes, compile and
scope checks, truthful V0.7 metadata projection, zero standalone internal IDs in the
primary report, exact five-tool diagnostics and preserved FastMCP 2.13/3.4.7 evidence.

Q-009 remains a separate live Goose usability gate. Repository acceptance does not
claim that Goose has already rendered the new primary Council text correctly.

## Campaign 005: Natural Primary Council Microcopy

### Live counterexample and scope

Published V0.7 live record `20260812T131614836886Z_e815e1cbf65f` proves that the
first normal Goose answer now exposes the Council process directly in four concise
Chinese sections with all six roles, truthful positive consensus and the verdict last.
The remaining defect is presentation polish, not review logic: the chief section still
shows procedural decision counters, while clean affirmative lenses attach repetitive
evidence containing implementation vocabulary and several mid-clause ellipses.

The sanitized evidence and independent correction of Goose's erroneous
`sampling_calls=0` summary are in
`harness/evaluations/CAMPAIGN-004-q009-live-review.md`. The persisted truth is six
successful samples within the 13-call standard budget.

### Frozen presentation rules

1. The primary report must omit the canonical procedural chief rationale containing
   Policy Gate/Council-fallback/user-choice/human-review counters. The complete
   `editor_synthesis`, chief decision and trace remain unchanged in structured content.
2. A clean affirmation or clean no-finding role lens shows one role-specific perspective
   without an evidence suffix. Evidence remains structured and retrievable.
3. Primary evidence remains visible when it is material to a blocker, major issue,
   concrete outcome choice, minority condition or coverage/unavailability warning.
4. Optional evidence is included only when it forms a complete bounded clause. If it
   cannot fit safely, omit the optional suffix rather than render a mid-token or
   mid-clause ellipsis.
5. Map established implementation vocabulary such as `Preflight`,
   `placeholder_parity`, `tag_integrity`, `Effective Brief`, standalone `Context`,
   `Policy Gate` and `Position Matrix` to natural Chinese when it reaches primary text.
   Internal IDs and hidden reasoning remain prohibited.
6. Keep the current adaptive section order, clean 1,800 target, absolute 3,200 cap, six
   role ownership, truthful consensus, material-risk visibility and verdict-last rule.
7. Do not change Council planning, reviewer prompts, sampling, elicitation,
   reconsideration, Policy Gate, user authority, persistence schema or structured
   evidence.

### Patch identity and package graph

- Package/module target: `0.7.1`.
- Diagnostic build target: `concise-council-display-v5.1`.
- Schema remains `2.2`; public tools remain five; budgets remain 6/13/18.
- `PKG-030`: primary microcopy filtering, conditional evidence and natural terminology.
- `PKG-031`: V0.7.1 identifiers, live-shaped regression, docs, fresh build and pinned
  Goose revalidation recipe.

### Acceptance gates

1. The exact live-shaped clean fixture contains no procedural decision counts,
   `Council fallback`, `Preflight`, `placeholder_parity`, `tag_integrity`,
   `Effective Brief` or standalone `Context` in primary text.
2. Its six roles each appear once, positive consensus and final disposition remain, no
   interaction section is invented, and clean output stays below 1,800 code points.
3. A disputed/blocking fixture preserves actionable evidence, minority condition,
   degradation/human-review meaning and the final disposition.
4. No optional evidence ends with a truncation ellipsis caused by the presentation
   budget; long optional evidence is omitted as a unit.
5. Structured compact/full content, including chief rationale and original role
   evidence, is byte-for-byte semantically preserved apart from version metadata.
6. Sampling stays unchanged, exact five tools/schema/defaults/budgets pass, all prior
   regressions remain green, and fresh 0.7.1 artifacts smoke successfully.

### Non-goals

- New tools, arguments, display modes, widgets or Goose-specific UI.
- Changing role prompts, evidence generation, adjudication or sampling budgets.
- Removing evidence from structured content or rewriting historical records.
- Broad copy editing outside the primary deterministic renderer.

### Campaign 005 acceptance

`CAMPAIGN-005-r1` is accepted by
`harness/evaluations/CAMPAIGN-005-r1-review.md` at
`c8616eb66b49de4be00672e6439ad6b1ea468967`. F-028 and F-029 are accepted.
Independent evidence includes 203 full passes, 42 focused passes, compile and scope
checks, a 539-code-point live-shaped clean report, unchanged structured chief/role
evidence, fresh 0.7.1 artifacts and an isolated FastMCP 3.4.7 registered-tool smoke.

Q-009 remains a separate post-publication Goose gate. Repository acceptance does not
claim that the published build has already passed the normal-user live revalidation.

Campaign 005 was published through protected-main PR #8 at
`e2e2ba34dc890591a66d60b86e1373eb0316e80b`. Rebase publication maps the accepted
local implementation/acceptance tree to remote commits `2580536`, `f34073f` and
`e2e2ba3`; the published tree is byte-for-byte identical to accepted local commit
`cf375be`. All six required Windows/Linux Python checks passed.

### V0.7 non-goals

- Custom MCP App/widget or control over Goose's visual layout.
- A new presentation mode argument, sixth tool or separate `show_report` tool.
- Removing structured fields needed by automation or full audit.
- Hiding material evidence merely to meet a preferred length.
- Additional model summarization calls, streaming hidden reasoning or raw chain-of-thought.
- Changing review logic, roles, Policy Gate, user authority, budgets, persistence schema or translation-application boundary.

## Campaign 006: Context-Coherent Panoramic Council

`CAMPAIGN-006-r1` was published as Foreman history through PR #10, which advanced
protected `main` after its baseline was written. Its product design remains unchanged,
but its exact admission baseline is no longer the shared-worktree HEAD. It is superseded
by `CAMPAIGN-006-r2`, which changed only the reachable baseline and versioned report/
ledger paths. That correction has now been executed; r1 remains immutable history and
r3 is the only active contract.

`CAMPAIGN-006-r2` implemented the full V0.8 package graph and passed independent compile,
217-test, routing, precedence, presentation and tool/version checks. Foreman review found
one bounded direct-answer gap: a caller-supplied binding glossary/reference, or an
unambiguous caller statement that the text is a brand slogan or functional UI element,
is not visible to the current `already_answered` classifier and can trigger a redundant
follow-up. `CAMPAIGN-006-r3` preserves every other r2 behavior and corrects only that
caller-context recognition path.

Campaign 006 is accepted by `harness/evaluations/CAMPAIGN-006-r3-review.md` at
`f3e9bde1b74ff4591d91b66a38558b8bebe6efab`. Independent final evidence includes the
exact four-file r3 correction scope, 39 focused passes, 220 full passes, the direct-answer
positive/negative truth table, exact six-role marketing routing, five-tool/version/schema/
budget probes and preserved r2 artifacts/current-FastMCP wheel smoke. Publication and
live Q-010 validation remain separate from repository acceptance.

Publication completed through protected-main PR #11. All six Windows/Linux Python
checks passed, and remote commit `1f8e6981b9fdef08f42a35fc52c7a216b123a94a`
has the same Git tree (`f832035855fd60ff7f3bf0b0dea4caf17d4df877`) as local
accepted archive commit `91b71d7b980a2933e5a98840dc46af4ae37273e5`. The
accepted implementation commit `f3e9bde1b74ff4591d91b66a38558b8bebe6efab` maps to
published rebase commit `fbe0eb1de63b6d26b4ffbf96e5e05b76fe4b86f8`. Q-010 is
the only remaining Campaign 006 gate.

The first Q-010 live round is reviewed in
`harness/evaluations/CAMPAIGN-006-q010-live-review.md`. The clean marketing run accepts
Q-009 and proves the intended six-lens first-response experience. The mixed run proves
material-gap detection but not the unresolved branch: Goose submitted non-assumption
answers copied from caller context despite the instruction to pause, then reconstructed
impossible role/status/coverage fields. Q-010 therefore has partial live evidence and
requires one `interactive_mode=off` revalidation with literal full-record JSON.

The `interactive_mode=off` revalidation is reviewed in
`harness/evaluations/CAMPAIGN-006-q010-r2-live-review.md` and accepts Q-010. Its primary
Goose report visibly lowered context confidence, retained two unanswered material blind
spots, omitted user outcomes, required confirmation before adjudication and ended in
human review. Goose exposed only the Markdown channel to its outer model even though the
server returns the unchanged record in FastMCP `structured_content`; invalid prose
reconstructions are rejected rather than treated as raw telemetry. Campaign 006 is
closed. Bounded concurrent independent sampling is a separate future latency opportunity,
not an unresolved Campaign 006 defect.

### Live counterexample and evidence boundary

The published V0.7.1 presentation correction reached normal Goose: the first answer for
`bigger than bigger` → `比大更大` exposed the Council process directly, omitted internal
telemetry and kept material dissent plus the verdict visible. The run also combined a
marketing brief with the retained UI-button context, which exposed deeper orchestration
gaps recorded in `harness/evaluations/CAMPAIGN-005-q009-live-review.md`.

The follow-up Goose audit is not raw telemetry evidence. It reported values that violate
the current schema and registry (`reviewer_coverage=1.0`, `not_sampled`, obsolete role
IDs and zero calls despite sampling/elicitation effects). Campaign 006 must test literal
record dictionaries and must not add duplicate diagnostics merely to compensate for an
outer agent's prose reconstruction.

### Frozen V0.8 decisions

1. Standard marketing uses six relevant perspectives in deterministic order:
   fidelity, terminology, product context, brand voice, risk/ambiguity and fluency.
   Lightweight remains intentionally narrow; strict contains every standard marketing
   lens. Technical and UX roles are not added to marketing merely to reach a count.
2. Context comes before wording. A question distinguishing brand slogan from functional
   UI copy, or asking whether an official/binding slogan glossary applies, is material
   because it can change role routing, option validity or the final disposition.
3. Context-gap selection remains bounded to two questions and sampling-neutral. It may
   use a small deterministic impact grammar across question plus materiality, but cannot
   turn model prose into a hard rule or blocker.
4. Direct already-answered questions may be suppressed; compound alternatives are not
   considered answered merely because some usage-context text exists. Duplicate,
   generic, immaterial and question-limit provenance remains explicit.
5. Selected context questions are elicited and actually answered before affected-role
   reconsideration, discussion and outcome selection. The explicit assumption value,
   decline, cancel, unsupported, malformed or error actions leave material context
   unresolved.
6. Unresolved material context lowers `context_confidence`, prevents outcome elicitation
   in that run and conservatively yields `NEEDS_HUMAN_REVIEW` with bounded warning and
   fallback provenance. A real answer may continue through reconsideration and valid
   user authority.
7. Suppressed immaterial questions do not appear as user decisions. Unresolved material
   questions appear as blind spots or required confirmation. Primary issue labels are
   natural Chinese and renderer punctuation must not produce `。；依据`.
8. Runtime metadata, review statuses, role IDs and coverage remain the existing V2.2
   source of truth. Add invariant tests, not a duplicate fact sheet, new tool or new
   telemetry field.
9. Package/module target is `0.8.0`; diagnostic build is
   `context-coherent-council-v6`. Record schema remains `2.2`; old V1/V2 records remain
   readable. Public tools remain exactly five and budgets remain 6/13/18.
10. Preserve review-only, briefing/outcome forms, Policy Gate, user authority, bounded
    discussion, persistence privacy, concise primary presentation and full structured
    evidence.

### Package graph

1. `PKG-032` — reproduce the live marketing/mixed-context counterexamples and harden
   context-gap impact classification without a schema change.
2. `PKG-033` — enforce material-context precedence, confidence/status truth and bounded
   context reconsideration before outcomes.
3. `PKG-034` — expand standard/strict marketing to the frozen six relevant roles within
   the unchanged budgets.
4. `PKG-035` — correct context-first primary presentation, issue-label localization,
   punctuation and record-invariant regressions.
5. `PKG-036` — migrate to V0.8 identifiers, documentation, fresh artifacts, installed
   wheel verification and two pinned live recipes.

Packages execute in order because guided selection, orchestration, role routing and the
digest share behavior. The Main Worker owns all production integration; implementation
subagents are forbidden for this tightly coupled correction.

### Acceptance gates

1. A standard marketing plan contains exactly the six frozen relevant role IDs and six
   role lenses; lightweight remains bounded and strict is a superset.
2. The sanitized live-shaped brand-versus-UI and official-glossary gaps are selected,
   asked before any outcome form and reconsider only affected active roles after actual
   answers.
3. Decline, unsupported, malformed, cancelled, error and explicit assumption answers do
   not trigger an outcome form; each produces truthful unresolved-context provenance,
   lowered confidence, `NEEDS_HUMAN_REVIEW` and visible required confirmation.
4. Actual answers can lead to a valid outcome choice and clean completion when no other
   blocker, coverage loss or degraded work remains.
5. No suppressed immaterial question is rendered as a completed decision; no raw `ux`
   issue label or `。；依据` appears; verdict remains last and primary text stays within
   the accepted 3,200 cap.
6. New raw records use only registered role IDs, valid sample-status/coverage literals
   and call counts consistent with executed samples/interactions. Structured evidence is
   not removed or duplicated.
7. Exact five tools, schema 2.2, review-only/defaults and 6/13/18 pass in source and a
   fresh installed 0.8.0 wheel; all 203 baseline tests plus new regressions pass.
8. Documentation distinguishes literal record evidence from outer-agent prose and
   supplies clean-marketing and deliberately mixed-context live recipes.

### Non-goals

- General semantic contradiction detection over arbitrary prose.
- An extra LLM call for briefing classification or presentation.
- A new schema field, telemetry projection, diagnostic tool, custom Goose widget or
  change to Goose itself.
- Restoring literal majority voting, weakening valid user authority or allowing context
  answers to create deterministic hard constraints.
- Broad role redesign outside the bounded standard/strict marketing route.

## Campaign 007: Bounded Parallel Independent Review

### Why this Campaign exists

Live V0.8 evidence showed that the off-mode six-role path took 15.31 seconds and the
answered mixed path required at least eight model calls. Local aggregation and history
reads are small; the dominant latency is the sum of sequential provider round trips.
The six initial role reviews share the same frozen task, brief and preflight and do not
depend on one another, so that single phase can safely use bounded concurrency without
turning the Council into a faster but less coherent pipeline.

### Frozen design

1. Only independent role review may overlap. Briefing finishes before the batch;
   context-gap handling, affected-role reconsideration, discussion, outcome interaction,
   outcome reconsideration, Policy Gate and adjudication remain sequential phase
   boundaries.
2. The default independent-review concurrency is three. Operators may set
   `COUNCIL_REVIEW_CONCURRENCY` to `1`, `2` or `3`; missing configuration uses three and
   invalid or out-of-range configuration conservatively uses one. This is an operator
   control, not a new normal MCP tool or user-facing decision.
3. The batch reserves its full role-call budget before starting any provider request.
   Calls are attempted exactly once. There is no automatic sequential replay after a
   concurrency error because replay could duplicate cost, exceed budget or obscure
   provider behavior.
4. Each result remains correlated to its role and is emitted in deterministic
   `CouncilPlan.active_role_ids` order even when requests finish out of order. A single
   error is normalized as that role's unavailable sample and cannot cancel siblings.
5. Concurrency never changes role routing, prompts, token caps, context selection,
   deliberation, user authority, Policy Gate, presentation, persistence privacy or the
   6/13/18 call budgets.
6. Runtime records distinguish end-to-end wall-clock duration from accumulated provider
   wait and record the effective independent-review limit, actual peak concurrency and
   batch count. Telemetry is bounded and content-free. Existing `elapsed_ms` remains
   readable and is not silently reinterpreted.
7. New records use schema `2.3`; V1 and V2.0 through V2.2 remain readable with safe
   defaults for new telemetry. Package/module become `0.9.0`; build becomes
   `bounded-parallel-council-v7`.
8. The public tool count remains exactly five, the primary report stays concise and
   review-only, and standard marketing retains the exact six accepted V0.8 lenses.

### Package graph

1. `PKG-037` — deterministic bounded sampling batch and configuration parser.
2. `PKG-038` — independent-review orchestration integration, budget reservation,
   stable ordering and failure isolation.
3. `PKG-039` — V2.3 concurrency/wall-clock telemetry and backward-compatible record
   parsing/persistence.
4. `PKG-040` — FastMCP/server diagnostics, sequential override and phase-order
   integration evidence.
5. `PKG-041` — V0.9 metadata, documentation, artifacts and installed-wheel smoke.

Packages are sequential because runtime, orchestration, metadata and compatibility
interfaces overlap. The Main Worker must not delegate implementation subagents in the
shared worktree. Q-011 remains a post-publication Foreman live gate: the same standard
six-role Goose case will be compared with effective limits one and three, requiring full
coverage and no protocol failure before latency improvement is accepted.

CAMPAIGN-007-r1 delivered the bounded scheduler, independent-review integration, V2.3
schema/compatibility, diagnostics and V0.9 artifacts. Foreman review preserved that
evidence but requested one bounded correction: continuation children had recorded
`wall_clock_ms=0` despite reconsideration sampling and reset retained independent-review
concurrency provenance to `legacy`; normal records had also captured wall time before final
digest/display construction. CAMPAIGN-007-r2 corrects only truthful record-finalization
telemetry and must not redesign the accepted concurrent path.

CAMPAIGN-007-r2 is accepted by
`harness/evaluations/CAMPAIGN-007-r2-review.md` at
`e835566a2c8d60ba153b68175d19685cb96185fe`. Fresh Foreman evidence includes the three
corrected timing counterexamples, 83 focused passes, 246 full passes, compile, exact
four-path correction scope, protected hashes and fresh artifacts. Combined r1+r2
evidence accepts F-035 through F-039. Publication and Q-011 remain separate: live Goose
must compare effective limits one and three because the isolated in-memory FastMCP
callback serialized sampling callbacks and cannot prove provider overlap.

Publication PR #15 exposed a packaging-only admission defect: the accepted V0.9 source
metadata was not propagated to the root project entry in `uv.lock`, so every CI matrix
job stops at `uv sync --locked --group dev` before compile or tests. This does not reopen
F-035 through F-039. CAMPAIGN-007-r3 is a strict lockfile-only correction; it may update
the root package version from 0.8.0 to 0.9.0 but must stop on any dependency graph drift.

CAMPAIGN-007-r3 stopped correctly because the locally installed uv 0.6.13 rewrote the
newer revision-3 lock format. Foreman isolation proved the CI-pinned uv 0.12.3 changes
only the editable root version. CAMPAIGN-007-r4 therefore freezes uv 0.12.3 plus
repository-local cache and tool directories; lock-generation contracts must pin the
same generator used by CI instead of relying on an ambient `uv` executable.

CAMPAIGN-007-r4 exposed the remaining incremental-lock rule: plain uv 0.12.3 preserves
a semantically current revision-1 lock and does not reconstruct discarded artifact
metadata. Foreman proved that pinned `uv lock --refresh` deterministically restores
revision 3 and all 586 upload-time entries, keeps all 78 resolved packages unchanged,
and yields the exact expected V0.9 lock with only the editable-root version diff.
CAMPAIGN-007-r5 authorizes that exact refresh and freezes its expected SHA-256.

CAMPAIGN-007-r5 is accepted at
`28817d6ea7a0d547ae89579d4597cea0fbae0b2b`. Independent Foreman verification confirms
the one-line root-version diff, exact target lock hash, locked CI-version sync, compile,
246 tests and all V0.9 public invariants. The local publication defect is cleared;
protected-main CI and Q-011 remain external gates.

PR #15 CI round 2 proves the lock fix across all six matrix jobs, but exposes one
Windows Python 3.12-only test defect. The continuation test reports a hard-coded 20ms
sampling event after `asyncio.sleep(0.02)` and assumes wall time is at least 15ms; the
runner observed an actual 9ms wall interval. CAMPAIGN-007-r6 is test-only: measure the
test double's real sampling duration and assert positive sampling wait does not exceed
the encompassing wall clock. Production telemetry and scheduling remain frozen.

CAMPAIGN-007-r6 is accepted at
`516db0ea88ec69cdd7df5e3490eb8aa08b74eca3`. Independent Windows Python 3.12 evidence
includes 20/20 isolated continuation passes, 23 timing-focused passes and 246 complete
passes. The correction is test-only; publication still requires a fresh all-green PR
#15 matrix before merge.

Publication completed on `main` at
`641ef46b6fdde380463b40d39a654cf8eb1248c2` with protected-main CI green. Q-011 is
accepted by `harness/evaluations/CAMPAIGN-007-q011-live-review.md`: six literal normal-
Goose records preserved full 6/6 coverage and clean protocol behavior, sequential
limit/peak/batches `1/1/6`, parallel `3/3/2`, and reduced median server wall time from
16,363 ms to 5,712 ms (`65.09%`, `2.86x`). Campaign 007 is closed. The sequential
operator override remains available for providers with stricter rate limits.

## Campaign 008: Council Value Visibility and Evaluation Intelligence

Campaign 008 moves from protocol completeness and latency to the product's central value:
showing users material blind spots without making six reviewers repeat the same approval.
It adds deterministic role-contribution and marginal-discussion diagnostics, a value-first
five-section primary report, and the audit's complete 18-case Golden Corpus. Metrics are
descriptive only and cannot become votes, role rankings, confidence theater or Policy Gate
weights. Full natural evidence remains in structured history.

The frozen implementation graph is PKG-042 V2.4 models/compatibility, PKG-043 deterministic
metrics, PKG-044 value-first presentation, PKG-045 Golden evaluation framework and PKG-046
V0.10 migration/artifacts/docs. Exact five tools, review-only default, budgets 6/13/18,
bounded concurrency and all user-authority rules remain unchanged. Q-012 is a separate
post-publication live usefulness gate.

CAMPAIGN-008-r1 produced the V2.4 models, ordinary structured contribution/discussion
metrics, value-first display, V0.10 identifiers and package evidence. Foreman review at
`harness/evaluations/CAMPAIGN-008-r1-review.md` preserved that work but reproduced a
deterministic correctness contradiction: preflight-only placeholder/markup clusters have
no model finding IDs, so the value projection called the technical role
confirmation-only and claimed no material issue while the chief correctly required a
fix. The r1 digest fallback also semantically classified free-form lens prose, contrary
to the frozen structured-only basis.

The r1 18-case fixture is enumeratively complete but not executable product evidence:
each case stores a manually identical `expected` and `observed` dictionary and the runner
only compares them. CAMPAIGN-008-r2 is a two-package bounded correction. PKG-047 makes
deterministic preflight contributions visible without double-counting an equivalent model
finding and removes prose heuristics. PKG-048 replaces copied observations with outcomes
derived by an offline scripted execution of real product components. All other V0.10
behavior remains frozen.

CAMPAIGN-008-r2 successfully removed the false-clean placeholder report and replaced
fixture-authored observations with an executable offline 18-case runner. Foreman review
preserves the 18/18 production-path corpus, authority/continuation evidence, prose-free
compatibility fallback and placeholder/markup correlation. Extended structured
counterexamples found one remaining bounded gap: required literals and numeric parity
plus equivalent reviewer evidence still count twice, and a missing URL is counted once
by command parity and once by URL parity. CAMPAIGN-008-r3 corrects only preflight-rooted
exact logical-issue correlation across the existing deterministic check families.

CAMPAIGN-008-r3 completed its required deterministic check-family matrix, but Foreman
non-overmerge review found one model-only regression: two production clusters from
different issue families merge when they share the same source/candidate span. r4 is a
minimal correction that restricts r3 exact aliases to attaching reviewer evidence onto
preflight-rooted groups; reviewer-only clusters retain their production issue identity.

CAMPAIGN-008-r4 is accepted by
`harness/evaluations/CAMPAIGN-008-r4-review.md` at
`84c6c64d40836875cf6515a6bf0c615c9e5ea0c9`. Combined r1-r4 evidence accepts F-040
through F-044: deterministic contribution and discussion-value metrics, value-first
presentation, the executable 18-case Golden Corpus and V0.10 migration. Publication and
Q-012 remain separate gates; no further local implementation Campaign is active.

V0.10 was published through protected-main PR #17 after all six Linux/Windows Python
3.10/3.12/3.13 CI jobs passed. Published `main` is
`e3d3de275915088c1430a243dfd9c2e410cbc58a`. Q-012 is issued by
`harness/contracts/CAMPAIGN-008-q012-live.md`: one fixed normal-Goose configuration,
three live cases for clean compression, deterministic blocker correlation and panoramic
non-repetitive value, with persisted structured records as evidence authority.

Q-012 stopped after its first admissible live record, documented in
`harness/evaluations/CAMPAIGN-008-q012-live-review.md`. The record proves normal Goose
compatibility and full reviewer coverage but reproduces two value-contract defects:
primary text repeats one placeholder defect across roles/checks, and discussion counts
six rephrasings of existing facts as six new evidence items. CAMPAIGN-009-r1 is a bounded
V0.10.1 correction for deterministic discussion novelty and grouped human presentation;
raw evidence, adjudication, tools, budgets, concurrency and Schema 2.4 remain frozen.

## Campaign 009 acceptance and next gate

- r1 decision: `CHANGES_REQUESTED` by
  `harness/evaluations/CAMPAIGN-009-r1-review.md`.
- r2 decision: `ACCEPTED` by
  `harness/evaluations/CAMPAIGN-009-r2-review.md`.
- Accepted implementation HEAD: `4a3c692ad528db03e4f72a025d60c4eb775454f0`.
- F-045: accepted by combined CAMPAIGN-009-r1/r2 evidence.
- Next: archive and publish the accepted V0.10.1 tree, then run Q-012 normal-Goose A/B/C
  revalidation against the exact published commit. Offline acceptance does not accept
  Q-012, and an unpinned or stale Goose installation is not admissible evidence.
- Signed live protocol: `harness/contracts/CAMPAIGN-009-q012-live.md`; the user's normal
  extension command remains unchanged and version admission prevents stale-cache tests.
- Published through PR #18 at protected-main commit
  `f3b232cb2f3c9500fed04d204ef6198f2ee49af4`; all six required Linux/Windows Python
  checks passed and the published product tree is equivalent to accepted HEAD.
