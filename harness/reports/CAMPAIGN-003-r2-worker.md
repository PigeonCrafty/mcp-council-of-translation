# CAMPAIGN-003-r2 Worker Report

## Disposition

`READY_FOR_REVIEW`

This is a Main Worker handoff for independent Foreman review, not Campaign acceptance
or project completion.

## Authority and scope

- HARNESS_ROLE: WORKER / MAIN WORKER
- HARNESS_MODE: STRICT_CAMPAIGN
- Contract: `harness/contracts/CAMPAIGN-003-r2.md`
- Contract SHA-256:
  `AA0C69FF175FC0D33C05156B7A0699EF5731B13FC76B4616282B279A9598461E`
- Exact admitted baseline:
  `3de6e5fafb0d6a0a4347b68469e99ce7ef8bc816`
- Baseline subject: `Retain safe guided metadata counts`
- Final HEAD: `9dac21dd3cee9d9a299786e8cdec525f28a0c517`
- Final subject: `Fix auto briefing context sufficiency`
- Subagent policy/use: forbidden / 0
- Authorized implementation paths: only
  `src/council_of_translation/localization/guided.py` and
  `tests/integration/test_v22_briefing.py`.
- This report is the sole new Harness asset and remains uncommitted.

## Admission gate

Before any edit, the Main Worker completely read the pigeon-harness skill, Common and
Worker protocols, `AGENTS.md`, plan, features, progress, both r1 contract/report/ledger,
the r1 Foreman review, and this r2 contract.

Admission evidence:

- `git rev-parse HEAD` -> exact baseline.
- `git log -1 --format=%s` -> exact baseline subject.
- Git index -> empty.
- Worktree inventory -> only the protected Foreman/user assets enumerated below.
- r2 contract hash -> exact expected value.
- All ten contract-listed protected hashes -> exact; mismatch count 0.
- `python -m compileall -q src tests` -> exit 0, `ADMISSION_COMPILE_OK`.
- `.venv\Scripts\python.exe -m pytest -q --basetemp
  .tmp\campaign003-r2-admission -p no:cacheprovider` -> exit 0,
  `182 passed in 2.00s`.

Admission disposition: PASS. No file was edited before the gate passed.

## Defect reproduction and correction

The pre-edit helper probe reproduced the Foreman counterexample:

```text
recognized_plus_two=True
alias_plus_two=True
recognized_plus_one=False
unknown_plus_two=False
unknown_plus_three=True
unknown_plus_all_four=True
source_target_only=False
```

The prior predicate counted raw field groups and returned true at a numeric threshold of
three, allowing unknown content type to bypass briefing.

The correction is deliberately isolated:

1. `_provided_context_count()` remains unchanged because it also supports existing
   context-confidence behavior.
2. A private category counter represents exactly four independent categories:
   usage/reference, audience, style/brand, and glossary/project/technical authority.
3. `context_is_sufficient()` now requires both a recognized normalized content type and
   at least two present categories.
4. `known_exceptions`, `notes`, hard constraints and do-not-translate literals are not
   counted, while their existing authority and storage paths remain untouched.

No public tool, argument, mode, schema field, form field, dependency, version, build,
budget, persistence, orchestration, context-gap, reconsideration, digest or continuation
behavior changed.

## Test coverage and truth table

The focused test file now includes direct positive/negative coverage for:

- recognized `ui` plus context and audience;
- recognized `UI button` alias plus reference and brand categories;
- recognized content plus only one category;
- unknown content plus two, three, or all four categories;
- source/target only;
- ignored exceptions/notes/hard-constraint/DNT fields;
- a full Core path proving unspecified content plus all four categories still elicits a
  briefing.

Final direct helper output:

```text
recognized_plus_two=True
alias_plus_two=True
recognized_plus_one=False
unknown_plus_two=False
unknown_plus_three=False
unknown_plus_all_four=False
source_target_only=False
```

Existing source/target-only briefing-before-sampling, rich skip, `always`, `off`, and
accept/decline/cancel/unsupported/malformed tests were retained and passed.

## Required verification

- Final compile:
  `python -m compileall -q src tests` -> exit 0, `FINAL_COMPILE_OK`.
- Focused:
  `.venv\Scripts\python.exe -m pytest -q
  tests\integration\test_v22_briefing.py --basetemp
  .tmp\campaign003-r2-focused -p no:cacheprovider` -> exit 0,
  `11 passed in 0.41s`.
- Full:
  `.venv\Scripts\python.exe -m pytest -q --basetemp
  .tmp\campaign003-r2-full -p no:cacheprovider` -> exit 0,
  `184 passed in 3.62s`.
- Fresh build:
  `$env:UV_CACHE_DIR='.tmp\campaign003-r2-uv-cache'; uv build --out-dir
  .tmp\campaign003-r2-dist` -> exit 0.
- Wheel: `council_of_translation-0.6.0-py3-none-any.whl`, 70,396 bytes,
  SHA-256
  `2031D023EAF2677BD8EC27B2B929668110F611BC119A763AC7F3F8AE66086278`.
- Sdist: `council_of_translation-0.6.0.tar.gz`, 63,997 bytes,
  SHA-256
  `6477A0ACDCE2E609BB8023289226439A7987C11C8A57E34AF1B5C4C60960C2B7`.
- Wheel inspection: distribution metadata `Version: 0.6.0`; corrected
  `council_of_translation/localization/guided.py` present; recognized-content gate,
  two-category threshold, and all four frozen category expressions present.
- `git diff --check
  3de6e5fafb0d6a0a4347b68469e99ce7ef8bc816..HEAD` -> exit 0.
- Baseline-to-final audit -> exactly two modified files, 100 insertions / 1 deletion,
  disallowed path count 0. The complete diff was inspected before commit.
- Final Git index -> empty.

## Commit and changed files

Exactly one local commit was created:

```text
9dac21dd3cee9d9a299786e8cdec525f28a0c517 Fix auto briefing context sufficiency
```

Committed paths:

```text
M src/council_of_translation/localization/guided.py
M tests/integration/test_v22_briefing.py
```

No Harness or protected asset was staged or committed. No push, PR, tag, release or
deployment was performed.

## Protected state and repository hygiene

Final contract-listed hashes equal admission:

| Protected asset | SHA-256 |
| --- | --- |
| `harness/plan.md` | `2D287FB16AD60D35E94289C9EDF3F2430DFD48F1EF6C35864F952AC95DA7F96A` |
| `harness/features.json` | `7E1A6C258ABBB1A25D6270B1202902DECEF7D8D0F421A173689E3D21092EF1F4` |
| `harness/progress.md` | `18BBE2DE28381EA5BCF216834175C4FDB3D987BEB492B56A3FA3CA378212E73F` |
| `harness/contracts/CAMPAIGN-003-r1.md` | `6A1017CF7C8205CC1FB753EC747529B0BF7920676655A53314C8B71B29239A46` |
| `harness/evaluations/CAMPAIGN-003-r1-review.md` | `B2CC11664F70352F45998BCBA6EE42EB2BBA1E8BE94CACB4B470A0D112B32DB3` |
| `harness/reports/CAMPAIGN-003-r1-ledger.md` | `7641B0D4CD5121D2CEA635DDD10B43D174A3CDD781E853591E6C142BD6E063BE` |
| `harness/reports/CAMPAIGN-003-r1-worker.md` | `1267643257A87942D90E539830A3FB68E653A543B14A848CD525FD20E0782770` |
| `.learnings/LEARNINGS.md` | `22F939E6F980DF52487AAFE97EDCA9B90CF3931DDB7A31BF8A5BBB8F052E658F` |
| `.learnings/ERRORS.md` | `F99EB75886781958BF5AE6DCF844FD476CBCA45937896A25EE3B2E9D6CD34F0A` |
| audit Markdown | `B48073E063C4C9F34E0B6B4DAE94E80079EAAAD3B2F8E273DD60B2F25F6ABD76` |

Final worktree inventory contains the original protected Foreman/user assets plus this
permitted untracked r2 report. `myTest/` is absent. The Git index is empty.

## Deviations, retries, omissions and risk

- The first post-edit focused run reported `1 failed, 10 passed`. Diagnosis: the new
  all-four integration fixture submitted the six-field answer packet even though the
  existing rich context correctly reduced the actual form to `content_type` and
  `primary_focus`; strict field-set validation therefore returned `malformed`. The test
  fixture was corrected to submit exactly those two displayed fields. Production code
  did not change for this retry, and the final focused/full suites passed.
- The self-improvement protocol was read after that unexpected test failure, but no
  `.learnings/**` entry was written because the active contract explicitly protects and
  forbids edits to that directory.
- Initial wheel-version inspection used a regex that did not account for CRLF metadata
  lines and printed False. A read-only line-by-line metadata check then printed
  `Version: 0.6.0` and `WHEEL_VERSION_0_6_0=True`; no artifact was changed or rebuilt.
- Required checks skipped: none. Dependency reinstallation and the r1 isolated FastMCP
  smoke were explicitly preserved and not required by this predicate-only contract.
- Subagents: 0.
- Git authority escalations: 2 (one exact-path `git add`, one local `git commit`).
- Live Goose/model/provider calls: 0.
- External mutations: 0. No package downloads were observed during the repository-local
  fresh build.
- Evidence is content-minimized and contains no credentials, tokens, private review
  payloads, hidden reasoning or unnecessary model/user prose.
- Remaining risk: independent Foreman review must confirm the predicate and accepted r1
  behavior. Live Goose rendering remains outside this correction and was not invoked.
