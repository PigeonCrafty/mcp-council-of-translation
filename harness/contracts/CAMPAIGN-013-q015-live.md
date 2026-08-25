# Live Gate Contract: CAMPAIGN-013 Q-015

## Control

- Gate: `Q-015 / Normal-Goose calibrated decision-support evidence`
- Role: `USER-OPERATED NORMAL GOOSE; FOREMAN ACCEPTANCE`
- State: `ISSUED`
- Published protected `main`: `95d90cf383d045778ce61afaa50dbcec199579ce`
- Accepted implementation: `4f976c2764a463dceb403084fa3faead5300211e`
- Publication PR: `#31`; PR and post-merge six-job CI: passed
- Required package/module: `0.13.0`
- Required diagnostic build: `calibrated-evidence-council-v11`
- Required persisted Review Schema: `2.6`
- Required verification receipt Schema: `1.1`
- Public tools: exactly five
- Sampling budgets: `6/13/18`
- Default independent-review concurrency: `3`
- Cases: exactly A, B and C below, each in a fresh Goose conversation
- Acceptance authority: Foreman only

## Runtime boundary and admission

Keep the existing Goose Desktop extension command unchanged:

```text
uvx --refresh --from git+https://github.com/PigeonCrafty/mcp-council-of-translation mcp_council_of_translation
```

Do not add a commit suffix, change extension environment variables, point at a local
checkout, or change Goose/provider/model/account between cases. Restart Goose once before
admission so `uvx --refresh` resolves current protected `main`.

Before Case A, call `get_server_info` exactly once. Stop without running any case unless
it reports package/module `0.13.0`, build `calibrated-evidence-council-v11`, persisted
Schema `2.6`, verification receipt Schema `1.1`, detail levels
`full/summary/verification`, budgets 6/13/18, concurrency limit/max 3 and exactly five
public tools.

For every case:

1. Start a fresh Goose conversation.
2. Call `review_translation` exactly once with the exact parameters below.
3. Preserve the complete original five-section `display_report`, its structured
   `decision_support` object when exposed, and the returned `review_id`.
4. Call `view_review_record(review_id, detail_level="full")` exactly once and preserve
   the recorded `decision_support` object when the client exposes structured content.
5. Call `view_review_record(review_id, detail_level="verification")` exactly once.
6. Do not call `continue_review`, retry, or ask a model to reconstruct a missing field.
7. Print the complete original verification primary text verbatim.
8. Locate the literal label `Canonical verification_receipt JSON:`. Immediately after it
   there must be exactly one fenced `json` block and nothing after that fence. Parse and
   print that JSON unchanged. If the label/block is absent or parsing fails, stop the case
   and report the literal failure.

The parsed canonical JSON is the evidence authority. Its exact top-level key order is:
`receipt_schema_version`, `review_id`, `record`, `serving`, `routing`,
`reviewer_execution`, `runtime`, `preflight`, `issues`, `outcome`, `decision_support`,
`coherence`, `availability`.

For all three cases, `decision_support` must contain exactly:
`level`, `support_target`, `basis_codes`, `limitation_codes`, `assessment_basis`,
`outcome_coherent`. `support_target` must be `chief_disposition`, `assessment_basis` must
be `deterministic_structured_trace_v1`, and `outcome_coherent` must be `true`.

The normal report must keep exactly five sections in order: 审校背景, Council 新增视角,
角色覆盖与分工, 共识、分歧与盲区, 主编结论. It must contain exactly one natural
`结论依据` line before exactly one last-line `最终处置`, and must not expose raw support
codes or a full replacement translation.

## Case A — clean, well-supported disposition

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

- legal-risk lightweight route with four ordered active roles and four
  `structured_success` samples; coverage/successful/unavailable is `full/4/0`;
- sampling/budget/elicitation is exactly `4/6/0`;
- no blocker, issue, degradation, warning or fallback;
- outcome is `COMPLETED`, `可发布 / 否`, with no suggested translation;
- decision support is `well_supported`; basis codes contain
  `full_reviewer_coverage` and `clean_confirmation`; limitation codes are empty;
- normal report says `结论依据：充分` and explicitly avoids implying that the translation
  is necessarily correct;
- verification is complete with no missing or redacted fields.

## Case B — material edits, supported with limits

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

- legal-risk standard route with six ordered active roles and six successful samples;
  coverage is full and unavailable is zero;
- sampling is between 6 and 13, budget is 13 and elicitation is zero;
- preflight remains nonblocking, issue count is nonzero, and the report preserves the
  precision, selected-partner scope and withdrawal-right reversal without inventing law;
- outcome is `COMPLETED`, `修改后可发布 / 否`, with no suggested translation;
- decision support is `supported_with_limits`; basis codes include
  `full_reviewer_coverage` and `structured_material_evidence`; limitation codes retain
  every applicable bounded limit, including `material_disagreement` when recorded;
- normal report says `结论依据：有限制`;
- verification is complete with no missing or redacted fields.

## Case C — unresolved material context, insufficient evidence

```json
{
  "source_text": "This notice applies to users in the covered region.",
  "candidate_translation": "本通知适用于涵盖地区的用户。",
  "source_language": "en",
  "target_language": "zh-CN",
  "content_type": "legal_risk",
  "context": "合规通知；调用方尚未提供 covered region 指向的国家、地区、司法辖区或适用项目规则，不同范围会改变风险措辞判断。",
  "audience": "中国大陆普通软件用户",
  "mode": "standard",
  "output_mode": "review_only",
  "interactive_mode": "off",
  "briefing_mode": "off",
  "trace_level": "summary",
  "history_mode": "full",
  "project_rules": "必须先确认 covered region 的适用范围后才能作发布裁决；当前没有提供该范围。"
}
```

Required evidence:

- legal-risk standard route, full successful reviewer coverage, budget 13 and no actual
  elicitation because interaction is off;
- at least one selected material context gap remains unanswered; the record must not
  pretend that a user supplied an answer;
- outcome is `NEEDS_HUMAN_REVIEW`, `需人工复核 / 是`, with no suggested translation;
- decision support is `insufficient`; limitation codes include
  `unresolved_material_context`; basis codes remain bounded structured facts only;
- normal report says `结论依据：不足` and that current evidence only supports transfer to
  human review;
- verification is complete with no missing or redacted fields.

If the live provider does not produce a material context gap, report the exact observed
record as a Q-015 deviation; do not retry or manually fabricate one.

## Identity, privacy and return packet

Every canonical receipt must report record/serving package/module 0.13.0, build
`calibrated-evidence-council-v11`, record Schema 2.6 and receipt Schema 1.1. Neither
verification text nor JSON may expose source/candidate text, reviewer/evidence prose,
credentials, filesystem paths, environment values, suggested translation text or
internal issue IDs. Combined verification text must remain within its 12,000-code-point
cap.

Return to the Foreman:

1. the one admission `get_server_info` response;
2. A/B/C `review_id` values;
3. each complete original normal `display_report`;
4. each recorded full-view `decision_support` object when exposed, otherwise literal
   `not exposed by client`;
5. each complete verification primary text and parsed canonical JSON object unchanged;
6. wall-clock duration when available; and
7. every retry, provider error, missing field or deviation, using `none` explicitly.

Q-015 passes only after the Foreman reviews all three fresh records together. A failed or
unavailable reviewer, missing context gap or client-channel limitation is evidence and
must not be hidden by retry.
