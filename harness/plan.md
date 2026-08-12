# Council of Translation V0.4 Harness Plan

## Control

- Harness mode: `STRICT_CAMPAIGN`
- Foreman: Codex
- Main Worker: Codex Main Worker in a separate new conversation
- Active Campaign: `CAMPAIGN-001-r5` (accepted implementation; live validation pending)
- Source baseline: `34d41946717f1993b8954260afc893737198a3bb`
- Product target: `0.4.0`
- Diagnostic build target: `structured-deliberation-v2`
- Acceptance authority: Foreman only

Repository artifacts are the source of truth. Conversation summaries do not override this plan, `features.json`, `progress.md`, or the active Campaign contract.

The Foreman and Main Worker are separate Codex conversations. The Worker must bootstrap exclusively from repository assets and must not assume access to the Foreman's conversation context.

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
