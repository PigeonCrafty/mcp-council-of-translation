# Live Gate Protocol: CAMPAIGN-007 Q-011

## Control

- Role: FOREMAN
- Gate: `Q-011` bounded-parallel Goose compatibility and latency evidence
- Published `main` snapshot at protocol issuance:
  `641ef46b6fdde380463b40d39a654cf8eb1248c2`
- Transport command: retain the normal unpinned `main` command; do not replace it with a
  commit-pinned command for this or later normal-user tests
- Required package/module: `0.9.0`
- Required diagnostic build: `bounded-parallel-council-v7`
- Required schema: `2.3`
- Provider/model rule: use the same configured Goose provider, model and account for all
  measured runs
- Mutation boundary: live provider calls and review-record writes are authorized; source,
  tests, lockfiles, dependencies, Goose installation, credentials, Git and GitHub state
  must not be changed by this gate

Q-011 is a post-publication Foreman gate, not a Worker implementation contract. It tests
the normal Goose sampling path that the deterministic FastMCP callback could not prove.

## Why this is an A/B test

The only independent variable is `COUNCIL_REVIEW_CONCURRENCY`:

- control: `1`, which forces six sequential independent-review batches;
- treatment: `3`, which permits two batches of three reviewers.

Use one dedicated `COUNCIL_REVIEWS_DIR`; each record carries its effective concurrency,
and the six review IDs make the literal persisted records unambiguous. Do not use Goose's
prose reconstruction of hidden structured fields as telemetry evidence. The primary
report is valid UX evidence; the JSON record is the telemetry authority.

## Goose STDIO configuration

Keep the existing extension command and arguments unchanged. For each arm, change only
the concurrency environment value, then fully restart Goose so a new STDIO server
process receives it. The review-directory value is set once and remains unchanged.

```yaml
extensions:
  pigeoncounciloftranslation:
    type: stdio
    name: pigeoncounciloftranslation
    enabled: true
    cmd: uvx
    args:
      - --refresh
      - --from
      - git+https://github.com/PigeonCrafty/mcp-council-of-translation
      - mcp_council_of_translation
    envs:
      COUNCIL_REVIEW_CONCURRENCY: "1"
      COUNCIL_REVIEWS_DIR: 'C:\Users\GeZhu\MyMCP\mcp-council-of-translation\.tmp\q011'
    timeout: 300
```

For the treatment arm, change only:

```yaml
    envs:
      COUNCIL_REVIEW_CONCURRENCY: "3"
      COUNCIL_REVIEWS_DIR: 'C:\Users\GeZhu\MyMCP\mcp-council-of-translation\.tmp\q011'
```

The command therefore remains exactly:

```text
uvx --refresh --from git+https://github.com/PigeonCrafty/mcp-council-of-translation mcp_council_of_translation
```

Because this intentionally follows `main`, do not push any repository change between the
two arms. The `get_server_info` admission check is mandatory on every run; a version,
build or schema mismatch invalidates the comparison before sampling starts.

On Windows, Goose's normal configuration file is
`%APPDATA%\Block\goose\config\config.yaml`. Desktop Settings may be used instead when it
exposes the same command, arguments and environment fields.

## Frozen review case

Each measured run must call `get_server_info` once, then call `review_translation` once
with these exact values:

```json
{
  "source_text": "Bigger than bigger",
  "candidate_translation": "比大更大",
  "source_language": "en",
  "target_language": "zh-CN",
  "content_type": "marketing",
  "context": "中国大陆官网首页的纯品牌宣传标语，不是按钮、CTA、导航或任何交互控件。",
  "audience": "中国大陆普通消费者",
  "mode": "standard",
  "output_mode": "review_only",
  "interactive_mode": "off",
  "briefing_mode": "off",
  "decision_fallback": "council_adjudication",
  "trace_level": "summary",
  "history_mode": "full",
  "term_glossary": "Bigger than bigger = 比大更大（项目批准译法）",
  "style_guide": "品牌标语保持短促、自然、有冲击力。",
  "project_rules": "本条为已批准的品牌宣传标语，不得改写为按钮或功能文案。",
  "brand_guidelines": "保留项目批准译法‘比大更大’，除非发现语义、技术完整性或明确硬规则冲突。",
  "reference_translations": "Bigger than bigger -> 比大更大（approved）",
  "technical_constraints": "纯文本；无占位符；不承担交互动作。",
  "do_not_translate_literals": [],
  "hard_constraints": [],
  "known_exceptions": "无",
  "notes": "Q-011 固定六角色并发 A/B 用例。"
}
```

Do not call `view_review_record` or `list_review_records` inside a measured run. They do
not affect the server-reported review wall time, but extra agent turns make the user's
perceived duration unsuitable for the A/B comparison.

## Goose instruction

Paste this instruction into a fresh Goose session for every run:

```text
这是 Council of Translation V0.9 的 Q-011 实测。只允许依次调用两个工具：
1）get_server_info；2）review_translation 一次。不要调用 view_review_record、
list_review_records 或 continue_review，不要自行补造结构化字段。

先确认 package_version=0.9.0、diagnostic_build=bounded-parallel-council-v7、
schema_version=2.3，并报告 independent_review_concurrency_limit 与 disposition。
若版本或并发值不符，立即停止。

review_translation 必须使用以下参数：
source_text="Bigger than bigger"
candidate_translation="比大更大"
source_language="en"
target_language="zh-CN"
content_type="marketing"
context="中国大陆官网首页的纯品牌宣传标语，不是按钮、CTA、导航或任何交互控件。"
audience="中国大陆普通消费者"
mode="standard"
output_mode="review_only"
interactive_mode="off"
briefing_mode="off"
decision_fallback="council_adjudication"
trace_level="summary"
history_mode="full"
term_glossary="Bigger than bigger = 比大更大（项目批准译法）"
style_guide="品牌标语保持短促、自然、有冲击力。"
project_rules="本条为已批准的品牌宣传标语，不得改写为按钮或功能文案。"
brand_guidelines="保留项目批准译法‘比大更大’，除非发现语义、技术完整性或明确硬规则冲突。"
reference_translations="Bigger than bigger -> 比大更大（approved）"
technical_constraints="纯文本；无占位符；不承担交互动作。"
do_not_translate_literals=[]
hard_constraints=[]
known_exceptions="无"
notes="Q-011 固定六角色并发 A/B 用例。"

工具完成后，只输出 get_server_info 的并发值、原始 display_report 和 review_id。
不要追加诊断工具调用，也不要把你推测的 telemetry 当作工具原始数据。
```

## Run count and order

1. Set limit `1`, fully restart Goose, and run the frozen case three times in fresh
   sessions. Record the three review IDs as `S1`, `S2`, `S3`.
2. Set limit `3`, fully restart Goose, and run the same case three times in fresh
   sessions. Record the three review IDs as `P1`, `P2`, `P3`.
3. If a run has any sampling count other than six, any elicitation, discussion or
   reconsideration sampling, or a provider retry/error, label it invalid for latency and
   rerun it once. Preserve the invalid record for diagnosis.

Three runs per arm are the minimum latency sample. A single run per arm is sufficient
only for compatibility smoke evidence, not for accepting a performance claim.

## Literal record extraction

After all six valid runs, extract the persisted JSON directly. This PowerShell command is
read-only and selects the newest six records in the dedicated directory:

```powershell
$q011Rows = Get-ChildItem -LiteralPath 'C:\Users\GeZhu\MyMCP\mcp-council-of-translation\.tmp\q011' -Filter '*.json' |
  Sort-Object LastWriteTime |
  Select-Object -Last 6 |
  ForEach-Object {
    $q011Record = Get-Content -LiteralPath $_.FullName -Raw | ConvertFrom-Json
    [pscustomobject]@{
        arm = if ($q011Record.runtime_metadata.independent_review_concurrency_limit -eq 1) { 'sequential' } else { 'parallel' }
        review_id = $q011Record.review_id
        wall_ms = $q011Record.runtime_metadata.wall_clock_ms
        sampling_wait_ms = $q011Record.runtime_metadata.sampling_wait_ms
        sampling_calls = $q011Record.runtime_metadata.sampling_calls
        limit = $q011Record.runtime_metadata.independent_review_concurrency_limit
        peak = $q011Record.runtime_metadata.independent_review_peak_concurrency
        batches = $q011Record.runtime_metadata.independent_review_batch_count
        disposition = $q011Record.runtime_metadata.independent_review_concurrency_disposition
        successful = $q011Record.runtime_metadata.reviewer_samples_successful
        unavailable = $q011Record.runtime_metadata.reviewer_samples_unavailable
        coverage = $q011Record.runtime_metadata.reviewer_coverage
        status = $q011Record.status
        degraded = $q011Record.degraded
        warnings = ($q011Record.warnings -join '|')
        fallback = $q011Record.fallback_reason
    }
  }
$q011Rows | Sort-Object arm, review_id | Format-Table -AutoSize
```

Return the six review IDs and this table to the Foreman. The Foreman will independently
open the six JSON files, verify the full role/status fields, calculate each arm's median
`wall_clock_ms`, and archive the decision in
`harness/evaluations/CAMPAIGN-007-q011-live-review.md`.

## Acceptance matrix

### Compatibility gate — all six valid records

- package/module `0.9.0`, build `bounded-parallel-council-v7`, schema `2.3`;
- the frozen role IDs `fidelity_reviewer`, `terminology_consistency_manager`,
  `product_context_reviewer`, `brand_tone_gatekeeper`, `risk_ambiguity_reviewer` and
  `naturalness_polisher` are present in that order, and all six independent samples have
  `sample_status="success"`;
- `sampling_calls=6`, reviewer success/unavailable `6/0`, coverage `full`;
- no elicitation, discussion or reconsideration sampling;
- `status=COMPLETED`, `degraded=false`, empty warnings and no fallback;
- primary report retains the six role lenses and ends with the chief disposition;
- control records: limit/peak/batches `1/1/6`, disposition `configured`;
- treatment records: limit/peak/batches `3/3/2`, disposition `configured`;
- no MCP protocol error, empty sampling response, parse failure, timeout or rate-limit
  failure.

### Latency gate

- compare medians of server-recorded `wall_clock_ms`, not Goose's total answer time;
- treatment median must be lower than control median;
- a material performance acceptance requires treatment median at most 75% of control
  median, equivalent to at least 25% lower wall time;
- report `sampling_wait_ms` for diagnostic context only. It is the sum of sampling waits
  and may exceed wall time under real parallelism.

## Decision rules

- `ACCEPTED`: both compatibility and material-latency gates pass.
- `CHANGES_REQUESTED`: correctness/compatibility passes but the treatment median is not
  at least 25% lower, or measured records contain avoidable extra phases.
- `BLOCKED`: the provider is unavailable, the tested commit/configuration cannot be
  established, or literal record files cannot be obtained after exhausting the isolated
  review directories.
- Any coverage loss, protocol failure or rate-limit regression at limit `3` rejects the
  parallel default for this provider even if one wall-time number is faster.
