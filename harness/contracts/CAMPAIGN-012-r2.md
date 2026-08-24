# Campaign Contract: CAMPAIGN-012-r2

## Control

- HARNESS_ROLE: `WORKER`
- HARNESS_MODE: `STRICT_CAMPAIGN`
- State: `ASSIGNED`
- Repository: `C:\Users\GeZhu\MyMCP\mcp-council-of-translation`
- Exact Git baseline: `06b0e378adc99826c48cd9fc7cc4337d8bc25367`
- Parent contract: `harness/contracts/CAMPAIGN-012-r1.md`
- Parent review: `harness/evaluations/CAMPAIGN-012-r1-review.md`
- Product remains: package/module `0.12.0`
- Diagnostic build remains: `verifiable-evidence-council-v10`
- Persisted record schema remains: `2.5`
- Verification receipt schema remains: `1.0`
- Required Worker report: `harness/reports/CAMPAIGN-012-r2-worker.md`
- New ledger: not required
- Commit policy: exactly two scoped local commits, one per package
- Implementation subagents: forbidden
- Read-only subagents: optional, maximum two, disclose all
- Acceptance authority: Foreman only

Read completely before editing: `AGENTS.md`, `harness/plan.md`,
`harness/features.json`, `harness/progress.md`, this contract, the parent r1 contract,
the r1 Foreman review, Worker report and ledger. Repository assets override conversation
summaries.

## Objective

Correct only the r1 verification-receipt privacy, boundedness and coherence defects.
Hostile persisted values must produce a bounded privacy-safe receipt rather than a path
leak or renderer exception; terminal coherence must be true only when the structured
disposition appears exactly once and is the final non-empty report line. Complete the
already frozen serving-version primary display without changing the canonical JSON
field contract or any ordinary review behavior.

## Preserved r1 evidence

The following work is accepted as evidence to preserve, but F-053 through F-057 remain
unaccepted until this correction passes independent Foreman review:

- additive `detail_level="verification"` on the existing history tool and exact five-tool
  surface;
- canonical receipt Schema 1.0 field names, nesting and history-aware null semantics;
- zero-save, zero-sampling, zero-elicitation retrieval purity;
- V0.12 package/build/docs/lock migration and exact root-only lock diff;
- 334-test regression, exact 24/24 Golden evidence and r1 artifact/smoke results.

## Frozen invariants

1. Keep package/module/build `0.12.0` / `0.12.0` /
   `verifiable-evidence-council-v10`; persisted Schema `2.5`; receipt Schema `1.0`.
2. Keep exactly five public tools, `review_only`, defaults, budgets 6/13/18 and
   concurrency behavior unchanged.
3. Do not change review/continuation orchestration, prompts, roles, routing, sampling,
   elicitation, discussion, Policy Gate, adjudication, persistence bytes or ordinary
   display reports.
4. Do not add receipt keys, rename keys, change JSON types or introduce alias values.
5. Receipt projection remains pure, deterministic and derived from one loaded record
   plus current server identity.
6. The five verification Markdown headings and 3,200-code-point hard cap remain exact.
7. Do not expose raw source/candidate/context, reviewer prose, findings/evidence,
   warnings, internal IDs, paths, environment values or secrets.

## PKG-070 — bounded privacy-safe receipt identity

Observable outcome: hostile parent IDs and active-role/sample structures are rejected as
unavailable evidence without leaking raw values or making verification retrieval fail.

Required behavior:

- `record.parent_review_id` is emitted only when null or when it matches one of the
  existing supported record ID grammars:
  - current: `^[0-9]{8}T[0-9]{12}Z_[0-9a-f]{8,32}$`
  - legacy: `^[0-9]{8}_[0-9]{6}$`
- A non-null invalid parent becomes JSON null and adds exactly
  `record.parent_review_id` to sorted `availability.redacted_fields`; no raw value
  survives JSON serialization or Markdown.
- Validate the active-role list once. It must be an ordered, duplicate-free list of
  registry-backed reviewer IDs and cannot exceed the number of registered reviewer
  roles. Routing and sample projection must reuse that exact validated list.
- Duplicate, oversized or invalid active roles redact both `routing.active_role_ids` and
  `reviewer_execution.samples`. Missing, duplicate, extra, invalid or mismatched sample
  roles redact `reviewer_execution.samples`. Raw values never survive.
- Hostile list shapes must still return a canonical receipt and a deterministic report
  within 3,200 code points. The public `verification` history view must not propagate a
  renderer exception.
- Full valid V2.5, metadata and legacy behavior remains byte-equivalent except for the
  expressly corrected cases.

Required counterexamples:

1. Safe current parent ID, safe legacy parent ID and null parent round-trip exactly.
2. `C:/PRIVATE_PARENT_SENTINEL`, `..\\private`, an overlong string and an arbitrary
   prose parent become null/redacted and are absent from both channels.
3. 100 repeated safe role IDs, one duplicate within an otherwise valid portfolio,
   unknown roles and non-list values return bounded null/redaction rather than a crash.
4. Valid roles with duplicate, missing, extra, reordered or invalid sample members
   preserve truthful null/redaction. Valid ordered samples still project exactly.
5. Actual `view_review_record(detail_level="verification")` exercises at least the path
   and duplicate-role hostile records and returns its normal bounded wrapper.

Authorized paths:

- `src/council_of_translation/localization/verification.py`
- `src/council_of_translation/tools/review.py` only if narrowly required to guarantee a
  bounded public error result after safe projection; explain why in the Worker report
- `tests/unit/test_verification_receipt.py`
- `tests/integration/test_v12_verification_view.py`

## PKG-071 — exact terminal coherence and complete serving display

Observable outcome: both channels report terminal agreement truthfully and the primary
receipt exposes all four canonical serving identifiers.

Required behavior:

- `terminal_disposition_occurrences` remains the exact count of full-line matches.
- `terminal_disposition_is_last_report_line` remains true only when the final non-empty
  line equals the structured expected disposition.
- `terminal_disposition_matches_structured` is true if and only if the occurrence count
  is exactly one and that match is the final non-empty line.
- Zero matches, duplicate expected lines, expected-then-conflicting-final and
  conflicting-only reports all produce false without rewriting record or chief fields.
- Primary Markdown shows serving package, module, diagnostic build and Schema from the
  canonical `serving` object. It retains exactly the five frozen headings, exact
  canonical values and the 3,200 hard cap.
- Existing normal `review_translation`/`continue_review` primary text and history
  `full`/`summary` structured results remain unchanged.

Required counterexamples:

1. Expected disposition exactly once and last: matches true.
2. Expected disposition once but followed by a conflicting final disposition: matches
   false, occurrence 1, last false.
3. Expected disposition duplicated with the final duplicate last: matches false,
   occurrence 2, last true.
4. No expected disposition and conflicting-only disposition: matches false.
5. Markdown includes exact serving `package_version`, `module_version`,
   `diagnostic_build` and `schema_version` and remains bounded for full, partial and
   redacted receipts.

Authorized paths:

- `src/council_of_translation/localization/verification.py`
- `tests/unit/test_verification_receipt.py`
- `tests/integration/test_v12_verification_view.py`
- `tests/integration/test_tool_surface_v2.py`
- `tests/integration/test_v10_release_contract.py`

## Forbidden scope

- Every path not explicitly authorized above, except the required new Worker report
- `__init__.py`, docs, package metadata, dependencies and `uv.lock`
- Models, compatibility, persistence, orchestration, digest, evaluation, prompts, roles,
  routing, Policy Gate, adjudication and runtime adapters
- Any sixth tool, new parameter, new schema or receipt-field change
- All Foreman Harness assets, parent reports/contracts/evaluations and user assets
- `.learnings/**`, `reviews/**`, `.tmp/q012/**`, `myTest/**` and the user audit report
- Goose/provider/model/account calls, credentials, GitHub, push, PR, release,
  deployment or publication

## Admission and protected assets

Verify the exact baseline, contract SHA-256, empty index, admitted dirty/untracked set
and every hash below before editing. Admission compile and complete suite must pass with
exactly `334 passed`; stop on unexplained drift.

| Protected asset | SHA-256 |
| --- | --- |
| `harness/plan.md` | `4F769635554555250B1E3AC8784E369BCC71DBB3AC91E8E2648A3D184C1EB45C` |
| `harness/features.json` | `D3A4FFBCCA49953F61F8CB159A77621B7E3B25C7362A80A64C44B476BEA53422` |
| `harness/progress.md` | `3D8F960AB493AB8761E6DF780D2B3458CF9C5B10E8B88C80A0AFBF745C5B0C01` |
| `harness/contracts/CAMPAIGN-012-r1.md` | `E4E1CAAFB5E6E08729B5E726C5144793D3BE7E029699AA24984F37E97D587548` |
| `harness/evaluations/CAMPAIGN-012-r1-review.md` | `F0E3F8BB0A8D16EF51602F0352C9703646658BC2993A39BB6F1AFB064A08CEA8` |
| `harness/reports/CAMPAIGN-012-r1-worker.md` | `43966E75BF6348B3B144ECA8BC517516DCC499AF9238B7288B8306B7F3760ECB` |
| `harness/reports/CAMPAIGN-012-r1-ledger.md` | `4B462BB8252793F72B8D75BD9A5B02230CE82FF1AEB10CE0009B44640C231944` |
| `AGENTS.md` | `4A1839CE8E71E93D7DF3F35875535C1D9E0C14E07DAC857FBF756501A308110F` |
| `.learnings/LEARNINGS.md` | `F2A49AE9E08483F777D4145CB1FC9AA734CD3A2877B2F17A1C1DFFC5E2DCD4C8` |
| `.learnings/ERRORS.md` | `48800E1BA3D7BC7A709F0194C353AC802B1D015D750B408D5570A4822DF78F91` |
| `mcp-council-of-translation-audit-and-upgrade-recommendations.md` | `B48073E063C4C9F34E0B6B4DAE94E80079EAAAD3B2F8E273DD60B2F25F6ABD76` |

All other Harness assets and user dirty/untracked assets are protected. The Worker may
create only `harness/reports/CAMPAIGN-012-r2-worker.md`, which must remain untracked and
unstaged.

## Execution policy

1. Inspect the baseline diff and reproduce all three Foreman counterexamples before
   editing.
2. Make exactly two local commits in package order. Never amend, reset, restore, clean
   or rewrite history.
3. Preserve admitted dirty assets and keep the Git index empty at handoff.
4. Do not refresh or edit `uv.lock`. Build fresh artifacts from final HEAD with exact
   ephemeral directories; remove only Worker-created temporary paths after resolving
   their absolute targets.
5. Stop `BLOCKED` only for baseline/hash/index drift or if correction requires a frozen
   subsystem. Failing tests within the authorized paths are Worker work.

## Required verification

1. Admission: compile and exact `334 passed` full suite.
2. PKG-070 parent-ID, role-list, sample-set, serialization, report-bound and actual-tool
   counterexamples.
3. PKG-071 four-way terminal truth table and serving-display counterexamples.
4. Complete existing V0.12 receipt/history/tool-surface/release matrix.
5. Exact 24/24 Golden corpus with all eight aggregate metrics at 1.0.
6. Final compile and complete test suite with no regression.
7. Exact five tools, version/build, Schema 2.5, receipt Schema 1.0, review-only,
   budgets 6/13/18 and concurrency 3/3.
8. Programmatic proof of one load, zero saves, zero sampling, zero elicitation and no
   record mutation for verification retrieval.
9. Fresh wheel and sdist plus isolated CPython 3.12/current FastMCP installed-wheel
   smoke covering all five tools, verification hostile controls and dual channels.
10. `uv.lock` byte-identical; `git diff --check`; exact authorized path audit; dead-import
    scan; protected hashes exact; index empty.

Use a unique repository-local basetemp/cache if the known Windows host temporary-root
permission defect occurs. Record the original failure and bounded rerun. Do not delete,
skip or weaken a failing test to improve the count.

## Handoff

Write `harness/reports/CAMPAIGN-012-r2-worker.md`. Start with exactly
`READY_FOR_REVIEW` or `BLOCKED`, then report contract hash, baseline/final HEAD, exactly
two commits, changed paths, every hostile counterexample, coherence truth table, serving
display, focused/full/Golden results, artifact hashes, wheel smoke, unchanged lock,
scope/index/protected hashes, skipped checks, subagents, authority/dependency/live-call
counts and remaining risks. Do not claim Campaign acceptance, Q-014, publication or
project completion.

## Stop conditions

Stop with `BLOCKED` rather than guessing if the exact baseline, contract hash, index or
protected hashes differ; a required correction needs a forbidden file or receipt schema
change; ordinary review/full/summary behavior changes; lock/package/version identifiers
drift; privacy data survives either channel; a required verification/build/smoke cannot
establish the result; or the task would require live Goose/provider calls, credentials,
remote mutation, publication or destructive cleanup.
