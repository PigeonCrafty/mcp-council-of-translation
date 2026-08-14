# CAMPAIGN-009-r1 Main Worker Ledger

## Control

- Role/mode: `WORKER / MAIN WORKER`, `STRICT_CAMPAIGN`
- Contract: `harness/contracts/CAMPAIGN-009-r1.md`
- Contract SHA-256: `F4C8EB61730E94279E028821FF08E1CA6E2B81C772D8CFC90AF63C3538DF8758`
- Baseline: `e3d3de275915088c1430a243dfd9c2e410cbc58a`
- Package order: PKG-049 -> PKG-050 -> PKG-051 -> PKG-052
- Subagents: 0
- Acceptance authority: Foreman only

## Admission

- Exact HEAD/subject: passed (`Archive accepted Campaign 008`).
- Git index: empty.
- Declared Foreman/user dirty and untracked assets: recorded and protected.
- Contract and all enumerated protected SHA-256 values: matched.
- Baseline compile: passed.
- Baseline complete suite: `278 passed in 7.17s`.

## Package state

| Package | State | Commit/files | Verification |
| --- | --- | --- | --- |
| PKG-049 | COMPLETE | `30ddddf`; `value_metrics.py`, `test_v24_value_metrics.py` | Focused `21 passed`; complete suite `280 passed`; diff check passed |
| PKG-050 | COMPLETE | `ef864a3`; `digest.py`, `orchestration.py`, `test_v24_presentation.py` | Presentation focus `19 passed`; complete suite `281 passed`; diff check passed |
| PKG-051 | COMPLETE | `1987c4c`; new `test_v101_live_shaped_value.py` | V2.4/A-B/Golden focus `31 passed`; exact Golden `18/18`, `113` samples, `4` elicitations, all eight metrics `1.0`; complete suite `283 passed` |
| PKG-052 | COMPLETE | `62f2ee9`; version/build, docs, exact tests, `uv.lock` | Release focus `39 passed`; pinned lock one-line root change; complete suite `283 passed`; fresh build and wheel smoke passed |

## Integrated verification

- Final HEAD: `62f2ee9bf1860f80281afbbad53734db5f700205`; four scoped commits; index empty.
- Final compile: passed; complete regression: `283 passed in 3.80s`.
- Final named Campaign selection: `64 passed in 1.67s`.
- Exact executable Golden Corpus: `18/18`, `113` scripted samples, `4` scripted
  elicitations, eight aggregate metrics at `1.0`.
- Pinned uv `0.12.3` refresh: lock revision `3`, `78` packages, `586` upload-time
  entries; baseline diff only editable root `0.10.0 -> 0.10.1`; final SHA-256
  `5AF8048D3FEA8F19EBDB0CCDB576C0E3B5B217DE5CBD19B042AC335DD46289F3`.
- Fresh wheel SHA-256:
  `B12310E4A4180FA9FEBE766119CF2BF60CCE4095297050D6F3E6F622E7CE852D`.
- Fresh sdist SHA-256:
  `D0A3447C8AB4D1CB3A207D23664F9477988C2A23FA48A06733EF3571453FD0E5`.
- Isolated Python `3.12.9` / FastMCP `3.4.7`: all five tools called; source/build/
  schema and A/B corrections passed.
- Baseline scope: exactly 16 authorized paths; `git diff --check` passed; changed
  production modules have no dead imports; protected hashes matched; temporary files
  removed.
- Subagents: 0. Live Goose/provider/model calls: 0. Push/PR/release/deploy: 0.

## Incidents and deviations

- Initial exact Git staging/commit attempt was denied by the sandbox at `.git/index.lock`.
  The index remained empty; the contract-protected `.learnings/**` log was not edited,
  and the same exact stage/commit was retried with bounded Git authority.
- The first PKG-050 focused collection found a local unterminated quote in a new test
  assertion. The assertion was corrected; no production test ran before that fix.
- Two read-only `rg` expressions failed because of an unsupported lookaround and a
  PowerShell quote parse; simplified literal searches succeeded. A large documentation
  patch missed exact context and made no partial edit; it was split into verified patches.
- The first installed-wheel smoke assumed `list_review_records` used the key `records`;
  FastMCP returned the documented `reviews` key. A shape diagnostic called all five tools,
  the harness assertion was corrected, and the complete installed-wheel smoke passed.
