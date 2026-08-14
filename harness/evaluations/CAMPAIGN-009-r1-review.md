# Foreman Review: CAMPAIGN-009-r1

## Decision

`CHANGES_REQUESTED`

- Role/mode: `FOREMAN`, `STRICT_CAMPAIGN`
- Contract: `harness/contracts/CAMPAIGN-009-r1.md`
- Contract SHA-256: `F4C8EB61730E94279E028821FF08E1CA6E2B81C772D8CFC90AF63C3538DF8758`
- Baseline: `e3d3de275915088c1430a243dfd9c2e410cbc58a`
- Worker final HEAD: `62f2ee9bf1860f80281afbbad53734db5f700205`
- Worker report: `harness/reports/CAMPAIGN-009-r1-worker.md`
- Ledger: `harness/reports/CAMPAIGN-009-r1-ledger.md`

The bounded V0.10.1 direction is sound, the Worker stayed within scope, and the main
Q-012 A/B regressions are corrected. Independent review nevertheless found two exact
counterexamples against the frozen truth and presentation rules. The Campaign cannot be
accepted until those boundaries are corrected.

## Independent evidence

- Baseline-to-final scope: exactly four commits and 16 contract-authorized paths.
- Git index: empty; all ten protected hashes matched; `git diff --check` passed.
- Fresh compile: passed.
- Fresh complete suite: `283 passed in 3.61s`.
- Fresh risk-weighted suite: `42 passed in 1.28s` across V2.4 metrics, presentation,
  live-shaped A/B, Golden and release/tool invariants.
- Lock invariants: revision `3`, 78 packages and 586 upload-time entries; only the root
  editable version changed from 0.10.0 to 0.10.1.
- Version/build/schema and frozen surface remain `0.10.1`,
  `evidence-value-council-v8.1`, `2.4`, exact five tools and budgets 6/13/18.

## Accepted package evidence retained

- PKG-049 correctly makes the recorded Q-012 Case B paraphrases yield discussion new
  evidence `0`, position changes `0`, resolved issues `0`, and marginal value `none`.
- PKG-050 correctly groups the six Case A confirmation-only roles into one concise line
  and reduces the Case B `{count}` primary checklist to one work item while preserving
  the distinct semantic reversal.
- PKG-051 keeps the exact 18/18 Golden Corpus, 113 scripted samples, four elicitations and
  all eight aggregate metrics at 1.0. Full structured A/B evidence remains immutable.
- PKG-052 version, docs, lock and package evidence is internally consistent. These items
  do not need redesign or another version bump for the bounded correction.

## Failed criteria and counterexamples

### 1. Existing typed provenance can be counted as new

With an existing `RolePosition.rule_refs=["TB-1"]`, a discussion evidence item
`rule_ref:TB-1` produces `discussion_new_evidence_count=1` and marginal value `low`.
The reference already exists in the pre-discussion structured position, so this violates
PKG-049 and F-041. The inventory stores the raw value as an `exact:` key but does not add
the equivalent typed `provenance:rule_ref:` identity. The same boundary applies to
`IssueCluster.immutable_hard_constraints` and `constraint_ref:`.

Expected correction: inventory typed rule and constraint fields under their canonical
provenance identity, without treating arbitrary prose as evidence and without weakening
the genuinely-new structured-anchor positive control.

### 2. A corroborated material disagreement can disappear from primary text

A minimal disputed cluster with two corroborating roles and topic
`候选译文把“trial”误写成“正式版”，会改变授权状态。` renders only:

- `交叉印证：1 个问题得到多个专业视角支持。`
- `忠实度审校员、术语与一致性管理员：共同交叉印证“trial → 正式版”相关问题。`
- a generic statement that the minority position was retained.

The actual material problem text is absent. `render_display_report()` currently treats
every cluster topic as already represented before proving that the topic was emitted.
This violates PKG-050/F-042 requirements to preserve material disagreements and state a
shared issue once. An anchor is attribution, not a substitute for the issue meaning.

Expected correction: suppress repetition only after a bounded material topic has really
been rendered. Every material unique/corroborated/disputed issue must remain intelligible
at least once, while confirmation grouping, role accounting, minority conditions, final
disposition and the 3,200 cap remain intact.

## Audit note

The r1 Worker report contains a one-character transcription error in the displayed
`.learnings/LEARNINGS.md` hash (an extra trailing `A`). The actual protected file matched
the contract. Do not rewrite the historical r1 report; the r2 report must state hashes
accurately.

## Required continuation

Issue `CAMPAIGN-009-r2` as a bounded correction from exact HEAD
`62f2ee9bf1860f80281afbbad53734db5f700205`. Preserve all accepted r1 evidence and make
no package/version/schema/tool/prompt/authority/lock change.
