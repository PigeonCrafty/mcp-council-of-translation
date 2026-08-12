# Campaign 003 Live Goose Presentation Review

## Control

- Role: FOREMAN
- Evidence source: normal Goose session against published V0.6 `main`
- Record: `20260812T113302675410Z_611c7d32146e`
- Package/build/schema observed: `0.6.0` / `guided-deliberation-v4` / `2.2`
- Decision: Q-008 `ACCEPTED`; Q-009 `CHANGES_REQUESTED`
- Raw record location is user-local and intentionally not copied into Git.

## Q-008 — source/target-only briefing

Accepted evidence:

- `briefing_mode=auto` requested one six-field form before the first reviewer sample.
- The accepted brief persisted six bounded values with explicit provenance and `full` context confidence.
- Content type normalized to `ui`; six reviewers then completed with full coverage.
- Sampling remained 6/13, no degradation or fallback occurred, and review-only remained intact.

The full record phase order is `briefing`, `preflight`, `planning`, then `independent_review`. The outer Goose test summary incorrectly described briefing as after preflight, so future usability acceptance must inspect the record rather than trust a paraphrased phase claim.

## Q-009 — process-first digest usability

Changes are required even though the server generated a complete process digest and `display_report`:

1. Goose's first response replaced the Council process with a ten-item diagnostic report because the MCP tool returned one large structured object and left presentation selection to the outer agent.
2. The process became visible only after an explicit second prompt requested `display_report`.
3. The visible report repeated six long affirmative paragraphs and evidence blocks, mixed English headings/internal role IDs with Chinese prose, and retained several empty/no-op sections.
4. Six independently successful affirmative reviews were rendered as `未形成需合并的实质共识项`, which is technically inherited from issue clustering but misleading to a user.
5. Technical phrases such as Policy Gate counts and `actor_action_object` displaced the practical professional insight.
6. The intended tone-goal and primary-focus values appeared reversed in the stored brief relative to the test instruction. Deterministic schema/value round-trip evidence is required before attributing this solely to user entry or Goose rendering.

## Product conclusion

The Council process exists and is retrievable, but the default presentation contract is not yet reliable or concise. V0.7 must make a compact human report the primary MCP text content, retain structured data separately, summarize positive consensus truthfully, compress role lenses without erasing distinct perspectives, hide empty sections and technical metadata, and preserve full evidence on demand.

## Remaining live acceptance

Q-009 may become accepted only after a normal user request—without a diagnostic checklist or second retrieval prompt—shows the concise Council process directly, with distinct role insights, truthful consensus, conditional detail and the final disposition last.
