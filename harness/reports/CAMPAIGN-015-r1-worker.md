READY_FOR_REVIEW

# CAMPAIGN-015-r1 Main Worker Report

## Identity and admission

- HARNESS_ROLE: WORKER / MAIN WORKER
- HARNESS_MODE: STRICT_CAMPAIGN
- Contract: `harness/contracts/CAMPAIGN-015-r1.md`
- Contract SHA-256: `98B1AC4DBC7E8F2E7356293E9754BAACA12AF99E6B53145FDA16EEB196A6AE53` (matched before edits and at final reconciliation)
- Required/observed baseline: `c7d788ca37ecb5d6bd3f1ebec01d48d5c7d52fb4`
- Admitted/unchanged local `origin/main`: `dde2761469f5b5f6f8fd841ed4230ba4efe2827b`
- Admission index: empty
- Admission tracked dirty set: exactly protected `harness/features.json`, `harness/plan.md`, `harness/progress.md`
- Admission starting-file and protected hashes: all matched
- Admission compile: PASS
- Admission regression: exactly `576 passed in 5.84s`, zero skips

The first admission pytest invocation used a nested `--basetemp` whose authorized parent did not yet exist and ended with `426 passed, 150 errors`. This was an environment/setup failure (`FileNotFoundError` for the basetemp), not a product result. After creating only `.tmp/campaign015-r1-worker`, a fresh-basetemp complete rerun produced the required exact 576 passes. Both commands are recorded in the ledger.

The forbidden trees `.learnings/**`, `reviews/**` and `myTest/**` were not read, traversed, copied, hashed, modified, deleted or staged.

## Commits and exact scope

Final HEAD: `c0f0d190ff5b5bc753f9dc743ce3a5743fe32bdf`.

1. `d2d49abec3e98bec167a7cad5f3cdd99daa3a4af` — `PKG-088 preserve continuation discussion evidence`
   - `src/council_of_translation/localization/orchestration.py`
   - `tests/integration/test_v132_continuation_evidence_gap.py`
2. `16da96bf620c15e9a2f976278cea6eb54117ed67` — `PKG-089 verify continuation terminal coherence`
   - `tests/integration/test_v132_continuation_evidence_gap.py`
3. `c0f0d190ff5b5bc753f9dc743ce3a5743fe32bdf` — `PKG-090 release V0.13.2 terminal truthfulness closure`
   - `AGENTS.md`
   - `README.md`
   - `docs/v0.13.1-stage-closure-report.md`
   - `docs/v0.13.2-terminal-truthfulness-closure.md`
   - `docs/v0.4-architecture.md`
   - `docs/v0.4-tool-contract.md`
   - `pyproject.toml`
   - `src/council_of_translation/__init__.py`
   - `tests/integration/test_tool_surface_v2.py`
   - `tests/integration/test_v10_release_contract.py`
   - `tests/unit/test_persistence_v2.py`
   - `uv.lock`

Baseline-to-final scope is exactly the contract's 14 authorized paths. Per-package staged-name, staged-diff and `git diff --check` inspections passed. No commit rewrites, squashes or amendments were used.

## PKG-088 red-to-green evidence

The new regression drives actual `run_structured_review` and `continue_structured_review` paths. Issue A is a major cross-role disagreement whose malformed discussion envelope produces canonical `discussion_unavailable`; Issue B is a separate valid non-material DecisionPoint.

- Red command: `.venv\Scripts\python.exe -m pytest -q tests\integration\test_v132_continuation_evidence_gap.py --basetemp .tmp\campaign015-r1-worker\pkg088-red`
- Red result: expected `1 failed in 0.35s`; the child returned defective `COMPLETED` instead of `NEEDS_HUMAN_REVIEW`.
- Green focused result: `1 passed in 0.26s`.
- PKG-088 affected matrix: `73 passed in 1.97s`, zero skips/deselections/xfails.

The bounded correction recognizes only exact `discussion_unavailable` warning equality or an exact semicolon-delimited fallback code. It does not scrape prose, use substring matching, inherit all degradation, create a generic gap framework or change Schema.

The corrected child simultaneously retains:

- `warnings == ["discussion_unavailable"]`
- `fallback_reason == "discussion_unavailable"`
- `degraded == true`
- `decision_support.level == "insufficient"`
- `status == "NEEDS_HUMAN_REVIEW"`
- chief disposition `需人工复核 / 是`

The unrelated valid user choice remains effective: selected option/outcome preserved, product-context reconsideration completed, and DecisionTrace reports `valid_user_choice` with the selected option.

## PKG-089 cross-channel and negative-control evidence

- Focus: `2 passed in 0.27s`.
- Expanded affected matrix: `228 passed in 2.23s`, zero skips/deselections/xfails.
- Parent object and persisted bytes remain unchanged; child has its own ID and correct `parent_review_id`.
- Full record, compact response, discussion phase (`degraded`), primary report, verification receipt and canonical receipt text agree on the fail-closed terminal state.
- Receipt is complete and non-redacted for the canonical fallback; its JSON exactly equals the text-channel copy and terminal disposition occurs exactly once as the last report line.
- Clean-parent continuation does not acquire `discussion_unavailable`, degradation or human review and remains `COMPLETED`.
- Adversarial and clean paths each preserve exactly 7 parent prompts + 1 continuation prompt, zero elicitation, no retry and exactly two saves (parent + child).

## PKG-090 release and provenance evidence

- Package/module version: `0.13.2`
- Diagnostic build: `truthful-boundaries-council-v11.2`
- Frozen Schemas: ReviewRecord `2.6`, receipt `1.1`, evaluator `2.1`
- Frozen surface/defaults: exactly 5 tools; review-only; 15 routes; budgets `6/13/18`; concurrency `3/3`; defaults unchanged
- Release matrix: `38 passed in 1.40s`
- Integrated affected matrix: `246 passed in 2.46s`

The historical stage report now distinguishes the six frozen provenance roles: local accepted implementation, protected-main squash/black-box provenance, accepted documentation HEAD, evidence publication, final closure and stage-report publication. It explicitly does not describe `9d23ed01...` as final protected-main runtime publication.

The V0.13.2 closure document records the defect, bounded correction, no-schema-bump decision, local verification scope, known specific support boundary and Feature Freeze/observation handoff. It makes no premature acceptance, CI, publication, tag, release, deployment or production-validation claim.

## Golden, complete regression and static checks

- Golden pytest: `4 passed in 1.16s`
- Golden production aggregate: Schema `2.1`; exact `30/30`; `failed_case_ids=[]`
- Inherited accuracy metrics, decision-support accuracy and support/disposition coherence: all `1.0`
- Insufficient false-reassurance rate: `0.0`
- Final pre-commit complete suite: `578 passed in 6.41s`
- Post-commit compile: PASS
- Post-commit complete suite: `578 passed in 5.91s`, zero skips; admitted count increased from 576 to 578
- Dead-import AST scan: zero unused imports across 6 changed Python files
- Runtime invariant probe: PASS for `5 tools / 15 routes / 6-13-18 budgets / 3-3 concurrency / 0.13.2 / v11.2 / Schemas 2.6-1.1-2.1 / frozen defaults`
- Baseline-to-final diff check: PASS

One temporary invariant probe initially imported a nonexistent constant name and was corrected to validate the evaluator's actual output. The failed command and rerun are in the ledger.

## Lock, artifacts and installed-wheel smokes

Pinned tool: exact `uv 0.12.3 (507230998 2026-08-07 x86_64-pc-windows-msvc)` with repository-local `UV_CACHE_DIR` and `UV_TOOL_DIR`.

- Canonical command: `uvx --from uv==0.12.3 uv lock --refresh`
- Result: 78 packages resolved; only editable root `0.13.1 -> 0.13.2`
- Lock before: 200959 bytes, SHA-256 `E7E4E44A19A3A7F1813EE3B5CFDC5814A70BF29C71CD5115582AF4E64A352E00`
- Lock after: 200959 bytes, SHA-256 `8D6F90F994B44E4785B31965F8A5CFA7AD40F3D55D9A43F53D0A993F79EE66EF`
- Lock invariants: revision/package/upload-times `3/78/586`; dependency graph unchanged

Fresh artifacts:

- `council_of_translation-0.13.2-py3-none-any.whl` — 110425 bytes — SHA-256 `4BB74C181EE516E7E12C1BA25369649ED5AF070E507940D64FCB78D8936AEC8E`
- `council_of_translation-0.13.2.tar.gz` — 103515 bytes — SHA-256 `28B77549974D410283D4CFA34380A7722547ED02B49A87FCCC79F82879CA881A`

Archive inspection passed: 31 wheel members and 42 sdist members; correct version, Python and FastMCP metadata; no Harness, audit, review, learning, user, test, Git or temp assets. The build's upstream warning that the repo-local uv cache was inside the source tree did not correspond to an included archive member. A first inspection-script assertion used the wrong `Requires-Python` ordering; the semantic metadata check was corrected and rerun successfully.

Two fresh CPython 3.12.9 environments installed the built wheel:

- FastMCP `2.13.0.2`: PASS from isolated `Lib/site-packages`; all five tools called; adversarial and clean full/compact/phase/report/receipt paths passed. The known upstream Authlib deprecation warning was observed.
- FastMCP `3.4.7`: PASS from isolated `Lib/site-packages`; all five tools called; adversarial and clean paths passed.

The first 3.4.7 smoke attempt failed because the temporary probe used the removed server-side `mcp.get_tools()` method. It was corrected to use cross-version client `list_tools()` and rerun on both supported FastMCP points; both passed.

## Repository hygiene and counts

- Protected hash reconciliation: all 12 exact contract hashes MATCH
- Tracked dirty set at final audit: exactly protected `harness/features.json`, `harness/plan.md`, `harness/progress.md`
- Worker report: `harness/reports/CAMPAIGN-015-r1-worker.md` (untracked/unstaged)
- Worker ledger: `harness/reports/CAMPAIGN-015-r1-ledger.md` (untracked/unstaged)
- Bounded Worker temp: safely removed and confirmed absent
- Git index: empty
- Required checks skipped: none
- Subagents: 0
- Successful local Git filesystem authority escalations: 6; authority expansion: 0
- Dependency/environment operations: 7; build invocations: 1
- Live Goose/provider/model calls: 0
- Remote Git/GitHub calls: 0
- Push/PR/tag/publication/release/deploy calls: 0

## Remaining risks and boundary

- Foreman acceptance, protected-main CI, publication and release remain outside Worker authority and are not claimed.
- No live model/provider/Goose validation was permitted; deterministic scripted and installed-wheel evidence does not prove open-distribution model quality.
- The correction is deliberately specific to canonical `discussion_unavailable`; a structurally distinct sticky evidence gap requires a new contract.
- FastMCP 2.13.0.2 retains the known upstream Authlib deprecation warning.

## Foreman launch prompt

```text
HARNESS_ROLE: FOREMAN
HARNESS_MODE: STRICT_CAMPAIGN

Independently review CAMPAIGN-015-r1 at final Worker HEAD
c0f0d190ff5b5bc753f9dc743ce3a5743fe32bdf.

Use harness/contracts/CAMPAIGN-015-r1.md as the frozen source of truth. Read the
untracked Worker report and ledger, inspect all three scoped commits, independently
rerun the required acceptance checks, reconcile protected hashes and decide acceptance.
Do not infer acceptance from READY_FOR_REVIEW and do not modify or stage the Worker
reports during independent review.
```
