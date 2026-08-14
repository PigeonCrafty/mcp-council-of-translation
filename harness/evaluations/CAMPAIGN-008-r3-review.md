# Foreman Review: CAMPAIGN-008-r3

## Decision

`CHANGES_REQUESTED`

r3 完成了所有既定 deterministic preflight 关联反例，但引入了一个纯 reviewer
路径回归：两个生产 clustering 已明确分开的 model-only issues，只要共享相同文本
anchor，就会被价值指标重新合并为一个 corroborated issue。修复仅需在逻辑分组中
区分 preflight-rooted groups 与 reviewer-only groups；r1-r3 其余证据全部保留。

## Control and scope

- Role: FOREMAN
- Mode: STRICT_CAMPAIGN
- Contract: `harness/contracts/CAMPAIGN-008-r3.md`
- Contract SHA-256:
  `25E38BE0AD014A0B0F7A5F7351FCFB93AE63FC0EAE283CDD8357AA3E7005EF6B`
- Baseline: `6464f96f681aa3531c14cd631689673561193027`
- Worker final HEAD: `c3fcfec363878d069b64e15a65a364c7fd55468b`
- Commit: `c3fcfec363878d069b64e15a65a364c7fd55468b`
- Diff: exactly three authorized paths, 193 insertions and 8 deletions; index empty;
  `git diff --check` passed
- Contract/report/protected hashes and declared worktree state matched

## Independently accepted r3 evidence

- Fresh compile passed.
- Fresh full regression: `276 passed in 3.90s`.
- Fresh exact-correlation focus: `17 passed in 0.24s`.
- Fresh V2.4/Golden selection: `28 passed in 0.50s`.
- Required literal, forbidden literal, numeric parity, explicit DNT and missing-URL
  overlap each retain their source clusters while producing one logical contribution.
- Placeholder plus URL remains two issues; two distinct required literals remain two.
- Existing unavailable precedence and false-clean suppression remain correct.
- Golden Corpus remains executable and exact: 18/18, no failures, all eight metrics 1.0,
  113 scripted samples and four scripted elicitations.
- Version `0.10.0`, build `evidence-value-council-v8`, schema `2.4`, exact five tools,
  review-only behavior, budgets and concurrency remain unchanged.
- Worker artifact and isolated FastMCP evidence is credible; the final correction must
  regenerate artifacts once more.

## Failed acceptance criterion: reviewer-only issue identity is not preserved

The reviewer pass computes matches against every previously created group. When the first
reviewer-only cluster has no deterministic match, it is appended to `groups`; a later
reviewer-only cluster with the same exact source/candidate anchor then matches that group,
despite the comment and frozen rule that production clustering owns model-only identity.

Fresh Foreman counterexample:

```text
cluster 1: category=correctness, role=fidelity_reviewer,
           source=Continue, candidate=继续
cluster 2: category=language_choice, role=terminology_reviewer,
           source=Continue, candidate=继续
```

Production correctly returns two distinct issue IDs and families. r3 metrics incorrectly
return:

```text
unique_material_issue_count=0
corroborated_issue_count=1
fidelity_reviewer=corroborating
terminology_reviewer=corroborating
```

The truthful result is two unique material issues, one per role. Shared text location is
not proof that semantic correctness and terminology policy are the same issue. This
violates the accepted ordinary model-finding behavior and r3 requirements 2, 5 and 7.

## Required r4 correction

1. Mark or otherwise retain which logical groups are rooted in deterministic preflight
   clusters.
2. A reviewer cluster may exact-match only those deterministic-rooted groups.
3. A reviewer cluster with no deterministic match remains its own production issue group;
   later reviewer clusters must not join it through the r3 anchor alias layer.
4. Preserve production clustering's existing same-family deduplication/corroboration;
   value metrics must consume, not replace, that identity.
5. Add the cross-family same-span counterexample above plus a same-family production-
   clustered corroboration control.
6. Preserve every r3 deterministic correlation/non-overmerge test and the executable
   Golden aggregate.

## Authority and remaining risk

- Foreman production/test edits: 0
- Live calls: 0
- External mutations: 0
- Subagents: 0
- Artifact rebuild not repeated after the deterministic defect was established
- Q-012 remains the only live post-publication risk after local acceptance

