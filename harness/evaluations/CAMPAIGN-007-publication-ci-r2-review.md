# Foreman Publication Review: CAMPAIGN-007 CI Round 2

## Decision

`CHANGES_REQUESTED`

The accepted r5 lock correction reached PR #15 and cleared the original stale-lock
failure. All six Windows/Linux jobs passed locked dependency sync and compile; five jobs
passed the full suite. Windows Python 3.12 alone failed one timing assertion.

## Failure evidence

- PR: `https://github.com/PigeonCrafty/mcp-council-of-translation/pull/15`
- Workflow run: `31672130661`
- Passed: Ubuntu 3.10/3.12/3.13 and Windows 3.10/3.13.
- Failed: Windows 3.12,
  `test_return_pending_then_continue_creates_immutable_linked_revision`.
- Actual record: `sampling_wait_ms=20`, `wall_clock_ms=9`.
- Failing assertion: hard-coded `15 <= wall_clock_ms`.

## Diagnosis

The test double sleeps with `asyncio.sleep(0.02)` but records a fabricated constant
20ms sampling event instead of the observed duration. Windows event-loop scheduling can
resume a short timer before the nominal duration used by the test's lower bound. The
production implementation uses `perf_counter` and truthfully records actual end-to-end
wall time; the failure does not show a production timing regression.

## Required correction

Issue a test-only r6 correction. The delayed test executor must record its actual
`perf_counter` elapsed time, and the continuation assertion must verify the invariant
`0 < sampling_wait_ms <= wall_clock_ms < 2000`. This continues to catch the original
zero-wall regression while removing an operating-system timer assumption. No production,
lock, workflow or dependency change is authorized.

