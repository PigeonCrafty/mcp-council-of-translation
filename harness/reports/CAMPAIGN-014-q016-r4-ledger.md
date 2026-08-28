# CAMPAIGN-014 Q-016-r4 execution ledger

Terminal state: `READY_FOR_REVIEW`

This ledger exists because a diagnostic command failed. It is intentionally untracked
and unstaged.

## Admission

- Shared implementation baseline: `9d23ed01f94be2ef0c724b3e0a3e7e1beba75c09`.
- Protected-main baseline: `ab912c41d6deebeab440d8be9557371be2580dff`.
- Contract SHA-256: `3FFD9F75CE284BE2EB220E22D4F8F28746CFABFA61D3113B7BC807E360DDD6F3`.
- Git index: empty.
- Subagents: forbidden and unused.

## Failed commands and bounded responses

| Seq. | Command/operation | Result | Bounded response |
|---:|---|---|---|
| 1 | System-Python runtime identity probe with `PYTHONPATH=src` | Python 3.13.14 raised `ModuleNotFoundError: No module named 'fastmcp'`. No repository file changed. | Located the existing repository `.venv` (CPython 3.12.9, FastMCP 2.13.0.2) and use it for local verification. The failure was not treated as product evidence. Protected `.learnings/**` was not read or written. |
| 2 | Baseline `python -m pytest tests/integration/test_v10_release_contract.py -q` through `.venv` | `2 passed, 1 error`; fixture setup could not traverse host-owned `%TEMP%\\pytest-of-GeZhu`. Compile had already passed. | Use a fresh boundary-checked campaign temp root for `TEMP`/`TMP` and rerun the unchanged pytest arguments. This is environment containment, not a test or product correction. |
| 3 | First server provenance assertion | The observed `direct_url.json` URL was the correct `https://github.com/PigeonCrafty/mcp-council-of-translation`, but the check incorrectly required a trailing `.git`; its other observed fields were correct. | Before any transport, normalize an optional `.git` suffix and rerun only the read-only provenance assertion. No dependency reinstall or network retry was made. |
| 4 | First sandboxed `git add` / `git commit` attempt | Git could not create `.git/index.lock` under the managed sandbox. | Repeated the exact three-path local stage/commit operation with approved external filesystem authority; no remote Git operation occurred. |
| 5 | Optional `SamplingHandler` source introspection | `inspect.getsource` rejected the typing alias with `TypeError`; the required callable signature had already been printed. | Used the printed callable signature and bounded `CallToolResult` dataclass introspection; no server or transport was started. |
| 6 | Sole A4 transport runner's final receipt parser | All four authorized tool calls returned successfully, but the local parser passed a Markdown-fenced JSON block directly to `json.loads`, producing `JSONDecodeError`. Transport/tool retry count remained zero. | Preserved the 81,378-byte raw/structured evidence and server stderr. Parsed the already captured fenced JSON offline, proved exact text/structured receipt equality, and reran every remaining assertion without starting another transport. This is an evidence-run parser deviation, not a product defect. |
| 7 | First offline evidence-summary print | Windows GBK stdout could not encode one FastMCP banner character and raised `UnicodeEncodeError` after printing the main counts. | Set `PYTHONIOENCODING=utf-8` and repeated only local file inspection; no MCP or network operation occurred. |
| 8 | First recursive removal of the verified A4 temp root | Sandbox could not remove a host-owned cached wheel produced by the externally authorized Git install. | Repeated the same resolved-path checks and removed only that exact `%TEMP%` directory with approved external filesystem authority; final `Test-Path=False`. |

## Sole A4 operation

- Transport starts: 1; MCP tool calls: 4 (`get_server_info` 1, `review_translation` 1,
  full history 1, verification history 1).
- Sampling callbacks: 4 constant local envelopes; elicitation callbacks: 0.
- Continuations, second reviews, additional history calls and post-transport retries: 0.
- External provider/model calls: 0.
- Review ID: `20260828T042741132302Z_56841705d054`.
- Offline validation of the captured results: `PASS_OFFLINE_FROM_SINGLE_TRANSPORT_EVIDENCE`.

## Final verification

- `python -m compileall src tests`: PASS through repository `.venv` CPython 3.12.9.
- Release-contract regression: `4 passed in 3.72s`.
- Required six-file focused suite: `93 passed in 1.55s`.
- Complete regression: `576 passed in 5.29s`.
- `git diff --check 9d23ed01...HEAD`: PASS.
- Exact `git diff --check`: PASS; Git emitted only the pre-existing protected
  `harness/features.json` LF-to-CRLF advisory, with no whitespace error.
- Baseline-to-final committed paths: exactly `README.md`,
  `docs/v0.4-architecture.md`, and
  `tests/integration/test_v10_release_contract.py`.
- `uv.lock` SHA-256 before/after:
  `E7E4E44A19A3A7F1813EE3B5CFDC5814A70BF29C71CD5115582AF4E64A352E00`.
- Boundary-checked A4 temporary root cleanup: complete; final `Test-Path=False`.
