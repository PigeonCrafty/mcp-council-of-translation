# Live Gate Protocol Correction: Q-003 Interactive CLI Fallback r2

## Control

- Role: `FOREMAN`
- Harness mode: `STRICT_CAMPAIGN`
- Gate: `Q-003` Goose Desktop and interactive CLI evidence
- Contract revision: `r2`
- Parent contract: `harness/contracts/Q-003-desktop-cli-live-r1.md`
- Parent review: `harness/evaluations/Q-003-desktop-cli-live-r1-review.md`
- Parent review SHA-256:
  `2625B52D58578B670600F1A032B4CB8864F338B6C578F0E32BDD9DDE235CEE73`
- Published protected `main`: `617b696c94624988f03a64ab58e1d42a66697546`
- Required package/module: `0.10.2`
- Required diagnostic build: `evidence-value-council-v8.2`
- Required schema: `2.4`
- Client scope: the same interactive Goose CLI session only
- Evidence authority: the new persisted Schema 2.4 record plus the preserved r1 records

This revision preserves the accepted r1 Desktop evidence and the truthful r1 CLI pending
record. It corrects only the unsupported native-form parity assumption. It authorizes no
product, test, dependency, lock, Goose installation, extension-command, release or
deployment change and no Desktop rerun.

## Fixed runtime

Keep the existing extension command, provider, model and account unchanged:

```text
uvx --refresh --from git+https://github.com/PigeonCrafty/mcp-council-of-translation mcp_council_of_translation
```

Do not edit the extension configuration to satisfy r2. The prior CLI record already
proves V0.10.2/build v8.2/schema 2.4 and truthful failure before sampling.

## CLI-only corrected workflow

Continue in the same interactive CLI conversation that returned pending record
`20260824T014635498220Z_cb108a4de83e`. Supply the missing context in normal conversation,
then instruct Goose to call `review_translation` exactly once more with this complete
packet:

```text
source_text: Continue
candidate_translation: 继续
source_language: en
target_language: zh-CN
content_type: ui
context: 多步骤设置向导底部的主操作按钮
audience: 中国大陆普通软件用户
mode: standard
output_mode: review_only
interactive_mode: auto
briefing_mode: auto
decision_fallback: council_adjudication
trace_level: full
history_mode: full
style_guide: 简洁、直接
project_rules: 重点判断按钮是否明确表达进入下一阶段
notes: Q-003-r2 CLI explicit-context fallback 2026-08-24
```

Leave glossary, brand guidance, technical constraints, DNT, hard constraints,
references and known exceptions empty. Do not pass the literal Chinese word `空` as a
field value; omit an empty optional field instead.

Because this packet has a recognized content type plus multiple independent context
categories, `briefing_mode=auto` should proceed without native elicitation. Do not call
`continue_review`, `view_review_record` or `list_review_records`, and do not start another
review after this corrected call.

## Acceptance criteria

The new CLI record must satisfy all of the following:

1. Version/build/schema remain `0.10.2` / `evidence-value-council-v8.2` / `2.4`; the
   persisted task contains the unique r2 note.
2. The effective brief normalizes to `content_type=ui`, retains the supplied audience and
   usage context, and reports sufficient context without fabricated user-briefing
   provenance.
3. No native briefing form is required in the corrected call; briefing elicitation calls
   are zero and sampling begins only after the context-sufficiency decision.
4. All six planned UI reviewers complete with full structured coverage, zero unavailable
   samples and zero parse failures.
5. Sampling remains within the standard budget of 13 and configured concurrency remains
   bounded at three.
6. Status is a truthful completed disposition with `degraded=false`, no warning and no
   fallback caused by client transport or missing briefing.
7. The original primary report has exactly five sections, remains review-only, exposes no
   internal ID and has `suggested_translation=null`.
8. The r1 pending record remains immutable and auditable as the native-elicitation
   limitation; it is not counted as a successful Council review.

The corrected record need not reproduce Desktop wording byte-for-byte and need not open
an outcome DecisionPoint.

## Retry and evidence return

Allow at most one additional attempt only for a clearly transient provider/transport
failure. Do not retry for preferred wording. No screenshot is required in r2: user
client attribution, the unique persisted CLI note and the linked pending-to-success
record pair are the bounded identity evidence.

Return:

```text
CLI-r2: <new review_id>
Retry: none or exact transient-failure summary
```

The Foreman will independently load the new record and the preserved r1 pair, then write
`harness/evaluations/Q-003-desktop-cli-live-r2-review.md` and choose exactly one:

- `ACCEPTED`: Desktop native elicitation and CLI explicit-context fallback both work
  truthfully; mark Q-003 accepted.
- `CHANGES_REQUESTED`: the compatible CLI reaches the server but a repository-correctable
  defect prevents the bounded fallback workflow.
- `BLOCKED`: client startup, credentials, provider, transport or external availability
  prevents a valid corrected record.
