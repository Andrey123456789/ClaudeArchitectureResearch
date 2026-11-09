---
paths:
  - "docs/decisions/**"
---

> Level: 0 Core · Owns: decision classes, Reserved decisions, Decision Requests, headless behavior · Scope: common · Loads: always (imported by CLAUDE.md)

# Decision Control

Classify every consequential choice before acting on it.

## Decision classes

- **Decided** — already settled: the accepted architecture (Level 1 architecture overview), the approved stack and project defaults (Level 3 project decisions), and the approved product sources. Follow it; **must not** reopen it without approval. When an approved technology exists for a need, use it rather than silently selecting an alternative.
- **Delegated** — local, reversible, and does not materially change a boundary, dependency, accepted convention, public contract or observable behavior. Routine internal implementation choices already constrained by the specification, the approved stack, existing code or these rules are Delegated: decide and proceed without asking.
- **Reserved** — **requires approval**: changes an accepted architecture, stack or public-behavior decision, or is materially expensive to reverse.

## Reserved decisions

Unless the approved product sources or the established project structure already require it, each of these **requires explicit approval**:

1. changing an already accepted project or architecture decision;
2. adopting a new architectural style or pattern — for example a Rich Domain Model or systematic DDD tactical patterns, CQRS, mediator-based organization, Vertical Slice Architecture, event sourcing, microservices;
3. adding a production project, layer or assembly, or changing the project reference graph;
4. changing persistence boundaries (for example multiple persistence contexts) or adopting a substantially different persistence technology;
5. adding an infrastructure category — messaging, background processing, distributed cache, search, external storage, external identity;
6. adding a major library or framework, or replacing an approved baseline technology;
7. introducing a project-wide convention or abstraction that other code is expected to follow — for example a project-wide Result/railway model;
8. changing the authentication or authorization architecture;
9. making a breaking public API change or adopting API versioning;
10. defining product behavior or tunable values that the product sources do not define (product governance).

## Unclear cases

Ask the five questions. Any **yes** makes the decision Reserved.

1. Does it add, remove or replace a dependency, framework or infrastructure capability?
2. Does it change a project, layer or reference boundary?
3. Does it establish a convention that other code is expected to follow?
4. Does it change observable behavior or a public contract?
5. Would it be expensive to reverse after other code depends on it?

## Decision Request

When a Reserved decision is needed, stop the affected part of the work and present:

- **Context** — what requires the decision and why now;
- **Options** — realistic alternatives with trade-offs;
- **Recommendation** — the preferred option and why;
- **Blocked** — what cannot proceed until the decision is made;
- **Proceeding with** — the policy-compliant work that continues meanwhile.

An explicit user instruction counts as approval; the accepted decision **must** be recorded where its class belongs — architecture in the Level 1 architecture overview, stack and defaults in the Level 3 project decisions, product behavior in `SPECIFICATION.md`, tunable values in `CUSTOM_SETTINGS.md`. Procedure: `architecture-decision` workflow.

## Autonomous and headless runs

Choose only a policy-compliant, non-Reserved path. **Must not** silently make a Reserved decision; report every unresolved Decision Request explicitly in the final report.
