# CAMPAIGN-011-r3 Execution Ledger

Status: `READY_FOR_REVIEW`

## Control

- Role: `WORKER / MAIN WORKER`
- Mode: `STRICT_CAMPAIGN`
- Contract: `harness/contracts/CAMPAIGN-011-r3.md`
- Contract SHA-256: `BA884359309326C179E5A42AF44D24872B960FD0D717130B59E88C534066C64A`
- Baseline: `938c3a4bb9f14c7688286b25eabd8aff9f18a09d`
- Subagents: `0`; no delegation authority was granted.

## Admission

- Exact HEAD matched and Git index was empty.
- Admission compile: exit 0.
- Admission complete suite: `307 passed in 4.17s`.
- Protected path hashes and the admitted dirty/untracked set were captured before implementation.
- `.tmp/q012/**`, `.learnings/**`, and `reviews/**` were confirmed present without traversal; raw content was not read or copied.

## Package state

| Package | State | Files | Commit | Main Worker verification |
| --- | --- | --- | --- | --- |
| PKG-063 | `MAIN_WORKER_VERIFIED` | `digest.py`, new `test_v25_risk_routing.py` | `4fce7d6` | 4 new counterexamples passed; affected presentation 21 passed; routing/Golden 10 passed |
| PKG-064 | `MAIN_WORKER_VERIFIED` | nine changed authorized release-migration paths | `76921ec` | release/persistence/tool surface 38 passed; affected presentation/routing/Golden 31 passed; full integration 311 passed |

## Final integration evidence

- Final HEAD: `76921ecb69ec26f0034ec772433e102a3f7715bf`.
- Exact two commits since baseline: `4fce7d6`, `76921ec`.
- Final compile: exit 0; complete suite: `311 passed in 3.81s`.
- Golden: `24/24`, no failures, all eight aggregate metrics `1.0`; 148 sampling calls, 4 elicitation calls, aggregate budget 296, zero routing/display model calls.
- Pinned uv 0.12.3 lock check: exit 0; revision/package/upload-time counts remain `3/78/586`; only root version changed `0.11.0 -> 0.11.1`.
- Baseline-to-final: 11 authorized paths, `194 insertions, 25 deletions`; `git diff --check` passed and index is empty.
- Fresh sdist/wheel built and inspected; isolated Python 3.12.9/FastMCP 3.4.7 smoke called all five tools and verified dual-channel terminal-disposition coherence.
- Protected hashes reconciled exactly; sensitive directories remained untraversed.

## Deviations

- Ruff and pyflakes were unavailable; a standard-library AST scan found zero unused imports in the changed Python hotspots. No dependency was added.
- The first isolated smoke assertion treated the allowed review-ID footer as part of `display_report`; the corrected probe separately verified the report terminal line and footer and passed.
- The first new focused-test run exposed the existing eight-entry digest bound. The authorized direct caller was corrected to retain seven bounded digest actions plus the canonical final; the full structured chief remains unchanged.

## Operations

- Live Goose/provider/model calls: `0`.
- External mutations: `0`.
- Push/PR/release/deploy operations: `0`.
- Sandbox authority escalations: `4`, limited to two scoped `git add` and two scoped `git commit` operations.
- Pinned uv operations: `7` (`--version`, refresh, two lock checks, build, isolated venv, isolated install).
