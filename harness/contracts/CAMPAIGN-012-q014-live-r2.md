# Live Gate Contract: CAMPAIGN-012 Q-014-r2

## Control

- Gate: `Q-014 / Normal-Goose canonical verification receipt evidence`
- Role: `USER-OPERATED NORMAL GOOSE; FOREMAN ACCEPTANCE`
- State: `ISSUED`
- Published protected `main`: `c5d38a1f2f8ef4cafaada98f93583e1532405a3b`
- Published implementation: `47ec9256f0eb55892f5f58ec4bd6609aacf18aa8`
- Required package/module: `0.12.1`
- Required diagnostic build: `verifiable-evidence-council-v10.1`
- Required persisted schema: `2.5`
- Required verification receipt schema: `1.0`
- Public tools: exactly five
- Sampling budgets: `6/13/18`
- Default independent-review concurrency: `3`
- Cases: exactly A, B and C below, each in a fresh Goose conversation
- Acceptance authority: Foreman only

This revision supersedes `harness/contracts/CAMPAIGN-012-q014-live.md`. The original
Council behavior evidence remains valid, but r1 failed because normal Goose did not
expose MCP structured content. V0.12.1 therefore places the same canonical receipt JSON
inside the verification response's first text block.

## Runtime boundary

Keep the existing Goose Desktop extension command unchanged:

```text
uvx --refresh --from git+https://github.com/PigeonCrafty/mcp-council-of-translation mcp_council_of_translation
```

Do not add a commit suffix, change extension environment variables, point at a local
checkout, or change Goose/provider/model/account between cases. Restart Goose once before
admission so `uvx --refresh` resolves current `main`.

Before Case A, call `get_server_info` exactly once. Stop without running any case unless
it reports package/module `0.12.1`, build `verifiable-evidence-council-v10.1`, persisted
Schema `2.5`, receipt Schema `1.0`, detail levels `full/summary/verification`, budgets
6/13/18, concurrency limit/max 3 and exactly five public tools.

For every case:

1. Start a fresh Goose conversation.
2. Call `review_translation` exactly once with the exact parameters below.
3. Preserve its original five-section `display_report` and returned `review_id`.
4. Call `view_review_record(review_id, detail_level="verification")` exactly once.
5. Do not call `continue_review`, request `full`, retry, or ask any model to reconstruct
   missing fields.
6. Print the complete original verification primary text verbatim.
7. Locate the literal label `Canonical verification_receipt JSON:`. Immediately after it
   there must be exactly one fenced `json` block and nothing after that fence.
8. Parse that block as JSON and print it verbatim. Do not translate, infer, rename,
   reorder or regenerate any field. If the label/block is absent or parsing fails, stop
   the case and report the literal failure.

The parsed text JSON is the evidence authority for this gate. It must use exactly these
top-level keys in order: `receipt_schema_version`, `review_id`, `record`, `serving`,
`routing`, `reviewer_execution`, `runtime`, `preflight`, `issues`, `outcome`, `coherence`,
`availability`.

The human receipt preceding the JSON must retain exactly five headings in order:
`Council 验证回执`, `记录与路由`, `覆盖与调用`, `风险与裁决`, `一致性与可用性`.
The combined verification text must remain at most 12,000 Unicode code points.

## Case A — lightweight clean control

```json
{
  "source_text": "You may withdraw this authorization at any time.",
  "candidate_translation": "您可以随时撤回此授权。",
  "source_language": "en",
  "target_language": "zh-CN",
  "content_type": "legal_risk",
  "context": "隐私设置中的授权说明；原文与译文都只表达用户可随时撤回本次授权。",
  "audience": "中国大陆普通软件用户",
  "mode": "lightweight",
  "output_mode": "review_only",
  "interactive_mode": "off",
  "briefing_mode": "off",
  "trace_level": "summary",
  "history_mode": "full",
  "project_rules": "保持授权与撤回语义，不增加法律结论。"
}
```

Required parsed JSON evidence:

- route/profile/reasons are exactly the legal-risk lightweight route and
  `content_legal_risk`, `mode_lightweight`, `deterministic_preflight_coverage`,
  `risk_focused`;
- ordered active roles are fidelity, terminology, risk ambiguity and fluency using their
  canonical IDs;
- four samples are `structured_success`, coverage is `full`, successful/unavailable are
  4/0;
- sampling/budget/elicitation are 4/6/0;
- no blocker, degradation, warning or fallback is fabricated;
- publishability/review-needed is `可发布/否`; suggested translation is absent;
- terminal disposition occurs once, is last and matches structured outcome;
- verification is complete with no missing/redacted fields.

## Case B — standard material-edit disposition

```json
{
  "source_text": "By continuing, you authorize us to share your precise location with selected partners. You may withdraw this authorization at any time.",
  "candidate_translation": "继续即表示您同意我们与合作伙伴共享您的大致位置。您不可撤回同意。",
  "source_language": "en",
  "target_language": "zh-CN",
  "content_type": "legal_risk",
  "context": "隐私设置确认页；在用户允许向第三方共享精确定位前展示。只评估译文是否忠实表达授权范围、数据精度和撤回权，不提供法律意见。",
  "audience": "中国大陆普通软件用户",
  "mode": "standard",
  "output_mode": "review_only",
  "interactive_mode": "off",
  "briefing_mode": "off",
  "trace_level": "summary",
  "history_mode": "full",
  "project_rules": "不得把 authorize 弱化为普通同意；不得把 precise location 改成大致位置；不得省略 selected 的范围限定；不得反转撤回权。"
}
```

Required parsed JSON evidence:

- route/profile/reasons are exactly the legal-risk standard route and
  `content_legal_risk`, `mode_standard`, `deterministic_preflight_coverage`,
  `risk_panorama`;
- ordered active roles are fidelity, terminology, product context, UX copy, risk
  ambiguity and fluency using canonical IDs;
- six samples succeed, coverage is `full`, unavailable is zero;
- sampling is between 6 and 13, budget is 13 and elicitation is zero;
- issue count is nonzero while deterministic preflight remains nonblocking unless a
  genuine deterministic check fails;
- publishability/review-needed is `修改后可发布/否`; suggested translation is absent;
- terminal disposition occurs once, is last and matches structured outcome;
- verification is complete.

The normal five-section report must preserve the precision, partner-scope and
withdrawal-right errors without inventing statutes or legal advice.

## Case C — strict deterministic blocker plus semantic issue

```json
{
  "source_text": "I have read the Terms at {terms_url} and authorize ACME to process account data for this request only.",
  "candidate_translation": "我已阅读条款，并授权 ACME 处理所有账户数据。",
  "source_language": "en",
  "target_language": "zh-CN",
  "content_type": "legal_risk",
  "context": "账户数据处理授权确认页；{terms_url} 是运行时必须保留的条款链接，占位符不可删除；授权范围仅限当前请求。",
  "audience": "中国大陆普通软件用户",
  "mode": "strict",
  "output_mode": "review_only",
  "interactive_mode": "off",
  "briefing_mode": "off",
  "trace_level": "summary",
  "history_mode": "full",
  "technical_constraints": "必须逐字保留 {terms_url}，不得扩大授权的数据范围或用途范围。",
  "do_not_translate_literals": ["{terms_url}"],
  "hard_constraints": ["required_literal:{terms_url}"]
}
```

Required parsed JSON evidence:

- route/profile/reasons are exactly the legal-risk strict route and
  `content_legal_risk`, `mode_strict`, `deterministic_preflight_coverage`, `risk_strict`;
- ordered active roles are technical safety, fidelity, terminology, product context, UX
  copy, risk ambiguity and fluency using canonical IDs;
- seven samples succeed, coverage is `full`, unavailable is zero;
- sampling is between 7 and 18, budget is 18 and elicitation is zero;
- preflight is blocking, blocking counts are nonzero and the failed kind list records the
  missing required literal/placeholder check without raw prose;
- the authorization-scope expansion remains a separate substantive issue;
- publishability/review-needed is `需人工复核/是`; suggested translation is absent;
- terminal disposition occurs once, is last and matches structured outcome;
- verification is complete.

## Shared identity, privacy and return packet

Every normal review report must retain exactly five sections in order: 审校背景,
Council 新增视角, 角色覆盖与分工, 共识、分歧与盲区, 主编结论. It must not gain
verification metadata or a full replacement translation.

Every parsed canonical receipt must report record/serving package and module 0.12.1,
build v10.1, persisted Schema 2.5 and receipt Schema 1.0. Neither the human verification
receipt nor its JSON may expose source/candidate text, reviewer/evidence prose,
credentials, filesystem paths, environment values, suggested translation text or
internal issue IDs.

Return to the Foreman:

1. the one preparation `get_server_info` response;
2. A/B/C `review_id` values;
3. each original normal `review_translation` `display_report`;
4. each complete original verification primary text, including the canonical JSON block;
5. each parsed canonical JSON object unchanged;
6. wall-clock duration when Goose reports it;
7. every retry, provider error, missing field or deviation, using `none` explicitly.

Q-014 passes only after the Foreman reviews all three fresh records together. A failed or
unavailable reviewer is live evidence and must not be hidden by retry.
