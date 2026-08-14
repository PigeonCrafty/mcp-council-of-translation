# Campaign Contract: CAMPAIGN-009-r2

## Control

- HARNESS_ROLE: `WORKER`
- HARNESS_MODE: `STRICT_CAMPAIGN`
- State: `ASSIGNED`
- Repository: `C:\Users\GeZhu\MyMCP\mcp-council-of-translation`
- Exact Git baseline: `62f2ee9bf1860f80281afbbad53734db5f700205`
- Parent contract: `harness/contracts/CAMPAIGN-009-r1.md`
- Parent review: `harness/evaluations/CAMPAIGN-009-r1-review.md`
- Product remains: package/module `0.10.1`
- Diagnostic build remains: `evidence-value-council-v8.1`
- Record schema remains: `2.4`
- Required Worker report: `harness/reports/CAMPAIGN-009-r2-worker.md`
- New ledger: not required for this bounded correction
- Commit policy: one scoped commit per package, two commits maximum
- Subagents: forbidden
- Acceptance authority: Foreman only

Read completely before editing: `AGENTS.md`, `harness/plan.md`,
`harness/features.json`, `harness/progress.md`, this contract, the parent contract,
parent Worker report/ledger and parent Foreman review.

## Objective

Correct the two exact r1 counterexamples without redesigning or redoing accepted r1
work. Existing typed rule/constraint provenance must not become “new” merely because a
discussion prefixes its identifier, and every material corroborated/disputed issue must
remain intelligible at least once in primary text.

## Frozen invariants

1. Preserve all accepted CAMPAIGN-009-r1 behavior and tests, including the live-shaped A
   and B corrections, exact 18/18 Golden Corpus and immutable full structured history.
2. Keep version/build/schema `0.10.1` / `evidence-value-council-v8.1` / `2.4`.
3. Keep exactly five tools, review-only behavior, budgets 6/13/18 and existing
   concurrency semantics.
4. Add no sampling, elicitation, discussion, reconsideration, retry or hidden model call.
5. Do not change prompts, roles, routing, clustering identity, Policy Gate, positions,
   adjudication, persistence schema, dependencies, docs or lock.
6. Do not use fuzzy matching, embeddings, prose similarity or named-example shortcuts.
7. Metrics remain pure/descriptive and presentation remains a non-mutating projection.
8. Primary output retains exactly five sections, every role accounted for once, final
   disposition last, clean target 1,200 and hard cap 3,200 code points.

## PKG-053 — canonical typed provenance inventory

Observable outcome: a discussion reference to an already-present typed rule or immutable
constraint counts zero; an absent, explicitly typed bounded provenance marker can still
count once.

Requirements:

- Inventory each `RolePosition.rule_refs` entry under a canonical `rule_ref:` provenance
  identity in addition to any bounded token aliases. Accept both raw IDs such as `TB-1`
  and already-prefixed values without double-prefixing or double-counting.
- Inventory each `IssueCluster.immutable_hard_constraints` entry under a canonical
  `constraint_ref:` provenance identity with the same normalization rule.
- Discussion evidence `rule_ref:TB-1` is zero when the position already contains `TB-1`
  or `rule_ref:TB-1`; `constraint_ref:placeholder-parity` is zero when the cluster already
  contains `placeholder-parity` or the prefixed form.
- The same markers repeated across turns remain zero.
- A genuinely absent valid `rule_ref:` or `constraint_ref:` marker counts exactly one
  evidence item and yields `low` only when no position/resolution delta exists.
- Malformed, unbounded or prose-embedded pseudo-markers count zero. Preserve the r1 URL/
  structured-token positive controls and position/resolution behavior.

Authorized paths:

- `src/council_of_translation/localization/value_metrics.py`
- `tests/unit/test_v24_value_metrics.py`
- `tests/integration/test_v101_live_shaped_value.py` only if an integration assertion is
  useful; production truth must be covered at unit level

Verification:

- Exact raw/prefixed rule and constraint counterexamples.
- Existing V2.4 value-metric tests and r1 live-shaped Case B.
- Pure/non-mutating and zero-call assertions remain green.

## PKG-054 — material-topic visibility before deduplication

Observable outcome: a shared material issue is stated once in understandable language;
its topic is suppressed later only after that material meaning was actually rendered.

Requirements:

- Do not initialize “represented” topics from every cluster merely because the cluster
  exists. Track only bounded material topic(s) actually emitted in an earlier primary
  line.
- For a corroborating logical group, show one bounded human issue summary plus the exact
  role attribution. An anchor may support attribution but cannot replace issue meaning.
- A disputed cluster topic must remain visible at least once even when no chief checklist
  item repeats it. Preserve its minority decision condition when present.
- Do not reintroduce the r1 repetition: one shared issue appears once, confirmation roles
  remain grouped, the Case B placeholder work item remains singular, and distinct
  `cannot`/`可以` reversal remains visible.
- Unique, unavailable, unresolved-context, warning/degradation and compatibility paths
  remain truthful. Do not mutate digest, metrics, clusters or full history.

Required exact counterexample:

- Two corroborating roles, disputed topic
  `候选译文把“trial”误写成“正式版”，会改变授权状态。`, source anchor `trial`, candidate
  anchor `正式版`, no chief repair prose: the complete topic or an equivalently bounded
  deterministic topic projection appears exactly once; both role names appear exactly
  once; the decisive condition remains; final disposition remains last.

Authorized paths:

- `src/council_of_translation/localization/digest.py`
- `tests/integration/test_v24_presentation.py`
- `tests/integration/test_v101_live_shaped_value.py`

Verification:

- Exact counterexample above plus r1 A/B projections.
- All existing presentation/privacy/compatibility/cap tests.
- Explicit non-mutation assertions.

## Forbidden scope

- Any path not explicitly authorized above, except the required r2 Worker report
- `orchestration.py`, models, prompts, roles, clustering, persistence, package metadata,
  docs, `uv.lock`, dependency files or public tool code
- Foreman plan/features/progress/contracts/evaluations and all prior reports/ledgers
- `.learnings/**`, `reviews/**`, `myTest/**`, `.tmp/**`, user audit and live records
- Goose/provider/model calls, credentials, push, PR, release, deployment or publication

## Admission and protected assets

Verify exact baseline, contract SHA-256, empty index, admitted dirty/untracked set and all
hashes below before editing. Admission compile and complete suite must pass with exactly
`283 passed`; stop on unexplained drift.

| Protected asset | SHA-256 |
| --- | --- |
| `harness/plan.md` | `D13F55E308555F93011A3FAE2544D374C91C4A7E7E3570EE9B8CBCFB767FFE1A` |
| `harness/features.json` | `769B33DEDC3D44B7199CE468476500FD958D9EF11B3587A25FE6F36323EB116A` |
| `harness/progress.md` | `511A49FAD1054DB10D885E86E6D0DEFBF5E3B941B6C6EFE3E7886D5384AF04D6` |
| `harness/contracts/CAMPAIGN-009-r1.md` | `F4C8EB61730E94279E028821FF08E1CA6E2B81C772D8CFC90AF63C3538DF8758` |
| `harness/evaluations/CAMPAIGN-009-r1-review.md` | `C9F4B9BB79EC1106147BE395217D4EE17CE807BF4339A1A9A449E07D741AB2C2` |
| `harness/reports/CAMPAIGN-009-r1-worker.md` | `EFB07E0FD3873FB70AFE730E3E8485EB08A60489AB2F5E36EDE2BE1F79194A01` |
| `harness/reports/CAMPAIGN-009-r1-ledger.md` | `C6E66E07C2358F9E529DF85B932121AB039DAD766D75543AAE16EAEF02D8DC08` |
| `.learnings/LEARNINGS.md` | `52DC1BA8043481911C0DEABB3AC882504D9CBE8BB63D60F391C188586A230DF0` |
| `.learnings/ERRORS.md` | `F99EB75886781958BF5AE6DCF844FD476CBCA45937896A25EE3B2E9D6CD34F0A` |
| `mcp-council-of-translation-audit-and-upgrade-recommendations.md` | `B48073E063C4C9F34E0B6B4DAE94E80079EAAAD3B2F8E273DD60B2F25F6ABD76` |

All other Harness assets are protected. The Worker may create only
`harness/reports/CAMPAIGN-009-r2-worker.md`, which must remain untracked and unstaged.

## Execution policy

1. Execute PKG-053 then PKG-054; one exact-path local commit per package, two maximum.
2. Preserve the r1 commits and never amend, reset, restore, clean or rewrite history.
3. Keep the index empty after each commit and at handoff.
4. Do not rerun package builds or lock generation; r1 package evidence is preserved
   because release inputs are forbidden and unchanged.
5. Stop `BLOCKED` only for exact baseline/protected drift or if correction requires a
   frozen/forbidden change. Ordinary test failures inside the two authorized packages are
   Worker work.

## Campaign verification

1. Admission compile and exact `283 passed`.
2. PKG-053 and PKG-054 exact counterexamples plus all affected V2.4/r1 A/B tests.
3. Exact 18/18 Golden Corpus, 113 scripted samples, four elicitations and eight aggregate
   metrics at 1.0.
4. Final compile and complete suite with no regression.
5. Exact five tools, version/build/schema, review-only, budgets and concurrency invariants.
6. Assert zero added calls and byte-equivalent structured records before/after rendering.
7. Baseline-to-final `git diff --check`, exact authorized scope, protected hashes,
   dead-import scan and empty index.

## Handoff

Write `harness/reports/CAMPAIGN-009-r2-worker.md`. Start the conversational handoff with
exactly `READY_FOR_REVIEW` or `BLOCKED`, then report contract hash, baseline/final HEAD,
commits/files, both before/after counterexamples, r1 A/B and Golden preservation, complete
suite, scope/index/protected hashes, skipped checks, subagents, authority/external/live
counts and remaining risks. Do not claim Campaign acceptance, Q-012 acceptance,
publication or project completion.
