# CAMPAIGN-011-r1 Worker Report

## Terminal status

`BLOCKED`

PKG-057 through PKG-061 are implemented, independently reverified by the Main Worker,
and committed in dependency order. PKG-062 reached a mandatory contract stop condition:
truthful new runtime records use Schema 2.5, but
`tests/integration/test_v08_presentation_invariants.py::test_literal_v22_record_runtime_and_role_invariants`
asserts the obsolete literal `2.4`. That tracked test is not in the contract's exhaustive
allowed-test list. Passing the complete suite therefore requires either authority to update
that path or an incorrect production regression to Schema 2.4. No such regression was made.

## Control and admission

- Role/mode: `WORKER / MAIN WORKER`, `STRICT_CAMPAIGN`
- Contract: `harness/contracts/CAMPAIGN-011-r1.md`
- Required/observed baseline: `610eae8e7c2df31fd9052b0ae76a2d718805f28d`
- Required/observed contract SHA-256:
  `9EB1317585B0BC999AA9615D37DAC86992EC31BCBD87B0FC45330DB9A39D83E0`
- Admission index: empty
- Admitted protected dirty/untracked assets: modified `harness/plan.md`,
  `harness/features.json`, `harness/progress.md`; untracked `.learnings/`, the Campaign
  contract, the audit report and `reviews/`. None overlapped an authorized implementation
  path.
- Python: `3.12.9`
- Admission compile: `python -m compileall src tests` -> exit 0
- Admission suite:
  `.venv\Scripts\python.exe -m pytest -q --basetemp=.tmp/campaign011-r1-admission`
  -> `294 passed in 3.85s`
- Raw live records were not read, copied or modified.

Protected files retained their admission hashes:

- `harness/plan.md`: `75F2FAA2FDD00402A06393E8DDAFC29332451E26F8D0B1A23A8CE3FCB6A1F9EC`
- `harness/features.json`: `C31F5D33DC2ACFF72A735FDB7874332E5BA52896E28F5EA0C11A8F267EBB01B1`
- `harness/progress.md`: `6CB0D5263AC258DC361D18B498F3F6A39D9D1C63B90C22E1BC503BCC2A9DAEDB`
- Campaign contract: `9EB1317585B0BC999AA9615D37DAC86992EC31BCBD87B0FC45330DB9A39D83E0`
- Audit report: `B48073E063C4C9F34E0B6B4DAE94E80079EAAAD3B2F8E273DD60B2F25F6ABD76`
- `.learnings/ERRORS.md`: `48800E1BA3D7BC7A709F0194C353AC802B1D015D750B408D5570A4822DF78F91`
- `.learnings/LEARNINGS.md`: `F2A49AE9E08483F777D4145CB1FC9AA734CD3A2877B2F17A1C1DFFC5E2DCD4C8`
- `reviews/20260810_145151.json`: `BA2607DEAF9BA440C514FB3D6E5AB34197EDEFA7CC04D9F83859A6EDE4E8FC73`

## Commits and package evidence

Final committed HEAD is `1ae3a7419c1eaeb293a944a49d0873cdf95952e1`.
The index is empty. Five of the required six package commits exist:

1. PKG-057 — `29e28d73085219a07ddf0756a2f8a7f9c24b9db3`
   `Add deterministic routing profiles`
   - Added bounded routing profile/reason types, conservative historical defaults and
     the explicit 15-profile registry.
   - Focused verification: `19 passed in 0.23s`; scoped diff check passed.
2. PKG-058 — `43c6613c026bff76ccbb6ccfaea26fd6dba9c4ed`
   `Add legal risk reviewer portfolios`
   - Added exact legal-risk 4/6/7 portfolios, applicable product/UX/risk metadata and
     universal no-invented-law/no-legal-advice boundaries; retained nine definitions.
   - Focused verification: `17 passed in 0.15s`; scoped diff check passed.
3. PKG-059 — `cc2d4bdbe5a21f7600cf3bee34af07e3eb2527d2`
   `Persist routing provenance in schema 2.5`
   - Added V2.5 parsing/writes, compact/full/metadata bounded provenance, immutable
     continuation copying and exact call-budget regressions.
   - Focused verification: `42 passed in 1.05s`; legal clean calls `4/6/7`, standard
     deepest path `6+3+1+3=13`, strict `7<=18`, zero routing elicitation, and parent
     plan/file immutability covered; scoped diff check passed.
4. PKG-060 — `fd5589b32b18f0c970cbfc83a107301c0bcc90b9`
   `Render concise legal risk routing`
   - Added fixed natural Chinese route summaries, risk-role lens correction, bounded
     internal-route sanitization and section-aware whole-line capping.
   - Focused verification: `21 passed in 0.23s`; five sections, clean `<=1200`, hostile
     `<=3200`, material safety lines, privacy, verdict-last and render non-mutation covered;
     scoped diff check passed.
5. PKG-061 — `1ae3a7419c1eaeb293a944a49d0873cdf95952e1`
   `Expand golden corpus for legal risk`
   - Preserved the original 18 cases at canonical SHA-256
     `2b00acceaa6b34563686a65b3256bbbead1b26cdd20bd5b62b91e7c4e017120d`
     and appended the exact six legal-risk cases.
   - Focused verification: `22 passed in 0.55s`; exact 24/24, sampling calls `148`,
     elicitation calls `4`, budget sum `296`, routing/display calls `0`, and all eight
     aggregate accuracy/rate metrics `1.0`; scoped diff check passed.
6. PKG-062 — no commit; blocked during release migration.
   - Authorized unstaged edits currently exist in `AGENTS.md`, `README.md`,
     `docs/v0.4-architecture.md`, `docs/v0.4-tool-contract.md`, `pyproject.toml`,
     `src/council_of_translation/__init__.py`,
     `src/council_of_translation/tools/review.py`,
     `tests/integration/test_tool_surface_v2.py`, and
     `tests/integration/test_v10_release_contract.py`.
   - Focused release verification:
     `.venv\Scripts\python.exe -m pytest -q tests/integration/test_tool_surface_v2.py tests/integration/test_v10_release_contract.py --basetemp=.tmp/campaign011-pkg062-releasea`
     -> `16 passed in 1.18s`.
   - Full suite:
     `.venv\Scripts\python.exe -m pytest -q --basetemp=.tmp/campaign011-pkg062-fulla`
     -> `304 passed, 3 failed in 3.90s`.
   - Fatal failure: the unauthorized V0.8 presentation test expects new runtime
     `schema_version == "2.4"`; actual truthful value is `2.5`.
   - The other two failures are allowed PKG-062 identifier expectations in
     `tests/unit/test_persistence_v2.py` still naming version `0.10.2` and build v8.2.
     They were not edited after the mandatory stop condition fired.

Committed baseline-to-HEAD paths are limited to the authorized routing, persistence,
presentation, evaluation and focused-test/fixture paths listed in the ledger. No protected
asset is present in any commit.

## Skipped verification and artifacts

The following required PKG-062/Campaign checks were not run after the mandatory stop:

- pinned `uv 0.12.3 lock --refresh` and its exact root-only lock-diff proof;
- release package commit;
- final compile and passing complete regression;
- final named-test replay and deterministic probe bundle;
- baseline-to-final Campaign diff/scope/dead-import audit;
- fresh sdist/wheel build, archive inspection, hashes and isolated Python 3.12 / FastMCP
  3.4.7 five-tool wheel smoke.

`uv.lock` is untouched. No build artifacts were produced. These are materially skipped:
the Campaign cannot be handed off as review-ready without resolving the test-path authority
conflict and completing PKG-062.

## Delegation, authority and external state

- Subagents: 2, both bounded read-only analysts. One covered PKG-057–059 and one covered
  PKG-060–061. The Main Worker inspected both returned proposals; neither produced a diff.
- Approval/escalation requests: 5, each limited to one scoped local package commit.
- Dependency operations: 0.
- Live Goose/provider/model calls: 0.
- Credentials requested: 0.
- Pushes, PRs, releases, deployments and other external mutations: 0.

The initial read-only tool dispatch used a nonexistent nested tool name, one PowerShell
regex command was under-escaped, and one inspection used Bash brace expansion in
PowerShell. All failed before mutation and were rerun safely. Self-improvement files were
not changed because `.learnings/**` is protected; the ledger records the incidents.

## Required resolution

Foreman action is required: either issue a revision contract authorizing the single stale
test path `tests/integration/test_v08_presentation_invariants.py` (and the already allowed
PKG-062 paths), or otherwise reconcile the explicit Schema 2.5 requirement with that
test's hard-coded Schema 2.4 expectation. The Worker has not self-accepted any package,
Campaign, feature, publication or Q-013 gate.
