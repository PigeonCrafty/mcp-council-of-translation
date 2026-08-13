# Campaign Foreman Review: CAMPAIGN-006-r3

## Control

- Role: FOREMAN
- Mode: STRICT_CAMPAIGN
- Decision: `ACCEPTED`
- Contract: `harness/contracts/CAMPAIGN-006-r3.md`
- Worker report: `harness/reports/CAMPAIGN-006-r3-worker.md`
- Preserved ledger: `harness/reports/CAMPAIGN-006-r2-ledger.md`
- Reviewed baseline: `8ed8d866076acab9dc22a57c6fd31d4ff6792fe4`
- Reviewed final state: `f3e9bde1b74ff4591d91b66a38558b8bebe6efab`
- Contract SHA-256: `1AA82AFAC5E8A9AFD01A1DD3D7457F58AF700ED1CF5D68B799E0688B67C9759A`
- Worker report SHA-256: `FC01B5C0163E505BC32D626EE8007D3CB0BB89610DD17CCB0768E4B56A54B45D`

## Scope and repository review

- Complete baseline-to-final diff inspected: yes; exactly four authorized paths, 160 insertions and 3 deletions.
- Commit mapping: the single required commit `f3e9bde` implements only caller-context-aware direct-answer recognition and focused regressions.
- Boundary compliance: pass. No model/schema/public argument, version/build, role, prompt, budget, tool, dependency, presentation, persistence or Policy Gate change.
- The selector receives the already existing effective `ReviewTaskV2` internally; caller packets are inspected only for bounded presence and do not become hard rules or blockers.
- All twelve protected hashes match. Git index is empty; declared Foreman/user assets and r2/r3 reports remain preserved.
- Subagents were forbidden and none were used. One local commit, zero live calls and zero external publication/deployment actions match the contract.

## Correction review

| Acceptance behavior | Independent Foreman result |
| --- | --- |
| Supplied official/binding `term_glossary` answers the corresponding existence question | PASS — suppressed with `already_answered` |
| Supplied approved `reference_translations` answers the corresponding existence question | PASS — Chinese tests and independent English probe both pass |
| Explicit marketing brand-slogan context answers the compound brand/UI question | PASS |
| Explicit UI functional-button context answers the compound brand/UI question | PASS |
| Marketing type alone, missing/vague/unspecified context remain unresolved | PASS |
| Marketing plus functional-button or mixed brand/UI context remains unresolved | PASS |
| Unrelated style/project packet does not suppress glossary/reference or semantic questions | PASS |
| Existing dedupe, generic/immaterial/limit, active-role and unresolved-status behavior | PASS |

## Campaign acceptance review

| Criterion | Foreman evidence | Result |
| --- | --- | --- |
| 1–2 | Direct glossary/reference presence cases produce `suppressed / already_answered`; missing packets remain selected. | PASS |
| 3–4 | Matching explicit single-side brand/UI cases suppress; marketing-only, vague, opposite and mixed cases stay unanswered. | PASS |
| 5 | Unrelated packet probe stays selected; existing bounded classification regressions pass. | PASS |
| 6 | Core supplied-glossary path opens no context form; missing glossary with unsupported interaction returns `NEEDS_HUMAN_REVIEW` and zero outcome calls. | PASS |
| 7 | Exact six marketing roles, deep budget path, presentation/runtime tests, five tools, 0.8.0/build v6/schema 2.2 and budgets 6/13/18 pass. | PASS |
| 8 | No accepted test removed or weakened; compile, 39 focused, 220 full, scope/diff/hashes/index all pass. | PASS |

## Independent integration verification

| Command/workflow | Result |
| --- | --- |
| `git diff --stat/name-status/check 8ed8d86..f3e9bde` and complete four-file inspection | exact authorized scope; clean diff |
| `.venv\Scripts\python.exe -m compileall -q src tests` | passed |
| Contracted seven-suite focused run | `39 passed in 2.10s` |
| `.venv\Scripts\python.exe -m pytest -q -p no:cacheprovider --basetemp .tmp/foreman-c006-r3-full` | `220 passed in 2.53s` |
| Independent seven-case Chinese/English boundary truth table | four clear supplied cases suppressed; marketing-only, conflict and unrelated-packet cases remain unanswered |
| Source FastMCP/diagnostic inspection | exact five tools; package/module 0.8.0; build v6; schema 2.2; budgets 6/13/18 |
| Marketing plan inspection | exact frozen standard six in order |
| Twelve protected hashes and final index | exact; index empty |

Fresh build/wheel verification was intentionally not repeated: r3 forbids package,
version, dependency and runtime-adapter changes, and the accepted r2 artifact/current-
FastMCP evidence therefore remains applicable. No live Goose/provider/model call was
made; Q-010 remains a required post-publication live validation gate.

## Preserved Campaign 006 evidence

- r2 PKG-033 through PKG-036 and the corrected PKG-032 are accepted together at final
  HEAD `f3e9bde1b74ff4591d91b66a38558b8bebe6efab`.
- Standard/strict marketing exact-six routing, context-before-outcome phase order,
  conservative unresolved status, deep 13/13 budget path, concise truthful presentation,
  literal V2.2 telemetry, privacy/compatibility, exact five tools, fresh 0.8.0 artifacts
  and installed FastMCP 3.4.7 wheel behavior remain accepted evidence.
- Bounded phrase recognition is intentionally conservative. Unknown wording may ask a
  redundant question, but it cannot silently manufacture an answer or bypass the
  human-review gate.

## Decision rationale

The r3 correction resolves the sole r2 acceptance failure without disturbing any
preserved Campaign behavior. Both the positive supplied-context cases and the crucial
negative/conflicting cases are independently demonstrated, and the complete 220-test
repository regression is green. F-030 through F-034 and Campaign 006 repository
implementation are accepted at `f3e9bde1b74ff4591d91b66a38558b8bebe6efab`.

This is repository implementation acceptance, not live-provider acceptance. Publication
and the pinned normal-user Goose Q-010 recipes remain before V0.8 can be declared fully
closed in real use.

## Next action

Archive the r2/r3 contracts, reports and evaluations with the accepted Foreman state;
publish the accepted implementation through the protected-main workflow; then execute
the two pinned Q-010 Goose cases: a clean explicit marketing slogan and a deliberately
mixed marketing-versus-functional-UI case.
