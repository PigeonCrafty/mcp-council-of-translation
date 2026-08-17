READY_FOR_REVIEW

# CAMPAIGN-010-r2 Worker Report

## Control and admission

- Role: `WORKER / MAIN WORKER`
- Harness mode: `STRICT_CAMPAIGN`
- Contract: `harness/contracts/CAMPAIGN-010-r2.md`
- Contract SHA-256: `2A1F01AA9E59527B8D822A893CD968EDD335F5C738EA70939455DABFA2F3D711`
- Required and observed baseline: `144ecebb6bfbd507ccdfb09a9b87efac3d59e9e1`
- Admission index: empty.
- Admission compile: `.venv\Scripts\python.exe -m compileall -q src tests` -> exit 0.
- Admission regression: `.venv\Scripts\python.exe -m pytest -q --basetemp=.pytest-c010-r2-admission` -> exactly `291 passed in 4.27s`.
- Admission protected hashes: all 13 contract-listed values matched after the values were re-read directly from the contract.
- Admission `uv.lock` SHA-256: `31F0173F9325A4CA1C5BF95BB281B75E00374C8A241A19DFC38AB39C95F5347D`.

The admitted pre-existing dirty/untracked assets were the modified Foreman-owned
`harness/plan.md`, `harness/features.json`, and `harness/progress.md`; untracked
`.learnings/**`, `reviews/**`, the user audit report, r1/r2 contracts, r1 Worker report,
and the CAMPAIGN-009/CAMPAIGN-010 evaluations. The raw `.tmp/q012` records were not read,
copied, edited, staged, deleted, moved, or committed. Only their contract-required
SHA-256 values were checked.

## Commit and exact scope

- Final HEAD: `f58306d0df42fc27d46dd5049348ccfce8a0f6f8`
- Single local commit: `f58306d0df42fc27d46dd5049348ccfce8a0f6f8 Fix zero-proposal work item grouping`
- Baseline-to-final changed paths, exactly the three authorized paths:
  - `src/council_of_translation/localization/digest.py`
  - `tests/integration/test_v101_live_shaped_value.py`
  - `tests/integration/test_v24_presentation.py`
- Diff size: 210 insertions, 22 deletions.
- `git diff --check 144ecebb6bfbd507ccdfb09a9b87efac3d59e9e1..HEAD` -> exit 0.
- AST dead-import scan of `digest.py` -> `[]`.
- No version, documentation, package metadata, dependency, `uv.lock`, prompt, role,
  routing, clustering, metric, persistence, Policy Gate, adjudication, runtime, or public
  tool path changed.

This report is intentionally untracked and unstaged. No Campaign ledger is required or
authorized by r2.

## PKG-057 correction

The primary-only projection now retains the accepted r1 exact source/candidate/action
identity whenever a concrete non-current action exists. Only clusters with no such action
can use the r2 fallback. That fallback requires:

- non-empty normalized source anchors that are exact, or singleton anchors with direct
  containment;
- the same independent rule for candidate anchors;
- different category families for every member;
- pairwise compatibility across the group, preventing transitive bridging;
- no member with a non-current concrete action.

The first topic is the repair statement and later bounded topics are consequences, so the
first topic is not repeated as its own consequence. The projection does not mutate any
record, digest, cluster, metric, finding, or full-history structure.

Exact evidence:

- Live-shaped B production clustering creates two actionless/current-only reversal
  clusters from nested `cannot be undone` / full-source and `可以撤销` / full-candidate
  anchors. Both bounded consequences occur once on one reversal line. The deterministic
  `{count}` repair remains separate.
- The direct B counterexample contains exactly one natural `{count}` placeholder repair
  and one actionless reversal repair, no duplicate execution line, and each reversal
  consequence once.
- C uses exact shared source/candidate anchors with one cluster current-outcome-only and
  the other empty. It renders one repair, no duplicate execution line, and both accuracy
  and user-impact consequences once.
- Negative controls pass for conflicting concrete replacements, different protected
  literals, related source/unrelated candidate, related candidate/unrelated source,
  placeholder and reversal in one sentence, and exact same spans with incompatible
  non-current actions.
- Re-render assertions preserve the complete synthetic record and/or digest, clusters,
  and value metrics byte-equivalently via pre/post JSON-mode dumps.

## Test and Golden evidence

- Focused final B/C and negative-control selection:
  `.venv\Scripts\python.exe -m pytest -q tests/integration/test_v101_live_shaped_value.py tests/integration/test_v24_presentation.py --basetemp=.pytest-c010-r2-focused-4`
  -> `15 passed in 0.23s`.
- Affected r1 presentation/privacy/value/Golden/release/tool/persistence selection:
  10 named modules -> `82 passed in 1.46s`.
- Executable Golden aggregate: exact `18/18`; failed IDs `[]`; scripted totals `113`
  samples and `4` elicitations; all eight rates were exactly `1.0`:
  critical recall, false-positive-free, contribution kind, conflict detection, user
  authority, chief consistency, call budget, and discussion marginal value.
- Pre-commit full suite: `294 passed in 3.56s`.
- Final compile: `.venv\Scripts\python.exe -m compileall -q src tests` -> exit 0.
- Final full suite from committed HEAD:
  `.venv\Scripts\python.exe -m pytest -q --basetemp=.pytest-c010-r2-final`
  -> `294 passed in 3.71s`.

The baseline had 291 tests. The three added regressions account for the final 294. Static
inspection found no sample or elicitation call site added to `digest.py`; the production
change is deterministic rendering only.

## Frozen surface proof

The committed source probe returned:

- exact tools in frozen order: `review_translation`, `continue_review`,
  `view_review_record`, `list_review_records`, `get_server_info`;
- package/module `0.10.2` / `0.10.2`;
- build `evidence-value-council-v8.2`;
- schema `2.4`;
- default output `review_only`;
- budgets `6/13/18`;
- independent review concurrency `3/3`, disposition `default`.

No production sampling, elicitation, retry, discussion, persistence, or hidden model call
was added.

## Fresh build and isolated wheel smoke

Using repository-local `UV_CACHE_DIR`/`UV_TOOL_DIR` and pinned `uv 0.12.3`:

- `uvx --from uv==0.12.3 uv --version` -> `uv 0.12.3`.
- `uvx --from uv==0.12.3 uv build --out-dir .build-c010-r2` -> fresh sdist and wheel
  succeeded from final HEAD.
- Wheel: `council_of_translation-0.10.2-py3-none-any.whl`, 92,935 bytes, 29 members,
  SHA-256 `67AB2B980EE858C0AA8DEE02F6E402C875B3D3CBFBD0763793065DFC08C0F400`.
- Sdist: `council_of_translation-0.10.2.tar.gz`, 86,705 bytes, 40 members,
  SHA-256 `F36230C0CFA6CA8C94ABF61E1F06291D72B8F5B47C15233ADE3E31ACA886E87F`.
- Neither archive contains build/cache/smoke/Q-012 temporary paths.
- Isolated environment: Python `3.12.9`, FastMCP `3.4.7`.
- Installed-wheel smoke called all five tools with local scripted model envelopes only.
  Main review completed with six samples, one grouped six-role confirmation line,
  review-only output and a 346-code-point report. Continuation completed with zero child
  samples; full view, list and server info passed. Version/build/schema and budgets were
  exact.
- All repository-local pytest/build/cache/tool/venv/synthetic-record directories created
  by this Worker were removed after evidence capture.

Final `uv.lock` SHA-256 remains byte-identical to admission:
`31F0173F9325A4CA1C5BF95BB281B75E00374C8A241A19DFC38AB39C95F5347D`.

## Protected assets and final Git state

Every protected hash matched again after commit, build, smoke, and cleanup:

- `harness/plan.md`: `7F76741892002C2FC6ABA459B79441321A4D220A40ADCD723E3A902DE288C4C6`
- `harness/features.json`: `D2FCE49FF59059218D12F02F8080B8E2A1478D76CD1DB43A93229FC497ADC2D0`
- `harness/progress.md`: `ABB4353457726ABE2D49C3CB2B241FA7BCFD756B28C5F05AAD18AC29DABAA474`
- r1 contract: `E09A31F3E544619D55B6A0DE456509E0F549DA694361C27925F1BFF2821535DE`
- r1 Foreman review: `B71BAAF6E7A894A143AB94F62A3B518E851C10C095CFA6AB2B303AF03BC16223`
- r1 Worker report: `AF17F84F5C02F08A4D6ED765E49514562E8CF9337902A8E8FA8A13DA1DDAB287`
- CAMPAIGN-009 Q-012 review: `7BF0FEC690540DFD19DC9380ECC2726A14933B0AC3C3284AF35FE2738E60B778`
- raw A/B/C records: `3652A7F55AEB1C25BAA34905C2E922957C6B184A58DF80CC513A5B1D20820F41`,
  `80C7A47D1B0330A40A824B47C718A92B9C84C399FB548D9EA60E90320CDC5CEF`,
  `07EB4B9E331B188B035D3397F6C2E418F8CDF3AB2E6872E8236EE914F773857B`
- `.learnings/LEARNINGS.md`: `52DC1BA8043481911C0DEABB3AC882504D9CBE8BB63D60F391C188586A230DF0`
- `.learnings/ERRORS.md`: `F99EB75886781958BF5AE6DCF844FD476CBCA45937896A25EE3B2E9D6CD34F0A`
- user audit: `B48073E063C4C9F34E0B6B4DAE94E80079EAAAD3B2F8E273DD60B2F25F6ABD76`

Final index is empty. The final worktree retains only the admitted protected dirty/
untracked assets plus this required untracked, unstaged r2 Worker report.

## Deviations, skipped checks, authority, and risks

- A first protected-hash script used several incorrectly reconstructed values from a
  compacted conversation summary. No file differed. The contract table was re-read
  directly and both admission and final checks then matched every value.
- A bulk asset read exceeded output limits; all required files were subsequently read in
  explicit complete chunks or individually before editing.
- Two focused attempts exposed an over-broad synthetic assertion that counted an
  unrelated retained reviewer placeholder message as a reversal repair. The fixture and
  assertion were narrowed to the contract's exact B work-item identity; the independent
  whole-sentence placeholder/reversal non-merge control remains. Final focused and full
  suites pass.
- The first archive inspection included `.gitignore` in the candidate list and attempted
  to open it as tar. The corrected `*.whl`/`*.tar.gz` inspection passed.
- Four wheel-smoke drafts carried source-environment assumptions: `.fn`, `get_tools()`, a
  required null key, and an expected continuation error. Read-only diagnostics established
  the installed FastMCP 3.4.7 shapes; the corrected complete smoke passed. These attempts
  used only synthetic local records, which were removed.
- The build warned that the repository-local uv cache was inside the source tree; explicit
  archive-member inspection proved no cache/build/smoke path was packaged.
- Self-improvement writes were not made because `.learnings/**` is protected.
- Required verification skipped: none.
- Contract-prohibited live Q-012/Goose/provider/model calls, push, PR, release, deploy and
  publication were not performed.
- Subagents: `0` (forbidden).
- Authority escalations: `2`, solely exact `git add` and the required local `git commit`.
- Successful package-tool invocations involving external resolution/build setup: `4`
  (pinned uv version/build, isolated venv, wheel dependency install).
- Live provider/model/Goose calls: `0`.
- Remaining risk: the fallback is intentionally conservative; multi-anchor or same-family
  actionless clusters remain separate unless existing production logical-issue grouping
  already corroborates them. This avoids fuzzy or transitive over-merging. Q-012 acceptance
  remains exclusively a Foreman decision.

No push, PR, release, deployment, publication, Campaign acceptance, or Q-012 acceptance
is claimed.
