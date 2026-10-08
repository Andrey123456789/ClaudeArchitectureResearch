Iteration 003 was not executed as a Claude Code session. Its artifacts were prepared through human-directed research work with ChatGPT assistance, reviewed by the researcher, and committed manually. `prompts/003-pre-generation-foundation.md` documents the intended scope of the iteration but is not an executed-prompt record.

# 003 — Pre-generation foundation

| | |
|---|---|
| Status | **COMPLETE / FROZEN** |
| Closed | 2026-10-07 |
| Policy IDs | 180 |
| Metrics | 59 |
| Templates changed | **None** |
| Concrete benchmark implementation | Deferred; protocol shape frozen |
| Project specification | TaskBoard intentionally not injected into candidates |

## Frozen outputs

Iteration 003 established the pre-generation research foundation:

- `research/policy/inventory.json` — single normative oracle, frozen before candidate generation;
- `research/metrics/metrics-manifest.json` — versioned metric/evidence contract;
- `research/benchmark/isolation-protocol.md` — construction/execution/evaluation information boundaries;
- `research/benchmark/plan.md` — accepted benchmark shape, recovery policy, T01–T06 scenario plan, primary checkpoint, and hidden Scenario Oracle rules;
- `research/capabilities/capability-framework.md` — accepted generic replaceable-capability definition with a limited first-experiment fixture;
- `research/e0/README.md` — mechanics-validation protocol to be executed in Iteration 004.

`content-pool/` and `skill-content-map.json` remain intentionally absent. `inventory.json` is the only committed normative-policy oracle.

## Benchmark decisions frozen at close

- every candidate receives byte-for-byte identical task text for a scenario;
- scenarios use identical frozen starting states and execution configuration;
- T02–T06 are independent fixtures rather than a chain built on each candidate's previous output;
- T01–T05 form the primary benchmark;
- primary results are checkpointed before T06;
- T06 is a secondary bug-fix stress test using the deterministic partial-delete/atomicity defect;
- first-pass and final-after-recovery results are both preserved;
- questions cost 1 operator-penalty point;
- corrective prompts cost 10 operator-penalty points;
- recovery time/tokens/tool usage remain fully counted separately;
- hidden Scenario Oracles are generated/reviewed/frozen before candidate generation and are never shown to benchmark-execution Claude.

Exact scenario wording, fixtures, response scripts, and oracle tests still require a dedicated freeze step before candidate generation. Their absence does not reopen the Iteration 003 methodology.

## Next gate

Iteration 004 performs E0 mechanics validation on the exact Claude Code environment intended for candidate generation and benchmarking.

After E0, the next pre-candidate step is to freeze detailed benchmark scenarios and hidden oracles. Candidate generation begins only after both mechanics assumptions and benchmark inputs are fixed.

## Final pre-candidate protocol amendment — 2026-10-07

After the initial Iteration 003 freeze, but **before any M/L/K candidate generation or benchmark result existed**, the protocol was amended once to make the already-approved recovery procedure measurable.

`metrics-manifest.json` advanced from v1.1 to **v1.2** and now records:

- `AUT-009` corrective prompt count;
- `AUT-010` operator penalty points (`questions × 1 + corrective prompts × 10`);
- `SPD-003` recovery duration;
- `CST-009` recovery token volume;
- `QLT-037` first-pass task success;
- immutable per-attempt result records so first-pass and final-after-recovery outcomes cannot overwrite one another.

The legacy 1/2/3/5 intervention-severity score remains only as supporting diagnostic information.

The T06 protocol was also clarified so its destructive defect-precondition check runs on a disposable clone/database and the actual Claude-visible benchmark begins from a new pristine copy of the same frozen fixture.

This amendment is pre-registered before candidate construction; it is not outcome-driven and does not use candidate or benchmark results.
