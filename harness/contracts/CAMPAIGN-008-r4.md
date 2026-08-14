# Campaign Contract: CAMPAIGN-008-r4

## Control

- HARNESS_ROLE: WORKER
- HARNESS_MODE: STRICT_CAMPAIGN
- State: ASSIGNED
- Repository: `C:\Users\GeZhu\MyMCP\mcp-council-of-translation`
- Exact Git baseline: `c3fcfec363878d069b64e15a65a364c7fd55468b`
- Baseline subject: `Complete deterministic issue correlation`
- Supersedes for execution: `CAMPAIGN-008-r3`
- Product identifiers remain: package/module `0.10.0`, build
  `evidence-value-council-v8`, schema `2.4`
- Required Worker report: `harness/reports/CAMPAIGN-008-r4-worker.md`
- New ledger: not required
- Commit policy: exactly one scoped local commit
- Subagent delegation: forbidden
- Acceptance authority: Foreman only

Read completely before editing: `AGENTS.md`, `harness/plan.md`,
`harness/features.json`, `harness/progress.md`, this contract, all Campaign 008 r1-r3
contracts/evaluations/Worker reports, and the r1 ledger.

## Bounded correction outcome

Preserve production clustering identity for model-only issues while retaining every
accepted r3 deterministic-preflight correlation. This is a grouping-boundary correction,
not a redesign of contribution semantics.

## Required correction

1. Track which logical groups are rooted in one or more deterministic preflight clusters
   (`finding_ids` empty).
2. A reviewer/model cluster may attach by r3 exact aliases only to deterministic-rooted
   groups.
3. If a reviewer cluster matches no deterministic-rooted group, append it as its own
   production issue group. No later reviewer cluster may join that group through r3
   alias matching.
4. A reviewer cluster may attach to multiple independent deterministic groups when it
   carries distinct exact anchors for each, but it cannot bridge or merge those groups.
5. Preserve production clustering's same-family deduplication/corroboration unchanged.
   `value_metrics` consumes the produced model cluster as one identity; it must not
   recreate semantic clustering across model clusters.
6. Preserve original clusters/evidence byte-for-structure, unavailable precedence,
   contribution priorities and zero-call behavior.

## Required counterexamples

- Two model-only clusters with the same `source_span`/`candidate_span` but different
  families (`accuracy`/correctness vs `terminology`/language_choice) remain two unique
  issues, with each role `unique_material`.
- Two reviewer findings that production clustering correctly combines into one
  same-family cluster continue to yield one corroborated issue.
- A model cluster matching a deterministic required-literal group still joins it once.
- All r3 required/forbidden literal, numeric, four Markdown, DNT, URL overlap,
  placeholder+URL, distinct-literal and unavailable counterexamples remain green.
- Golden Corpus remains exactly 18/18 with the same scripted call/interaction totals and
  all aggregate metrics 1.0.

## Authorized paths

- `src/council_of_translation/localization/value_metrics.py`
- `tests/unit/test_v24_value_metrics.py`
- optional only if a full-orchestration assertion is necessary:
  `tests/integration/test_v24_value_metrics.py`
- required `harness/reports/CAMPAIGN-008-r4-worker.md`

No other code, test, fixture, package, documentation, dependency, lock, Harness or user
path is authorized. Do not stage or commit the Worker report or protected assets.

## Admission and protected assets

Verify exact baseline, empty index, contract hash, admitted dirty/untracked set and all
hashes below before editing. Admission compile and complete suite must pass with at least
`276 passed`; stop on unexplained drift.

| Protected asset | SHA-256 |
| --- | --- |
| `harness/plan.md` | `AA14085768FF6A910EB0A9028D02FABD552DBB829DF7F085DC1D2268B21530B0` |
| `harness/features.json` | `A5E1A5030C9A307F4A3FE55682D9E5F49A6789C11D34C20F5A407084141DF984` |
| `harness/progress.md` | `4DC02397918A1B44B8D08CD6DFE7030EC482558FD075784937C5410A2A175DDC` |
| r1 contract | `3D477E8418B77A621EFEBB3BD496CD0508BCC9C39A22D833EFA79886A98EE366` |
| r2 contract | `9F01492711FDCA0CCF27D74851E8A3FDB26DA6454524CC4DAA799FA48E1201BB` |
| r3 contract | `25E38BE0AD014A0B0F7A5F7351FCFB93AE63FC0EAE283CDD8357AA3E7005EF6B` |
| r1 evaluation | `D85B7C35026C394001C7C17DE5FCE591128D917BB1961FA67ADED19E88FE3292` |
| r2 evaluation | `AC8E122CFC3AF539E4E74E8B8DE99845258D81F7AFF7B28BF87EB1F8850DE6EC` |
| r3 evaluation | `95A78CA651F50C8931AE434C72093BCC4466D3E97A4F70238969D37066D8F659` |
| r1 Worker report | `412A1E032B919289630EAE58A386B45EF5869B10C91C9FEC76C78313DC8AA37F` |
| r1 ledger | `26AD64BE56B776B9EECD07F927C116E9B360746194D1CE026E3AEE0295A5068A` |
| r2 Worker report | `12E9B7ECDE549ACCCF79B649446D7838BBDA586589363B4E86A2E92A9177A698` |
| r3 Worker report | `54559EE4256B0DB62D343B8745B94CD98CA8508686CC64960DEBC836111A7CE6` |
| `.learnings/LEARNINGS.md` | `52DC1BA8043481911C0DEABB3AC882504D9CBE8BB63D60F391C188586A230DF0` |
| `.learnings/ERRORS.md` | `F99EB75886781958BF5AE6DCF844FD476CBCA45937896A25EE3B2E9D6CD34F0A` |
| audit Markdown | `B48073E063C4C9F34E0B6B4DAE94E80079EAAAD3B2F8E273DD60B2F25F6ABD76` |

All other contracts/evaluations plus `reviews/**` and `myTest/**` are path-protected.

## Required verification

1. Admission compile and complete `276`-test suite.
2. Run the new cross-family same-span and same-family control tests.
3. Run all r3 deterministic-correlation and non-overmerge tests.
4. Run all V2.4 model/metrics/persistence/presentation/Golden tests; assert exact 18/18,
   113 scripted samples, four scripted elicitations and all aggregate metrics 1.0.
5. Run public tool/version/schema/budget/concurrency and compatibility invariants.
6. Final compile and complete suite.
7. Run `git diff --check c3fcfec363878d069b64e15a65a364c7fd55468b..HEAD`,
   exact authorized scope, protected hashes, dead-import scan and empty index.
8. Build fresh wheel/sdist and isolated Python 3.12/current-FastMCP smoke through all five
   tools plus cross-family model-only and required-literal deterministic probes.

## Stop conditions and handoff

Stop `BLOCKED` only if the correction requires clustering/preflight/schema/public/
dependency changes, another unauthorized path or live/external authority. A new test
failure is normal Worker work, not a blocker.

Write `harness/reports/CAMPAIGN-008-r4-worker.md`. Start the handoff with exactly
`READY_FOR_REVIEW` or `BLOCKED`, then report contract hash, baseline/final HEAD, one
commit and exact paths, before/after model-only counterexample, preserved deterministic
matrix, focused/Golden/full/build/wheel results, hashes/index/worktree, subagent/
authority/external/live counts and remaining risks. Do not push, create/update a PR,
release, deploy, call Goose/provider/model, claim Campaign acceptance, Q-012 acceptance
or project completion.

