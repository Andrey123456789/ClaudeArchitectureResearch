---
paths:
  - "backend/**/*"
---
> Level: 1-architecture | Capability: architecture/clean-architecture (architecture.boundaries) | Owns: role-to-layer mapping, dependency direction, layer responsibilities | Scope: backend, backend-tests | Loads: path (backend files)

# Clean Architecture Layering

## Role mapping

| Role | Location (`backend/<Name>.<Layer>/`) |
|---|---|
| domain model | `<Name>.Domain` — entities, enums, genuine domain behavior |
| use-case unit | `<Name>.Application` — Application Service (`Services/`) |
| persistence-access contract | `<Name>.Application` — specific repository interface (`Abstractions/Persistence/I<Entity>Repository`) |
| commit boundary | `<Name>.Application` — `IUnitOfWork` (`Abstractions/Persistence/`) |
| external-service contract | `<Name>.Application` — `Abstractions/ExternalServices/` |
| adapter | `<Name>.Infrastructure` — persistence implementation (`Persistence/`), external adapters (`Services/`) |
| entry point | `<Name>.Api` — Controller (`Controllers/`) |
| transport contract | `<Name>.Api` — `Contracts/Requests`, `Contracts/Responses` when needed |
| composition root | `<Name>.Api/Program.cs` |
| test-project role | `<Name>.Application.Tests`, `<Name>.IntegrationTests`; optional `<Name>.Domain.Tests`, `<Name>.Infrastructure.Tests` |

## Dependency direction

Dependencies point inward:

- Domain depends on no other application project.
- Application depends on Domain.
- Infrastructure depends on Application and Domain.
- Api depends on Application and may reference Infrastructure only for
  composition and dependency registration.
- Inner layers never depend on outer layers; never add Domain → Application,
  Domain → Infrastructure, or Application → Infrastructure. If a feature seems
  to need one of them, reconsider the abstraction boundary.

Test-project references: `<Name>.Domain.Tests` → Domain; `<Name>.Application.Tests`
→ Application (and Domain as needed); `<Name>.IntegrationTests` → Api (it
exercises Application and Infrastructure through the host);
`<Name>.Infrastructure.Tests` → Infrastructure plus narrower references as
required.

## Layer responsibilities

- Default: Application Services are the orchestration mechanism for use cases;
  they may coordinate domain objects, repositories, external-service
  abstractions, and the Unit of Work.
- Application defines the persistence and external-service abstractions its use
  cases require; Infrastructure implements them. Keep infrastructure
  implementation details out of Application.

Physical layout and scaffolding: `architecture.layout`. Mechanical check:
`node .claude/scripts/check-architecture.cjs`.
