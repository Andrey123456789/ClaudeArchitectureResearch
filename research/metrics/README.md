# Metrics

`metrics-manifest.json` is the canonical, versioned definition of experiment metrics and the run-result contract.

## Four global dimensions

1. **Speed** — elapsed execution time.
2. **Autonomy** — questions/interactions and corrective supervision.
3. **Cost** — raw token/resource usage and provider-reported monetary cost.
4. **Quality** — correctness, research validity, architecture/instruction reliability, maintainability and flexibility.

## First pass and recovery

A benchmark run preserves immutable per-attempt records:

- attempt `0` = initial/first-pass execution;
- attempts `1..N` = standardized corrective attempts.

`QLT-037` records first-pass success. `QLT-006` records final-after-recovery success.

All corrective work remains included in run-level time and cost. Recovery is also exposed separately through `SPD-003`, `CST-009`, and `AUT-009`.

The frozen human/operator burden score is:

```text
AUT-010 =
    AUT-001 user_questions_total * 1
  + AUT-009 corrective_prompt_count * 10
```

This point score is **not** wall-clock speed. Actual elapsed time, raw usage, monetary cost, and question classification remain separate evidence.

The older `AUT-005` 1/2/3/5 intervention-severity score is supporting diagnostic information only.

## Criticality vs evaluation stage

These are independent:

- `criticality` applies to **Quality and research-validity** metrics and describes consequence of failure;
- `evaluation_stage` controls when a check is run.

Speed, Autonomy and Cost do not become Quality blockers solely for being slow, interactive, or expensive.

## Measurement scope

Each metric declares where it is measured: benchmark preflight, benchmark run, candidate validation, static candidate analysis, trigger probe, findability probe, instruction-maintenance scenario, or replacement scenario.

## Evidence

Every computed metric requires evidence. Every skipped/not-applicable/technically-unavailable check also requires evidence for its disposition.

LLM review may interpret evidence but is never primary ground truth.

## Benchmark blindness

Benchmark-execution Claude must not see this manifest. See `research/benchmark/isolation-protocol.md`.
