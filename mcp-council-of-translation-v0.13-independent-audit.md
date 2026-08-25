# mcp-council-of-translation V0.13 独立审计与修复建议

> Repository: `PigeonCrafty/mcp-council-of-translation`
> Audit baseline: product implementation `95d90cf383d045778ce61afaa50dbcec199579ce`
> Governance / acceptance baseline: `bcdb0e2bc282e907e975b43882906872913f6bec`
> Audit date: 2026-08-25
> Intended audience: Foreman Codex / implementation planning agent
> Audit type: Independent external-style review, not a restatement of internal Harness acceptance

---

## 1. Executive Summary

This audit independently reviewed the current V0.13 implementation of `mcp-council-of-translation`, including the production code paths for role routing, deterministic preflight, reviewer sampling, issue clustering, targeted discussion, DecisionPoints, user interaction, reconsideration, Policy Gate, chief-editor adjudication, persistence, verification receipts, decision-support calibration, Golden Corpus evaluation, and CI evidence.

The project has progressed materially since the previous review. It is no longer accurately described as a simple multi-agent review server. The current implementation is closer to a **structured localization deliberation and decision-support system**:

- professional roles are defined as bounded responsibilities rather than generic personalities;
- deterministic evidence is separated from model-generated evidence;
- model findings cannot self-promote into hard constraints or blockers;
- user choices are restricted to Policy-Gate-valid outcomes;
- role output, issue clustering, reconsideration, decision trace, coverage truth, decision-support sufficiency, and verification receipts are represented as structured artifacts;
- missing reviewer coverage and unresolved context conservatively tighten the disposition instead of being silently treated as clean evidence.

The project direction is therefore considered sound.

However, the current baseline should **not proceed directly into the next feature campaign**. One confirmed High-severity issue can produce a formally “well supported” or publishable disposition for content that the Council never reviewed because the public tool silently truncates long inputs before the review pipeline.

### Audit decision

**BLOCK NEXT CAMPAIGN**

This is not a recommendation to redesign V0.13. The required response should be a narrowly scoped **Audit Remediation Campaign**.

The blocking condition is primarily:

- **AUD-001 — High:** truncated input can still receive a complete disposition.

Other confirmed defects should preferably be resolved in the same remediation campaign:

- **AUD-002 — Medium:** deterministic preflight false positives for natural-language `%` patterns and URL punctuation;
- **AUD-003 — Medium:** malformed Targeted Discussion payloads can escape the safe degradation boundary;
- **AUD-004 — Medium:** discussion may resolve the Position Matrix without recomputing issue consensus state;
- **AUD-005 — Medium:** legacy V1 `summary` retrieval falls through to the full V1 payload;
- **AUD-006 — Medium evidence finding:** Golden Corpus metric names overstate what is actually measured;
- **AUD-007 — Low:** declared FastMCP compatibility range is broader than the versions actually validated.

Expected disposition after remediation:

- fixing only AUD-001 should be sufficient to move from `BLOCK` to at least `PASS WITH FINDINGS`;
- fixing AUD-001 through AUD-005 plus adding the proposed regression tests should make a full stage pass plausible.

---

# 2. Audit Scope and Baseline Integrity

The audit baseline was explicitly frozen.

Product implementation:

```text
95d90cf383d045778ce61afaa50dbcec199579ce
```

Current `main` / governance acceptance:

```text
bcdb0e2bc282e907e975b43882906872913f6bec
```

The two commits between those revisions were independently checked. The changed files are confined to Harness / acceptance assets, including:

```text
harness/contracts/*
harness/evaluations/*
harness/features.json
harness/plan.md
harness/progress.md
```

No production source code changed between the product release commit and the current governance baseline.

Therefore the audit can safely reason about:

```text
product behavior = 95d90cf
governance state = bcdb0e2
```

GitHub Actions also confirms that `bcdb0e2` passed the configured CI matrix:

```text
ubuntu-latest / Python 3.10
ubuntu-latest / Python 3.12
ubuntu-latest / Python 3.13
windows-latest / Python 3.10
windows-latest / Python 3.12
windows-latest / Python 3.13
```

The `main` branch requires those six checks.

One limitation must remain explicit: the external audit environment could inspect the repository through the GitHub integration and verify CI evidence, but could not directly clone `github.com` into the local execution container. Therefore this audit does **not** claim an independent local reproduction of the exact internal statement `480 passed`. It confirms that the configured CI `pytest -q` jobs succeeded.

---

# 3. What the Current Architecture Gets Right

Before the defects, several architectural properties should be treated as accepted and preserved.

## 3.1 RoleDefinition is now a real capability boundary

Current roles are no longer just prompt personas. `RoleDefinition` includes responsibility and authority fields such as:

```text
mission
scope
must_check
must_not_decide
evidence_policy
blocking_conditions
applicable_modes
applicable_content_types
discussion_policy
priority
```

This is a meaningful improvement.

The implementation also prevents sampled model output from manufacturing hard authority:

```text
evidence_origin = model
blocking = false
hard constraint tier -> advisory
```

This invariant should remain untouched during remediation.

## 3.2 Deterministic evidence and model evidence are correctly separated

The current architecture has a useful authority hierarchy.

Deterministic layers can establish:

```text
placeholder parity
printf placeholder parity
variables
commands
markup/tag integrity
URL preservation
explicit DNT literals
machine-readable hard constraints
```

Model findings can express:

```text
accuracy
fluency
terminology
context
style
UX
risk
technical observations
```

but sampled findings cannot self-declare a deterministic blocker.

This is one of the strongest parts of the current system and should not be weakened.

## 3.3 User authority is bounded rather than absolute

User choices operate only over valid DecisionPoint outcomes.

A proposed local replacement must be:

1. represented as a concrete bounded `proposed_value`;
2. associated with a provable candidate anchor;
3. applied to the complete candidate reconstruction;
4. rechecked against deterministic constraints;
5. rejected or suppressed if validation is ambiguous or unsafe.

This prevents a user preference from bypassing protected technical material.

## 3.4 Reviewer coverage truth is conservative

Reviewer envelope validation is semantic, not merely JSON syntactic success.

Invalid or malformed review output does not count as clean evidence.

The current design distinguishes:

```text
full coverage
partial coverage
no coverage
```

Partial/no coverage forces human review rather than allowing “missing reviewer output” to become evidence of absence.

This is correct.

## 3.5 Decision-support is directionally correct

The current `DecisionSupportAssessment` is explicitly categorical rather than probabilistic:

```text
well_supported
supported_with_limits
insufficient
```

It is based on structured trace facts rather than model self-confidence or vote counts.

Most importantly, insufficient support can tighten a permissive chief disposition, while support classification cannot relax Policy Gate or deterministic blockers.

That asymmetry should be preserved.

## 3.6 Verification availability semantics are correctly conservative

The verification projection checks whether fields were physically recorded rather than blindly trusting Pydantic defaults.

Historical / metadata-only missing facts are represented as:

```text
null
not_recorded_fields
```

instead of being reconstructed from default empty values.

This avoids a subtle but serious historical-truth bug and should remain unchanged.

---

# 4. Findings Summary

| ID | Severity | Type | Summary | Blocks Next Campaign |
|---|---|---|---|---|
| AUD-001 | **High** | Confirmed production defect | Truncated input can still receive a full publishability disposition | **Yes** |
| AUD-002 | Medium | Confirmed deterministic false positive | Preflight regex can misclassify natural language as protected technical tokens | No |
| AUD-003 | Medium | Confirmed robustness defect | Malformed discussion payload can escape graceful degradation | No |
| AUD-004 | Medium | Confirmed trace-consistency defect | Discussion can resolve positions without updating consensus state | No |
| AUD-005 | Medium | Confirmed privacy/data-minimization defect | V1 `summary` returns full V1 record | No |
| AUD-006 | Medium | Evaluation evidence gap | Golden metrics are narrower than their names imply | No |
| AUD-007 | Low | Compatibility risk | FastMCP declared range exceeds independently validated range | No |

---

# 5. AUD-001 — High — Truncated Input Can Still Receive a Full Disposition

## 5.1 Problem

The public tool boundary caps source and candidate fields at approximately 12,000 characters.

The tool records:

```text
source_original_length
source_reviewed_length
source_truncated
candidate_original_length
candidate_reviewed_length
candidate_truncated
```

However, the actual review pipeline operates only on the sanitized / truncated strings.

The downstream system does not currently convert:

```text
source_truncated = true
candidate_truncated = true
```

into a disposition constraint.

The following layers therefore evaluate only the truncated prefix:

```text
preflight
independent reviewers
context analysis
clustering
discussion
DecisionPoints
Policy Gate
chief adjudication
decision_support
```

while the final operational disposition may still describe the entire caller-supplied source/candidate pair.

## 5.2 Why This Is High Severity

This is not merely “long-document model recall may be weak.”

The system deterministically knows that part of the input was never reviewed.

A minimal adversarial example is:

```text
SOURCE:
[A repeated until the input limit]
Do not delete this data.

CANDIDATE:
[A repeated until the input limit]
删除这些数据。
```

If the meaningful defect lies outside the retained prefix, the actual review task presented to the Council no longer contains it.

The reviewed prefix can therefore produce:

```text
Preflight clean
All reviewers clean
No issue clusters
Full coverage
Clean confirmation
Chief publishability = 可发布
```

even though the complete caller input contains an unreviewed critical defect.

This creates a false completeness claim at the disposition layer.

## 5.3 Required Remediation

The remediation campaign should choose one of two safe policies.

### Preferred V0.13 remediation: fail closed / require human review

If either input was truncated:

```text
record.degraded = true
warning += input_truncated
decision_support = insufficient
chief.publishability = 需人工复核
chief.review_needed = 是
status = NEEDS_HUMAN_REVIEW
```

The primary report should visibly state that the review covered only a bounded prefix.

The compact structured response should expose this fact directly or through a stable warning/fallback code.

Suggested bounded codes:

```text
input_truncated
source_input_truncated
candidate_input_truncated
```

Avoid free-form host-sensitive strings.

### Alternative strict policy: reject incomplete reviews

The tool may reject input larger than the supported complete-review limit:

```text
INPUT_TOO_LARGE_FOR_COMPLETE_REVIEW
```

This is architecturally cleaner than silent truncation, although less convenient.

## 5.4 Not Recommended in This Campaign

Do not expand this remediation into a full long-document architecture unless explicitly approved.

Do not add:

```text
chunking
cross-chunk issue synthesis
chunk overlap
document-level alignment
multi-segment aggregation
```

as part of the audit fix.

Those belong to a separate feature campaign.

## 5.5 Acceptance Criteria

Add deterministic tests covering at least:

```text
source only truncated
candidate only truncated
both truncated
critical defect located beyond limit
clean prefix + unsafe omitted suffix
```

Required assertions:

```text
publishability != 可发布
review_needed == 是
status == NEEDS_HUMAN_REVIEW
decision_support.level == insufficient
degraded == true
stable truncation warning/fallback is present
compact response makes truncation visible
verification receipt does not misrepresent complete review
```

No test may accept a “clean” terminal disposition when any reviewed input is incomplete.

---

# 6. AUD-002 — Medium — Deterministic Preflight False Positives

## 6.1 Problem A: printf placeholder scanner

The current printf pattern allows a literal space as a flag.

This can classify ordinary natural-language percentages as printf tokens.

Examples:

```text
100% safe
50% discount
25% off
Save 100% safely
```

may yield token-like matches such as:

```text
% s
% d
% o
```

A translated sentence that naturally removes the following English character can then appear to violate printf placeholder parity.

Example:

```text
Source:    100% safe
Candidate: 100% 安全
```

Possible result:

```text
printf_placeholder_parity
severity = critical
blocking = true
```

This is a deterministic false positive.

## 6.2 Problem B: URL punctuation

The URL regex can absorb sentence-final punctuation.

Example patterns:

```text
Visit https://example.com.
请访问 https://example.com。
```

can produce different literal URL matches solely because punctuation changed with localization.

This can incorrectly trigger URL preservation failure.

## 6.3 Why This Matters

Preflight evidence has stronger authority than model evidence.

A false positive at this layer is not merely a suggestion; it can force:

```text
blocking issue
Policy Gate failure
human review
```

Therefore deterministic scanners require higher precision than normal heuristic checks.

## 6.4 Required Remediation

Refine token recognition conservatively.

The implementation should distinguish:

```text
printf syntax
ordinary percentage prose
URL literal
sentence punctuation
slash command
ordinary slash text
```

The exact regex strategy is implementation-specific; the required outcome is behavioral.

## 6.5 Add a Dedicated Negative Corpus

At minimum cover:

```text
100% safe
50% discount
25% off
100% satisfied

https://example.com.
https://example.com,
https://example.com)
https://example.com。
https://example.com，

localized punctuation around URLs
parenthesized URLs
URLs before Chinese punctuation

ordinary slash prose
path-like text that is not an executable command
percentage + plural noun
percentage + adjective
```

The negative tests should assert:

```text
no deterministic blocker
no false protected-token mismatch
```

Do not weaken legitimate cases such as:

```text
%2$s
%d
%.2f
{name}
${APP}
/help
--force
```

---

# 7. AUD-003 — Medium — Discussion Output Is Not Fully Inside the Safe Degradation Boundary

## 7.1 Problem

Independent reviewer output is carefully validated.

Malformed reviewer output becomes:

```text
unavailable sample
missing evidence
coverage degradation
```

without crashing the whole review.

Discussion does not have equivalent envelope validation.

The workflow effectively assumes:

```json
{
  "turns": [
    { ... valid turn dict ... }
  ]
}
```

A malformed but valid JSON response such as:

```json
{
  "turns": ["bad"]
}
```

can reach logic that assumes each element has `.get(...)`.

This can raise an exception rather than treating the discussion as unavailable.

Similarly, malformed individual `DiscussionTurn` values can potentially escape without a local conservative fallback.

## 7.2 Required Remediation

Add a discussion-envelope parser analogous to reviewer-envelope validation.

Suggested behavior:

```text
invalid top-level turns container
    -> discussion unavailable
    -> preserve pre-discussion matrix
    -> bounded warning/fallback
    -> continue review

invalid turn entry
    -> discard invalid entry
    or reject entire discussion envelope conservatively
    -> do not alter matrix

invalid position change
    -> ignore change
    -> do not escalate authority
```

Discussion failure must never invalidate otherwise usable independent review evidence.

## 7.3 Acceptance Criteria

Add cases:

```text
turns missing
turns = null
turns = string
turns contains string
turns contains integer
turn missing issue_id
turn invalid stance
turn invalid confidence
turn references unknown role
turn references unknown issue
position_changed with unknown candidate action
```

Required invariant:

```text
workflow completes safely
pre-discussion positions remain authoritative when discussion invalid
no new blocker is created
failure is represented as bounded degradation/trace
```

---

# 8. AUD-004 — Medium — Discussion Can Resolve Positions Without Updating Consensus State

## 8.1 Problem

The discussion layer can update a role’s Position Matrix row.

Example:

```text
Before discussion:
terminology -> option A
fluency     -> option B

After discussion:
terminology -> option B
fluency     -> option B
```

The final matrix is now converged.

However, the issue object can retain the original:

```text
consensus_status = disputed
needs_user_input = true
```

because discussion update logic changes `cluster.positions` but does not recompute issue-level state.

## 8.2 Inconsistency

This creates contradictory structured evidence.

`CouncilValueMetrics` independently checks the final Position Matrix and can detect:

```text
discussion_resolved_issue_count = 1
```

while the digest can still read:

```text
material_disagreements = [same issue]
```

because it trusts stale `cluster.consensus_status`.

The same stale state may also affect:

```text
decision_support limitation_codes
DecisionPoint creation
minority report
display report disagreement wording
```

## 8.3 Recommended Model Change

Do not simply set `needs_user_input = false` whenever roles converge.

Two concepts should be separated:

### Role consensus

```text
Do current participating roles materially agree?
```

### User-choice usefulness

```text
Do multiple Policy-valid language outcomes still exist where user preference/context is useful?
```

These are not equivalent.

Example:

```text
roles unanimously recommend "继续"
but "下一步" is also technically valid
```

It is coherent to represent:

```text
role consensus = consensus
user preference point = still available
```

## 8.4 Minimum Remediation

After applying discussion updates, recompute at least:

```text
final distinct option IDs among material participants
consensus_status
```

Then ensure digest, decision-support, minority report, and value metrics derive disagreement from the same post-discussion truth.

If `needs_user_input` remains independent, document that explicitly.

## 8.5 Acceptance Criteria

Add a production-path test where discussion changes one role and makes all relevant positions identical.

Required assertions:

```text
final Position Matrix has one option
discussion_resolved_issue_count == 1
issue.consensus_status == consensus
same issue absent from material_disagreements
decision_support does not retain material_disagreement solely from stale pre-discussion state
```

If a user DecisionPoint is intentionally still shown, add a test proving that it exists because multiple valid outcomes remain, not because the Council is still classified as disputed.

---

# 9. AUD-005 — Medium — V1 Summary Retrieval Returns Full Legacy Payload

## 9.1 Problem

The public tool claims three detail levels:

```text
full
summary
verification
```

V2 summary correctly uses a compact projection.

V1 summary does not.

The current branch logic is effectively:

```text
if V2 and summary:
    compact response

otherwise:
    full model_dump()
```

Therefore:

```text
V1 + detail_level="summary"
```

returns the full V1 record.

Legacy V1 records can contain:

```text
task
reviews
conflict_reviews
chief_editor_decision
```

which is inconsistent with the documented data-minimization semantics of a summary request.

## 9.2 Required Remediation

Implement a legacy compact projection.

Suggested V1 summary fields:

```text
schema_version
review_id
mode
status
publishability
review_needed
```

Optionally include only bounded non-prose metadata that is clearly safe.

Do not include:

```text
source/candidate
task free text
raw reviewer prose
conflict reviewer prose
full chief rationale
```

## 9.3 Acceptance Criteria

Add:

```text
V1 + full        -> existing complete compatible payload
V1 + summary     -> bounded compact legacy projection
V1 + verification -> existing privacy-safe receipt
```

Explicitly assert that V1 summary does not contain task or review prose.

---

# 10. AUD-006 — Medium Evidence Finding — Golden Metrics Need Calibration

## 10.1 What Is Good

The current Golden Corpus infrastructure is substantially better than fixture-only assertion testing.

The evaluator traverses the real production orchestration path and mutation tests rerun the actual system.

This should be kept.

## 10.2 Problem

Some metric names imply more than the implementation measures.

### `critical_issue_recalled`

Current logic is effectively:

```text
Did any critical or blocking cluster exist?
```

It does not prove:

```text
Did the system recall the expected critical defect identity?
```

A wrong critical finding can satisfy the metric while the intended defect is missed.

### `false_positive_free`

For clean cases:

```text
no cluster == pass
```

For non-clean cases the current metric is effectively always true.

Therefore an input with one expected defect plus several invented false findings may still be considered false-positive-free.

## 10.3 Required Response

This is not a release blocker and does not require production behavior changes.

Choose one of:

### Option A — rename metrics conservatively

Examples:

```text
critical_presence_contract_accuracy
clean_case_no_cluster_accuracy
```

### Option B — strengthen the evaluation model

For blind evaluation cases record expected structured identity:

```text
expected issue family
expected source span or bounded span range
expected candidate span
severity range
allowed alternative interpretations
forbidden findings
```

Then score:

```text
defect identity recall
span overlap
severity calibration
false positive count
duplicate finding ratio
```

## 10.4 Strong Recommendation

Do not solve this only by increasing the Golden Corpus from 30 to 50 or 100 handcrafted cases.

The next meaningful evaluation asset should be an independently curated **blind evaluation set** that is not continuously shaped by the same implementation loop.

---

# 11. AUD-007 — Low — Declared FastMCP Compatibility Range Exceeds Validation Evidence

Current package dependency:

```text
fastmcp>=2.13.0.2
```

This allows future major versions.

Current stage evidence validates specific contemporary FastMCP behavior, but does not establish compatibility with every version permitted by the package declaration.

This is an engineering risk rather than a current production defect.

Possible responses:

```text
pin tested major range
```

for example:

```text
fastmcp>=3.x,<4
```

or add compatibility CI against:

```text
declared minimum
current tested version
latest compatible version
```

Do not change this blindly if downstream Goose environments rely on the current range; first inspect actual supported client/runtime constraints.

---

# 12. Targeted Discussion: Clarify the Product Semantics

Current Targeted Discussion is a real executable phase, but its semantics should be described accurately.

It is not a sequence of independently sampled reviewers replying to each other.

The current pattern is closer to:

```text
IssueCluster + Position Matrix
        |
        v
one bounded model sample
        |
        v
multiple speaker / target / stance turns
        |
        v
Core validates allowed position changes
        |
        v
updated Position Matrix
```

This is best described as:

**single-sample simulated cross-role deliberation**

rather than:

**independent agents actually debated each other**

This is not necessarily a weakness.

For a localization QA system it may be the better cost/latency/redundancy tradeoff.

However, evaluation and product documentation should not treat Round 2 discussion evidence as having the same independence as Round 1 independent reviewer samples.

No architectural change is required in the remediation campaign unless the product documentation currently makes stronger independence claims.

---

# 13. Recommended Remediation Campaign

Create a dedicated campaign, for example:

```text
CAMPAIGN-014-audit-remediation
```

or equivalent project naming.

The campaign should explicitly **not** include new product capabilities.

## 13.1 Mandatory scope

```text
AUD-001
AUD-002
AUD-003
AUD-004
AUD-005
```

## 13.2 Evidence scope

```text
AUD-006 metric calibration / blind-set design
```

## 13.3 Optional engineering cleanup

```text
AUD-007 dependency compatibility range
```

## 13.4 Explicit non-goals

Do not add in this campaign:

```text
new reviewer roles
new content types
generic adaptive Council
new provider integrations
long-document chunking
A2A integration
new UI
new editing capability
translation generation
extra voting
multi-round debate
new context MCP coupling
```

The purpose of this campaign is to restore and tighten truthfulness boundaries.

---

# 14. Suggested Implementation Order for Foreman Codex

## Phase 1 — Reproduce Before Fixing

For each AUD-001 through AUD-005:

1. write one or more failing regression tests against the current behavior;
2. confirm the tests fail for the intended reason;
3. preserve them as permanent regression assets.

Do not patch production code before establishing the failing tests.

## Phase 2 — Fix AUD-001 First

This is the only blocking issue.

Recommended implementation target:

```text
input completeness becomes an explicit disposition invariant
```

After AUD-001 passes, run:

```text
unit
integration
Golden Corpus
verification
persistence
tool surface
```

before proceeding.

## Phase 3 — Fix Deterministic and Robustness Boundaries

Order:

```text
AUD-002 preflight precision
AUD-003 discussion degradation
AUD-004 consensus truth
AUD-005 V1 summary
```

These are largely orthogonal and should not require major refactoring.

## Phase 4 — Evaluation Calibration

Review AUD-006 separately.

Do not mix evaluation nomenclature changes with adjudication logic unless necessary.

Produce a short design artifact for future blind evaluation.

## Phase 5 — Re-Audit Gate

Before opening the next feature campaign, require:

```text
all regression tests pass
CI matrix green
Golden Corpus remains green
no newly introduced permissive fallback
no verification privacy regression
no schema compatibility regression
audit remediation report completed
```

---

# 15. Required Invariants After Remediation

The following invariants should be treated as release gates.

## Input completeness

```text
The system must never represent an incomplete review as a complete review.
```

## Deterministic authority

```text
Only sufficiently precise deterministic checks may create deterministic blockers.
```

## Model authority

```text
Sampled model output cannot manufacture hard constraints or deterministic blockers.
```

## Discussion failure

```text
A malformed discussion cannot destroy valid Round 1 evidence or crash the review.
```

## Trace truth

```text
Position Matrix, consensus status, disagreement digest, decision support, and value metrics must describe the same post-discussion state.
```

## User authority

```text
Users may choose only among Policy-valid outcomes.
```

## Reviewer availability

```text
Missing reviewer output is missing evidence, never positive evidence.
```

## Historical truth

```text
Compatibility defaults are not historical facts.
```

## Retrieval minimization

```text
summary means summary for every supported schema version.
```

## Support calibration

```text
Insufficient evidence may tighten a result but may never relax a blocker.
```

---

# 16. Proposed Regression Test Matrix

The remediation campaign should add at least the following cases.

## Input truncation

```text
source > limit
candidate > limit
both > limit
defect after retained prefix
truncated clean prefix
truncated input + full reviewer coverage
truncated input + otherwise well_supported decision support
```

## Preflight negative cases

```text
100% safe
50% discount
25% off
100% satisfied
URL + period
URL + comma
URL + Chinese period
URL + Chinese comma
URL in parentheses
ordinary slash prose
```

## Discussion malformed output

```text
turns missing
turns null
turns string
turn entry string
turn entry integer
unknown role
unknown issue
invalid stance
invalid proposed action
invalid confidence
```

## Discussion state coherence

```text
disputed -> discussion convergence -> consensus
resolved count = 1
no stale material disagreement
DecisionPoint semantics explicitly checked
```

## Legacy summary

```text
V1 full
V1 summary
V1 verification
```

---

# 17. Re-Audit Decision Criteria

After remediation, use the following decision logic.

## PASS

All true:

```text
AUD-001 fixed
AUD-002 through AUD-005 fixed or demonstrated non-reproducible
new regression tests present
CI matrix green
Golden Corpus green
no Critical/High findings
no privacy regression
no new disposition inconsistency
```

## PASS WITH FINDINGS

Acceptable if:

```text
AUD-001 fixed
no Critical/High issues remain
one or more Medium/Low non-permissive issues remain
their behavior is bounded and documented
```

## BLOCK

Any true:

```text
incomplete review can still be publishable
deterministic false evidence can bypass or corrupt authority
model output can create hard authority
missing reviewer evidence can become positive evidence
malformed model output can produce unsafe disposition
verification exposes protected prose unexpectedly
user choice can override deterministic constraints
```

---

# 18. Product-Level Assessment

The current project should no longer be treated as a conventional “multiple reviewers vote on a translation” MCP.

A more accurate description is:

> A structured localization deliberation and decision-support runtime that collects bounded role evidence, distinguishes deterministic and model authority, exposes material disagreements, optionally elicits human judgment, applies policy constraints, and produces an auditable chief-editor disposition.

This positioning is supported by the current implementation.

The remaining work is increasingly less about adding more reviewers and more about protecting the semantic integrity of the evidence system itself.

That changes engineering priorities.

For the next stage, truthfulness properties such as:

```text
what was actually reviewed
what was not reviewed
what was deterministic
what was model-derived
what evidence was missing
what the user decided
what changed after discussion
why the final disposition is allowed
```

should receive higher priority than adding new capabilities.

---

# 19. Final Audit Verdict

**Current verdict: BLOCK NEXT CAMPAIGN**

Reason:

```text
AUD-001 allows a Council disposition to cover input content that was deterministically omitted before review.
```

This breaks the central product promise of an evidence-supported disposition.

At the same time, the architecture itself is judged to be on the correct path and does not require broad redesign.

Recommended action:

> Freeze feature development temporarily and execute a narrow Audit Remediation Campaign covering AUD-001 through AUD-005, then perform a short re-audit before opening the next feature campaign.

The foreman Codex should first convert this report into a bounded implementation plan with failing regression tests and explicit acceptance gates, rather than directly modifying production code.
