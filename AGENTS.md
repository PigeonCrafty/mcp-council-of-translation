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
- Default decision fallback: `council_adjudication`
- Default trace level: `summary`
- Default history mode: `full`
- Current expected diagnostic build: `structured-deliberation-v2`
- Current version: `0.4.0`

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

Findings are clustered by issue, optionally discussed once, and adjudicated through a Policy Gate and evidence-weighted Position Matrix. RolePositions and DecisionPoints share one deterministic option identity. Repeated findings do not multiply a reviewer's authority: each reviewer has one fixed total matrix influence, normalized across its distinct actions. Safe discussion changes update only an existing affected matrix row. The one batched form describes every choice and restricts fields to valid IDs; fallback selects a non-tied valid action and leaves genuine ties for human review. Structured reviewer coverage is recorded separately from finding count; full structured zero-finding responses are clean coverage, while partial or zero coverage requires human review and is exposed in fallback/runtime metadata. User choices are decisive only among valid options and cannot override technical integrity, semantic correctness, deterministically checked caller hard rules, or critical blockers. Use `hard_constraints` values `numeric_parity`, `markdown_parity`, `required_literal:<text>`, or `forbidden_literal:<text>` for machine-enforced caller rules; other rule packets remain authoritative reviewer context but do not become deterministic blockers by model assertion alone.

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

- `package_version`: `0.4.0`
- `module_version`: `0.4.0`
- `diagnostic_build`: `structured-deliberation-v2`

## Repository Hygiene

- Do not commit `myTest/` unless explicitly requested; it contains user test fixtures and output captures.
- Do not revert user-created files or test outputs.
- Keep MCP tool descriptions aligned with the output contract so clients do not keep asking for obsolete `recommended_translation`.
