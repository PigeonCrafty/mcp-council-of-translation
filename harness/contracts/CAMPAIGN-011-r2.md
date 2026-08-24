# Campaign Contract: CAMPAIGN-011-r2

## Control

- Role: `WORKER / MAIN WORKER`
- Mode: `STRICT_CAMPAIGN`
- State: `ASSIGNED`
- Repository: `C:\Users\GeZhu\MyMCP\mcp-council-of-translation`
- Exact committed baseline: `1ae3a7419c1eaeb293a944a49d0873cdf95952e1`
- Baseline subject: `Expand golden corpus for legal risk`
- Parent contract: `harness/contracts/CAMPAIGN-011-r1.md`
- Parent review: `harness/evaluations/CAMPAIGN-011-r1-review.md`
- Parent decision: `CHANGES_REQUESTED`
- Required report: `harness/reports/CAMPAIGN-011-r2-worker.md`
- New ledger: not required; cite the r1 ledger and report the r2 delta completely
- Commit policy: exactly one scoped local PKG-062 commit after all checks pass
- Subagents: forbidden; this is one bounded release correction
- Push, PR, tag, release, deployment and live Goose/provider/model calls: forbidden

## Outcome

Complete only PKG-062/F-052 for V0.11.0. Preserve the five committed r1 packages and
their evidence. Correct three obsolete release assertions, finish the already admitted
release intermediate, refresh only the editable root version in `uv.lock`, and provide a
passing complete regression plus fresh package and isolated-wheel evidence.

This revision changes no product design. It does not authorize a different routing matrix,
schema, role, budget, concurrency policy, output contract, public tool or dependency.

## Admission and preserved state

Admission must satisfy all of the following before any edit:

1. `HEAD` is exactly `1ae3a7419c1eaeb293a944a49d0873cdf95952e1` and the Git index is empty.
2. The nine unstaged PKG-062 files exist with these exact SHA-256 hashes:

| Path | SHA-256 |
| --- | --- |
| `AGENTS.md` | `D8B1FB1DBA99752E68C30553CF917D89589828B039B865D3A637F188E33C0858` |
| `README.md` | `06F186621070BCC95B5A0B5C610E747DEE78D5BD1DEC59C4DC1BA416F2407963` |
| `docs/v0.4-architecture.md` | `21617CEED67A4015A982F4ED1C3A5FED19BC3DFD452922657D0BEECEE2F73932` |
| `docs/v0.4-tool-contract.md` | `4115165BF6F4EB8F50F35F3FBF5DEBC1A06298F6C87F44DDE7E443295EB462BE` |
| `pyproject.toml` | `8041F32FE3D8963ED1196DEFA8D521FFCEF8161985D68F5C964849204B68CF12` |
| `src/council_of_translation/__init__.py` | `42620AE9F4826A23F9E16F3D96587C24DE6573672A3847944B33CA0571585E4C` |
| `src/council_of_translation/tools/review.py` | `AE6274BEC32C7B4620169EDF26D26BF6906AB9861F5843F58624B5020D852A30` |
| `tests/integration/test_tool_surface_v2.py` | `17175DD514D8FEA1BB0F28505BE47B80992FD9610362A7F55D23A5D31AC8575D` |
| `tests/integration/test_v10_release_contract.py` | `0FDCF287A4E9DCA1A1D44E0EC3EE64F1755C052323AB64F127B91E1ED6D0E16C` |

3. `uv.lock` is byte-identical to SHA-256
   `31F0173F9325A4CA1C5BF95BB281B75E00374C8A241A19DFC38AB39C95F5347D`,
   revision 3, 78 packages and 586 `upload-time` entries.
4. The r1 evidence assets remain exact:
   - contract `9EB1317585B0BC999AA9615D37DAC86992EC31BCBD87B0FC45330DB9A39D83E0`;
   - ledger `27EDC3D89AE4221C6A3D0219A779F6E0AE89730063ACBD45C78981BDFC0A0936`;
   - Worker report `F60C1C068B8891F18735A9F21C9BCAA2D0328BCD409FBAB69F6F7D0507992810`;
   - Foreman review `04CB5A50B7C5EA79489D7C34AA210C1A583E87C1AC46627E54D1BE5BA9A65865`.
5. Foreman/user assets are protected and must not be modified:
   - `harness/plan.md` `0BAA9B05583FD9B94E913D8478E008EFF8F198C4D933D16F024FFAD7237A39EC`;
   - `harness/features.json` `C31F5D33DC2ACFF72A735FDB7874332E5BA52896E28F5EA0C11A8F267EBB01B1`;
   - `harness/progress.md` `65FB7F6D95690E8ED003AA70D6A39F086447B7150FAFCFFB70E806102AA4ED1D`;
   - `.learnings/**`, `reviews/**`, `myTest/**`, the independent audit Markdown and all
     other existing untracked/user assets.

The Worker may read the named r1 Harness evidence. It must not read raw `reviews/**`,
`.learnings/**`, `myTest/**` or user test output into product or report content.

## Exact correction

### 1. Migrate the omitted current-runtime assertion

Authorize `tests/integration/test_v08_presentation_invariants.py` solely to correct
`test_literal_v22_record_runtime_and_role_invariants` so a newly executed V0.11 review
expects Schema `2.5`. Historical fixture/read compatibility assertions must remain 2.4 or
older where the fixture itself is historical. A historical filename does not make a newly
created runtime record historical.

### 2. Finish release-identifier assertions

Authorize `tests/unit/test_persistence_v2.py` solely to update the two parametrized
new-write expectations from package `0.10.2` / build `evidence-value-council-v8.2` to
package `0.11.0` / build `risk-coherent-council-v9`. Renaming the obsolete test function
to describe current new-write behavior is allowed but not required. Do not weaken any
privacy, full/metadata, historical-read or path-safety assertion.

### 3. Retain and verify the admitted release intermediate

The nine admitted PKG-062 files already implement the authorized migration to:

- package/module `0.11.0`;
- diagnostic build `risk-coherent-council-v9`;
- write schema `2.5`;
- authoritative V0.11 routing/documentation text.

Inspect them, make no unrelated prose or API changes, and include them in the single
PKG-062 commit only after all required checks pass.

### 4. Canonically refresh the lock

Use repository-local `UV_CACHE_DIR` and `UV_TOOL_DIR` below `.tmp/`. Verify exact uv
`0.12.3`, then invoke:

```powershell
uv tool run --from uv==0.12.3 uv --version
uv tool run --from uv==0.12.3 uv lock --refresh
```

The only accepted `uv.lock` diff is the editable root package version
`0.10.2 -> 0.11.0`. Revision 3, 78 packages and 586 upload-time entries must remain.
No manual lock edit, restore-from-another-commit, format downgrade or alternate lock flag
is authorized. Stop if canonical refresh produces any additional drift.

## Authorized paths

Only these paths may differ from baseline in the r2 PKG-062 commit:

- `AGENTS.md`
- `README.md`
- `docs/v0.4-architecture.md`
- `docs/v0.4-tool-contract.md`
- `pyproject.toml`
- `src/council_of_translation/__init__.py`
- `src/council_of_translation/tools/review.py`
- `tests/integration/test_tool_surface_v2.py`
- `tests/integration/test_v10_release_contract.py`
- `tests/integration/test_v08_presentation_invariants.py`
- `tests/unit/test_persistence_v2.py`
- `uv.lock`

The only Worker evidence path is untracked and unstaged
`harness/reports/CAMPAIGN-011-r2-worker.md`. All other paths are forbidden.

## Frozen acceptance invariants

- Exact public tool order remains:
  `review_translation`, `continue_review`, `view_review_record`,
  `list_review_records`, `get_server_info`.
- Default output remains `review_only`; `suggested_translation` remains absent/null unless
  the caller explicitly requests `full_rewrite`.
- Budgets remain 6/13/18. Independent-review concurrency remains default/max 3 with only
  1/2/3 accepted.
- Schema is exactly 2.5 for new writes; V1 and V2.0 through V2.4 remain readable without
  rewriting historical records.
- Legal-risk portfolios remain 4/6/7 and non-legal profiles remain unchanged.
- Standard deepest path remains exactly `6+3+1+3=13`; routing/display add zero sampling
  and zero elicitation.
- Primary output remains exactly five sections, clean target <=1200, hard cap <=3200,
  internal IDs hidden and chief disposition last.
- Golden remains exact 24/24 with all eight aggregate metrics 1.0.

## Required verification

Run and report at minimum, with unique workspace-local basetemps:

```powershell
python -m compileall src tests
python -m pytest -q tests/integration/test_v08_presentation_invariants.py tests/unit/test_persistence_v2.py
python -m pytest -q tests/integration/test_tool_surface_v2.py tests/integration/test_v10_release_contract.py
python -m pytest -q tests/unit/test_roles_v2.py tests/integration/test_v11_routing.py tests/integration/test_v24_golden_corpus.py tests/integration/test_v24_presentation.py
python -m pytest -q
uv tool run --from uv==0.12.3 uv lock --check
git diff --check 1ae3a7419c1eaeb293a944a49d0873cdf95952e1..HEAD
```

Then:

1. build fresh sdist and wheel from the final committed tree;
2. inspect both archives for V0.11 source, metadata and the corrected tests where packaged;
3. install the wheel into an isolated Python 3.12 environment with FastMCP 3.4.7;
4. prove imports come from isolated `site-packages`;
5. call all five registered tools and verify version/build/schema, defaults, budgets,
   concurrency and dual-channel human-tool results;
6. audit baseline-to-final paths, commit contents, index, untracked report and all protected
   hashes.

## Commit and handoff

- Create exactly one commit with subject equivalent to `Complete V0.11 release migration`.
- Do not amend, rebase, squash or otherwise rewrite the five preserved r1 commits.
- Leave the Git index empty and the r2 Worker report untracked/unstaged.
- In chat begin with exactly `READY_FOR_REVIEW` or `BLOCKED`, then report the contract hash,
  baseline/final HEAD, commit, exact paths, all test/build/artifact evidence, lock diff,
  protected reconciliation, skipped checks and operation counts.
- Do not claim Campaign, feature, publication or Q-013 acceptance.

## Stop conditions

Stop immediately if admission hashes differ; any additional production/test/doc path is
required; production would need to return Schema 2.4; lock drift exceeds the one root
version line; a dependency/public tool/role/budget/profile/output contract must change; or
completion requires credentials, live provider/Goose, push, PR, release or deployment.

