# Campaign Review: CAMPAIGN-011-r2

## Decision

`ACCEPTED`

CAMPAIGN-011-r2 completes the bounded PKG-062 release correction without changing the
frozen V0.11 design. Combined r1/r2 evidence accepts F-047 through F-052 and the local
V0.11 implementation. Publication and Q-013 remain separate gates.

## Control

- Role: `FOREMAN`
- Harness mode: `STRICT_CAMPAIGN`
- Contract: `harness/contracts/CAMPAIGN-011-r2.md`
- Contract SHA-256:
  `295A701866F90A6BC0E8FD249E62784D2DEDE792541089A32DA8C499F9D3F663`
- Baseline: `1ae3a7419c1eaeb293a944a49d0873cdf95952e1`
- Accepted HEAD: `565e97d19efbbd7ff009f747a48979fceb002d11`
- Commit: `565e97d Complete V0.11 release migration`
- Worker report: `harness/reports/CAMPAIGN-011-r2-worker.md`
- Worker report SHA-256:
  `3D6D2993C3913FE4CED0434EE1C350EDD018A8B0626FFE1F98EDD12CC152DC17`

## Scope and correction review

- The baseline is an ancestor of accepted HEAD and the r2 delta is exactly one commit,
  53 insertions and 47 deletions over the twelve contract-authorized paths.
- The nine admitted release files remain byte-identical to their admission hashes. The
  additional changes are limited to one current-runtime Schema assertion, two parametrized
  current-write version/build assertions and the root lock version.
- Historical V2.0 through V2.4 parsing remains asserted; the corrected Schema 2.5 assertion
  concerns a newly executed V0.11 record, not a historical fixture.
- `uv.lock` changes only the editable root version from 0.10.2 to 0.11.0 and retains
  revision 3, 78 packages and 586 upload-time entries. Its final SHA-256 is
  `6C8846F9560B5057657AB8CBAD48912F606D0FAC5899087306C76D298ED9D8E2`.
- `git diff --check` passes. The index is empty and the Worker report remains untracked.
  No protected/user asset, dependency, public tool, role, route, budget or external state
  changed outside the contract.

## Independent verification

- Contract, report, r1 evidence and all pre-review protected hashes matched exactly.
- Full compile passed and the complete suite passed `307 passed in 4.09s` with a unique
  repository-local basetemp.
- Direct runtime probes verified package/module `0.11.0`, diagnostic build
  `risk-coherent-council-v9`, Schema `2.5`, exact five tools, budgets 6/13/18 and
  concurrency limit/max 3.
- Direct legal-risk probes verified exact ordered reviewer portfolios of 4 in lightweight,
  6 in standard and 7 in strict.
- The production Golden runner passed exactly 24/24. All eight aggregate metrics are 1.0;
  runtime totals are 148 samples, four elicitations, aggregate budget 296, zero routing
  calls and zero display calls.
- Pinned uv 0.12.3 `lock --check` resolved the same 78 packages.
- A fresh Foreman wheel and sdist build succeeded. Archive inspection found no `.tmp`
  content and verified V0.11 metadata/source. Loading directly from the fresh wheel verified
  version/build/schema and exact five-tool registration.
- The Foreman artifact hashes differ from the Worker artifact hashes because these Python
  archives embed build timestamps. File scope, metadata, installed source and observable
  behavior match; reproducible binary hashes were not a contract criterion.

## Campaign acceptance

- F-047: accepted — deterministic 15-profile routing and bounded provenance.
- F-048: accepted — exact legal-risk 4/6/7 panoramic portfolios without a new legal role.
- F-049: accepted — Schema 2.5 persistence/continuation provenance and old-record
  compatibility within existing budgets.
- F-050: accepted — concise, privacy-safe five-section risk-route presentation.
- F-051: accepted — executable 24-case Golden risk corpus with all metrics at 1.0.
- F-052: accepted — V0.11.0/build v9 migration, full regression and fresh artifacts.

The accepted local product implementation is
`565e97d19efbbd7ff009f747a48979fceb002d11`. This review does not claim publication or
Q-013 live Goose acceptance. The next gate is protected-main archival/publication followed
by a pinned normal-Goose Q-013 risk-routing run.

## Disclosed verification incident

The first Foreman wheel-registration probe called a FastMCP convenience method not present
in the current project environment. No repository state changed. The rerun used that
version's available `get_tools()` interface and passed. The self-improvement log was not
modified because `.learnings/**` is a protected user asset. A later read-only JSON
validation one-liner also had a missing closing brace and failed before inspection; the
corrected validation passed without changing repository state.
