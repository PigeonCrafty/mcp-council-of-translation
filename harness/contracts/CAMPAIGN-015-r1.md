# Campaign Contract: CAMPAIGN-015-r1 — V0.13.2 Terminal Truthfulness Closure

## Control

- Harness role: `MAIN WORKER`
- Harness mode: `STRICT_CAMPAIGN`
- Campaign: `CAMPAIGN-015-r1`
- Campaign class: `closure_only`
- State: `ASSIGNED`
- Repository: `C:\Users\GeZhu\MyMCP\mcp-council-of-translation`
- Local implementation baseline HEAD: `c7d788ca37ecb5d6bd3f1ebec01d48d5c7d52fb4`
- Protected-main audit reference: `dde2761469f5b5f6f8fd841ed4230ba4efe2827b`
- Admitted local `origin/main`: `dde2761469f5b5f6f8fd841ed4230ba4efe2827b`
- Product target: `0.13.2`
- Diagnostic build target: `truthful-boundaries-council-v11.2`
- Review/receipt/evaluator Schema targets: `2.6` / `1.1` / `2.1`
- Acceptance authority: Foreman only
- Execution ledger: `harness/reports/CAMPAIGN-015-r1-ledger.md`
- Worker report: `harness/reports/CAMPAIGN-015-r1-worker.md`
- Commit policy: exactly three green, scoped commits, one for each package PKG-088
  through PKG-090; never commit a known failing state
- Subagents: forbidden; this correction is tightly coupled and must retain one Main
  Worker reasoning and evidence chain
- Parallel package implementation: forbidden; execute PKG-088, PKG-089 and PKG-090
  sequentially

This is a narrow engineering-closure Campaign, not a new product Feature Campaign. It
closes confirmed independent-audit defect `NEW-AUD-008`, corrects release provenance,
and produces a locally verifiable V0.13.2 candidate. It does not authorize acceptance,
protected-main integration, publication, tagging, GitHub Release creation, deployment,
Goose validation or a new roadmap.

## Closure outcome

Deliver a V0.13.2 candidate in which an unresolved Targeted Discussion evidence gap
cannot disappear merely because a later `continue_review()` resolves an unrelated,
valid DecisionPoint. The child review must preserve the unresolved terminal-safety
boundary while also preserving and applying the user's valid unrelated choice.

The Campaign must also make the public audit trail distinguish local Campaign history,
protected-main publication history and black-box execution provenance, then perform the
patch-version release migration without changing any public tool, default, budget,
concurrency, routing or schema contract.

## Admission

Start only if all of the following are true:

1. `HEAD` is exactly the local implementation baseline and the local `origin/main` ref
   is exactly the admitted protected-main reference. Do not fetch, pull, checkout,
   merge, rebase, reset or otherwise normalize the intentionally divergent lineage.
2. Git index is empty, verified through the exit code of
   `git diff --cached --quiet`.
3. The only tracked dirty files are the three Foreman-owned Harness state files below.
   Their hashes must match and they are protected: do not modify, restore, stage or
   commit them.
4. Existing untracked Foreman, user, audit, report and review assets are admitted.
   Preserve them exactly. Do not convert their untracked status into authority to stage
   them, except for the two release-document paths explicitly authorized under PKG-090.
5. Compile succeeds and the complete baseline suite is exactly `576 passed` with zero
   failures and zero skips. Use a unique repository-local basetemp.
6. Every starting-file and protected hash below matches exactly.
7. The SHA-256 of this contract matches the launch prompt.

### Starting-file hashes

| Path | SHA-256 |
| --- | --- |
| `AGENTS.md` | `F3878FDF4B43DA8CD0C96349A192C6C6EEE564034A63157ABC06FA10F71DE306` |
| `README.md` | `409C08CE38C3A65A7D57DA2AEFF79FF53EF45678F8613C5B62D862BCCFCFC960` |
| `docs/v0.4-architecture.md` | `9A83AE3EEE5124CFA28A173BDC5C10A8F8F22CDEC8442CECCB73262CB2E675F7` |
| `docs/v0.4-tool-contract.md` | `49664CC290A5CE66E1C3A80CBE2B6624217C9C62AF8D5D3F24B1837B163D2828` |
| `docs/v0.13.1-stage-closure-report.md` | `A0D24F7F97914DE23AA5FA1B9BE37C01932EEAC9A8EE88BF8DB1BF75E0299200` |
| `pyproject.toml` | `29F7096257F0D34886B370793FAD208AF8A437BA32B3124410C1CC1486E525A0` |
| `src/council_of_translation/__init__.py` | `F098F514E41F0827D0D353D4EF8BDB67F3C11E08F65521F4F1B8A00E0C32D884` |
| `src/council_of_translation/localization/orchestration.py` | `BB704F234266FDEF5FDB9802111740D659E46AE7045F6A1856227C6BD1C9B9FF` |
| `tests/integration/test_v10_release_contract.py` | `7AB5C1D804DC170BF5C0C06B86B5B9D7695DC307FAE5FC21D6D1229DB82D233B` |
| `tests/integration/test_tool_surface_v2.py` | `DCB9AED4B4A47B9EAEFE6C72D0452411C03405832B6FED7B77BF8B978D146EB4` |
| `tests/unit/test_persistence_v2.py` | `F4BCE874023480465DFB664242055873CFDB9560FAAE14841407116A2BFF652C` |
| `uv.lock` | `E7E4E44A19A3A7F1813EE3B5CFDC5814A70BF29C71CD5115582AF4E64A352E00` |

### Protected hashes

| Path | SHA-256 |
| --- | --- |
| `harness/features.json` | `8609E687FB39A5A2A35010B895693B112820E10E0BB04A0A9F43D1584D2D78B5` |
| `harness/plan.md` | `4FFAFA49089E40CFED207C23E1993BCFF4A7A340BFC6D0BE7807CF1D999FC60C` |
| `harness/progress.md` | `8076CEE9046059E97E623AFA3F3E34068A3C81BC840CD57470E485D0F90E1E58` |
| `harness/evaluations/V0.13.1-INDEPENDENT-REVIEW-FOREMAN-RESPONSE.md` | `9324F28706A45D7539405564D934CD827A65A20BE025F380239049686E93847B` |
| `mcp-council-of-translation-v0.13.1-independent-review.md` | `9187F14F198B12B328BB6B23D63245871E0E8D1CED3B98E63B018D525920AE10` |
| `mcp-council-of-translation-v0.13-independent-audit.md` | `0B608DF956448C92AC4112452709129FB45B27478C0F571118660DAA89FBA179` |
| `mcp-council-of-translation-audit-and-upgrade-recommendations.md` | `B48073E063C4C9F34E0B6B4DAE94E80079EAAAD3B2F8E273DD60B2F25F6ABD76` |
| `.github/workflows/ci.yml` | `0B37598E7D53D27B04E5524BAA4D46A2AB69D5E2607A5FF9F0437512CF8EF645` |
| `docs/v0.13-stage-development-report.md` | `DA03138EB0E07F27C1FFEF1F1BA044DB13D590427BC7F8EA3CB53D26168C6C94` |
| `harness/evaluations/CAMPAIGN-014-q016-r4-review.md` | `65A417D62BECB418BE84D49FF62403DC6D0E60443E0E36433C32083766EBEFF6` |
| `harness/reports/CAMPAIGN-014-q016-r4-worker.md` | `9EAA63BF034663FEE0A5A01ECA3C20355B298194EE76F1386348D64C3A0A734C` |
| `harness/reports/CAMPAIGN-014-q016-r4-ledger.md` | `FE0EA8C0B496EB1A00CFB5B191F2ADFD9249CBA46EA5608221BB78C31DFF9B7A` |

Do not read, traverse, copy, hash, modify, delete or stage `.learnings/**`,
`reviews/**` or `myTest/**`. Do not inspect protected raw review-record directories.
Stop before edits on any admission mismatch.

## Confirmed defect and frozen semantics

The independent adversarial reproduction is accepted as the red baseline:

```text
Issue A:
major cross-role disagreement
-> Targeted Discussion malformed/unavailable
-> Parent fails closed

Issue B:
independent valid non-material DecisionPoint
-> continue_review resolves only Issue B
```

The observed defective child incorrectly clears Issue A's unresolved evidence gap and
becomes permissive. The frozen fix is:

> An evidence gap may clear only when new evidence of equivalent or higher authority
> actually fills that same gap. An unrelated continuation cannot clear unresolved
> historical degradation.

Apply the following exact boundaries:

1. Derive the inherited Targeted Discussion gap from canonical structured parent state,
   using exact reason/warning code equality for `discussion_unavailable`. A semicolon-
   delimited fallback-reason list may be parsed into exact codes. Do not use substring
   matching, localized display prose, report scraping or free-form model text.
2. `continue_review()` does not rerun Targeted Discussion. Therefore, when the parent has
   an unresolved canonical `discussion_unavailable` gap, the child must retain that gap
   unless this continuation actually produces structured evidence that resolves the
   same gap. This Campaign does not add such a resolution path, so the adversarial child
   remains fail-closed.
3. Before final decision-support classification, terminal disposition, compact response,
   trace rendering and persistence, the child must coherently retain:

   ```text
   warnings contains discussion_unavailable
   fallback_reason contains discussion_unavailable
   degraded == true
   decision_support.level == insufficient
   status == NEEDS_HUMAN_REVIEW
   chief_editor_decision.publishability == 需人工复核
   chief_editor_decision.review_needed == 是
   ```

4. Do not cancel, roll back or ignore the valid user choice for Issue B. The child must
   simultaneously retain its selected valid outcome, apply the corresponding bounded
   reconsideration successfully, and record `valid_user_choice` in DecisionTrace.
5. Preserve parent/child immutability and linkage. The stored parent must not be mutated;
   the child must retain the correct parent review identity and its own complete trace.
6. The gap must agree across the full structured record, normal compact response, phase
   trace, primary display report and verification receipt. A record may not be degraded
   while its receipt claims a complete, non-degraded, empty-fallback outcome; the phase
   trace may not claim successful discussion when discussion was unavailable.
7. Negative control: a clean parent without `discussion_unavailable` must not acquire
   that code, degradation or a stricter disposition merely because it is continued.
8. Do not introduce unconditional inheritance of all warnings, all degradation or all
   fallback codes. Preserve current behavior for genuinely resolved, unrelated or clean
   conditions.
9. Do not introduce a generic `persistent_evidence_gaps` framework, new persistence
   field, new public enum or schema migration. If implementation proves a second
   structurally distinct sticky-gap class is necessary, stop and request a revised
   contract rather than generalizing.

## Frozen public and release boundaries

- Public tools remain exactly five:
  `review_translation`, `continue_review`, `view_review_record`,
  `list_review_records`, `get_server_info`.
- Preserve review-only behavior, defaults, Policy Gate, caller/user authority,
  deterministic hard-rule authority, history privacy, receipt purity and all existing
  routing profiles.
- Sampling budgets remain `6/13/18`; concurrency limit/max remain `3/3`, accepting only
  configured values `1`, `2` or `3` with the existing visible fallback behavior.
- ReviewRecord Schema remains `2.6`; verification receipt Schema remains `1.1`;
  evaluator Schema remains `2.1`.
- Version becomes `0.13.2`; diagnostic build becomes
  `truthful-boundaries-council-v11.2` everywhere the current release contract requires.
- No tool parameter, response contract, display-report section, routing profile, role,
  sample budget, model call, elicitation, retry or persistence write may be added.
- `uv.lock` may change only for the editable root version `0.13.1 -> 0.13.2`.
  Preserve lock revision/package/upload-time invariants `3/78/586` and the complete
  dependency graph.

## Exact production/test/document allowlist

Only the following paths may be created or modified by the Worker:

1. `src/council_of_translation/localization/orchestration.py`
2. `tests/integration/test_v132_continuation_evidence_gap.py` (new)
3. `tests/integration/test_v10_release_contract.py`
4. `tests/integration/test_tool_surface_v2.py`
5. `tests/unit/test_persistence_v2.py`
6. `AGENTS.md`
7. `README.md`
8. `docs/v0.4-architecture.md`
9. `docs/v0.4-tool-contract.md`
10. `docs/v0.13.1-stage-closure-report.md`
11. `docs/v0.13.2-terminal-truthfulness-closure.md` (new)
12. `pyproject.toml`
13. `src/council_of_translation/__init__.py`
14. `uv.lock`

Authorized Worker-only evidence and temporary paths are:

- `harness/reports/CAMPAIGN-015-r1-ledger.md` (new; leave untracked/unstaged)
- `harness/reports/CAMPAIGN-015-r1-worker.md` (new; leave untracked/unstaged)
- `.tmp/campaign015-r1-worker/**` (bounded verification only; remove before handoff)

No other source, test, fixture, documentation, workflow, dependency, Harness, user or
external path may change. If an omitted path is required, stop with `BLOCKED` and name
it. Do not weaken, delete, skip, deselect or xfail an existing test to fit this contract.

## Sequential package work

### PKG-088 — Red-to-green terminal-safety correction

1. Before changing production code, create the new adversarial integration regression
   using the actual orchestration and continuation path. Do not synthesize the pass by
   manually mutating a persisted ReviewRecord or by bypassing production finalization.
2. Construct both Issue A and Issue B exactly as frozen above. Make Targeted Discussion
   malformed/unavailable through the existing bounded test seam. Require the parent to
   be `NEEDS_HUMAN_REVIEW`, degraded, carry `discussion_unavailable`, require human
   review and have `decision_support.level == insufficient`.
3. Continue exactly once and resolve only Issue B through a valid user option. Capture
   the current red behavior before production edits; the focused regression must fail
   because the child improperly clears the unrelated discussion gap. Record the command,
   failure and assertion in the ledger. Do not commit the red state.
4. Implement the smallest correction in `orchestration.py` consistent with the frozen
   semantics. Do not add a general gap framework or refactor unrelated orchestration.
5. Require the child to retain Issue A's fail-closed terminal fields while retaining
   Issue B's selected outcome, completed targeted reconsideration and
   `valid_user_choice` trace provenance.
6. Run the new test and the affected continuation/discussion/decision-support selection.
   Commit only after green with subject:
   `PKG-088 preserve continuation discussion evidence`.

### PKG-089 — Cross-channel coherence and negative controls

1. Extend the new integration test only; do not change production code in this package.
2. Prove parent immutability and parent/child linkage.
3. Prove exact `discussion_unavailable` and fail-closed disposition coherence across:
   full record, compact response, phase trace, primary display report and canonical
   verification receipt, including receipt/text equality and terminal-disposition
   coherence.
4. Prove the verification receipt remains complete and non-redacted for the canonical
   code, while faithfully reporting degraded execution and the retained fallback.
5. Add a clean-parent continuation negative control. It must preserve normal successful
   continuation behavior and must not invent `discussion_unavailable`, degradation or a
   human-review disposition.
6. Prove the correction adds no sampling, elicitation, retry or persistence mutation
   beyond the existing continuation behavior.
7. Run the expanded focus and affected matrix. Commit only after green with subject:
   `PKG-089 verify continuation terminal coherence`.

### PKG-090 — Provenance correction and V0.13.2 release migration

1. Correct `docs/v0.13.1-stage-closure-report.md` so provenance roles are explicit and
   not collapsed. At minimum distinguish:

   | Role | SHA |
   | --- | --- |
   | local Campaign implementation accepted HEAD | `9d23ed01f94be2ef0c724b3e0a3e7e1beba75c09` |
   | protected-main squash publication and black-box execution provenance | `9d8f1f987efe73946377883e6ad3a681abe11989` |
   | Q-016 accepted documentation HEAD | `c7d788ca37ecb5d6bd3f1ebec01d48d5c7d52fb4` |
   | Q-016 evidence publication SHA | `292fa8b4d41310ed029d6fbd947dab5e3e92f1dc` |
   | Q-016 final closure SHA | `6f12db065fa42d422dd2ebeb1ff99be26fc95dd2` |
   | stage-report publication SHA | `dde2761469f5b5f6f8fd841ed4230ba4efe2827b` |

   Do not describe `9d23ed01...` as the final protected-main runtime publication SHA.
2. Add `docs/v0.13.2-terminal-truthfulness-closure.md` documenting the confirmed defect,
   bounded fix, no-schema-bump decision, verification scope, known support boundary and
   post-release Feature Freeze/observation handoff. Do not claim acceptance, CI,
   publication, release, tag or production validation before those events occur.
3. Migrate package/module/docs/release tests to `0.13.2` and
   `truthful-boundaries-council-v11.2`. Keep Schemas `2.6/1.1/2.1` and every frozen
   public invariant.
4. Refresh `uv.lock` using pinned `uv 0.12.3`. Require only the editable root version
   delta and exact invariants `3/78/586`.
5. Run release, affected, Golden and complete regressions, build and installed-wheel
   verification below. Commit only after all local source/test checks are green with
   subject: `PKG-090 release V0.13.2 terminal truthfulness closure`.

## Required verification

Use `.venv\Scripts\python.exe` for repository checks where available and pinned
`uv 0.12.3` for lock/build/environment operations. Use unique repository-local
basetemps and caches to avoid the known Windows host-temp permission boundary. Record
every failed command and bounded rerun; never hide a failure.

### Focused and affected tests

Run, at minimum:

- `tests/integration/test_v132_continuation_evidence_gap.py`;
- continuation/reconsideration/discussion coverage from
  `tests/integration/test_orchestration_v2.py`,
  `tests/integration/test_v21_reconsideration.py`,
  `tests/integration/test_v131_discussion_coherence.py` and
  `tests/integration/test_r4_reviewer_coverage.py`;
- decision-support/input-completeness coverage from
  `tests/integration/test_v26_decision_support.py`,
  `tests/integration/test_v131_input_completeness.py` and
  `tests/unit/test_decision_support.py`;
- verification/persistence coverage from
  `tests/integration/test_v12_verification_view.py`,
  `tests/unit/test_verification_receipt.py` and
  `tests/unit/test_persistence_v2.py`;
- release/tool-surface coverage from
  `tests/integration/test_v10_release_contract.py` and
  `tests/integration/test_tool_surface_v2.py`.

All selected tests must pass with zero skips, deselections or xfails. Report exact test
counts for PKG-088, PKG-089, the integrated affected matrix and release matrix.

### Golden, complete regression and static checks

1. Run `python -m compileall src tests` at admission and final state.
2. Run the Golden evaluator and require Schema `2.1`, exact `30/30`, all inherited
   accuracy metrics `1.0` and false-reassurance metric `0.0`.
3. Run the complete suite and require all tests pass, zero skips. The final count must be
   greater than the admitted `576`; do not freeze an invented final count in advance.
4. Run `git diff --check` for each package and for baseline-to-final.
5. Run the established dead-import/static scan over changed Python files and report its
   exact result. Do not suppress findings.
6. Verify exact five tools, review-only behavior, defaults, 15 routing profiles,
   budgets `6/13/18`, concurrency `3/3`, version/build targets and Schemas
   `2.6/1.1/2.1`.
7. Verify baseline-to-final scope is a subset of exactly the 14 authorized paths and
   that the Git index is empty at handoff.

### Fresh artifacts and installed-wheel smokes

1. Build a fresh wheel and sdist into the bounded Worker temporary directory. Inspect
   both archives for package contents/version and absence of unintended repository,
   Harness, audit, review, learning or user assets. Record filename, byte size and
   SHA-256 for each artifact.
2. Create two fresh isolated CPython 3.12.9 environments. Install the built wheel with
   exact FastMCP `2.13.0.2` in one and exact FastMCP `3.4.7` in the other.
3. Each smoke must import from isolated `site-packages`, call all five public tools, and
   verify version/build/Schemas/defaults/budgets/concurrency.
4. Each installed-wheel smoke must also exercise the adversarial parent/continuation
   terminal-safety scenario and its clean-parent negative control without a live model,
   provider or Goose call. Require the same full/compact/trace/receipt coherence as the
   repository regression.
5. Treat either FastMCP point failure as a blocker. Record warnings such as known
   upstream deprecations without hiding them.

## Required Worker evidence

The ledger and report must include:

- contract SHA-256, all admission commands/results and the exact 576-test baseline;
- red regression command and failure before production edits, then exact green result;
- proof Issue A remains fail-closed after Issue B's valid choice, plus proof the choice,
  selected outcome, reconsideration and `valid_user_choice` trace remain effective;
- full/compact/phase/report/receipt coherence and clean-parent negative control;
- parent immutability, child linkage and sampling/elicitation/retry/save-count evidence;
- exact three commits, subjects and changed paths per package;
- focused, affected, release, Golden and complete-regression counts;
- version/build/schema/tool/default/routing/budget/concurrency invariants;
- exact provenance wording correction and no premature publication claims;
- `uv.lock` command, byte/hash delta and `3/78/586` invariants;
- wheel/sdist names, sizes, SHA-256, archive inspection and both installed-wheel smokes;
- compile, diff, static/dead-import and exact scope audits;
- reconciliation of every protected hash, index state and bounded temp cleanup;
- subagent count, authority escalations, dependency/build operations, live/provider/model/
  Goose calls, remote Git/GitHub operations and every skipped required check;
- remaining risks without claiming Foreman acceptance, protected-main CI, release or
  engineering completion.

## Authority and stop conditions

Authorized: read-only repository inspection; local source/test/doc/metadata edits inside
the exact allowlist; local tests; pinned dependency sync; lock refresh; builds; isolated
wheel environments; boundary-checked cleanup limited to
`.tmp/campaign015-r1-worker/**`; and exactly three scoped local Git stage/commit cycles.
Inspect exact staged names and staged diff before every commit. Local Git operations stay
inside the sandbox.

Not authorized: fetch, pull, push, remote Git/GitHub HTTPS, PR, merge, protected-main
integration, tag, GitHub Release, publication, deployment, Goose/provider/model calls,
credentials/config changes, workflow edits, schema changes, Feature Campaign work or
release acceptance. Native Windows remote Git operations are unnecessary and prohibited
in this Worker Campaign.

Stop with `BLOCKED` if any of the following occurs:

- admission HEAD/ref/index/test/hash mismatch;
- a path outside the exact allowlist is required;
- the fix requires a second structurally distinct sticky-gap class, generic gap
  framework, schema migration or public-contract change;
- the valid unrelated DecisionPoint cannot remain effective while fail-closed terminal
  truthfulness is restored;
- any channel or receipt contradicts the structured terminal state;
- clean-parent behavior becomes sticky or stricter without cause;
- an existing assertion must be weakened, skipped, deselected or xfailed;
- lock drift exceeds the exact editable-root version change;
- Golden, complete regression, archive inspection or either installed-wheel smoke fails;
- protected assets change, the index cannot be left empty, or safe bounded cleanup
  cannot be completed.

## Handoff

Leave both Worker evidence files untracked/unstaged and the Git index empty. In chat,
start with exactly `READY_FOR_REVIEW` or `BLOCKED`. Report contract hash, baseline and
final HEAD, all three commits, exact scope, red-to-green evidence, terminal and user-
choice preservation, cross-channel coherence, negative control, test/Golden/static
results, version/build/schemas, lock, artifacts, both installed-wheel smokes, protected
hashes, cleanup, subagent/authority/dependency/build/live/remote counts, skipped checks
and remaining risk. The Worker must not claim Campaign acceptance, V0.13.2 publication,
tagging, CI confirmation, Q-017 issuance or `ENGINEERING FEATURE COMPLETE`.
