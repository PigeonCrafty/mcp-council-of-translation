READY_FOR_REVIEW

# CAMPAIGN-012-r4 Worker Report

## Control and repository state

- HARNESS_ROLE: `WORKER / MAIN WORKER`
- HARNESS_MODE: `STRICT_CAMPAIGN`
- Contract: `harness/contracts/CAMPAIGN-012-r4.md`
- Contract SHA-256: `29A6453ECD30C15CF204DB5C1B4DA3019632F9CBFE8B8FD222AC0CA7356A0255`
- Exact admitted baseline: `aceac3383b2a597bbf5414362d9b71ac6e601267`
- Final HEAD: `46849c9198213ad6d1e9888e8a0503bb1bccc61c`
- Admission: exact HEAD, empty index, admitted dirty/untracked set, all 15 protected
  hashes, compile PASS and exact `441 passed in 4.31s`.
- Final index: empty. The existing Foreman dirt and user assets remain unstaged and
  unmodified. This report and its ledger remain untracked/unstaged. The exact
  repository-local `.tmp/campaign012-r4-worker` and generated root `build` directories
  were safety-checked, removed after evidence capture, and are absent at handoff.

## Commits and changed paths

Exactly two scoped local commits were created in dependency order:

1. `a2078a462fc6f9d23c1a01d1e4b338764301f6eb` —
   `feat: embed canonical verification receipt JSON`
   - `src/council_of_translation/localization/verification.py`
   - `src/council_of_translation/presentation.py`
   - `src/council_of_translation/tools/review.py`
   - `tests/integration/test_v12_verification_view.py`
   - `tests/unit/test_verification_receipt.py`
2. `46849c9198213ad6d1e9888e8a0503bb1bccc61c` —
   `chore: release canonical receipt fallback 0.12.1`
   - `AGENTS.md`, `README.md`
   - `docs/v0.4-architecture.md`, `docs/v0.4-tool-contract.md`
   - `pyproject.toml`, `src/council_of_translation/__init__.py`
   - `tests/integration/test_tool_surface_v2.py`
   - `tests/integration/test_v10_release_contract.py`
   - `tests/unit/test_persistence_v2.py`, `uv.lock`

The baseline-to-final audit found exactly these 15 authorized paths, with no unexpected
or missing path. Each staged name list and staged diff check passed before commit.

## PKG-073 evidence

The actual pre-edit FastMCP reproduction returned one 838-code-point text block, footer
last, with zero canonical labels and zero JSON fences. The correction now appends, only
for a valid canonical verification receipt, the exact same in-memory receipt object
serialized with `ensure_ascii=False` and separators `(',', ':')`. The frozen Markdown
and review footer precede the non-heading label and one `json` fence; nothing follows
the closing fence. The combined hard cap is 12,000 Unicode code points and overflow
returns a bounded payload-free `ValueError` tool result without save or mutation.

- Affected compile: PASS.
- Receipt, verification-view and dual-channel matrix:
  `135 passed in 1.18s`.
- Text-only A/B/C canonical evidence:
  - A: 3,800 code points; standard; calls/budget `7/13`; publishability/review-needed
    `修改后可发布/否`.
  - B: 3,478 code points; lightweight; calls/budget `4/6`; `可发布/否`.
  - C: 3,980 code points; strict; calls/budget `8/18`; `需人工复核/是`.
- In all three cases, fenced text parsed equal to the structured receipt, had exactly
  five frozen headings, ended at the JSON fence, and contained none of
  `receipt_version`, `calls`, `chief_editor`, `terminal_disposition_check`, or
  `git_commit` as keys.
- Full, metadata, legacy, unavailable, continuation and hostile projections were
  parseable, privacy-safe and under 12,000 code points. The hostile huge-count value,
  private parent sentinel and impossible oversized receipt did not escape.
- Direct purity probe: load/save/model-executor/interaction-gateway counts `1/0/0/0`;
  record mutation `false`. Persisted-byte/timestamp/counter/report controls passed.

## PKG-074 and final verification

- Package/module: `0.12.1`; diagnostic build:
  `verifiable-evidence-council-v10.1`.
- Record Schema `2.5`; receipt Schema `1.0`; exactly five tools; defaults remain
  review-only/auto/auto/summary/full; budgets `6/13/18`; concurrency default/max `3/3`.
- Documentation now states that verification retains structured content and embeds the
  exact compact canonical receipt in the same first text channel for clients that
  ignore MCP structured content. Normal callers still call `review_translation`.
- Focused release/tool/persistence plus PKG-073 matrix:
  `171 passed in 1.35s`.
- Final compile: PASS.
- Complete final suite: `444 passed in 3.98s`; no failures or skips.
- Focused privacy/purity/overflow controls: `4 passed in 0.96s`.
- Golden pytest: `4 passed`; exact production aggregate `24/24`,
  `failed_case_ids=[]`, all eight metrics `1.0`; runtime sampling/elicitation/budget
  `148/4/296`, routing/display calls `0/0`.
- `git diff --check`: PASS. Read-only AST scan across all nine changed Python files:
  zero unused imports.

Normal primary byte controls passed for review, continuation, full, summary and error;
their SHA-256 values were respectively
`8820D283197FD0384DA713AF8CF6A4B00AB234D7FCD744BD083893766240CAE3`,
`D4C1F14B21369907A84E83CB741BAACB125DBC474BF3FD5769792A6242F66EE1`,
`8820D283197FD0384DA713AF8CF6A4B00AB234D7FCD744BD083893766240CAE3`,
`8820D283197FD0384DA713AF8CF6A4B00AB234D7FCD744BD083893766240CAE3`,
and `623F95B141F307E0640A144452398B347DFED14062F7279D0AD3BEF96D05CD8F`.
The canonical label was absent from every normal/error primary path. List and diagnostic
retained their structured-only tool implementations and exact identity assertions.

## Lock, artifacts and installed-wheel smoke

Exact `uv 0.12.3 (507230998 2026-08-07 x86_64-pc-windows-msvc)` used repository-local
cache/tool directories. Canonical refresh and final `lock --check` resolved 78 packages.
`uv.lock` SHA-256 is
`6B5E166D19F9466209C793624D92DE1F33EB254417CD571F653DD0A8B8E932DF`;
revision/package/upload-time counts are `3/78/586`. Its entire baseline diff is the
editable root version `0.12.0 -> 0.12.1`; no dependency, source, hash, edge, format or
other lock entry changed.

Fresh artifacts:

- `council_of_translation-0.12.1-py3-none-any.whl` — 102,738 bytes — SHA-256
  `29D3907AC9B4F3C64245FEEE7487E93E55D98AD98F3D504CA214D2475B1C5B6A`.
- `council_of_translation-0.12.1.tar.gz` — 96,442 bytes — SHA-256
  `FADD8801EF3DD9C357D327E3AE10CFE79007A371944401A499B12AA36C2D7AB4`.

Both archives contained the verification module, version `0.12.1`, normalized Python
range `<3.14,>=3.10`, exact direct dependencies and no `.tmp` member. The isolated
CPython 3.12.9/FastMCP 3.4.7 smoke imported from the wheel environment's
`Lib/site-packages`, called all five tools, and reported exact tool/version/schema/
budget/concurrency identity. Its verification text was one 2,713-code-point block;
footer preceded JSON, five headings remained, compact serialization was exact, text JSON
equaled the structured receipt, the closing fence was terminal, and source content was
absent.

## Protected reconciliation

All contract-listed hashes matched at final verification:

- `harness/features.json` — `50E1A1B10E0A273809F1D0CD689C57F038B73045F78138B1A4BDBF5C0ECA44DC`
- `harness/plan.md` — `8F8D46C5ADD70E6B2259EC005EC60C7618653A8410AC14BF24ADB18804ABCDFF`
- `harness/progress.md` — `73921F878FE5719F219B0F21A116EAB189FAF13AD44C556E763E28EEE1BFEE48`
- Q-014 live contract/review —
  `87369C91AE827C7B64E8956F3CB627ABF87D7B1300AE0764658760D6D8E2B864` /
  `3431A480D126A596C137C08E8728227340754DAED9EC0E0D64DA84F9FB694AAD`
- r3 publication-CI review —
  `CFEA7631F560AB776F5B1E08C36DF3ED75066F3E48BA601DAC923E0F27ECDC99`
- r1/r2/r3 contracts —
  `E4E1CAAFB5E6E08729B5E726C5144793D3BE7E029699AA24984F37E97D587548` /
  `1B628133452A89F1BA4F47798F124B0E07C9E25E4B994C52834D65A1FAFCB615` /
  `E6EF7A7CC8468124E85CAA87C649141D2947D25506F6A00C6901F94487928161`
- r1/r2/r3 reviews —
  `F0E3F8BB0A8D16EF51602F0352C9703646658BC2993A39BB6F1AFB064A08CEA8` /
  `FD74C91C3275FDE662A49D2DAB31051876F7718857DA7239DF0376BE23B08009` /
  `9948709C712A5F39738BA7DA13692CCD818C3E27C833D9571AC835B913956415`
- r1/r2/r3 Worker reports —
  `43966E75BF6348B3B144ECA8BC517516DCC499AF9238B7288B8306B7F3760ECB` /
  `54746D80619E5E4C35A69CA514381F0EBECF3E6E52B0D4050024B44BCB412A44` /
  `BBFA01ABAE507C7DBD1D89A93E96BBD571E934DA754BE1489C908944333652D8`

Per contract, `.learnings/**`, `reviews/**`, `myTest/**`, `dist/**` and the independent
audit Markdown were not traversed or hashed. They were not modified, staged or committed.

## Skips, counts, deviations and remaining risk

- Skipped by contract: live Goose/provider/model calls; push/PR/release/publication/
  deployment; Goose/configuration/credential changes; forbidden asset traversal.
- Test skips: `0`.
- Subagents: `0` (delegation forbidden).
- Authority escalations: `4` (two scoped staging operations, two local commits).
- Dependency-operation invocations: `6` (exact uv acquisition/version check, lock
  refresh, build, isolated venv, isolated install, final lock check).
- Live Goose/provider/model calls: `0`; remote Git/GitHub calls: `0`; push/PR calls: `0`.
- Corrected local command issues: missing nested pytest basetemp parent; default `rg`
  lookahead; normalized archive Python-range ordering; FastMCP 3.4.7 tool-list API; AST
  treatment of `__future__`. Each corrected rerun passed. The self-improvement skill was
  consulted, but its `.learnings/**` target was contract-protected; no such asset was
  read or written.
- Remaining risk: normal live Goose text-only behavior was deliberately not called in
  this Worker run. The actual FastMCP and isolated-wheel text-only evidence is ready for
  Foreman/Q-014 independent verification. No acceptance or publication claim is made.

Worker report: `harness/reports/CAMPAIGN-012-r4-worker.md`  
Ledger: `harness/reports/CAMPAIGN-012-r4-ledger.md`
