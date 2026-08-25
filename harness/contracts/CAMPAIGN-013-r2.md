# Campaign Revision Contract: CAMPAIGN-013-r2

## Control

- Harness role: `MAIN WORKER`
- Harness mode: `STRICT_CAMPAIGN`
- Campaign: `CAMPAIGN-013-r2`
- State: `ASSIGNED_REVISION`
- Repository: `C:\Users\GeZhu\MyMCP\mcp-council-of-translation`
- Revision baseline HEAD: `6a07f4ebc61146e60af8bb6e7456f2b144ce15a4`
- Original Campaign baseline: `44b1969677cd6b1fda63047ca514aede6609bdad`
- Preserved PKG-075 commit: `6a07f4ebc61146e60af8bb6e7456f2b144ce15a4`
- Parent contract: `harness/contracts/CAMPAIGN-013-r1.md`
- Foreman review: `harness/evaluations/CAMPAIGN-013-r1-review.md`
- Product target: `0.13.0`
- Diagnostic build target: `calibrated-evidence-council-v11`
- Persisted Review Schema target: `2.6`
- Verification receipt Schema target: `1.1`
- Acceptance authority: Foreman only
- Execution ledger: `harness/reports/CAMPAIGN-013-r2-ledger.md`
- Worker report: `harness/reports/CAMPAIGN-013-r2-worker.md`
- Commit policy: exactly four new scoped local commits, one each for PKG-076 through
  PKG-079; the complete Campaign must end with exactly five package commits including
  preserved PKG-075

This revision incorporates the complete r1 contract except where this document
explicitly overrides admission state, report paths, commit count and test allowlist.
Every frozen design rule, non-goal, acceptance criterion, verification requirement,
authority boundary and stop condition from r1 remains binding.

## Revision outcome

Complete the original five-package V0.13 Campaign without weakening its conservative
decision-support semantics. r1 correctly stopped because two legacy test files outside
its allowlist still asserted permissive completion for cases now intentionally classified
as insufficient. r2 authorizes only the bounded expectation migration needed to resolve
that conflict and then resumes PKG-076 through PKG-079.

## Admission and exact intermediate

Start only if all of the following are true:

1. `HEAD` is exactly the revision baseline and local `origin/main` is still the original
   Campaign baseline.
2. Git index is empty.
3. Commit `6a07f4e` changes exactly the three PKG-075 paths reported by r1.
4. The only uncommitted product/test intermediate is the following exact PKG-076 state;
   verify its SHA-256 values before any edit:

| Path | SHA-256 |
| --- | --- |
| `src/council_of_translation/localization/compatibility.py` | `2FE24F6BA3B4F46B280EF08CECBFEC849D16D99F29145FF4C3750F5A5D23A7EA` |
| `src/council_of_translation/localization/decision_support.py` | `AA5397C79A776028C1A4FFD6D662B71E059693F74E0F59D17432B378B1131D8F` |
| `src/council_of_translation/localization/models.py` | `ADB0D62ED3C80CC62D7E2AA4AA7493ECDBC4C32F6D607A5BFDFEAB9B4314CA85` |
| `src/council_of_translation/localization/orchestration.py` | `E3D6A299FD8AB7A9C3F4BE21F4595F70EA1A5193E60E351E19A63F7DDBA5FE66` |
| `src/council_of_translation/localization/persistence.py` | `1D29D6946930EA0BEC61475FC3B26772949D06FB7268C0FA2BCFA4FD9676026B` |
| `tests/integration/test_orchestration_v2.py` | `0F15983957553D14393A3FBE1562B723E5B28B4537E896E2E8F1DCF4ACEA6D2C` |
| `tests/integration/test_r4_reviewer_coverage.py` | `3F057728B341EDE6AFAC933830AED168DA2D4B843722EA02A8FC243ED893189F` |
| `tests/integration/test_v21_reconsideration.py` | `5A629C03DDCC3DBF1FB9B926FE90562ED36B3967A0C21A4D11871F5B7C530E72` |
| `tests/integration/test_v22_briefing.py` | `BBEA9E76BC8CB4500FFDE02AA46949B9379CFA23ED7ACF00B8FF6CD90E710AFE` |
| `tests/integration/test_v26_decision_support.py` | `48A2B4986BE8ED548C6A573DBFC21AA8E2BD7CC8B26FD6B9226B30CD221D493A` |
| `tests/unit/test_decision_support.py` | `63319E7529055195807B0F8F20AD1E5B3ED9C472666B9B57C5B5267F91B1A5BB` |
| `tests/unit/test_persistence_v2.py` | `55F5D66E3FD475EF946C1471A1FB6FB02E2D4F757405377FD87FD82D8F985A45` |
| `tests/unit/test_v22_models_persistence.py` | `C5870A8FDF112C37966E486519DF3B015AF0001A881D53951B77C429902D7846` |

The tracked Harness changes and untracked Foreman/user assets are deliberately admitted.
Preserve these Foreman assets exactly:

| Path | SHA-256 |
| --- | --- |
| `harness/features.json` | `4EA2B552B1A9F6862672AC24A0552BA0BB42330925DBCB756F153FE45FAFD245` |
| `harness/plan.md` | `12C55E19CD18193359EEA5597A6E7C97602A413FDD8CC295DF41C44F6ABED2B5` |
| `harness/progress.md` | `570B007651AFE5B977932E41B078D10A106FBD128EC37D41FDF94F7D0A550885` |
| `harness/evaluations/NEXT-CAMPAIGN-013-ASSESSMENT.md` | `60570A7A7A8476E8B74F1CF32EB3999229524B1778DFDE9DABCA6C4746A5EDFA` |
| `harness/evaluations/CAMPAIGN-013-r1-review.md` | `D02E62E52095DC238BC0CE58ED2BDB9808206273A93D00187CC4DA14B24C3602` |
| `harness/contracts/CAMPAIGN-013-r1.md` | `D11C672105A740BFD2413C9794878BF6BD1FB7011C3407406ED45B50B20A29B5` |
| `harness/reports/CAMPAIGN-013-r1-worker.md` | `11780C8CD07FA461C5DA318DD9EB7AB397BCD67356C892AB6DE79ED79C0916D8` |
| `harness/reports/CAMPAIGN-013-r1-ledger.md` | `70EC662C82F449FD33773CB7B5FC601E82E3BC1460BEC2237FCA9350C6EF72B3` |
| `harness/evaluations/CAMPAIGN-012-q014-live-r2-review.md` | `6207A0DDC7798B61C8B2003FE492BE7312186FC0F781E397730C12293CC6EE6A` |

Do not read, traverse, copy, hash, modify or stage `.learnings/**`, `reviews/**`,
`myTest/**`, the user audit report or any other user-owned untracked content. If any
admission fact or protected hash differs, stop before editing.

## Frozen semantic ruling

The r1 design is correct and must not be relaxed:

- `degraded=true` always yields decision support `insufficient`.
- A recorded runtime fallback yields `insufficient` unless it is exactly the explicit,
  non-degraded `user_delegated_to_council` path.
- Anchor suppression from a missing or ambiguous candidate anchor is degraded and must
  end with chief `需人工复核 / 是` and status `NEEDS_HUMAN_REVIEW`.
- Decision elicitation `unsupported`, `decline`, `cancel` or interaction `off` is a
  non-exempt Council fallback and must end with chief `需人工复核 / 是` and status
  `NEEDS_HUMAN_REVIEW`.
- These paths retain their bounded fallback reason, warning/degradation facts, decision
  trace and Council-selected option. Tightening release authority must not erase
  provenance or pretend that no Council decision occurred.
- Explicit non-degraded user delegation remains `supported_with_limits` and
  `COMPLETED_WITH_FALLBACK`; it is the sole exemption.
- No other support level changes chief authority.

## Allowlist override

All r1 authorized paths remain authorized. Add exactly these two test paths for PKG-076:

- `tests/integration/test_r3_outcome_suppression.py`
- `tests/integration/test_r3_workflow.py`

No other scope expansion is authorized. The two files may change only assertions and
test names/comments needed to express the frozen V0.13 behavior. Do not weaken or remove
checks for option identity, Council outcome, sampling/elicitation counts, fallback reason,
warnings, degradation, privacy, persistence or bounded suppression provenance.

Authorized new Worker evidence paths are:

- `harness/reports/CAMPAIGN-013-r2-ledger.md` (new, untracked/unstaged)
- `harness/reports/CAMPAIGN-013-r2-worker.md` (new, untracked/unstaged)
- `.tmp/campaign013-r2-worker/**` for bounded temporary verification only; remove before
  handoff

## Sequential work orders

### PKG-076 / F-060 — finish coherence and compatibility

1. Continue from the admitted intermediate; do not discard or recreate PKG-075.
2. Migrate all seven stale fallback assertions in the two newly authorized files.
3. Add direct assertions for `decision_support.level == "insufficient"`, coherent chief
   `需人工复核 / 是`, and `status == "NEEDS_HUMAN_REVIEW"`.
4. Preserve the outcome trace, selected option, warnings, fallback and degraded fields.
5. Resolve the already-observed metadata receipt failure only within the original r1
   authorized PKG-076/PKG-077 boundaries; do not infer absent metadata.
6. Run the complete PKG-076 matrix and the full suite. Commit exactly once only when the
   seven migrated regressions and all PKG-076-owned assertions pass.

### PKG-077 / F-061 — presentation and receipt 1.1

Execute the complete original r1 work order. Resolve the expected receipt/schema
assertions, preserve text/structured equality and retrieval purity, then commit once.

### PKG-078 / F-062 — executable 30-case Golden

Execute the complete original r1 work order. Existing 24 cases remain unchanged; add six
production-executed calibration cases, prove all eleven aggregate metrics and negative
mutation controls, then commit once.

### PKG-079 / F-063 — V0.13 release migration

Execute the complete original r1 work order. Update identifiers/docs and perform the
canonical pinned lock refresh with exact root-only drift, then commit once.

## Required verification

In addition to every r1 required check, report:

1. Exact migration evidence for all seven old assertions, including both anchor
   suppression variants, metadata history and all four interaction actions.
2. An explicit counterexample showing non-degraded user delegation still remains
   `supported_with_limits` plus `COMPLETED_WITH_FALLBACK`.
3. Full-suite recovery from the independently reproduced `467 passed, 10 failed` state
   to zero failures without deleting or deselecting tests.
4. Exact baseline-to-final audit from the original baseline and revision-baseline audit
   from `6a07f4e`; the only r2 allowlist delta is the two named legacy tests.
5. Exactly four r2 commits and exactly five total Campaign package commits.
6. All protected hashes, an empty index, fresh artifacts, installed-wheel behavior and
   every original final invariant.

Use a unique repository-local pytest basetemp/cache to avoid the known Windows temp-root
permission defect. Do not hide a failure through deselection, conditional skips or
permissive compatibility behavior.

## Authority and stop conditions

Local tests, build, exact temporary cleanup, dependency sync and four scoped local commits
are authorized under the same boundaries as r1. No push, remote mutation, PR, release,
publication, deployment, Goose/provider/model call, credential change or Q-015 action is
authorized.

Stop with `BLOCKED` if the correction requires changing the frozen semantic ruling,
editing another unlisted path, losing provenance, reducing test coverage, changing
public tools/routing/prompts/budgets/concurrency, introducing prose/score inference, or
violating any inherited r1 stop condition.

## Handoff

Leave the r2 ledger and Worker report untracked/unstaged and the Git index empty. In chat,
start with exactly `READY_FOR_REVIEW` or `BLOCKED`, then report contract hash, baseline and
final HEAD, all five total Campaign commits, path scope, migrated regression evidence,
package/final verification, artifact hashes, protected hashes, subagent/authority/
dependency/live-call counts, skipped checks and remaining risks. Do not claim Campaign
acceptance, publication or Q-015 completion.
