# Campaign Revision Contract: CAMPAIGN-014-r2

## Control

- Harness role: `MAIN WORKER`
- Harness mode: `STRICT_CAMPAIGN`
- Campaign: `CAMPAIGN-014-r2`
- State: `ASSIGNED_REVISION`
- Repository: `C:\Users\GeZhu\MyMCP\mcp-council-of-translation`
- Revision baseline HEAD: `742128a1dfc2282d7aad4ee016d37ff94922c9ca`
- Original Campaign baseline: `4f976c2764a463dceb403084fa3faead5300211e`
- Published product baseline: `95d90cf383d045778ce61afaa50dbcec199579ce`
- Admitted local `origin/main`: `bcdb0e2bc282e907e975b43882906872913f6bec`
- Parent contract: `harness/contracts/CAMPAIGN-014-r1.md`
- Foreman review: `harness/evaluations/CAMPAIGN-014-r1-review.md`
- Product target: `0.13.1`
- Diagnostic build target: `truthful-boundaries-council-v11.1`
- Review/receipt/evaluator Schema targets: `2.6` / `1.1` / `2.1`
- Acceptance authority: Foreman only
- Execution ledger: `harness/reports/CAMPAIGN-014-r2-ledger.md`
- Worker report: `harness/reports/CAMPAIGN-014-r2-worker.md`
- Commit policy: preserve the seven existing PKG-080 through PKG-086 commits and create
  exactly one new scoped commit for PKG-087; the complete Campaign must end with exactly
  eight package commits from the original baseline

This revision incorporates the complete r1 contract except where this document
explicitly overrides admission state, Worker evidence paths, commit count, cleanup scope
and the test allowlist. Every frozen architecture rule, package acceptance criterion,
non-goal, verification requirement, authority boundary and stop condition from r1
remains binding.

## Revision outcome

Finish the already-implemented V0.13.1 audit-remediation Campaign without weakening or
reworking PKG-080 through PKG-086. r1 correctly stopped because one persistence unit-test
file outside its allowlist contains two stale V0.13.0/v11 release assertions. r2 adds
only that path, admits the exact PKG-087 release intermediate and requires the skipped
final verification and artifact evidence.

## Admission and exact intermediate

Start only if all of the following are true:

1. `HEAD` is exactly the revision baseline and local `origin/main` is exactly the
   admitted governance ref. Do not fetch or mutate remote state.
2. Git index is empty, verified through the exit code of
   `git diff --cached --quiet`.
3. The seven commits after the original baseline are exactly, in order:
   `ed1f1ec54b730f6a2bf44e73214d36c1e4ec55c8`,
   `2cad51702a77545a4e78419aac99142541f63261`,
   `651d97f0d6ad8ce750f96a6a6c51ecbded29193a`,
   `0208badaeaab3f2eec05bd73f8bd8f404015d7dd`,
   `a523283efa5604dd49331118e941d68a7b851445`,
   `5ba1db58ba0075d5f3eff7e3d96ab6ef77b949e9` and
   `742128a1dfc2282d7aad4ee016d37ff94922c9ca`.
4. Their combined diff contains exactly the 21 paths reported by r1, all inside the r1
   allowlist, and `git diff --check` passes.
5. The only uncommitted product/package/documentation intermediate is the following
   exact PKG-087 state; verify every SHA-256 before editing:

| Path | SHA-256 |
| --- | --- |
| `AGENTS.md` | `F3878FDF4B43DA8CD0C96349A192C6C6EEE564034A63157ABC06FA10F71DE306` |
| `README.md` | `FDA09C7D57A6BAE7DD962E6A5917EBC7839E87A7B4782EA810B89665AAA0CC9F` |
| `docs/v0.4-architecture.md` | `1F56197A1873E0092ECE408F7DEEBD46EC6899D058B98B13393EBDBD861AEE0A` |
| `docs/v0.4-tool-contract.md` | `49664CC290A5CE66E1C3A80CBE2B6624217C9C62AF8D5D3F24B1837B163D2828` |
| `pyproject.toml` | `29F7096257F0D34886B370793FAD208AF8A437BA32B3124410C1CC1486E525A0` |
| `src/council_of_translation/__init__.py` | `F098F514E41F0827D0D353D4EF8BDB67F3C11E08F65521F4F1B8A00E0C32D884` |
| `tests/integration/test_v10_release_contract.py` | `104041DED121392B23889CB21C78FFF80A988F1A8F99CEC302EC8EF940500385` |
| `uv.lock` | `E7E4E44A19A3A7F1813EE3B5CFDC5814A70BF29C71CD5115582AF4E64A352E00` |

6. Compile passes. A focused replay of `tests/unit/test_persistence_v2.py` and
   `tests/integration/test_tool_surface_v2.py` reproduces exactly `31 passed, 3 failed`;
   the failures are the `full` and `metadata` parameterizations of
   `test_new_write_persists_truthful_v0130_runtime_and_version_identifiers` and
   `test_server_info_and_versioned_defaults`.
7. Every protected hash below matches exactly.
8. The SHA-256 of this contract matches the launch prompt.

### Protected hashes

| Path | SHA-256 |
| --- | --- |
| `harness/features.json` | `A281AF219307A79B2D8D5F376802422488745815AE32E213E94CE13E20F58BC1` |
| `harness/plan.md` | `8C03EE54FE36C85C4D3C06C9ACC7E872D0FD1F2C8A35E995C8483213238DA957` |
| `harness/progress.md` | `1946E7864D89A41D428E1F535EC9861AC770A67A1DA1A9D4B357CE7985252032` |
| `harness/evaluations/CAMPAIGN-014-r1-review.md` | `844EFF7CC40D5C87B337C22899460D0B2C3A74E5141CB3313CAC133C6C2F257A` |
| `harness/contracts/CAMPAIGN-014-r1.md` | `4FBCF691DF9702587EC6A5D2F5FB1215D4440D3A6229ACBA1D4A969C7F09B2A0` |
| `harness/reports/CAMPAIGN-014-r1-worker.md` | `5DE10A22E34E07CB8F5CFCED842215A6B4BF74439CB95BFF8D972C99E59969A1` |
| `harness/reports/CAMPAIGN-014-r1-ledger.md` | `2BE0435A7B6A0CFA6867F0F9B7E1BA4F872E8E0B19BFD9006D3BC08D0839615C` |
| `mcp-council-of-translation-v0.13-independent-audit.md` | `0B608DF956448C92AC4112452709129FB45B27478C0F571118660DAA89FBA179` |
| `mcp-council-of-translation-audit-and-upgrade-recommendations.md` | `B48073E063C4C9F34E0B6B4DAE94E80079EAAAD3B2F8E273DD60B2F25F6ABD76` |
| `harness/evaluations/CAMPAIGN-013-INDEPENDENT-AUDIT-FOREMAN-RESPONSE.md` | `7440C47877D2C76313F1848ABCF65269A1A8FD089CE4A3FE9AA4793907903CD4` |
| `harness/evaluations/NEXT-CAMPAIGN-014-AUDIT-REMEDIATION-ASSESSMENT.md` | `A7D4F770C6F7660964CB926F44A62D3F540F0A3B43C388E1D64B886B900A1529` |
| `docs/v0.13-stage-development-report.md` | `DA03138EB0E07F27C1FFEF1F1BA044DB13D590427BC7F8EA3CB53D26168C6C94` |
| `.github/workflows/ci.yml` | `0B37598E7D53D27B04E5524BAA4D46A2AB69D5E2607A5FF9F0437512CF8EF645` |

Existing Foreman/user dirty and untracked assets are admitted. Preserve them exactly.
Do not read, traverse, copy, hash, modify, delete or stage `.learnings/**`, `reviews/**`
or `myTest/**`. Do not modify or stage any Harness path except the two new r2 report
paths. Stop before edits on any admission mismatch.

## Frozen correction

The V0.13.1 production identifiers in the admitted PKG-087 intermediate are correct.
The three failures are test migration debt, not evidence for a production workaround.

1. In `tests/unit/test_persistence_v2.py`, rename the V0.13.0-specific test accurately
   and update only its package/build expectations to `0.13.1` and
   `truthful-boundaries-council-v11.1` for both `full` and `metadata` history modes.
2. Preserve its schema, round-trip, metadata privacy and loaded-record assertions.
3. In `tests/integration/test_tool_surface_v2.py`, update only the stale package/module/
   build expectations. Preserve every public-tool/default/budget/concurrency assertion.
4. Do not add version-conditional production behavior, compatibility shims, skips,
   deselection, xfail, retry or alternate release identifiers.

## Allowlist override

All r1 authorized paths remain authorized for verification. Add exactly this test path
for the bounded correction:

- `tests/unit/test_persistence_v2.py`

For new edits in r2, PKG-087 is restricted to exactly these ten paths:

- `AGENTS.md`
- `README.md`
- `docs/v0.4-architecture.md`
- `docs/v0.4-tool-contract.md`
- `pyproject.toml`
- `src/council_of_translation/__init__.py`
- `tests/integration/test_v10_release_contract.py`
- `tests/integration/test_tool_surface_v2.py`
- `tests/unit/test_persistence_v2.py`
- `uv.lock`

No earlier commit may be rewritten. No other production, test, fixture, documentation,
dependency, workflow, Harness, user or external path may change.

Authorized new Worker evidence and temporary paths are:

- `harness/reports/CAMPAIGN-014-r2-ledger.md` (new, untracked/unstaged)
- `harness/reports/CAMPAIGN-014-r2-worker.md` (new, untracked/unstaged)
- `.tmp/campaign014-r2-worker/**` for bounded verification only

The admitted `.tmp/campaign014-r1-worker/**` may be removed only after all r2 evidence
has been captured and its resolved absolute path is verified inside this repository's
`.tmp` directory. The r2 temporary directory must likewise be removed before handoff.

## Sequential work order: finish PKG-087

1. Verify admission and preserve the eight-file release intermediate byte-for-byte
   until the bounded test corrections begin.
2. Apply only the two test migrations above. Run the focused pair and require all
   `34 passed` with no deselection.
3. Inspect the complete PKG-087 diff. It must contain only the ten authorized paths and
   preserve the canonical lock delta: editable root `0.13.0 -> 0.13.1`, FastMCP
   `>=2.13.0.2 -> >=2.13.0.2,<4`, revision/package/upload-time `3/78/586`.
4. Run every r1-required integrated and final check. The complete suite must recover
   from `572 passed, 3 failed` to exactly `575 passed`, zero failures and zero skips.
5. Create exactly one commit, subject `PKG-087 release V0.13.1 audit remediation` or a
   clear equivalent, only after local source/test verification passes. Inspect exact
   staged names and staged diff first. Never stage Worker reports or protected assets.
6. Build a fresh wheel and sdist, inspect both archives, record names/sizes/SHA-256, and
   run both isolated CPython 3.12 installed-wheel smokes with exact FastMCP 2.13.0.2 and
   3.4.7. Each must import from isolated `site-packages`, call all five tools and verify
   the r1-required clean/truncation/discussion/V1-summary behavior.
7. Reconcile original-baseline-to-final and revision-baseline-to-final scope, all
   protected hashes, empty index and temporary cleanup.

## Required final evidence

In addition to every inherited r1 requirement, report:

- exact focused recovery `31 passed, 3 failed -> 34 passed` and full recovery
  `572 passed, 3 failed -> 575 passed`;
- the two persistence history modes and the tool-surface assertion migrated without
  production changes;
- exact eight total Campaign commits and one r2 commit;
- exact 30/30 Golden, evaluator Schema 2.1 and all required metrics;
- package/module/build `0.13.1`/v11.1; Review/Receipt/Evaluator Schemas
  `2.6`/`1.1`/`2.1`; five tools; defaults; budgets `6/13/18`; concurrency `3/3`; all 15
  routing profiles;
- no added model/sampling/elicitation/retry/save behavior and unchanged privacy,
  persistence count, Policy Gate, user authority and review-only boundaries;
- lock invariants/diff, `git diff --check`, dead-import scan, compile, complete suite,
  artifact inspection/hashes and both exact FastMCP installed-wheel results;
- exact protected-hash reconciliation, empty index, cleanup, subagent/authority/
  dependency/build/live/remote counts and every skipped check.

Use unique repository-local basetemps/caches for the known Windows host-temp permission
boundary. Record any failed command and bounded rerun; do not hide failures.

## Authority and stop conditions

Local tests, build, pinned dependency sync, bounded temporary cleanup and the one scoped
local commit are authorized under the inherited r1 boundaries. No push, fetch, remote
mutation, PR, release, publication, deployment, Goose/provider/model call, credential
change or Q-016 action is authorized.

Stop with `BLOCKED` if the correction requires production behavior changes, another
unlisted path, rewriting any prior commit, weakening assertions, losing history/privacy
coverage, drifting the lock beyond the exact delta, failing either installed FastMCP
point or violating any inherited r1 stop condition.

## Handoff

Leave the r2 ledger and Worker report untracked/unstaged and the Git index empty. In chat,
start with exactly `READY_FOR_REVIEW` or `BLOCKED`, then report contract hash, original
and revision baselines, final HEAD, all eight commits, exact path scope, focused/full
recovery, Golden/invariants, lock, artifacts, both installed-wheel smokes, protected
hashes, cleanup, subagent/authority/dependency/build/live/remote counts, skipped checks
and remaining risks. Do not claim Campaign acceptance, publication or Q-016 completion.
