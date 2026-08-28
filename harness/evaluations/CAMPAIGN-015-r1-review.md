# Campaign Foreman Review: CAMPAIGN-015-r1

## Control

- Role: `FOREMAN`
- Mode: `STRICT_CAMPAIGN`
- Decision: `ACCEPTED`
- Contract: `harness/contracts/CAMPAIGN-015-r1.md`
- Contract SHA-256: `98B1AC4DBC7E8F2E7356293E9754BAACA12AF99E6B53145FDA16EEB196A6AE53`
- Campaign Worker report: `harness/reports/CAMPAIGN-015-r1-worker.md`
- Worker report SHA-256: `41EDA2F59CA8DA683F4F22C5E297744936862CA069FB983913FD40344944BD68`
- Execution ledger: `harness/reports/CAMPAIGN-015-r1-ledger.md`
- Ledger SHA-256: `F20048D55B97318A75375871A2A76363FB5888F94C2E2A7C8F19A058E67B6E81`
- Reviewed baseline: `c7d788ca37ecb5d6bd3f1ebec01d48d5c7d52fb4`
- Accepted final HEAD: `c0f0d190ff5b5bc753f9dc743ce3a5743fe32bdf`
- Admitted and unchanged local `origin/main` ref:
  `dde2761469f5b5f6f8fd841ed4230ba4efe2827b`
- Review date: `2026-08-28 Asia/Shanghai`

## Scope and repository review

- Complete baseline-to-final diff inspected: yes; exactly 14 authorized paths,
  581 insertions and 29 deletions. Set comparison against the contract allowlist returned
  zero missing or extra paths.
- Global boundary and non-goal compliance: PASS. The production correction is confined
  to 19 changed lines in `orchestration.py`; no generic persistent-gap architecture,
  schema, tool, role, route, provider, prompt or workflow change was introduced.
- User changes preserved: PASS. The only tracked dirty files remain the three protected
  Foreman Harness state files. Existing user/Foreman untracked assets were not staged.
- Commit/worktree policy compliance: PASS. Exactly three ordered green commits exist;
  the red regression was recorded but not committed; Git index is empty.
- Required Worker capability and delegation-policy compliance: PASS. Subagents were
  forbidden and none were used.
- External/destructive action compliance: PASS. No remote Git/GitHub, push, PR, tag,
  release, publication, deployment, Goose, provider or model operation occurred.
- Resume/retry and side-effect safety: PASS. Admission basetemp, invariant-probe,
  archive-inspection and smoke-probe failures were disclosed with bounded corrections;
  no product side effect was repeated.
- Sensitive evidence hygiene: PASS. No protected raw record, learning, review or user
  fixture tree was added to product commits or built archives.

## Task graph review

| Package | Boundary/dependency review | Worker evidence | Foreman verification | Result |
| --- | --- | --- | --- | --- |
| PKG-088 | Exact canonical `discussion_unavailable` inheritance only; valid unrelated choice remains effective | Red child was `COMPLETED`; green child retains fail-closed state; 73 affected tests | Inspected full production/test diff; fresh adversarial regression included in 246-test matrix | PASS |
| PKG-089 | Test-only coherence and clean-parent controls after PKG-088 | 2 focused and 228 expanded tests; parent bytes unchanged; two saves; no elicitation/retry | Read every assertion for full, compact, phase, report, receipt, linkage, user choice and clean parent | PASS |
| PKG-090 | Provenance correction plus patch release; no schema or dependency-graph change | 38 release, 246 integrated, 30/30 Golden, 578 full; dual installed-wheel smoke | Independently inspected release/docs/lock diff, rebuilt archives, checked metadata and ran both installed tool-surface smokes | PASS |

## Campaign acceptance review

| Criterion | Worker evidence | Foreman verification | Result |
| --- | --- | --- | --- |
| Historical evidence gap remains fail-closed | Child retains warning/fallback, degraded, insufficient, `NEEDS_HUMAN_REVIEW`, `需人工复核 / 是` | Production order writes canonical state before `finalize_decision_support`; adversarial test passed | PASS |
| Unrelated valid user decision remains authoritative | Selected option/outcome, completed product-context reconsideration and `valid_user_choice` retained | Direct test assertions inspected and rerun | PASS |
| Cross-channel terminal truthfulness | Full/compact/phase/display/receipt agree; receipt complete and unredacted | Fresh 246-test matrix passed; receipt assertions inspect exact canonical object/text equality | PASS |
| No unconditional sticky fallback | Clean continuation remains non-degraded `COMPLETED` | Negative control inspected and rerun | PASS |
| Parent/child and operation purity | Parent object/file immutable, linked child, two saves, 7+1 samples, zero elicitations | Assertions inspected; no new production call site was added | PASS |
| V0.13.2 identifiers and frozen schemas | `0.13.2`, build v11.2, Schemas `2.6/1.1/2.1` | Fresh full suite and installed-wheel diagnostics passed | PASS |
| Frozen public invariants | Five tools, 15 routes, budgets `6/13/18`, concurrency `3/3`, review-only defaults | Release/tool-surface tests and two installed Client tool listings passed | PASS |
| Lock and dependency graph | Root version only; hash `8D6F...`; invariants `3/78/586` | Independent diff shows the single root-version line; counts reproduced | PASS |
| Provenance correction | Six distinct SHA roles; `9d23ed01...` no longer described as final protected-main runtime publication | Stage report inspected directly | PASS |
| Golden and complete regression | Schema 2.1 exact 30/30; all accuracy metrics 1.0; false reassurance 0.0; 578 passed | Fresh Golden 4/4 and complete 578/578 | PASS |
| Artifacts and supported FastMCP points | Worker wheel/sdist inspected; exact 2.13.0.2 and 3.4.7 smokes passed | Fresh build had 31/42 members, no forbidden assets; both installed environments imported from `site-packages`, exposed five tools and correct diagnostics | PASS |
| Repository hygiene and authority | Protected hashes exact, index empty, no remote/live calls | All 12 hashes independently reconciled; status/index inspected | PASS |

## Independent integration verification

| Command/workflow | Result | Evidence |
| --- | --- | --- |
| `python -m compileall -q src tests` | PASS | Foreman repository run |
| Frozen affected matrix | `246 passed in 2.37s` | Fresh `.tmp/campaign015-foreman-review/affected` basetemp |
| Golden corpus | `4 passed in 0.86s`; embedded assertions require Schema 2.1, 30/30, all accuracy metrics 1.0 and false reassurance 0.0 | Fresh Foreman Golden basetemp |
| Complete regression | `578 passed in 5.62s`, zero skips | Fresh Foreman full basetemp |
| `git diff --check` and exact allowlist comparison | PASS; zero path differences | Baseline-to-final diff |
| Pinned `uv 0.12.3` build | PASS | Fresh wheel 110425 bytes/31 members; sdist 103533 bytes/42 members |
| Archive privacy/scope scan | PASS | Zero Harness/review/learning/user/test/Git/temp members |
| FastMCP 2.13.0.2 installed smoke | PASS | CPython 3.12.9, isolated `site-packages`, five tools, correct diagnostics; known Authlib warning only |
| FastMCP 3.4.7 installed smoke | PASS | CPython 3.12.9, isolated `site-packages`, five tools, correct diagnostics |
| Protected hashes / index | 12/12 exact; index empty | Fresh Foreman reconciliation |

The Foreman build initially invoked host `uv 0.6.13`, which failed on its sandbox-external
user cache. It was replaced by the contract-required pinned `uv 0.12.3` with a
repository-local cache. Two temporary installed-smoke probes then used the wrong import
surface before tool execution (`server.get_server_info`, then decorated FunctionTool
direct call); the final probe used `_server_info` plus cross-version `Client.list_tools`
and passed on both exact FastMCP versions. These are disclosed Foreman evidence-harness
errors, not product failures. No product file was changed by the corrections.

Fresh archive SHA-256 values differ from the Worker's hashes because the build backend
embeds new archive timestamps; the wheel size and member count match, and independent
member, metadata and installed-import verification passed. Reproducible archive bytes
were not a frozen criterion.

## Delegation and integration audit

- Package/subagent/file/commit mapping reconciled: exact three commits; no subagents.
- Frozen interface and dependency compliance: PASS.
- Collision/conflict handling: sequential packages; no overlapping concurrent edits.
- Main Worker verification independently checked: PASS for risk-weighted and complete
  paths.
- Ledger/report/repository consistency: PASS. Report and ledger hashes are frozen above.

## Findings

No correctness, privacy, authority, scope or release-contract finding requiring a
revision was identified.

The known FastMCP 2.13.0.2 Authlib deprecation warning remains an upstream support note,
not a Council defect. Live provider/Goose behavior and protected-main CI were not
authorized in this local Campaign and remain separate release evidence.

## Preserved evidence

All PKG-088, PKG-089 and PKG-090 evidence is accepted. `NEW-AUD-008` is closed locally.

## Decision rationale

The implementation satisfies the frozen minimal-correction principle: it preserves only
the already-canonical unresolved discussion gap, keeps the unrelated valid user decision
effective, proves terminal coherence across every exposed channel, and does not invent a
general architecture or schema burden. Independent risk-weighted, Golden, full-regression,
archive and installed-wheel verification passed. The Campaign is therefore `ACCEPTED` at
final HEAD `c0f0d190ff5b5bc753f9dc743ce3a5743fe32bdf`.

This acceptance establishes a local V0.13.2 release candidate only. It does not yet
complete CLOSURE-004, publish protected main, confirm the six required CI contexts,
create tag `v0.13.2`, create a GitHub Release or establish production validation.

## User audit index

- Contract: `harness/contracts/CAMPAIGN-015-r1.md`
- Worker report and ledger: `harness/reports/CAMPAIGN-015-r1-worker.md`,
  `harness/reports/CAMPAIGN-015-r1-ledger.md`
- Baseline-to-final commits: `d2d49ab`, `16da96b`, `c0f0d19`
- Key regression: `tests/integration/test_v132_continuation_evidence_gap.py`
- Release note: `docs/v0.13.2-terminal-truthfulness-closure.md`
- Remaining gate: CLOSURE-004 protected-main publication, six-way CI, annotated tag,
  GitHub Release, artifacts/checksums and final Feature Freeze declaration.

## Next action

Archive the accepted Campaign evidence and publish the accepted V0.13.2 candidate
through protected main. Confirm all six required Windows/Linux Python 3.10/3.12/3.13
contexts, then create an annotated `v0.13.2` tag and GitHub Release with wheel/sdist
artifacts, SHA-256 checksums and known limitations. Only after CLOSURE-004 is independently
verified may the Foreman declare `ENGINEERING FEATURE COMPLETE` and enter Feature Freeze
plus real-project observation.
