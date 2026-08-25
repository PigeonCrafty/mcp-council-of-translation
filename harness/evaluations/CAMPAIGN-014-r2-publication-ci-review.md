# CAMPAIGN-014 V0.13.1 Publication and CI Review

- Decision: `PUBLISHED; SIX_WAY_CI_ACCEPTED; Q-016_READY_TO_ISSUE`
- Accepted implementation: `9d23ed01f94be2ef0c724b3e0a3e7e1beba75c09`
- Protected-main publication PR: `#34`
- PR URL: `https://github.com/PigeonCrafty/mcp-council-of-translation/pull/34`
- Published protected `main`: `9d8f1f987efe73946377883e6ad3a681abe11989`
- Publication date: 2026-08-25 Asia/Shanghai

## Publication integrity

- The release branch rebased the eight accepted CAMPAIGN-014 product commits onto the
  admitted remote governance baseline and archived the r1/r2 contracts, ledgers, Worker
  reports, Foreman reviews, independent audit, audit response, assessment and stage
  report.
- The rebased product tree matched accepted implementation `9d23ed0` on every product
  path before publication. The only later product-tree difference was a test-only Python
  3.10 import fallback in `tests/integration/test_v10_release_contract.py`; production,
  dependency, lock and workflow bytes were unchanged.
- The PR used protected-main squash merge. The resulting published tree contains V0.13.1
  plus its accepted governance evidence at `9d8f1f9`.

## CI correction and independent verification

Initial PR workflow run `32841294199` exposed one portability defect in the release test:
Ubuntu and Windows Python 3.10 could not import standard-library `tomllib`. Python 3.12
and 3.13 passed, and the failure occurred before any product assertion.

The bounded correction added the conventional Python 3.10 test fallback to `tomli` in
that one authorized test module. Local exact Python 3.10 verification then passed the
focused release tests and the complete `575 passed` suite. No source, dependency, lock,
workflow or runtime contract changed.

Updated PR workflow run `32841766264` passed all six required jobs:

- Ubuntu / Python 3.10: passed in 25s
- Ubuntu / Python 3.12: passed in 19s
- Ubuntu / Python 3.13: passed in 14s
- Windows / Python 3.10: passed in 39s
- Windows / Python 3.12: passed in 30s
- Windows / Python 3.13: passed in 39s

Post-merge protected-main workflow run `32841918734` also passed all six jobs:

- Ubuntu / Python 3.10: passed in 22s
- Ubuntu / Python 3.12: passed in 19s
- Ubuntu / Python 3.13: passed in 16s
- Windows / Python 3.10: passed in 38s
- Windows / Python 3.12: passed in 38s
- Windows / Python 3.13: passed in 33s

## Published contract

- Package/module: `0.13.1`
- Diagnostic build: `truthful-boundaries-council-v11.1`
- Persisted Review Schema: `2.6`
- Verification receipt Schema: `1.1`
- Golden evaluator Schema: `2.1`
- Public tools: exactly five
- Review-only boundary, defaults, budgets `6/13/18`, concurrency `1..3` and 15 routing
  profiles remain frozen.
- FastMCP supported range: `>=2.13.0.2,<4`; installed-wheel evidence covers exact
  `2.13.0.2` and `3.4.7`.

## Next gate

Q-016 may now be issued. It combines three fresh normal-Goose published-main cases with
an independent repository re-audit of AUD-001 through AUD-007. Publication and passing CI
do not accept Q-016 and do not lift the external-audit feature-expansion block. No live
Goose/provider call, package-index publication or deployment occurred in this review.
