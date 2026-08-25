# V0.13 Independent Audit — Foreman Response

## Disposition

Foreman accepts the audit's top-level decision:

```text
BLOCK NEXT FEATURE CAMPAIGN
PROCEED ONLY WITH A NARROW AUDIT-REMEDIATION CAMPAIGN
```

The block applies to new product expansion, not to the established V0.13 architecture
as a whole. The remediation plan preserves the five-tool review-only surface, role
authority boundaries, Policy Gate, bounded user authority, evidence provenance,
budgets, routing portfolios and current Review/Receipt schemas.

Audit source:
`mcp-council-of-translation-v0.13-independent-audit.md`

Audited product baseline:
`95d90cf383d045778ce61afaa50dbcec199579ce`

Audited governance baseline:
`bcdb0e2bc282e907e975b43882906872913f6bec`

## Finding-by-finding decision

| Finding | Foreman decision | Planning action |
|---|---|---|
| AUD-001 | Fully accepted; High and campaign-blocking | F-064: incomplete-input reviews fail closed and visibly require human review |
| AUD-002 | Fully accepted; Medium | F-065: raise deterministic token precision and add a negative corpus without weakening valid protected tokens |
| AUD-003 | Fully accepted; Medium | F-066: validate the entire discussion envelope and degrade safely while preserving Round 1 evidence |
| AUD-004 | Fully accepted; Medium | F-067: recompute post-discussion role consensus and keep user-choice usefulness as a separate concept |
| AUD-005 | Fully accepted; Medium | F-068: add a bounded privacy-safe V1 summary projection |
| AUD-006 | Accepted with scope calibration | F-069: rename or version overclaimed metrics and define an independently curated blind-set contract; this is an evidence defect, not a runtime adjudication defect |
| AUD-007 | Partially accepted | F-070: freeze a tested compatibility policy after checking Goose constraints; do not blindly remove the validated FastMCP 2.x floor |
| Discussion semantics | Clarification accepted; current documentation checked | Explicitly document the phase as one sampled, simulated cross-role deliberation; no architecture change in this remediation |

## Independent Foreman evidence

The decisions above are not based only on the audit narrative. Foreman independently
inspected and exercised the implicated paths:

| Finding | Repository evidence | Independent result |
|---|---|---|
| AUD-001 | `tools/review.py:38,86,128-131`; truncation diagnostics are not consumed as a downstream safety condition | A long source/candidate pair was recorded as truncated while six clean envelopes still produced `COMPLETED`, no warnings and `可发布 / 否` |
| AUD-002 | `localization/preflight.py:14,17,134,138` | `100% safe`, `50% discount`, `25% off` and URLs followed by localized punctuation reproduced deterministic parity blockers |
| AUD-003 | `localization/orchestration.py:1121-1124`; `localization/deliberation.py:87` | `turns` as a string, scalar list or null raised instead of becoming bounded unavailable discussion evidence |
| AUD-004 | `localization/deliberation.py:111`; digest and decision-support consumers read `consensus_status` | Converged final positions incremented resolved-discussion value while the cluster stayed `disputed` and retained `needs_user_input=true` |
| AUD-005 | `tools/review.py:282-296` special-cases only V2 summary | A synthetic V1 summary response exposed task, reviews, conflict reviews and the full chief object |
| AUD-006 | `src/council_of_translation/evaluation.py:271-272,394-413` | The predicates match the audit description: critical presence is not identity recall, and non-clean cases do not test false-positive absence |
| AUD-007 | `pyproject.toml:7`, `uv.lock:411-413`, `docs/v0.13-stage-development-report.md:170,204-216,221-225`; CI run `32815713433` | The range is open-ended, but tested evidence includes both the locked 2.13.0.2 floor and isolated 3.4.7 behavior |

These were bounded diagnostic probes. They did not modify production code, persisted
records, protected evidence or external systems.

## Accepted findings

### AUD-001 — incomplete input can receive a complete disposition

The finding is confirmed. The public boundary caps source and candidate fields, records
the truncation, and passes only the bounded strings downstream. That known omission is
not currently converted into a safety constraint. A clean reviewed prefix can therefore
produce `COMPLETED` and a permissive chief disposition for a larger caller input that was
not completely reviewed.

The chosen remediation is fail-closed rather than immediate rejection:

- retain bounded-prefix review evidence as useful but explicitly incomplete;
- set degraded execution and stable source/candidate truncation codes;
- classify decision support as `insufficient`;
- force `NEEDS_HUMAN_REVIEW` and `需人工复核 / 是`;
- make the incomplete coverage visible in the primary report, compact response and
  verification receipt.

Long-document chunking, overlap and cross-chunk synthesis are explicitly out of scope.

### AUD-002 — deterministic preflight false positives

The finding is confirmed. The printf scanner can treat ordinary prose such as
`100% safe`, `50% discount` and `25% off` as protected printf tokens, while URL matching
can absorb sentence punctuation. Because deterministic checks have blocking authority,
precision must be improved before any new heuristic coverage is added.

The repair must preserve legitimate cases including `%2$s`, `%d`, `%.2f`, `{name}`,
`${APP}`, `/help` and `--force`.

### AUD-003 — malformed discussion escapes safe degradation

The finding is confirmed. Structurally invalid but JSON-valid `turns` values can reach
code that assumes mappings and can raise instead of producing a conservative trace.

The preferred policy is whole-envelope rejection: an invalid discussion payload becomes
unavailable, the pre-discussion Position Matrix remains authoritative, no blocker or
position change is manufactured, and bounded degradation/warning/phase provenance is
persisted. This also keeps malformed-output policy simple and auditable.

### AUD-004 — stale consensus after discussion

The finding is confirmed. Discussion can converge role positions while the cluster
retains its pre-discussion `disputed` status. That can contradict value metrics, digest,
minority reporting and decision-support limitations.

The fix must separate two facts:

- role consensus: whether material participating roles now agree;
- user-choice usefulness: whether more than one Policy-valid wording remains available
  for a legitimate preference decision.

Post-discussion consumers must use the recomputed role-consensus truth. A DecisionPoint
may remain only for the second reason, never because stale disagreement survived.

### AUD-005 — V1 summary is not minimized

The finding is confirmed. `detail_level="summary"` has a compact V2 projection but a V1
record falls through to the full legacy dump. A bounded V1 summary will retain only
identity/status/disposition metadata and omit task text, reviewer prose, conflict prose
and full rationale. Existing V1 full retrieval and privacy-safe verification behavior
remain compatible.

## Accepted with qualifications

### AUD-006 — Golden metric semantics

The audit is correct that `critical_issue_recalled` currently proves the presence of a
critical/blocking cluster, not identity-level recall of the intended defect. It is also
correct that `false_positive_free` only has substantive clean-case meaning in the
current evaluator.

Foreman classifies this as an evaluation-contract and naming defect, not a production
review/adjudication defect. The current Golden Corpus still provides useful production-
path regression evidence, but its metric labels must not imply blind quality validity.

The remediation will:

1. version or rename the current metrics to match exactly what they measure;
2. preserve the existing deterministic production-path corpus as regression evidence;
3. define a separate blind-set schema with expected issue family, bounded anchors,
   severity range, allowed alternatives and forbidden findings;
4. require independent curation/evaluation before claiming defect-identity recall or
   broad false-positive performance.

Increasing the same handcrafted corpus from 30 to a larger number is not an acceptable
substitute for independent blind evidence.

### AUD-007 — FastMCP range

The compatibility risk is real: `fastmcp>=2.13.0.2` has no upper bound, so future major
versions are declared compatible without automatic evidence.

One evidence calibration is useful. The audit correctly says the declared range is
broader than the validated range; the repository records these two tested points:

- the canonical lock resolves FastMCP `2.13.0.2` and the protected CI matrix validates
  it on Windows/Ubuntu with Python 3.10, 3.12 and 3.13;
- the V0.13 isolated wheel smoke additionally validated FastMCP `3.4.7` on CPython
  3.12.9.

Therefore Foreman does not accept a blind change to `fastmcp>=3,<4`, because it would
discard a tested 2.x floor and could break Goose environments unnecessarily. F-070 will
first establish the supported client/runtime policy, then either add a justified upper
bound or a minimum/current/latest-compatible CI matrix.

## Targeted Discussion terminology

The proposed phrase **single-sample simulated cross-role deliberation** is accepted as
the clearest product description. Round 2 must not be described as independent agents
replying to one another, and its evidence must not inherit Round 1 independence.

The audit makes this warning conditionally and does not assert that current authoritative
documentation already makes the stronger claim. Foreman checked `README.md:43`,
`docs/v0.4-architecture.md:18,38` and
`docs/v0.13-stage-development-report.md:105,114`; they already specify at most one
discussion call/round and state that only independent reviewer sampling is concurrent.
No conflicting claim was found. The planned change is therefore an affirmative
terminology clarification, not an architecture correction.

## Remediation boundary

The next contract may include only F-064 through F-070 and release/evidence work needed
for them. It must not add new roles, content types, providers, tools, output modes,
translation generation, file editing, A2A behavior, UI, long-document chunking,
multi-round debate or context-MCP coupling.

Campaign completion requires AUD-001 through AUD-005 to be closed, F-069 to deliver
truthful metric semantics plus the blind-set schema/design contract, and F-070 to end in
a recorded evidence-backed supported-range decision. F-070 may conclude that no
dependency code change is safer, but an undocumented deferral is not completion.

## Requested re-audit questions

The independent auditor is asked to confirm or challenge these four Foreman positions:

1. Is fail-closed bounded-prefix review sufficient for AUD-001 without introducing
   document chunking into this patch campaign?
2. Is whole-envelope rejection for malformed discussion output an acceptable and
   auditable AUD-003 policy?
3. Does the distinction between role consensus and user-choice usefulness resolve the
   AUD-004 ambiguity without suppressing legitimate DecisionPoints?
4. Given validated FastMCP 2.13.0.2 and 3.4.7 evidence, should compatibility first be
   expressed as a tested matrix, an upper bound, or both?

## Foreman conclusion

No audit finding is dismissed outright. The response fully adopts five production
defects, adopts the evaluation finding with a narrower classification, and accepts the
compatibility and discussion recommendations with evidence calibration and explicit
terminology. V0.13.1 may be published after independent Foreman acceptance and
protected-main CI because normal-Goose Q-016 needs published bytes. That publication
does not lift the feature-expansion block: a new feature Campaign remains blocked until
the post-publication external Q-016 re-audit passes.
