# Campaign Review: CAMPAIGN-010-r1

## Decision

`CHANGES_REQUESTED`

The deterministic primary projection and V0.10.2 migration are valid, but the required
model-only live-shaped projection is not. The Worker fixtures supplied a shared non-empty
replacement; the immutable live records contain ordinary `issue` findings with no
`proposed_value`, so their cluster `candidate_actions` contain only the current outcome.
The production renderer therefore skips the new model grouping and reproduces the Q-012
non-repetition defect.

## Control

- Role: `FOREMAN`
- Harness mode: `STRICT_CAMPAIGN`
- Contract: `harness/contracts/CAMPAIGN-010-r1.md`
- Contract SHA-256:
  `E09A31F3E544619D55B6A0DE456509E0F549DA694361C27925F1BFF2821535DE`
- Baseline: `9cd0f317ca6ecedef3477ac322c73189d430ded8`
- Worker final HEAD: `144ecebb6bfbd507ccdfb09a9b87efac3d59e9e1`
- Worker report: `harness/reports/CAMPAIGN-010-r1-worker.md`
- Commits: `38689f2`, `144eceb`
- Scope: exactly 12 authorized paths; index empty

## Scope and preserved evidence

- Baseline is an ancestor of final HEAD and the complete 12-path diff matches the two
  authorized packages. `git diff --check` passes.
- Protected Foreman, user and raw Q-012 assets retain their admission hashes.
- Independent compile and full regression pass: `291 passed in 3.97s`.
- `uv lock --check` passes with a repository-local cache; the lock changes only the root
  version and preserves revision/package/upload metadata.
- Package/module/build/schema are `0.10.2` / `0.10.2` /
  `evidence-value-council-v8.2` / `2.4`; five tools, review-only, budgets 6/13/18 and
  concurrency remain frozen.
- The accepted deterministic correction maps three missing-`{count}` checks to one
  natural primary repair and hides raw check telemetry.
- Case A grouping, structured-record non-mutation, Golden evidence and four r1 negative
  controls remain valid.

## Independent immutable-record replay

The Foreman parsed each accepted Schema 2.4 JSON into `ReviewRecordV2` and rendered it
with the final V0.10.2 `render_display_report`, without modifying the record.

### Case A

- 369 code points; byte-identical to the accepted V0.10.1 report.
- One six-role confirmation line and clean chief disposition.
- Result: pass.

### Case B

- Reduced from 902 to 719 code points.
- Three deterministic `{count}` messages collapse to one natural repair.
- Raw `required_literal` and English check messages disappear.
- Failure: the two live semantic-reversal clusters still produce two separate
  `建议修复` lines. The contract requires one placeholder repair plus one reversal repair.

### Case C

- 1,276 code points and materially unchanged from the failing live report.
- Failure: the same scope restoration remains two `建议修复` lines and two `执行顺序`
  lines. The contract requires one repair with bounded distinct consequences.

## Root cause

`_primary_work_item_groups` adds model-only groups only when `_replacement_actions`
returns a non-empty action different from `current_outcome`. The r1 Case C fixture was
constructed with such a shared replacement. The live B/C clusters have no proposed
replacement; their candidate actions are empty or repeat the current outcome. They are
therefore excluded before exact source/candidate anchor grouping can occur.

This is a test-shape error, not a provider, sampling, transport, schema, clustering or
metric failure.

## Required r2 correction

1. Add sanitized fixtures matching the real structural condition: no `proposed_value`,
   and no non-current candidate action.
2. Permit primary-only model grouping from exact or bidirectionally contained bounded
   source and candidate anchors when no conflicting concrete repair action exists.
3. Keep groups separate when concrete replacements conflict, protected anchors differ,
   only one side is structurally related, or the placeholder and semantic-reversal work
   items are distinct.
4. Retain all r1 deterministic grouping, natural messages, negative controls and full
   structured non-mutation.
5. Keep version/build/schema and all non-presentation subsystems unchanged.

CAMPAIGN-010-r2 is a one-package correction. Q-012 and F-046 remain unaccepted.
