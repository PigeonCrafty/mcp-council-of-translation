# CAMPAIGN-011 Q-013 Final Archive and Protected-Main Publication Review

- Foreman decision: `ARCHIVED; PUBLISHED; CAMPAIGN-011 CLOSED`
- Accepted live contract: `harness/contracts/CAMPAIGN-011-q013-live-r2.md`
- Accepted live review: `harness/evaluations/CAMPAIGN-011-q013-live-r2-review.md`
- Accepted V0.11.1 publication evidence:
  `harness/evaluations/CAMPAIGN-011-r3-publication-ci-review.md`
- Archive source commit: `27c150f3e8e87d73d505af921f246eb765c99167`
- Published protected-main commit: `6544d41d308f9ed7ab253dac5a70a94581cd04d8`
- Pull request: `#25`
- Merged at: `2026-08-24T06:14:08Z`

## Archive scope

The archive commit contains exactly the accepted Q-013-r2 live contract and review, the
accepted V0.11.1 publication review, and the corresponding Foreman state in
`harness/features.json`, `harness/plan.md`, and `harness/progress.md`. No product source,
test, dependency, lock, package, raw live record, credential, Goose configuration, or
user-owned asset is included.

The accepted archive commit and the protected-main publication have the identical tree:

`b03d7ea346066538bb1e02ff3c58e90b6d913d0b`

This tree equivalence is the authoritative mapping across GitHub's rebase merge, which
truthfully changed the commit identity while preserving the accepted content.

## Protected-main and CI evidence

`main` required a linear history, administrator enforcement, resolved conversations and
six strict status checks. PR #25 was mergeable and clean before merge. Workflow run
`32696328264` completed successfully with all required jobs passing:

| Platform | Python | Result | Duration |
| --- | --- | --- | --- |
| Ubuntu | 3.10 | passed | 15 s |
| Ubuntu | 3.12 | passed | 15 s |
| Ubuntu | 3.13 | passed | 13 s |
| Windows | 3.10 | passed | 36 s |
| Windows | 3.12 | passed | 30 s |
| Windows | 3.13 | passed | 50 s |

The PR was merged with the repository's protected-main rebase workflow. The temporary
remote and local archive branches were deleted afterward. Local `main`, `origin/main`
and `origin/HEAD` now resolve to the published commit, and their tracked trees have no
diff.

## Reconciliation and incident note

One broad `gh pr view` query returned an empty client result while PR state was being
checked. No merge decision was made from that empty response. A smaller explicit query
was retried, returned the expected clean/mergeable state, and the six checks were
independently enumerated before merge. This was a transient CLI observability issue, not
a repository or CI failure.

The pre-existing user-owned `.learnings/`, `reviews/`, and audit recommendation document
remain untracked and untouched. Q-013-r2 remains accepted on persisted Schema 2.5 record
evidence; Goose-authored aliases or summaries are not promoted to authoritative facts.

## Final disposition

V0.11.1 and the final Q-013 A/B/C acceptance assets are durably published through the
protected branch. All 52 planned features and all 13 quality gates are accepted.
CAMPAIGN-011 has no remaining implementation, publication, or live-validation work.
