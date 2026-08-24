# Publication Review: Council of Translation V0.12.0

## Decision

`PUBLISHED; Q-014 ISSUED`

The accepted CAMPAIGN-012-r3 implementation and complete Campaign archive were
published through protected `main` by PR #26. All six required CI checks passed before
merge, and all six protected-main checks passed again after publication. This decision
accepts V0.12.0 publication; it does not accept Q-014, which still requires fresh
normal-Goose A/B/C evidence.

## Publication identity

- Accepted local implementation: `e940044c5367ff2ef86e4c58bd75e1f85e4da4cf`
- Published equivalent implementation: `213cce55bb21d6854f76e89bee33a4e9e2f9dd8c`
- Accepted local archive: `fd6d5a10c7b59db3626aa163e9a0f1fa6b453ff7`
- Published protected `main`: `6c4366f7a43135388d0cf68655a6a3638d6bbe1b`
- Pull request: `https://github.com/PigeonCrafty/mcp-council-of-translation/pull/26`
- PR workflow run: `https://github.com/PigeonCrafty/mcp-council-of-translation/actions/runs/32712478320`
- Protected-main workflow run: `https://github.com/PigeonCrafty/mcp-council-of-translation/actions/runs/32712643635`
- Merge method: rebase, preserving the repository's required linear history
- Merged at: `2026-08-24T09:38:30Z`

The accepted and published implementation trees are both
`eca79f9deac92f5f187ea0a22471f25e0c711dc7`; their diff is empty. The accepted and
published archive trees are both `b6d5b4308f911539089a23383aa4de0194a5208f`; their
diff is empty.

## Required CI

PR #26 passed exactly six required checks before merge:

- Ubuntu Python 3.10: passed
- Ubuntu Python 3.12: passed
- Ubuntu Python 3.13: passed
- Windows Python 3.10: passed
- Windows Python 3.12: passed
- Windows Python 3.13: passed

Protected `main` commit `6c4366f` then passed the same six-job matrix. GitHub reported
PR #26 `CLEAN` and `MERGEABLE` before merge. No direct push to protected `main` was
attempted.

## Repository reconciliation

After merge, the Foreman fetched `origin/main`, proved exact implementation and archive
tree equivalence, and rebased the local `main` onto the published linear history. Git
correctly skipped all nine already-applied local commits, leaving local and remote
`main` synchronized. Existing user `.learnings/**`, `reviews/**` and the independent
audit Markdown remain untouched.

## Operational deviations

- The repository metadata API advertised merge commits, but the protected-main rule
  rejected `gh pr merge --merge`. The Foreman did not retry that strategy and used the
  accepted rebase merge instead.
- The managed workspace exposes `.git` read-only, so exact local staging, commit and
  reconciliation operations required bounded local-only elevation. All GitHub and Git
  HTTPS operations ran separately outside the sandbox as required.
- One unquoted PowerShell revision expression interpreted `^{tree}` incorrectly. The
  read-only check was repeated with quoted revisions and proved exact tree equality.

No credentials, provider settings, Goose installation or product files were changed by
these deviations.

## Next gate

Publication authorizes `harness/contracts/CAMPAIGN-012-q014-live.md`. Q-014 remains
unaccepted until one unchanged normal-Goose extension produces fresh A/B/C reviews and
their canonical `detail_level="verification"` receipts without client-side field
renaming, inferred values or confusion between reviewer successes, total sampling calls
and the applicable budget.
