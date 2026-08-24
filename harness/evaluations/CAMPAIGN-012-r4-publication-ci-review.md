# Publication Review: Council of Translation V0.12.1

## Decision

`PUBLISHED; Q-014-r2 CONTRACT SIGNED`

The accepted CAMPAIGN-012-r4 implementation and its complete Foreman archive were
published through protected `main` by PR #28. All six required CI checks passed before
merge, and all six protected-main checks passed again after publication. This decision
accepts V0.12.1 publication; it does not accept Q-014, which still requires fresh
normal-Goose A/B/C evidence under the r2 live contract.

## Publication identity

- Accepted local implementation: `46849c9198213ad6d1e9888e8a0503bb1bccc61c`
- Published equivalent implementation: `47ec9256f0eb55892f5f58ec4bd6609aacf18aa8`
- Accepted local archive: `16931f1fd42553b460db30f4d9579cb75fc4753a`
- Published protected `main`: `c5d38a1f2f8ef4cafaada98f93583e1532405a3b`
- Pull request: `https://github.com/PigeonCrafty/mcp-council-of-translation/pull/28`
- PR workflow run:
  `https://github.com/PigeonCrafty/mcp-council-of-translation/actions/runs/32719721002`
- Protected-main workflow run:
  `https://github.com/PigeonCrafty/mcp-council-of-translation/actions/runs/32719838126`
- Merge method: rebase, preserving the required linear history
- Merged at: `2026-08-24T11:02:49Z`

The accepted and published implementation trees are both
`629af8afb3f49bc48c5869f13d98db0e180e0fd4`; their diff is empty. The accepted and
published archive trees are both `521ad74a326deec428f51926d8f865f08f407c88`; their
diff is empty.

## Required CI

PR #28 passed exactly six required checks before merge:

- Ubuntu Python 3.10: passed
- Ubuntu Python 3.12: passed
- Ubuntu Python 3.13: passed
- Windows Python 3.10: passed
- Windows Python 3.12: passed
- Windows Python 3.13: passed

Protected `main` commit `c5d38a1` then passed the same six-job matrix. GitHub reported
PR #28 `CLEAN` and `MERGEABLE` before merge. No direct push to protected `main` was
attempted.

## Repository reconciliation

After merge, the Foreman fetched `origin/main`, proved exact implementation and archive
tree equivalence, and rebased local `main` onto the published linear history. Git skipped
the three already-applied local commits, leaving local and remote `main` synchronized.
Existing user `.learnings/**`, `reviews/**` and the independent audit Markdown remain
untouched.

## Operational deviations

- The managed workspace exposes `.git` read-only. Local staging, commit and rebase were
  attempted in the sandbox first and then used narrowly scoped local-only elevation after
  the expected `index.lock` / `rebase-merge` permission failures.
- All remote Git HTTPS and GitHub operations ran outside the sandbox as explicitly
  required by the user.
- The Worker report retains one intentional Markdown hard-break line reported by
  `git diff --check`; the accepted production baseline-to-final diff itself is clean.

No credentials, provider settings, Goose installation or product behavior were changed
by these deviations.

## Next gate

Publication authorizes `harness/contracts/CAMPAIGN-012-q014-live-r2.md`. Q-014 remains
unaccepted until the unchanged normal-Goose extension produces fresh A/B/C reviews whose
verification primary text contains the exact canonical receipt JSON after the fixed
label. The JSON must be parsed from that text block without renamed fields, inferred
values or model reconstruction.
