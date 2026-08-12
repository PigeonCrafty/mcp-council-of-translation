# Live Goose Review: CAMPAIGN-004 Q-009

## Control

- Role: FOREMAN
- Gate: `Q-009` process-first digest usability
- Decision: `CHANGES_REQUESTED`
- Published build: `2bf090ac368c7b8af24b51ff534a145f88752ad0`
- Live review ID: `20260812T131614836886Z_e815e1cbf65f`
- Evidence: user-supplied first and second Goose answers plus independent read of the local persisted V2.2 record

## Accepted live evidence

- The first normal-user answer directly displayed the primary Council report; no second history prompt was needed to discover the process.
- The report used four Chinese sections in the frozen order and ended with the final disposition.
- All six professional roles appeared exactly once with distinct role ownership.
- Positive consensus truthfully supported retaining `继续`; no material disagreement was fabricated.
- Empty decision/reconsideration sections were omitted.
- The persisted display report is 1,184 Unicode code points; estimated primary text with footer is 1,257, below the 1,800 clean target.
- Review-only held: `suggested_translation` is null.
- Record status is `COMPLETED`, reviewer coverage is full, six samples succeeded and zero were unavailable.
- No raw issue/cluster/position/decision/option/gap identifier appeared in the display report.

## Independent corrections to the Goose audit

The second Goose answer incorrectly reported `sampling_calls: 0`. The persisted record contains:

- `sampling_calls: 6`;
- `sample_budget: 13`;
- `reviewer_samples_successful: 6`;
- `reviewer_samples_unavailable: 0`;
- `elicitation_calls: 1`.

This is an outer-agent audit-summary error, not a Council execution or persistence error.

The Goose answer also reported 1,281 characters. The persisted `display_report` is 1,184 code points; the server primary text including its review-ID footer is approximately 1,257. Either remains within contract bounds.

## Remaining presentation defects

1. The primary chief-editor section still exposes procedural telemetry: `用户有效选择 0 项，Council fallback 0 项，人工复核 0 项；未使用票数多数`. This violates the frozen rule that unnecessary Policy Gate counters and internal adjudication jargon do not appear in primary text.
2. Clean affirmative role lines attach evidence that repeats the perspective and leaks implementation vocabulary such as `Preflight`, `placeholder_parity`, `tag_integrity`, `Effective Brief` and `Context`.
3. Several evidence anchors are cut mid-expression with an ellipsis, reducing readability rather than adding actionable evidence.
4. The literal microcopy `约束审查 后裁决` contains an unnatural space and still describes process mechanics instead of the user-relevant synthesis.

## Decision rationale

The core Q-009 objective is materially achieved: the Council process is visible in the first normal answer and is far shorter and clearer than V0.6. Formal acceptance is withheld because the live output contradicts the explicit primary-text integrity requirement and still carries avoidable implementation noise in the exact clean case that should be the simplest presentation.

## Bounded recommended correction

- Keep the full `editor_synthesis` and evidence in structured content, but suppress procedural counter lines from primary text.
- For clean affirmations, show the role-specific perspective without a redundant evidence suffix; retain evidence for blockers, material choices, minority conditions and unavailable coverage.
- Map or suppress known implementation labels before rendering and avoid cutting an evidence anchor mid-token or mid-clause.
- Preserve the current five tools, schema 2.2, 6/13/18 budgets, dual-channel structure, report limits, review-only behavior and all accepted Campaign 004 logic.

No production-code change is authorized by this evaluation alone. A new bounded Foreman contract requires user approval.
