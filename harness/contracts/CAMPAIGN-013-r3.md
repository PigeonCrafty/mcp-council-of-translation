# CAMPAIGN-013-r3 Contract

## Authority and mode

- Harness role: `MAIN_WORKER`
- Harness mode: `STRICT_CAMPAIGN`
- Foreman acceptance authority: exclusive
- Parent Campaign: `CAMPAIGN-013-r2`
- Foreman review: `harness/evaluations/CAMPAIGN-013-r2-review.md`
- Original product baseline: `44b1969677cd6b1fda63047ca514aede6609bdad`
- r3 admission baseline / required HEAD:
  `b01461b792ecb5eeda20229d47a404015ec6910c`
- Product target: package/module `0.13.0`
- Diagnostic build: `calibrated-evidence-council-v11`
- Review Schema: `2.6`
- Verification receipt Schema: `1.1`

Use `C:/Users/GeZhu/.agents/skills/pigeon-harness/SKILL.md` and its Worker protocol.
This is a bounded documentation correction, not a new product-design iteration.

## Objective

Preserve the complete five-commit CAMPAIGN-013-r2 implementation and make exactly one
additional commit that aligns the current V0.13 architecture description with the
implemented verification receipt Schema 1.1, backed by an existing release-contract
regression assertion.

## Admission

Before editing:

1. Confirm HEAD is exactly `b01461b792ecb5eeda20229d47a404015ec6910c` and the Git
   index is empty.
2. Confirm the five preserved Campaign commits are present in order:
   `6a07f4e`, `393b947`, `613faee`, `2ed6973`, `b01461b`.
3. Confirm the contract SHA-256 supplied by the Foreman matches this file.
4. Confirm each protected asset below matches exactly.
5. Run `python -m compileall -q src tests` and the complete regression with a unique,
   repository-local pytest basetemp. Admission must pass at least the accepted r2
   baseline of 480 tests.
6. If admission, hashes, HEAD, index or the stated one-line defect differ, stop and
   report `BLOCKED` without editing.

## Frozen correction

The only product-authoritative defect is this current statement in
`docs/v0.4-architecture.md`:

`It performs one load and deterministically derives a receipt-schema 1.0 wrapper without`

Change only the schema value in that statement to `1.1`. The historical `v0.4-*`
filename remains unchanged for path stability. Do not rewrite surrounding architecture
prose.

Extend the existing V0.13 release-contract test in
`tests/integration/test_v10_release_contract.py` so it reads the authoritative
architecture document and proves:

- the current wrapper statement contains `receipt-schema 1.1 wrapper`; and
- the stale exact phrase `receipt-schema 1.0 wrapper` is absent.

Prefer adding these assertions to an existing V0.13 release test so the test count need
not change. Do not introduce a broad documentation scanner or infer historical-version
rules from filenames.

## Authorized paths

The implementation commit may change exactly these two paths:

- `docs/v0.4-architecture.md`
- `tests/integration/test_v10_release_contract.py`

The Worker may also create, but must leave untracked and unstaged:

- `harness/reports/CAMPAIGN-013-r3-worker.md`

No ledger is required. No other product, test, documentation, Harness, learning,
temporary, package, dependency, workflow or lock path is authorized.

## Preserved invariants

- Preserve all five r2 commits and all production bytes at the r3 baseline.
- Preserve exact five public tools, review-only behavior, frozen defaults, budgets
  6/13/18, concurrency 1 through 3 and all 15 routing profiles.
- Preserve package/module 0.13.0, build `calibrated-evidence-council-v11`, Review Schema
  2.6 and receipt Schema 1.1.
- Preserve the decision-support truth table, one-way safety tightening, compatibility,
  receipt projection, primary presentation and Golden corpus semantics.
- Preserve `uv.lock` byte-for-byte. Do not refresh, edit, sync or rebuild it.
- Do not rebuild wheel/sdist or create an isolated environment. r2 Worker and independent
  Foreman fresh-build/archive evidence already cover unchanged packaged inputs.
- Do not access or modify `.learnings/**`, `.tmp/q012/**`, `reviews/**`, `myTest/**` or
  admitted user/Foreman assets outside the exact admission hash operations below.
- Do not call live Goose, providers or models. Do not push, open/update a PR, publish,
  release or deploy.

## Protected assets

Verify these SHA-256 values at admission and again before handoff:

| Path | SHA-256 |
| --- | --- |
| `harness/features.json` | `E10B63ED502441871CEB557F21788D57F9D966610865E4F4A096399A0433B971` |
| `harness/plan.md` | `69CADDDDD5F82734523026E4E24D297C14BC602B772884A43189CDB5058E3205` |
| `harness/progress.md` | `02913881FC3E1772ACF719D032B55DCA2F24A4B8E39704FBB496F84ABC037D2B` |
| `harness/evaluations/CAMPAIGN-013-r2-review.md` | `FD9183DC8E3306F44D6EB18CADE4B62C2CE973D6E3573173D2E33CED5E25F27E` |
| `harness/evaluations/NEXT-CAMPAIGN-013-ASSESSMENT.md` | `60570A7A7A8476E8B74F1CF32EB3999229524B1778DFDE9DABCA6C4746A5EDFA` |
| `harness/evaluations/CAMPAIGN-013-r1-review.md` | `D02E62E52095DC238BC0CE58ED2BDB9808206273A93D00187CC4DA14B24C3602` |
| `harness/contracts/CAMPAIGN-013-r1.md` | `D11C672105A740BFD2413C9794878BF6BD1FB7011C3407406ED45B50B20A29B5` |
| `harness/contracts/CAMPAIGN-013-r2.md` | `0FD5641A76FB859C14FB4D331B00E38931AEA98589C5D580F0E675DB4537B4E2` |
| `harness/reports/CAMPAIGN-013-r1-worker.md` | `11780C8CD07FA461C5DA318DD9EB7AB397BCD67356C892AB6DE79ED79C0916D8` |
| `harness/reports/CAMPAIGN-013-r1-ledger.md` | `70EC662C82F449FD33773CB7B5FC601E82E3BC1460BEC2237FCA9350C6EF72B3` |
| `harness/reports/CAMPAIGN-013-r2-worker.md` | `278A619A26002D0306D2A716C8142E7019F6559698B17EABF4845C7B6D8AB42B` |
| `harness/reports/CAMPAIGN-013-r2-ledger.md` | `043C2DEE22F17BFA641EFEDBF5E1A68F4B11CA141E4947B6411AA320F3111FDA` |
| `harness/evaluations/CAMPAIGN-012-q014-live-r2-review.md` | `6207A0DDC7798B61C8B2003FE492BE7312186FC0F781E397730C12293CC6EE6A` |

## Required implementation and commit

1. Apply the exact architecture wording correction.
2. Add the bounded regression assertion.
3. Run the verification below.
4. Stage only the two authorized paths and create exactly one commit with subject:
   `Align V0.13 receipt architecture`
5. Leave the index empty and the Worker report untracked/unstaged.

## Required verification

- `python -m compileall -q src tests`
- Focused release test:
  `python -m pytest -q tests/integration/test_v10_release_contract.py`
- Complete regression with a unique repository-local basetemp; no regression below the
  admitted 480 passing tests is allowed.
- Exact counterexample search proving the stale current phrase is absent and the 1.1
  phrase is present in the architecture document.
- Original r3-baseline-to-final `git diff --check`.
- Exact baseline-to-final scope: only the two authorized paths.
- `uv.lock` byte identity and all protected hashes.
- Empty Git index and no uncommitted implementation edits.

If a required check fails or any extra path is needed, stop and report `BLOCKED`; do not
expand scope, change production or weaken a test.

## Worker handoff

Write `harness/reports/CAMPAIGN-013-r3-worker.md` with:

- contract SHA-256;
- baseline and final HEAD;
- the unique commit hash and exact two-path scope;
- before/after wording counterexample;
- compile, focused and full regression results;
- diff, lock, protected-hash and index evidence;
- skipped-check, subagent, authority, dependency, live-call and remote-mutation counts;
- remaining risk; and
- `READY_FOR_REVIEW` or `BLOCKED` without claiming acceptance, publication or Q-015.
