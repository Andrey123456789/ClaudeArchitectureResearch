# Iteration 003 revised patch

Direct GitHub write was attempted again but the connector returned HTTP 403 (`Resource not accessible by integration`), so this archive contains complete replacement/new files.

## Replace

- `research/policy/inventory.json`
- `research/policy/README.md`
- `research/metrics/metrics-manifest.json`
- `research/metrics/README.md`
- `prompts/003-pre-generation-foundation.md`
- `research/observations/003-pre-generation-foundation.md`

## Add

- `research/benchmark/isolation-protocol.md`

## Intentionally absent/deleted

- `research/policy/content-pool/`
- `research/policy/skill-content-map.json`

## Validation summary

- Policy groups: 10
- Policy IDs: 180
- Metric definitions: 54
- Duplicate policy IDs: 0
- Duplicate metric IDs: 0
- Missing metric descriptions: 0
- Benchmark-isolation validity metrics: QLT-031 / QLT-032
- Candidate semantic-parity metrics: QLT-033 / QLT-034
- Replacement metrics: QLT-035 (all candidates), QLT-036 (real module-boundary candidates)
