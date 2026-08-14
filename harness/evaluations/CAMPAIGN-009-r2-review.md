# Foreman Review: CAMPAIGN-009-r2

## Decision

`ACCEPTED`

- Role/mode: `FOREMAN`, `STRICT_CAMPAIGN`
- Contract: `harness/contracts/CAMPAIGN-009-r2.md`
- Contract SHA-256: `4E4158537F4FDB2CAEE2C0E2B4F3F5594A6FB6DD3FA5E81BBE9437F95A3DA759`
- Baseline: `62f2ee9bf1860f80281afbbad53734db5f700205`
- Accepted implementation HEAD: `4a3c692ad528db03e4f72a025d60c4eb775454f0`
- Worker report: `harness/reports/CAMPAIGN-009-r2-worker.md`
- Worker report SHA-256:
  `0773EF58312E333957C65714CA485FEBF1136F5D35130ECCF43064F218670807`

Both bounded r1 counterexamples are corrected without weakening the accepted V0.10.1
behavior or changing frozen release inputs. CAMPAIGN-009-r2 and the combined r1/r2 local
implementation are accepted. Q-012 remains a separate post-publication normal-Goose gate.

## Scope and integrity

- Exactly two commits and four authorized paths changed from the r2 baseline.
- Git index was empty; baseline-to-final `git diff --check` passed.
- All ten protected assets matched the r2 contract.
- No docs, lock, package metadata, schema, prompts, roles, routing, clustering, Policy
  Gate, persistence, dependencies or public tools changed.
- No subagents, external/network operations, live provider calls, pushes, PRs, releases
  or deployments occurred.

## Independent verification

- Fresh compile: passed.
- Fresh complete suite: `286 passed in 3.73s`.
- Fresh risk-weighted V2.4/r1 A-B/Golden/release selection: `50 passed in 1.30s`.
- Fresh provenance probes proved existing raw and repeatedly prefixed rule provenance
  yields zero new evidence, while an absent valid marker yields exactly one.
- Fresh presentation probe proved the disputed `trial` -> `正式版` authorization topic
  appears exactly once, both corroborating role names appear once, the decisive condition
  remains, final disposition is last, and digest/cluster JSON is unchanged.
- Frozen invariants passed: package/module `0.10.1`, build
  `evidence-value-council-v8.1`, schema `2.4`, exact five tools, budgets 6/13/18 and
  concurrency default/max 3/3.
- Modified production modules contain zero sampling or elicitation call sites.

## Acceptance by package

### PKG-053 — accepted

Raw and already-prefixed typed rule/constraint values canonicalize to the same bounded
provenance identity used by discussion evidence. Existing provenance no longer creates
false marginal value; absent valid provenance still counts once. Malformed and prose-
embedded markers remain ineligible, and natural-language novelty stays conservatively
undercounted.

### PKG-054 — accepted

Corroborating groups now include a bounded material topic as well as role attribution and
optional anchors. Topic deduplication occurs only after the topic was actually emitted,
so a material disagreement cannot disappear behind an anchor-only label. r1 A/B grouping,
minority conditions, structured-history immutability and report bounds remain green.

## Preserved Campaign evidence

- r1 A: one grouped six-role confirmation line and clean output below 1,200 code points.
- r1 B: discussion value zero, one primary `{count}` work item, distinct semantic
  reversal and unchanged full structured evidence.
- Golden Corpus: exact 18/18, 113 scripted samples, four elicitations and all eight
  aggregate metrics at 1.0.
- Accepted r1 package/wheel/lock evidence remains applicable because r2 changed only the
  two production projections and their tests, as explicitly frozen by the contract.

## Remaining risk and next gate

Bounded exact provenance deliberately undercounts unprovable natural-language novelty,
and exact topic projection may show semantically related non-identical statements rather
than risk hiding an issue. These are intended conservative behaviors.

Publish the accepted V0.10.1 tree, then rerun Q-012 in normal Goose against the exact
published commit. Offline acceptance does not itself accept Q-012.
