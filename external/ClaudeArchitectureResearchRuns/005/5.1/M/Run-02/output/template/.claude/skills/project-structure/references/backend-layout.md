> Owner: private reference of the `project-structure` workflow — backend project internals, reference graph, naming heuristics | Scope: backend | Loads: read by `project-structure` only | Enforced: `.claude/scripts/check-architecture.mjs` (reference graph)

# Backend Layout

Default physical structure of the ASP.NET Core backend. Boundaries and layer
responsibilities: `.claude/rules/architecture.md`; persistence:
`.claude/rules/persistence.md`. Create only directories that contain real code.

## Domain

```text
backend/
└── ProjectName.Domain/
    ├── Entities/
    └── Enums/
```

Possible later additions when an approved design justifies them: `ValueObjects/`,
`DomainServices/`, `Events/`, `Exceptions/`. Business rules or workflow behavior
alone do not justify DDD-oriented directories.

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

- `Abstractions/Persistence` — inward-facing persistence contracts:
  `ITaskRepository.cs`, `IOrderRepository.cs`, `IUnitOfWork.cs`.
- `Abstractions/ExternalServices` — Application-owned abstractions implemented
  by outer layers when needed: `IEmailSender.cs`, `ICurrentUser.cs`,
  `IFileStorage.cs`, `IPaymentGateway.cs`. Create it when the first such
  dependency exists.
- `Services` — Application Services and their public contracts:
  `ITaskService.cs`, `TaskService.cs`. No handler, CQRS, or MediatR trees.
- `DTOs` — Application-level operation and data models when useful; not a
  dumping ground.
- `Validation` — FluentValidation validators for Application-level input and
  use-case validation.
- `DependencyInjection.cs` — registers Application-owned services and
  Application-level validation; concrete Infrastructure implementations are
  registered by Infrastructure.

### Supporting Type Roles

Make each supporting type's responsibility clear from its name, its immediate
directory, or both. Useful suffixes:

- `Service` — use-case orchestration;
- `Dto` — data-transfer model;
- `Request` / `Response` — Application operation contracts (HTTP-specific
  contracts belong to the API layer);
- `Result` / `Outcome` — operation results;
- `Validator` — validation;
- `Rules` / `Policy` — decision or workflow rules;
- `Factory`, `Mapper`, `Adapter` — creation, mapping, boundary adaptation.

Prefer `TaskWorkflowRules`, `TaskWorkflowPolicy`, or `TaskWorkflowService` over an
ambiguous `TaskWorkflow`. Add responsibility-specific subdirectories when a
feature accumulates enough heterogeneous types that a flat directory becomes
hard to navigate, not to classify one or two files. Prefer a specific name over
generic `Models`, `Helpers`, `Common`, or `Utils` buckets.

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

- `Configurations` — EF Core entity mappings (`IEntityTypeConfiguration<T>`).
- `Repositories` — concrete repository implementations, optionally on an
  Infrastructure-only generic base that removes real duplication.
- `Migrations` — EF Core migrations.
- `Seeding` — Development database initialization (pattern in the `ef-core`
  skill).
- `Services` — technical implementations of Application abstractions
  (`EmailSender.cs`, `FileStorage.cs`, `PaymentGateway.cs`); add
  capability-specific subdirectories when they improve cohesion.
- `DependencyInjection.cs` — registers `AppDbContext`, repository
  implementations, `IUnitOfWork`, external adapters, the SQL Server provider,
  `HttpClient` integrations, and resilience handlers when used.

## API

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
  unless explicitly requested.
- `Contracts` — transport-specific request/response contracts when separation
  from Application models provides value.
- `Middleware` — only when custom middleware exists.
- `Extensions` — cohesive API and composition extension methods; do not move
  arbitrary code out of `Program.cs` merely to shorten it.
- `Program.cs` — the composition root:

```csharp
builder.Services.AddApplication();
builder.Services.AddInfrastructure(builder.Configuration);
```

What Controllers may depend on: `.claude/rules/architecture.md` § API.

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

`ProjectName.Domain.Tests` and `ProjectName.Infrastructure.Tests` are added only
when their layer has non-trivial behavior that benefits from a dedicated test
assembly.

## Project References

The reference graph that implements `.claude/rules/architecture.md`
§ Dependency Direction:

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

Test project references (`.claude/rules/testing.md` § Test Project References):

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

Integration tests exercise Application, Infrastructure, EF Core, routing, DI,
serialization, and persistence transitively through the API host.
`node .claude/scripts/check-architecture.mjs` reports references outside this
graph.
