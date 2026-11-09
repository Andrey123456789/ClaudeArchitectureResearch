---
paths:
  - "**/*"
---
> Level: 1-architecture | Owns: stable architecture role vocabulary | Scope: common | Loads: always (imported by CLAUDE.md)

# Architecture Roles

Rules, workflows, and capability facets outside the architecture frame use these
roles instead of the frame's own layer names. The selected architecture frame
maps every role to a concrete project and location.

| Role | Responsibility |
|---|---|
| domain model | business entities, enums, value types, and invariants the business genuinely owns |
| use-case unit | orchestrates one application use case: loads state through contracts, applies use-case rules, decides when to commit |
| persistence-access contract | use-case-facing contract for loading and staging persistent state for one cohesive need |
| commit boundary | use-case-facing contract that commits the staged changes of one use case |
| external-service contract | use-case-facing contract for an outside capability (e-mail, payments, current user, remote API) |
| adapter | technical implementation of a contract: persistence implementation, remote-service client, cache, startup initialization |
| entry point | transport endpoint that binds and validates input, invokes use-case units, and maps outcomes to transport responses |
| transport contract | request/response shape published by an entry point |
| composition root | host startup that registers implementations and builds the request pipeline |
| test-project role | automated test assembly for one target: use-case/domain unit tests, host-level integration tests, optional adapter tests |
