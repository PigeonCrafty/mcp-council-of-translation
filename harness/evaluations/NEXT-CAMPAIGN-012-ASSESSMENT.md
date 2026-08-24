# Next Product Campaign Assessment: Client-verifiable Evidence Receipt

- Assessment decision: `RECOMMEND CAMPAIGN-012 DESIGN`
- Proposed product release: `0.12.0`
- Proposed diagnostic build: `verifiable-evidence-council-v10`
- Proposed persisted schema: remain `2.5` unless implementation proves a stored-field
  migration is necessary
- Proposed feature packages: 5
- Proposed post-publication quality gate: `Q-014`
- Implementation authorization: not issued by this assessment

## Executive assessment

The original audit's product architecture is now substantially complete: realistic
specialist roles, deterministic preflight, issue clustering, bounded discussion,
interactive briefing and decisions, targeted reconsideration, Policy Gate, evidence-
weighted adjudication, content-aware routing, compact process-first presentation,
persistence, concurrency, executable Golden evidence and live Goose validation are all
implemented and accepted. The current state is 52/52 accepted features and 13/13
accepted quality gates.

The highest-value remaining gap is no longer Council reasoning quality. It is the handoff
of authoritative execution facts through clients such as Goose. Q-013 proved that the
normal human report can be concise and correct while the outer agent still renames role
IDs, substitutes status aliases, or reports the wrong sampling budget when asked to
reconstruct technical evidence. The persisted record remains correct, but a user should
not need to trust a second model-generated paraphrase to verify it.

CAMPAIGN-012 should therefore add a deterministic, client-neutral evidence receipt to
the existing history tool. It should not add another reviewer, another public MCP tool,
another model call, or more ordinary-report detail.

## Product outcome

An auditor or outer agent can call the existing
`view_review_record(review_id, detail_level="verification")` and receive two matching
channels:

1. a bounded, human-readable verification receipt as primary text; and
2. a canonical structured receipt containing the same facts with stable field names.

Both projections are derived only from the persisted review record. They perform zero
sampling and zero elicitation, never alter the record, and never replace the normal
five-section `review_translation` report.

## Proposed feature packages

### PKG-065: Canonical verification receipt contract

Define a versioned derived receipt with explicit semantics for:

- review ID, package/module version, build and schema;
- routing profile, reason codes and ordered active roles;
- per-role sample status, coverage, successful and unavailable counts;
- total sampling calls, applicable budget and elicitation calls;
- canonical status, degradation, warnings and fallback provenance;
- chief publishability, human-review flag and suggested-translation presence;
- deterministic preflight blockers and bounded material issue summaries;
- runtime wall-clock, sampling-wait and concurrency provenance; and
- terminal-disposition count and text/structure coherence.

The receipt must distinguish server-measured runtime from external Goose wall time and
must distinguish total sampling calls from independent-review success count.

### PKG-066: Privacy-safe deterministic projector

Project the receipt from persisted data without model inference. Omit raw source,
candidate, full reviewer prose, credentials, filesystem paths and internal issue IDs by
default. Old records with absent fields must say `not_recorded`, never guess. A future
integrity fingerprint may be evaluated separately; it is not required for the first
release.

### PKG-067: Existing-tool verification view

Add `verification` as a backward-compatible `detail_level` on
`view_review_record`. Preserve `full` and `summary`, exact five-tool registration,
review-only defaults, normal report limits, budgets, concurrency and every adjudication
rule. The verification primary text should be compact, tabular or short-list oriented,
and should not expose raw internal IDs unless they are explicitly part of the receipt
contract.

### PKG-068: Coherence, compatibility and privacy evidence

Add live-shaped A/B/C record fixtures and negative controls proving:

- both channels agree on status and terminal disposition;
- routing, roles, calls and budgets are copied exactly rather than paraphrased;
- deterministic blockers remain separate from model-only issues;
- unavailable/legacy fields remain truthful;
- receipt generation makes no sampling, elicitation or persistence mutation;
- hostile prose cannot leak into receipt metadata; and
- FastMCP supported-version behavior and the exact five-tool surface remain stable.

Extend the executable Golden framework only where receipt assertions add new evidence;
do not duplicate all translation-quality cases.

### PKG-069: V0.12 release and operator documentation

Migrate package/module/build identifiers, refresh only the editable root lock metadata,
build fresh wheel/sdist artifacts, and document when to use normal, summary, full and
verification views. The ordinary caller guidance remains: call `review_translation`
directly; use the verification view only for audits, acceptance and diagnostics.

## Q-014 live gate

After protected-main publication, run normal Goose against one unchanged extension
command and validate at least:

- clean lightweight legal-risk coverage;
- standard material-edit disposition; and
- strict deterministic blocker plus separate semantic issue.

For each case, Goose must print the receipt without renaming canonical fields, inventing
values or confusing total calls with role successes. The receipt itself, not Goose's
surrounding prose, is the evidence authority. Normal `review_translation` presentation
must remain unchanged and concise.

## Explicit non-goals

- No new public MCP tool.
- No file translation, batch ingestion, translation-memory ownership or edit application.
- No dynamic model/provider routing or role voting.
- No new reviewer role merely to increase apparent coverage.
- No fuzzy semantic deduplication.
- No raw full-record dump in the ordinary primary response.
- No change to user authority, Policy Gate, review-only safety or 6/13/18 budgets.

## Alternatives considered

Batch/cross-segment consistency and long-document chunking have real user value, but
they expand this review-only server into workflow and file ownership already assigned to
the outer agent. More roles or multi-model routing would increase cost and complexity
without addressing the live evidence mismatch. Confidence calibration is a plausible
later Campaign after trustworthy measurement can be exported consistently.

## Principal risks

1. A receipt can become another verbose report. Keep it opt-in and bounded.
2. Field names can imply false precision. Define every count and timing source explicitly.
3. A derived view can accidentally become a second source of truth. Persisted records
   remain authoritative and receipt tests must prove deterministic derivation.
4. Backward compatibility can encourage guessed legacy fields. Missing historical data
   must remain visibly unavailable.
5. Exposing technical evidence can leak source or model prose. The default receipt must
   be privacy-safe by construction.

## Readiness judgment

The Campaign is technically feasible, bounded and aligned with the product purpose. It
addresses the only repeated live-client defect left by Q-013 while preserving the
Council's process-first user experience. Recommended planning size is five feature
packages plus one post-publication live gate. The next Foreman action should freeze the
receipt field contract and issue a versioned CAMPAIGN-012 implementation contract; no
production implementation begins from this assessment alone.
