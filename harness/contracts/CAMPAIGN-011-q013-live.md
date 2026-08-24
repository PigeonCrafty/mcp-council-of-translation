# Live Gate Contract: CAMPAIGN-011 Q-013

## Control

- Gate: `Q-013 / Risk-sensitive panoramic routing live evidence`
- Role: `USER-OPERATED NORMAL GOOSE; FOREMAN ACCEPTANCE`
- State: `ISSUED`
- Published protected `main`: `938c3a4bb9f14c7688286b25eabd8aff9f18a09d`
- Published implementation mapping: `7f7d050ad7cd5ef931b38eafd11f988619afced1`
- Required package/module: `0.11.0`
- Required diagnostic build: `risk-coherent-council-v9`
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

Do not add a commit suffix, do not change extension environment variables, do not point
at a local checkout and do not modify Goose/provider/model settings between cases. Restart
Goose once after publication so `uvx --refresh` resolves current `main`. Use one provider,
model and account for all three cases.

Before Case A, call `get_server_info` exactly once. Stop without running any case unless it
reports package/module `0.11.0`, build `risk-coherent-council-v9`, schema `2.5`, budgets
6/13/18, concurrency limit/max 3 and the exact five tools. Normal case calls then use
`review_translation` directly.

For every case:

- call `review_translation` exactly once with the exact parameters below;
- call `view_review_record(review_id, detail_level="full")` exactly once after success;
- do not call `continue_review`, do not retry and do not ask another model to reinterpret
  missing structured fields;
- preserve the original primary `display_report` and the exact structured fields requested;
- if no `review_id` is returned, stop that case and report the literal failure.

## Case A — standard panoramic risk review

Call `review_translation` with:

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
- exact ordered roles: fidelity, terminology, product context, UX copy, risk ambiguity,
  fluency;
- exact reason codes: legal-risk content, standard mode, deterministic preflight coverage,
  risk panorama;
- six successful independent reviewers, full coverage, total sampling between 6 and 13,
  zero elicitation, no degradation/fallback;
- the primary report identifies the material precision, partner-scope and withdrawal-right
  reversals without inventing statutes or giving legal advice;
- it must not give an unqualified clean-release conclusion.

## Case B — lightweight clean control

Call `review_translation` with:

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
- exact ordered roles: fidelity, terminology, risk ambiguity, fluency;
- exact reason codes: legal-risk content, lightweight mode, deterministic preflight
  coverage, focused risk;
- four successful independent reviewers, full coverage, exactly four sampling calls,
  zero elicitation, no degradation/fallback;
- no fabricated blocker, statute or legal advice; a clean/publishable result is allowed;
- concise five-section primary report with all four roles accounted for.

## Case C — strict technical and scope blocker

Call `review_translation` with:

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
- exact ordered roles: technical safety, fidelity, terminology, product context, UX copy,
  risk ambiguity, fluency;
- exact reason codes: legal-risk content, strict mode, deterministic preflight coverage,
  strict risk;
- seven successful independent reviewers, full coverage, total sampling between 7 and 18,
  zero elicitation, no degradation/fallback;
- `{terms_url}` loss is a deterministic blocker and the expansion from “this request only”
  to “all account data” remains a distinct material scope issue;
- final disposition requires correction/human review and `suggested_translation` remains
  null/absent under review-only.

## Shared presentation and privacy acceptance

Every case must return exactly the five primary sections in order: 审校背景, Council
新增视角, 角色覆盖与分工, 共识、分歧与盲区, 主编结论. The chief disposition is last.
No internal route/profile/reason/role/issue/cluster/position/decision/option/gap ID may
appear in primary Markdown. Structured full history must retain routing provenance,
reviewer evidence and runtime counts. No case may emit a full replacement translation.

## Evidence handoff

Return to the Foreman:

1. the preparation `get_server_info` response;
2. A/B/C `review_id` values;
3. each original `display_report`;
4. for each case, exact `council_plan.routing_profile`, `routing_reason_codes`,
   `active_role_ids`, every independent review `agent_name`/`sample_status`,
   `reviewer_coverage`, `reviewer_samples_successful`, `reviewer_samples_unavailable`,
   `sampling_calls`, `sample_budget`, `elicitation_calls`, `status`, `degraded`, `warnings`,
   `fallback_reason`, chief publishability/review-needed, and suggested-translation state;
5. actual wall-clock duration reported by Goose for each review when available;
6. any retry, provider error, missing field or deviation. `none` must be stated explicitly.

Q-013 passes only after Foreman reviews all three admissible records together. A failure or
unavailable reviewer is evidence about live behavior and must not be hidden by an automatic
retry.
