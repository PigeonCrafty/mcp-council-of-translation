# Live Gate Protocol: CAMPAIGN-010 Q-012 V0.10.2 Final Revalidation

## Control

- Role: `FOREMAN`
- Harness mode: `STRICT_CAMPAIGN`
- Gate: `Q-012` value-first Council live usefulness and non-repetition evidence
- Accepted product commit: `f58306d0df42fc27d46dd5049348ccfce8a0f6f8`
- Published protected `main`: `2b4297d003a7ac4b69185200c8e2fd96dca738ce`
- Publication PR: `https://github.com/PigeonCrafty/mcp-council-of-translation/pull/20`
- Required package/module: `0.10.2`
- Required diagnostic build: `evidence-value-council-v8.2`
- Required schema: `2.4`
- Provider/model rule: use one unchanged normal Goose provider, model and account
- Runtime rule: keep the existing extension command without a Git commit suffix
- Evidence authority: persisted Schema 2.4 JSON, not Goose prose reconstruction

Q-012 remains `changes_requested` until all three new post-publication cases are valid
and independently accepted. Local replay and publication CI do not accept the live gate.

## Fixed Goose extension

Keep the existing command unchanged:

```text
uvx --refresh --from git+https://github.com/PigeonCrafty/mcp-council-of-translation mcp_council_of_translation
```

Set these raw environment values in Goose Desktop with no quotes or surrounding spaces:

```text
COUNCIL_REVIEW_CONCURRENCY
3

COUNCIL_REVIEWS_DIR
C:\Users\GeZhu\MyMCP\mcp-council-of-translation\.tmp\q012-final
```

Fully exit Goose so the old STDIO child terminates, then restart it once. Do not change
the command, environment, provider, model or account between cases.

## Admission

Call `get_server_info` once. Stop before sampling unless all values match:

- package/module `0.10.2`;
- build `evidence-value-council-v8.2`;
- schema `2.4`;
- concurrency limit/disposition `3/configured`;
- budgets `6/13/18`.

## Common review call

Run each case in a fresh Goose conversation. Call `review_translation` exactly once with
`source_language=en`, `target_language=zh-CN`, `mode=standard`,
`output_mode=review_only`, `interactive_mode=off`, `briefing_mode=off`,
`decision_fallback=council_adjudication`, `trace_level=full`, `history_mode=full`.

Do not call `view_review_record`, `list_review_records` or `continue_review` in a case
conversation. Ask Goose to return the original `display_report`, `review_id`, status,
`council_value_metrics`, sampling/coverage fields and final disposition without
inventing fields absent from the tool result.

## Case A — clean grouped confirmation

- Source: `Bigger than bigger`
- Candidate: `比大更大`
- Content type: `marketing`
- Context: 中国大陆官网首页的纯品牌宣传标语，不是按钮、CTA、导航或交互控件。
- Audience: 中国大陆普通消费者
- Glossary/reference: `Bigger than bigger = 比大更大（项目批准译法）`
- Style: 品牌标语保持短促、自然、有冲击力。
- Project rule: 本条为已批准的品牌宣传标语，不得改写为按钮或功能文案。
- Brand guideline: 保留批准译法“比大更大”，除非存在语义、技术或明确硬规则冲突。
- Technical constraints: 纯文本；无占位符；不承担交互动作。

Accept only if six marketing roles complete with full coverage, confirmation-only roles
are grouped into one readable line, no false issue appears, the report uses exactly five
sections, stays at most 1,200 code points and ends with the chief disposition.

## Case B — placeholder blocker plus semantic reversal

- Source: `Delete {count} files? This action cannot be undone.`
- Candidate: `删除文件吗？此操作可以撤销。`
- Content type: `ui`
- Context: 批量永久删除前的确认对话框；`{count}` 是运行时文件数量并须原样保留。
- Audience: 中国大陆普通软件用户
- Style: 危险操作必须明确、直接，不得弱化不可撤销性。
- Project rules: 不得遗漏数量占位符；不得把不可撤销改成可以撤销。
- Technical constraints: 必须逐字保留 `{count}`。
- DNT: `[{count}]`
- Hard constraints: `[required_literal:{count}]`

Accept only if placeholder loss remains a deterministic blocker, deterministic/reviewer
evidence forms one logical issue and exactly one primary work item, `cannot` -> `可以`
remains one distinct semantic repair, discussion paraphrases add zero new evidence unless
a genuine structured delta exists, duplicate execution-order prose is absent, and the
chief does not return unqualified publishability.

## Case C — panoramic privacy-copy value

- Source: `We only use your location while the app is open.`
- Candidate: `我们会使用您的位置信息。`
- Content type: `legal_risk`
- Context: 中国大陆移动应用首次请求定位权限前的说明；实际只在应用打开期间使用定位。
- Audience: 中国大陆普通移动应用用户
- Style: 准确、克制、易懂；不得扩大数据使用范围。
- Project rule: 必须保留 `only` 和 `while the app is open` 限定的使用范围。
- Technical constraints: 纯文本，无占位符。

Accept only if the omitted scope limitation is material and visible before the chief;
the shared repair renders exactly once; distinct fidelity/product-UX/risk consequences
remain visible without duplicate execution-order prose; no unsupported statute or hidden
reasoning appears; and displayed discussion value matches structured deltas.

## Evidence return and decision

Return only the three new review IDs labeled `A`, `B`, `C`. The Foreman will read those
exact files from `.tmp/q012-final`, verify version, calls, coverage, contribution totals,
issue identity, report order/length/privacy, chief consistency, null
`suggested_translation` and marginal discussion truth, then issue one versioned Q-012
review.

- `ACCEPTED`: all three valid records satisfy their case and shared invariants.
- `CHANGES_REQUESTED`: compatible live records reproduce a server value/presentation
  defect.
- `BLOCKED`: provider, credentials, transport or external availability prevents enough
  valid records to evaluate the gate.
