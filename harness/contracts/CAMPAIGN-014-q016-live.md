# External Gate Contract: CAMPAIGN-014 Q-016

## Control

- Gate: `Q-016 / Independent audit-remediation and incomplete-input evidence`
- Role: `INDEPENDENT AUDITOR + USER-OPERATED NORMAL GOOSE; FOREMAN ACCEPTANCE`
- State: `ISSUED`
- Published protected `main`: `9d8f1f987efe73946377883e6ad3a681abe11989`
- Accepted implementation: `9d23ed01f94be2ef0c724b3e0a3e7e1beba75c09`
- Publication PR: `#34`
- PR CI run: `32841766264` — six jobs passed
- Protected-main CI run: `32841918734` — six jobs passed
- Publication review: `harness/evaluations/CAMPAIGN-014-r2-publication-ci-review.md`
- Publication review SHA-256:
  `E685A257DCA91605B41BB33E930423F19CAA3DEF300EF231381357212D71C480`
- Required package/module: `0.13.1`
- Required diagnostic build: `truthful-boundaries-council-v11.1`
- Required persisted Review Schema: `2.6`
- Required verification receipt Schema: `1.1`
- Required Golden evaluator Schema: `2.1`
- Public tools: exactly five
- Sampling budgets: `6/13/18`
- Default independent-review concurrency: `3`
- Acceptance authority: Foreman only

Q-016 has two inseparable evidence parts. Part I is three fresh normal-Goose calls against
published protected `main`. Part II is an independent repository re-audit of the
deterministic fixes and the bounded evaluator/compatibility claims. Passing only one part
does not pass Q-016. Do not retry a live case to hide provider variation.

## Part I — normal-Goose published-main evidence

Keep the existing Goose Desktop extension command unchanged:

```text
uvx --refresh --from git+https://github.com/PigeonCrafty/mcp-council-of-translation mcp_council_of_translation
```

Do not add a commit suffix, alter extension environment variables, point at a local
checkout, or change Goose/provider/model/account between cases. Restart Goose once before
admission so `uvx --refresh` resolves current protected `main`.

Before Case A, call `get_server_info` exactly once. Stop unless it reports package/module
`0.13.1`, build `truthful-boundaries-council-v11.1`, schemas `2.6/1.1`, detail levels
`full/summary/verification`, budgets `6/13/18`, concurrency limit/max `3`, and exactly the
five public tools `review_translation`, `continue_review`, `view_review_record`,
`list_review_records`, `get_server_info`.

For every case:

1. Start a fresh Goose conversation.
2. Call `review_translation` exactly once with the specified values.
3. Preserve the complete original five-section `display_report`, returned `review_id`,
   compact structured fields when exposed, and actual duration when available.
4. Call `view_review_record(review_id, detail_level="full")` exactly once.
5. Call `view_review_record(review_id, detail_level="verification")` exactly once.
6. From the verification primary text, locate `Canonical verification_receipt JSON:`;
   parse and reproduce the immediately following fenced JSON unchanged.
7. Do not call `continue_review`, retry, invent a hidden field, or claim a value from
   prose when the client did not expose it.
8. Report every retry, provider error, missing field and deviation, using `none` when
   there was none.

The canonical JSON is the receipt authority. It must retain exact version identity,
terminal coherence, `verification_complete=true`, and no missing/redacted fields unless
the case explicitly demonstrates otherwise. Default `review_only` must not contain a
suggested translation.

### Case A — incomplete source must fail closed

Materialize `source_text` as a literal string containing exactly 12,001 uppercase ASCII
`S` characters. Do not pass a repetition expression, ellipsis, summary or attachment;
the MCP argument itself must contain all 12,001 characters.

```json
{
  "source_text": "<exactly 12,001 literal uppercase ASCII S characters>",
  "candidate_translation": "示例文本",
  "source_language": "en",
  "target_language": "zh-CN",
  "content_type": "ui",
  "context": "Q-016 输入完整性验证；只验证超过服务审校边界的源文本不得获得发布许可。",
  "audience": "中国大陆普通软件用户",
  "mode": "standard",
  "output_mode": "review_only",
  "interactive_mode": "off",
  "briefing_mode": "off",
  "trace_level": "summary",
  "history_mode": "full"
}
```

Required evidence:

- recorded source original length is `12001`, reviewed length is `12000`, and
  `source_truncated=true`; candidate is not truncated;
- warnings contain `input_truncated` and `source_input_truncated`;
- status is `NEEDS_HUMAN_REVIEW`, degradation is true, fallback reason code is
  `input_truncated`, disposition is `需人工复核 / 是`;
- decision support is `insufficient` and coherent with the terminal disposition;
- the primary report visibly says only a bounded prefix was reviewed and that it is not
  full-text publication permission;
- sampling stays within budget and elicitation remains zero.

If Goose cannot materialize the exact literal argument, report Case A as `CLIENT_LIMIT`
without substituting a smaller string. That is a Q-016 deviation, not proof of a server
failure.

### Case B — ordinary percentages and surrounding URL punctuation must not block

```json
{
  "source_text": "Progress is 100% complete. See (https://example.com/a).",
  "candidate_translation": "进度已完成 100%。请查看 https://example.com/a。",
  "source_language": "en",
  "target_language": "zh-CN",
  "content_type": "ui",
  "context": "状态页上的完成进度与帮助链接；括号和句末标点不是 URL 身份的一部分。",
  "audience": "中国大陆普通软件用户",
  "mode": "lightweight",
  "output_mode": "review_only",
  "interactive_mode": "off",
  "briefing_mode": "off",
  "trace_level": "summary",
  "history_mode": "full"
}
```

Required evidence:

- deterministic preflight is nonblocking and has no failed printf-placeholder or URL
  preservation check;
- `100%` is not classified as a printf token, and source wrapper punctuation is not part
  of URL identity;
- any model-authored language preference remains distinct from deterministic preflight;
  it must not be misreported as a protected-token blocker;
- no truncation warning or input-truncation fallback is present.

### Case C — real protected tokens must still block

```json
{
  "source_text": "Delete {count} files with %s. See https://example.com/search?q=(term).",
  "candidate_translation": "删除文件。请查看 https://example.com/search?q=(term。",
  "source_language": "en",
  "target_language": "zh-CN",
  "content_type": "ui",
  "context": "危险操作确认；{count}、%s 和完整帮助 URL 都是运行时必需的技术字面量。",
  "audience": "中国大陆普通软件用户",
  "mode": "strict",
  "output_mode": "review_only",
  "interactive_mode": "off",
  "briefing_mode": "off",
  "trace_level": "summary",
  "history_mode": "full",
  "do_not_translate_literals": [
    "{count}",
    "%s",
    "https://example.com/search?q=(term)"
  ],
  "hard_constraints": [
    "required_literal:{count}",
    "required_literal:%s",
    "required_literal:https://example.com/search?q=(term)"
  ]
}
```

Required evidence:

- preflight is blocking and independently records the missing `{count}`, missing `%s`,
  and damaged balanced URL identity; protected-token checks remain deterministic;
- status/disposition is `NEEDS_HUMAN_REVIEW`, `需人工复核 / 是`, with no suggested
  translation and no truncation fallback;
- reviewer findings may corroborate but must not erase or downgrade deterministic
  blockers; verification remains terminally coherent.

## Part II — independent repository re-audit

Audit the public repository at exact protected-main commit
`9d8f1f987efe73946377883e6ad3a681abe11989`. Do not audit a local unpublished branch.
Use source inspection plus fresh tests; prior Worker/Foreman prose is supporting evidence,
not a substitute for independent checks.

At minimum run:

```text
python -m compileall src tests
python -m pytest tests/integration/test_v131_input_completeness.py tests/unit/test_preflight_v2.py tests/integration/test_v131_discussion_coherence.py tests/integration/test_v131_history_minimization.py tests/integration/test_v131_evaluation_contract.py tests/integration/test_v10_release_contract.py -q
python -m pytest -q
```

Re-evaluate the original audit findings individually:

- `AUD-001`: truncation is a recorded fail-closed condition across normal completion,
  briefing return, persistence/history and continuation; a clean reviewed prefix cannot
  authorize the omitted suffix.
- `AUD-002`: percentage prose and URL wrapper punctuation are negative controls, while
  real printf placeholders and balanced internal URL syntax remain protected.
- `AUD-003`: a malformed discussion envelope causes one atomic unavailable round,
  preserves Round 1, does not consume partial statements and does not retry.
- `AUD-004`: post-discussion cluster consensus is recomputed from final material role
  positions and remains separate from optional narrative summaries.
- `AUD-005`: V1 `summary` is the exact bounded six-field privacy projection; V1 `full`
  remains byte-compatible and V1 verification stays canonical/private.
- `AUD-006`: Golden Evaluator Schema `2.1` names only critical-presence-contract accuracy
  and clean-case-no-cluster accuracy. It must not claim defect-identity recall, span
  recall, severity calibration, general false-positive performance or an included blind
  benchmark. `docs/blind-evaluation-set.schema.json` must require independent-curation
  provenance and is a handoff schema, not a quality result.
- `AUD-007`: declared FastMCP range is exactly `>=2.13.0.2,<4`. Evidence covers the exact
  locked/CI floor and installed-wheel 3.4.7 smoke; the range is an evidence boundary, not
  a claim that every intervening release was tested.

Also verify that documentation describes Targeted Discussion as one model sample asked
to simulate bounded cross-role deliberation, not actual peer-to-peer agent communication.

For each AUD item return `CLOSED`, `PARTIALLY_CLOSED`, or `OPEN`, with exact file/line or
test evidence and a counterexample for every non-closed result. Explicitly state whether
the original `BLOCK NEXT CAMPAIGN` recommendation can be lifted. Separate product defects
from documentation/evidence limitations.

## Acceptance and return packet

Return one packet containing:

1. the admission `get_server_info` result;
2. A/B/C review IDs, complete original reports, full-view structured fields when exposed,
   canonical verification JSON and durations;
3. every live deviation without retry;
4. exact audited Git commit and commands/results;
5. the AUD-001..AUD-007 disposition table with evidence;
6. a final independent recommendation: `LIFT BLOCK`, `KEEP BLOCK`, or
   `LIFT WITH EXPLICIT LIMITATIONS`.

Q-016 passes only if the Foreman accepts all three fresh live records and the independent
re-audit. Live model wording may vary; deterministic safety, receipt truth, bounded claims
and terminal coherence may not. Until acceptance, CAMPAIGN-014 is published but not
externally closed, and ordinary feature expansion remains blocked.
