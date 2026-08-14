# CAMPAIGN-009-r2 Main Worker Report

## Terminal status

READY_FOR_REVIEW

This is a Worker handoff only. Campaign acceptance, Q-012 acceptance, publication and
project completion remain Foreman authority.

## Control and admission

- HARNESS_ROLE: `WORKER / MAIN WORKER`
- HARNESS_MODE: `STRICT_CAMPAIGN`
- Contract: `harness/contracts/CAMPAIGN-009-r2.md`
- Contract SHA-256:
  `4E4158537F4FDB2CAEE2C0E2B4F3F5594A6FB6DD3FA5E81BBE9437F95A3DA759`
- Exact admitted baseline: `62f2ee9bf1860f80281afbbad53734db5f700205`, subject
  `Release V0.10.1 value corrections`
- Admission index: empty
- Admission compile: `.venv\Scripts\python.exe -m compileall -q src tests` -> exit 0
- Admission full regression, using an explicit system-temp `--basetemp`:
  `283 passed in 3.53s`
- All ten contract-enumerated protected hashes matched before implementation.
- Admitted modified Foreman assets: `harness/plan.md`, `harness/features.json`,
  `harness/progress.md`.
- Admitted untracked protected assets: both Q-012 protocols, Campaign r1/r2 contracts,
  Campaign-008 publication/Q-012 reviews, r1 Foreman review, r1 report/ledger,
  `.learnings/**`, the user audit Markdown and `reviews/20260810_145151.json`.
- The historical r1 report's extra trailing `A` in the displayed LEARNINGS hash was
  treated as the documented transcription error. The actual file and r2 contract both
  matched `52DC1BA8043481911C0DEABB3AC882504D9CBE8BB63D60F391C188586A230DF0`.
- Subagent policy: forbidden; no subagents were used.

## Final Git state and commits

- Final HEAD: `4a3c692ad528db03e4f72a025d60c4eb775454f0`
- Commit count from baseline: exactly two
- Git index: empty
- Baseline-to-HEAD scope: exactly four authorized paths; scope comparison passed
- `git diff --check 62f2ee9bf1860f80281afbbad53734db5f700205..HEAD`: passed
- Forbidden release/package/docs input changes: `0`
- Local commits, not pushed:
  1. `b1b362789160a6532b01d6b8456df08658ba8f72` —
     `Canonicalize typed discussion provenance`
  2. `4a3c692ad528db03e4f72a025d60c4eb775454f0` —
     `Preserve material topics in grouped presentation`

Changed files by package:

- PKG-053:
  `src/council_of_translation/localization/value_metrics.py`,
  `tests/unit/test_v24_value_metrics.py`
- PKG-054:
  `src/council_of_translation/localization/digest.py`,
  `tests/integration/test_v24_presentation.py`

Baseline-to-final numstat:

```text
32  11  src/council_of_translation/localization/digest.py
18   0  src/council_of_translation/localization/value_metrics.py
57   0  tests/integration/test_v24_presentation.py
105  0  tests/unit/test_v24_value_metrics.py
```

This r2 report is the only new r2 Harness asset. It remains untracked and unstaged as
required.

## PKG-053 — canonical typed provenance inventory

Implementation:

- Added one bounded canonicalization path for structured `rule_ref` and
  `constraint_ref` field values.
- Raw values such as `TB-1` and `placeholder-parity`, and already-prefixed equivalents,
  now inventory to the exact same typed provenance identities used by discussion
  markers.
- Repeated correct prefixes are stripped before creating one identity; set semantics
  prevent double counting.
- The existing exact/token inventory remains intact. Natural-language prose, malformed
  values and overlong pseudo-markers remain ineligible.

Before/after counterexamples:

- Before: existing `RolePosition.rule_refs=["TB-1"]` plus discussion
  `rule_ref:TB-1` produced new evidence `1`, marginal value `low`.
- After: raw and already-prefixed rule references both produce new evidence `0`,
  marginal value `none`, including three repeated discussion turns.
- Before: the equivalent raw immutable-constraint case produced the same false new
  evidence.
- After: raw and already-prefixed `constraint_ref:placeholder-parity` both produce `0` /
  `none`, including repeated turns.
- A genuinely absent valid `rule_ref:` or `constraint_ref:` marker produces exactly one
  new evidence item and `low` across three repetitions.
- Prose-embedded, whitespace-malformed and 121-character suffix pseudo-markers produce
  `0` / `none`.

Verification:

- Intentional pre-fix reproduction: the new typed-provenance test failed with
  `discussion_new_evidence_count == 1`.
- Final PKG-053 selection:
  `tests/unit/test_v24_value_metrics.py`,
  `tests/integration/test_v24_value_metrics.py`, and
  `tests/integration/test_v101_live_shaped_value.py` -> `25 passed in 0.24s`.
- This selection includes existing URL/structured-token controls, position/resolution
  materiality, Case B paraphrases, purity and zero-call behavior.

## PKG-054 — material-topic visibility before deduplication

Implementation:

- Corroborating logical groups now render one bounded human topic in addition to their
  exact role attribution and optional exact anchors.
- Reviewer-backed group topics are preferred over deterministic scanner wording; anchors
  locate the issue but no longer replace its meaning.
- The renderer no longer marks every cluster topic represented merely because a cluster
  exists. It derives the represented set only from bounded topic text literally emitted
  in earlier value/coverage lines.
- Consensus, disagreement and minority suppression therefore occurs only after the
  material topic has actually appeared.
- Digest, metrics, clusters and full structured records are not mutated.

Before/after required counterexample:

- Topic: `候选译文把“trial”误写成“正式版”，会改变授权状态。`
- Before: topic count in the primary report was `0`; only `trial -> 正式版` and a generic
  retained-minority sentence remained.
- After: the complete topic count is exactly `1`; the fidelity and terminology role
  names each occur exactly once; the decisive condition remains; the final disposition
  remains the last line; no chief repair prose is needed to preserve intelligibility.
- The exact test snapshots digest and cluster JSON and verifies no mutation.

Verification:

- Intentional pre-fix reproduction: the required test failed with topic count `0`.
- Exact presentation + r1 A/B selection: `7 passed in 0.19s`.
- Wider presentation/privacy/compatibility/persistence/tool-cap selection:
  `57 passed in 1.16s`.

## Integrated Campaign verification

Fresh named commands and results:

```text
.venv\Scripts\python.exe -m pytest -q --basetemp=<system-temp>
  tests/unit/test_v24_value_metrics.py
  tests/integration/test_v24_value_metrics.py
  tests/integration/test_v24_presentation.py
  tests/integration/test_v101_live_shaped_value.py
=> 30 passed in 0.26s

.venv\Scripts\python.exe -m pytest -q tests/integration/test_v24_golden_corpus.py
=> 4 passed in 0.35s

.venv\Scripts\python.exe -m compileall -q src tests
=> exit 0

.venv\Scripts\python.exe -m pytest -q --basetemp=<system-temp>
=> 286 passed in 3.54s

.venv\Scripts\python.exe -m pytest -q --basetemp=<system-temp>
  tests/integration/test_tool_surface_v2.py
  tests/integration/test_v10_release_contract.py
  tests/unit/test_deliberation_policy_v2.py
  tests/unit/test_runtime_concurrency.py
  tests/unit/test_roles_v2.py
=> 49 passed in 1.34s
```

Exact Golden runner output:

- cases: `18/18`
- failed IDs: `[]`
- scripted sampling calls: `113`
- scripted elicitation calls: `4`
- critical recall, false-positive-free rate, contribution-kind accuracy, conflict
  detection, user authority, chief consistency, call budget and discussion marginal
  accuracy: all `1.0`

Frozen invariants:

- package/module: `0.10.1`
- diagnostic build: `evidence-value-council-v8.1`
- record schema: `2.4`
- public tool surface: exactly five, in the accepted order
- review-only default: unchanged
- sample budgets: `6/13/18`
- concurrency: default/max `3/3`, valid `1/2/3`, invalid sequential fallback
- invariant selection above: `49 passed`
- no production sample/elicit call sites exist in either modified production module
- canonical JSON for a complete synthetic V2.4 record was byte-equivalent before and
  after presentation: `5,905` UTF-8 bytes; material topic rendered exactly once
- AST dead-import scan: `[]` for both modified production modules
- r1 live-shaped A/B tests remain green: grouped clean confirmation, Case B discussion
  value zero, singular primary placeholder chief work item, distinct `cannot`/`可以`
  reversal, full structured evidence and non-mutation preserved

## Protected assets and repository hygiene

Final SHA-256 values all matched the r2 contract:

- `harness/plan.md`:
  `D13F55E308555F93011A3FAE2544D374C91C4A7E7E3570EE9B8CBCFB767FFE1A`
- `harness/features.json`:
  `769B33DEDC3D44B7199CE468476500FD958D9EF11B3587A25FE6F36323EB116A`
- `harness/progress.md`:
  `511A49FAD1054DB10D885E86E6D0DEFBF5E3B941B6C6EFE3E7886D5384AF04D6`
- parent contract:
  `F4C8EB61730E94279E028821FF08E1CA6E2B81C772D8CFC90AF63C3538DF8758`
- parent Foreman review:
  `C9F4B9BB79EC1106147BE395217D4EE17CE807BF4339A1A9A449E07D741AB2C2`
- parent Worker report:
  `EFB07E0FD3873FB70AFE730E3E8485EB08A60489AB2F5E36EDE2BE1F79194A01`
- parent ledger:
  `C6E66E07C2358F9E529DF85B932121AB039DAD766D75543AAE16EAEF02D8DC08`
- `.learnings/LEARNINGS.md`:
  `52DC1BA8043481911C0DEABB3AC882504D9CBE8BB63D60F391C188586A230DF0`
- `.learnings/ERRORS.md`:
  `F99EB75886781958BF5AE6DCF844FD476CBCA45937896A25EE3B2E9D6CD34F0A`
- user audit Markdown:
  `B48073E063C4C9F34E0B6B4DAE94E80079EAAAD3B2F8E273DD60B2F25F6ABD76`

The protected dirty/untracked set remains unchanged apart from this authorized r2 report.
No protected path was staged or committed.

## Incidents, deviations, authority and skipped work

- An intentional pre-fix PKG-053 test run produced one assertion failure; it is the
  required before-state reproduction, not a regression in the final state.
- One focused pytest run used pytest's inaccessible default Windows temp root and ended
  with `19 passed, 6 setup errors`. The same selection was rerun with an explicit,
  validated system-temp `--basetemp` and passed `25/25`.
- The first inline Golden-summary command had a PowerShell/Python quoting `SyntaxError`;
  a simpler equivalent command produced the exact `18/18`, `113`, `4`, eight-at-1.0
  evidence.
- One read-only `rg` command included a nonexistent historical test path and exited 1
  after returning useful matches. The exact existing invariant files then passed 49/49.
- `ruff` is not installed in the project venv. A standard-library AST dead-import scan
  was used and found none. The first byte-equivalence probe omitted the required task
  model and raised a Pydantic validation error; the corrected complete-record probe
  passed. None of these command incidents changed repository files.
- The self-improvement skill was read after the unexpected temp-path failure. Its normal
  error log was not written because `.learnings/**` is contract-protected; incidents are
  preserved here instead.
- Deviations from product scope: none.
- Required checks skipped: none.
- Package build, lock refresh and installed-wheel smoke were intentionally not rerun:
  the r2 execution policy explicitly forbids package/lock regeneration and preserves r1
  package evidence because every release input is unchanged.
- Subagents: `0`.
- Authority escalations: `4`, exactly two authorized `git add` and two authorized
  scoped `git commit` operations.
- External dependency/network operations: `0`.
- Live Goose/provider/model calls: `0`.
- Pushes, PR operations, releases, deployments, credential or Goose changes: `0`.

## Remaining risks

- Typed provenance remains deliberately restricted to bounded ASCII marker identities;
  natural-language novelty that cannot be proven structurally continues to be
  conservatively undercounted, as required.
- Topic representation uses literal bounded rendered text, not fuzzy/semantic matching.
  Semantically related but non-identical prose may remain separately visible rather than
  risk hiding a material issue.
- This report does not claim Campaign acceptance, Q-012 acceptance, publication or
  project completion.

