# CAMPAIGN-008-r4 Main Worker Report

## Terminal status

READY_FOR_REVIEW

This is a Worker handoff only. Campaign acceptance and Q-012 acceptance remain with the
Foreman.

## Control and admission

- Role/mode: `WORKER / MAIN WORKER`, `STRICT_CAMPAIGN`.
- Contract: `harness/contracts/CAMPAIGN-008-r4.md`.
- Contract SHA-256:
  `6A7B8F48BA20005174D0BF5871D3073BA72CEC9694B7D7C3F9193D296D35F3A7`.
- Exact admitted baseline: `c3fcfec363878d069b64e15a65a364c7fd55468b`, subject
  `Complete deterministic issue correlation`.
- Admission index: empty. The declared Foreman/user dirty and untracked assets were
  recorded and protected.
- Admission compile: passed.
- Admission complete regression: `276 passed in 4.30s`.
- Subagents were forbidden and none were used.

## Scoped correction and commit

Exactly one local commit was created and was not pushed:

- `84c6c64d40836875cf6515a6bf0c615c9e5ea0c9` —
  `Preserve model-only issue identity`

Baseline-to-final paths are exactly:

- `src/council_of_translation/localization/value_metrics.py`
- `tests/unit/test_v24_value_metrics.py`

The correction freezes the number of deterministic-preflight-rooted logical groups
before reviewer attachment. Reviewer exact aliases are matched only against that frozen
prefix. A reviewer cluster with no deterministic match is appended as its own production
issue identity, and later reviewer clusters cannot join it through the r3 alias layer.
Reviewer clusters may still attach to multiple distinct deterministic groups without
bridging those groups. No clustering, preflight, schema, API, dependency, prompt, Policy
Gate or call behavior changed.

## Before/after and controls

The direct Foreman-shaped counterexample used two production clusters at the same
`Continue` / `继续` anchors:

- correctness/accuracy from `fidelity_reviewer`;
- language-choice/terminology from `terminology_reviewer`.

Before r4, production returned two cluster IDs but metrics incorrectly reported
`unique_material_issue_count=0`, `corroborated_issue_count=1`, and both roles as
`corroborating`.

After r4, the same two production clusters remain byte-for-structure and metrics report
`unique_material_issue_count=2`, `corroborated_issue_count=0`, one unique issue per role,
and both roles as `unique_material`.

The same-family control uses two accuracy findings from fidelity and risk roles.
Production clustering still returns one cluster; metrics report one corroborated issue
and both roles remain `corroborating`. Thus value metrics consume production model
identity rather than recreating semantic clustering.

The existing required-literal deterministic/model test still retains two source clusters
and reports one logical issue. All r3 required/forbidden literal, numeric, four Markdown,
DNT, URL overlap, placeholder+URL, distinct-literal, unavailable, tag, duplicate-role,
discussion and clean zero-call tests remain green.

## Verification

- New cross-family and same-family controls plus the complete r3 deterministic matrix:
  `tests/unit/test_v24_value_metrics.py` and
  `tests/integration/test_v24_value_metrics.py` -> `19 passed in 0.31s`.
- All V2.4 model/metrics/persistence/presentation/Golden suites:
  `30 passed in 0.76s`.
- Exact executable Golden corpus: `18/18`, failed IDs `[]`; all eight aggregate metrics
  remained `1.0`; runtime totals remained exactly `113` scripted samples and `4`
  scripted elicitations.
- Compatibility, V1/V2.0-V2.3 reads, V2.4 persistence/privacy, five-tool release,
  budget and concurrency invariant selection: `77 passed in 2.64s`.
- Clean value-metrics path remains sampling/elicitation neutral.
- Pre-commit compile: passed; complete regression: `278 passed in 5.01s`.
- Final `python -m compileall -q src tests`: passed.
- Final complete regression: `278 passed in 4.56s`.
- Baseline-to-HEAD `git diff --check`: passed.
- AST dead-import scan: `DEAD_IMPORTS=[]`.

## Fresh artifacts and installed-wheel smoke

Fresh `uv build` produced:

- `council_of_translation-0.10.0-py3-none-any.whl`, 88,461 bytes, SHA-256
  `6AE0D1B5DD8B72C9E477E5636C80AE091BC78B1F9060AA5C7680CDE6D2C791E5`.
- `council_of_translation-0.10.0.tar.gz`, 81,620 bytes, SHA-256
  `C28A67F0576FB1DE3779EBEBA53F0CFFAA3E1D1DB6B156E6EFB34B9DB3A9EC73`.

The wheel was installed into isolated Python `3.12.9` with cached current FastMCP
`3.4.7`. In-memory smoke called all five tools in frozen order and verified
package/module `0.10.0`, build `evidence-value-council-v8` and schema `2.4`.
Installed-wheel production probes returned:

- cross-family model-only: two clusters, two unique issues, zero corroborated issues;
- required literal plus matching technical reviewer: two clusters, one logical issue.

No Goose, provider or model was called.

## Git and protected assets

- Final HEAD: `84c6c64d40836875cf6515a6bf0c615c9e5ea0c9`.
- Baseline-to-HEAD commit count: exactly one.
- Baseline diff: exactly two authorized paths, 59 insertions and 1 deletion.
- Final Git index: empty.
- This report is the only new r4 Harness asset and is intentionally untracked.
- Final worktree otherwise matches admission: modified Foreman-owned plan/features/
  progress and untracked protected `.learnings/`, Campaign 008 contracts/evaluations/
  prior reports/ledger, audit Markdown and `reviews/`.
- All temporary pytest, artifact and isolated-wheel directories created by this Worker
  were removed after evidence capture.

Protected SHA-256 values matched the contract at admission and handoff:

- plan: `AA14085768FF6A910EB0A9028D02FABD552DBB829DF7F085DC1D2268B21530B0`
- features: `A5E1A5030C9A307F4A3FE55682D9E5F49A6789C11D34C20F5A407084141DF984`
- progress: `4DC02397918A1B44B8D08CD6DFE7030EC482558FD075784937C5410A2A175DDC`
- r1/r2/r3 contracts:
  `3D477E8418B77A621EFEBB3BD496CD0508BCC9C39A22D833EFA79886A98EE366`,
  `9F01492711FDCA0CCF27D74851E8A3FDB26DA6454524CC4DAA799FA48E1201BB`,
  `25E38BE0AD014A0B0F7A5F7351FCFB93AE63FC0EAE283CDD8357AA3E7005EF6B`
- r1/r2/r3 evaluations:
  `D85B7C35026C394001C7C17DE5FCE591128D917BB1961FA67ADED19E88FE3292`,
  `AC8E122CFC3AF539E4E74E8B8DE99845258D81F7AFF7B28BF87EB1F8850DE6EC`,
  `95A78CA651F50C8931AE434C72093BCC4466D3E97A4F70238969D37066D8F659`
- r1 Worker report/ledger and r2/r3 Worker reports:
  `412A1E032B919289630EAE58A386B45EF5869B10C91C9FEC76C78313DC8AA37F`,
  `26AD64BE56B776B9EECD07F927C116E9B360746194D1CE026E3AEE0295A5068A`,
  `12E9B7ECDE549ACCCF79B649446D7838BBDA586589363B4E86A2E92A9177A698`,
  `54559EE4256B0DB62D343B8745B94CD98CA8508686CC64960DEBC836111A7CE6`
- `.learnings/LEARNINGS.md` / `.learnings/ERRORS.md`:
  `52DC1BA8043481911C0DEABB3AC882504D9CBE8BB63D60F391C188586A230DF0`,
  `F99EB75886781958BF5AE6DCF844FD476CBCA45937896A25EE3B2E9D6CD34F0A`
- audit Markdown:
  `B48073E063C4C9F34E0B6B4DAE94E80079EAAAD3B2F8E273DD60B2F25F6ABD76`

## Authority, skipped work and risks

- Authority escalations: seven bounded invocations — exact two-path `git add`, one
  `git commit`, fresh `uv build`, isolated `uv venv`, offline `uv pip install`, artifact
  hashing and cleanup of the two verified repository-local temporary directories.
- External dependency operations: three uv operations. The isolated install used
  `--offline`; no provider endpoint was contacted.
- Subagents: `0`.
- Live Goose/provider/model calls: `0`.
- Pushes, PR operations, releases, deployments and credential operations: `0`.
- No required verification was skipped. Contract-prohibited Q-012/live, push, PR,
  release and deployment work was not performed.
- Remaining risk: exact deterministic attachment intentionally does not merge separate
  model-only production clusters, even when their text anchors coincide. Live usefulness
  remains the separate post-publication Q-012 Foreman gate.
- This report makes no Campaign acceptance, publication or project-completion claim.
