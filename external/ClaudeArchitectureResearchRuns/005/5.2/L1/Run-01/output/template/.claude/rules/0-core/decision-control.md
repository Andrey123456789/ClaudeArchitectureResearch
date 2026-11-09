---
paths:
  - "**/*"
---
> Level: 0-core | Owns: decision classes, approval boundary, Decision Request format, headless behavior | Scope: common | Loads: always (imported by CLAUDE.md)

# Decision Control

Classify each consequential choice before acting.

- **Decided** — already settled by product inputs, the project decision
  artifacts (adopted architecture, project stack, capability selection), or an
  accepted ADR. Follow it; reopening it requires approval.
- **Delegated** — local, reversible, and does not materially change a boundary,
  dependency, accepted convention, public contract, or observable behavior.
  Routine internal implementation choices that do not change observable behavior
  do not require approval: decide and proceed.
- **Reserved** — requires explicit approval. Reserved decisions include at least:
  1. changing an accepted project or architecture decision, including a
     capability selection;
  2. adopting an architectural style or pattern the project has not adopted —
     for example a Rich Domain Model or systematic DDD tactical patterns, CQRS,
     mediator-based dispatch, Vertical Slice Architecture, event sourcing, a
     project-wide Result/railway-oriented model, or microservices;
  3. adding a production project, layer, or assembly, or changing the project
     reference graph;
  4. changing persistence boundaries (for example multiple persistence
     contexts) or the persistence technology;
  5. adding an infrastructure category — messaging, background processing,
     distributed cache, search, external storage, external identity;
  6. adding a major library or framework, or replacing an approved baseline
     technology;
  7. introducing a project-wide convention or abstraction that other code is
     expected to follow;
  8. changing the authentication/authorization architecture;
  9. making a breaking public API change or adopting API versioning;
  10. defining product behavior or tunable values that product sources do not
      define (product governance).

A choice already required by the specification or the established project
structure is Decided, not Reserved. Do not ask for approval of routine local
decisions already constrained by the specification, approved stack, existing
code, or rules.

For an unclear case, answer these questions; any "yes" makes it Reserved:

1. Does it add, remove, or replace a dependency, framework, or infrastructure capability?
2. Does it change a project, layer, or reference boundary?
3. Does it establish a convention that other code is expected to follow?
4. Does it change observable behavior or a public contract?
5. Would it be expensive to reverse after other code depends on it?

## Decision Request

When a Reserved decision is needed, stop that part of the work and present:

- **Context** — what requires the decision and why now;
- **Options** — realistic alternatives with key trade-offs;
- **Recommendation** — the preferred option and why;
- **Blocked** — what cannot proceed until the decision is made;
- **Proceeding with** — the policy-compliant, non-Reserved work that continues meanwhile.

An explicit user instruction counts as approval. Record every accepted Reserved
decision with the `architecture-decision` workflow.

## Autonomous and headless runs

Choose only a policy-compliant, non-Reserved path. Never make a Reserved
decision silently; list every unresolved Decision Request explicitly in the
final report.
