# Live Goose Review: CAMPAIGN-006 Q-010 r2

## Control

- Role: FOREMAN
- Gate: `Q-010` context-coherent panoramic Council live evidence
- Decision: `ACCEPTED`
- Tested published build: package/module `0.8.0`, diagnostic build
  `context-coherent-council-v6`, schema `2.2`
- Revalidation review ID: `20260813T031756071915Z_bb184d020ab1`
- Prior evidence: `harness/evaluations/CAMPAIGN-006-q010-live-review.md`
- Evidence boundary: the user-supplied live primary report is accepted as Goose UX
  evidence; Goose's later prose reconstruction of hidden fields is not accepted as
  literal structured telemetry.

## Live unresolved-context result

The required mixed marketing/UI case was rerun with `interactive_mode="off"`. Its first
tool response directly demonstrated the conservative unresolved branch:

- all six intended marketing perspectives remained visible;
- `context_confidence` was lowered to `minimal`;
- two outcome-changing brand-slogan-versus-functional-button questions remained visible
  as `未回答背景` blind spots;
- no `你的决定与复议` section or user outcome appeared;
- the chief explicitly stated that the wording could not be safely adjudicated before
  confirming the usage;
- the final disposition was `需人工复核；需人工复核：是`;
- wall-clock time reported by the live run was 15.31 seconds.

These are the user-visible acceptance outcomes required by Q-010. Together with the
prior clean run and mixed auto-interaction run, live evidence now covers clean contextual
coherence, material-gap detection, and conservative handling when the gap cannot be
answered.

## Structured-channel audit boundary

Goose reported that `view_review_record(detail_level="full")` exposed only the Markdown
primary text. That is a client/agent visibility limitation, not server-side JSON
suppression or a locked persistence store.

At the accepted published source, `review_translation`, `continue_review`, and
`view_review_record` return a FastMCP `ToolResult` with both:

1. bounded Markdown in `content`; and
2. the unchanged JSON-safe record in `structured_content`.

Fresh Foreman verification of the actual FastMCP path and conservative context workflow
passed 20 tests. The tested invariants include dual-channel review/view results and the
unresolved branch's literal status, warning, fallback, no-outcome and chief-review fields.

The following Goose prose claims are rejected because they are not valid V0.8 record
values and conflict with the displayed primary report:

- `context_gap_interaction.action="none"` — `none` is not a valid action; an off-mode
  selected gap uses `unsupported`;
- `status="COMPLETED"` — unresolved material context with a chief human-review decision
  yields `NEEDS_HUMAN_REVIEW`;
- `degraded=false`, empty warnings and null fallback — this path records degradation,
  `material_context_unresolved` warning and fallback provenance.

The gate does not require changing the server to duplicate the entire record in its
human text merely because Goose did not expose `structured_content` to the outer model.
The concise Council report remains the intended primary user experience.

## Latency finding

The 15.31-second run confirms that the expensive portion is live provider sampling, not
local record lookup or Markdown rendering. V0.8 awaits the six independent role samples
sequentially. Answered context gaps add sequential affected-role reconsiderations; an
optional discussion and outcome reconsiderations can add more. The earlier mixed auto
run visibly completed two background reconsiderations and therefore required at least
eight model samples, while the off-mode revalidation avoided those two calls.

History reads and deterministic aggregation are local operations and are not a plausible
explanation for the large difference between the live paths. Goose's additional
diagnostic calls and its own final prose generation can extend the perceived end-to-end
time, but provider round trips dominate the Council tool runtime.

## Decision

`Q-010` is `ACCEPTED`. Campaign 006 is closed: repository implementation, publication,
clean presentation, six-role marketing coverage, material context detection, and the
non-interactive conservative fallback have all been independently or live verified.

Remaining product opportunity, not a Campaign 006 defect: reduce latency by executing
independent role samples with bounded concurrency while retaining sequential phase
boundaries for context handling, discussion, Policy Gate and reconsideration. This needs
a separate design and live provider compatibility gate.
