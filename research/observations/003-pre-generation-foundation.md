# 003 — Pre-generation foundation

| | |
|---|---|
| Status | Draft for human review |
| Date | 2026-10-05 |
| Policy IDs | 132 |
| Metrics | 46 |
| Templates changed | **None** |
| Project specification | **None**; TaskBoard intentionally deferred |

## Produced artifacts

### Policy foundation
`research/policy/inventory.json` assigns stable IDs to normalized policy semantics with source traceability to the frozen V2 baseline. The same policies are grouped under `research/policy/content-pool/` for review.

`research/policy/skill-content-map.json` separates normative policy from shared workflow/knowledge material so candidate generators do not independently rewrite the same content.

This is a first-pass normalization, not a claim that every V2 sentence is perfectly classified. Human review should focus on omissions, over-strengthening/weakening, duplicate semantics, and policies that should be split/merged.

### Metrics
`research/metrics/metrics-manifest.json` is the future canonical standard for run-result JSON. A run result still embeds `metricsdictionary` for self-documentation, but the manifest is versioned and canonical.

### Capability model
`research/capabilities/capability-framework.md` separates the generic capability concept from the four-slot experimental fixture.

### E0
`research/e0/README.md` records the minimal probes required before physical template generation. E0 is intentionally marked **NOT EXECUTED**.

## Remaining gate before iteration 004

1. Human-review policy inventory/content pool and metrics manifest.
2. Execute minimal E0 probes on the exact Claude Code version intended for generation/benchmark.
3. Resolve any E0 failure consistently across candidate designs.
4. Freeze/tag the reviewed foundation.
5. Generate M/L0/L1/K0/K1 from the shared content pool, not by independently reconstructing V2.

TaskBoard remains outside the templates and will later be injected as the same frozen benchmark input for every candidate.
