# Live Gate Protocol: Q-003 Desktop/CLI Client Parity r1

## Control

- Role: `FOREMAN`
- Harness mode: `STRICT_CAMPAIGN`
- Gate: `Q-003` Goose Desktop and interactive CLI evidence
- Contract revision: `r1`
- Published protected `main`: `617b696c94624988f03a64ab58e1d42a66697546`
- Accepted product implementation: `f58306d0df42fc27d46dd5049348ccfce8a0f6f8`
- Required package/module: `0.10.2`
- Required diagnostic build: `evidence-value-council-v8.2`
- Required schema: `2.4`
- Provider/model rule: use one unchanged normal Goose provider, model and account
- Runtime rule: keep the existing extension command unchanged and restart the client between Desktop and CLI runs
- Evidence authority: persisted Schema 2.4 records plus one privacy-safe client-identity capture per run

This is an evidence-only live gate. It authorizes no product, test, dependency, lock,
Goose installation, extension-command, release or deployment change. It does not reopen
CAMPAIGN-010 and does not start CAMPAIGN-011.

## Purpose

The repository already has accepted live evidence for briefing, outcome selection,
Council delegation, targeted reconsideration, concise primary output, context coherence,
bounded concurrency and Council value. Q-003 remains partial only because the evidence
does not establish an interactive form round trip in both Goose Desktop and the
interactive Goose CLI.

Use the deterministic sampling-free Briefing Gate for this comparison. Do not require a
model-generated DecisionPoint: Q-007 already accepts that product path, while its
appearance is provider-output-dependent and would make a client-parity gate flaky.

## Fixed extension and environment

Keep the existing extension command unchanged in both clients:

```text
uvx --refresh --from git+https://github.com/PigeonCrafty/mcp-council-of-translation mcp_council_of_translation
```

Use these raw environment values, without quotes or surrounding spaces:

```text
COUNCIL_REVIEW_CONCURRENCY
3

COUNCIL_REVIEWS_DIR
C:\Users\GeZhu\MyMCP\mcp-council-of-translation\.tmp\q003-client-parity
```

The Desktop extension environment and the CLI process environment must resolve to these
same values. Do not change the extension command, provider, model or account between
runs. Fully exit Goose Desktop before the CLI run so the Desktop STDIO child is gone.

## Admission

In each client, start a fresh conversation and call `get_server_info` once. Stop before
`review_translation` unless all values match:

- package/module `0.10.2`;
- build `evidence-value-council-v8.2`;
- schema `2.4`;
- concurrency limit/disposition `3/configured`;
- budgets `6/13/18`;
- exact five public tools.

A version/cache mismatch is `BLOCKED` evidence, not permission to edit the extension
command during the run.

## Shared review case

Each client must call `review_translation` exactly once with these initial values:

```text
source_text: Continue
candidate_translation: 继续
source_language: en
target_language: zh-CN
content_type: unspecified
context: <empty>
audience: <empty>
mode: standard
output_mode: review_only
interactive_mode: auto
briefing_mode: always
decision_fallback: council_adjudication
trace_level: full
history_mode: full
notes: Q-003 client parity; use Desktop or CLI as the client label.
```

Leave glossary, style, project rules, brand guidance, technical constraints, DNT,
hard constraints, references and known exceptions empty. This deliberately requires the
Briefing Gate before any reviewer sampling.

When the form appears, submit exactly:

```text
domain: 软件产品
content_type: ui
audience: 中国大陆普通软件用户
tone_goal: 简洁、直接
primary_focus: 判断按钮是否明确表达进入下一阶段
usage_context: 多步骤设置向导底部的主操作按钮
```

Do not choose Council delegation in place of these values. Do not cancel or decline the
form. After the review returns, do not call `continue_review` and do not run a second
review in the same conversation.

## Client workflows

### D — Goose Desktop

1. Verify the fixed extension environment, fully restart Desktop and open a fresh chat.
2. Run admission, then the shared review case.
3. Capture one screenshot while the Briefing form is visibly rendered in Goose Desktop.
4. Submit the six fixed values and retain the returned `review_id`.
5. Capture or copy the original primary `display_report`; do not ask Goose to rewrite it.

### C — interactive Goose CLI

1. Fully exit Desktop and confirm its STDIO child has terminated.
2. Set the two fixed environment values in the normal user terminal, then start the
   installed interactive Goose CLI using its normal session command.
3. Run admission, then the shared review case.
4. Capture one terminal screenshot or transcript showing the CLI identity and the
   interactive Briefing prompt, without credentials or unrelated terminal history.
5. Submit the same six values and retain the returned `review_id` and original primary
   `display_report`.

The CLI executable's logging directory must be user-writable. A CLI startup failure
before MCP invocation is external `BLOCKED` evidence and must not be reported as a
Council server defect.

## Acceptance criteria

Both D and C must satisfy all of the following:

1. The correct V0.10.2 diagnostics pass before review sampling.
2. One Briefing form is visibly rendered by the named client and accepts all six fixed
   values.
3. `briefing` precedes the first independent-review sample in `phase_trace`.
4. `briefing_elicitation_calls=1`; no fabricated user answer is recorded.
5. `effective_brief` contains the submitted values, provenance identifies user briefing,
   and `context_confidence=full`.
6. Planned independent reviewers complete with full structured coverage; unavailable and
   parse-failure counts are zero.
7. Sampling remains within the standard budget of 13; no hidden retry exceeds budget.
8. The final status is a truthful completed disposition with `degraded=false`, no warning
   and no fallback caused by client transport or interaction.
9. The primary report uses the accepted five-section V0.10.2 presentation and does not
   expose internal IDs; `suggested_translation` is null.
10. The persisted full record can be loaded from the fixed review directory and agrees
    with the tool response.

Desktop and CLI prose need not be byte-identical. Provider wording, exact sampling wall
time and the presence or absence of a model-generated outcome DecisionPoint are not
cross-client parity criteria.

## Retry and evidence hygiene

- Permit at most one retry per client for a clearly transient provider or transport
  failure. Preserve and report the failed attempt's ID or absence of an ID and its error.
- Do not retry to obtain preferred model wording.
- Do not include API keys, provider tokens, account identifiers, full Goose configuration
  files or unrelated terminal content in captures.
- Raw records and screenshots remain ignored/local evidence. The Foreman evaluation will
  record only hashes, bounded telemetry, client identity and the acceptance decision.
- Do not commit `myTest/`, `.tmp/`, raw review records or screenshots.

## Evidence return and decision

Return:

```text
Desktop: <review_id>
CLI: <review_id>
Desktop capture: <attached or local path>
CLI capture/transcript: <attached or local path>
Retries: <none or exact bounded summary>
```

The Foreman will independently load the two exact records and verify form timing,
provenance, coverage, calls, status, presentation, review-only behavior and persistence.
The Foreman then writes `harness/evaluations/Q-003-desktop-cli-live-r1-review.md` and
chooses exactly one decision:

- `ACCEPTED`: both client records and identity captures satisfy the contract; Q-003 is
  marked accepted.
- `CHANGES_REQUESTED`: compatible clients reproduce a Council/MCP interaction or record
  defect that can be corrected within the repository.
- `BLOCKED`: client startup, credentials, provider, transport, capture availability or
  other external state prevents enough evidence to decide.
