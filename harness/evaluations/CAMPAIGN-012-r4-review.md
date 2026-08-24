# Campaign Review: CAMPAIGN-012-r4

## Decision

`ACCEPTED`

CAMPAIGN-012-r4 closes the normal-Goose verification-receipt handoff defect without
changing the canonical receipt object or any ordinary review/history response. F-058 is
accepted at final implementation HEAD
`46849c9198213ad6d1e9888e8a0503bb1bccc61c`. Q-014 remains a separate post-publication
normal-Goose revalidation gate and is not accepted by this offline review.

## Control

- Role: `FOREMAN`
- Harness mode: `STRICT_CAMPAIGN`
- Contract: `harness/contracts/CAMPAIGN-012-r4.md`
- Contract SHA-256:
  `29A6453ECD30C15CF204DB5C1B4DA3019632F9CBFE8B8FD222AC0CA7356A0255`
- Baseline: `aceac3383b2a597bbf5414362d9b71ac6e601267`
- Final HEAD: `46849c9198213ad6d1e9888e8a0503bb1bccc61c`
- Worker report: `harness/reports/CAMPAIGN-012-r4-worker.md`
- Worker ledger: `harness/reports/CAMPAIGN-012-r4-ledger.md`
- Commits: `a2078a4` (PKG-073) and `46849c9` (PKG-074)

## Scope and integrity

- The baseline is `origin/main` and an ancestor of final HEAD; the range contains exactly
  the two contracted commits.
- The complete diff changes exactly the 15 authorized production, test, documentation,
  metadata and lock paths. `git diff --check` passes and the Git index is empty.
- All 15 protected admission hashes and the contract hash match exactly. Existing
  Foreman/user dirty and untracked assets remain preserved and unstaged.
- `uv.lock` changes only the editable root version from 0.12.0 to 0.12.1 and retains
  revision/package/upload-time invariants `3/78/586`.

## Independent Foreman verification

- Compile passes under the repository Python 3.12.9 environment.
- Receipt, dual-channel, release, tool-surface and persistence matrix:
  `171 passed in 1.55s`.
- Complete regression: `444 passed in 4.12s`, with no skips.
- Direct critical probes pass for live-shaped A/B/C canonical JSON equality, exact
  `full`/`summary` text compatibility, one-load/zero-mutation verification retrieval and
  bounded private failure for an impossible oversized receipt.
- The implementation appends exactly one compact UTF-8 JSON object after the existing
  verification Markdown and footer, using the literal label
  `Canonical verification_receipt JSON:` and no trailing prose.
- Parsed text JSON equals the same structured `verification_receipt`; the five human
  receipt headings remain unchanged. Ordinary review, continuation, full, summary,
  list, diagnostic and error primary text remain outside this fallback.
- The combined text has a 12,000-code-point hard cap. Hostile, legacy, metadata,
  privacy, redaction and zero-side-effect controls pass.

The first Foreman test attempt used host Python 3.13 without `fastmcp` and therefore
failed at collection. A subsequent `uv run` attempt encountered the known host uv-cache
permission defect. Both are environment-selection failures; the canonical repository
`.venv` reruns above pass completely. The self-improvement log was intentionally not
written because `.learnings/**` is a contract-protected user asset.

## Frozen public invariants

- Package/module: `0.12.1`.
- Diagnostic build: `verifiable-evidence-council-v10.1`.
- Persisted Review Schema: `2.5`; verification receipt Schema: `1.0`.
- Exact five public tools, review-only authority, defaults, budgets 6/13/18 and
  concurrency 3/3 remain unchanged.
- Receipt retrieval remains deterministic, privacy-safe, one-load, zero-save,
  zero-sampling and zero-elicitation.

## Artifact evidence

The Worker produced fresh final-HEAD artifacts and an isolated CPython 3.12.9/FastMCP
3.4.7 five-tool smoke:

- wheel: 102,738 bytes, SHA-256
  `29D3907AC9B4F3C64245FEEE7487E93E55D98AD98F3D504CA214D2475B1C5B6A`;
- sdist: 96,442 bytes, SHA-256
  `FADD8801EF3DD9C357D327E3AE10CFE79007A371944401A499B12AA36C2D7AB4`.

The smoke proved that all five installed tools work and that text-only canonical JSON
parses equal to the structured receipt. Foreman did not traverse the contract-forbidden
historical `dist/**` directory.

## Acceptance and remaining gates

- F-058: accepted by `CAMPAIGN-012-r4`.
- Local V0.12.1 implementation: accepted at
  `46849c9198213ad6d1e9888e8a0503bb1bccc61c`.
- Publication through protected `main`, six-job CI and a fresh normal-Goose Q-014 A/B/C
  revalidation remain separate gates.
- No push, PR, publication, release, deployment, credential or live provider action was
  performed during this review.
