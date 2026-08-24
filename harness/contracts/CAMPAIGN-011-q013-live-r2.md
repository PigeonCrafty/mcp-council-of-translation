# Live Gate Contract: CAMPAIGN-011 Q-013-r2

## Control

- Gate: `Q-013 / Risk-sensitive panoramic routing final live revalidation`
- Role: `USER-OPERATED NORMAL GOOSE; FOREMAN ACCEPTANCE`
- State: `ISSUED`
- Published protected `main`: `f64d86fd37a0727d3a0a3ebcd8581fd26cc7e1a3`
- Published implementation mapping: `6d3a5b6843550ec37ae61ce2670de51a93580bf8`
- Required package/module: `0.11.1`
- Required diagnostic build: `risk-coherent-council-v9.1`
- Required schema: `2.5`
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

Before Case A, call `get_server_info` exactly once. Stop without running any case unless it
reports package/module `0.11.1`, build `risk-coherent-council-v9.1`, schema `2.5`, budgets
6/13/18, concurrency limit/max 3 and exactly five public tools.

For every case:

- start a fresh Goose conversation;
- call `review_translation` exactly once with the exact parameters below;
- after success, call `view_review_record(review_id, detail_level="full")` exactly once;
- do not call `continue_review`, retry, or ask another model to reconstruct missing data;
- return the original `display_report`, `review_id` and any exact structured fields that
  Goose actually exposes;
- if a field is unavailable, state `未返回`; never infer or invent it;
- if no `review_id` is returned, stop that case and report the literal failure.

The persisted full record is the evidence authority when Goose narrative and structured
content disagree. Goose commentary is not accepted as a substitute for record fields.

## Case A — standard panoramic risk review and repaired disposition

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

Required evidence:

- routing profile `route_legal_risk_standard_v1`;
- ordered roles: fidelity, terminology, product context, UX copy, risk ambiguity,
  fluency;
- reason codes: legal-risk content, standard mode, deterministic preflight coverage,
  risk panorama;
- six successful independent reviewers, full coverage, 6..13 sampling calls, zero
  elicitation, no degradation/fallback;
- material precision, partner-scope and withdrawal-right errors remain visible without
  statutes or legal advice;
- structured chief is exactly `修改后可发布 / 否`;
- the primary terminal is exactly `最终处置：修改后可发布；需人工复核：否`, appears once
  and is the final `display_report` line;
- `suggested_translation` remains null/absent.

## Case B — lightweight clean control

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

Required evidence:

- routing profile `route_legal_risk_lightweight_v1`;
- ordered roles: fidelity, terminology, risk ambiguity, fluency;
- reason codes: legal-risk content, lightweight mode, deterministic preflight coverage,
  focused risk;
- four successful independent reviewers, full coverage, exactly four sampling calls,
  zero elicitation, no degradation/fallback;
- no fabricated blocker, statute or legal advice;
- structured chief is exactly `可发布 / 否` and the primary report ends exactly once with
  `最终处置：可发布；需人工复核：否`;
- `suggested_translation` remains null/absent.

## Case C — strict technical and scope blocker

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

Required evidence:

- routing profile `route_legal_risk_strict_v1`;
- ordered roles: technical safety, fidelity, terminology, product context, UX copy, risk
  ambiguity, fluency;
- reason codes: legal-risk content, strict mode, deterministic preflight coverage, strict
  risk;
- seven successful independent reviewers, full coverage, 7..18 sampling calls, zero
  elicitation, no degradation/fallback;
- `{terms_url}` loss remains a deterministic blocker and authorization-scope expansion
  remains a distinct material issue;
- structured chief is exactly `需人工复核 / 是` and the primary report ends exactly once
  with `最终处置：需人工复核；需人工复核：是`;
- `suggested_translation` remains null/absent.

## Shared presentation and evidence handoff

Every primary report must contain exactly five sections in order: 审校背景, Council
新增视角, 角色覆盖与分工, 共识、分歧与盲区, 主编结论. No internal route/profile/
reason/role/issue/cluster/position/decision/option/gap ID may appear in primary Markdown.
Full history must retain routing provenance, evidence and runtime counts. No case may emit
a full replacement translation.

Return to the Foreman:

1. the preparation `get_server_info` response;
2. A/B/C `review_id` values;
3. each original `display_report`;
4. exact structured routing, role/sample, coverage, call/budget, status/degradation,
   chief disposition and suggested-translation fields when actually exposed;
5. wall-clock duration when Goose reports it;
6. every retry, provider error, missing field or deviation, using `none` explicitly.

Q-013 passes only after the Foreman reviews all three fresh records together. A failed or
unavailable reviewer is live evidence and must not be hidden by retry.
