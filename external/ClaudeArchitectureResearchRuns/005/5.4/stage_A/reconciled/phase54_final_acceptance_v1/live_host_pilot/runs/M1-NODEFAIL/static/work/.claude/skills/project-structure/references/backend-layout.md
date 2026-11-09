> Capability: architecture/clean-architecture · Private reference of `project-structure` · Backend placement technique for the frame · Rules: `.claude/rules/architecture.md`

# Backend Layout

## Domain

```text
backend/
└── ProjectName.Domain/
    ├── Entities/
    └── Enums/
```

Create additional directories only when the Domain needs them. Possible later
additions, when justified by an approved design, include `ValueObjects/`,
`DomainServices/`, `Events/`, and `Exceptions/`. Do not create DDD-oriented
directories merely because the Domain contains business rules or workflow
behavior.

## Application

```text
backend/
└── ProjectName.Application/
    ├── Abstractions/
    │   ├── Persistence/
    │   └── ExternalServices/
    ├── Services/
    ├── DTOs/
    ├── Validation/
    └── DependencyInjection.cs
```

Create only directories that contain real code.

- `Abstractions/Persistence` — inward-facing persistence contracts such as
  `ITaskRepository.cs`, `IOrderRepository.cs`, `IUnitOfWork.cs`; no
  persistence-technology types.
- `Abstractions/ExternalServices` — Application-owned abstractions implemented
  by outer layers when needed, such as `IEmailSender.cs`, `ICurrentUser.cs`,
  `IFileStorage.cs`, `IPaymentGateway.cs`; do not create it before such
  dependencies exist.
- `Services` — Application Services and useful public service contracts
  (`ITaskService.cs`, `TaskService.cs`); no handler/CQRS/mediator structures.
- `DTOs` — Application-level operation and data models when useful; not a
  dumping ground.
- `Validation` — FluentValidation validators for Application-level input and
  use-case validation when required.
- `DependencyInjection.cs` — registers Application-owned services and
  Application-level validation infrastructure; never concrete Infrastructure
  implementations.

### Supporting Type Roles

Within a feature or service area, make each supporting type's responsibility
clear from its name, its immediate directory, or both. Prefer established
suffixes: `Service` (use-case orchestration), `Dto` (data transfer),
`Request`/`Response` (Application operation contracts; HTTP transport contracts
belong to Api), `Result`/`Outcome` (operation results), `Validator`,
`Rules`/`Policy` (decision or workflow rules), `Factory`, `Mapper`, `Adapter`.

Avoid ambiguous names such as `TaskWorkflow` when the role cannot be inferred
without opening the file; prefer `TaskWorkflowRules`, `TaskWorkflowPolicy`, or
`TaskWorkflowService` according to the actual responsibility. Add
responsibility-specific subdirectories only when a flat directory becomes hard
to navigate, and avoid generic `Models`, `Helpers`, `Common`, or `Utils`
buckets when a more specific responsibility can be named.

## Infrastructure

```text
backend/
└── ProjectName.Infrastructure/
    ├── Persistence/
    │   ├── Configurations/
    │   ├── Repositories/
    │   ├── Migrations/
    │   └── Seeding/
    ├── Services/
    └── DependencyInjection.cs
```

- `Persistence/` — the persistence implementation: session, Unit of Work,
  entity configurations, concrete repositories (an Infrastructure-only generic
  base is allowed when it removes real duplication), migrations, and
  Development seeding. Technology-specific contents: the persistence knowledge
  skill.
- `Services/` — technical and external implementations of Application
  abstractions (`EmailSender.cs`, `FileStorage.cs`, `PaymentGateway.cs`); add
  capability-specific subdirectories when they improve cohesion.
- `DependencyInjection.cs` — registers Infrastructure-owned implementations and
  technical dependencies: the persistence session and provider, repository
  implementations, `IUnitOfWork`, external adapters, `HttpClient`
  integrations, resilience handlers when used.

## Api

```text
backend/
└── ProjectName.Api/
    ├── Controllers/
    ├── Contracts/
    │   ├── Requests/
    │   └── Responses/
    ├── Middleware/
    ├── Extensions/
    ├── Program.cs
    ├── appsettings.json
    └── appsettings.Development.json
```

Create optional directories only when needed.

- `Controllers` — ASP.NET Core Controllers are the HTTP endpoint mechanism; do
  not create Minimal API endpoint groups unless explicitly requested.
- `Contracts` — transport-specific request/response contracts, when
  `.claude/rules/architecture.md` § Layer Placement calls for them.
- `Middleware` — only when custom middleware exists.
- `Extensions` — cohesive API/composition extension methods; do not move
  arbitrary code out of `Program.cs` solely to shorten it.
- `Program.cs` — the composition root:

  ```csharp
  builder.Services.AddApplication();
  builder.Services.AddInfrastructure(builder.Configuration);
  ```

## Backend Test Projects

```text
backend/
├── ProjectName.Domain/
├── ProjectName.Application/
├── ProjectName.Application.Tests/
├── ProjectName.Infrastructure/
├── ProjectName.Api/
└── ProjectName.IntegrationTests/
```

Create only useful test projects. Add `ProjectName.Domain.Tests` only when the
Domain contains non-trivial behavior worth testing independently, and
`ProjectName.Infrastructure.Tests` only when Infrastructure has non-trivial
behavior that benefits from a dedicated test assembly. Test-project location:
`docs/capabilities/architecture.md` § Repository Layout.

Typical intent: `Application.Tests` covers application-service and use-case
behavior; `IntegrationTests` covers Api + Application + Infrastructure through
the real host (`WebApplicationFactory<Program>`).

## Project References

```text
ProjectName.Domain
    -> no application project references

ProjectName.Application
    -> ProjectName.Domain

ProjectName.Infrastructure
    -> ProjectName.Application
    -> ProjectName.Domain

ProjectName.Api
    -> ProjectName.Application
    -> ProjectName.Infrastructure
```

This graph implements `.claude/rules/architecture.md` § Dependency Direction.
If a feature seems to require an outward reference such as
`Application -> Infrastructure`, reconsider the abstraction boundary instead.

## Test References

```text
ProjectName.Domain.Tests              # optional
    -> ProjectName.Domain

ProjectName.Application.Tests
    -> ProjectName.Application
    -> ProjectName.Domain as needed

ProjectName.IntegrationTests
    -> ProjectName.Api

ProjectName.Infrastructure.Tests       # optional
    -> ProjectName.Infrastructure
    -> narrower references as required
```

Integration tests may transitively exercise Application, Infrastructure,
persistence, routing, dependency injection, and serialization through the Api
host.
