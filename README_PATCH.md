# Patch: close Iteration 003 and start Iteration 004

## Replace

- `research/policy/inventory.json`
- `research/metrics/metrics-manifest.json`
- `research/benchmark/isolation-protocol.md`
- `research/capabilities/capability-framework.md`
- `research/observations/003-pre-generation-foundation.md`
- `research/e0/README.md`

## Add

- `research/benchmark/plan.md`
- `prompts/004-e0-mechanics-validation.md`

## Do not modify

- prompts 001/002/003
- V2/V3 templates
- candidate DESIGN/CORE_FEATURES files

## Result

Iteration 003 is formally frozen. Iteration 004 is ready to run as E0 mechanics validation.

Important sequencing after E0:

1. freeze exact T01–T06 prompt texts, starting fixtures, response scripts, and hidden Scenario Oracles;
2. only then generate M/L0/L1/K0/K1;
3. validate/freeze candidates;
4. run pilot/main benchmarks.
