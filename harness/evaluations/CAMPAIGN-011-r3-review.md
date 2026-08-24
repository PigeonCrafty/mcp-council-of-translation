# Foreman Review: CAMPAIGN-011-r3

## Decision

`ACCEPTED`

CAMPAIGN-011-r3 satisfies the bounded V0.11.1 correction contract. The primary report
now preserves the canonical structured chief disposition exactly once and last even when
the action projection reaches its bound. Routing, adjudication, structured evidence,
Schema 2.5, budgets, concurrency and the five-tool surface remain unchanged.

This accepts the local V0.11.1 implementation. It does not publish it and does not accept
Q-013; protected-main publication and post-publication normal-Goose revalidation remain
separate gates.

## Control

- Role: `FOREMAN`
- Harness mode: `STRICT_CAMPAIGN`
- Contract: `harness/contracts/CAMPAIGN-011-r3.md`
- Contract SHA-256:
  `BA884359309326C179E5A42AF44D24872B960FD0D717130B59E88C534066C64A`
- Worker report: `harness/reports/CAMPAIGN-011-r3-worker.md`
- Worker report SHA-256:
  `D544D6B42124603FF971D3381238502C3D98E02569B28C27E0FDD4461EC5B975`
- Ledger: `harness/reports/CAMPAIGN-011-r3-ledger.md`
- Ledger SHA-256:
  `15B76B247A43E5FBC7A2E1F545AE3B8FB4930C4BBCADFDE40A72301A3B548742`
- Baseline: `938c3a4bb9f14c7688286b25eabd8aff9f18a09d`
- Accepted implementation: `76921ecb69ec26f0034ec772433e102a3f7715bf`
- Review date: 2026-08-24 Asia/Shanghai

## Scope and repository integrity

The exact baseline-to-final history contains two commits in the required order:

1. `4fce7d639934db414e640337de9daa6d9b82d948` — terminal disposition
   preservation;
2. `76921ecb69ec26f0034ec772433e102a3f7715bf` — V0.11.1 release migration.

The complete diff contains 11 authorized paths, 194 insertions and 25 deletions. PKG-063
changes only `digest.py` and its new V2.5 routing/presentation regression. PKG-064 changes
only nine authorized version, documentation, release-test and lock paths. No production
routing, orchestration, adjudication, persistence schema, prompt, role, dependency or
public-signature file changed. `git diff --check` passes and the Git index is empty.

All eight reported protected-file hashes were independently reproduced with zero
mismatch. Existing Foreman plan/progress modifications, contracts, evaluations, audit
Markdown and user-owned untracked paths remain outside both commits. The Worker reports
remain untracked and unstaged. The Worker reports zero subagents, zero live/model/Goose
calls and zero push/PR/release/deploy mutation; the diff and Git history show no contrary
evidence.

## PKG-063 review — dual-channel disposition coherence

The code change is narrow and implements the frozen design rather than masking the
counterexample:

- digest construction bounds action entries to seven and reserves the eighth bounded
  slot for the canonical chief final disposition;
- primary projection separates final-disposition entries from actionable work, retains
  the existing six-action primary cap and appends the last canonical final exactly once;
- the renderer keeps its conservative fallback only when a canonical final is genuinely
  absent;
- no verdict is inferred from severity, no Case A prose is hard-coded, and no structured
  chief, cluster, metric or telemetry object is mutated.

The new tests cover modified-publishable, true-human-review, clean, pending/degraded and
3,200-code-point boundary paths, including structured immutability and zero-call
telemetry. Independent focused execution passed `21 tests`.

The Foreman additionally rebuilt the process digest from the three exact persisted Q-013
records using current production code, without assigning it back to the record or
changing raw bytes:

| Case | Review ID | Structured chief | New primary terminal | Result |
| --- | --- | --- | --- | --- |
| A | `20260824T034709461394Z_33b581b3d0b6` | `修改后可发布 / 否` | exact same, once and last | pass |
| B | `20260824T034736890253Z_ee206d53abf7` | `可发布 / 否` | exact same, once and last | pass |
| C | `20260824T034809876049Z_c78aaf84819e` | `需人工复核 / 是` | exact same, once and last | pass |

Rebuilt reports remain five-section and measure 1,095, 368 and 683 Unicode code points.
The exact raw hashes remain the hashes accepted in the Q-013 live review. This closes the
observed Case A disagreement without weakening Case C's conservative disposition.

## PKG-064 review — release and frozen invariants

- Package/module: `0.11.1`.
- Diagnostic build: `risk-coherent-council-v9.1`.
- Schema: `2.5`.
- Public tools: exactly five, in the frozen order.
- Defaults, budgets `6/13/18` and concurrency limit/max `3/3`: unchanged.
- `uv.lock`: only editable root `0.11.0 -> 0.11.1`; revision 3, 78 packages and 586
  upload-time entries are preserved.
- Documentation and repository agent notes agree with the release identifiers.

## Independent verification

- Compile: passed.
- Focused presentation/routing selection: `21 passed`.
- Complete suite: `311 passed in 4.19s`.
- Golden: exact `24/24`, no failed IDs; all eight correctness, contribution, conflict,
  authority, chief, budget and discussion metrics are `1.0`.
- Golden runtime: 148 scripted samples, four scripted elicitations, aggregate budget 296,
  and zero routing/display model calls.
- Direct diagnostics: V0.11.1/build v9.1/schema 2.5, exact tools, budgets and concurrency
  passed.
- Worker artifact hashes were independently reproduced as
  `B7929DDE...EF4E1713` wheel and `1A40B975...5856F5E54` sdist.
- A fresh Foreman build with exact uv 0.12.3 also passed. Its timestamp-dependent hashes
  are `7B6C2F17...FD9E9630` wheel and `C85A349D...99D4A50` sdist; archive inspection found
  29/40 entries, zero `.tmp` entries, V0.11.1 metadata and the terminal-disposition fix.
- A fresh isolated Python 3.12.9/FastMCP 3.4.7 install imported from wheel
  `site-packages`, exposed exactly five tools, reported the frozen diagnostics and
  rendered the modified-publishable terminal once and last without mutating its digest.

The first Foreman isolated-wheel script used the older FastMCP `get_tools()` method and
failed because FastMCP 3.4.7 exposes `list_tools()`. The corrected probe passed. This is a
Foreman test-script API mismatch, not a product defect. The self-improvement procedure
was applied, but `.learnings/**` is protected and therefore was not modified; the incident
is recorded here.

## Remaining gate

CAMPAIGN-011-r3 is accepted. V0.11.1 is not yet published. Q-013 remains at
`CHANGES_REQUESTED` until this accepted tree is published through protected `main`, all
required CI succeeds, and a fresh normal-Goose post-publication run proves A/B/C on the
same V0.11.1 build. No project-completion claim is made.
