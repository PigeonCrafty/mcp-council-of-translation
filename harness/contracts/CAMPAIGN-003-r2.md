# Campaign Correction Contract: CAMPAIGN-003-r2

## Control

- Role: MAIN WORKER
- Mode: STRICT_CAMPAIGN
- State: ASSIGNED
- Repository: `C:\Users\GeZhu\MyMCP\mcp-council-of-translation`
- Exact baseline: `3de6e5fafb0d6a0a4347b68469e99ce7ef8bc816`
- Baseline subject: `Retain safe guided metadata counts`
- Parent contract: `harness/contracts/CAMPAIGN-003-r1.md`
- Parent review: `harness/evaluations/CAMPAIGN-003-r1-review.md`
- Worker report: `harness/reports/CAMPAIGN-003-r2-worker.md`
- Ledger: not required for this one-package correction
- Commit policy: exactly one scoped local correction commit; no push, PR, release, tag or deployment
- Subagents: forbidden
- Acceptance authority: Foreman only

This revision is a bounded correction. Do not reopen or redesign accepted r1 packages. Read `AGENTS.md`, the r1 contract, r1 Worker report, r1 ledger, r1 Foreman review, `harness/plan.md`, `harness/features.json` and `harness/progress.md` completely before editing.

## Admission gate

Before any edit:

1. verify exact HEAD and subject above;
2. verify the Git index is empty;
3. verify the only dirty/untracked assets are the protected Foreman/user assets below;
4. verify every SHA-256 value below and hash this r2 contract byte-for-byte;
5. run `python -m compileall -q src tests`;
6. run the full suite with a repository-local basetemp and cache provider disabled; expected baseline is exactly `182 passed`.

Stop `BLOCKED` on any unexplained mismatch. Never repair, stage, delete, move or rewrite protected assets.

| Protected asset | SHA-256 |
| --- | --- |
| `harness/plan.md` | `2D287FB16AD60D35E94289C9EDF3F2430DFD48F1EF6C35864F952AC95DA7F96A` |
| `harness/features.json` | `7E1A6C258ABBB1A25D6270B1202902DECEF7D8D0F421A173689E3D21092EF1F4` |
| `harness/progress.md` | `18BBE2DE28381EA5BCF216834175C4FDB3D987BEB492B56A3FA3CA378212E73F` |
| `harness/contracts/CAMPAIGN-003-r1.md` | `6A1017CF7C8205CC1FB753EC747529B0BF7920676655A53314C8B71B29239A46` |
| `harness/evaluations/CAMPAIGN-003-r1-review.md` | `B2CC11664F70352F45998BCBA6EE42EB2BBA1E8BE94CACB4B470A0D112B32DB3` |
| `harness/reports/CAMPAIGN-003-r1-ledger.md` | `7641B0D4CD5121D2CEA635DDD10B43D174A3CDD781E853591E6C142BD6E063BE` |
| `harness/reports/CAMPAIGN-003-r1-worker.md` | `1267643257A87942D90E539830A3FB68E653A543B14A848CD525FD20E0782770` |
| `.learnings/LEARNINGS.md` | `22F939E6F980DF52487AAFE97EDCA9B90CF3931DDB7A31BF8A5BBB8F052E658F` |
| `.learnings/ERRORS.md` | `F99EB75886781958BF5AE6DCF844FD476CBCA45937896A25EE3B2E9D6CD34F0A` |
| audit Markdown | `B48073E063C4C9F34E0B6B4DAE94E80079EAAAD3B2F8E273DD60B2F25F6ABD76` |

Also preserve `.learnings/**`, `reviews/**`, `myTest/**` if present, every prior Harness artifact, and all other user files. Only the required r2 Worker report may be created under `harness/`.

## Preserved r1 evidence

The Foreman preserves r1 evidence for PKG-017 and PKG-019 through PKG-022, including V2.2 persistence/privacy, bounded context gaps, form IA, process digest, phase trace, 6/13/18 budgets, five-tool surface, compatibility, docs and packaging. Do not alter those implementations or their tests.

PKG-018 evidence for briefing-before-sampling and the accept/decline/cancel/unsupported/malformed matrix is also preserved. Only the deterministic auto-mode sufficiency predicate and its missing counterexamples are reopened.

## Required correction

Implement the exact frozen auto-mode context sufficiency rule:

1. `content_type` must normalize to a recognized value other than `unspecified`; **and**
2. at least two independent categories below must be present:
   - usage/reference: non-empty `context` or `reference_translations`;
   - audience: non-empty `audience`;
   - style/brand: non-empty `style_guide` or `brand_guidelines`;
   - glossary/project/technical authority: non-empty `term_glossary`, `project_rules` or `technical_constraints`.

`known_exceptions`, `notes`, hard-constraint lists and do-not-translate literals do not by themselves make briefing context rich. They retain their existing authority and must not be weakened or erased.

Expected deterministic outcomes:

- recognized `ui` plus context plus audience: sufficient, auto skips;
- recognized alias `UI button` plus any two independent categories: sufficient, auto skips;
- recognized content plus only one category: insufficient, auto requests;
- unknown/unspecified content plus two, three or all four categories: insufficient, auto requests;
- source/candidate only: insufficient, auto requests;
- `briefing_mode=always` and `off` behavior remains unchanged.

Do not replace the predicate with a weighted score or raw field count. Do not sample to decide sufficiency.

## Allowed scope

- `src/council_of_translation/localization/guided.py`
- `tests/integration/test_v22_briefing.py`
- `harness/reports/CAMPAIGN-003-r2-worker.md`

No other production, test, documentation, dependency, version, Harness or user path is authorized. Stop if the correction requires broader scope.

## Non-goals and frozen interfaces

- No new MCP tool, argument, mode, schema field, form field or dependency.
- No change to version `0.6.0`, build `guided-deliberation-v4`, schema `2.2`, exact five tools or 6/13/18 budgets.
- No change to briefing answer precedence, context-gap behavior, reconsideration, digest, compact projection, persistence or continuation.
- No formatting sweep, refactor, rename or unrelated cleanup.
- No live Goose/model/provider call and no credential request.

## Acceptance criteria

1. The exact frozen predicate above is readable and deterministic.
2. Unit-level or focused tests cover every positive and negative counterexample listed above, including unknown content with all four independent categories.
3. Existing source/target-only ordering and full briefing action matrix remain green.
4. All 182 baseline tests plus new tests pass; no useful assertion is deleted or weakened.
5. Compile, focused/full tests, fresh wheel/sdist build, diff check, exact allowed-scope audit, protected hashes, empty index and repository hygiene pass.
6. Exactly one local correction commit contains only the two authorized implementation/test paths; the r2 Worker report remains uncommitted.

## Required verification

Run and report exact commands/results:

```powershell
python -m compileall -q src tests
.venv\Scripts\python.exe -m pytest -q tests\integration\test_v22_briefing.py --basetemp .tmp\campaign003-r2-focused -p no:cacheprovider
.venv\Scripts\python.exe -m pytest -q --basetemp .tmp\campaign003-r2-full -p no:cacheprovider
```

Print a direct Core/helper truth table containing at least:

```text
recognized_plus_two=True
alias_plus_two=True
recognized_plus_one=False
unknown_plus_two=False
unknown_plus_three=False
unknown_plus_all_four=False
source_target_only=False
```

Then build fresh repository-local artifacts:

```powershell
$env:UV_CACHE_DIR='.tmp\campaign003-r2-uv-cache'
uv build --out-dir .tmp\campaign003-r2-dist
```

Verify the fresh wheel is `0.6.0`, contains the corrected `guided.py`, and report its SHA-256. The r1 isolated FastMCP wheel smoke is preserved; no dependency reinstallation or live provider call is required for this predicate-only correction.

Finally run:

- `git diff --check 3de6e5fafb0d6a0a4347b68469e99ce7ef8bc816..HEAD`;
- baseline-to-final name/status and exact allowed-path audit;
- staged/index emptiness after commit;
- all protected hashes;
- final worktree inventory.

## Stop conditions

Return `BLOCKED` without edits if baseline, contract hash, admission test count, protected assets or authorized scope do not match. Stop rather than changing the frozen category definition, public interface, version, persistence, orchestration or accepted package evidence.

## Handoff

Write `harness/reports/CAMPAIGN-003-r2-worker.md`. In chat start with exactly `READY_FOR_REVIEW` or `BLOCKED`, then include:

- contract hash, admitted/final HEAD and commit;
- exact changed files;
- truth table and focused/full/build results;
- skipped checks, subagents (must be zero), Git authority escalations and external/live-call counts;
- protected-hash and worktree status;
- remaining risk.

Do not claim Campaign acceptance or project completion. Do not push.
