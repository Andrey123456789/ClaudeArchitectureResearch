# 003 — Pre-generation foundation

| | |
|---|---|
| Status | Draft for human review |
| Policy IDs | 180 |
| Metrics | 54 |
| Templates changed | **None** |
| Project specification | **None**; TaskBoard intentionally deferred |

## Policy oracle

`research/policy/inventory.json` is the single normative oracle. It stores every policy once inside human-navigation `policygroups`; the group boundaries have no candidate-architecture semantics.

The retired `content-pool/` and `skill-content-map.json` are intentionally absent.

The inventory is created before candidate generation and used post-generation to test:

- missing owner;
- duplicate owner;
- semantic drift;
- unapproved extra normative policy.

A second audit pass added material normative content that had previously remained only inside V2 skills/references, including DI, caching, HttpClient/resilience, configuration/logging, API versioning, Swagger/health, Docker/solution layout, Git/build-fix/CI/security-scan behavior.

## Metrics

`research/metrics/metrics-manifest.json` is the canonical standard for run-result JSON.

Changes in this revision include:

- P0-P4 criticality restricted to Quality/validity rather than Speed/Autonomy/Cost;
- measurement scope on every metric;
- complete descriptions for Quality metrics;
- exhaustive question taxonomy;
- separate correction-free vs fully-unattended autonomy outcomes;
- benchmark isolation validity metrics;
- semantic-drift and extra-policy metrics;
- symmetrical `replacement_change_surface` for all candidates;
- module-external blast radius only where a real module boundary exists;
- evidence completeness now handles skipped/not-applicable/unavailable checks explicitly;
- descriptive total-token sum demoted from a primary outcome.

## Benchmark isolation

`research/benchmark/isolation-protocol.md` defines three separate information surfaces:

1. **candidate construction** — may see candidate design, V2, inventory, shared invariants;
2. **benchmark execution** — sees only one frozen runtime candidate + frozen project/spec/task inputs;
3. **evaluation** — may see metrics, inventory, hidden oracle, candidate metadata and run evidence.

Research isolation is physical/allowlist-based, not an instruction asking Claude to ignore reachable files.

## Capability model

`research/capabilities/capability-framework.md` continues to define a generic replaceable-capability mechanism with four representative first-experiment slots.

## E0

`research/e0/README.md` remains **NOT EXECUTED** and defines the minimum mechanics probes required before physical template generation.

## Remaining gate before iteration 004

1. Human-review the revised inventory and metrics manifest.
2. Execute the minimal E0 probes on the exact Claude Code version intended for generation/benchmark.
3. Resolve E0 failures consistently across candidate designs.
4. Freeze/tag this foundation.
5. Generate M/L0/L1/K0/K1 in an isolated construction workspace from candidate design + V2 + inventory, while hiding metrics and future benchmark inputs.
6. Validate generated candidates against the inventory before freezing them.

TaskBoard remains outside the templates and will later be injected as the same frozen benchmark input for every candidate.
