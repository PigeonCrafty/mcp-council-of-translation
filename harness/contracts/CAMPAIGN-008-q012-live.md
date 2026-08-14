# Live Gate Protocol: CAMPAIGN-008 Q-012

## Control

- Role: `FOREMAN`
- Harness mode: `STRICT_CAMPAIGN`
- Gate: `Q-012` value-first Council live usefulness and non-repetition evidence
- Published `main` under test:
  `e3d3de275915088c1430a243dfd9c2e410cbc58a`
- Publication PR: `https://github.com/PigeonCrafty/mcp-council-of-translation/pull/17`
- Required package/module: `0.10.0`
- Required diagnostic build: `evidence-value-council-v8`
- Required schema: `2.4`
- Provider/model rule: use one unchanged Goose provider, model and account for all cases
- Mutation boundary: live provider calls and review-record writes are authorized; source,
  tests, dependencies, lockfiles, Goose installation, credentials, Git and GitHub state
  must not change during the gate

Q-012 is a post-publication Foreman gate, not a Worker implementation contract. It tests
whether the V0.10 primary report exposes material Council value without turning six roles
into six repetitive essays. Structured records, not Goose's paraphrase, are the telemetry
authority.

## Fixed Goose configuration

Keep the existing normal-main STDIO command unchanged for the whole gate:

```text
uvx --refresh --from git+https://github.com/PigeonCrafty/mcp-council-of-translation mcp_council_of_translation
```

Set these environment values once, then fully restart Goose once before the admission
check. Do not change the command, arguments, environment, provider or model between cases.

```yaml
envs:
  COUNCIL_REVIEW_CONCURRENCY: "3"
  COUNCIL_REVIEWS_DIR: 'C:\Users\GeZhu\MyMCP\mcp-council-of-translation\.tmp\q012'
```

No repository push is allowed until the gate is decided, so the normal-main command
continues to resolve the published snapshot named above. If `get_server_info` does not
report the required version, build, schema and concurrency `3/configured`, stop before
sampling and report the mismatch.

## Common call rules

Every case calls `review_translation` exactly once with:

- `source_language="en"`, `target_language="zh-CN"`;
- `mode="standard"`, `output_mode="review_only"`;
- `interactive_mode="off"`, `briefing_mode="off"`;
- `decision_fallback="council_adjudication"`;
- `trace_level="full"`, `history_mode="full"`.

Do not call `view_review_record`, `list_review_records` or `continue_review` inside the
case session. Return the tool's original `display_report`, `review_id`, status and
`council_value_metrics`; do not reconstruct missing fields.

## Case A — clean approved wording

Purpose: prove that six successful reviewers are visibly accounted for without six
repetitive approval paragraphs.

```json
{
  "source_text": "Bigger than bigger",
  "candidate_translation": "比大更大",
  "content_type": "marketing",
  "context": "中国大陆官网首页的纯品牌宣传标语，不是按钮、CTA、导航或任何交互控件。",
  "audience": "中国大陆普通消费者",
  "term_glossary": "Bigger than bigger = 比大更大（项目批准译法）",
  "style_guide": "品牌标语保持短促、自然、有冲击力。",
  "project_rules": "本条为已批准的品牌宣传标语，不得改写为按钮或功能文案。",
  "brand_guidelines": "保留项目批准译法‘比大更大’，除非发现语义、技术完整性或明确硬规则冲突。",
  "reference_translations": "Bigger than bigger -> 比大更大（approved）",
  "technical_constraints": "纯文本；无占位符；不承担交互动作。",
  "do_not_translate_literals": [],
  "hard_constraints": [],
  "known_exceptions": "无",
  "notes": "Q-012 Case A：clean confirmation compression。"
}
```

Expected evidence:

- six successful marketing roles and full coverage;
- zero unavailable roles and no false material blocker;
- primary report has exactly the five V0.10 sections in frozen order;
- `Council 新增视角` states that no new material issue was found, once;
- all roles are accounted for in `角色覆盖与分工`, but redundant natural evidence is
  compressed rather than repeated;
- report is at most 1,200 Unicode code points and chief disposition is last.

## Case B — deterministic blocker plus model corroboration

Purpose: prove that one placeholder defect remains one logical issue when deterministic
preflight and a reviewer both detect it, while a distinct semantic reversal remains
separate.

```json
{
  "source_text": "Delete {count} files? This action cannot be undone.",
  "candidate_translation": "删除文件吗？此操作可以撤销。",
  "content_type": "ui",
  "context": "批量永久删除前的确认对话框正文；{count} 是运行时文件数量，占位符必须原样保留。",
  "audience": "中国大陆普通软件用户",
  "style_guide": "危险操作必须明确、直接，不得弱化不可撤销性。",
  "project_rules": "不得遗漏数量占位符；不得把不可撤销改成可以撤销。",
  "technical_constraints": "必须逐字保留 {count}。",
  "do_not_translate_literals": ["{count}"],
  "hard_constraints": ["required_literal:{count}"],
  "notes": "Q-012 Case B：deduplicated blocker and distinct semantic issue。"
}
```

Expected evidence:

- placeholder loss is visible as a deterministic release blocker and the report never
  says that no material issue was found;
- deterministic and reviewer evidence for the same placeholder loss do not become two
  unique issues;
- the reversal of `cannot` to `可以` remains a distinct semantic issue if returned by a
  valid reviewer finding;
- chief disposition is not unqualified `可发布`;
- no user preference, Council fallback or model prose can override the placeholder rule.

## Case C — panoramic but non-repetitive privacy copy review

Purpose: prove that materially different professional lenses remain visible when the
candidate omits a usage limitation, without inventing six variants of the same point.

```json
{
  "source_text": "We only use your location while the app is open.",
  "candidate_translation": "我们会使用您的位置信息。",
  "content_type": "legal_risk",
  "context": "中国大陆移动应用首次请求定位权限前的说明文案；产品实际只在应用打开期间使用定位。",
  "audience": "中国大陆普通移动应用用户",
  "style_guide": "准确、克制、易懂；不得扩大数据使用范围。",
  "project_rules": "必须保留 only 和 while the app is open 所限定的使用范围。",
  "technical_constraints": "纯文本，无占位符。",
  "hard_constraints": [],
  "notes": "Q-012 Case C：distinct panoramic value without repetition。"
}
```

Expected evidence:

- the omitted scope limitation is material and visible before the chief conclusion;
- distinct fidelity, product/UX and risk implications may remain separate only when
  their structured issue identity or evidence is materially different;
- repeated statements of the same omission collapse into corroboration;
- no unsupported statute, mandatory legal conclusion or hidden chain-of-thought appears;
- if discussion occurs, its displayed marginal value matches structured deltas; if no
  discussion occurs, the report does not manufacture one.

## Evidence return

Return the three review IDs as `A`, `B`, `C`. After all cases, the Foreman will read only
those three JSON records from the fixed `COUNCIL_REVIEWS_DIR` and independently verify:

- exact package/build/schema, call budgets, sample coverage and provider parse status;
- five-section order, report lengths, final-disposition placement and absence of internal
  IDs;
- one contribution entry per active role and valid contribution-kind totals;
- issue deduplication/non-overmerge and truthful discussion marginal value;
- `review_only` keeps `suggested_translation` null.

## Acceptance decision

`ACCEPTED` requires all three valid records to satisfy protocol and safety invariants,
Case A to demonstrate material repetition compression, Case B to demonstrate blocker
truthfulness and exact correlation, and Case C to present at least one useful material
blind spot without repetitive padding. Provider wording may vary; exact prose equality is
not required.

`CHANGES_REQUESTED` applies when the server is compatible but the value-first display,
correlation, role accounting or chief consistency fails a reproducible criterion.

`BLOCKED` applies only when the fixed published build cannot complete enough valid live
records to evaluate the gate because of provider, credential, transport or external
availability failure.
