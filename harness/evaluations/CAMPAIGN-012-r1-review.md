# Campaign Review: CAMPAIGN-012-r1

## Decision

`CHANGES_REQUESTED`

CAMPAIGN-012-r1 establishes the intended V0.12 receipt surface, release identifiers,
history-view integration and broad regression evidence, but the canonical receipt is not
yet safe for hostile persisted records. Independent Foreman counterexamples reproduced
one path disclosure, one unbounded-list retrieval failure and one false-positive terminal
coherence result. These defects violate F-054 and F-056 and prevent Campaign acceptance.

## Control

- Role: `FOREMAN`
- Harness mode: `STRICT_CAMPAIGN`
- Contract: `harness/contracts/CAMPAIGN-012-r1.md`
- Contract SHA-256:
  `E4E1CAAFB5E6E08729B5E726C5144793D3BE7E029699AA24984F37E97D587548`
- Baseline: `6544d41d308f9ed7ab253dac5a70a94581cd04d8`
- Worker final HEAD: `06b0e378adc99826c48cd9fc7cc4337d8bc25367`
- Worker report: `harness/reports/CAMPAIGN-012-r1-worker.md`
- Worker ledger: `harness/reports/CAMPAIGN-012-r1-ledger.md`
- Commits: `1b5de81`, `a712d1d`, `da4f9c4`, `340d70d`, `06b0e37`
- Scope: exactly 14 contract-authorized paths; Git index empty

## Preserved r1 evidence

- The baseline is an ancestor of final HEAD. Per-package commit scopes and the complete
  14-path diff match the r1 allowlist; `git diff --check` passes.
- Independent compile and complete regression pass: `334 passed in 4.18s`.
- Independent receipt/tool/release selection passes: `38 passed in 1.54s`.
- Independent executable Golden selection passes: `4 passed`; the Worker reports exact
  24/24 cases and all eight aggregate metrics at 1.0.
- The existing history tool exposes the additive `verification` view through matching
  primary and structured channels without a sixth public tool.
- Package/module/build are `0.12.0` / `0.12.0` /
  `verifiable-evidence-council-v10`; persisted Schema remains `2.5`, receipt Schema is
  `1.0`, budgets remain 6/13/18 and concurrency remains 3/3.
- The lock changes only the editable root version `0.11.1 -> 0.12.0` and preserves the
  Worker-reported revision/package/upload-time invariants 3/78/586.
- Worker artifact and isolated Python 3.12/FastMCP 3.4.7 evidence is preserved for r2
  comparison, but production receipt changes require fresh final artifacts.

## Independent blocking counterexamples

### 1. Unsafe parent review ID crosses both receipt channels

A valid full V2.5 model with `parent_review_id="C:/PRIVATE_PARENT_SENTINEL"` is accepted
by the compatibility/model layer. The receipt copies that string directly into
`record.parent_review_id`; `availability.redacted_fields` remains empty. The raw path
therefore survives canonical JSON and the Markdown renderer can expose it.

This violates the r1 privacy rule that path/prose-shaped values be null and explicitly
redacted. A parent ID is an identifier, not an arbitrary string: it must match a bounded
supported review-ID grammar before projection.

### 2. Duplicate active roles make verification retrieval unbounded

A syntactically valid record with 100 repeated `fidelity_reviewer` entries is normalized
to one routing role by `_safe_string_list`, but `_sample_projection` iterates the original
unduplicated list and creates 100 sample rows. Rendering then raises
`ValueError("verification report exceeds hard cap")`. `view_review_record` does not catch
that exception, so the read-only verification view fails instead of returning a bounded
receipt.

The active-role list and sample projection must share one validated bounded identity.
Duplicates, oversize lists, mismatched sample sets and invalid members must yield null
plus deterministic redaction; hostile persisted input must never make rendering exceed
the 3,200-code-point cap or raise from the public history tool.

### 3. Terminal coherence can be reported true when the last verdict conflicts

A report containing the structured expected disposition once followed by a different
terminal disposition produces:

```text
terminal_disposition_occurrences = 1
terminal_disposition_is_last_report_line = false
terminal_disposition_matches_structured = true
```

This is a false-positive dual-channel coherence result. Matching the structured chief
requires exactly one occurrence and that occurrence must be the final non-empty report
line. The projector remains descriptive and must not repair either channel.

## Additional primary-contract omission

The canonical `serving` object correctly carries package, module, build and schema, but
the five-section Markdown displays only package and build. The r1 primary contract says
record and serving versions are visible. r2 must add the current module and serving
Schema values without changing headings, canonical JSON or the 3,200 hard cap.

## Required r2 correction

1. Validate `parent_review_id` with a bounded supported review-ID grammar; unsafe values
   become null and add `record.parent_review_id` to `redacted_fields`.
2. Validate active roles once and reuse that exact ordered list for routing and sample
   projection. Reject duplicates, oversize lists, invalid roles and sample-set mismatch
   as null/redacted without leaking raw values.
3. Guarantee that every valid or hostile receipt renders deterministically within the
   hard cap and the public verification view does not propagate a renderer exception.
4. Define terminal coherence as exactly one structured disposition occurring at the
   final non-empty report line; preserve occurrence and last-line diagnostics.
5. Show serving package/module/build/schema in primary Markdown while preserving the
   exact five headings and all normal/full/summary behavior.
6. Keep V0.12 identifiers, receipt/persisted schemas, tool count, routing, sampling,
   persistence, adjudication and every accepted r1 product invariant unchanged.

F-053 through F-057 and Q-014 remain unaccepted. CAMPAIGN-012-r2 is the bounded
correction contract.
