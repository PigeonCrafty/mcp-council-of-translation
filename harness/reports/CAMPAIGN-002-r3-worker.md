# CAMPAIGN-002-r3 Worker Report

## Terminal status

READY_FOR_REVIEW

Worker handoff only. Acceptance authority remains with the Foreman; this report does not claim Campaign acceptance.

## Control and admission

- HARNESS_ROLE: WORKER
- HARNESS_MODE: STRICT_SEQUENTIAL
- Contract: `harness/contracts/CAMPAIGN-002-r3.md`
- Contract SHA-256: `1908786C679B8F3ACF67B5925CE0FBD407C0AD9A2B05DD682739903176F68007`
- Exact admitted baseline: `f7a4f23865383d52dede37f95de091932918090c` (`Expose readable decision form titles`), verified as a commit
- Baseline branch: `main...origin/main [ahead 9]`
- Baseline index: empty
- Baseline full suite: `.venv\Scripts\python.exe -m pytest -q --basetemp .tmp\campaign002-r3-baseline -p no:cacheprovider` — `146 passed in 1.48s`
- Tracked dirt was limited to the three protected Foreman Harness state files. All listed protected/untracked Harness, `.learnings/`, audit, and `reviews/` assets matched the contract; `myTest/` was absent.
- Required capabilities were available. Subagents were forbidden and none were used.

## Implementation and commit

- Final HEAD: `ca3d24afdc8feaa65286b13c6118720809749436`
- Commit: `ca3d24afdc8feaa65286b13c6118720809749436` — `Enforce outcome eligibility and suppression provenance`
- Baseline-to-final scope: 11 authorized files; `386 insertions(+), 25 deletions(-)`.

Changed files:

- `src/council_of_translation/localization/clustering.py`
- `src/council_of_translation/localization/orchestration.py`
- `tests/integration/test_r3_outcome_suppression.py`
- `tests/integration/test_r3_workflow.py`
- `tests/unit/test_r3_deliberation_policy.py`
- `tests/unit/test_r4_role_normalization.py`
- `tests/unit/test_v21_outcomes.py`
- `README.md`
- `AGENTS.md`
- `docs/v0.4-architecture.md`
- `docs/v0.4-tool-contract.md`

The action-based legacy outcome fallback was removed. Only normalized `finding_kind="choice"` findings with a non-empty bounded string `proposed_value` can contribute a proposal; issue, affirmation, missing/invalid classification, and incomplete choices retain `action` only as advice.

Reconstruction validation now collects only `missing_candidate_anchor` and `ambiguous_candidate_anchor` suppression records. Each record contains validated deterministic `issue_id`, `decision_id`, and `reason_code` only; entries are deduplicated and capped at eight. Full history persists the records in `policy_gate_result.decision_suppressions`. Compact/full state exposes a deduplicated `decision_suppressed:<reason>` warning, `degraded=true`, `decision_validation_degraded`, and `COMPLETED_WITH_FALLBACK` unless a stronger existing status applies. Metadata retains only its existing safe status/degraded disposition and omits suppression details and prose. Deterministic protected-token rejection does not create anchor-degradation provenance.

Existing legacy tests that intentionally exercised outcome decisions were updated to state the V2.1 `choice`/`proposed_value` classification explicitly; production behavior was not weakened to preserve obsolete action selection.

## Before and after evidence

Baseline reproduction:

- Two omitted-classification findings with long action instructions produced `candidate_actions` containing both instructions, one DecisionPoint, and one elicitation request.
- Repeated and missing anchors produced zero DecisionPoints but `policy_gate_result` without suppression, empty warnings, `degraded=false`, empty fallback reason, and `COMPLETED`.

Final exact Core outputs:

- Omitted classification: `candidate_actions=[["继续"]]`, `decision_points=0`, `elicitation_requests=0`, no suppression/degradation.
- Explicit issue: `candidate_actions=[["继续"]]`, zero decisions/elicitation.
- Invalid classification: `candidate_actions=[["继续"]]`, zero decisions/elicitation.
- Choice with empty, non-string, or 501-character proposal: each `candidate_actions=[["继续"]]`, zero decisions/elicitation.
- Mixed valid choice/issue/affirmation: `candidate_actions=[["继续", "下一步"]]`; issue and affirmation actions are absent from selectable structures.
- Ambiguous anchor: persisted `[{"issue_id":"issue_1f2b24a4c751","decision_id":"decision_1f2b24a4c751","reason_code":"ambiguous_candidate_anchor"}]`; warning `decision_suppressed:ambiguous_candidate_anchor`; `degraded=true`; fallback `decision_validation_degraded`; status `COMPLETED_WITH_FALLBACK`.
- Missing anchor: persisted analogous content-free record with `missing_candidate_anchor`; matching warning/degraded/fallback/status.
- Actual `{count}` loss: zero DecisionPoints but empty suppression/warnings, `degraded=false`, empty fallback, `COMPLETED`.
- Readable schema control: Pydantic and FastMCP enum both exactly `["保留：继续", "改为：下一步", "暂不决定，由 Council 裁决"]` with readable question title.

## Verification

Final checks all exited 0 except the disclosed first offline install attempt:

- `python -m compileall src tests` — passed.
- `.venv\Scripts\python.exe -m pytest -q tests/unit/test_v21_outcomes.py tests/integration/test_r3_outcome_suppression.py tests/integration/test_v21_elicitation.py tests/integration/test_tool_surface_v2.py --basetemp .tmp/campaign002-r3-focused-final -p no:cacheprovider` — `36 passed in 1.04s`.
- `.venv\Scripts\python.exe -m pytest -q --basetemp .tmp\campaign002-r3-pytest -p no:cacheprovider` — `159 passed in 1.57s`.
- The named repository-local Core probe printed every required classification/action case, mixed control, repeated/missing persisted records, protected-token control, and Pydantic/FastMCP schema exactly as summarized above — exit 0.
- `$env:UV_CACHE_DIR='.tmp\campaign002-r3-uv-cache'; uv build --out-dir .tmp\campaign002-r3-dist` — exit 0; produced `council_of_translation-0.5.0.tar.gz` (50,151 bytes) and `council_of_translation-0.5.0-py3-none-any.whl` (55,742 bytes).
- Fresh isolated wheel install resolved and installed 70 packages. `-I` smoke asserted installed/package/module `0.5.0`, diagnostic build `outcome-first-decision-v3`, schema `2.1`, exact five tools, budgets 6/10/14, issue action non-promotion, and mixed valid choice. Output included `0.5.0 0.5.0 outcome-first-decision-v3 2.1 5 {'lightweight': 6, 'standard': 10, 'strict': 14}`.
- `git diff --check f7a4f23865383d52dede37f95de091932918090c..HEAD` — exit 0.
- `git diff --name-status f7a4f23865383d52dede37f95de091932918090c..HEAD` — exactly the 11 authorized files above.
- Complete correction diff, source searches for removed action fallback, index, worktree, and scope allowlist were inspected; no out-of-scope committed path was found.

The final 159-test suite keeps accepted r1/r2 readable enums, issue-local current outcomes, full-candidate reconstruction, long document, unrelated/affected placeholders, collision and per-field mapping, delegation and stale/malformed handling, influence/Policy Gate, reconsideration/degradation, coverage/compact/continuation, V1/V2.0/V2.1 persistence/privacy, review-only boundary, five tools, versions/build/schema, and budgets green.

## Acceptance mapping

| Criteria | Evidence |
| --- | --- |
| 1-3 no action promotion and mixed control | focused unit/Core production tests and exact printed action/classification outputs |
| 4 V1/V2.0 compatibility | full compatibility/persistence suite within `159 passed` |
| 5-6 repeated/missing suppression | production persistence tests and exact full/compact/reloaded outputs |
| 7 protected-token control | focused production test and exact empty-suppression output |
| 8 bounded/private provenance | cap/dedup/content-free test, full reload test, metadata allowlist test |
| 9 accepted r1/r2 behavior | focused readable schema plus complete `159 passed` and wheel smoke |
| 10 integrated gates | compile, focused/full tests, Core output, fresh build/wheel, diff and hashes |

## Protected state and repository hygiene

All final protected hashes equal the contract values:

- `harness/plan.md` — `B7955061A7519D9BEA92422DF04A5B31A1A51E7015C6C3B59D2727B331072CE6`
- `harness/features.json` — `AB58536DE655B4D44A18A8C636F843C49AA29BE251B65A89CFC8B8DDF6FC39D9`
- `harness/progress.md` — `5C2F940BC62FE8E19A615AD6E29D21C94AE7B6B30C4163542544726709D33823`
- r1 contract — `D58590B24E5CF2E4E7F7116F9E9F7B4D621009B6D3986CCA9A7784ECC1EC40BE`
- r2 contract — `C71FF5EB63630715B32D0AA2C1ED50A3E20121FA7F1AEC9D708777A2850977B6`
- r3 contract — `1908786C679B8F3ACF67B5925CE0FBD407C0AD9A2B05DD682739903176F68007`
- r1 review — `9DCBE1F727F8B38FB1B2996982015AA71E64A6A422BA05ABCC4DFE45B6226453`
- r2 review — `D4EF53646A3BDB41E976C5B127FD49D7AE1C0F2E1F1D9A02B23C52AE456F2894`
- r1 ledger — `10AD5BFB19B4DA3F94F06608EBBA98EF21977DED66ABAD016642E2085D37BA90`
- r1 Worker report — `E552F5A6B9FE3047057AC29E4CE35EBF91CD476ED758B197B4DA6921C67366D4`
- r2 Worker report — `F3DDB096C5CAA77A2AE055515FC9EEE9DEFD2566B48B7BF3538C7B0195145040`
- `.learnings/LEARNINGS.md` — `22F939E6F980DF52487AAFE97EDCA9B90CF3931DDB7A31BF8A5BBB8F052E658F`
- `.learnings/ERRORS.md` — `F99EB75886781958BF5AE6DCF844FD476CBCA45937896A25EE3B2E9D6CD34F0A`
- audit markdown — `B48073E063C4C9F34E0B6B4DAE94E80079EAAAD3B2F8E273DD60B2F25F6ABD76`
- `reviews/20260810_145151.json` — `BA2607DEAF9BA440C514FB3D6E5AB34197EDEFA7CC04D9F83859A6EDE4E8FC73`

The final index is empty. The working tree retains only admission-time protected Foreman/user dirt plus this new untracked r3 Worker report. No protected asset was edited by the Worker, staged, or committed.

## Deviations, skips, counts, and risk

- First wheel-install attempt used `--offline` with the fresh r3 cache and failed at dependency resolution because FastMCP was not cached. The same isolated environment then installed normally with network reads and passed the complete smoke. No dependency or production change was made.
- Required checks skipped: none.
- Subagents: 0.
- Authority escalations: 2, limited to staging and creating the required local commit because `.git` is outside the writable sandbox.
- Live Goose/provider calls: 0.
- External mutations: 0. Network use was dependency download only; all generated artifacts remained under repository-local `.tmp`.
- Pushes, PRs, releases, deployments, credential changes, Goose changes: 0.
- Remaining risk: live provider/Goose outcome UX was not exercised in r3; the contract does not require it. Fresh FastMCP 3.4.7 wheel registration and deterministic Core/schema behavior passed.

## Foreman launch prompt

```text
HARNESS_ROLE: FOREMAN
Use pigeon-harness in STRICT_SEQUENTIAL mode.
Review harness/reports/CAMPAIGN-002-r3-worker.md against
harness/contracts/CAMPAIGN-002-r3.md in
C:\Users\GeZhu\MyMCP\mcp-council-of-translation.
Inspect f7a4f23865383d52dede37f95de091932918090c..ca3d24afdc8feaa65286b13c6118720809749436
and verify independently. Decide ACCEPTED, CHANGES_REQUESTED, or BLOCKED.
```
