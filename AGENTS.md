# Council-of-Translation Agent Notes

## Project Purpose

Council-of-Translation is a review-only MCP server for localization translation QA. It does not translate files or apply edits directly. The outer agent owns translation memory, TB/SG retrieval, project rules, and the final edit application.

## Current Workflow

- Main tool: `review_translation(...)`
- Continuation tool: `continue_review(...)`
- History tools: `view_review_record(...)`, `list_review_records(...)`
- Diagnostic tool: `get_server_info()`
- Default output mode: `review_only`
- Default interactive mode: `auto`
- Default briefing mode: `auto`
- Default decision fallback: `council_adjudication`
- Default trace level: `summary`
- Default history mode: `full`
- Current expected diagnostic build: `risk-coherent-council-v9.1`
- Current version: `0.11.1`

Only independent reviewer sampling is concurrent. The per-review default is three;
`COUNCIL_REVIEW_CONCURRENCY` accepts only `1`, `2`, or `3`, and invalid values visibly
fall back to sequential execution. Briefing precedes the batch, and context interaction,
reconsideration, discussion, Policy Gate, adjudication, digest, and persistence remain
phase-ordered after the complete batch settles. Sampling budgets remain 6/13/18.

Normal callers should call `review_translation` directly. `get_server_info` is only for cache/version checks; `review_translation` already returns `server_info`.

## Review Output Contract

Independent reviewer output is intentionally two-layered:

- `role_feedback`: natural feedback from the reviewer role's real localization perspective.
- `findings`: lightweight MQM-like annotations for machine aggregation and outer-agent execution.

Each finding should include:

- `source_span`
- `candidate_span`
- `issue_type`
- `severity`
- `role_perspective`
- `problem`
- `evidence`
- `evidence_type`
- `action`

Before sampling, `briefing_mode=auto` asks source/candidate-only callers for bounded context; rich packets skip it, `always` requires it, and `off` records assumptions. Reviewers may also return optional material `context_gaps`; invalid gaps do not erase valid findings, Core asks at most two once, and accepted answers reconsider only affected roles. Context and outcome reconsideration provenance are separate.

Findings are clustered by issue, optionally discussed once, and adjudicated through a Policy Gate and evidence-weighted Position Matrix. V2.2 reviewers classify `issue`, `choice`, and `affirmation`; only `finding_kind="choice"` with a concrete bounded `proposed_value` can become an outcome, while `action` remains advice even for legacy, missing, invalid, or incomplete classifications. RolePositions and DecisionPoints share one deterministic outcome identity. Repeated or synonymous findings do not multiply a reviewer's authority. A consistent bounded `candidate_span` supplies the issue-local current outcome; proposed replacements are applied only at one provable anchor and deterministic checks run against the reconstructed complete candidate. Missing or repeated anchors persist content-free suppression provenance and surface degraded fallback warnings; ordinary hard-constraint rejection does not. The batched form uses human-readable enum values mapped per field to exact internal outcomes, keeps a known current outcome first, and offers explicit Council delegation last. Only contrary/materially affected roles reconsider; requested/completed/skipped/failed provenance is recorded, and budget/runtime gaps surface as degradation and warnings. Structured reviewer coverage is recorded separately from finding count. Success requires both envelope keys, a string `role_feedback`, a list `findings`, and safely validated finding objects; empty findings additionally require non-blank feedback. If any finding entry is invalid, the whole sample's findings are discarded and it is unavailable. Partial or zero coverage requires human review and is exposed in fallback/runtime metadata. User choices are decisive only among valid options and cannot override technical integrity, semantic correctness, deterministically checked caller hard rules, or critical blockers. Use `hard_constraints` values `numeric_parity`, `markdown_parity`, `required_literal:<text>`, or `forbidden_literal:<text>` for machine-enforced caller rules; other rule packets remain authoritative reviewer context but do not become deterministic blockers by model assertion alone.

Schema 2.5 adds bounded deterministic routing provenance to the existing structured trace. `CouncilPlan.routing_profile` selects one of 15 fixed content/mode portfolios and `routing_reason_codes` records only bounded vocabulary. Legal-risk routing is exactly 4 roles for lightweight, 6 for standard, and 7 for strict; routing never inspects free source, candidate, context, audience, or notes prose and adds no sampling or elicitation. Older V2.0-V2.4 records load with conservative unrecorded-routing defaults.

Schema 2.4 introduced deterministic `council_value_metrics`. Each active role is classified as `unique_material`, `corroborating`, `confirmation_only`, or `unavailable`; repeated same-role findings count once per issue. Discussion adds evidence value only for a new bounded structured anchor/provenance item absent from the validated pre-discussion inventory and prior turns; natural-language paraphrases conservatively add zero, while real position/resolution deltas remain independent. These diagnostics are descriptive, never votes or authority weights. The primary report uses exactly five sections: 审校背景, Council 新增视角, 角色覆盖与分工, 共识、分歧与盲区, 主编结论. Confirmation-only roles share one coverage line. Its human work-item projection groups deterministic checks and reviewer corroboration only through bounded protected anchors and check provenance; model-only cross-category findings group only when their exact source/candidate anchors and concrete replacement match. Distinct repairs and material consequences remain visible. This projection changes primary prose only: full clusters, checklist, metrics and structured evidence are unchanged. Clean output targets 1,200 Unicode code points and every report remains capped at 3,200.

Default `review_only` output must not include a full recommended translation. The chief editor returns an execution checklist such as:

- `must_fix`
- `should_fix`
- `optional_improvements`
- `terminology_decisions`
- `conflict_resolutions`
- `execution_order`

Only explicit `output_mode=full_rewrite` may return `suggested_translation`.

## Design Priorities

1. Preserve realistic reviewer roles instead of turning every reviewer into a generic MQM scorer.
2. Use findings as lightweight labels for aggregation, conflict detection, and execution.
3. Keep outputs compact for long documents.
4. Prefer actionable review advice over rewritten translations.
5. Respect caller-provided TB, SG, project rules, technical constraints, and known exceptions over generic reviewer preference.

## Local Testing

Run syntax checks:

```powershell
python -m compileall src tests
```

Run the lightweight unit/security test harness when pytest is unavailable:

```powershell
$env:PYTHONPATH='src'; @'
from tests.unit import test_security
for module in (test_security,):
    for name in dir(module):
        if name.startswith('test_'):
            getattr(module, name)()
print('OK')
'@ | python -
```

## Goose / uvx Usage

Use a pinned commit when testing a fresh version in Goose:

```powershell
uvx --refresh --from git+https://github.com/PigeonCrafty/mcp-council-of-translation@<approved-commit> mcp_council_of_translation
```

If Goose appears stale, call `get_server_info()` and verify:

- `package_version`: `0.11.1`
- `module_version`: `0.11.1`
- `diagnostic_build`: `risk-coherent-council-v9.1`

## Repository Hygiene

- Do not commit `myTest/` unless explicitly requested; it contains user test fixtures and output captures.
- Do not revert user-created files or test outputs.
- Keep MCP tool descriptions aligned with the output contract so clients do not keep asking for obsolete `recommended_translation`.
