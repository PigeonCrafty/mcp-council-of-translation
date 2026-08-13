# Foreman Review: CAMPAIGN-007-r4

## Decision

`CHANGES_REQUESTED`

The Worker correctly obeyed r4 and stopped without staging or committing. The pinned
generator was correct, but r4 incorrectly assumed plain incremental `uv lock` would
upgrade an already semantically current revision-1 lock to revision 3.

## Root cause

uv lock generation is incremental. Because the admitted r3 intermediate already
contained root version 0.9.0 and a valid 78-package resolution, uv 0.12.3 considered it
current and preserved its older lock representation. Pinning the executable alone cannot
reconstruct metadata previously removed by uv 0.6.13.

## Independently proven correction

Foreman created an isolated copy of the exact admitted intermediate and ran pinned uv
0.12.3 with `uv lock --refresh`. The result:

- upgraded revision 1 to revision 3;
- restored exactly 586 upload-time entries;
- retained exactly 78 packages and all dependency versions, edges, sources and hashes;
- matched byte-for-byte the independently generated expected V0.9 lock:
  `1CED44E8A6D0F88691A83FFC5B214232CAAA6E437BA5EC8820B5EDADA5C65E9D`;
- differed from the Git baseline by exactly one deletion/insertion: editable root
  version 0.8.0 to 0.9.0;
- passed pinned `uv lock --check`.

## Required revision

CAMPAIGN-007-r5 must authorize the exact pinned `uv lock --refresh` operation against
the admitted r3/r4 intermediate and require the proven target hash before sync, tests or
commit. No manual editing or Git restoration is needed. The r4 Worker report remains
truthful blocked evidence; r1/r2 implementation acceptance remains unchanged.

