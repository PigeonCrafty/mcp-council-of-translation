# Foreman Review: CAMPAIGN-007-r5

## Decision

`ACCEPTED`

CAMPAIGN-007-r5 resolves the V0.9 publication lock admission defect with the exact
CI-version metadata refresh. The final commit changes only the editable root package
version in `uv.lock`; no dependency graph, source, workflow or Council behavior changed.

## Control and scope

- Contract SHA-256:
  `F344D16FA84B32C275DCB55EF7D0B6769CE540CE374B6DED9F46E5E2FDE9B6C2`
- Baseline: `11fb742cda602d33cb66550d0f3d665234bd4193`
- Accepted final HEAD: `28817d6ea7a0d547ae89579d4597cea0fbae0b2b`
- Exactly one commit: `28817d6 Refresh V0.9 root lock metadata`
- Exact committed scope: `uv.lock`, one insertion and one deletion
- Exact semantic diff: editable root version `0.8.0` to `0.9.0`
- Index empty; user and Foreman assets preserved; all twenty protected hashes matched

## Independent Foreman evidence

- Final lock SHA-256:
  `1CED44E8A6D0F88691A83FFC5B214232CAAA6E437BA5EC8820B5EDADA5C65E9D`.
- Lock invariants: revision 3, 586 upload-time entries, 78 package entries and one
  editable root at 0.9.0.
- Pinned uv 0.12.3 `lock --check` and `sync --locked --group dev`: passed using separate
  repository-local Foreman cache/tool directories.
- Pinned compile: passed.
- Fresh complete suite: `246 passed in 4.60s`.
- Runtime diagnostics: package/module 0.9.0, build `bounded-parallel-council-v7`, schema
  2.3, exact five tools and budgets 6/13/18.
- Baseline-to-final name/status, numstat, textual diff and `git diff --check`: passed.

## Acceptance boundary

This accepts the lock correction and clears the local publication defect. It does not by
itself accept PR #15 publication or Q-011. PR CI must pass after the accepted commit and
normal Goose must still compare effective concurrency limits one and three.

