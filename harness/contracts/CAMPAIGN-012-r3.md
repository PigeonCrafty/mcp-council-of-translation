# Campaign Contract: CAMPAIGN-012-r3

## Control

- HARNESS_ROLE: `WORKER`
- HARNESS_MODE: `STRICT_CAMPAIGN`
- State: `ASSIGNED`
- Repository: `C:\Users\GeZhu\MyMCP\mcp-council-of-translation`
- Exact Git baseline: `5819a92e352c468021c3a8f30aa488508e4223f4`
- Parent contract: `harness/contracts/CAMPAIGN-012-r2.md`
- Parent review: `harness/evaluations/CAMPAIGN-012-r2-review.md`
- Product remains: package/module `0.12.0`
- Diagnostic build remains: `verifiable-evidence-council-v10`
- Persisted record schema remains: `2.5`
- Verification receipt schema remains: `1.0`
- Required Worker report: `harness/reports/CAMPAIGN-012-r3-worker.md`
- New ledger: not required
- Commit policy: exactly one scoped local commit
- Subagents: forbidden
- Acceptance authority: Foreman only

Read completely before editing: `AGENTS.md`, `harness/plan.md`,
`harness/features.json`, `harness/progress.md`, this contract, both parent contracts,
both Campaign 012 Foreman reviews and all r1/r2 Worker evidence. Repository assets
override conversation summaries.

## Objective

Close the remaining receipt count/cardinality boundary without changing the receipt
schema or product behavior. Every recorded integer exposed through the canonical receipt
must remain exactly representable by ordinary JSON/JavaScript clients and bounded in
Markdown; oversized independent-review lists must be rejected before iteration. Hostile
persisted records must always produce a bounded verification wrapper rather than a
renderer exception.

## Preserved evidence

Preserve all r1 and r2 implementation and evidence, especially:

- parent-ID privacy and supported current/legacy/null identity;
- one validated ordered active-role identity reused by routing and samples;
- exact sample-set/order checking and bounded duplicate-role behavior;
- exact-once-and-last terminal coherence truth table;
- complete serving package/module/build/Schema primary display;
- history-aware availability, five headings, 3,200 hard cap and pure retrieval;
- V0.12 identifiers, exact five tools, unchanged lock, 360-test regression, exact 24/24
  Golden evidence, fresh artifacts and isolated-wheel behavior.

F-053 through F-057 remain planned until independent Foreman acceptance.

## Frozen invariants

1. Keep package/module/build `0.12.0` / `0.12.0` /
   `verifiable-evidence-council-v10`; persisted Schema `2.5`; receipt Schema `1.0`.
2. Keep the exact canonical receipt keys, nesting and JSON field types. Oversized or
   unsafe recorded values use the existing null plus `redacted_fields` mechanism.
3. Keep exactly five tools, ordinary `full`/`summary` views, normal review/continuation
   reports, review-only behavior, defaults, budgets 6/13/18 and concurrency unchanged.
4. Change no model, compatibility, persistence, orchestration, prompt, role, routing,
   sampling, elicitation, discussion, Policy Gate, adjudication, dependency or lock.
5. Add no retry, model call, interaction, persistence save or receipt field.

## PKG-072 — JSON-safe numeric and sample-cardinality bounds

Observable outcome: every hostile count/list fixture returns a canonical bounded receipt
and five-section report, while all valid boundary values remain exact.

Required behavior:

- Define one internal constant for the maximum safe receipt integer:
  `9_007_199_254_740_991` (`2**53 - 1`).
- `_safe_count` accepts only a non-boolean Python integer in the inclusive range
  `0..9_007_199_254_740_991`.
- A negative value, boolean, or integer greater than the maximum becomes null and adds
  exactly the caller-supplied dotted field path to sorted
  `availability.redacted_fields`; raw decimal digits do not enter Markdown.
- Apply this rule consistently to every recorded numeric receipt field already routed
  through `_safe_count`, without changing field names or types.
- Before iterating `independent_reviews`, require its list length to equal the validated
  active-role count. A mismatch immediately redacts `reviewer_execution.samples`.
- Valid sample lists still preserve exact CouncilPlan order and statuses. Existing
  duplicate/missing/extra/reordered/invalid behavior remains unchanged.
- `build_verification_receipt`, `render_verification_report` and actual
  `view_review_record(detail_level="verification")` remain total and bounded for the
  required hostile cases.

Required counterexamples:

1. For a representative recorded runtime field, values `0`, `1` and
   `9_007_199_254_740_991` round-trip exactly.
2. Values `9_007_199_254_740_992` and `10**3500` become null/redacted; the latter's
   decimal representation is absent from JSON/Markdown and no renderer exception occurs.
3. Cover every recorded numeric receipt path with at least a parameterized safety test;
   existing model-bounded values remain exact.
4. An oversized `independent_reviews` list is rejected before member iteration. Use a
   bounded test double or equivalent instrumentation proving the mismatched tail is not
   traversed, not only that the final report is short.
5. Actual FastMCP history-tool invocation with a 3,501-digit runtime integer and an
   oversized sample list returns the normal wrapper, matching primary/structured
   redaction and a report no longer than 3,200 code points.
6. All r2 parent, active-role, sample-order, four-way coherence and serving-display
   counterexamples remain green.

Authorized paths:

- `src/council_of_translation/localization/verification.py`
- `tests/unit/test_verification_receipt.py`
- `tests/integration/test_v12_verification_view.py`

## Forbidden scope

- Every path not explicitly authorized above, except the required new Worker report
- Tools, models, persistence, compatibility, orchestration, digest, evaluations,
  prompts, roles, routing, Policy Gate, adjudication and runtime adapters
- Docs, `AGENTS.md`, package metadata, dependencies, artifacts checked into the repo and
  `uv.lock`
- Any new tool, parameter, schema, receipt field, alias, fallback or ordinary-report text
- All Foreman Harness assets, parent contracts/evaluations/reports and user assets
- `.learnings/**`, `reviews/**`, `.tmp/q012/**`, `myTest/**`, historical `dist/**` and
  the user audit report
- Goose/provider/model/account calls, credentials, GitHub, push, PR, release,
  deployment or publication

## Admission and protected assets

Verify the exact baseline, contract SHA-256, empty index, admitted dirty/untracked set
and every hash below before editing. Admission compile and complete suite must pass with
exactly `360 passed`; stop on unexplained drift.

| Protected asset | SHA-256 |
| --- | --- |
| `harness/plan.md` | `1777160F0AA58407CE99D48C3BB9F4E163A460038B3FEB3DC705F3E62B9B5099` |
| `harness/features.json` | `0BE313661C6EA8D0922E629D8C3D0F756385A67DC20D374A26EC40C6B1E05A38` |
| `harness/progress.md` | `36E6BBF29F2B1B2D46FA053C89462356069D1FAE6D86189C6C67E7A39D4FB949` |
| `harness/contracts/CAMPAIGN-012-r1.md` | `E4E1CAAFB5E6E08729B5E726C5144793D3BE7E029699AA24984F37E97D587548` |
| `harness/contracts/CAMPAIGN-012-r2.md` | `1B628133452A89F1BA4F47798F124B0E07C9E25E4B994C52834D65A1FAFCB615` |
| `harness/evaluations/CAMPAIGN-012-r1-review.md` | `F0E3F8BB0A8D16EF51602F0352C9703646658BC2993A39BB6F1AFB064A08CEA8` |
| `harness/evaluations/CAMPAIGN-012-r2-review.md` | `FD74C91C3275FDE662A49D2DAB31051876F7718857DA7239DF0376BE23B08009` |
| `harness/reports/CAMPAIGN-012-r1-worker.md` | `43966E75BF6348B3B144ECA8BC517516DCC499AF9238B7288B8306B7F3760ECB` |
| `harness/reports/CAMPAIGN-012-r1-ledger.md` | `4B462BB8252793F72B8D75BD9A5B02230CE82FF1AEB10CE0009B44640C231944` |
| `harness/reports/CAMPAIGN-012-r2-worker.md` | `54746D80619E5E4C35A69CA514381F0EBECF3E6E52B0D4050024B44BCB412A44` |
| `AGENTS.md` | `4A1839CE8E71E93D7DF3F35875535C1D9E0C14E07DAC857FBF756501A308110F` |
| `.learnings/LEARNINGS.md` | `F2A49AE9E08483F777D4145CB1FC9AA734CD3A2877B2F17A1C1DFFC5E2DCD4C8` |
| `.learnings/ERRORS.md` | `48800E1BA3D7BC7A709F0194C353AC802B1D015D750B408D5570A4822DF78F91` |
| `mcp-council-of-translation-audit-and-upgrade-recommendations.md` | `B48073E063C4C9F34E0B6B4DAE94E80079EAAAD3B2F8E273DD60B2F25F6ABD76` |

All other Harness and user dirty/untracked assets are protected. The Worker may create
only `harness/reports/CAMPAIGN-012-r3-worker.md`, which must remain untracked and
unstaged.

## Execution policy

1. Reproduce the 3,501-digit count failure before editing.
2. Make exactly one local commit. Never amend, reset, restore, clean or rewrite history.
3. Preserve admitted dirty assets and keep the Git index empty at handoff.
4. Do not inspect or clean historical `dist/**`. Build fresh artifacts only in an exact
   Worker-created temporary directory; remove only that verified directory.
5. Do not refresh or edit `uv.lock`.
6. Stop `BLOCKED` only for baseline/hash/index drift or if satisfying the correction
   requires a forbidden subsystem. Failures inside the three authorized paths are Worker
   work.

## Required verification

1. Admission compile and exact `360 passed`.
2. Complete PKG-072 boundary matrix, including actual-tool and no-tail-iteration proof.
3. All r1/r2 receipt privacy, availability, role/sample, coherence, serving and purity
   tests.
4. Complete V0.12 history/tool/release matrix.
5. Exact 24/24 Golden corpus with all eight aggregate metrics at 1.0.
6. Final compile and complete suite with zero failures.
7. Exact five tools, version/build, Schema 2.5, receipt Schema 1.0, review-only,
   budgets 6/13/18 and concurrency 3/3.
8. Fresh wheel/sdist in a Worker temp directory plus isolated CPython 3.12/current
   FastMCP installed-wheel smoke for all five tools and the hostile-count wrapper.
9. `uv.lock` byte-identical; `git diff --check`; exact three-path maximum scope;
   dead-import scan; protected hashes exact; index empty.

Use a unique repository-local basetemp if the known Windows host temporary-root
permission defect occurs. Record the original failure and bounded rerun. Do not skip,
delete or weaken a failing test to improve the count.

## Handoff

Write `harness/reports/CAMPAIGN-012-r3-worker.md`. Start with exactly
`READY_FOR_REVIEW` or `BLOCKED`, then report contract hash, baseline/final HEAD, single
commit and paths, numeric truth table, no-tail-iteration evidence, actual-tool hostile
result, r1/r2 preservation, focused/full/Golden results, artifact hashes, wheel smoke,
unchanged lock, scope/index/protected hashes, skipped checks, subagent/authority/
dependency/live-call counts and remaining risks. Do not claim Campaign acceptance,
Q-014, publication or project completion.

## Stop conditions

Stop with `BLOCKED` rather than guessing if the baseline, contract hash, index or any
protected hash differs; a fix needs a forbidden path, schema/key/type change or ordinary
report change; package/lock/version identifiers drift; hostile digits survive either
channel; a required test/build/smoke cannot establish the result; or live/external/
destructive authority would be required.
