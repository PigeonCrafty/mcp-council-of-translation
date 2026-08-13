# Live Gate Protocol Correction: CAMPAIGN-007 Q-011 r2

## Control

- Role: FOREMAN
- Gate: `Q-011` bounded-parallel Goose compatibility and latency evidence
- Corrects: `harness/contracts/CAMPAIGN-007-q011-live.md`
- Corrected protocol baseline SHA-256:
  `86E7D12BA3B14BE94CD8CBCF5E0B2572FC08BE2117721AFC4D6F5DC0F8040092`
- Published `main` under test: `641ef46b6fdde380463b40d39a654cf8eb1248c2`
- Package/build/schema: `0.9.0` / `bounded-parallel-council-v7` / `2.3`

## Bounded correction

The r1 live protocol used three descriptive aliases rather than the canonical V0.9
record literals. The source, persisted schema and pre-existing tests establish the
canonical values:

- `terminology_reviewer`, not `terminology_consistency_manager`;
- `brand_voice_reviewer`, not `brand_tone_gatekeeper`;
- `fluency_reviewer`, not `naturalness_polisher`;
- successful `independent_reviews[*].sample_status` is `structured_success`, not
  `success`.

The canonical six-role order is therefore:

1. `fidelity_reviewer`
2. `terminology_reviewer`
3. `product_context_reviewer`
4. `brand_voice_reviewer`
5. `risk_ambiguity_reviewer`
6. `fluency_reviewer`

This correction changes no input, provider/model rule, environment, run count,
telemetry threshold or product requirement. It does not authorize a rerun: the six
already returned review IDs are admissible because their inputs, version, build,
schema, concurrency arms and canonical record values can be verified directly.

All other criteria and decision rules in the r1 protocol remain binding. The Foreman
must evaluate only the six user-designated IDs and must exclude unrelated records in
the same persistence directory.
