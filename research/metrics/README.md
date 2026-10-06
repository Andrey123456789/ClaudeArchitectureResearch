# Metrics

`metrics-manifest.json` is the canonical, versioned definition of the experiment's metrics and result-report contract.

## Four global dimensions

1. **Speed** — finish minus start.
2. **Autonomy** — how often Claude asks the human and how much corrective supervision is required.
3. **Cost** — raw token categories and provider-reported monetary cost.
4. **Quality** — correctness plus architecture/instruction-system reliability, maintainability and flexibility.

## Manifest vs run-result JSON

The manifest is frozen before benchmark runs. Each run result records its version/SHA and may embed a copy of `metricsdictionary` to remain self-documenting.

The result JSON keeps the agreed rich structure: values, calculation, status, evidence, evaluation trace, skipped checks and final review.

## Criticality vs evaluation stage

These are independent:

- `criticality` = consequence if the metric is bad;
- `evaluation_stage` = when the check is run to avoid wasting time.

## Evidence

Every metric value requires evidence. Quotes are capped at 200 characters and point to a concrete artifact/locator. Human-coded events also require evidence.

LLM review may interpret results, but is never primary ground truth.
