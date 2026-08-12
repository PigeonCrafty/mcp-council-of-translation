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
- Current expected diagnostic build: `concise-council-display-v5`
- Current version: `0.7.0`

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

- `package_version`: `0.7.0`
- `module_version`: `0.7.0`
- `diagnostic_build`: `concise-council-display-v5`

## Repository Hygiene

- Do not commit `myTest/` unless explicitly requested; it contains user test fixtures and output captures.
- Do not revert user-created files or test outputs.
- Keep MCP tool descriptions aligned with the output contract so clients do not keep asking for obsolete `recommended_translation`.
