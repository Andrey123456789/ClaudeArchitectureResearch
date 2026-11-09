> Private reference of the project-structure workflow. Owns: backend project layout examples, directory roles, and naming heuristics · Scope: backend, backend-tests · Loads: read by project-structure when creating or reorganizing backend projects · Depends on: .claude/skills/project-structure/SKILL.md

# Backend Layout

Layer rules, allowed project references, and test-project reference limits:
`.claude/rules/architecture.md`. Repositories, Unit of Work, and seeding:
`.claude/rules/persistence.md`. The trees below are targets; create only
directories that contain real code.

## Domain

```text
backend/
└── ProjectName.Domain/
    ├── Entities/
    └── Enums/
```

Later additions such as `ValueObjects/`, `DomainServices/`, `Events/`, or
`Exceptions/` belong only to an approved design that uses them; business rules
or workflow behavior alone do not justify DDD-oriented directories.

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

- `Abstractions/Persistence` — inward-facing persistence contracts such as
  `ITaskRepository.cs`, `IOrderRepository.cs`, `IUnitOfWork.cs`; no EF Core
  types.
- `Abstractions/ExternalServices` — Application-owned abstractions implemented
  by outer layers, such as `IEmailSender.cs`, `ICurrentUser.cs`,
  `IFileStorage.cs`, `IPaymentGateway.cs`; create it only when such
  dependencies exist.
- `Services` — Application Services and useful public service contracts, such
  as `ITaskService.cs` and `TaskService.cs`; no handler/CQRS/MediatR trees.
- `DTOs` — Application-level operation and data models when useful; not a
  generic dumping ground.
- `Validation` — FluentValidation validators for Application-level input and
  use-case validation when required.
- `DependencyInjection.cs` — registers Application-owned services and
  Application-level validation; Infrastructure registers its own
  implementations (`.claude/rules/architecture.md`, Composition and
  Configuration).

### Supporting Type Roles

Within a feature or service area, make each supporting type's responsibility
clear from its name, its directory, or both. Established suffixes:

- `Service` — use-case orchestration;
- `Dto` — data-transfer models;
- `Request` / `Response` — Application operation contracts (HTTP-specific
  contracts belong to the Api layer);
- `Result` / `Outcome` — operation results;
- `Validator` — validation;
- `Rules` / `Policy` — decision or workflow rules;
- `Factory` — object creation;
- `Mapper` — mapping;
- `Adapter` — boundary adaptation.

Avoid ambiguous names such as `TaskWorkflow` when the role cannot be inferred
without opening the file; prefer `TaskWorkflowRules`, `TaskWorkflowPolicy`, or
`TaskWorkflowService` according to the actual responsibility. Use
responsibility-specific subdirectories when a feature accumulates enough
heterogeneous types that a flat directory becomes hard to navigate, but not to
classify one or two files whose roles are obvious. Avoid generic `Models`,
`Helpers`, `Common`, or `Utils` buckets when a specific responsibility can be
named.

## Infrastructure

```text
backend/
└── ProjectName.Infrastructure/
    ├── Persistence/
    │   ├── AppDbContext.cs
    │   ├── UnitOfWork.cs
    │   ├── Configurations/
    │   ├── Repositories/
    │   ├── Migrations/
    │   └── Seeding/
    │       ├── DbSeeder.cs
    │       └── DatabaseInitializationExtensions.cs
    ├── Services/
    └── DependencyInjection.cs
```

- `Configurations` — EF Core entity mappings.
- `Repositories` — concrete repository implementations (an
  Infrastructure-only generic base is allowed when it removes real
  duplication).
- `Migrations` — EF Core migrations.
- `Seeding` — Development database initialization (`ef-core` skill).
- `Services` — technical/external implementations of Application abstractions,
  such as `EmailSender.cs`, `FileStorage.cs`, `PaymentGateway.cs`; use
  capability-specific subdirectories when they improve cohesion.
- `DependencyInjection.cs` — registers `AppDbContext`, repository
  implementations, `IUnitOfWork`, external adapters, the SQL Server provider,
  `HttpClient` integrations, and resilience handlers when used.

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

- `Controllers` — ASP.NET Core Controllers; no Minimal API endpoint groups
  unless explicitly requested and approved.
- `Contracts` — transport-specific request/response contracts when separation
  from Application models provides value.
- `Middleware` — only when custom middleware exists.
- `Extensions` — cohesive Api/composition extension methods; do not move
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

`ProjectName.Domain.Tests` is added when Domain contains non-trivial behavior
worth testing independently, and `ProjectName.Infrastructure.Tests` when
Infrastructure has non-trivial behavior that benefits from a dedicated test
assembly. Integration tests may transitively exercise Application,
Infrastructure, EF Core, routing, DI, serialization, and persistence through the
Api host.
