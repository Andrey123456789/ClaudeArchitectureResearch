# Metrics

`metrics-manifest.json` is the canonical, versioned definition of experiment metrics and the run-result contract.

## Four global dimensions

1. **Speed** — elapsed execution time.
2. **Autonomy** — questions/interactions and corrective supervision.
3. **Cost** — raw token/resource usage and provider-reported monetary cost.
4. **Quality** — correctness, research validity, architecture/instruction reliability, maintainability and flexibility.

## Criticality vs evaluation stage

These are independent:

- `criticality` applies to **Quality and research-validity** metrics and describes consequence of failure;
- `evaluation_stage` controls when a check is run to avoid wasting evaluation time.

Speed, Autonomy and Cost use priority/direction/targets but do not become Quality blockers solely for being slow, interactive, or expensive.

## Measurement scope

Each metric declares where it is measured: benchmark preflight, benchmark run, candidate validation, static candidate analysis, trigger probe, findability probe, instruction-maintenance scenario, or replacement scenario.

This prevents static/template metrics from being confused with per-task benchmark metrics.

## Manifest vs run-result JSON

The manifest is frozen before benchmark runs. Each run result records its version/SHA and may embed `metricsdictionary` for self-documentation.

The result JSON keeps the agreed rich structure: metric values, calculation, status, evidence, evaluation trace, skipped checks, raw artifacts, and final review.

## Evidence

Every computed metric requires evidence. Every skipped/not-applicable/technically-unavailable check also requires evidence for its disposition.

Evidence quotes are capped at 200 characters and point to a concrete artifact/locator. LLM review may interpret evidence but is never primary ground truth.

## Benchmark blindness

Benchmark-execution Claude must not see this manifest. See `research/benchmark/isolation-protocol.md`.
