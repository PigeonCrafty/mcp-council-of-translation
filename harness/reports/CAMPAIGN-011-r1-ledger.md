# CAMPAIGN-011-r1 Execution Ledger

## Control

- Role: `WORKER / MAIN WORKER`
- Mode: `STRICT_CAMPAIGN`
- Contract: `harness/contracts/CAMPAIGN-011-r1.md`
- Contract SHA-256: `9EB1317585B0BC999AA9615D37DAC86992EC31BCBD87B0FC45330DB9A39D83E0`
- Baseline: `610eae8e7c2df31fd9052b0ae76a2d718805f28d`
- Reports remain untracked and unstaged.

## Admission

- Observed HEAD matched the exact baseline; Git index was empty.
- Admitted dirty/untracked set matched the contract and did not overlap authorized implementation paths.
- Python: `3.12.9`; admission compile: exit 0.
- Admission suite: `294 passed in 3.85s`.
- Protected hash snapshot:
  - `harness/plan.md`: `75F2FAA2FDD00402A06393E8DDAFC29332451E26F8D0B1A23A8CE3FCB6A1F9EC`
  - `harness/features.json`: `C31F5D33DC2ACFF72A735FDB7874332E5BA52896E28F5EA0C11A8F267EBB01B1`
  - `harness/progress.md`: `6CB0D5263AC258DC361D18B498F3F6A39D9D1C63B90C22E1BC503BCC2A9DAEDB`
  - contract: `9EB1317585B0BC999AA9615D37DAC86992EC31BCBD87B0FC45330DB9A39D83E0`
  - user audit: `B48073E063C4C9F34E0B6B4DAE94E80079EAAAD3B2F8E273DD60B2F25F6ABD76`
  - `.learnings/**`: 2-file aggregate `150EB407CD40B18C42BCB2E656B49C63174B98E42C5485536B1102E902265E97`
  - `reviews/**`: 1-file aggregate `EB0B499CE4710BBAFA24B5B8ABE92572095D6ECDC801DB35A9FFB4F00336254F`
- Raw live records were not read or copied.
- Initial tool-interface error: a read-only call used an unavailable `shell_command`; rerun with `exec_command`. Self-improvement logging is skipped because `.learnings/**` is protected; the incident will remain in this ledger/report.

## Package matrix

| Package | Owner | State | Files/commit | Verification |
| --- | --- | --- | --- | --- |
| PKG-057 | Main Worker | Main Worker verified | `29e28d7`; models, roles, 2 unit tests | `19 passed`; scoped diff check passed |
| PKG-058 | Main Worker | Main Worker verified | `43c6613`; roles and new routing integration test | `17 passed`; scoped diff check passed |
| PKG-059 | Main Worker | Main Worker verified | `cc2d4bd`; models, compatibility, persistence, orchestration, 4 focused test files | `42 passed in 1.05s`; legal clean calls `4/6/7`, legal standard deep path `13`, compact/full/metadata and continuation provenance covered; scoped diff check passed |
| PKG-060 | Main Worker | Main Worker verified | `fd5589b`; digest and presentation integration test | `21 passed in 0.23s`; exact five sections, legal standard natural route, clean `<=1200`, hostile `<=3200`, verdict last, bounded internal-route sanitization, non-mutation; scoped diff check passed |
| PKG-061 | Main Worker | Main Worker verified | `1ae3a74`; evaluation runner, Golden fixture and integration test | `22 passed in 0.55s`; original 18 canonical SHA `2b00acce...120d`; exact 24/24, sampling `148`, elicitation `4`, budget sum `296`, routing/display calls `0`, all eight aggregate metrics `1.0`; scoped diff check passed |
| PKG-062 | Main Worker | BLOCKED by contract stop condition | no package commit; authorized release edits remain unstaged in `AGENTS.md`, `README.md`, both authoritative docs, `pyproject.toml`, `__init__.py`, `tools/review.py`, and two release tests | focused release tests `16 passed in 1.18s`; full suite `304 passed, 3 failed in 3.90s`. One required failure is in unauthorized `tests/integration/test_v08_presentation_invariants.py` and expects obsolete schema `2.4` from a new runtime record. Contract allows neither that path nor a false 2.4 runtime response. Lock/build/smoke stopped. |

## Delegation log

- `/root/routing_analysis`: bounded read-only PKG-057–059 architecture/test analysis; returned; Main Worker reviewed the architecture/test proposal; no diff existed.
- `/root/presentation_golden_analysis`: bounded read-only PKG-060–061 architecture/test analysis; returned; Main Worker reviewed the architecture/test proposal; no diff existed.
- No subagent has implementation, integration, staging, commit, Harness, external-call or acceptance authority.

## Deviations and incidents

- A PKG-058 inspection command used an unescaped PowerShell regex alternation and failed before its inspection ran. The focused test in the same command exposed two over-broad patch matches; a literal `Get-Content` inspection located them and the Main Worker corrected both before the passing focused run. No incorrect state was committed.
- A subsequent PKG-059 combined inspection used Bash-style brace path expansion in PowerShell and failed at parse time; it was rerun as two literal-path commands. No repository state changed.
- PKG-062 documentation patch attempts twice failed atomically because exact long-line context did not match; the edits were reapplied in smaller authorized patches. No partial change from either failed patch call survived.
- Mandatory stop: truthful Schema 2.5 runtime output makes tracked legacy test `tests/integration/test_v08_presentation_invariants.py::test_literal_v22_record_runtime_and_role_invariants` fail on its literal `2.4` assertion. That test is outside the exhaustive allowed-test list. The full suite result was `304 passed, 3 failed`; the other two failures are in the authorized persistence test and are ordinary release identifier updates, but work stopped on the forbidden-path condition before any PKG-062 commit or lock operation.

## Final blocked state

- Final committed HEAD: `1ae3a7419c1eaeb293a944a49d0873cdf95952e1` (five scoped package commits).
- Index: empty.
- PKG-062 authorized work remains unstaged and uncommitted; `uv.lock` is untouched.
- Protected hashes rechecked unchanged: plan `75F2FAA2...F9EC`, features `C31F5D33...1B1`, progress `6CB0D526...AEDB`, contract `9EB13175...3E0`, audit `B48073E0...BD76`; the two `.learnings` files and one `reviews` record retain their admission file hashes.
- Subagents: 2 read-only; approval/escalation requests: 5 (scoped local commits); dependency operations: 0; live/model/provider calls: 0; external mutations: 0.
