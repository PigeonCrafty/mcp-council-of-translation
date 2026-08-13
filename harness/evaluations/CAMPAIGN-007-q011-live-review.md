# Live Goose Review: CAMPAIGN-007 Q-011

## Decision

`ACCEPTED`

Q-011 passes both the normal-Goose compatibility gate and the material latency gate.
Campaign 007 is accepted, published and closed.

## Control

- Role: FOREMAN
- Harness mode: `STRICT_CAMPAIGN`
- Gate: `Q-011` bounded-parallel Goose compatibility and latency evidence
- Protocol: `harness/contracts/CAMPAIGN-007-q011-live.md`
- Protocol correction: `harness/contracts/CAMPAIGN-007-q011-live-r2.md`
- Published `main`: `641ef46b6fdde380463b40d39a654cf8eb1248c2`
- Package/module: `0.9.0`
- Diagnostic build: `bounded-parallel-council-v7`
- Schema: `2.3`
- Evidence boundary: six user-designated persisted full JSON records under ignored
  `.tmp/q011`; Goose prose was not used as structured telemetry
- Excluded record: `20260813T065923763611Z_41725e75a3ee` was not designated as S1-S3 or
  P1-P3 and was not included in any calculation

## Protocol correction

The issued r1 protocol named conceptual role aliases and `sample_status="success"`.
Published V0.9 source, tests and records use the canonical IDs frozen by r2 and the
literal status `structured_success`. This was a Foreman protocol defect, not a product
or live-run defect. The input case, A/B configuration and thresholds were unchanged;
no rerun was required.

## Literal evidence

| Run | Review ID | Wall ms | Sampling wait ms | Limit | Peak | Batches | Calls | Success/unavailable | Coverage |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | --- | --- |
| S1 | `20260813T065611953868Z_284178e299d4` | 16,009 | 16,001 | 1 | 1 | 6 | 6 | 6/0 | full |
| S2 | `20260813T065649465256Z_a50c24de8d8e` | 27,214 | 27,207 | 1 | 1 | 6 | 6 | 6/0 | full |
| S3 | `20260813T065706455989Z_dd6f57eb25a4` | 16,363 | 16,356 | 1 | 1 | 6 | 6 | 6/0 | full |
| P1 | `20260813T070205951458Z_0d5d78615646` | 5,639 | 15,409 | 3 | 3 | 2 | 6 | 6/0 | full |
| P2 | `20260813T070235520489Z_d90cc3be2934` | 5,712 | 16,726 | 3 | 3 | 2 | 6 | 6/0 | full |
| P3 | `20260813T070301354900Z_8073776e5d1e` | 5,914 | 16,843 | 3 | 3 | 2 | 6 | 6/0 | full |

Record SHA-256 values:

- S1: `338582A31EBC5CD6729EA2EFDD157CB5B6987F57BD8F1DE6047DBD3080E4E39C`
- S2: `BE1C5DA230D0401E385CA05AAE5CFA73360D21B90993F95F55FB75FEDFD88331`
- S3: `34CBE865673E57D2403CEEAF73B4B8502F505B857D4D37449B73A1971FC30102`
- P1: `AF1941FC3B2F7D7E4216D4C39119F051133C5C405CD0F1D27AD3C9BF431FF43A`
- P2: `A272F6AD600FB0D6FFE1F2EFD5E6B94F058B80BFF339F8816218C91E36D53512`
- P3: `94C3A19B51D189038752AA15A0AC262D95A34BBEC3197DD9170D92E8740AD655`

## Compatibility gate

All six records independently satisfy the required invariants:

- identical frozen review task, same standard marketing route, briefing off,
  interaction off, summary trace and full persistence;
- package `0.9.0`, build `bounded-parallel-council-v7`, schema `2.3`;
- canonical six roles in frozen order in both the plan and process digest;
- all 36 independent samples are `structured_success`;
- each record has exactly six sampling calls, zero elicitation calls, zero parse
  failures, zero discussion rounds and no reconsideration;
- coverage is `full`, status is `COMPLETED`, degradation is false, warnings and fallback
  are empty;
- all six primary reports have the same four-section structure, preserve all six role
  lenses and end with `## 主编结论`;
- `review_only` remains effective: chief `suggested_translation` is null;
- sequential records are exactly limit/peak/batches `1/1/6`; parallel records are
  exactly `3/3/2`; all dispositions are `configured`;
- no empty response, MCP error, timeout, rate-limit failure or coverage loss occurred.

Compatibility is accepted.

## Latency gate

- Sequential wall values: `16,009`, `27,214`, `16,363` ms.
- Sequential median: `16,363` ms.
- Parallel wall values: `5,639`, `5,712`, `5,914` ms.
- Parallel median: `5,712` ms.
- Required maximum for a 25% reduction: `12,272.25` ms.
- Observed reduction: `65.09%`.
- Observed median speedup: `2.86x`.

The parallel median is substantially below the required threshold. In P1-P3,
`sampling_wait_ms` exceeds wall time while peak concurrency is three, which is the
expected sum-of-waits behavior under real overlap and corroborates that Goose did not
serialize the six provider callbacks.

Latency is accepted.

## Remaining risk

This gate establishes compatibility and material speedup for the provider/model/account
used in these six runs. It does not prove identical rate-limit behavior for every Goose
provider. Operators retain `COUNCIL_REVIEW_CONCURRENCY=1` as the safe sequential
override; default limit three is validated for the tested normal-Goose path.

No source, tests, dependencies, lockfiles, Goose installation, credentials, Git remote
or GitHub state were changed during live acceptance.
