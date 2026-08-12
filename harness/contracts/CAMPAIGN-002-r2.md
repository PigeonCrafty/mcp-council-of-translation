# Correction Work Order: CAMPAIGN-002-r2

## Control

- Role: WORKER
- Mode: STRICT_SEQUENTIAL
- State: ASSIGNED
- Repository: `C:\Users\GeZhu\MyMCP\mcp-council-of-translation`
- Exact baseline commit: `5687208aaeaaf3e6b00c192fb42596fb9b6cbf47`
- Baseline subject: `Bound compact review output`
- Parent Campaign: `CAMPAIGN-002-r1`
- Required review: `harness/evaluations/CAMPAIGN-002-r1-review.md`
- Worker report: `harness/reports/CAMPAIGN-002-r2-worker.md`
- Commit policy: one or more scoped local correction commits; no push, PR, release, deployment, credentials, or Goose installation changes
- Subagent policy: forbidden; this is one tightly coupled correction slice
- Acceptance authority: Foreman only

Read `AGENTS.md`, the active Harness plan/features/progress, this work order, the r1 Foreman review, and the r1 Worker report completely before editing. Preserve r1 passing behavior and evidence unless this correction necessarily touches it.

## Admission gate

Before editing, verify and report:

1. `git rev-parse HEAD` equals the exact baseline above and resolves as a commit.
2. Index is empty.
3. Tracked dirt is limited to the Foreman-owned Harness assets below.
4. All protected hashes match exactly.
5. The complete 141-test baseline passes with repository-local temp paths.

| Protected asset | SHA-256 |
| --- | --- |
| `harness/plan.md` | `8F6556389406923598266D676E9093AEC59C1E3B4E13663E3EE105D1635450B5` |
| `harness/features.json` | `3F2286B568087CEDF2B30F808FFD57363C6729D33293E6D4E042BF70E030A204` |
| `harness/progress.md` | `9D25E762439696750F8D301B3DF534A528F07BB1E181545599B0B029B2F35774` |
| `harness/contracts/CAMPAIGN-002-r1.md` | `D58590B24E5CF2E4E7F7116F9E9F7B4D621009B6D3986CCA9A7784ECC1EC40BE` |
| `harness/evaluations/CAMPAIGN-002-r1-review.md` | `9DCBE1F727F8B38FB1B2996982015AA71E64A6A422BA05ABCC4DFE45B6226453` |
| `.learnings/LEARNINGS.md` | `22F939E6F980DF52487AAFE97EDCA9B90CF3931DDB7A31BF8A5BBB8F052E658F` |
| `mcp-council-of-translation-audit-and-upgrade-recommendations.md` | `B48073E063C4C9F34E0B6B4DAE94E80079EAAAD3B2F8E273DD60B2F25F6ABD76` |

Hash this r2 contract on admission and preserve it byte-for-byte. Also preserve `.learnings/**`, `reviews/**`, both r1 reports, every prior contract/evaluation, the audit markdown, and `myTest/` if present. The only authorized Harness write is the new r2 Worker report.

Stop as `BLOCKED` before edits if admission differs. Do not repair or stage protected assets.

## Goal

Close the three coupled r1 acceptance gaps without redesigning the accepted V2.1 architecture:

1. actual form enum values must be concise human-readable outcomes, not opaque hashes;
2. the current outcome must be issue-local, not the entire candidate translation;
3. deterministic constraints must validate a safely reconstructed full candidate after a local outcome replacement, not compare the full source against an isolated replacement string.

## Allowed files

- `src/council_of_translation/localization/models.py` only if a minimal bounded field/provenance addition is necessary
- `src/council_of_translation/localization/clustering.py`
- `src/council_of_translation/localization/deliberation.py`
- `src/council_of_translation/localization/orchestration.py`
- focused files under `tests/unit/**` and `tests/integration/**`
- `README.md`, `AGENTS.md`, `docs/v0.4-architecture.md`, `docs/v0.4-tool-contract.md` only for corrected behavior wording
- `harness/reports/CAMPAIGN-002-r2-worker.md`

## Forbidden scope

- Other production modules, dependencies, version/build/schema identifiers, public tools or arguments, defaults, budgets, storage locations, reviewer roles, sampling parsing, discussion policy, Position Matrix weights, reconsideration ranking/cap, compact response shape, or custom UI
- Majority voting, new MCP tools/resources/widgets, provider-specific branches, automatic file editing, budget expansion, or unrestricted model reasoning
- Reworking accepted persistence/privacy, coverage, chief-output, or degradation behavior beyond required regression preservation
- Any external mutation or live provider requirement

## Required correction design

### Issue-local current outcome

- Derive the displayed current outcome from non-empty normalized `candidate_span` anchors belonging to the cluster, not from `task.candidate_translation` wholesale.
- When all usable anchors resolve to one materially identical local value, that value is the current outcome and appears first.
- When anchors are empty, contradictory, overlong, or otherwise ambiguous, do not invent a current outcome. Two independently proposed valid outcomes may still form a DecisionPoint; fewer than two valid distinct outcomes must not.
- A single-span task where `candidate_span == task.candidate_translation` remains supported.
- Long documents must not expose, truncate, or discard the whole candidate merely because it exceeds the outcome bound.

### Safe full-candidate reconstruction

- Validate each local outcome by applying it to the complete candidate translation at the cluster's unambiguous candidate anchor, then running deterministic preflight/hard constraints against the complete reconstructed candidate.
- The current outcome validates the unchanged complete candidate.
- A replacement is unambiguous only when the implementation can prove the intended anchor occurrence. Do not silently replace every occurrence or guess among repeated occurrences.
- If safe reconstruction is impossible, mark/drop that option conservatively with explicit bounded provenance such as an ambiguous or missing anchor reason; do not crash and do not falsely claim a deterministic constraint failure.
- Unrelated placeholders, numbers, tags, URLs, DNT literals, or Markdown elsewhere in the document must not invalidate a safe local replacement.
- A replacement that actually removes or changes a protected token inside its affected span remains invalid.
- Policy-Gate-valid options and user authority remain unchanged after reconstruction.

### Human-readable standard form values

- The literal values in the emitted Pydantic/FastMCP JSON Schema `enum` must themselves be concise human-readable choices. A generic standard client must not need to interpret a prose mapping from `choice_<hash>` or `delegate_<hash>` tokens.
- Valid examples are bounded values such as `保留：继续`, `改为：下一步`, and `暂不决定，由 Council 裁决`; exact copy may be refined while staying outcome-first and readable.
- Keep a server-side per-field mapping from the readable submitted value to the exact stable internal `option_id` and `outcome_value`.
- Do not expose stable internal option IDs or hash-like surrogate IDs as user-facing enum values, titles, labels, or descriptions.
- Resolve truncation/collision deterministically with readable disambiguation, not opaque hashes. Reject unknown, stale, mismatched, and duplicated keys safely.
- The same readable value may legitimately appear in different decision fields; validation must be per field and must not reject two independent fields merely because their submitted strings are equal.
- Council delegation remains last, explicit, and distinct from decline/cancel/unsupported/malformed/error.
- Preserve at most three fields and at most four choices per field, label/description bounds, one batched form, and one normal submit action.

## Acceptance criteria

1. The exact `Continue` / `继续` / `下一步` form schema has readable enum values; no enum/title/description contains a stable `option_...`, `choice_<hex>`, or `delegate_<hex>` token.
2. Submitted readable values round-trip to exact internal option IDs/outcomes; current, alternative, and delegation paths work.
3. Unknown/stale/malformed field/value responses remain conservative. Equal readable values in two different valid fields are accepted independently.
4. A candidate document longer than 500 characters with local `candidate_span="继续"` produces local options `继续` and `下一步`; it never displays the entire document and does not lose the current option because of document length.
5. For source `Welcome {name}\nContinue`, candidate `欢迎 {name}\n继续`, and local proposal `下一步`, both local outcomes remain valid because the reconstructed full candidates preserve `{name}`.
6. For source `Continue {count}`, candidate/local span `继续 {count}`, and proposal `下一步`, the proposal remains invalid because the affected replacement removes `{count}`.
7. Repeated or ambiguous candidate anchors never trigger an arbitrary replacement. The result is explicit and conservative, with no exception or silent all-occurrence mutation.
8. Empty/contradictory/overlong candidate spans cannot invent a current outcome. DecisionPoint eligibility still requires two distinct valid outcomes.
9. Duplicate/synonymous proposal collapse, materially distinct separation, affirmations, one-role influence, Policy Gate, user decisiveness, fallback, reconsideration, degradation, compact output, V1/V2.0/V2.1 persistence/privacy, malformed coverage, continuation, review-only behavior, and exact five tools remain green.
10. Package/module version remains `0.5.0`, schema remains `2.1`, diagnostic build remains `outcome-first-decision-v3`, defaults remain unchanged, and budgets remain 6/10/14.
11. Authoritative docs describe readable enum values and conservative local reconstruction accurately; they do not claim live Goose validation.
12. Complete suite, focused counterexamples, syntax, fresh sdist/wheel build, built-wheel smoke, protected hashes, and baseline-to-final diff all pass.

## Required verification

Run and report exact commands, exits, counts, and outputs:

```powershell
python -m compileall src tests
```

```powershell
.venv\Scripts\python.exe -m pytest -q --basetemp .tmp\campaign002-r2-pytest -p no:cacheprovider
```

Run a named focused suite that directly covers every r2 criterion. Also print the exact Pydantic schema and FastMCP `get_elicitation_schema(...)` output for the reference form, plus the exact long-document, unrelated-placeholder, affected-placeholder, and ambiguous-anchor outcomes.

Build fresh artifacts because production code changes:

```powershell
$env:UV_CACHE_DIR='.tmp\campaign002-r2-uv-cache'; uv build --out-dir .tmp\campaign002-r2-dist
```

Smoke the fresh wheel in an isolated repository-local environment and assert 0.5.0/module/build/schema/five tools. Finally run:

```powershell
git diff --check 5687208aaeaaf3e6b00c192fb42596fb9b6cbf47..HEAD
git diff --name-status 5687208aaeaaf3e6b00c192fb42596fb9b6cbf47..HEAD
git status --short
```

Inspect the complete correction diff, recheck every protected hash, and confirm the index and committed implementation scope are clean. Live Goose/provider calls remain optional and are not required for `READY_FOR_REVIEW`; disclose exact count.

## Required evidence

- Admission/final full SHAs, commit(s), changed files, exact test/build commands and counts.
- Before/after outputs for all three r1 counterexamples and the repeated-anchor conservative case.
- Criterion-to-test/evidence mapping.
- Explicit statement that preserved r1 package behavior remains green.
- Protected hashes, index/worktree state, authority escalation count, subagent count zero, external mutation count, and live-call count.

## Stop conditions

- Admission baseline/protected state differs.
- A fix needs a new public field/tool, custom UI, provider-specific code, dependency, budget change, or frozen design revision.
- Safe issue-local reconstruction cannot be made deterministic with existing anchors.
- Readable enum values cannot be expressed through the current standard FastMCP/Pydantic form without changing the protocol design.
- Required full test/build/wheel evidence cannot be established after safe in-scope alternatives.

Stop and report the exact design/authority decision needed; do not weaken criteria or silently fall back to opaque values.

## Handoff

Write `harness/reports/CAMPAIGN-002-r2-worker.md`. In chat start with `READY_FOR_REVIEW` or `BLOCKED`, then summarize baseline/final SHAs, commits/files, verification, the exact corrected schema values, protected state, skips, counts, and remaining risk. Stop without push or acceptance claim.
