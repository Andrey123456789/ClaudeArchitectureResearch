# 004 — E0 Claude Code mechanics validation

## Goal

Empirically validate, on this machine and the exact Claude Code environment intended for the research, the mechanics that our candidate instruction architectures and benchmark harness rely on.

This is an experiment about **Claude Code behavior**, not a request to redesign the M/L/K candidates or to make every probe pass.

## Context to read

Start with:

- `research/e0/README.md`
- `research/requirements.md`
- `research/observations/002-candidate-space-analysis.md`
- the candidate `DESIGN.md` / `CORE_FEATURES.md` files only as needed to understand which physical mechanics they depend on
- `research/benchmark/isolation-protocol.md`

Do not use TaskBoard or any future benchmark scenario as an E0 fixture.

## Required outcome

Create a minimal reproducible E0 fixture/harness and execute the probes defined in `research/e0/README.md`:

- E0-R1
- E0-R2
- E0-S1
- E0-S2
- E0-A1
- E0-I1
- E0-T1
- E0-W1

Use unique harmless markers, positive/negative controls where meaningful, and fresh Claude Code sessions/processes where technically possible.

For every probe preserve enough raw evidence that a human can independently verify the result. Do not treat Claude's own assertion that something loaded as proof when an observable behavior/file/output check is possible.

For E0-W1 use only a harmless generated outside-root canary. Do not inspect unrelated files.

For E0-T1 distinguish direct telemetry from derived values and record technical unavailability rather than guessing.

## Execution constraint

If this Claude Code session cannot safely/reliably launch the fresh child sessions needed for a probe, do not fake the result and do not weaken the probe.

Instead:

1. create the complete reproducible fixture/harness and exact commands;
2. mark that probe `NOT_EXECUTED` / `INCONCLUSIVE`;
3. tell the user exactly which top-level command/session must be run next;
4. continue executing any other probes that can be validated correctly.

## Research integrity

Do not modify:

- `templates/v2-baseline/`
- `templates/v3/`
- `research/policy/inventory.json`
- `research/metrics/metrics-manifest.json`
- `research/benchmark/plan.md`
- candidate `DESIGN.md` or `CORE_FEATURES.md`

A failed mechanic is valuable evidence. Do not rewrite candidate definitions merely to obtain a PASS.

If a mechanic fails or behaves differently from our assumption, document:

- what was observed;
- which candidates/design assumptions it affects;
- the smallest consistent adaptation options;
- what should be decided before candidate generation.

Do not implement those candidate-design changes in this iteration unless the user explicitly approves them after seeing the result.

## Deliverables

At minimum:

1. reproducible probe fixtures/harness;
2. raw result/evidence artifacts for every executed probe;
3. a machine-readable summary containing environment metadata and PASS/FAIL/LIMITED/INCONCLUSIVE status for each probe;
4. `research/observations/004-e0-mechanics-validation.md` explaining findings, limitations, affected candidate assumptions, and the gate to the next iteration;
5. update `research/e0/README.md` only as necessary to point to the executed result and reflect actual status.

Do not commit or push unless explicitly requested.

## Completion rule

Do not report Iteration 004 complete merely because the fixture was created.

Report it complete only when every required mechanic is either empirically characterized in the intended environment or explicitly blocked with a reproducible next step and no candidate generation is relying on an unknown assumption.
