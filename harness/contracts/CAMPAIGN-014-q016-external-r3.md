# External Gate Revision: CAMPAIGN-014 Q-016-r3

## Control

- Gate: `Q-016-r3 / Black-box incomplete-input evidence and final independent re-audit`
- Role: `MAIN WORKER IN A SEPARATE NEW CONVERSATION; FOREMAN ACCEPTANCE`
- Mode: `STRICT_CAMPAIGN`
- State: `ISSUED`
- Protected-main baseline: `26e2822cb375f1d593ee386d9d66b3c13f89c3fe`
- Published product commit: `9d8f1f987efe73946377883e6ad3a681abe11989`
- Package/module: `0.13.1`
- Diagnostic build: `truthful-boundaries-council-v11.1`
- Review/receipt/evaluator schemas: `2.6/1.1/2.1`
- Parent contract: `harness/contracts/CAMPAIGN-014-q016-live.md`
- r2 contract: `harness/contracts/CAMPAIGN-014-q016-live-r2.md`
- r2 Foreman review: `harness/evaluations/CAMPAIGN-014-q016-live-r2-review.md`
- Acceptance authority: Foreman only

This is an evidence-only revision. It authorizes no production, test, dependency,
package, lock, workflow, extension, provider, model, release or deployment change.

## Frozen evidence and client boundary

Carry forward without rerun:

- Case B: `20260828T024458690799Z_8badddd7158f`
- Case C: `20260828T024543336644Z_2422acf98836`

Preserve the r2 Goose result verbatim as client-boundary evidence:

```text
CLIENT_LIMIT：无法保证向 MCP 工具传入两个超过 12,000 字符的实际字面字符串
```

Do not call Goose, modify its extension, repeat admission, or rerun B/C. Do not reinterpret
`CLIENT_LIMIT` as a product failure. Q-016-r3 authorizes one black-box MCP Case A3 and one
independent repository re-audit.

## Part I — Case A3 black-box MCP evidence

### Isolation and runtime identity

Run from a fresh temporary directory outside the repository checkout. Use an isolated
CPython 3.12 client with pinned `fastmcp==3.4.7`. Start the server only through STDIO from
the exact published product commit:

```text
uvx --refresh --from git+https://github.com/PigeonCrafty/mcp-council-of-translation@9d8f1f987efe73946377883e6ad3a681abe11989 mcp_council_of_translation
```

On native Windows, every remote Git HTTPS operation must run with the required external
authority; local Git operations remain sandboxed. Record the client Python and FastMCP
versions and prove the server import/runtime identity comes from the isolated published
command, not a local checkout.

Connect with `fastmcp.Client` and `StdioTransport`. Supply an async sampling handler that
returns the same valid clean reviewer envelope for every server sampling request:

```json
{
  "role_feedback": "The reviewed synthetic source and candidate prefixes are identical; no material translation issue is supported by this bounded fixture.",
  "findings": []
}
```

The handler must not inspect hidden repository state, fabricate findings or vary by role.
Record every sampling request count. Do not configure an elicitation handler.

### Exact A3 call

Programmatically construct one Python string of exactly 16,000 uppercase ASCII `S`
characters and pass the same in-memory string object value as both `source_text` and
`candidate_translation`. Assert both lengths and equality immediately before the MCP
call; serialize the actual characters in the tool arguments.

Call `review_translation` exactly once with:

```json
{
  "source_text": "<programmatically materialized 16,000-character S string>",
  "candidate_translation": "<the identical complete string>",
  "source_language": "en",
  "target_language": "en",
  "content_type": "ui",
  "context": "Q-016-r3 synthetic input-completeness fixture. Source and candidate are intentionally identical and carry no user-facing semantic distinction; this case only verifies fail-closed behavior when both inputs exceed the review boundary.",
  "audience": "localization QA engineers",
  "mode": "lightweight",
  "output_mode": "review_only",
  "interactive_mode": "off",
  "briefing_mode": "off",
  "trace_level": "summary",
  "history_mode": "full",
  "project_rules": "Treat the two identical synthetic strings as equivalent. Do not request product context or propose wording changes; report only evidence supported by the supplied record."
}
```

Then call `view_review_record(review_id, detail_level="full")` exactly once and
`view_review_record(review_id, detail_level="verification")` exactly once. Do not call
`get_server_info`, `continue_review` or retry any operation.

Preserve each `CallToolResult` first text block and structured content separately. Parse
the canonical receipt only from structured content or the exact JSON after
`Canonical verification_receipt JSON:`; assert both representations are equal.

### A3 required assertions

All must pass:

- pre-call source/candidate lengths are exactly `16000` and their contents are equal;
- recorded original lengths are `16000`, reviewed lengths are `12000`, and both
  truncated flags are true;
- warnings include `input_truncated`, `source_input_truncated` and
  `candidate_input_truncated`;
- status is `NEEDS_HUMAN_REVIEW`, degradation true, fallback reason exactly
  `input_truncated`, and chief disposition `需人工复核 / 是`;
- primary report contains both `仅审校了有界前缀` and `不构成全文发布许可`;
- decision support is `insufficient` and outcome coherent;
- all planned reviewers are `structured_success`, coverage is full, sampling stays
  within lightweight budget 6, and elicitation is zero;
- canonical receipt is complete with zero not-recorded and zero redacted fields;
- suggested translation is absent/false;
- exactly one terminal disposition is at the final report line and matches structure;
- no second fallback, retry, provider call or local-source import occurred.

Any failure is preserved without retry and reported as a deviation. A client transport,
sampling-handler or dependency failure is evidence-run failure, not automatically a
product defect.

## Part II — independent repository re-audit

Audit exact public commit `9d8f1f987efe73946377883e6ad3a681abe11989` from a fresh
checkout. Prior Worker/Foreman prose is context only. Run at minimum:

```text
python -m compileall src tests
python -m pytest tests/integration/test_v131_input_completeness.py tests/unit/test_preflight_v2.py tests/integration/test_v131_discussion_coherence.py tests/integration/test_v131_history_minimization.py tests/integration/test_v131_evaluation_contract.py tests/integration/test_v10_release_contract.py -q
python -m pytest -q
```

Independently assess and return `CLOSED`, `PARTIALLY_CLOSED` or `OPEN` for each item, with
exact file/line and fresh test/counterexample evidence:

- `AUD-001`: all truncation paths fail closed, persist truthful diagnostics and cannot
  grant whole-input publication permission from a bounded prefix;
- `AUD-002`: percentage prose and URL wrapper punctuation are negative controls while
  real printf placeholders and balanced internal URL syntax remain protected;
- `AUD-003`: malformed discussion is one atomic unavailable round, preserving Round 1
  without consuming partial statements or retrying;
- `AUD-004`: final material role positions recompute consensus independently of optional
  narrative summaries;
- `AUD-005`: V1 summary is the exact six-field privacy projection while full reads remain
  compatible and verification stays canonical/private;
- `AUD-006`: evaluator Schema 2.1 claims only its implemented critical-presence and
  clean-case-no-cluster semantics; the blind-set schema is a handoff contract, not a
  benchmark result;
- `AUD-007`: FastMCP range is exactly `>=2.13.0.2,<4`, with evidence bounded to the tested
  floor and 3.4.7 rather than every intervening version.

Also verify documentation truthfully describes Targeted Discussion as one bounded model
sample simulating cross-role deliberation, not peer-to-peer agent communication.

## Scope, hygiene and report

- Product/source/test/docs/dependency/lock/workflow edits: forbidden.
- Git commits, pushes, PRs, releases and deployments: forbidden.
- Goose/provider/model calls: forbidden.
- Temporary client/checkouts/scripts: allowed only under a boundary-checked temporary
  directory and must be removed after evidence capture.
- Never read or copy user review records, `.learnings/**`, `reviews/**`, `myTest/**` or
  unrelated `.tmp/**` content.
- Required Worker report:
  `harness/reports/CAMPAIGN-014-q016-r3-worker.md`, untracked and unstaged.
- Ledger is not required unless a stop condition or failed command occurs; if needed use
  `harness/reports/CAMPAIGN-014-q016-r3-ledger.md`, untracked and unstaged.

The report must include exact commands, environment versions, public commit, A3 raw text
and structured evidence, assertion table, AUD-001..AUD-007 table, test counts, all
failures/deviations, temporary cleanup, authority/dependency/live/remote operation counts,
and a final independent recommendation: `LIFT BLOCK`, `KEEP BLOCK`, or
`LIFT WITH EXPLICIT LIMITATIONS`.

Do not claim Q-016 acceptance. Foreman alone decides final acceptance and whether the
ordinary feature-expansion block can be lifted.

