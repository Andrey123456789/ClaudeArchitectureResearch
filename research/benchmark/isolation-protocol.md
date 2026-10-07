# Benchmark Isolation Protocol

## Status

Draft for human review. This protocol is a **research-validity requirement**.

## Principle

The model under test must not be able to inspect evaluation criteria, hidden oracles, competing candidates, historical baselines, or prior results that could change its behavior.

Isolation is enforced by **workspace contents and reachability**, not by asking Claude to ignore files that remain accessible.

## Phase A — Candidate template construction

Claude constructing a candidate may see:

- the assigned candidate `DESIGN.md` / `CORE_FEATURES.md`;
- shared candidate invariants/design material required to interpret that design;
- the frozen V2 source template;
- `research/policy/inventory.json`;
- `research/capabilities/capability-framework.md` for L1/K1;
- the construction prompt.

Candidate-construction Claude must **not** see:

- `research/metrics/**`;
- benchmark scenarios or TaskBoard specification;
- hidden acceptance tests/oracles;
- benchmark scoring rules;
- prior benchmark results/transcripts;
- candidate rankings or aggregate comparisons.

Run candidate construction in a temporary allowlisted workspace rather than exposing the whole research repository.

## Phase B — Benchmark execution

The benchmark Claude may see only:

- exactly one frozen runtime candidate template;
- the frozen project specification;
- the frozen starting project/code state;
- the benchmark task prompt;
- normal project/runtime files required for the task.

It must not be able to access:

- `research/**`;
- `prompts/**`;
- prior `results/**`;
- `inventory.json`;
- `metrics-manifest.json`;
- V2 or V3;
- any other candidate;
- candidate `DESIGN.md` / `CORE_FEATURES.md`;
- hidden acceptance criteria/oracles;
- evaluation scripts that reveal expected implementation;
- prior transcripts, metrics, verdicts, rankings, or aggregate results;
- the candidate label M/L0/L1/K0/K1 when it can reasonably be omitted.

Prefer a neutral path such as `run-017`, not `K1-run-017`.

Do not clone the full research repository and merely ask Claude not to inspect it. Prefer building the run workspace from an explicit allowlist. If Git is needed for diff capture, initialize a fresh local repository in the isolated workspace or use a fixture repository with no research history/remotes.

## Phase C — Evaluation

The evaluator may see:

- frozen metrics manifest;
- policy inventory;
- candidate design metadata;
- candidate-validation output;
- hidden acceptance tests/oracles;
- transcript/tool events;
- start/final states and diff;
- build/test/check logs;
- human annotations;
- result JSON and aggregate data.

Evaluation material must never be copied back into the model-visible benchmark workspace.

## Pre-run isolation gate

Before Claude starts a benchmark run, the harness must:

1. enumerate the model-visible workspace;
2. verify the allowlisted root/file structure;
3. scan for forbidden paths, names, and research markers;
4. verify Git remotes/history cannot expose the research repository when Git is present;
5. record candidate-runtime and fixture hashes;
6. store the isolation report outside the model-visible workspace;
7. start Claude only if the isolation gate passes.

A failed gate invalidates the run before model execution.

## Minimum forbidden patterns

The exact versioned list belongs to the harness and supports explicit false-positive exceptions, but it must cover at least:

```text
research/
prompts/
results/
inventory.json
metrics-manifest.json
CORE_FEATURES.md
DESIGN.md
templates/v2-baseline/
templates/v3/
templates/candidates/
benchmark-oracle*
hidden-acceptance*
```

## Leakage discovered later

If forbidden research/evaluation material becomes reachable during execution, record it and invalidate the run. Do not reinterpret leakage as a normal candidate failure.

The absence of evidence that Claude opened a forbidden file is not sufficient. The primary control is that the forbidden material was physically absent or unreachable.

## Evidence to preserve

Outside the model-visible workspace, preserve:

- workspace file manifest;
- forbidden-pattern scan output;
- Git remote/history exposure check;
- allowed-input hashes;
- isolation-protocol version/hash;
- start timestamp;
- PASS/FAIL result.

These artifacts support `QLT-031` and `QLT-032`.
