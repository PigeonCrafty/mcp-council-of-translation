# CAMPAIGN-002-r2 Worker Report

## Terminal status

READY_FOR_REVIEW

This is a Worker handoff only. Acceptance authority remains with the Foreman; no Campaign or project completion is claimed.

## Control and admission

- HARNESS_ROLE: WORKER / MAIN WORKER
- HARNESS_MODE: STRICT_SEQUENTIAL
- Contract: `harness/contracts/CAMPAIGN-002-r2.md`
- Contract SHA-256: `C71FF5EB63630715B32D0AA2C1ED50A3E20121FA7F1AEC9D708777A2850977B6` (exact expected value)
- Admitted baseline: `5687208aaeaaf3e6b00c192fb42596fb9b6cbf47` (`Bound compact review output`), verified as a commit
- Baseline branch state: `main...origin/main [ahead 7]`
- Baseline index: empty
- Baseline full suite: `141 passed in 1.62s`
- Admission tracked dirt was limited to protected Foreman-owned `harness/plan.md`, `harness/features.json`, and `harness/progress.md`; protected untracked Harness, `.learnings/`, audit, and `reviews/` assets matched the work order. `myTest/` was absent.
- No subagents were used.

## Implementation and commits

Final HEAD: `f7a4f23865383d52dede37f95de091932918090c`

1. `4e49b6271a9bbd88ec7eabd1bd80d69b21be63ac` — `Correct readable local outcome validation`
2. `f7a4f23865383d52dede37f95de091932918090c` — `Expose readable decision form titles`

Baseline-to-final committed scope is 13 allowed files, `242 insertions(+), 57 deletions(-)`:

- `src/council_of_translation/localization/models.py`
- `src/council_of_translation/localization/clustering.py`
- `src/council_of_translation/localization/deliberation.py`
- `src/council_of_translation/localization/orchestration.py`
- `tests/unit/test_v21_outcomes.py`
- `tests/integration/test_v21_elicitation.py`
- `tests/integration/test_v21_reconsideration.py`
- `tests/integration/test_orchestration_v2.py`
- `tests/integration/test_r3_workflow.py`
- `README.md`
- `AGENTS.md`
- `docs/v0.4-architecture.md`
- `docs/v0.4-tool-contract.md`

The correction derives a bounded current outcome from materially consistent cluster `candidate_span` values, retains an exact replacement anchor only when safe, reconstructs the complete candidate at exactly one occurrence before preflight, and records bounded `missing_candidate_anchor` / `ambiguous_candidate_anchor` provenance when reconstruction is impossible. The standard form now emits bounded readable enum literals with readable collision suffixes and maps each field independently to stable internal options. Pydantic/FastMCP field titles use the readable question rather than an internal decision-derived title.

Two accepted workflow fixtures previously asserted `candidate_span="继续按钮"` while the actual candidate was `继续`. They were corrected to the true local anchor; the production implementation was not weakened to accept a missing anchor.

## Before/after counterexamples

| Probe | r1 baseline | r2 final |
| --- | --- | --- |
| Reference form | `choice_d5ae1e894631`, `choice_99ab5485672e`, `delegate_e2f76c056b55` | `保留：继续`, `改为：下一步`, `暂不决定，由 Council 裁决` in both Pydantic and FastMCP schema |
| Long candidate (>500) | current was the whole document, exceeded the outcome bound, and left only `['下一步']` | length `603`; current `继续`; valid outcomes `['继续', '下一步']`; whole document absent from enum |
| Unrelated placeholder | `Welcome {name}\nContinue` versus isolated outcome yielded zero valid DecisionPoints | reconstructed `欢迎 {name}\n下一步`; both `继续` and `下一步` valid |
| Affected placeholder | proposal was dropped by comparing full source to isolated `下一步`, without a reconstruction step | reconstructed complete candidate `下一步`; `braced-placeholder-parity` blocks it; zero DecisionPoints |
| Repeated anchor | whole candidate could be treated as an outcome and no explicit replacement ambiguity was produced | reconstruction is `null`, provenance is `ambiguous_candidate_anchor`, zero DecisionPoints |

Final exact reference enum:

```text
["保留：继续", "改为：下一步", "暂不决定，由 Council 裁决"]
```

Both printed schemas used title `请选择“wording choice”的有效处理方式`; neither enum/title/description exposed `option_...`, `choice_<hex>`, or `delegate_<hex>` values.

## Verification

All listed final commands exited 0 unless explicitly recorded under deviations.

- `python -m compileall src tests` — exit 0.
- `.venv\Scripts\python.exe -m pytest -q tests/unit/test_v21_outcomes.py tests/integration/test_v21_elicitation.py tests/integration/test_tool_surface_v2.py --basetemp .tmp/campaign002-r2-focused-final-2 -p no:cacheprovider` — `23 passed in 1.54s`.
- `.venv\Scripts\python.exe -m pytest -q --basetemp .tmp\campaign002-r2-pytest -p no:cacheprovider` — `146 passed in 1.96s`.
- The repository-local schema/counterexample probe printed identical Pydantic and FastMCP enum/title/description data plus:
  - `LONG_DOCUMENT={"candidate_length": 603, "current_outcome": "继续", "outcomes": ["继续", "下一步"]}`
  - `UNRELATED_PLACEHOLDER={"reconstructed": "欢迎 {name}\n下一步", "valid_outcomes": ["继续", "下一步"]}`
  - `AFFECTED_PLACEHOLDER={"blocking_failures": ["braced-placeholder-parity"], "decision_points": 0}`
  - `AMBIGUOUS_ANCHOR={"provenance": "ambiguous_candidate_anchor", "reconstructed": null, "decision_points": 0}`
- `$env:UV_CACHE_DIR='.tmp\campaign002-r2-uv-cache'; uv build --out-dir .tmp\campaign002-r2-dist` — exit 0; produced `council_of_translation-0.5.0.tar.gz` and `council_of_translation-0.5.0-py3-none-any.whl`.
- Fresh isolated wheel install completed with 70 packages. Final `-I` wheel smoke asserted installed/package/module `0.5.0`, diagnostic build `outcome-first-decision-v3`, schema `2.1`, and exactly the five frozen tools. Output: `0.5.0 0.5.0 outcome-first-decision-v3 2.1 5` and `get_server_info,review_translation,continue_review,view_review_record,list_review_records`.
- `git diff --check 5687208aaeaaf3e6b00c192fb42596fb9b6cbf47..HEAD` — exit 0, no findings.
- `git diff --name-status 5687208aaeaaf3e6b00c192fb42596fb9b6cbf47..HEAD` — exactly the 13 allowed committed files above.

The complete 146-test suite preserves the accepted r1 duplicate/synonym collapse, one-role influence, affirmations, Policy Gate and user authority, fallback, continuation, reconsideration/degradation, compact output, reviewer coverage, V1/V2.0/V2.1 persistence/privacy, review-only boundary, budgets, versions/build identifiers, and exact five-tool surface.

## Acceptance evidence map

| Criteria | Evidence |
| --- | --- |
| 1-3 readable schema and round trip | `test_continue_form_uses_readable_enum_values_and_exact_round_trip`, delegation/malformed tests, per-field equal-value test, collision test, printed Pydantic/FastMCP schemas |
| 4 long document/local current | `test_long_document_keeps_issue_local_current_and_full_reconstruction`, printed 603-character probe |
| 5 unrelated protected material | `test_unrelated_placeholder_survives_local_reconstruction`, printed full reconstruction |
| 6 affected protected token | focused affected-placeholder test plus existing production-path regression; printed `braced-placeholder-parity` |
| 7 repeated/ambiguous anchor | focused reconstruction test; printed `ambiguous_candidate_anchor` and zero points |
| 8 empty/contradictory/overlong anchors | `test_empty_contradictory_and_overlong_spans_do_not_invent_current_outcome` |
| 9 preserved r1 behavior | complete `146 passed` suite |
| 10 identifiers/defaults/budgets | source suite and isolated wheel smoke |
| 11 documentation | four authoritative allowed docs updated; no live Goose claim added |
| 12 package/integration evidence | compile, focused/full pytest, fresh build, isolated wheel smoke, diff and hash checks |

## Protected state

Final protected hashes equal admission values:

- `harness/plan.md` — `8F6556389406923598266D676E9093AEC59C1E3B4E13663E3EE105D1635450B5`
- `harness/features.json` — `3F2286B568087CEDF2B30F808FFD57363C6729D33293E6D4E042BF70E030A204`
- `harness/progress.md` — `9D25E762439696750F8D301B3DF534A528F07BB1E181545599B0B029B2F35774`
- r1 contract — `D58590B24E5CF2E4E7F7116F9E9F7B4D621009B6D3986CCA9A7784ECC1EC40BE`
- r2 contract — `C71FF5EB63630715B32D0AA2C1ED50A3E20121FA7F1AEC9D708777A2850977B6`
- r1 evaluation — `9DCBE1F727F8B38FB1B2996982015AA71E64A6A422BA05ABCC4DFE45B6226453`
- r1 ledger — `10AD5BFB19B4DA3F94F06608EBBA98EF21977DED66ABAD016642E2085D37BA90`
- r1 Worker report — `E552F5A6B9FE3047057AC29E4CE35EBF91CD476ED758B197B4DA6921C67366D4`
- `.learnings/LEARNINGS.md` — `22F939E6F980DF52487AAFE97EDCA9B90CF3931DDB7A31BF8A5BBB8F052E658F`
- `.learnings/ERRORS.md` — `F99EB75886781958BF5AE6DCF844FD476CBCA45937896A25EE3B2E9D6CD34F0A`
- audit markdown — `B48073E063C4C9F34E0B6B4DAE94E80079EAAAD3B2F8E273DD60B2F25F6ABD76`
- `reviews/20260810_145151.json` — `BA2607DEAF9BA440C514FB3D6E5AB34197EDEFA7CC04D9F83859A6EDE4E8FC73`

The final index is empty. The working tree retains only the admission-time protected tracked dirt/untracked assets plus this new untracked r2 Worker report. No protected asset was staged or committed.

## Deviations, skips, and counts

- Initial isolated dependency install timed out at 120.5 seconds after resolving 70 packages and downloading most large wheels. Re-running the same install against the same repository-local environment/cache completed successfully in 31.4 seconds.
- The first wheel surface probe used the FastMCP 2.x test helper `get_tools()`; freshly resolved FastMCP 3.4.7 exposes `list_tools()` instead. The read-only probe was adapted to that installed API and then passed the same exact five-tool assertion. No production code or dependency constraint was changed.
- Skipped required checks: none.
- Optional live Goose/provider calls: 0.
- Subagents: 0.
- Authority escalations: 4, limited to staging/creating the two required local commits because `.git` is outside the writable sandbox surface.
- External mutations: 0. Local repository `.tmp` build/cache/venv writes only.
- Pushes, PRs, releases, deployments, credential changes, Goose changes: 0.

Remaining risk: no live Goose/provider behavior was exercised, as permitted by the contract. The installed wheel was tested against currently resolved FastMCP 3.4.7 for import, diagnostics, schema identity, and tool registration; model/provider behavior remains outside this correction.

## Foreman launch prompt

```text
HARNESS_ROLE: FOREMAN
HARNESS_MODE: STRICT_SEQUENTIAL

Independently review CAMPAIGN-002-r2 from exact baseline
5687208aaeaaf3e6b00c192fb42596fb9b6cbf47 through Worker HEAD
f7a4f23865383d52dede37f95de091932918090c.

Read harness/contracts/CAMPAIGN-002-r2.md and
harness/reports/CAMPAIGN-002-r2-worker.md. Re-run acceptance independently,
verify protected hashes and scope, and issue the Foreman verdict. Do not infer
acceptance from the Worker READY_FOR_REVIEW status.
```
