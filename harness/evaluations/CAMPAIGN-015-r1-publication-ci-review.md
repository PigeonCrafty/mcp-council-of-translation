# CAMPAIGN-015-r1 Publication and CLOSURE-004 Review

## Disposition

- Role: `FOREMAN`
- Mode: `STRICT_CAMPAIGN`
- Decision: `ACCEPTED`
- Closure item: `CLOSURE-004`
- Stage declaration: `FEATURE SCOPE COMPLETE`; `ENGINEERING FEATURE COMPLETE`;
  `PRODUCTION VALIDATED: NOT YET`
- Review date: `2026-08-28 Asia/Shanghai`

## Provenance

- Local Campaign implementation baseline: `c7d788ca37ecb5d6bd3f1ebec01d48d5c7d52fb4`
- Local Campaign accepted HEAD: `c0f0d190ff5b5bc753f9dc743ce3a5743fe32bdf`
- Publication branch final HEAD: `77d952ce977c5a8fa0bf3adfbaa7e6dec68ac23c`
- Protected-main squash publication SHA: `b3c36b0998730d9380d4838e642733ca5ffeb9c3`
- Publication PR: [#41](https://github.com/PigeonCrafty/mcp-council-of-translation/pull/41)
- Annotated tag: `v0.13.2`
- Annotated tag object: `4d5fb4b2586af9cef2d92699ee3fe8c0d013385b`
- Tag target: `b3c36b0998730d9380d4838e642733ca5ffeb9c3`
- GitHub Release:
  [Council of Translation V0.13.2](https://github.com/PigeonCrafty/mcp-council-of-translation/releases/tag/v0.13.2)

The local Campaign accepted HEAD is an implementation-review reference, not the public
protected-main release commit. The tag and released artifacts are anchored to the
protected-main squash publication SHA.

## Protected-main publication and CI

- Publication branch reproduced the accepted product blobs exactly and added only the
  bounded acceptance archive.
- Pre-push verification: compile PASS; complete regression `578 passed`.
- Initial PR CI run `33153817565` exposed a test-only Python 3.10 import incompatibility:
  `test_v10_release_contract.py` imported the Python 3.11-only stdlib module `tomllib`.
- After explicit user authorization, commit `77d952c` added the bounded
  `tomllib`/`tomli` test import fallback. Product runtime, version, schemas and lock were
  unchanged. Focused `4 passed` and complete `578 passed` locally.
- Final PR CI run [33154237497](https://github.com/PigeonCrafty/mcp-council-of-translation/actions/runs/33154237497)
  passed Ubuntu and Windows on Python 3.10, 3.12 and 3.13.
- Post-merge protected-main run
  [33154325010](https://github.com/PigeonCrafty/mcp-council-of-translation/actions/runs/33154325010)
  passed the same six-job matrix.

## Named release and checksums

The release was built from the verified protected-main commit using exact `uv 0.12.3`.
Archive inspection found 31 wheel members and 42 sdist members, with no Harness,
reviews, learnings, tests, user fixtures, Git metadata or temporary assets.

| Asset | Size | SHA-256 |
| --- | ---: | --- |
| `council_of_translation-0.13.2-py3-none-any.whl` | 110403 bytes | `7F50A197F4BAD6E8573278203C146B8E72C7CA1915E05F423AFC463F8C235BBC` |
| `council_of_translation-0.13.2.tar.gz` | 103104 bytes | `C058B204019006467A650C01046647DFFAD82B04489A9D3F305EE335F1951C91` |
| `SHA256SUMS.txt` | 216 bytes | `9511C328B3CA641C49D439BFE0F0EA380480461CEB62AC22B3B942FB6E2B6C4B` |

GitHub reported matching SHA-256 digests for all three uploaded assets. The annotated tag
is unsigned; its value here is stable naming and auditable commit linkage, while artifact
integrity is supplied by the published checksums.

## Closure decision

CLOSURE-004 is accepted because the accepted V0.13.2 candidate is published through
protected main, both required six-job CI matrices passed, and an annotated named tag plus
GitHub Release reference the verified protected-main commit with checksum-verifiable
wheel/sdist artifacts and bounded known limitations.

Known limitations remain explicit: FastMCP 2.13.0.2 may emit its upstream Authlib
deprecation warning; bounded-input fail-closed behavior is not long-document chunking;
Targeted Discussion is one bounded simulated deliberation sample; production validation
is not yet claimed.

Ordinary Feature Campaign work is frozen. Reopening product development requires an
evidence-driven trigger from real-project observation, independent blind evaluation,
provider/client compatibility or a confirmed correctness/privacy/authority defect.
