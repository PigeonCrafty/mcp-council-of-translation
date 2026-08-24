# Foreman Live Review: Q-003 Desktop/CLI Client Parity r1

## Control

- Role: `FOREMAN`
- Harness mode: `STRICT_CAMPAIGN`
- Decision: `CHANGES_REQUESTED`
- Quality gate: `Q-003` — Goose Desktop and interactive CLI evidence
- Contract: `harness/contracts/Q-003-desktop-cli-live-r1.md`
- Contract SHA-256:
  `0811B9A56CF0EBB3D20B9D2B1843BF2FA4ED66F045C009189591F2FCFF623234`
- Published protected `main`: `617b696c94624988f03a64ab58e1d42a66697546`
- Review date: 2026-08-24 Asia/Shanghai

## Evidence policy and deviations

The user identified one run as Goose Desktop and one as the interactive Goose CLI and
returned their complete client responses. No screenshot was retained, so r1's visual
client-identity requirement is not satisfied. The Foreman independently loaded the two
fresh persisted Schema 2.4 JSON records and used those records—not the outer agent's
summary—as telemetry truth.

Both records were written to the previously configured `.tmp/q012` directory rather than
the r1-requested `.tmp/q003-client-parity` directory. Their fresh IDs, exact task notes,
record hashes and user client attribution make them unambiguous. This storage deviation
does not change their runtime meaning, but it confirms that Goose retained prior
extension environment state.

No credential, token, full Goose configuration, screenshot, source-code change or raw
record content is copied into Harness. The raw records remain ignored local evidence.

## Desktop evidence — accepted for reuse

- Review ID: `20260824T014417482642Z_da47683d8f04`.
- Raw record SHA-256:
  `C4BDF07819B4B2C414B00FC03749FF69F8E7A439A7580E547D2353F1859452A2`.
- Version/build/schema: `0.10.2` / `evidence-value-council-v8.2` / `2.4`.
- Briefing: requested once, six fields asked, action `accept`, and every accepted answer
  has `user_briefing` provenance. The normalized content type is `ui`, location is `ui`
  and context confidence is `full`.
- Phase order: accepted briefing precedes preflight, planning and independent review.
- Runtime: one accepted briefing elicitation, six successful samples of budget 13, full
  reviewer coverage, zero unavailable samples and zero parse failures.
- Concurrency: configured limit 3, observed peak 3, two batches.
- Result: `COMPLETED`, `degraded=false`, no warnings and no fallback.
- Presentation: 346 Unicode code points, exactly five sections, six roles grouped as
  confirmation-only coverage, chief disposition last and `suggested_translation=null`.

The persisted record proves the complete Desktop-side product path. The absent screenshot
prevents r1 acceptance but does not require the Desktop run to be repeated under r2.

## CLI evidence — r1 failure

- Review ID: `20260824T014635498220Z_cb108a4de83e`.
- Raw record SHA-256:
  `8DAC331013C2D3DAD3D72875D12A1205A99E9B1A1A4EDBD35C9CC09C992DDA8D`.
- Version/build/schema: `0.10.2` / `evidence-value-council-v8.2` / `2.4`.
- Briefing: requested once and six fields asked, but action is `error`; accepted answers
  and answer provenance are empty.
- Runtime: one errored elicitation, zero sampling calls, zero completed reviewer samples,
  coverage `not_applicable` and concurrency peak zero.
- Result: `RETURNED_PENDING`, `degraded=true`, warning
  `briefing_not_accepted:error`, fallback `briefing_error` and truthful human review.
- Presentation: five sections and null suggested translation correctly expose that review
  did not start; unavailable roles are not misrepresented as successful coverage.

The CLI result fails r1 criteria 2, 4, 5, 6 and 8. It is nevertheless a useful and
truthful negative result: the server stops before sampling rather than fabricating form
answers or a Council decision.

## Root cause and scope decision

The evidence does not establish a Council orchestration defect. It establishes that r1
made an unsupported Foreman assumption: native MCP elicitation would render and round-trip
identically in Goose Desktop and the interactive CLI. Desktop supports that path; this
CLI run returned an elicitation error and then exposed a conversational request for the
same context.

Q-003's durable requirement is evidence that both normal Goose clients can use the MCP,
not proof that both clients implement the same native form widget. The bounded correction
is therefore an evidence-protocol revision, not a production-code Campaign: preserve the
accepted Desktop record and test the CLI's explicit-context fallback after the truthful
pending record.

## Decision

`CHANGES_REQUESTED`.

Q-003 remains `partial_live_evidence`. Issue r2 for one CLI-only retry using an explicit
rich context packet with `briefing_mode=auto`. Accept the gate only if that new CLI record
completes real reviewer sampling with full coverage, clean status, bounded calls,
five-section review-only presentation and a unique persisted CLI note. The r1 pending
record remains part of the evidence chain and must not be overwritten or reclassified as
a successful review.
