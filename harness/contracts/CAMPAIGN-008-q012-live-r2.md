# Live Gate Protocol Correction: CAMPAIGN-008 Q-012 r2

## Control

- Role: `FOREMAN`
- Harness mode: `STRICT_CAMPAIGN`
- Gate: `Q-012` value-first Council live usefulness and non-repetition evidence
- Corrects configuration guidance in:
  `harness/contracts/CAMPAIGN-008-q012-live.md`
- Published `main` under test:
  `e3d3de275915088c1430a243dfd9c2e410cbc58a`
- Product/build/schema remain `0.10.0` / `evidence-value-council-v8` / `2.4`

## Reproduced admission failure

All three initial attempts completed no durable review and returned
`review record write failed`. The configured evidence directory
`.tmp\q012` did not exist after the attempts. Goose's persisted extension record showed
`envs: {}` with `COUNCIL_REVIEW_CONCURRENCY` and `COUNCIL_REVIEWS_DIR` under
`env_keys`, so their values are supplied through Goose's protected environment-value
store rather than as literal YAML values. Concurrency reached the server as
`3/configured`; the review directory did not resolve to the issued absolute path.

The protected value itself is not readable from `config.yaml`, so the bounded diagnosis
is a stored path-value mismatch: stale, empty, or malformed rather than the issued raw
absolute path. The strongest concrete hazard is that r1 showed the Windows path with YAML
quotes. Those quotes are YAML delimiters only. If copied into a Goose Desktop
environment-value input, they become part of the value. A value beginning with `'C:\`
is not a fully qualified Windows path and resolves beneath the process working directory
with an invalid embedded drive separator, which makes the atomic record write fail.

This is a live-protocol/configuration defect, not evidence of a Council sampling,
deliberation or V0.10 product defect. The three failed attempts are inadmissible for
Q-012 and do not count as Cases A, B or C.

## Correct Goose Desktop values

Remove the existing stored entries, then re-add them in the extension's
environment-variable editor exactly as raw text, with no single quotes, double quotes,
backticks or surrounding whitespace:

```text
COUNCIL_REVIEW_CONCURRENCY
3

COUNCIL_REVIEWS_DIR
C:\Users\GeZhu\MyMCP\mcp-council-of-translation\.tmp\q012
```

The evidence directory has been pre-created with inherited write permissions. Save the
extension, fully exit all Goose windows so every old STDIO child process terminates, and
then start Goose again. Do not edit `config.yaml` manually and do not change the normal
extension command.

## Corrected run order

1. Run the r1 Case A instruction in a fresh Goose session.
2. Admission still requires package/module `0.10.0`, build
   `evidence-value-council-v8`, schema `2.4`, and concurrency `3/configured`.
3. If Case A again returns `review record write failed`, stop. Do not spend provider
   calls on Cases B or C. Report the error for a second configuration diagnosis.
4. If Case A returns a valid `review_id`, confirm that a corresponding JSON file appears
   under `.tmp\q012`, then run Cases B and C in fresh sessions without any configuration
   change.
5. Return only the new valid IDs as A, B and C. The initial failed attempts remain
   excluded.

All case inputs, output requirements, acceptance criteria, mutation boundaries and
provider/model invariants from the r1 protocol remain unchanged.
