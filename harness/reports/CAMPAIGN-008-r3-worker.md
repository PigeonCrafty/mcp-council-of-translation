# CAMPAIGN-008-r3 Main Worker Report

## Terminal status

READY_FOR_REVIEW

This is a Worker handoff only. Campaign acceptance and Q-012 acceptance remain with the
Foreman.

## Control and admission

- Role/mode: `WORKER / MAIN WORKER`, `STRICT_CAMPAIGN`.
- Contract: `harness/contracts/CAMPAIGN-008-r3.md`.
- Contract SHA-256:
  `25E38BE0AD014A0B0F7A5F7351FCFB93AE63FC0EAE283CDD8357AA3E7005EF6B`.
- Exact admitted baseline: `6464f96f681aa3531c14cd631689673561193027`, subject
  `Execute V2.4 offline golden corpus`.
- Admission index: empty. The declared Foreman/user dirty and untracked assets were
  recorded and protected.
- Admission compile: passed.
- Admission complete regression: `269 passed in 4.17s`.
- Subagents were forbidden and none were used.

## Scoped correction and commit

Exactly one local commit was created and was not pushed:

- `c3fcfec363878d069b64e15a65a364c7fd55468b` —
  `Complete deterministic issue correlation`

Baseline-to-final implementation/test paths are exactly:

- `src/council_of_translation/localization/value_metrics.py`
- `tests/unit/test_v24_value_metrics.py`
- `tests/integration/test_v24_value_metrics.py`

The correction builds bounded NFKC/case-folded exact aliases only from cluster
source/candidate spans and recognized `required_literal:` / `forbidden_literal:`
constraint prefixes. Deterministic scanners are grouped first; a reviewer cluster may
corroborate a deterministic group only through an exact alias and cannot bridge two
otherwise distinct deterministic issues. URL structure contributes the exact slash-token
alias produced by the command scanner. No topic, problem, evidence prose, fuzzy rule,
embedding, vote, model call or public behavior is involved.

All original clusters, findings, preflight checks and evidence remain unchanged. Focused
tests compare each cluster's full JSON projection before and after metric computation.
Only descriptive logical counts and role contribution projection change.

## Required counterexamples

- `required_literal:Acme` plus technical anchor `Acme`: two retained clusters, one
  logical material issue.
- `forbidden_literal:危险` plus technical anchor `危险`: two retained clusters, one
  logical material issue.
- hard `numeric_parity`, `10 -> 9`, plus technical anchor `10`: two retained clusters,
  one logical material issue.
- hard Markdown parity for each `heading`, `list`, `link` and `fence` signal plus its
  exact structured reviewer anchor: two retained clusters and one logical issue in each
  case.
- explicit DNT loss for `Pigeon` plus exact technical anchor: two retained clusters, one
  logical material issue.
- missing `https://example.com`: command `/example` and full URL clusters both remain,
  but the value projection reports one logical issue.
- missing `{count}` plus missing `https://example.com`: three retained scanner clusters
  and two logical issues, proving placeholder and URL do not overmerge.
- distinct `required_literal:Acme` and `required_literal:Beta`: two clusters and two
  logical issues. Together with the prior case, this proves common technical role and
  integrity category alone never join issues.
- Full orchestration with failed technical sampling and missing required literal:
  technical contribution stays `unavailable`, role and aggregate issue count stay one,
  unavailable count is one, the report exposes coverage risk, the false-clean statement
  is absent, and publishability is not `可发布`.
- Existing placeholder/tag correlation, duplicate-same-role, corroboration, discussion
  delta and clean-review zero-call cases remain green.

## Verification

- New exact-correlation/non-overmerge focus:
  `tests/unit/test_v24_value_metrics.py` plus
  `tests/integration/test_v24_value_metrics.py` -> `17 passed in 0.29s`.
- All V2.4 models, metrics, presentation and Golden suites: `28 passed in 0.51s`.
- Exact executable Golden corpus: `18/18`, failed IDs `[]`; all eight aggregate metrics
  were `1.0`; runtime used `113` scripted sampling calls and `4` scripted elicitations.
  The fixture remains free of authored `observed` objects.
- Compatibility, V1/V2.0-V2.3 reads, V2.4 persistence/privacy, five-tool release
  contract, budgets, concurrency, metrics and presentation invariant selection:
  `77 passed in 2.51s`.
- Clean runtime metric probe remains four routed lightweight samples and zero
  elicitations; metric computation adds no calls.
- Pre-commit complete regression: `276 passed in 3.92s`.
- Final `python -m compileall -q src tests`: passed.
- Final complete regression: `276 passed in 3.85s`.
- Baseline-to-HEAD `git diff --check`: passed.
- AST dead-import scan for the changed production module: `DEAD_IMPORTS=[]`.

## Fresh artifacts and installed-wheel smoke

Fresh `uv build` produced:

- `council_of_translation-0.10.0-py3-none-any.whl`, 88,432 bytes, SHA-256
  `1FE25343A6178D1687616A4ED8A1CD2CCA7F9E3CB36892EF862728B3E9263349`.
- `council_of_translation-0.10.0.tar.gz`, 81,603 bytes, SHA-256
  `D42DF560AE7BDB765DC9CDB931BF8E6D8AE4F56DD7FCD96DE76B5014444CDA9B`.

The fresh wheel was installed into an isolated Python `3.12.9` environment with cached
current FastMCP `3.4.7`. In-memory FastMCP smoke called all five tools in frozen order:
`review_translation`, `continue_review`, `view_review_record`, `list_review_records`,
`get_server_info`. It verified package/module `0.10.0`, build
`evidence-value-council-v8` and schema `2.4`. Installed-wheel direct production probes
also returned `(clusters=2, logical_issues=1)` for required literal, numeric parity and
URL command/full-URL overlap. No Goose, provider or model was called.

## Git and protected-asset evidence

- Final HEAD: `c3fcfec363878d069b64e15a65a364c7fd55468b`.
- Baseline-to-HEAD commit count: exactly one.
- Baseline diff: exactly three authorized paths, 193 insertions and 8 deletions.
- Final Git index: empty.
- This report is the only new r3 Harness asset and is intentionally untracked.
- Final dirty/untracked set otherwise matches admission: modified Foreman-owned
  `harness/features.json`, `harness/plan.md`, `harness/progress.md`; untracked protected
  `.learnings/`, r1/r2/r3 contracts, r1/r2 evaluations, r1/r2 reports, r1 ledger, audit
  Markdown and `reviews/`.
- All temporary pytest, artifact and isolated-wheel directories created by this Worker
  were removed after evidence capture.

Protected SHA-256 values matched the contract at admission and final handoff:

- `harness/plan.md`:
  `98EB6C387FEE226615F1C342CB5BC7288E020027523235F91542BFAAA758800D`
- `harness/features.json`:
  `A5E1A5030C9A307F4A3FE55682D9E5F49A6789C11D34C20F5A407084141DF984`
- `harness/progress.md`:
  `F90D9BD2629FA6E8AD1F69493AE767876E1B86E316329337F3835B2A836DA3C0`
- r1/r2 contracts: `3D477E8418B77A621EFEBB3BD496CD0508BCC9C39A22D833EFA79886A98EE366`,
  `9F01492711FDCA0CCF27D74851E8A3FDB26DA6454524CC4DAA799FA48E1201BB`
- r1/r2 evaluations: `D85B7C35026C394001C7C17DE5FCE591128D917BB1961FA67ADED19E88FE3292`,
  `AC8E122CFC3AF539E4E74E8B8DE99845258D81F7AFF7B28BF87EB1F8850DE6EC`
- r1 Worker report/ledger and r2 Worker report:
  `412A1E032B919289630EAE58A386B45EF5869B10C91C9FEC76C78313DC8AA37F`,
  `26AD64BE56B776B9EECD07F927C116E9B360746194D1CE026E3AEE0295A5068A`,
  `12E9B7ECDE549ACCCF79B649446D7838BBDA586589363B4E86A2E92A9177A698`
- `.learnings/LEARNINGS.md` / `.learnings/ERRORS.md`:
  `52DC1BA8043481911C0DEABB3AC882504D9CBE8BB63D60F391C188586A230DF0`,
  `F99EB75886781958BF5AE6DCF844FD476CBCA45937896A25EE3B2E9D6CD34F0A`
- audit Markdown:
  `B48073E063C4C9F34E0B6B4DAE94E80079EAAAD3B2F8E273DD60B2F25F6ABD76`

## Incidents, authority and skipped work

- Initial non-elevated Git index write and uv user-cache reads were denied by the
  workspace sandbox. Seven bounded elevated invocations were used: exact three-path
  `git add`, one `git commit`, fresh `uv build`, isolated `uv venv`, offline `uv pip
  install`, artifact hashing and cleanup of the two verified repository-local temporary
  directories.
- The self-improvement skill was consulted after the command failure. Its requested
  `.learnings/ERRORS.md` write was skipped because this contract explicitly protects
  `.learnings/`.
- External dependency operations: three uv operations (fresh build, isolated venv and
  offline cached wheel/dependency installation). The wheel install used `--offline` and
  did not contact an index.
- Subagents: `0`.
- Live Goose/provider/model calls: `0`.
- Pushes, PR operations, releases, deployments and credential operations: `0`.
- No required verification was skipped. Contract-prohibited live Q-012, push, PR,
  release and deployment work was not performed.

## Remaining risks

- Correlation is intentionally exact and preflight-rooted. Semantically similar prose
  without an exact structured anchor remains separate, avoiding the forbidden fuzzy or
  prose-scoring behavior.
- The isolated smoke proves installed-wheel behavior with scripted/local inputs, not live
  model usefulness. Q-012 remains a separate post-publication Foreman gate.
- This report makes no Campaign acceptance, publication or project-completion claim.
