# Campaign Contract: CAMPAIGN-009-r1

## Control

- HARNESS_ROLE: `WORKER`
- HARNESS_MODE: `STRICT_CAMPAIGN`
- State: `ASSIGNED`
- Repository: `C:\Users\GeZhu\MyMCP\mcp-council-of-translation`
- Exact Git baseline: `e3d3de275915088c1430a243dfd9c2e410cbc58a`
- Baseline subject: `Archive accepted Campaign 008`
- Trigger: Q-012 `CHANGES_REQUESTED` at
  `harness/evaluations/CAMPAIGN-008-q012-live-review.md`
- Product target: package/module `0.10.1`
- Diagnostic build target: `evidence-value-council-v8.1`
- Record schema remains: `2.4`
- Required ledger: `harness/reports/CAMPAIGN-009-r1-ledger.md`
- Required Worker report: `harness/reports/CAMPAIGN-009-r1-worker.md`
- Commit policy: one scoped local commit per package, four commits maximum
- Subagent delegation: allowed only for bounded, non-overlapping assignments; Main Worker
  owns integration and verification
- Acceptance authority: Foreman only

Read completely before editing: `AGENTS.md`, `harness/plan.md`,
`harness/features.json`, `harness/progress.md`, this contract, both Q-012 live protocols,
the Q-012 live review, all CAMPAIGN-008 contracts/evaluations/reports and the audit's
sections on Council value, non-manufactured discussion and marginal discussion value.

## Product objective

Make the already-published V0.10 value projection truthful and easier to scan under real
Goose output. A discussion may not claim that paraphrases of known facts are new evidence,
and the primary report may not repeat one logical defect or one confirmation sentence for
every role merely to prove role coverage.

This is a bounded V0.10.1 correction. It does not redesign Council authority, clustering,
role prompts, adjudication or the full structured record.

## Frozen invariants

1. The MCP surface remains exactly five tools in the existing order.
2. Default output remains `review_only`; `suggested_translation` stays null unless
   `full_rewrite` is explicit.
3. Sampling budgets remain `6/13/18`; independent concurrency remains default/max `3/3`
   with values 1/2/3 and invalid sequential fallback.
4. No new sampling, retry, elicitation, discussion or reconsideration call is allowed.
5. Schema remains `2.4`; V1 and V2.0 through V2.4 history remains readable.
6. Raw preflight checks, issue clusters, findings, natural role feedback, positions,
   discussion turns, chief checklist and trace remain fully available in structured
   history. Do not merge, delete or rewrite raw evidence merely to shorten display text.
7. Existing same-family and cross-family model issue identity from CAMPAIGN-008-r4
   remains unchanged. Presentation grouping is not production-cluster mutation.
8. Technical integrity, semantic correctness, caller hard rules, Policy Gate, user
   authority, coverage and adjudication remain unchanged.
9. Value diagnostics remain descriptive and cannot become votes, weights or authority.
10. Do not use fuzzy similarity, embeddings, semantic prose scoring, named-example
    shortcuts or a hidden model call. When novelty cannot be proven from bounded
    structured provenance, report zero new evidence conservatively.
11. Primary text retains exactly five sections, no internal IDs, chief disposition last,
    1,200 clean target and 3,200 hard cap.

## Frozen task graph

### PKG-049 — truthful marginal discussion evidence

Correct `discussion_new_evidence_count` and `discussion_marginal_value` without changing
the persisted `DiscussionTurn` schema.

- Build a deterministic pre-discussion inventory from validated structured artifacts
  already available to metric computation: issue/source/candidate anchors, immutable
  constraint identifiers, rule references, bounded evidence and positions.
- A discussion evidence item counts as new only when it adds a separately verifiable
  bounded structured anchor/provenance item absent from that inventory and absent from
  prior turns.
- A new sentence that only restates existing spans, constraints, rules, claims or evidence
  counts as zero even when wording differs.
- Position-change and resolved-issue deltas remain independently counted exactly as now.
- When existing function inputs cannot prove novelty, use the conservative zero result;
  do not infer novelty from prose style or token-overlap scores.
- Metric computation remains pure, deterministic, non-mutating and zero-call.

Required counterexamples:

- A live-shaped Case B discussion with six paraphrased `{count}`, permanent-delete,
  `cannot` and existing-rule evidence strings yields new-evidence `0`, position-change
  `0`, resolved `0`, marginal value `none`.
- Repeating the same evidence across three discussion turns still yields zero.
- A positive control with one genuinely new, exactly validated structured anchor yields
  one new evidence item and `low` when no position changes or resolutions occur.
- A material position change or resolution remains `material` independent of evidence
  prose novelty.

### PKG-050 — grouped value-first human presentation

Make primary text visibly account for every active role without repeating identical
prose or one logical defect across sections.

- `confirmation_only` roles are grouped into one concise coverage line naming every role
  exactly once. Do not emit the identical confirmation sentence once per role.
- Corroborating roles are grouped by the existing deterministic logical contribution
  identity. Name each role exactly once and state the shared issue once; do not recompute
  fuzzy semantic groups.
- Unique-material and unavailable roles remain prominent and individually attributable
  when grouping would hide unique value or a coverage gap.
- In primary chief text only, multiple deterministic checks for the same exact protected
  literal/placeholder/anchor collapse into one human work item with bounded check labels
  if useful. Full chief checklist and raw preflight clusters remain unchanged.
- Do not duplicate the same issue in unique value, role coverage, disagreements, minority
  and chief sections unless the later occurrence adds a materially different decision,
  condition or action.
- Preserve minority views, decisive conditions, unresolved context, warnings,
  degradation and final disposition.

Required live-shaped projections:

- Case A (`Bigger than bigger` / `比大更大`) remains correct, six roles
  `confirmation_only`, but uses one grouped coverage line; every Chinese role name appears
  exactly once and the report remains below 1,200 code points.
- Case B retains the placeholder blocker and distinct `cannot`/`可以` reversal, but the
  placeholder defect is one primary human work item with bounded corroborating-role
  attribution. The false `讨论补充 6 条新证据` line disappears.
- Full structured A/B records retain all original roles, findings, preflight checks,
  issue clusters, discussion turns and chief checklist entries.

### PKG-051 — regression and Golden integration

- Add deterministic fixtures/probes shaped from the two Q-012 records without embedding
  review IDs, provider metadata or unnecessary raw model prose.
- Extend unit and integration coverage for discussion novelty, grouped confirmations,
  grouped corroboration, chief-display deduplication and full-record preservation.
- Preserve all CAMPAIGN-008 exact-correlation/non-overmerge counterexamples.
- Run the exact 18-case executable Golden Corpus. Update an expected marginal-value
  property only when the existing fixture is demonstrably paraphrase-only under the new
  frozen truth rule; never edit expectations merely to make the suite green.
- Metrics add zero calls and presentation does not mutate records.

Depends on PKG-049 and PKG-050.

### PKG-052 — V0.10.1 migration and package evidence

- Set package/module version to `0.10.1` and diagnostic build to
  `evidence-value-council-v8.1`; keep record schema `2.4`.
- Update authoritative README, AGENTS and existing architecture/tool-contract documents
  with the conservative novelty and grouped-presentation rules.
- Update exact version/build tests.
- Regenerate `uv.lock` only for the editable root version using pinned uv `0.12.3`, a
  repository-local cache/tool directory and canonical `uv lock --refresh`. Revision 3,
  upload-time entries and the resolved dependency graph must remain intact.
- Build fresh wheel/sdist and smoke the installed wheel with Python 3.12 and current
  FastMCP through all five tools plus the A/B display/value probes.

Depends on PKG-049 through PKG-051.

## Authorized paths

Production and focused tests:

- `src/council_of_translation/localization/value_metrics.py`
- `src/council_of_translation/localization/digest.py`
- `src/council_of_translation/localization/orchestration.py` only if required to pass
  already-structured provenance into the two components above
- `tests/unit/test_v24_value_metrics.py`
- `tests/integration/test_v24_value_metrics.py`
- `tests/integration/test_v24_presentation.py`
- `tests/integration/test_v24_golden_corpus.py`
- `tests/fixtures/v24_golden_corpus.json` only under the expectation rule above
- one new focused fixture/test file under `tests/fixtures/` or `tests/integration/` if
  keeping the live-shaped probes isolated is materially clearer

Release contract:

- `src/council_of_translation/__init__.py`
- `pyproject.toml`
- `uv.lock`
- `README.md`
- `AGENTS.md`
- `docs/v0.4-architecture.md`
- `docs/v0.4-tool-contract.md`
- `tests/integration/test_v10_release_contract.py`
- `tests/integration/test_tool_surface_v2.py`
- any existing test file containing an exact package/build literal only if the literal
  must change to `0.10.1` / `evidence-value-council-v8.1`

Worker-owned handoff only:

- `harness/reports/CAMPAIGN-009-r1-ledger.md`
- `harness/reports/CAMPAIGN-009-r1-worker.md`

Do not stage or commit the Worker ledger/report or any protected asset.

## Forbidden scope

- Foreman-owned plan, feature, progress, contracts and evaluations
- all prior Campaign reports and ledgers
- `.learnings/**`, `reviews/**`, `myTest/**`, `.tmp/**` and the user audit report
- raw Q-012 records or provider/session logs in production, tests or Git
- public signatures, sixth tool, schema bump, new dependency, role/prompt/routing change,
  Policy Gate/adjudication change or full-record deletion
- Goose configuration/installation, credentials, live provider/model calls
- push, PR, release, deployment or publication

## Admission and protected assets

Verify exact baseline, contract hash, empty index, admitted dirty/untracked set and all
hashes below before editing. Admission compile and full suite must pass with at least
`278 passed`; stop on unexplained drift.

| Protected asset | SHA-256 |
| --- | --- |
| `harness/plan.md` | `A6DF6092F3ED67D6D2C97D320A7B3F839D008081BC3F5D9362649E02C9C2581F` |
| `harness/features.json` | `769B33DEDC3D44B7199CE468476500FD958D9EF11B3587A25FE6F36323EB116A` |
| `harness/progress.md` | `A06632A6836ADF189BEB86DC8A4128E8024FEAD400288D9B70E3CB61C29226F1` |
| `harness/contracts/CAMPAIGN-008-q012-live.md` | `39032065F7539EAAC94DA13393A816DCC35D1584B68ECB1ED3674730CC564DC4` |
| `harness/contracts/CAMPAIGN-008-q012-live-r2.md` | `72F223CE524371794372D2C3DDEEF5378942DA701607C414427729DE28A9F5F2` |
| `harness/evaluations/CAMPAIGN-008-publication-ci-review.md` | `643AB70D3C7D7258898D4F61D265D79A96EC4339CBF5EAB05C9EBABBE9762F53` |
| `harness/evaluations/CAMPAIGN-008-q012-live-review.md` | `A13A86B4D6CD5F1247EB673E4FB77DB6E04F548229E295B7E44C05A2CCF32C0F` |
| `.learnings/LEARNINGS.md` | `52DC1BA8043481911C0DEABB3AC882504D9CBE8BB63D60F391C188586A230DF0` |
| `.learnings/ERRORS.md` | `F99EB75886781958BF5AE6DCF844FD476CBCA45937896A25EE3B2E9D6CD34F0A` |
| `mcp-council-of-translation-audit-and-upgrade-recommendations.md` | `B48073E063C4C9F34E0B6B4DAE94E80079EAAAD3B2F8E273DD60B2F25F6ABD76` |

All other Harness paths plus `reviews/**` and `myTest/**` are path-protected. The two
ignored `.tmp/q012` records are read-only Foreman evidence and forbidden to the Worker.

## Execution and commit policy

1. Reconcile baseline and protected assets before running admission.
2. Execute PKG-049 through PKG-052 sequentially. Later packages may not weaken earlier
   truth rules.
3. Create one scoped local commit per package; combine PKG-049/050 only if their shared
   implementation makes separation artificial. Four commits maximum.
4. Use exact-path staging. Keep the index empty after every commit and at handoff.
5. Do not amend, reset, restore, clean, rebase or modify unrelated user/Foreman assets.
6. If lock regeneration changes anything beyond the root package version or loses
   revision/upload-time metadata, stop `BLOCKED` without manual lock editing/restoration.

## Required verification

1. Admission compile and full baseline suite (`>=278 passed`).
2. PKG-049 focused novelty counterexamples and all existing V2.4 metric tests.
3. PKG-050 A/B live-shaped primary/full-record projections plus all presentation tests.
4. PKG-051 exact 18/18 Golden run, exact call/elicitation totals expected by the fixture,
   all eight aggregate metrics 1.0, and all CAMPAIGN-008 correlation/non-overmerge tests.
5. Assert no added sampling/elicitation and no mutation of clusters, turns, positions,
   chief checklist or structured history.
6. Exact five tools, review-only, schema 2.4, budgets 6/13/18 and concurrency invariants.
7. Final `python -m compileall src tests` and complete suite.
8. `git diff --check e3d3de275915088c1430a243dfd9c2e410cbc58a..HEAD`, exact
   authorized-scope audit, protected hashes, dead-import scan and empty index.
9. Fresh wheel/sdist and isolated Python 3.12/current-FastMCP installed-wheel smoke
   calling all five tools and asserting version/build/schema plus A/B corrected output.

## Stop conditions and handoff

Stop `BLOCKED` only if truthful correction requires a schema/public-signature/prompt/
authority/dependency change, an unauthorized path, live external authority, or the exact
baseline/protected assets do not match. New test failures and bounded implementation
choices inside this contract are normal Worker work, not blockers.

Maintain `harness/reports/CAMPAIGN-009-r1-ledger.md` and write
`harness/reports/CAMPAIGN-009-r1-worker.md`. Start the handoff with exactly
`READY_FOR_REVIEW` or `BLOCKED`, then report contract hash, baseline/final HEAD, commits
and files per package, before/after A/B counterexamples, novelty/grouping/full-record
evidence, Golden/correlation/full/build/wheel results, hashes/index/worktree, subagent/
authority/external/live counts and remaining risks. Do not push, create a PR, publish,
call Goose/provider/model, claim Campaign acceptance, Q-012 acceptance or completion.
