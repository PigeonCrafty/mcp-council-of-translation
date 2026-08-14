# Foreman Review: CAMPAIGN-008-r4

## Decision

`ACCEPTED`

CAMPAIGN-008-r4 correctly preserves production identity for reviewer-only issues while
retaining all accepted deterministic-preflight correlation. Combined r1-r4 evidence now
satisfies F-040 through F-044 and closes the local V0.10 implementation Campaign.
Publication and live Q-012 remain separate gates.

## Control and scope

- Role: FOREMAN
- Mode: STRICT_CAMPAIGN
- Contract: `harness/contracts/CAMPAIGN-008-r4.md`
- Contract SHA-256:
  `6A7B8F48BA20005174D0BF5871D3073BA72CEC9694B7D7C3F9193D296D35F3A7`
- Baseline: `c3fcfec363878d069b64e15a65a364c7fd55468b`
- Accepted implementation HEAD: `84c6c64d40836875cf6515a6bf0c615c9e5ea0c9`
- Commit: `84c6c64 Preserve model-only issue identity`
- Diff: exactly two authorized paths, 59 insertions and one deletion
- Git index: empty; `git diff --check` passed
- Worker report SHA-256:
  `533EB12D5D50BF85E3CB98354BB6EA7A1A23468A15E93AA4DFEA637CCAB170E0`
- All contract-protected hashes independently matched

## Independent r4 verification

- Source and complete baseline-to-final diff inspected. The implementation freezes the
  deterministic-rooted group prefix before reviewer attachment; reviewer-only groups can
  no longer become alias match targets for later reviewer clusters.
- Fresh compile passed.
- Fresh complete regression: `278 passed in 4.99s`.
- Fresh exact-correlation/reviewer-identity focus: `19 passed in 0.24s`.
- Fresh V2.4 model, persistence, metrics, presentation and Golden selection:
  `30 passed in 0.52s`.
- Fresh public/compatibility/concurrency selection: `33 passed in 1.65s`.
- Exact five tools, package/module `0.10.0`, build `evidence-value-council-v8`, schema
  `2.4` and budgets 6/13/18 independently matched.

## Counterexample results

- Cross-family model-only findings at identical `Continue` / `继续` anchors remain two
  production clusters and two unique material issues; fidelity and terminology each own
  one unique contribution.
- Same-family fidelity/risk findings remain one production cluster and one corroborated
  issue; both roles remain corroborating.
- A mixed three-role probe retains two production issues: one unique correctness issue
  and one corroborated language-choice issue.
- Required/forbidden literals, numeric parity, four Markdown signals, explicit DNT,
  URL command/full-URL overlap, placeholders, tags and unavailable technical sampling
  preserve the accepted r3 counts.
- Placeholder plus URL remains two issues, and two distinct caller literals remain two;
  common role/category alone does not merge them.
- Metric computation does not mutate clusters or add sampling/elicitation.

## Campaign 008 integrated acceptance

### F-040 — deterministic Council contribution metrics

Accepted. Active roles receive bounded `unique_material`, `corroborating`,
`confirmation_only` or `unavailable` classifications from validated structured artifacts.
Production model-cluster identity and preflight-rooted exact aliases prevent both repeated
inflation and cross-family overmerge. Metrics remain descriptive and do not affect Policy
Gate authority.

### F-041 — marginal discussion value telemetry

Accepted. Only bounded new evidence, validated position changes and real issue resolution
produce marginal value; rephrased prose alone produces none. Construction adds no call.

### F-042 — value-first concise Council presentation

Accepted. The primary five-section report leads with material additions, compresses
confirmation, visibly accounts for roles, preserves blockers/minority/context/degradation
and keeps the chief disposition last. Full structured history remains intact.

### F-043 — executable 18-case Golden evaluation framework

Accepted. The fixture contains exactly 18 declarative input/expectation cases and no
authored observations. The runner executes real review orchestration and continuation
with deterministic gateways. Fresh Foreman execution returned 18/18, 113 scripted
samples, four scripted elicitations, no failed case and all eight aggregate metrics 1.0.

### F-044 — V0.10 evidence-value migration

Accepted. Version/build/schema, five tools, 6/13/18 budgets, concurrency controls,
review-only behavior and V1/V2.0-V2.3 compatibility are preserved. Worker produced fresh
wheel/sdist and isolated Python 3.12/FastMCP 3.4.7 five-tool smoke; hashes are recorded in
the r4 Worker report.

## Evidence provenance and risks

- Combined implementation spans r1 through r4; each revision has a durable Worker report
  and independent Foreman evaluation.
- Subagents in r4: 0
- Foreman production/test edits: 0
- Live Goose/provider/model calls: 0
- Push/PR/release/deployment actions: 0
- The failed direct diagnostic calls during Foreman verification were harness invocation
  mistakes against a FastMCP `FunctionTool`; corrected inspection through `.fn()` and
  focused tool tests passed. `.learnings/` remained untouched because it is protected.
- Deliberately exact correlation may leave semantically similar model prose separate when
  production clustering supplies no shared structured identity. This is conservative and
  preferable to prohibited fuzzy/prose scoring.
- Live user-perceived usefulness, non-repetition and provider behavior remain unverified
  until published V0.10 passes Q-012 in normal Goose.

## Next gate

Archive the accepted Harness assets and publish the accepted implementation through the
repository's protected-main workflow. After publication, run Q-012 against a pinned
published commit using normal Goose configuration; do not change the extension command
between cases.

