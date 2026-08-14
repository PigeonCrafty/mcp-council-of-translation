# Foreman Review: CAMPAIGN-008-r1

## Decision

`CHANGES_REQUESTED`

V2.4 的模型、持久化、一般贡献度计算、价值优先展示和 V0.10 迁移已经形成可信基础，
但两个验收缺口会直接影响产品结论：确定性 preflight 阻断项没有进入 Council 价值
指标；18 案例 Golden Corpus 也没有执行生产路径，而是比较夹具中预先写成相同值的
`expected` 与 `observed`。这些问题可以通过一个边界清晰的 r2 修订解决，不需要推翻
r1 架构。

## Control and scope

- Role: FOREMAN
- Mode: STRICT_CAMPAIGN
- Contract: `harness/contracts/CAMPAIGN-008-r1.md`
- Contract SHA-256:
  `3D477E8418B77A621EFEBB3BD496CD0508BCC9C39A22D833EFA79886A98EE366`
- Baseline: `c4d2e42f5bfee377cdbebaed776272cb996c679c`
- Worker final HEAD: `6e28c103f98a6b0481ab7d103580b83f8e6c4cfa`
- Commits inspected: `5cec253`, `6d03558`, `6baa9fc`, `f68969c`, `6e28c10`
- Diff: 31 authorized paths, 1,074 insertions and 88 deletions; index empty;
  `git diff --check` passed
- Worker report and ledger: present, internally consistent and preserved
- Protected Foreman/user assets: preserved; no scope mismatch found

## Independently accepted r1 evidence

- Fresh compile passed.
- Fresh full regression: `263 passed in 3.84s`.
- Fresh Campaign-focused suite: `13 passed in 1.08s`.
- V2.4 `RoleContribution` and `CouncilValueMetrics` are bounded and persisted with a
  privacy-safe metadata projection; V1 and V2.0 through V2.3 remain readable.
- Structured model-finding paths correctly distinguish unique, corroborating,
  confirmation-only and unavailable roles in the covered cases. Duplicate findings from
  one role do not multiply its counts, and rephrased discussion prose alone does not
  create marginal value.
- Normal orchestration computes the metrics from existing artifacts and adds no sampling
  or elicitation.
- The primary report uses the frozen five-section value-first order, accounts for active
  roles, keeps degradation/minority information visible and leaves the chief disposition
  last within the existing 3,200-code-point bound.
- Package/module `0.10.0`, build `evidence-value-council-v8`, schema `2.4`, exact five
  tools, review-only behavior, budgets 6/13/18 and concurrency controls are preserved.
- Worker fresh wheel/sdist and isolated FastMCP 3.4.7 smoke evidence is credible. It must
  be regenerated after r2 because production/evaluation behavior will change.

This evidence preserves PKG-042, the discussion-delta and ordinary model-finding parts of
PKG-043, most of PKG-044, and the packaging/compatibility portion of PKG-046 unless r2
invalidates them.

## Acceptance defect 1: deterministic blockers disappear from value metrics

`value_metrics._material_roles()` currently returns no roles whenever an issue cluster
has no `finding_ids`. Deterministic preflight clusters intentionally have structured
participant roles and evidence but no model finding IDs, so a real placeholder-loss
blocker is discarded from the contribution projection.

The Foreman reproduced this through both the direct preflight/cluster/metric path and a
complete scripted `run_structured_review` path using:

```text
source:    Delete {count} files
candidate: 删除文件
```

The correctness path properly returned `NEEDS_HUMAN_REVIEW` and a missing-placeholder
fix, but `council_value_metrics` reported:

```text
technical_safety_reviewer = confirmation_only
unique_material_issue_count = 0
confirmation_only_role_count = 6
```

The primary report consequently said “未发现新增实质问题；6 个角色完成确认性覆盖”
before later sections disclosed the blocker. This is a user-visible contradiction and
fails F-040 and F-042, as well as Golden case 1.

A naïve inclusion of every preflight cluster would create a second defect: when the
technical reviewer also returns an equivalent model finding, preflight and model
evidence currently occupy separate clusters and could double-count the same issue. r2
must correlate/deduplicate equivalent deterministic and model-supported issue-local
contributions while retaining both evidence sources in full history.

## Acceptance defect 2: free-form fallback classification violates the frozen basis

`digest._fallback_value_metrics()` classifies role lenses by inspecting free-form prose,
including substring checks such as `不可用`, and can infer `unique_material` from the
rendered lens text. The r1 contract explicitly forbids semantic scoring of free-form
prose with substring heuristics. When structured metrics are unavailable, presentation
must use conservative structured/default accounting and must not invent unique material
value from natural text.

## Acceptance defect 3: the 18-case corpus is not executable product evidence

The fixture contains all 18 required case names, but every case stores a manually copied
`observed` object identical to `expected`. `evaluate_golden_cases()` only compares those
two dictionaries. It does not run preflight, reviewer-envelope validation, clustering,
context/outcome interaction, Policy Gate, adjudication, contribution metrics or the
chief decision. The tests prove only that identical fixture dictionaries compare equal,
then mutate a few already-derived values to prove the comparator can notice inequality.

This structure allowed the placeholder-loss defect above to coexist with a perfect
Golden aggregate. PKG-045 and F-043 therefore remain unaccepted. The corpus must retain
machine-checkable expectations but derive observations by executing deterministic
production paths with scripted reviewer/interaction inputs and no provider call.

## Required r2 correction

1. Treat deterministic preflight integrity clusters as material structured evidence and
   attribute them to their registered participant role(s).
2. Correlate equivalent preflight and model findings issue-locally so one underlying
   issue does not multiply unique/corroborating counts or authority.
3. Preserve unavailable-role precedence and all existing ordinary structured-finding and
   discussion-delta behavior.
4. Remove free-form/substr-based contribution classification from the digest fallback.
   Missing metrics may yield conservative coverage/default labels, but not invented
   unique contributions.
5. Replace fixture-provided observations with an offline executable 18-case harness.
   Expectations stay declarative; observations must be derived from real production
   components using bounded scripted samples/interactions.
6. Add explicit placeholder-loss, broken-markup, preflight-plus-equivalent-model-finding,
   unavailable-technical-role and primary-report contradiction counterexamples.
7. Rerun compile, full regression, exact corpus/aggregate checks, zero-call/budget checks,
   fresh package build and isolated current-FastMCP smoke.

No live Goose/provider call is required or authorized in r2. Q-012 remains a separate
post-publication live usefulness gate.

## Authority and remaining risk

- Foreman production edits: 0
- Foreman test/fixture edits: 0
- Live calls: 0
- External mutations: 0
- Subagents: 0
- Decision basis: source/diff inspection, fresh automated verification and two locally
  scripted deterministic counterexamples
- Remaining risk after r2: live Goose usefulness/non-repetition still requires Q-012

