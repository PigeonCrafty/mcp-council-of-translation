# CAMPAIGN-010-r1 Worker Report

## Control

- HARNESS_ROLE: `WORKER / MAIN WORKER`
- HARNESS_MODE: `STRICT_CAMPAIGN`
- Campaign/contract: `CAMPAIGN-010-r1` / `harness/contracts/CAMPAIGN-010-r1.md`
- Contract SHA-256: `E09A31F3E544619D55B6A0DE456509E0F549DA694361C27925F1BFF2821535DE` (exact match before edits and at handoff)
- Exact admitted baseline: `9cd0f317ca6ecedef3477ac322c73189d430ded8`
- Final HEAD: `144ecebb6bfbd507ccdfb09a9b87efac3d59e9e1`
- Execution order: PKG-055, then PKG-056
- Subagents: `0` (forbidden by contract)
- Live Goose/provider/model calls: `0`
- Pushes, PR operations, releases, deployments, credential changes and Goose changes: `0`

The pigeon-harness skill, common protocol and Worker protocol were read completely. AGENTS.md, the contract, plan, features, progress, Q-012 live trigger/protocol, both Campaign-009 contracts, prior Worker reports/ledger and both Foreman reviews were read before implementation. Repository artifacts were the source of truth.

## Admission gate

- HEAD matched the exact baseline and the Git index was empty.
- Admitted dirty/untracked assets were recorded and preserved:
  - modified `harness/features.json`, `harness/plan.md`, `harness/progress.md`;
  - untracked `.learnings/ERRORS.md`, `.learnings/LEARNINGS.md`, active contract, Q-012 review, user audit and `reviews/20260810_145151.json`.
- Every contract-listed protected hash matched before edits.
- Admission compile: `.venv\Scripts\python.exe -m compileall -q src tests` -> exit 0.
- Admission regression with an explicit writable `--basetemp`: exactly `286 passed in 4.34s`.

## Commits and changed files

1. `38689f2` — `fix: project primary review work items`
   - `src/council_of_translation/localization/digest.py`
   - `tests/integration/test_v101_live_shaped_value.py`
   - `tests/integration/test_v24_presentation.py`
2. `144eceb` — `chore: release council review 0.10.2`
   - `AGENTS.md`
   - `README.md`
   - `docs/v0.4-tool-contract.md`
   - `pyproject.toml`
   - `src/council_of_translation/__init__.py`
   - `tests/integration/test_tool_surface_v2.py`
   - `tests/integration/test_v10_release_contract.py`
   - `tests/unit/test_persistence_v2.py`
   - `uv.lock`

Baseline-to-final scope is exactly these 12 authorized paths. `git diff --check 9cd0f317ca6ecedef3477ac322c73189d430ded8..HEAD` passed. No other production, test, dependency, Harness or user path was committed.

## PKG-055 — primary human work-item projection

The primary-only projection now derives bounded work-item identity from existing structured clusters without mutating them:

- Deterministic failures use immutable check provenance and bounded protected literals. Known placeholder, URL, tag, numeric, Markdown, DNT, required-literal and forbidden-literal outcomes render as natural Chinese rather than raw check telemetry.
- Reviewer corroboration attaches to a deterministic item only through an exact protected span or independent structured evidence carrying the same anchor. A whole source sentence that merely contains the token cannot absorb a distinct semantic reversal.
- Model-only cross-category clusters group only when normalized source spans, candidate spans and the same non-empty concrete replacement all match. The projected repair appears once and bounded distinct consequences remain readable.
- Duplicate must/should/execution lines for an already rendered work item are suppressed. Final disposition, minority conditions, coverage/unavailable risks and degradation remain outside this suppression.
- No sampling, elicitation, orchestration, clustering, value-metric or structured-record path changed.

Exact regression evidence:

- Sanitized Case B reproduces three deterministic `{count}` failures whose raw messages omit or expose the literal, reviewer spans `{count}` and `Delete {count} files?`, and a separate `cannot` / `可以` reversal. The chief primary section contains one natural placeholder repair and one reversal repair, exposes none of `explicit do-not-translate literal missing`, `explicit caller hard constraint violated`, `missing=['{count}']` or `required_literal:{count}`, ends in human review and leaves the full record byte-equivalent across rendering.
- Sanitized Case C uses correctness and language-choice clusters with exact `only use your location while the app is open` / `使用您的位置信息` anchors and the same concrete replacement. The primary chief requests that replacement once, retains both accuracy and user-impact consequences, emits no duplicate execution instruction, and leaves digest, clusters and value metrics unchanged.
- Negative controls passed for two different required literals, placeholder loss plus URL loss, whole-sentence placeholder containment plus semantic reversal, and identical spans with different repair actions.
- Case A still renders one six-role confirmation line and unqualified clean disposition.
- Affected presentation/privacy/compatibility/value/Golden selection: `57 passed in 1.39s`.
- Post-change full suite before migration: `291 passed in 3.45s`.
- Static search found no sampling or elicitation call site in `digest.py`.

## Golden Corpus

- Golden pytest: `4 passed in 0.35s`.
- Executable aggregate: exact `18/18`, failed IDs `[]`.
- Scripted calls: `113` sampling, `4` elicitation.
- All eight frozen aggregate rates remained `1.0`: critical recall, false-positive-free, contribution-kind, conflict detection, user authority, chief consistency, call-budget and discussion marginal-value accuracy.

## PKG-056 — V0.10.2 migration and package proof

- Package/module version: `0.10.2`.
- Diagnostic build: `evidence-value-council-v8.2`.
- Schema: unchanged `2.4`.
- Public tools: exactly five in frozen order.
- Defaults: review-only, Council adjudication, briefing auto, independent reviewer concurrency 3/default with max 3.
- Sampling budgets: unchanged `6/13/18`.
- Documentation now describes the primary human work-item projection and explicitly states that full checklist, clusters, metrics and structured evidence remain unchanged.

Pinned canonical lock operation used `uv 0.12.3` and repository-local temporary cache/tool directories after the host global cache denied access:

```text
uvx --from uv==0.12.3 uv --version
uvx --from uv==0.12.3 uv lock --refresh
```

- Lock diff: exactly editable root `0.10.1 -> 0.10.2` (`1` insertion / `1` deletion).
- Lock revision: `3`.
- Package count: `78`.
- Preserved upload-time entries: `586`.
- Final `uv.lock` SHA-256: `31F0173F9325A4CA1C5BF95BB281B75E00374C8A241A19DFC38AB39C95F5347D`.

Fresh pinned artifacts:

- `council_of_translation-0.10.2-py3-none-any.whl`: 92,415 bytes; SHA-256 `7EF8BF44A731D26D4D9768D03F5D5B4F50B7254E4F44AEEC920DC03FAE1F62D7`.
- `council_of_translation-0.10.2.tar.gz`: 86,059 bytes; SHA-256 `5FB012F2C0670588F3C71645DFB1DB3915EA6621D9CB8997677CADCA7C6CAD13`.
- Wheel had 29 members and neither wheel nor sdist contained build/cache/smoke/Q-012 temporary paths.

Installed-wheel smoke:

- Python `3.12.9`; current resolved FastMCP `3.4.7`.
- Distribution/module `0.10.2`; build `evidence-value-council-v8.2`; schema `2.4`.
- Called all five registered tools: `review_translation`, `continue_review`, `view_review_record`, `list_review_records`, `get_server_info`.
- Confirmed budgets `6/13/18`, review-only/null suggested translation, one clean confirmation group and a 432-code-point primary response.
- Confirmed text plus structured content on review, continuation and view results.
- All local pytest/build/cache/tool/venv/smoke-record temporary directories were removed after evidence capture.

## Integrated final verification

- Final compile: `.venv\Scripts\python.exe -m compileall -q src tests` -> exit 0.
- Final complete suite: `291 passed in 3.88s`.
- Final named Campaign selection: `90 passed in 1.52s`.
- Exact server-info probe confirmed five tools, `0.10.2`, v8.2, schema 2.4, review-only, budgets 6/13/18 and concurrency 3/3.
- AST dead-import scan of changed production modules: none.
- Baseline-to-final scope audit: exactly 12 authorized paths.
- Baseline-to-final diff check: passed.
- Final index: empty.
- Worker report remains untracked and unstaged as required.

## Protected assets

Every listed value matched admission again at final handoff:

- contract: `E09A31F3E544619D55B6A0DE456509E0F549DA694361C27925F1BFF2821535DE`
- plan: `C5AB434DF90B2F0FC2E95545C6ED3A4BD0A8BD8255F691C0105169DD346DD50D`
- features: `D2FCE49FF59059218D12F02F8080B8E2A1478D76CD1DB43A93229FC497ADC2D0`
- progress: `75FFA69617A952B8C75DAEB9E9788D1D1920844094BA3D522BE6C8CE1C84A82E`
- Q-012 live review: `7BF0FEC690540DFD19DC9380ECC2726A14933B0AC3C3284AF35FE2738E60B778`
- Q-012 protocol: `53C7C2FBD6140B84FF9365304F18CD3BF8F28DDB3738AD4222303FFD71B8261F`
- publication CI review: `39462F9DA32A9B4497AE92DE61E9EFE182CA08DC832E866B20BF4134E3A24391`
- raw Q-012 A/B/C records: `3652A7F55AEB1C25BAA34905C2E922957C6B184A58DF80CC513A5B1D20820F41`, `80C7A47D1B0330A40A824B47C718A92B9C84C399FB548D9EA60E90320CDC5CEF`, `07EB4B9E331B188B035D3397F6C2E418F8CDF3AB2E6872E8236EE914F773857B`
- learnings/errors: `52DC1BA8043481911C0DEABB3AC882504D9CBE8BB63D60F391C188586A230DF0`, `F99EB75886781958BF5AE6DCF844FD476CBCA45937896A25EE3B2E9D6CD34F0A`
- user audit: `B48073E063C4C9F34E0B6B4DAE94E80079EAAAD3B2F8E273DD60B2F25F6ABD76`

The final admitted dirty/untracked set is unchanged except for this required untracked Worker report. No raw Q-012 record was read into source/tests/docs or copied into committed fixtures.

## Incidents, authority, external work and skipped checks

- One read-only combined `rg` command returned code 1 because its optional search had no matches; the preceding protocol read succeeded.
- Two focused pytest attempts hit inaccessible host temp roots (pytest default and `C:\Windows\Temp`). All selections were rerun successfully with exact repository-local temporary roots, which were then removed.
- The first non-elevated Git staging attempt failed on `.git/index.lock`; both exact scoped commits then succeeded with bounded Git authority.
- Host global uv cache access failed; contract-authorized repository-local temporary uv cache/tool roots succeeded and were removed.
- Three installed-wheel smoke assertions initially used the source environment's FastMCP 2.x enumeration API or full-record field names against the compact response. Read-only inspection established FastMCP 3.4.7's `list_tools()` API and compact keys; the corrected complete smoke passed without product changes.
- The self-improvement skill was read after command failures. Its requested `.learnings/**` writes were skipped because those files are protected by this contract.
- Authority escalations: `2`, both exact contract-required local Git commits.
- Successful isolated dependency command invocations after cache fallback: `5` (pinned uv acquisition/version, lock refresh, fresh build, Python 3.12 venv, wheel/dependency install). Provider/model/Goose external calls: `0`.
- Required verification skipped: none.
- Contract-prohibited live Q-012 revalidation, push, PR, release, deployment and publication were not performed.

## Remaining risks

- The projection deliberately uses exact bounded anchors, deterministic provenance and exact replacement identity. Semantically similar but structurally unprovable repairs remain separate rather than introducing fuzzy merging.
- Provider wording was not re-tested because live model/Goose calls are forbidden. Normal-user usefulness and Q-012 acceptance remain Foreman gates.
- This report does not claim Campaign acceptance, Q-012 acceptance, publication or project completion.
