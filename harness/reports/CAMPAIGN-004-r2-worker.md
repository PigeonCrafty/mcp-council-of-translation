# CAMPAIGN-004-r2 Main Worker Report

## Terminal disposition

`READY_FOR_REVIEW`

This is a Worker handoff only. It does not claim Campaign acceptance or project
completion.

## Authority and admission

- HARNESS_ROLE: WORKER / MAIN WORKER
- HARNESS_MODE: STRICT_CAMPAIGN
- Contract: `harness/contracts/CAMPAIGN-004-r2.md`
- Contract SHA-256:
  `7FF4F4BC13A8527C73504E2DD43FA2CACBA3491B8F85DBF8AF37049D80A3BC3A`
- Exact baseline: `ff0e345ff174f1f39741bbb47979aa51e277ca52`
  (`Release concise Council display contract`)
- Admission: exact HEAD/subject and contract hash, empty index, expected declared dirt,
  all eleven protected hashes exact, `myTest/` absent, compile pass, and exactly
  `196 passed in 2.46s`.
- Subagents: forbidden / 0 used.

## Before/after counterexamples

### PKG-028 metadata-only history

Before editing, a real `ReviewStore.save(..., history_mode="metadata")` and raw JSON read
reported both metadata blocks as:

- `runtime_metadata`: `0.6.0 / guided-deliberation-v4`
- `version_metadata`: `0.6.0 / guided-deliberation-v4`

After correction, the same real save/read path reports:

- `runtime_metadata`: `0.7.0 / concise-council-display-v5`
- `version_metadata`: `0.7.0 / concise-council-display-v5 / schema 2.2`

The projection uses two local constants as one source of truth. Its existing field
allowlist is unchanged; full/off behavior, read compatibility, names, atomic writes and
existing record files were not changed or rewritten.

### PKG-029 primary-text identifiers

Before editing, the Foreman examples `cluster_deadbeef` and `POSITION_F00DBABE` both
survived into `display_report` primary text.

After correction, one deterministic sanitizer runs through `_human_line` for every
renderer field family. It case-insensitively removes standalone `issue_`, `cluster_`,
`position_`, `decision_`, `option_` and `gap_` identifiers, translates exact raw role
IDs to Chinese display names, and removes established implementation labels.

The post-fix boundary probe found zero standalone internal IDs. It preserved ordinary
embedded translation tokens (`precluster_deadbeef`, `optioning`), `{count}`, blocker
language and the final disposition. The adversarial test covers background, role
perspective/evidence, consensus, disagreement, blind spots, minority/condition,
interaction, editor synthesis and checklist, plus the dual-channel first text and
permitted review-ID footer.

## Commits and changed files

Final HEAD: `3779a78a9788018082470408fdd4d87a042985dc`

1. `5caaf2cead25b875f464526be72ffd406a644ce2` — Fix V0.7 metadata history identifiers
   - `src/council_of_translation/localization/persistence.py`
   - `tests/unit/test_persistence_v2.py`
2. `3779a78a9788018082470408fdd4d87a042985dc` — Sanitize primary Council internal identifiers
   - `src/council_of_translation/localization/digest.py`
   - `tests/unit/test_v07_report.py`

Baseline-to-final: four authorized files, 121 insertions and 8 deletions; scope mismatch
count 0. No other production/test/doc/config file changed.

## Verification

- Admission compile: pass.
- Admission full suite: `196 passed in 2.46s`.
- PKG-028 focused persistence: `16 passed in 0.27s`.
- PKG-029 final report/integrity/dual-channel focused suite: `11 passed in 1.05s`.
  The first run was `1 failed, 10 passed` because a preserved test token contained the
  forbidden sample as a substring; the non-overlapping ordinary-token sentinel was
  corrected without weakening the production rule.
- Integrated focused command over all four authorized test files:
  `27 passed in 1.11s`.
- Final `python -m compileall -q src tests`: pass.
- Final full command:
  `.venv\Scripts\python.exe -m pytest -q --basetemp .tmp\campaign004-r2-full -p no:cacheprovider`
  -> `198 passed in 2.01s`.
- `git diff --check ff0e345ff174f1f39741bbb47979aa51e277ca52..HEAD`: pass.
- Exact allowed-path audit: four changed files, zero mismatches.
- Invariant probe: exactly five tools, module/package 0.7.0, build
  `concise-council-display-v5`, schema 2.2 and budgets 6/13/18.
- Index: empty after both commits and at final inspection.

## Fresh artifacts and isolated wheel smoke

Fresh repository-local `uv build` produced:

- `council_of_translation-0.7.0-py3-none-any.whl` — 74,274 bytes — SHA-256
  `5C7F575B5D583B3632B7D0447115BDE2C5E40AD5233783B1A73E71C4712ADC21`
- `council_of_translation-0.7.0.tar.gz` — 67,707 bytes — SHA-256
  `B19399B89543F9A048245709697F294FF73522C021700F1D4F1E42CC30B9E7F8`

The wheel was installed into one fresh repository-local environment with current
FastMCP 3.4.7 / MCP 1.29.0. An isolated `-I` script invoked registered tools and
verified:

- exact five-tool surface and 0.7.0/build/schema/budget invariants;
- real `review_translation` primary text plus structured content;
- real metadata-history file with both V0.7 identifier blocks and no source/candidate;
- adversarial primary report has no six-family IDs while retaining `{count}`, material
  risk, degradation, final disposition and the allowed review-ID footer;
- structured content remains complete and may retain its internal marker.

Result:
`R2_WHEEL_SMOKE_OK fastmcp=3.4.7 mcp=1.29.0 tools=5 primary_len=634 metadata=0.7.0 sanitized_len=245`.

Per contract, r1 FastMCP 2.13 evidence was reused and no second network-dependent
compatibility environment was created.

## Protection, authority and deviations

- Contract SHA-256 remains exact.
- All eleven listed protected assets remain byte-for-byte exact; mismatch count 0.
- Original tracked Foreman dirt remains exactly `harness/features.json`,
  `harness/plan.md`, and `harness/progress.md`.
- Protected/untracked r1/r2 Harness assets, `.learnings/`, `reviews/`, audit Markdown
  remain present and untouched. This report is the sole new Harness asset.
- Git authority escalations: four requests for two exact staging operations and two
  local commits. The first staging request timed out at the tool boundary, but read-only
  reconciliation proved both intended files had been staged; it was not repeated.
- Self-improvement logging was intentionally not written because `.learnings/**` is
  protected; the staging timeout and test retry are recorded here.
- External package/network operations: one fresh current wheel dependency resolution,
  served mostly from the existing repository-local cache; no retry.
- Live Goose/model/provider calls: 0.
- No push, PR, tag, release, deployment, credential request, dependency change or Goose
  modification.

## Skipped checks and remaining risks

- Live Goose/provider validation was prohibited and skipped. Q-009 remains for Foreman
  or later post-acceptance validation.
- FastMCP 2.13 was not reinstalled or rerun, as the r2 contract explicitly reuses r1
  evidence.
- The sanitizer deliberately targets standalone implementation-token grammar. Ordinary
  larger source/translation tokens containing the same substring are preserved; this is
  the frozen non-erasure boundary and has explicit tests.
