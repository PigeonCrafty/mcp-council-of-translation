# CAMPAIGN-014 Q-016-r3 Foreman Review

- Decision: `CHANGES_REQUESTED`
- Role/mode: `FOREMAN / STRICT_CAMPAIGN`
- Contract: `harness/contracts/CAMPAIGN-014-q016-external-r3.md`
- Contract SHA-256:
  `2A39143062D068F5103C9779797E8F9732876283B5C44D71F2DB9C8DC199BE10`
- Worker report: `harness/reports/CAMPAIGN-014-q016-r3-worker.md`
- Worker report SHA-256:
  `F707CAB42B282A9E8C20EED2FF109BB340545B367858022FBD4213AC6875351D`
- Failure ledger: `harness/reports/CAMPAIGN-014-q016-r3-ledger.md`
- Failure ledger SHA-256:
  `89D9A9BB392CF012EC57E90DAA9B85343B0EC67D86990F4AB1629CA500403515`
- Published product commit: `9d8f1f987efe73946377883e6ad3a681abe11989`
- Review date: 2026-08-28 Asia/Shanghai

## Boundary and hygiene

The Worker preserved the shared historical HEAD
`9d23ed01f94be2ef0c724b3e0a3e7e1beba75c09`, left the index empty, created no product
diff or commit, and kept the report and ledger untracked/unstaged. Cases B/C were not
rerun, Goose/provider/model calls were zero, and all temporary assets were removed.

The r3 contract's embedded baseline `26e2822…` was historical by execution time. The
user launch baseline and fresh protected-main clone both resolved to
`ab912c41d6deebeab440d8be9557371be2580dff`; this disclosed governance drift did not
change the immutable product audit target.

## A3 decision — replacement required

The Worker correctly materialized equal 16,000-character source/candidate values in an
isolated CPython 3.12.9/FastMCP 3.4.7 client and launched the exact pinned public Git
command once. The `uvx --refresh` process updated and built the product but did not
complete MCP initialization within 240 seconds. There were zero tool dispatches,
sampling callbacks, elicitation callbacks, records or retries.

This is an evidence-run setup failure, not a demonstrated product defect. It supplies no
A3 receipt, input diagnostics, bounded-prefix report, truncation fallback or terminal
coherence and therefore cannot satisfy Part I. The next revision must provision the
published package before the single MCP transport attempt, verify direct-URL provenance,
and launch the already-installed console script directly.

## Independent re-audit decision

The Worker independently audited exact public commit `9d8f1f9…`: compile passed, the
required focused selection passed `92/92`, and the full suite passed `575/575`. The
Foreman independently reran compile, the same focused selection (`92 passed`) and the
full suite (`575 passed`). Source/test inspection supports each Worker disposition:

- `AUD-001`: `CLOSED`
- `AUD-002`: `CLOSED`
- `AUD-003`: `CLOSED`
- `AUD-004`: `CLOSED`
- `AUD-005`: `CLOSED`
- `AUD-006`: `CLOSED`
- `AUD-007`: `CLOSED`

These seven dispositions and their fresh test evidence are accepted for carry-forward.
They must not be rerun in r4 unless the bounded documentation/test correction changes
an audited assertion.

## Targeted Discussion documentation decision

The separate documentation check is `OPEN`. Published README and architecture text say
there is one bounded discussion round, and production contains one model-sampling call,
but no public documentation explicitly says that Targeted Discussion is one bounded
model sample simulating cross-role deliberation and is not peer-to-peer communication
among autonomous agents. The wording is not false; it is less explicit than the frozen
audit-remediation contract requires.

This is a bounded documentation-contract defect. r4 may change only the README,
architecture wording, and one exact release-contract regression test. It does not reopen
the Council architecture, runtime behavior, schema, version, dependency or tool surface.

## Gate state

Q-016 remains `CHANGES_REQUESTED`, not `BLOCKED`: both failures have bounded corrections
that need no user decision, new product authority or redesign. Carry forward unchanged:

- Case B: `20260828T024458690799Z_8badddd7158f`
- Case C: `20260828T024543336644Z_2422acf98836`
- the r2 Goose `CLIENT_LIMIT` boundary evidence;
- `AUD-001` through `AUD-007` as `CLOSED`;
- compile, focused `92/92`, and full `575/575` independent audit evidence.

Accepted quality gates remain `15/16`. Ordinary feature expansion stays frozen pending
one pre-provisioned black-box A4 record, the bounded documentation correction, Foreman
acceptance, and protected-main publication/CI of that correction.

