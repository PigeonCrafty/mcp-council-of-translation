# Campaign Contract: CAMPAIGN-002-r1

## Control

- Role: WORKER
- Mode: STRICT_CAMPAIGN
- State: ASSIGNED
- Repository: `C:\Users\GeZhu\MyMCP\mcp-council-of-translation`
- Exact baseline commit: `824559afd68f170758837769b1d1d19df991db4b`
- Baseline subject: `Record V0.4 test branch publication`
- Product target: `0.5.0`
- Record schema target: `2.1`
- Diagnostic build target: `outcome-first-decision-v3`
- Prior accepted review: `harness/evaluations/CAMPAIGN-001-r5-review.md`
- Worker ledger: `harness/reports/CAMPAIGN-002-r1-ledger.md`
- Worker report: `harness/reports/CAMPAIGN-002-r1-worker.md`
- Acceptance authority: Foreman only
- Commit policy: required, scoped local commits; no push, PR, release, deployment, credentials, or Goose installation changes
- Live calls: optional only when already configured; never request or expose provider credentials

The Worker must read `AGENTS.md`, `harness/plan.md`, `harness/features.json`, `harness/progress.md`, this contract, and the prior accepted review completely before editing. Repository assets override conversation context.

## Admission gate

Before edits, verify all of the following and record the evidence in the ledger:

1. `git rev-parse HEAD` equals the exact baseline above and the object resolves as a commit.
2. No staged changes exist.
3. Existing tracked dirt is limited to the three Foreman-owned Harness assets listed below.
4. User-owned untracked assets are preserved.
5. The protected hashes match exactly.
6. The accepted V0.4 baseline compiles and its complete test suite passes using repository-local temp/cache paths.

Protected hashes at contract issuance:

| Asset | SHA-256 |
|---|---|
| `harness/plan.md` | `B7B6C977AC51A4D8DD2349BD09CB57E94C6EB750DAD9D1D3E620764EF7DF1F20` |
| `harness/features.json` | `6DC37D15433ED555ACFEEE506FA140EB927229D42A911E7C9CF1A1CBF3433575` |
| `harness/progress.md` | `D0A5487456C5B286EB92A1BD482937D7595B0468602652F01AC2875FFFA82CE3` |
| `.learnings/LEARNINGS.md` | `22F939E6F980DF52487AAFE97EDCA9B90CF3931DDB7A31BF8A5BBB8F052E658F` |
| `mcp-council-of-translation-audit-and-upgrade-recommendations.md` | `B48073E063C4C9F34E0B6B4DAE94E80079EAAAD3B2F8E273DD60B2F25F6ABD76` |
| external live record `20260812T060954605875Z_1d988172bd1f.json` | `8F10CB0538BF8BE2FCC3559608AE3F6FDBB612C4E5EE51D7A968AB52A3998A16` |

The contract file itself is Foreman-owned. Hash it on admission and preserve it byte-for-byte. Treat `reviews/`, `.learnings/`, the audit markdown, all prior contracts/evaluations/reports, and `myTest/` if present as protected regardless of whether Git tracks them.

Stop as `BLOCKED` before changes if the baseline, staged state, or protected hashes differ. Do not repair or commit Foreman/user assets.

## Goal

Turn the V0.4 interaction from a structurally successful but verbose reviewer-action form into an outcome-first Council decision experience that is readable in standard Goose MCP elicitation, preserves user authority within valid options, spends reconsideration budget on truly affected roles, and reports degraded execution truthfully.

## Primary live counterexample

Read this record as immutable, read-only evidence when accessible:

`C:\Users\GeZhu\AppData\Local\Council-of-Translation\reviews\20260812T060954605875Z_1d988172bd1f.json`

The record proves the V0.4 end-to-end path works. It also shows four overlapping action-text options for the `Continue` decision, internal-looking option values, `reconsideration_budget_unavailable`, an unqualified `COMPLETED` status, weak compact visibility into effective inputs, and an affirmation treated as an improvement. Do not edit or copy private record content into fixtures beyond the minimal synthetic facts needed for deterministic tests.

## Frozen invariants

- Exactly five public tools remain: `review_translation`, `continue_review`, `view_review_record`, `list_review_records`, and `get_server_info`.
- Review-only remains the default and no tool edits translation files.
- `interactive_mode=auto`, `decision_fallback=council_adjudication`, `trace_level=summary`, and `history_mode=full` remain defaults.
- Sampling budgets remain lightweight 6, standard 10, strict 14.
- Maximum one targeted discussion round and maximum three DecisionPoints remain.
- User choice is decisive only among Policy-Gate-valid outcomes and cannot override technical integrity, semantic correctness, deterministic hard constraints, or critical blockers.
- Council fallback is evidence-weighted Position Matrix adjudication, never raw majority voting.
- No hidden chain-of-thought is requested, persisted, or returned.
- V1 and V2.0 records remain readable.
- No custom MCP App/widget/UI is introduced.

## Shared V2.1 contract

### Finding classification

- Add `finding_kind` with values `issue`, `choice`, and `affirmation`.
- Add `proposed_value` for the concrete candidate outcome when a finding proposes a choice.
- A valid zero-finding envelope and clean affirmations continue to count as reviewer coverage.
- Affirmations may support consensus, but they do not create IssueClusters, DecisionPoints, must-fix items, or optional improvements by themselves.
- Legacy V2.0 findings normalize conservatively and cannot gain blocking authority through migration.

### Outcome normalization

- Derive candidate outcomes from concrete `proposed_value` values, the current candidate, and admissible proposals; raw `action` prose remains advice/evidence.
- Normalize harmless formatting differences without merging materially different translations.
- Equivalent outcomes from multiple roles map to one option and one influence contribution per role.
- Include the current candidate explicitly when valid.
- Do not create a DecisionPoint unless at least two materially distinct valid outcomes remain after the Policy Gate.
- Invalid, empty, ambiguous, overlong, or non-string model proposals fail conservatively and cannot become hard constraints or selectable values.

### DecisionOption and form mapping

Each decision option must retain a stable internal `option_id`, machine-comparable `outcome_value`, concise `label`, concise `description`, support role IDs, bounded support rationale, and policy validity provenance.

The standard MCP form must:

- batch at most three DecisionPoints;
- show at most four choices per point including delegation;
- use outcome labels no longer than 48 Unicode code points and descriptions no longer than 160;
- avoid displaying internal option IDs as labels or embedding full reviewer feedback;
- deterministically order current candidate first when valid, alternatives next, and `暂不决定，由 Council 裁决` last;
- use stable safe form values and reject unknown, stale, duplicated, or mismatched values;
- map accepted values back to exact internal option IDs and outcome values.

Explicit delegation is a valid user action, distinct from unsupported, declined, cancelled, malformed, or runtime failure. It invokes existing Council adjudication without being labeled an interaction failure.

### Targeted reconsideration and status

- Reconsider only roles whose recorded position conflicts with the selected outcome or whose expertise is materially affected.
- Do not resample a supporting role solely because the selected outcome matches its position.
- Prioritize dissenting roles by role relevance, blocking expertise, evidence tier, and configured priority within remaining budget.
- Persist requested, completed, skipped, and failed role IDs separately.
- The deterministic standard reference path of six independent reviewers, one chief-editor/adjudication call, and up to three affected-role calls must fit the 10-call budget without `reconsideration_budget_unavailable`.
- If required reconsideration is skipped or fails, set `degraded=true`, emit bounded warnings, preserve fallback provenance, and return `COMPLETED_WITH_FALLBACK` or `NEEDS_HUMAN_REVIEW` according to integrity impact. Never report unqualified `COMPLETED`.

### Compact result

Expose bounded, serialization-safe fields for:

- `effective_task`: normalized content type, audience, mode, and material rule context actually used;
- `deliberation_summary`: consensus, material disagreement, evidence basis, user selection/delegation, final outcome, and reconsidered roles;
- `degraded` and `warnings`;
- deduplicated chief-editor checklist and terminology/conflict decisions.

The default result must be useful without opening the full record, but detailed role feedback and trace stay on demand. Do not leak full input packets, unrestricted model reasoning, or metadata-mode private content.

## Package execution

Execute packages sequentially. After each package, update the ledger with files, commands, results, risks, and commit SHA before starting the next package. A later package may refine earlier work only within the shared contract.

### PKG-011 — V2.1 models, migration, and persistence

Allowed implementation areas:

- `src/council_of_translation/localization/models.py`
- `src/council_of_translation/localization/compatibility.py`
- `src/council_of_translation/localization/persistence.py`
- directly focused unit/integration tests

Deliver schema 2.1 classification, options, decisions, reconsideration provenance, compact status fields, safe defaults, and V1/V2.0 read compatibility. Preserve metadata privacy and atomic persistence.

### PKG-012 — Outcome extraction and normalization

Allowed implementation areas:

- `src/council_of_translation/localization/clustering.py`
- `src/council_of_translation/localization/deliberation.py`
- `src/council_of_translation/localization/policy.py`
- `src/council_of_translation/localization/prompt_builders.py`
- directly focused tests

Deliver outcome-first normalization, deduplication, current-candidate representation, Policy-Gate filtering, DecisionPoint eligibility, affirmation handling, and bounded prompt/schema instructions. Preserve one-role-one-influence behavior.

### PKG-013 — Goose-readable elicitation

Allowed implementation areas:

- `src/council_of_translation/localization/runtime.py`
- `src/council_of_translation/localization/orchestration.py`
- directly focused tests

Deliver readable bounded form fields, explicit Council delegation, stable value mapping, and conservative handling of unknown/stale/malformed responses. Use only standard MCP/FastMCP elicitation capabilities.

### PKG-014 — Reconsideration and degradation

Allowed implementation areas:

- `src/council_of_translation/localization/orchestration.py`
- `src/council_of_translation/localization/deliberation.py`
- `src/council_of_translation/localization/models.py`
- `src/council_of_translation/localization/runtime.py`
- directly focused tests

Deliver contrary/affected-role selection, deterministic prioritization, correct call accounting, requested/completed/skipped/failed provenance, and truthful status/warnings.

### PKG-015 — Compact decision experience

Allowed implementation areas:

- `src/council_of_translation/localization/orchestration.py`
- `src/council_of_translation/localization/policy.py`
- the existing server/tool registration modules under `src/council_of_translation/`
- directly focused tests

Deliver effective-task visibility, a bounded chief-editor deliberation digest, explicit degraded/warnings surface, and semantic checklist deduplication. Keep default output review-only and `suggested_translation` exclusive to explicit `full_rewrite`.

### PKG-016 — Release evidence and documentation

Allowed areas:

- `pyproject.toml`
- package `__init__.py` and existing version/build metadata sites
- `README.md`, `AGENTS.md`, `docs/**`
- `tests/**`
- `harness/reports/CAMPAIGN-002-r1-ledger.md`
- `harness/reports/CAMPAIGN-002-r1-worker.md`

Align authoritative documentation and tool descriptions, bump package/module version to `0.5.0`, set diagnostic build to `outcome-first-decision-v3`, complete regression/evaluation fixtures, and build fresh distributions.

Shared files named in more than one package are Main Worker integration hotspots. No two agents may edit them concurrently.

## Delegation policy

The Main Worker is Codex in a separate conversation. It may use at most three bounded Codex subagents for independent, non-overlapping implementation or read-only review. The Main Worker must retain ownership of integration hotspots, sequential package admission, final tests, Git staging, commits, ledger, and report. Concurrent production edits to the same file are forbidden. Record every subagent task and result.

## Acceptance criteria

1. The synthetic source `Continue`, candidate `继续`, UI context fixture yields real valid alternatives such as keeping `继续` versus using `下一步`; selectable labels are outcomes, not reviewer instructions.
2. Repeated synonymous findings from one or many roles do not duplicate options or multiply normalized influence.
3. Six valid clean/affirming reviewers produce full coverage without manufactured clusters, DecisionPoints, checklist items, or human review.
4. The current candidate is explicit when valid; fewer than two valid distinct outcomes produces no DecisionPoint.
5. Each point contains no more than four readable choices including Council delegation; limits and deterministic ordering are enforced for Unicode and adversarial model text.
6. Form values round-trip to exact internal options. Internal IDs are retained in trace but not displayed as user labels. Unknown/stale/malformed values cannot select an option.
7. Explicit delegation invokes Council adjudication and is distinguished from decline, cancel, unsupported, malformed, and failure telemetry.
8. A user-selected valid outcome remains decisive after targeted reconsideration unless newly established immutable constraints invalidate it; any invalidation is explicit and traceable.
9. Only contrary/materially affected roles reconsider. A supporting role is not resampled merely for agreeing. The standard reference flow uses at most 10 model calls and no unavailable-budget fallback.
10. Forced insufficient budget or reconsideration runtime failure produces requested/completed/skipped/failed provenance, `degraded=true`, warnings, and a conservative non-clean status.
11. Compact output shows the effective normalized task, bounded Council reasoning summary, decision/delegation, reconsideration effect, degraded state, warnings, review ID, and retrieval hint without duplicative reviewer prose.
12. Chief-editor `must_fix`, `should_fix`, `optional_improvements`, terminology decisions, and conflict resolutions are semantically deduplicated; affirmations are not mislabeled as improvements.
13. V2.1 full/off/metadata persistence, collision-safe IDs, atomic writes, and V1/V2.0 migration pass. Metadata mode persists no source, candidate, TB/SG packets, raw model text, user free text, or derived text that reconstructs them.
14. Malformed reviewer envelopes, reasoning-only sampling, transport errors, partial/none coverage, continuation, hard constraints, one-role influence, no-conflict, and review-only regressions remain conservative.
15. Exact five public tools, defaults, 6/10/14 budgets, package/module version `0.5.0`, diagnostic build `outcome-first-decision-v3`, and record schema `2.1` are verified.
16. All 117 accepted V0.4 tests and new focused V0.5 tests pass, syntax compilation passes, `git diff --check` passes, and fresh sdist/wheel artifacts build successfully through repository-local paths.
17. Documentation explains that one submit button is normal for the batched standard form, how Council delegation works, how to inspect full traces, how degradation is surfaced, and how to run a pinned-commit Goose test.

## Required deterministic evidence

At minimum, add and report tests/probes for:

- `Continue` outcome choice round-trip and exact user-facing form schema;
- duplicated/synonymous proposal collapse and materially distinct proposal separation;
- current candidate inclusion and one-outcome/no-DecisionPoint behavior;
- clean affirmation/no-issue behavior;
- label/description/choice/DecisionPoint limits with hostile Unicode and overlong input;
- accept, explicit delegate, decline, cancel, unsupported, malformed, stale, and runtime-error form paths;
- supporting versus dissenting role reconsideration selection and exact sampling counts;
- standard within-budget and forced budget/runtime degraded paths;
- compact/full result parity, checklist deduplication, effective task, warnings, and no hidden reasoning;
- V1/V2.0/V2.1 persistence plus metadata privacy;
- malformed/full/partial/none reviewer coverage and continuation regressions;
- exact five-tool/version/build/default/budget introspection;
- fresh package installation or import smoke test from built wheel when practical.

Use deterministic scripted executors and gateways. Do not make live provider behavior a prerequisite for Worker readiness.

## Required verification

Run and record exact commands, exit codes, counts, and relevant outputs:

```powershell
python -m compileall src tests
```

```powershell
.venv\Scripts\python.exe -m pytest -q --basetemp .tmp\campaign002-r1-pytest -p no:cacheprovider
```

```powershell
$env:UV_CACHE_DIR='.tmp\campaign002-uv-cache'; uv build --out-dir .tmp\campaign002-dist
```

Also run focused named tests/probes for every acceptance group, exact tool introspection, and a built-wheel smoke import. Use repository-local cache/temp paths. Because the version changes, prior V0.4 build evidence cannot replace a fresh V0.5 build. If the build cannot be established after safe local alternatives, stop and report the exact blocker rather than declaring readiness.

Before handoff run:

```powershell
git diff --check 824559afd68f170758837769b1d1d19df991db4b..HEAD
git diff --name-status 824559afd68f170758837769b1d1d19df991db4b..HEAD
git status --short
```

Inspect the complete baseline-to-final diff, verify protected hashes again, and prove only authorized implementation/test/doc files were committed. Foreman-owned dirty Harness files must remain unstaged and byte-identical. The new ledger/report remain uncommitted unless the Foreman issues a later archival instruction.

## Commit policy

- Create scoped commits at coherent package/integration boundaries. Do not squash accepted evidence into one opaque commit unless the implementation genuinely cannot be separated.
- Stage explicit authorized paths only. Never use broad staging commands that capture protected files.
- Do not amend, rebase, reset, force, merge, pull, push, open a PR, or modify branch protection.
- Do not commit `.tmp/`, build artifacts, caches, user records, credentials, Foreman assets, the ledger, or the Worker report.
- End with tracked production/test/doc changes clean and all local implementation commits ahead of the unchanged baseline.

## Stop conditions

Stop as `BLOCKED` when:

- admission baseline, staged state, or protected hashes differ;
- a requirement needs a sixth public tool, custom Goose UI, budget expansion, provider-specific behavior, majority voting, or translation/file editing;
- safe V1/V2.0 migration or metadata privacy cannot be maintained;
- deterministic outcome normalization cannot avoid inventing or silently merging materially different translations;
- required verification or a fresh V0.5 package build cannot be established after safe in-scope alternatives;
- an external mutation, credential, protected asset, or forbidden boundary would be required.

Do not weaken acceptance criteria to continue. Record partial evidence and the exact decision needed.

## Worker handoff

Write `harness/reports/CAMPAIGN-002-r1-worker.md` and maintain `harness/reports/CAMPAIGN-002-r1-ledger.md`. In chat, start with `READY_FOR_REVIEW` or `BLOCKED`, then report:

- baseline and final full SHAs;
- commits and changed files by package;
- test/build/probe commands, counts, and skips;
- criterion-to-evidence map;
- exact tool/version/build/default/budget results;
- protected hashes and worktree/index state;
- subagent, escalation, external mutation, and live-call counts;
- remaining risks and the pinned Goose validation command/prompt.

Stop after the handoff. Do not claim Campaign acceptance, project completion, or release readiness; only the Foreman can decide those states.
