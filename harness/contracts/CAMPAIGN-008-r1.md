# Campaign Contract: CAMPAIGN-008-r1

## Control

- HARNESS_ROLE: WORKER
- HARNESS_MODE: STRICT_CAMPAIGN
- Campaign: `CAMPAIGN-008-r1`
- Product theme: Council value visibility and evaluation intelligence
- Repository: `C:\Users\GeZhu\MyMCP\mcp-council-of-translation`
- Exact Git baseline: `c4d2e42f5bfee377cdbebaed776272cb996c679c`
- Product target: package/module `0.10.0`
- Diagnostic build target: `evidence-value-council-v8`
- Record schema target: `2.4`
- Required ledger: `harness/reports/CAMPAIGN-008-r1-ledger.md`
- Required Worker report: `harness/reports/CAMPAIGN-008-r1-worker.md`
- Subagent delegation: forbidden in the shared worktree

The Foreman has frozen this design. The Main Worker implements, integrates, verifies and
reports; it must not edit Foreman-owned state or claim Campaign acceptance.

## Product objective

Make the Council's marginal value visible without manufacturing disagreement or turning
roles into a leaderboard. The normal user should quickly see which perspectives surfaced
new material information, which merely corroborated it, what remained unresolved, and
whether a discussion actually changed evidence or positions. Full natural role evidence
must remain available in the structured record.

This Campaign responds directly to the product purpose: the Council is valuable when it
reveals blind spots, not when six roles repeat the same approval in longer prose.

## Frozen invariants

1. The MCP surface remains exactly these five tools, in order:
   `review_translation`, `continue_review`, `view_review_record`,
   `list_review_records`, `get_server_info`.
2. Default output remains `review_only`; no complete suggested translation appears unless
   `output_mode=full_rewrite` is explicit.
3. Sampling budgets remain lightweight/standard/strict `6/13/18`.
4. Independent-review concurrency remains default/max `3/3`, with operator values 1/2/3
   and invalid fallback to sequential one.
5. No new model call, retry, elicitation, discussion or reconsideration may be introduced
   to compute value metrics or presentation.
6. User authority, Policy Gate, hard constraints, role routing, outcome identity,
   coverage rules and adjudication semantics remain unchanged.
7. Value metrics are descriptive diagnostics, never votes, quality scores, authority
   weights or confidence theater.
8. All metrics must derive deterministically from already validated structured findings,
   clusters, positions, discussion turns and provenance. Do not semantically score free-
   form prose with substring heuristics or a hidden model call.
9. Repeated or synonymous findings from one role do not multiply contribution.
10. Existing V1 and V2.0 through V2.3 records remain readable with conservative V2.4
    defaults. Historical records are not rewritten.

## Frozen V2.4 value model

Add a bounded structured projection equivalent to:

```text
CouncilValueMetrics
  role_contributions[]
    role_id
    contribution_kind = unique_material | corroborating | confirmation_only | unavailable
    unique_issue_count
    corroborated_issue_count
    material_finding_count
  unique_material_issue_count
  corroborated_issue_count
  confirmation_only_role_count
  unavailable_role_count
  discussion_new_evidence_count
  discussion_position_change_count
  discussion_resolved_issue_count
  discussion_marginal_value = not_applicable | none | low | material
  metric_basis = structured_findings_and_trace
```

Exact Pydantic naming may differ only where repository conventions require it, but the
semantics, bounded enums and information content are frozen.

Contribution classification priority is deterministic:

1. unavailable sample -> `unavailable`;
2. at least one issue-local material contribution not supplied by another role ->
   `unique_material`;
3. material findings that support an already represented issue/outcome ->
   `corroborating`;
4. valid review with no material structured finding -> `confirmation_only`.

One role may expose counts for unique and corroborating findings, but its primary kind
uses the priority above. IDs and counts belong in structured data; internal issue IDs do
not leak into the primary report.

Discussion marginal value is based only on trace deltas: new bounded evidence, a real
position change, or a resolved material issue. Rephrased prose alone counts as `none`.

## Frozen primary presentation

Replace repetitive clean-case role paragraphs with a value-first concise projection:

1. `## 审校背景`
2. `## Council 新增视角`
3. `## 角色覆盖与分工`
4. `## 共识、分歧与盲区`
5. `## 主编结论`

Rules:

- every active role remains visibly accounted for exactly once in the coverage section;
- material unique contributions appear before confirmations;
- corroboration is summarized without repeating the same issue prose six times;
- confirmation-only roles are visible as completed coverage, not presented as new
  discoveries;
- discussion value appears only when a discussion occurred;
- unavailable roles and incomplete coverage remain prominent and conservative;
- the chief disposition remains last;
- clean report target is at most 1,200 Unicode code points; hard maximum remains 3,200;
- `view_review_record(detail_level="full")` preserves complete natural role feedback,
  findings, evidence and trace.

Do not hide a material minority view merely because it is not unique or did not win.

## Golden evaluation corpus

Create deterministic, non-provider fixtures covering all 18 cases from the independent
audit:

1. placeholder loss
2. broken markup
3. meaning reversal
4. negation error
5. modality shift
6. critical omission
7. hard terminology-base violation
8. natural but inaccurate
9. accurate but unnatural
10. UI context mismatch
11. terminology-versus-fluency conflict
12. consent/authorization ambiguity
13. brand-only preference
14. clean translation
15. multiple valid candidates
16. user context changes the decision
17. user preference conflicts with a blocker
18. no real conflict

Each case must declare machine-checkable expected properties, not one brittle full-text
snapshot. At minimum cover critical recall, false positive behavior, contribution kinds,
conflict detection, user-authority boundary, chief consistency, call budget and whether
discussion added marginal value.

Provide a deterministic offline comparison runner or library entry that returns JSON-
safe aggregate metrics. It must not add an MCP tool, dependency or live model call.

## Package graph

### PKG-042 — V2.4 value models and compatibility

- Add bounded value/contribution models, serialization and conservative old-record
  defaults.
- Persist full records and metadata projections truthfully without exposing user/model
  prose in metadata mode.
- Verify V1 and V2.0-V2.3 reads.

### PKG-043 — Deterministic contribution and discussion metrics

- Compute role contribution from validated structured artifacts after deliberation.
- Compute marginal discussion value from trace deltas.
- Prove duplicate/synonymous findings cannot inflate authority or contribution.
- Prove computation adds zero sampling and zero elicitation.

Depends on PKG-042.

### PKG-044 — Value-first digest and primary display

- Add the frozen five-section projection.
- Keep all active roles visible once while collapsing repetitive confirmation prose.
- Preserve minority, unresolved context, degradation and chief-last behavior.
- Preserve full structured evidence through review and history tools.

Depends on PKG-042 and PKG-043.

### PKG-045 — Golden corpus and regression comparison

- Add all 18 deterministic cases and machine-checkable expected properties.
- Add aggregate metrics and regression comparison without provider/model calls.
- Include clean, issue-rich, disagreement, context-change and blocker-conflict probes.

Depends on PKG-043; may overlap PKG-044 tests only after the presentation interface is
frozen. Execute sequentially in the shared worktree.

### PKG-046 — V0.10 migration, package and documentation

- Migrate package/module to `0.10.0`, build to `evidence-value-council-v8`, schema to
  `2.4`.
- Keep exact five tools, defaults, budgets and concurrency diagnostics.
- Update README, AGENTS and authoritative architecture/tool-contract documentation.
- Build fresh sdist/wheel and smoke the installed wheel with current FastMCP.
- Update `uv.lock` only for the editable root version. Use pinned uv `0.12.3`, repository-
  local cache/tool directories and canonical `uv lock --refresh`; revision 3, artifact
  metadata and resolved dependency graph must remain intact.

Depends on PKG-042 through PKG-045.

## Authorized implementation paths

- `src/council_of_translation/**`
- `tests/unit/**`
- `tests/integration/**`
- `tests/fixtures/**`
- `README.md`
- `AGENTS.md`
- `docs/v0.4-architecture.md`
- `docs/v0.4-tool-contract.md`
- `pyproject.toml`
- `uv.lock`
- required Worker report and ledger paths only

New focused test or fixture files under authorized test directories are allowed. Do not
rename historical documentation paths merely to match the new version.

## Forbidden scope

- Foreman-owned `harness/plan.md`, `harness/features.json`, `harness/progress.md`, all
  contracts and all evaluations
- prior Worker reports/ledgers
- `.github/**`
- `.learnings/**`, `reviews/**`, `myTest/**` and the user audit report
- Goose installation/configuration, provider credentials or external services
- new runtime dependencies
- a sixth MCP tool, batch/file translation, translation-memory retrieval or edit
  application
- live Goose/provider/model calls
- push, PR, release, deployment or publication

## Commit and execution policy

- Start only if HEAD is exactly the contracted baseline and admitted dirty files are
  limited to Foreman/user assets.
- Execute PKG-042 through PKG-046 sequentially.
- Create one scoped local commit per package; never stage protected assets or reports.
- Keep the Git index empty after each commit and at final handoff.
- If canonical lock regeneration changes anything beyond the editable root version or
  expected generator metadata preservation, stop `BLOCKED`; do not manually edit or
  restore the generated lock.
- Do not use destructive Git operations.

## Required verification

1. Admission compile and complete test suite at the exact baseline.
2. Focused package tests after each package plus complete regression.
3. Exact 18-case corpus coverage and aggregate metric assertions.
4. Counterexamples proving repeated findings and rephrased discussion do not create
   false marginal value.
5. Clean and issue-rich presentation probes with exact section order, role accounting,
   chief-last behavior and length bounds.
6. Zero additional sampling/elicitation compared with equivalent baseline paths.
7. V1 and V2.0-V2.3 compatibility plus V2.4 full/metadata persistence.
8. Exact five tools, defaults, budgets 6/13/18 and concurrency 3/3 with override behavior.
9. `python -m compileall src tests` and complete test suite.
10. Fresh sdist/wheel, isolated Python 3.12/current FastMCP installed-wheel smoke calling
    all five tools and checking 0.10.0/build/schema.
11. `git diff --check`, exact authorized-scope audit, protected hashes and empty index.

Live Goose is a separate post-publication `Q-012` Foreman gate and must not be run by the
Worker.

## Worker report

Maintain `harness/reports/CAMPAIGN-008-r1-ledger.md` during execution and write
`harness/reports/CAMPAIGN-008-r1-worker.md`. Start the conversational handoff with exactly
`READY_FOR_REVIEW` or `BLOCKED`, then report baseline/final HEAD, commits and files per
package, package and integrated verification, fresh artifact hashes, skipped checks,
subagent count, authority/escalation count, external dependency operations, live-call
count and remaining risks. Do not claim Campaign acceptance, publication or project
completion.

