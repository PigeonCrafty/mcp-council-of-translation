# Council-of-Translation Agent Notes

## Project Purpose

Council-of-Translation is a review-only MCP server for localization translation QA. It does not translate files or apply edits directly. The outer agent owns translation memory, TB/SG retrieval, project rules, and the final edit application.

## Current Workflow

- Main tool: `review_translation(...)`
- Diagnostic tool: `get_server_info()`
- Default output mode: `review_only`
- Default conflict review mode: `auto`
- Current expected diagnostic build: `role-feedback-findings-v1`
- Current version: `0.3.0`

Normal callers should call `review_translation` directly. `get_server_info` is only for cache/version checks; `review_translation` already returns `server_info`.

## Review Output Contract

Reviewer output is intentionally two-layered:

- `role_feedback`: natural feedback from the reviewer role's real localization perspective.
- `findings`: lightweight MQM-like annotations for machine aggregation and outer-agent execution.

Each finding should include:

- `span`
- `issue_type`
- `severity`
- `role_perspective`
- `problem`
- `evidence`
- `action`

Default `review_only` output must not include a full recommended translation. The chief editor should return an execution checklist such as:

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
from tests.unit import test_localization_review, test_security
for module in (test_localization_review, test_security):
    for name in dir(module):
        if name.startswith('test_'):
            getattr(module, name)()
print('OK')
'@ | python -
```

## Goose / uvx Usage

Use a pinned commit when testing a fresh version in Goose:

```powershell
uvx --refresh --from git+https://github.com/PigeonCrafty/mcp-council-of-translation@70d8162 mcp_council_of_translation
```

If Goose appears stale, call `get_server_info()` and verify:

- `package_version`: `0.3.0`
- `module_version`: `0.3.0`
- `diagnostic_build`: `role-feedback-findings-v1`

## Repository Hygiene

- Do not commit `myTest/` unless explicitly requested; it contains user test fixtures and output captures.
- Do not revert user-created files or test outputs.
- Keep MCP tool descriptions aligned with the output contract so clients do not keep asking for obsolete `recommended_translation`.
