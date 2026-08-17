# Campaign Contract: CAMPAIGN-010-r1

## Control

- HARNESS_ROLE: `WORKER`
- HARNESS_MODE: `STRICT_CAMPAIGN`
- State: `ASSIGNED`
- Repository: `C:\Users\GeZhu\MyMCP\mcp-council-of-translation`
- Exact Git baseline: `9cd0f317ca6ecedef3477ac322c73189d430ded8`
- Trigger review: `harness/evaluations/CAMPAIGN-009-q012-live-review.md`
- Parent product acceptance: `harness/evaluations/CAMPAIGN-009-r2-review.md`
- Product target: package/module `0.10.2`
- Diagnostic build target: `evidence-value-council-v8.2`
- Record schema remains: `2.4`
- Required Worker report: `harness/reports/CAMPAIGN-010-r1-worker.md`
- New ledger: not required for this bounded two-package Campaign
- Commit policy: one scoped commit per package, two commits maximum
- Subagents: forbidden
- Acceptance authority: Foreman only

Read completely before editing: `AGENTS.md`, `harness/plan.md`,
`harness/features.json`, `harness/progress.md`, this contract, the trigger review, the
Q-012 live protocol, CAMPAIGN-009 r1/r2 contracts, reports and Foreman reviews.

## Objective

Correct the two admitted live presentation counterexamples without changing Council
reasoning or structured evidence. Primary text must map all evidence for one user repair
to one human work item, preserve distinct repairs and bounded consequences, and avoid
implementation telemetry. Full structured clusters and metrics remain the audit truth.

## Frozen invariants

1. Preserve every accepted V0.10.1 behavior except the bounded primary projection defect.
2. Keep Schema `2.4`, exactly five tools, review-only default, budgets 6/13/18 and all
   concurrency semantics.
3. Add no sampling, elicitation, discussion, reconsideration, retry or hidden model call.
4. Do not change prompts, roles, routing, clustering, value-metric identity, Policy Gate,
   positions, adjudication, persistence schema, dependencies or public signatures.
5. Human work-item grouping is presentation-only and cannot mutate findings, clusters,
   discussion, metrics, digest inputs or persisted full history.
6. Do not use fuzzy similarity, embeddings, language-model classification, locale-specific
   phrase dictionaries or named-example conditionals.
7. Use only bounded structured evidence: deterministic check kind/provenance, exact
   protected literals, normalized source/candidate anchors, containment of a protected
   literal within a bounded span, category family and existing checklist provenance.
8. Never merge two distinct protected literals, distinct source/candidate repairs or an
   omission with a semantic reversal merely because they share a sentence.
9. Primary output retains exactly five sections, final disposition last, clean target
   1,200 and hard cap 3,200 Unicode code points, with no internal IDs or raw check labels.

## PKG-055 — bounded human work-item projection

Observable outcome: live-shaped B presents one `{count}` repair plus one distinct
`cannot`/`可以` repair; live-shaped C presents one scope-restoration repair while keeping
its distinct material consequences readable.

Requirements:

- Derive primary-only work-item groups from existing structured clusters and checklist
  entries without altering the structured objects.
- Canonicalize the three deterministic missing-`{count}` messages through their existing
  check kind/provenance and protected anchor, even when the message itself omits the
  literal.
- Attach reviewer corroboration whose bounded span contains the same protected anchor to
  that human work item for presentation only.
- Treat source/candidate span containment as one repair only when the bounded inner span
  and action direction agree; keep the `cannot`/`可以` reversal separate.
- For model-only cross-family clusters sharing the same exact repair anchors, retain all
  structured cluster/metric identity but render one primary repair with materially
  distinct consequences at most once each.
- Suppress duplicate `must_fix`, `should_fix` and `execution_order` primary lines for an
  already-rendered work item. Do not suppress final disposition, blockers, minority
  conditions, degradation or unavailable coverage.
- Translate known deterministic check outcomes into natural Chinese primary wording;
  do not expose `explicit do-not-translate literal missing`, `explicit caller hard
  constraint violated`, `missing=[...]`, or `required_literal:...` as user work-item text.

Required counterexamples:

1. Sanitized Case B shape: three deterministic checks for `{count}`, reviewer spans
   `{count}` and `Delete {count} files?`, plus a separate `cannot`/`可以` reversal. Chief
   primary text has exactly two repairs, mentions the placeholder repair once, retains
   the reversal once and ends in human review. Full clusters remain unchanged.
2. Sanitized Case C shape: correctness and language-choice clusters share exact
   `only use your location while the app is open` / `使用您的位置信息` anchors. Primary chief
   text requests scope restoration once, retains distinct accuracy/user-impact meaning,
   and does not repeat the same execution instruction. Both clusters and metrics remain.
3. Negative controls: two different required literals; placeholder loss plus URL loss;
   same sentence with placeholder loss plus semantic reversal; same spans with genuinely
   different repair actions. None may overmerge.
4. Preserve Case A one-line six-role confirmation and all existing material-topic,
   minority, privacy, cap and compatibility behavior.

Authorized paths:

- `src/council_of_translation/localization/digest.py`
- `tests/integration/test_v101_live_shaped_value.py`
- `tests/integration/test_v24_presentation.py`
- `tests/unit/test_v24_value_metrics.py` only if a non-mutation assertion is needed;
  production value-metric behavior is frozen

Verification:

- Exact positive and negative counterexamples above.
- Existing V0.10.1 live-shaped, V2.4 presentation/value and Golden tests.
- Explicit before/after equality of clusters, metrics, digest and full record structures.
- Static proof that no sampling or elicitation call site is added.

## PKG-056 — V0.10.2 migration and package proof

Observable outcome: installed artifacts identify the correction without changing the
public contract.

Requirements:

- Set package/module version to `0.10.2` and diagnostic build to
  `evidence-value-council-v8.2`; keep Schema `2.4`.
- Update authoritative user/developer documentation to describe primary human work-item
  projection and the unchanged full structured record.
- Refresh `uv.lock` canonically so only the root project version changes; preserve lock
  revision, package count and upload-time metadata.
- Build fresh wheel and sdist and run isolated Python 3.12/current FastMCP smoke against
  all five registered tools and the dual-channel result contract.

Authorized paths:

- `AGENTS.md`
- `README.md`
- `docs/v0.4-tool-contract.md`
- `pyproject.toml`
- `src/council_of_translation/__init__.py`
- `tests/integration/test_tool_surface_v2.py`
- `tests/integration/test_v10_release_contract.py`
- `tests/unit/test_persistence_v2.py`
- `uv.lock`

## Forbidden scope

- Any path not explicitly authorized above, except the required Worker report
- Orchestration, models, prompts, roles, routing, clustering, value metrics, persistence
  implementation, Policy Gate, adjudication, runtime adapters or public tool code
- Foreman plan/features/progress/contracts/evaluations and all prior reports/ledgers
- `.learnings/**`, `reviews/**`, `myTest/**`, `.tmp/**`, the user audit and every live
  record
- Raw live record content copied into source, tests, docs or committed fixtures
- Goose/provider/model calls, credentials, push, PR, release, deployment or publication

## Admission and protected assets

Verify the exact baseline, contract SHA-256, empty index, admitted dirty/untracked set and
every hash below before editing. Admission compile and complete suite must pass with
exactly `286 passed`; stop on unexplained drift.

| Protected asset | SHA-256 |
| --- | --- |
| `harness/plan.md` | `C5AB434DF90B2F0FC2E95545C6ED3A4BD0A8BD8255F691C0105169DD346DD50D` |
| `harness/features.json` | `D2FCE49FF59059218D12F02F8080B8E2A1478D76CD1DB43A93229FC497ADC2D0` |
| `harness/progress.md` | `75FFA69617A952B8C75DAEB9E9788D1D1920844094BA3D522BE6C8CE1C84A82E` |
| `harness/evaluations/CAMPAIGN-009-q012-live-review.md` | `7BF0FEC690540DFD19DC9380ECC2726A14933B0AC3C3284AF35FE2738E60B778` |
| `harness/contracts/CAMPAIGN-009-q012-live.md` | `53C7C2FBD6140B84FF9365304F18CD3BF8F28DDB3738AD4222303FFD71B8261F` |
| `harness/evaluations/CAMPAIGN-009-publication-ci-review.md` | `39462F9DA32A9B4497AE92DE61E9EFE182CA08DC832E866B20BF4134E3A24391` |
| `.tmp/q012/20260817T065433950821Z_5ca7ecf52b3a.json` | `3652A7F55AEB1C25BAA34905C2E922957C6B184A58DF80CC513A5B1D20820F41` |
| `.tmp/q012/20260817T065512032949Z_e19fcdfc832c.json` | `80C7A47D1B0330A40A824B47C718A92B9C84C399FB548D9EA60E90320CDC5CEF` |
| `.tmp/q012/20260817T065532734548Z_0270f5294463.json` | `07EB4B9E331B188B035D3397F6C2E418F8CDF3AB2E6872E8236EE914F773857B` |
| `.learnings/LEARNINGS.md` | `52DC1BA8043481911C0DEABB3AC882504D9CBE8BB63D60F391C188586A230DF0` |
| `.learnings/ERRORS.md` | `F99EB75886781958BF5AE6DCF844FD476CBCA45937896A25EE3B2E9D6CD34F0A` |
| `mcp-council-of-translation-audit-and-upgrade-recommendations.md` | `B48073E063C4C9F34E0B6B4DAE94E80079EAAAD3B2F8E273DD60B2F25F6ABD76` |

All other Harness assets are protected. The Worker may create only
`harness/reports/CAMPAIGN-010-r1-worker.md`, which must remain untracked and unstaged.

## Execution policy

1. Execute PKG-055, verify and commit it before PKG-056.
2. One exact-path local commit per package, two commits maximum; never amend, reset,
   restore, clean or rewrite history.
3. Preserve the admitted dirty assets and keep the index empty after each commit and at
   handoff.
4. Use a repository-local uv cache if the host global cache denies access. Canonical lock
   refresh may change only the root version; stop on lock-format or metadata drift.
5. Stop `BLOCKED` only for exact baseline/protected drift or if the fix requires a frozen
   subsystem. Ordinary failures within authorized paths are Worker work.

## Campaign verification

1. Admission compile and exact `286 passed`.
2. PKG-055 exact live-shaped positive/negative controls and all affected presentation,
   privacy, compatibility and value tests.
3. Exact 18/18 Golden Corpus with unchanged aggregate metrics and call counts.
4. Final compile and complete suite with no regression.
5. Exact five tools, `0.10.2`/build v8.2/schema 2.4, review-only, budgets and concurrency.
6. Zero added model/interaction calls and byte-equivalent structured evidence before and
   after primary rendering.
7. Fresh sdist/wheel plus isolated installed-wheel smoke on current FastMCP.
8. Baseline-to-final `git diff --check`, exact authorized scope, protected hashes,
   dead-import scan and empty index.

## Handoff

Write `harness/reports/CAMPAIGN-010-r1-worker.md`. Start the conversational handoff with
exactly `READY_FOR_REVIEW` or `BLOCKED`, then report contract hash, baseline/final HEAD,
commits/files, exact B/C counterexamples, negative controls, A/Golden preservation,
complete suite, artifacts/smoke, lock diff, scope/index/protected hashes, skipped checks,
subagents, authority/external/live counts and remaining risks. Do not claim Campaign
acceptance, Q-012 acceptance, publication or project completion.
