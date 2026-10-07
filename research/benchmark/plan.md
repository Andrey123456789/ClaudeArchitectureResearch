# Benchmark Plan

## Status

**Protocol accepted at Iteration 003 close.**

This file freezes the benchmark shape before E0 results and before candidate generation.
Exact task wording, starting fixtures, response scripts, and hidden Scenario Oracles are still to be authored and frozen in a dedicated pre-candidate iteration. Candidate-construction Claude must not see those hidden benchmark materials.

## Experimental subjects

The benchmark compares:

- V2 — frozen historical baseline;
- M — Minimal Modular;
- L0 — Stability-first + Embedded;
- L1 — Stability-first + Replaceable;
- K0 — Kinds × Scopes + Embedded;
- K1 — Kinds × Scopes + Replaceable.

The same task text, starting state, model, effort, autonomy/permission mode, Claude Code version, and benchmark harness are used for every candidate in a scenario.

## Scenario independence

T02–T06 do **not** continue from a candidate's T01 output.

Each scenario starts from its own frozen canonical starting state so that a mistake in an earlier scenario does not contaminate later comparisons.

T01 is the only greenfield scenario.

## Primary benchmark — T01 to T05

### T01 — Greenfield TaskBoard

Create the TaskBoard application from a frozen project specification using a goal-oriented prompt rather than a step-by-step implementation script.

Primary purpose:

- whole-template usefulness;
- instruction discovery/loading;
- architecture and project-structure discipline;
- autonomy and cost on a realistic greenfield task.

### T02 — Cross-layer feature

Add task tags and filtering by tags to the canonical TaskBoard.

The frozen scenario is expected to exercise, where applicable:

- persistence/schema evolution;
- Application/use-case code;
- API contract and HTTP behavior;
- Angular UI/data-access behavior;
- maintained tests.

Primary purpose: ordinary multi-layer feature work without a reason to change the project architecture.

### T03 — Business-rule change

Add a frozen board/task lifecycle rule whose correct implementation requires meaningful business/use-case logic but **does not justify introducing a Rich Domain Model, CQRS, MediatR, VSA, or another consequential architecture change**.

The exact rule and observable behavior will be frozen with its Scenario Oracle before candidate generation.

Primary purpose:

- correct placement of business/use-case rules;
- resistance to unnecessary architectural escalation;
- preservation of the project's simple-domain default.

### T04 — Decision/ambiguity gate

Use a task containing a deliberate material product/architecture decision that the frozen policy says must be escalated to the user rather than silently chosen.

The exact task and a standardized response script will be frozen before candidate generation.

Primary purpose:

- whether Claude asks when it genuinely should;
- whether it proceeds autonomously on everything that does not require escalation;
- decision-control correctness.

### T05 — Technology replacement

Replace NUnit with xUnit in the frozen canonical TaskBoard while preserving behavior and test coverage.

Primary purpose:

- replacement change surface;
- stale references;
- replaceability-axis comparison L0↔L1 and K0↔K1;
- cost, time, questions, and correctness of a realistic technology substitution.

## Primary checkpoint

After T01–T05:

1. compute and preserve the primary benchmark results;
2. freeze the resulting aggregate/report artifact with hashes of the metrics manifest, candidates, scenarios, and raw runs;
3. record conclusions/trade-offs **before** T06 is run.

T06 must not retroactively redefine the primary metric interpretation or primary benchmark ranking.

## Secondary stress benchmark — T06

### T06 — Partial-delete / atomicity bug

T06 is intentionally run **after** the primary checkpoint because diagnosis and repair paths are less predictable.

The frozen TaskBoard fixture contains a deterministic deletion defect with this user-visible symptom:

1. the user deletes a task;
2. the UI reports an error;
3. after refresh, the task is nevertheless gone.

The underlying fixture deliberately performs deletion in the wrong persistence order / transaction boundary so part of the operation is committed before a later dependent cleanup fails. The initial implementation does not restore atomicity after the later failure.

The benchmark prompt describes the observable symptom, not the diagnosis. It must not mention orphan cleanup, transaction boundaries, SaveChanges ordering, or the intended fix.

Precondition checks must prove before every run that:

- the task and relevant dependent state exist;
- the delete request reproduces the expected failure;
- the task has nevertheless disappeared after the failed request;
- unrelated baseline behavior is still healthy.

Because reproducing this defect intentionally performs a partial commit, the destructive precondition check **must not run against the benchmark instance that Claude will receive**.

For every T06 run:

1. create a disposable clone/database from the frozen T06 starting fixture;
2. execute the precondition/negative-control oracle against that disposable state;
3. require the expected defect to reproduce;
4. destroy/reset the disposable state;
5. create a new pristine benchmark workspace/database from the same frozen fixture/hash;
6. verify its non-destructive identity/hash checks;
7. only then launch benchmark-execution Claude.

A precondition run that mutates the actual Claude-visible starting state invalidates the benchmark run.

Postcondition checks must verify at least:

- normal deletion succeeds;
- dependent state is cleaned consistently;
- no unintended orphan/inconsistent state remains;
- a failure during the delete operation leaves the aggregate/persistence state consistent rather than partially committed;
- API/UI behavior reflects the actual outcome;
- unrelated CRUD behavior remains intact;
- architecture/static checks still pass.

T06 is reported as a **secondary stress result**, not folded silently into the previously frozen primary checkpoint.

## First-pass and recovery results

Every scenario records two logically separate outcomes:

1. **first-pass result** — state when Claude first declares/finishes the task;
2. **final-after-recovery result** — state after standardized corrective prompts, if needed.

A candidate that succeeds immediately must remain distinguishable from one that reaches the same final state only after correction.

All recovery work remains part of measured cost and time.

## Human/operator penalty

The currently frozen derived penalty is:

```text
operator_penalty_points =
    user_questions_total * 1
  + corrective_prompt_count * 10
```

Interpretation:

- every explicit question after the initial task prompt = **1 point**;
- every additional corrective prompt after a failed verification = **10 points**.

This score does **not** replace wall-clock time, token usage, or question counts. It is a separate derived human/operator-burden measure and is represented by `AUT-010` in metrics-manifest v1.2.

Question classification is still preserved separately:

- legitimate Reserved/material decision;
- necessary clarification;
- invalid/unnecessary question.

A legitimate question still costs one operator point because it still consumes human attention.

The hard maximum number of corrective rounds, if any, must be frozen with the detailed scenario protocol before candidate generation.

## Corrective prompts

Corrective prompts must be standardized and minimally diagnostic.

They may report:

- which frozen verification/check failed;
- concrete evidence/locator required to reproduce the failure.

They must not reveal the intended implementation or prescribe the fix.

Example shape:

```text
Verification failed.

<check-id>: <observable failure/evidence>.

Correct the implementation so the requested behavior and all applicable
project instructions pass verification. Do not change unrelated behavior.
```

All correction tokens, tool calls, elapsed time, questions, and verification work are included in the run evidence/cost.

## Scenario Oracle

Every task has a hidden, frozen **Scenario Oracle** prepared before candidate generation by an oracle-building process that does not see M/L/K candidate implementations.

The benchmark-execution Claude must not see the hidden oracle.

The oracle may contain:

1. black-box / end-to-end tests for user-observable behavior;
2. API/integration acceptance tests for edge cases, HTTP/persistence semantics, and data consistency;
3. architecture/static checks for boundaries and forbidden structural/pattern changes;
4. build/test commands required for the scenario;
5. scenario preconditions proving the starting fixture is in the intended state;
6. standardized response script for expected user questions.

The evaluator executes the same oracle against every candidate result.

A test generated by the Claude instance under benchmark is **not** accepted as the hidden ground-truth oracle merely because it passes.

## Oracle construction and freeze

Before candidate generation:

1. freeze exact T01–T06 task text;
2. freeze every canonical starting state;
3. use an independent oracle-builder Claude/session to propose end-to-end/integration/static checks from the specification and scenario only;
4. human-review the generated oracle for correctness, completeness, architecture neutrality, and absence of candidate-specific assumptions;
5. prove negative controls where applicable (for example T06 must fail its defect oracle before repair);
6. freeze oracle files and hashes;
7. keep all oracle/evaluation files outside candidate-construction and benchmark-execution contexts.

## Repetitions

Main comparison defaults remain defined by the metrics manifest:

- 3 repetitions per candidate/scenario initially;
- 5 for noisy/disputed comparisons where justified.

Before the main series, run small pilot executions solely to validate harness/evidence collection. Pilot results are not used as primary comparative evidence.

## Interpretation

Primary causal comparisons remain:

- L0 ↔ K0 — decomposition with embedded technologies;
- L1 ↔ K1 — decomposition with replaceable capabilities;
- L0 ↔ L1 — replaceability within Stability-first;
- K0 ↔ K1 — replaceability within Kinds × Scopes;
- M ↔ L/K — value/cost of formal metaarchitecture.

V2 remains the historical baseline. V2-vs-experimental differences may include both organization and normalized-policy/enforcement improvements, so V2 alone is not a clean causal comparison of decomposition strategy.
