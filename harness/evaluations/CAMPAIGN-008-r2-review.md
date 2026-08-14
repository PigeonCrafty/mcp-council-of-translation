# Foreman Review: CAMPAIGN-008-r2

## Decision

`CHANGES_REQUESTED`

r2 已经修复 r1 的用户可见矛盾，并把 18 案例语料转化为真实执行生产编排的
离线证据；但是其“等价 preflight/model 问题只计一次”只覆盖占位符与标签。
Foreman 对同一合同范围内的 required literal、数字一致性和 URL 做扩展反例后，
仍能稳定复现一个底层问题被计为两个独立贡献。一次很小的 r3 结构化关联修订即可
完成 Campaign 008，本轮不接受整体 Campaign。

## Control and scope

- Role: FOREMAN
- Mode: STRICT_CAMPAIGN
- Contract: `harness/contracts/CAMPAIGN-008-r2.md`
- Contract SHA-256:
  `9F01492711FDCA0CCF27D74851E8A3FDB26DA6454524CC4DAA799FA48E1201BB`
- Baseline: `6e28c103f98a6b0481ab7d103580b83f8e6c4cfa`
- Worker final HEAD: `6464f96f681aa3531c14cd631689673561193027`
- Commits: `c4c8fc616afedf9977c314e93e721d346367dd27`,
  `6464f96f681aa3531c14cd631689673561193027`
- Diff: seven authorized paths, 777 insertions and 89 deletions; no scope mismatch;
  index empty; `git diff --check` passed
- Contract and all ten protected hashes independently matched
- Worker report: present, complete and consistent with repository state

## Independently accepted r2 evidence

- Fresh compile passed.
- Fresh complete regression: `269 passed in 3.95s`.
- Fresh r2-focused suite: `17 passed in 0.58s`.
- The original `Delete {count} files` -> `删除文件` counterexample now reports one
  unique material issue, marks the technical role correctly, retains human review and no
  longer prints the false-clean line.
- Placeholder and markup preflight/model duplicates collapse to one logical contribution
  while full clusters/evidence remain retained. An unavailable technical sample remains
  `unavailable` while the deterministic issue stays visible.
- The compatibility display no longer assigns contribution kinds from natural role
  prose; it explicitly says that structured contribution metrics are absent.
- The fixture contains exactly 18 cases and no fixture-authored `observed` object.
  `evaluate_golden_cases()` invokes real `run_structured_review()` and, for the authority
  boundary, real `continue_structured_review()` with deterministic scripted gateways.
- Fresh Foreman corpus execution returned 18/18, eight aggregate metrics at 1.0, 113
  scripted samples and four scripted elicitations. Input/envelope mutations rerun the
  production path and are detected.
- Context-update and invalid-outcome authority paths are exercised through real forms and
  continuation rather than copied expected values.
- Package/module `0.10.0`, build `evidence-value-council-v8`, schema `2.4`, exact five
  tools, review-only, budgets 6/13/18 and concurrency controls remain unchanged.
- Worker fresh wheel/sdist and isolated FastMCP 3.4.7 evidence is credible; r3 must
  regenerate artifacts after the final production correction.

This preserves the executable Golden Corpus, evaluator, digest correction, all r1
accepted evidence, and the placeholder/markup/unavailable portions of PKG-047.

## Failed acceptance criterion: structured equivalence is incomplete

The r2 contract requires one underlying deterministic/model-supported issue to contribute
once and explicitly includes blocking and warning preflight evidence. The implementation
extracts only a limited `_STRUCTURED_TOKEN` set. Exact machine-enforced values outside
that set cannot join their equivalent model finding, while overlapping preflight scanners
can also count one token twice.

Fresh Foreman direct production-component probes produced:

```text
required_literal:Acme + matching technical finding
  clusters=2, technical.unique_issue_count=2, aggregate.unique_material_issue_count=2

numeric_parity (10 -> 9) + matching technical finding for 10
  clusters=2, technical.unique_issue_count=2, aggregate.unique_material_issue_count=2

missing https://example.com with no model finding
  command-parity reports /example
  url-parity reports https://example.com
  technical.unique_issue_count=2, aggregate.unique_material_issue_count=2
```

Each is one user-facing integrity issue. The clusters should remain as full diagnostic
evidence, but the descriptive Council value projection must not call them two independent
discoveries. This violates r2 PKG-047 criteria 1, 3 and 4 and the frozen rule that
repeated/synonymous evidence cannot inflate contribution.

The defect is bounded to logical-issue correlation in `value_metrics.py`. It does not
invalidate the correctness decision, Policy Gate, Golden production runner, persistence,
presentation layout or public API.

## Required r3 correction

1. Build preflight-rooted exact structured aliases for all existing deterministic
   preflight families: placeholders/printf/variables, commands, tags, URLs, caller DNT,
   required/forbidden literals, numeric parity and Markdown structural signals.
2. Join a model cluster only through exact bounded anchors/constraint tokens derived from
   the deterministic cluster. Do not inspect topic/problem/evidence prose, use fuzzy
   similarity or add a model call.
3. Join overlapping deterministic scanners when they identify the same exact underlying
   token, including the command-like URL path plus full URL counterexample.
4. Preserve every original cluster and evidence item. Correlation changes only value
   counts and contribution classification.
5. Prove distinct deterministic issues remain distinct; shared role/category alone must
   never merge them.
6. Preserve unavailable precedence, placeholder/tag behavior, zero-call behavior and the
   accepted 18-case executable aggregate.

## Authority and remaining risk

- Foreman production/test edits: 0
- Live calls: 0
- External mutations: 0
- Subagents: 0
- Fresh artifact rebuild not repeated after the deterministic acceptance defect was
  established; r3 must rebuild once after correction
- Remaining post-r3 risk: live model usefulness and non-repetition remains Q-012

