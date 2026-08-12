# Council of Translation V0.5 Harness Plan

## Control

- Harness mode: `STRICT_CAMPAIGN`
- Foreman: Codex
- Main Worker: Codex Main Worker in a separate new conversation
- Active Campaign: `CAMPAIGN-002-r3` (`ACCEPTED / LIVE_VALIDATION_PENDING`)
- Source baseline: `824559afd68f170758837769b1d1d19df991db4b`
- Product target: `0.5.0`
- Diagnostic build target: `outcome-first-decision-v3`
- Acceptance authority: Foreman only

Repository artifacts are the source of truth. Conversation summaries do not override this plan, `features.json`, `progress.md`, or the active Campaign contract.

The Foreman and Main Worker are separate Codex conversations. The Worker must bootstrap exclusively from repository assets and must not assume access to the Foreman's conversation context.

The V0.4 sections below are the accepted architectural foundation and remain binding unless Campaign 002 explicitly refines them. The `Campaign 002: Outcome-first Decision UX` section is the authoritative delta for the active V0.5 target.

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

The repository implementation is accepted at `ca3d24afdc8feaa65286b13c6118720809749436` by `harness/evaluations/CAMPAIGN-002-r3-review.md`. F-011 through F-016 are accepted. Q-007 remains pending until the accepted commit is pushed and a real Goose/provider interaction confirms the V0.5 decision-form UX and compact result.

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
