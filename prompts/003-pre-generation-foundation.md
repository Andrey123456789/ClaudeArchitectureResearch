# 003 — Pre-generation foundation

## Goal

Freeze the experimental protocol required before generating M/L0/L1/K0/K1 runtime templates.

## Deliverables

1. A V2-derived normative `inventory.json` with stable IDs and human-navigation policy groups.
2. A versioned `metrics-manifest.json` defining Speed, Autonomy, Cost and Quality; evidence rules; validity gates; criticality; evaluation order; and measurement scopes.
3. A benchmark-isolation protocol that keeps construction inputs separate from evaluation inputs and physically blinds benchmark-execution Claude from research artifacts.
4. Clarification that replaceable capabilities are a generic mechanism while the first experiment implements only four representative slots.
5. Minimal E0 mechanics probe plan for Claude Code behaviors that affect physical template layout.
6. Observation file recording the remaining gate before template generation.

## Constraints

- Do not modify `templates/v2-baseline/` or `templates/v3/`.
- Do not generate M/L0/L1/K0/K1 runtime templates yet.
- Do not introduce a concrete project specification such as TaskBoard.
- Candidate architectures may move/split/neutralize shared content, but may not independently strengthen or weaken it.
- Do not create a second committed copy of inventory policy text.
- Candidate-construction Claude may use V2 + inventory, but must not see metrics or future benchmark tasks/oracles.
- Benchmark-execution Claude later sees only one frozen runtime candidate + frozen project/task inputs and no research artifacts.
- Mark newly produced foundation material as draft for human review.
