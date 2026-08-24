# Live Gate Contract: CAMPAIGN-012 Q-014

## Control

- Gate: `Q-014 / Normal-Goose canonical verification receipt evidence`
- Role: `USER-OPERATED NORMAL GOOSE; FOREMAN ACCEPTANCE`
- State: `ISSUED`
- Published protected `main`: `6c4366f7a43135388d0cf68655a6a3638d6bbe1b`
- Published implementation mapping: `213cce55bb21d6854f76e89bee33a4e9e2f9dd8c`
- Required package/module: `0.12.0`
- Required diagnostic build: `verifiable-evidence-council-v10`
- Required persisted schema: `2.5`
- Required verification receipt schema: `1.0`
- Public tools: exactly five
- Sampling budgets: `6/13/18`
- Default independent-review concurrency: `3`
- Live cases: exactly A, B and C below, each in a fresh Goose conversation
- Acceptance authority: Foreman only

## Runtime boundary

Use the existing normal Goose Desktop extension unchanged:

```text
uvx --refresh --from git+https://github.com/PigeonCrafty/mcp-council-of-translation mcp_council_of_translation
```

Do not add a commit suffix, change extension environment variables, point at a local
checkout or change Goose/provider/model settings between cases. Restart Goose once after
publication so `uvx --refresh` resolves current `main`. Use the same provider, model and
account for all three cases.

Before Case A, call `get_server_info` exactly once. Stop without running any case unless
it reports package/module `0.12.0`, build `verifiable-evidence-council-v10`, persisted
schema `2.5`, verification receipt schema `1.0`, detail levels
`full/summary/verification`, budgets 6/13/18, concurrency limit/max 3 and exactly five
public tools.

For every case:

- start a fresh Goose conversation;
- call `review_translation` exactly once with the exact parameters below;
- retain its original five-section `display_report` and returned `review_id`;
- call `view_review_record(review_id, detail_level="verification")` exactly once;
- do not call `continue_review`, request `full`, retry, or ask another model to
  reconstruct missing data;
- print the verification tool's original primary `display_report` verbatim;
- print the complete structured `verification_receipt` as JSON with canonical field
  names and values unchanged;
- if a field is unavailable, print its actual `null` plus the corresponding availability
  entry; never infer, translate or rename it;
- if no `review_id` is returned, stop that case and report the literal failure.

The structured `verification_receipt` is the evidence authority. Goose commentary and
the normal Council report are not substitutes for canonical receipt fields.

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

Required receipt evidence:

- `routing.profile` is exactly `route_legal_risk_lightweight_v1`;
- `routing.reason_codes` is exactly
  `content_legal_risk, mode_lightweight, deterministic_preflight_coverage, risk_focused`;
- ordered `routing.active_role_ids` is exactly `fidelity_reviewer`,
  `terminology_reviewer`, `risk_ambiguity_reviewer`, `fluency_reviewer`;
- all four `reviewer_execution.samples[].sample_status` values are
  `structured_success`, coverage is `full`, successes/unavailable are 4/0;
- `runtime.sampling_calls_total` is 4, `sample_budget_total` is 6 and
  `elicitation_calls_total` is 0;
- no deterministic blocker, degradation, warning or fallback is fabricated;
- `outcome.publishability/review_needed` is exactly `可发布/否`, and
  `suggested_translation_present` is false;
- terminal disposition occurs exactly once, is last and matches structured output;
- `availability.verification_complete` is true with empty not-recorded/redacted lists.

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

Required receipt evidence:

- `routing.profile` is exactly `route_legal_risk_standard_v1`;
- `routing.reason_codes` is exactly
  `content_legal_risk, mode_standard, deterministic_preflight_coverage, risk_panorama`;
- ordered active roles are exactly fidelity, terminology, product context, UX copy,
  risk ambiguity and fluency using their canonical IDs;
- six independent samples succeed with full coverage and zero unavailable reviewers;
- `runtime.sampling_calls_total` is between 6 and 13,
  `sample_budget_total` is exactly 13 and `elicitation_calls_total` is 0;
- issue counts are nonzero, while `preflight.blocking` remains false unless a genuine
  deterministic check fails;
- `outcome.publishability/review_needed` is exactly `修改后可发布/否`, and
  `suggested_translation_present` is false;
- terminal disposition occurs exactly once, is last and matches structured output;
- `availability.verification_complete` is true.

The normal five-section report must still visibly preserve precision, partner-scope and
withdrawal-right errors without statutes or legal advice.

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

Required receipt evidence:

- `routing.profile` is exactly `route_legal_risk_strict_v1`;
- `routing.reason_codes` is exactly
  `content_legal_risk, mode_strict, deterministic_preflight_coverage, risk_strict`;
- ordered active roles are exactly technical safety, fidelity, terminology, product
  context, UX copy, risk ambiguity and fluency using their canonical IDs;
- seven independent samples succeed with full coverage and zero unavailable reviewers;
- `runtime.sampling_calls_total` is between 7 and 18,
  `sample_budget_total` is exactly 18 and `elicitation_calls_total` is 0;
- `preflight.blocking` is true, blocking check counts are nonzero, and the bounded failed
  kind list records the missing required literal/placeholder check without raw prose;
- issue counts retain a separate semantic authorization-scope issue;
- `outcome.publishability/review_needed` is exactly `需人工复核/是`, and
  `suggested_translation_present` is false;
- terminal disposition occurs exactly once, is last and matches structured output;
- `availability.verification_complete` is true.

## Shared presentation, identity and privacy requirements

Every normal `review_translation` report must retain exactly five sections in order:
审校背景, Council 新增视角, 角色覆盖与分工, 共识、分歧与盲区, 主编结论. It must not
gain verification metadata or a full replacement translation.

Every verification response must contain exactly `review_id`, `display_report` and
`verification_receipt`. The receipt must use the canonical top-level order and names:
`receipt_schema_version`, `review_id`, `record`, `serving`, `routing`,
`reviewer_execution`, `runtime`, `preflight`, `issues`, `outcome`, `coherence`,
`availability`. Record and serving versions must be 0.12.0/build v10/Schema 2.5 as
applicable, and receipt schema must be 1.0.

Neither receipt channel may contain source text, candidate translation, reviewer prose,
evidence prose, suggested-translation text, credentials, filesystem paths, environment
values or internal issue IDs. The verification primary Markdown must contain exactly
five receipt sections in order: Council 验证回执 title, 记录与路由, 覆盖与调用,
风险与裁决, 一致性与可用性.

Return to the Foreman:

1. the preparation `get_server_info` response;
2. A/B/C `review_id` values;
3. each original normal `review_translation` `display_report`;
4. each original verification `display_report`;
5. each complete canonical `verification_receipt` JSON object;
6. wall-clock duration when Goose reports it;
7. every retry, provider error, missing field or deviation, using `none` explicitly.

Q-014 passes only after the Foreman reviews all three fresh records together. A failed
or unavailable reviewer is live evidence and must not be hidden by retry.
