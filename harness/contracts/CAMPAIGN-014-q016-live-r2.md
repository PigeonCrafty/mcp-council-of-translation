# External Gate Revision: CAMPAIGN-014 Q-016-r2

## Control

- Gate: `Q-016-r2 / Replacement normal-Goose truncation evidence`
- Role: `USER-OPERATED NORMAL GOOSE; FOREMAN ACCEPTANCE`
- State: `ISSUED`
- Current protected `main`: `d595daf54eea141451fe3a1db4c7f45764fa980e`
- Published product commit: `9d8f1f987efe73946377883e6ad3a681abe11989`
- Package/module: `0.13.1`
- Diagnostic build: `truthful-boundaries-council-v11.1`
- Review/receipt schemas: `2.6/1.1`
- Parent contract: `harness/contracts/CAMPAIGN-014-q016-live.md`
- Parent contract SHA-256:
  `CE7BE423518D976D6C63417CDC4A93E097EEFAD0BABDB4054C4BA5AB146F92F6`
- Parent live review: `harness/evaluations/CAMPAIGN-014-q016-live-review.md`
- Parent live review SHA-256:
  `E5904C0708EA3EDC6F186DF2499A6189DDF8C9D99613C23809180117CB370449`
- Acceptance authority: Foreman only

## Frozen carry-forward evidence

The r1 admission and the following two records are accepted and immutable for Q-016:

- Case B: `20260828T024458690799Z_8badddd7158f`
- Case C: `20260828T024543336644Z_2422acf98836`

Do not call `get_server_info` again. Do not rerun, continue or replace B or C. A rerun of
B/C is a protocol deviation and does not supersede the accepted records.

The r1 Case A record `20260828T024323225222Z_918a4a44c6af` is retained as negative client
evidence but is not truncation acceptance evidence. This revision authorizes exactly one
replacement record, Case A2.

The parent contract's independent AUD-001 through AUD-007 repository re-audit remains
unchanged and outstanding. Passing A2 completes only the normal-Goose portion of Q-016;
it does not by itself accept Q-016 or lift the feature-expansion block.

## Runtime boundary

Use the existing unchanged Goose extension, provider, model and account. Start one fresh
Goose conversation. Do not modify extension commands or environment variables. Call
`review_translation` exactly once, `view_review_record(full)` exactly once and
`view_review_record(verification)` exactly once. Do not call `get_server_info`,
`continue_review`, any B/C record, or retry A2.

## Case A2 — identical over-limit inputs

Construct one literal string containing exactly 16,000 uppercase ASCII `S` characters.
Use that same complete literal string as both `source_text` and
`candidate_translation`. The MCP arguments must contain the actual characters, not a
repetition expression, variable, ellipsis, summary or attachment reference.

If Goose cannot guarantee that both actual arguments contain more than 12,000 characters,
stop before calling `review_translation` and report `CLIENT_LIMIT`. Do not silently send
a shorter value.

Use these parameters:

```json
{
  "source_text": "<the complete literal 16,000-character S string>",
  "candidate_translation": "<the exact same complete literal 16,000-character S string>",
  "source_language": "en",
  "target_language": "en",
  "content_type": "ui",
  "context": "Q-016-r2 synthetic input-completeness fixture. Source and candidate are intentionally identical and carry no user-facing semantic distinction; this case only verifies fail-closed behavior when both inputs exceed the review boundary.",
  "audience": "localization QA engineers",
  "mode": "lightweight",
  "output_mode": "review_only",
  "interactive_mode": "off",
  "briefing_mode": "off",
  "trace_level": "summary",
  "history_mode": "full",
  "project_rules": "Treat the two identical synthetic strings as equivalent. Do not request product context or propose wording changes; report only evidence supported by the supplied record."
}
```

After the review returns:

1. Preserve the returned `review_id` and complete original five-section report.
2. Call `view_review_record(review_id, detail_level="full")` exactly once.
3. Call `view_review_record(review_id, detail_level="verification")` exactly once.
4. Preserve the complete verification primary text.
5. Parse and reproduce unchanged the JSON immediately after the literal label
   `Canonical verification_receipt JSON:`.
6. For fields not exposed by the client, write `not exposed by client`; never reconstruct
   them from prose.
7. Report actual duration and every retry, provider error, missing field or deviation,
   using `none` explicitly.

## A2 acceptance

All of the following are required:

- the primary report explicitly contains both `仅审校了有界前缀` and
  `不构成全文发布许可`;
- the outcome is `NEEDS_HUMAN_REVIEW`, degraded true, `需人工复核 / 是`, with no
  suggested translation;
- decision support is `insufficient` and coherent with the chief disposition;
- canonical receipt `fallback_reason_code` is `input_truncated`, not empty, null,
  redacted or replaced by a non-truncation fallback;
- verification is complete with zero missing and zero redacted fields;
- full or compact structured content, when exposed, records both
  `source_input_truncated` and `candidate_input_truncated` warnings;
- input diagnostics, when exposed, show both original lengths greater than `12000`, both
  reviewed lengths no greater than `12000`, and both truncated flags true;
- reviewer execution remains full and successful, sampling stays within lightweight
  budget 6, and elicitation is zero;
- there is exactly one terminal disposition at the last report line and it matches the
  structured result.

If any reviewer is unavailable, any additional fallback makes the truncation code
ambiguous/redacted, or the primary bounded-prefix warning is absent, preserve that result
without retry and report A2 as a deviation.

## Return packet

Return only:

1. A2 `review_id`;
2. complete original `display_report`;
3. full-view input diagnostics, warnings, status, degradation, fallback, decision support
   and chief disposition when exposed;
4. complete verification primary text and unchanged canonical JSON;
5. the A2 acceptance checklist; and
6. duration plus retry/provider-error/missing-field/deviation accounting.

Do not repeat r1 admission, B or C output. Refer to their frozen review IDs only.
