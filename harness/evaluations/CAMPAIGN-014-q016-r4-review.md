# CAMPAIGN-014 Q-016-r4 Foreman Review

- Decision: `ACCEPTED`
- Role/mode: `FOREMAN / STRICT_CAMPAIGN`
- Contract: `harness/contracts/CAMPAIGN-014-q016-external-r4.md`
- Contract SHA-256:
  `3FFD9F75CE284BE2EB220E22D4F8F28746CFABFA61D3113B7BC807E360DDD6F3`
- Worker report: `harness/reports/CAMPAIGN-014-q016-r4-worker.md`
- Worker report SHA-256:
  `9EAA63BF034663FEE0A5A01ECA3C20355B298194EE76F1386348D64C3A0A734C`
- Execution ledger: `harness/reports/CAMPAIGN-014-q016-r4-ledger.md`
- Execution ledger SHA-256:
  `FE0EA8C0B496EB1A00CFB5B191F2ADFD9249CBA46EA5608221BB78C31DFF9B7A`
- Baseline: `9d23ed01f94be2ef0c724b3e0a3e7e1beba75c09`
- Accepted HEAD: `c7d788ca37ecb5d6bd3f1ebec01d48d5c7d52fb4`
- Accepted commit: `c7d788c Clarify Targeted Discussion boundary`
- Review date: 2026-08-28 Asia/Shanghai

## Scope and boundary

The complete baseline-to-final diff contains exactly the three authorized paths:

- `README.md`
- `docs/v0.4-architecture.md`
- `tests/integration/test_v10_release_contract.py`

The change is 27 insertions and one deletion in one local commit. The Git index is empty.
No production code, prompt, dependency, lock, workflow, package version, build ID,
schema, tool or budget changed. `uv.lock` remains byte-identical at SHA-256
`E7E4E44A19A3A7F1813EE3B5CFDC5814A70BF29C71CD5115582AF4E64A352E00`.

## Documentation correction

Both public documents now state that Targeted Discussion is one bounded model sample
simulating cross-role deliberation and is not peer-to-peer communication among
autonomous agents. The release-contract regression requires the three independent
semantic clauses and proves that the old phrase `optional single bounded discussion
round` alone cannot satisfy the assertion. The correction closes the r3 documentation
finding without changing architecture.

## A4 acceptance

The pre-provisioned black-box run proves exact public Git provenance
`9d8f1f987efe73946377883e6ad3a681abe11989`, CPython 3.12.9 and FastMCP 3.4.7. Exactly
one transport completed exactly four authorized calls: admission, one review, one full
read and one verification read. It used four constant local sampling callbacks, zero
elicitation, zero provider/model calls, zero continuation and zero transport/tool retry.

Accepted review ID:
`20260828T042741132302Z_56841705d054`.

Accepted product evidence:

- identical complete pre-call inputs `16000/16000`;
- recorded source/candidate diagnostics `16000 -> 12000`, both truncated;
- warnings `input_truncated`, `source_input_truncated`, and
  `candidate_input_truncated`;
- full four-role `structured_success` coverage and calls/budget/elicitation `4/6/0`;
- `NEEDS_HUMAN_REVIEW`, degraded true, fallback exactly `input_truncated`, chief
  `需人工复核 / 是`, decision support `insufficient` and no suggested translation;
- the primary report contains `仅审校了有界前缀` and `不构成全文发布许可`;
- receipt Schema 1.1 is complete with no not-recorded/redacted fields and exact terminal
  coherence.

The Worker runner's final local parser passed a Markdown-fenced JSON block directly to
`json.loads` after all authorized calls and evidence capture completed. It did not retry
the transport or any tool. A separate offline validator stripped only the documented
fence from that same preserved file and proved text/structured receipt equality. The
Foreman independently parsed the receipt, bounded full-record projection and primary
report from the durable Worker report and reproduced every acceptance value. This is an
accepted evidence-tooling deviation, not missing product evidence.

## Independent verification

The Foreman independently ran:

- compile: PASS;
- release-contract suite: `4 passed`;
- required affected selection: `93 passed`;
- complete regression: `576 passed`;
- baseline-to-final `git diff --check`: PASS;
- exact three-path scope and unchanged lock hash: PASS;
- offline canonical receipt, input-diagnostic and primary-text assertions: PASS.

Worker external actions were within contract: no subagents, one remote Git HTTPS package
installation, no push/PR/publication/release/deployment, no Goose/provider/model call,
and temporary evidence environments were removed after bounded report capture.

## Carry-forward and gate state

The following remain accepted without rerun:

- Case B `20260828T024458690799Z_8badddd7158f`;
- Case C `20260828T024543336644Z_2422acf98836`;
- AUD-001 through AUD-007 as `CLOSED`;
- r2 `CLIENT_LIMIT` as truthful Goose client-boundary evidence.

Q-016-r4 is accepted locally. Q-016 remains `15/16` and
`ACCEPTED_PENDING_PROTECTED_MAIN_PUBLICATION` until this exact documentation/test commit
and the Foreman review/archive assets are merged through protected main and all six PR
plus post-merge CI jobs pass. No further Goose, A4, B/C or AUD rerun is required.

