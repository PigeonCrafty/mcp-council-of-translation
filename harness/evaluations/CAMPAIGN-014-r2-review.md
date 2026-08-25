# CAMPAIGN-014-r2 Foreman Review

## Disposition

`ACCEPTED`

Foreman independently reviewed `harness/reports/CAMPAIGN-014-r2-worker.md` against
`harness/contracts/CAMPAIGN-014-r2.md` in `STRICT_CAMPAIGN` mode. The revision closes
the r1 allowlist omission without changing the frozen remediation design, and the
combined eight-commit Campaign satisfies its local acceptance contract.

## Identity and scope

- Contract SHA-256:
  `6B0A2FB0D122F3E67F12D0A4FADAD2BC17BA93A62DBC7802C748F294EC0FB404`
- r2 baseline: `742128a1dfc2282d7aad4ee016d37ff94922c9ca`
- Final HEAD: `9d23ed01f94be2ef0c724b3e0a3e7e1beba75c09`
- Original Campaign baseline: `44b1969677cd6b1fda63047ca514aede6609bdad`
- r2 contains exactly one new commit, `9d23ed0` (`PKG-087`), and the Campaign history
  contains exactly eight ordered, scoped package commits.
- The r2 baseline-to-final diff contains exactly 10 contract-authorized paths. The
  original Campaign baseline-to-final diff contains exactly 29 authorized paths and no
  path outside the contract allowlist.
- `git diff --check` passed. The Git index was empty. All 13 r2 protected hashes matched.

## Independent verification

- Syntax compilation passed.
- The focused recovery selection passed `34/34`.
- The risk-weighted affected matrix passed `180/180`.
- The complete repository regression passed `575/575` in 5.76 seconds.
- Golden evaluator Schema 2.1 passed exactly `30/30`; ten accuracy/coherence metrics
  were `1.0`, `insufficient_false_reassurance_rate` was `0.0`, and there were no failed
  case IDs.
- Runtime diagnostics independently returned package/module `0.13.1`, build
  `truthful-boundaries-council-v11.1`, Review Schema `2.6`, receipt Schema `1.1`, exact
  five tools, review-only defaults, budgets `6/13/18`, and concurrency `3/3`.
- `uv.lock` retained revision 3, 78 packages and 586 upload-time entries; its accepted
  SHA-256 is
  `E7E4E44A19A3A7F1813EE3B5CFDC5814A70BF29C71CD5115582AF4E64A352E00`.

## Package and compatibility evidence

The Worker artifacts were verified as reported:

- wheel: 110309 bytes, SHA-256
  `4582ACDB48D5B6E5C008A0E9B11020B290D60C1C812A6A7F7A7328AC76F1CDB8`
- sdist: 103191 bytes, SHA-256
  `41863D980E3597078CD2B808742D632C62BAA122B0CD56CA0BBA0C1D04C8EE43`

Foreman also performed a separate pinned-uv 0.12.3 build in a clean temporary output
directory. Archive metadata, version and the bounded dependency declaration
`fastmcp>=2.13.0.2,<4` were correct and neither archive contained temporary assets.
Archive hashes differed from the Worker's hashes because build timestamps are not
reproducible inputs; installed behavior and archive contents required by the contract
matched.

The fresh wheel imported from isolated `site-packages` and called all five tools under
both FastMCP `2.13.0.2` and `3.4.7`. The 2.13.0.2 run emitted only the already-known
upstream Authlib deprecation warning. The first Foreman smoke inherited the repository
working directory and was discarded; both accepted smokes were rerun from isolated
working directories with empty injected review storage and no persistence mutation.
All Foreman temporary assets were removed afterward.

## Acceptance rationale

PKG-087 truthfully migrates the remaining release assertions to V0.13.1/v11.1 and does
not weaken any frozen audit-remediation rule. Combined evidence accepts:

- F-064 fail-closed incomplete-input review;
- F-065 high-precision deterministic token scanning;
- F-066 safe malformed-discussion degradation;
- F-067 post-discussion consensus and choice coherence;
- F-068 privacy-minimized legacy V1 summary;
- F-069 truthful Golden semantics and blind-set contract; and
- F-070 evidence-bounded FastMCP compatibility policy.

No required check was skipped and no local implementation blocker remains. Publication,
protected-main CI and Q-016 remain distinct Foreman/user gates; this acceptance does not
itself authorize remote mutation or lift the external feature-expansion block.

## Remaining risk

- FastMCP 2.13.0.2 emits an upstream Authlib deprecation warning but passed installed
  wheel behavior.
- Compatibility evidence is intentionally bounded to the locked floor and isolated
  FastMCP 3.4.7, not every future FastMCP 3.x release.
- Q-016 must still externally re-audit the published remediation and exercise the
  normal-Goose truncation receipt before ordinary feature expansion resumes.
