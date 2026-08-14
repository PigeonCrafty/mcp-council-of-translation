# Live Goose Review: CAMPAIGN-008 Q-012

## Decision

`CHANGES_REQUESTED`

Published V0.10 is transport-compatible and persists complete Schema 2.4 records after
the corrected Goose environment setup. The clean Case A is correct and bounded, while
the issue-rich Case B reproduces failures in marginal-value truth and primary
non-repetition. Q-012 cannot be accepted without a bounded implementation correction.
The remaining live case is stopped to avoid unnecessary provider cost.

## Control

- Role: `FOREMAN`
- Harness mode: `STRICT_CAMPAIGN`
- Gate: `Q-012` value-first Council live usefulness and non-repetition evidence
- Protocols: `harness/contracts/CAMPAIGN-008-q012-live.md` and
  `harness/contracts/CAMPAIGN-008-q012-live-r2.md`
- Published `main`: `e3d3de275915088c1430a243dfd9c2e410cbc58a`
- Package/build/schema: `0.10.0` / `evidence-value-council-v8` / `2.4`
- Admissible Case A record: `20260814T082515308822Z_acd09409c766`
- Case A SHA-256:
  `8CB528793F5D9F4F97B76822349E6EB1BAB88A3EE6097A4079ADBD9ADF1D81B3`
- Admissible Case B record: `20260814T082144326698Z_eee1cf4ac053`
- Case B SHA-256:
  `5CF9DB8EF84FFF5CE68876E0B0A0A80B54094A71FF1A74C1B4B62DDC91E3879A`
- Initial three persistence failures: excluded; no records or review IDs were created

## Compatibility evidence preserved

- The corrected path wrote both complete records under `.tmp/q012`.
- Package/module, build and schema match the published V0.10 contract.
- Six canonical UI roles all returned `structured_success`; coverage is `full` with
  successful/unavailable `6/0`.
- Sampling is `7/13`: six independent reviews plus one discussion, within budget.
- Status is `NEEDS_HUMAN_REVIEW`, degradation is false, warnings and fallback are empty.
- The placeholder hard rule remains blocking and the `cannot`/`可以` reversal remains a
  distinct correctness issue. User preference does not override either.
- `review_only` remains active.

## Clean Case A evidence

Case A is semantically and operationally correct: six marketing roles returned
`structured_success`, calls are `6/13`, coverage is full, status is `COMPLETED`, there is
no discussion, and all six roles are truthfully `confirmation_only`. The 467-code-point
report is comfortably below the 1,200 clean target and the chief disposition is last.

The coverage section nevertheless repeats the identical sentence `完成确认性覆盖，未提交实质问题`
six times. This satisfies literal once-per-role accounting but is a usability opportunity:
one grouped confirmation line can name all six roles once with less scanning. This alone
would not fail Q-012; it is included in the bounded presentation correction because Case
B demonstrates materially harmful repetition of issue prose.

## Failed criterion 1 — repetitive primary presentation

The Case B primary report is 1,501 Unicode code points. It repeats `{count}` loss throughout
the unique-value line, corroboration count, five role-coverage lines, consensus,
disagreements, minority report and three separate chief `must_fix` lines. Structured
preflight truth is correctly retained, but the human presentation does not collapse the
same logical defect into one concise issue plus bounded corroborating-role attribution.

The raw record contains three legitimate hard preflight signals for the same placeholder
loss (`explicit-dnt-preservation`, `required_literal:{count}` and
`braced-placeholder-parity`) plus several model clusters. These may remain independently
auditable in full history, but primary text must not present them as repeated work items.

## Failed criterion 2 — false marginal discussion value

`council_value_metrics` reports:

- `discussion_new_evidence_count = 6`
- `discussion_position_change_count = 0`
- `discussion_resolved_issue_count = 0`
- `discussion_marginal_value = low`

All six discussion evidence strings restate facts already present before discussion:
the `{count}` requirement, the permanent-delete context, the `cannot` semantic reversal,
and existing style/project rules. New wording is not new structured evidence. The primary
report therefore makes a false value claim: `讨论补充 6 条新证据，未改变立场。`

This contradicts accepted F-041 and the audit rule that rephrased prose alone has no
marginal discussion value.

## Outer-agent reporting defect

The user initially labelled the valid Case B response as Case A, then supplied the actual
Case A record. Goose also returned reconstructed metric keys
such as `claims_added_by_council` rather than the literal Schema 2.4 fields. These outer-
agent statements are excluded from telemetry judgment. The persisted JSON is the source
of truth and remains complete. This does not require an MCP schema change, but future live
instructions should request only the review ID and primary report; Foreman can read the
record directly.

## Required correction

Issue CAMPAIGN-009-r1 as a bounded V0.10.1 correction:

1. Discussion evidence counts as new only when deterministic structured provenance can
   prove a new bounded anchor; unprovable or rephrased prose contributes zero.
2. Primary coverage groups corroborating and confirmation-only roles without repeating
   the same issue prose while naming every active role exactly once.
3. Chief primary text collapses multiple deterministic checks for one logical defect
   into one human work item while full history remains unchanged.
4. Preserve exact issue safety, model-only cross-family identity, raw clusters, Policy
   Gate authority, five tools, budgets, concurrency and Schema 2.4 compatibility.

Q-012 remains `CHANGES_REQUESTED`. Case C is not required on the known-failing build.
After the bounded correction is independently accepted and published, rerun a revised
live gate with clean and issue-rich cases.
