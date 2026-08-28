# External Gate Revision: CAMPAIGN-014 Q-016-r4

## Control

- Gate: `Q-016-r4 / Pre-provisioned black-box truncation evidence and discussion wording`
- Role: `MAIN WORKER IN A SEPARATE NEW CONVERSATION; FOREMAN ACCEPTANCE`
- Mode: `STRICT_CAMPAIGN`
- State: `ISSUED`
- Protected-main baseline: `ab912c41d6deebeab440d8be9557371be2580dff`
- Shared implementation baseline: `9d23ed01f94be2ef0c724b3e0a3e7e1beba75c09`
- Published product commit: `9d8f1f987efe73946377883e6ad3a681abe11989`
- Package/module/build: `0.13.1/0.13.1/truthful-boundaries-council-v11.1`
- Review/receipt/evaluator schemas: `2.6/1.1/2.1`
- Parent contract: `harness/contracts/CAMPAIGN-014-q016-external-r3.md`
- Parent review: `harness/evaluations/CAMPAIGN-014-q016-r3-review.md`
- Acceptance authority: Foreman only

## Frozen carry-forward evidence

Do not rerun or reinterpret:

- Case B: `20260828T024458690799Z_8badddd7158f`;
- Case C: `20260828T024543336644Z_2422acf98836`;
- r2 `CLIENT_LIMIT` as truthful Goose client-boundary evidence;
- `AUD-001` through `AUD-007` as independently `CLOSED`;
- r3 compile, focused `92/92`, and full `575/575` evidence.

r4 authorizes only one A4 evidence run and one bounded documentation/test correction.
No Goose, provider or model call is authorized.

## Package R4-1 — explicit Targeted Discussion documentation

Authorized paths:

- `README.md`
- `docs/v0.4-architecture.md`
- `tests/integration/test_v10_release_contract.py`

Add one concise, technically exact statement to both public documentation paths:

> Targeted Discussion is one bounded model sample that simulates cross-role
> deliberation; it is not peer-to-peer communication among autonomous agents.

Natural surrounding wording may vary, but both concepts must be explicit: one bounded
model sample simulates the discussion, and no peer-to-peer autonomous-agent
communication occurs. Add a regression assertion that both documents retain this
meaning and that stale ambiguous-only wording cannot satisfy the test by itself.

Do not change runtime code, prompts, discussion behavior, package version, build ID,
schemas, dependencies, lockfile, workflow, tools or budgets. This is documentation truth,
not an architecture redesign.

## Package R4-2 — Case A4 pre-provisioned black-box MCP evidence

### Provisioning phase

Create fresh isolated CPython 3.12 client and server virtual environments outside the
repository. Pin the client to FastMCP `3.4.7`. Before starting any MCP transport,
preinstall into the server environment:

- FastMCP `3.4.7`; and
- `Council-of-Translation` directly from public Git commit
  `9d8f1f987efe73946377883e6ad3a681abe11989`.

Remote Git HTTPS operations on native Windows require external authority; local Git
operations remain sandboxed. Dependency provisioning is setup and may be retried only
before the MCP evidence attempt if a package download itself fails. Record every setup
attempt. Once the first MCP transport starts, no retry is permitted.

Before transport, verify:

- the server console script resolves inside the isolated server environment;
- installed package/module versions are `0.13.1`;
- installed FastMCP is `3.4.7`;
- the distribution's `direct_url.json` names the expected Git repository and exact
  commit `9d8f1f987efe73946377883e6ad3a681abe11989`;
- neither client nor server `sys.path` contains the shared/local repository.

### Single transport and calls

Use `fastmcp.Client`/`StdioTransport` from the client environment. Launch the already
installed server console script directly—do not place `uvx`, Git, package build or
dependency resolution inside `StdioTransport`. Point `COUNCIL_REVIEWS_DIR` to an isolated
temporary evidence directory. Use an initialization timeout of 120 seconds and preserve
all stderr.

Supply the same constant async clean sampling handler frozen by r3 and no elicitation
handler. Start exactly one transport. After connection:

1. call `get_server_info` exactly once and verify package/module `0.13.1`, build
   `truthful-boundaries-council-v11.1`, schemas `2.6/1.1`, budgets `6/13/18`, concurrency
   `3/3`, and exactly five public tools;
2. programmatically materialize one 16,000-character uppercase ASCII `S` string, assert
   its length and equality, and pass the complete value as both source and candidate;
3. call `review_translation` exactly once using the exact r3 A3 parameter packet;
4. call `view_review_record(full)` exactly once;
5. call `view_review_record(verification)` exactly once;
6. make no continuation, second review, retry, provider/model call or additional history
   call.

Preserve raw first text blocks and structured content independently. Parse the canonical
receipt from both representations and assert exact equality.

### A4 acceptance

All r3 A3 assertions remain required:

- pre-call lengths `16000/16000`, equal content;
- recorded original lengths `16000/16000`, reviewed lengths `12000/12000`, both
  truncated flags true;
- warnings contain `input_truncated`, `source_input_truncated`, and
  `candidate_input_truncated`;
- `NEEDS_HUMAN_REVIEW`, degraded true, fallback exactly `input_truncated`, chief
  `需人工复核 / 是`, no suggested translation;
- primary report contains both `仅审校了有界前缀` and `不构成全文发布许可`;
- decision support `insufficient` and outcome coherent;
- full structured-success reviewer coverage, sampling within budget 6, elicitation zero;
- verification complete, zero not-recorded/redacted fields, text/structured receipt
  equality;
- exactly one final terminal disposition matching the structured outcome;
- one transport, one review, zero retries after transport start, zero provider/model
  calls, and no local-source import.

Any failure after transport start is preserved without retry and reported as an
evidence-run deviation rather than automatically a product defect.

## Verification

Run at minimum:

```text
python -m compileall src tests
python -m pytest tests/integration/test_v10_release_contract.py -q
python -m pytest tests/integration/test_v131_input_completeness.py tests/unit/test_preflight_v2.py tests/integration/test_v131_discussion_coherence.py tests/integration/test_v131_history_minimization.py tests/integration/test_v131_evaluation_contract.py tests/integration/test_v10_release_contract.py -q
python -m pytest -q
git diff --check
```

Inspect the baseline-to-final diff and prove it contains exactly the three authorized
paths. Verify `uv.lock` is byte-identical and all package/runtime invariants remain
unchanged. A package rebuild is not required because no package input changes.

## Commit, hygiene and stop conditions

- Exactly one local commit is required for R4-1.
- Git push, PR, publication, release and deployment are forbidden.
- Subagents are forbidden; this correction is tightly bounded.
- The A4 runner and evidence may exist only in a boundary-checked temporary directory
  outside the repository and must be removed after report capture.
- Never traverse/read/copy `.learnings/**`, `reviews/**`, `myTest/**`, user review
  records or unrelated `.tmp/**` content.
- Preserve all admitted dirty/untracked assets and leave the index empty.
- Stop if any non-authorized repository path must change, published provenance cannot be
  proved, transport initialization fails again, any A4 tool call requires retry, or a
  frozen B/C/AUD item would need rerun.

Required Worker report:
`harness/reports/CAMPAIGN-014-q016-r4-worker.md`, untracked and unstaged. Create
`harness/reports/CAMPAIGN-014-q016-r4-ledger.md` only if a command fails or a stop
condition occurs.

The report must begin `READY_FOR_REVIEW` or `BLOCKED` and include baseline/final HEAD,
commit/path scope, exact commands/results, documentation assertions, complete A4 raw and
structured evidence, provenance checks, call/retry counts, cleanup, authority/dependency/
live/remote counts, skipped checks and remaining risk. Do not claim Q-016 acceptance or
lift the feature-expansion block; Foreman alone owns that decision.

