# Publication Review: CAMPAIGN-009 V0.10.1

## Decision

`ACCEPTED`

- Publication PR: `https://github.com/PigeonCrafty/mcp-council-of-translation/pull/18`
- Merge method: rebase, as required by the protected branch policy
- Published `main`: `f3b232cb2f3c9500fed04d204ef6198f2ee49af4`
- Accepted local implementation: `4a3c692ad528db03e4f72a025d60c4eb775454f0`
- Product tree equivalence: exact for `AGENTS.md`, `README.md`, `docs/**`,
  `pyproject.toml`, `src/**`, `tests/**` and `uv.lock`
- Package/build/schema: `0.10.1` / `evidence-value-council-v8.1` / `2.4`

All six required GitHub Actions checks passed before merge:

- Ubuntu Python 3.10, 3.12 and 3.13
- Windows Python 3.10, 3.12 and 3.13

Campaign 009 is archived and V0.10.1 is published on protected `main`. This publication
decision does not accept Q-012; the separately issued normal-Goose A/B/C protocol remains
the final live usefulness/non-repetition gate.
