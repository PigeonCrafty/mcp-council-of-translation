# CAMPAIGN-013 V0.13 Publication and CI Review

- Decision: `PUBLISHED; SIX_WAY_CI_ACCEPTED; Q-015_READY_TO_ISSUE`
- Accepted implementation: `4f976c2764a463dceb403084fa3faead5300211e`
- Protected-main publication PR: `#31`
- PR URL: `https://github.com/PigeonCrafty/mcp-council-of-translation/pull/31`
- Published protected `main`: `95d90cf383d045778ce61afaa50dbcec199579ce`
- Publication date: 2026-08-25 Asia/Shanghai

## Publication integrity

- The remote publication branch contained the six accepted V0.13 product commits and 15
  CAMPAIGN-013/Harness archive assets.
- Local sandbox policy prevented writing `.git/index`; no local Git write was elevated.
  The accepted product HEAD was pushed over HTTPS and the archive was constructed with
  the GitHub Git Data API on the dedicated release branch.
- The first remote archive tree preserved the working-copy CRLF bytes of
  `harness/features.json`, unlike normal Git clean-filter behavior. A one-file remote
  correction normalized it before PR creation. Final branch `diff --check` passed and all
  15 remote archive blobs matched their local accepted content.
- PR #31 used squash merge, so the intermediate remote line-ending correction is absent
  from protected-main history.
- The final PR branch tree and published protected-main tree are identical. The published
  non-Harness product tree is identical to accepted implementation `4f976c2`.

## Six-way CI

PR workflow run `32805729165` passed all required jobs:

- Ubuntu / Python 3.10: passed in 19s
- Ubuntu / Python 3.12: passed in 17s
- Ubuntu / Python 3.13: passed in 18s
- Windows / Python 3.10: passed in 34s
- Windows / Python 3.12: passed in 39s
- Windows / Python 3.13: passed in 33s

The post-merge protected-main workflow run `32805814076` also completed successfully for
the same six-job matrix at published SHA `95d90cf`.

## Published contract

- Package/module: `0.13.0`
- Diagnostic build: `calibrated-evidence-council-v11`
- Persisted Review Schema: `2.6`
- Verification receipt Schema: `1.1`
- Public tools: exactly five
- Review-only boundary, defaults, budgets `6/13/18`, concurrency `1..3` and 15 routing
  profiles remain frozen.

## Next gate

Q-015 may now be issued as a user-operated normal-Goose gate. It remains unaccepted until
the Foreman reviews three fresh published-main records together. No live Goose, provider,
credential, package release or deployment action occurred during publication review.
