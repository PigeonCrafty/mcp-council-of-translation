# Correction Work Order: CAMPAIGN-002-r3

## Control

- Role: WORKER
- Mode: STRICT_SEQUENTIAL
- State: ASSIGNED
- Repository: `C:\Users\GeZhu\MyMCP\mcp-council-of-translation`
- Exact baseline commit: `f7a4f23865383d52dede37f95de091932918090c`
- Baseline subject: `Expose readable decision form titles`
- Parent revision: `CAMPAIGN-002-r2`
- Required Foreman review: `harness/evaluations/CAMPAIGN-002-r2-review.md`
- Worker report: `harness/reports/CAMPAIGN-002-r3-worker.md`
- Commit policy: scoped local correction commit(s), no push/PR/release/deployment/credential/Goose changes
- Subagents: forbidden
- Acceptance authority: Foreman only

Read `AGENTS.md`, Harness plan/features/progress, this contract, the r2 Foreman review, and the r2 Worker report completely before editing.

## Admission gate

Verify exact HEAD, empty index, protected dirt only, all hashes below, and a fresh 146-test baseline before edits. Stop `BLOCKED` if any value differs.

| Protected asset | SHA-256 |
| --- | --- |
| `harness/plan.md` | `B7955061A7519D9BEA92422DF04A5B31A1A51E7015C6C3B59D2727B331072CE6` |
| `harness/features.json` | `AB58536DE655B4D44A18A8C636F843C49AA29BE251B65A89CFC8B8DDF6FC39D9` |
| `harness/progress.md` | `5C2F940BC62FE8E19A615AD6E29D21C94AE7B6B30C4163542544726709D33823` |
| `harness/contracts/CAMPAIGN-002-r1.md` | `D58590B24E5CF2E4E7F7116F9E9F7B4D621009B6D3986CCA9A7784ECC1EC40BE` |
| `harness/contracts/CAMPAIGN-002-r2.md` | `C71FF5EB63630715B32D0AA2C1ED50A3E20121FA7F1AEC9D708777A2850977B6` |
| `harness/evaluations/CAMPAIGN-002-r1-review.md` | `9DCBE1F727F8B38FB1B2996982015AA71E64A6A422BA05ABCC4DFE45B6226453` |
| `harness/evaluations/CAMPAIGN-002-r2-review.md` | `D4EF53646A3BDB41E976C5B127FD49D7AE1C0F2E1F1D9A02B23C52AE456F2894` |
| `harness/reports/CAMPAIGN-002-r1-ledger.md` | `10AD5BFB19B4DA3F94F06608EBBA98EF21977DED66ABAD016642E2085D37BA90` |
| `harness/reports/CAMPAIGN-002-r1-worker.md` | `E552F5A6B9FE3047057AC29E4CE35EBF91CD476ED758B197B4DA6921C67366D4` |
| `harness/reports/CAMPAIGN-002-r2-worker.md` | `F3DDB096C5CAA77A2AE055515FC9EEE9DEFD2566B48B7BF3538C7B0195145040` |
| `.learnings/LEARNINGS.md` | `22F939E6F980DF52487AAFE97EDCA9B90CF3931DDB7A31BF8A5BBB8F052E658F` |
| `.learnings/ERRORS.md` | `F99EB75886781958BF5AE6DCF844FD476CBCA45937896A25EE3B2E9D6CD34F0A` |
| audit markdown | `B48073E063C4C9F34E0B6B4DAE94E80079EAAAD3B2F8E273DD60B2F25F6ABD76` |

Hash this r3 contract on admission and preserve it byte-for-byte. Preserve `reviews/**`, `.learnings/**`, all prior Harness artifacts, audit markdown, and `myTest/` if present. Only the r3 Worker report may be added under Harness.

## Goal

Close the final two untrusted-output/transparency gaps while preserving all accepted r1/r2 behavior:

1. raw reviewer `action` prose can never become a selectable outcome, including legacy, missing, invalid, or incomplete V2.1 classification paths;
2. a meaningful DecisionPoint suppressed because a local replacement anchor is missing or ambiguous must leave bounded persisted provenance and a truthful compact degraded/fallback result.

## Allowed files

- `src/council_of_translation/localization/clustering.py`
- `src/council_of_translation/localization/models.py` only for a minimal bounded suppression-provenance field if needed
- `src/council_of_translation/localization/orchestration.py`
- `src/council_of_translation/localization/policy.py` only if required to include suppression metadata in the existing Policy Gate result
- focused unit/integration tests
- `README.md`, `AGENTS.md`, `docs/v0.4-architecture.md`, `docs/v0.4-tool-contract.md` only if implemented suppression semantics require clarification
- `harness/reports/CAMPAIGN-002-r3-worker.md`

## Forbidden scope

- Other production modules, public tools/arguments, dependencies, version/schema/build, budgets, roles, persistence location/privacy, sampling parser, discussion, matrix weights, reconsideration, compact fields, output modes, or provider behavior
- Reverting readable enums, issue-local anchors, full-candidate reconstruction, custom UI, majority voting, translation edits, extra calls, or budget expansion
- Protected assets, external mutations, push/PR/release/deployment

## Frozen correction behavior

### No action promotion

- Only a validated finding with `finding_kind="choice"` and a non-empty bounded string `proposed_value` may contribute a proposed outcome.
- The issue-local current outcome may still come from a consistent bounded `candidate_span` under the accepted r2 rules.
- `finding_kind="issue"`, `finding_kind="affirmation"`, missing/invalid classification normalized to `issue`, and `choice` with missing/invalid/empty/overlong `proposed_value` must never contribute `action` to `candidate_actions`, RolePosition option identity, DecisionOptions, form values, or adjudication.
- Raw `action` remains evidence/advice and may influence the outer execution checklist only through the existing issue finding semantics; it is never a selectable value.
- V1/V2.0 records remain readable. Read compatibility does not imply reactivating obsolete action-based decision generation.
- Two issue-only findings with different action instructions produce no DecisionPoint and no elicitation request.

### Explicit reconstruction suppression

- When a pre-validation DecisionPoint has at least two distinct candidate outcomes but a non-current option cannot be reconstructed because its candidate anchor is `missing_candidate_anchor` or `ambiguous_candidate_anchor`, persist bounded, content-free suppression provenance.
- The full record's existing Policy Gate area or a minimal typed V2.1 field must identify the affected `issue_id`/`decision_id` and one of the allowed reason codes. Do not store candidate/source text in that provenance.
- Surface a bounded compact warning such as `decision_suppressed:ambiguous_candidate_anchor`; deduplicate it.
- Set `degraded=true`; include `decision_validation_degraded` in `fallback_reason`; return `COMPLETED_WITH_FALLBACK` unless an existing stronger state requires `NEEDS_HUMAN_REVIEW` or `RETURNED_PENDING`.
- Do not treat a deterministic hard-constraint rejection such as placeholder loss as runtime degradation. It remains normal Policy Gate invalidation/blocking behavior.
- If at least two other valid outcomes remain, the readable DecisionPoint may still be elicited; suppression provenance/warning remains truthful for the dropped option.
- Metadata history must not gain source/candidate/proposal/user/model prose. Existing allowlist behavior remains.

## Acceptance criteria

1. Two valid structured reviewer envelopes whose findings omit `finding_kind/proposed_value` and contain different long action instructions produce zero DecisionPoints, zero elicitation requests, and no action text in any selectable structure.
2. Explicit `finding_kind="issue"` findings with actions, invalid classification normalized to issue, and `choice` findings with empty/non-string/overlong proposals never promote action.
3. A valid concrete `choice` proposal plus issue/affirmation advice retains r2 current/proposed readable outcomes without adding advice as a third option.
4. V1/V2.0 stored records remain readable and sampled findings remain conservative/non-blocking.
5. The repeated-anchor production workflow persists `ambiguous_candidate_anchor` suppression provenance, exposes a bounded warning, sets `degraded=true`, includes `decision_validation_degraded`, and cannot report unqualified `COMPLETED`.
6. A missing-anchor production workflow does the same with `missing_candidate_anchor`.
7. A proposal rejected for actual `{count}` loss does not set anchor-degradation warnings merely because the option is invalid.
8. Suppression provenance is bounded, deduplicated, content-free, schema-2.1 serializable, visible in full/compact as specified, and absent from metadata except existing safe status/degraded disposition.
9. Exact readable enum values, per-field round trip, long document, unrelated/affected placeholders, collision handling, delegation, stale/malformed interaction, influence, policy, reconsideration, compact output, coverage, continuation, persistence/privacy, review-only, five tools, identifiers and 6/10/14 budgets remain green.
10. Full suite, focused production counterexamples, compile, fresh sdist/wheel, isolated wheel smoke, diff and protected hashes pass.

## Required verification

Run:

```powershell
python -m compileall src tests
.venv\Scripts\python.exe -m pytest -q --basetemp .tmp\campaign002-r3-pytest -p no:cacheprovider
```

Run a named focused suite and print exact Core outputs for:

- omitted classification plus two action instructions;
- explicit issue actions;
- invalid classification;
- choice with empty/non-string/overlong proposal;
- valid mixed choice/issue/affirmation control;
- repeated-anchor persisted record;
- missing-anchor persisted record;
- actual protected-token-loss control;
- readable schema control.

Build and smoke fresh artifacts:

```powershell
$env:UV_CACHE_DIR='.tmp\campaign002-r3-uv-cache'; uv build --out-dir .tmp\campaign002-r3-dist
```

Then run `git diff --check f7a4f23865383d52dede37f95de091932918090c..HEAD`, changed-file/status checks, complete correction diff inspection, and all protected hashes. Record exact commands, exits, counts, commit/file scope, skips, escalations, subagent count zero, live-call count, and external mutation count.

## Stop conditions

- Admission differs.
- Fix requires a public-surface, dependency, schema-version, budget, provider, custom UI, or persistence-privacy redesign.
- Explicit suppression cannot be represented without storing private text or weakening normal deterministic constraint handling.
- Required test/build evidence cannot be established.

Stop `BLOCKED` instead of weakening the frozen outcome contract.

## Handoff

Write `harness/reports/CAMPAIGN-002-r3-worker.md`. Start chat with `READY_FOR_REVIEW` or `BLOCKED`; include baseline/final SHA, commits/files, focused/full/build evidence, raw-action and suppression outputs, protected state, counts, and remaining risk. Do not push or claim acceptance.
