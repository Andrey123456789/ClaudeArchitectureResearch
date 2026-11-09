> Owns: backend project contents, naming heuristics, reference graph, and Development configuration examples (technique) | Scope: backend, backend-tests | Loads: private reference, read only by the project-structure skill

# Backend Layout

Architectural behavior is governed by `.claude/rules/architecture.md`; this reference shows the physical shape used while scaffolding. Which
directories to create at all: `.claude/rules/repository-structure.md`.

## Domain

```text
backend/
└── ProjectName.Domain/
    ├── Entities/
    └── Enums/
```

Later additions such as `ValueObjects/`, `DomainServices/`, `Events/`, or
`Exceptions/` appear only when an approved design needs them; business rules or
workflow behavior alone do not justify DDD-oriented directories.

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
  `ITaskRepository.cs`, `IOrderRepository.cs`, `IUnitOfWork.cs`.
- `Abstractions/ExternalServices` — Application-owned abstractions implemented
  by outer layers when needed (`IEmailSender.cs`, `ICurrentUser.cs`,
  `IFileStorage.cs`, `IPaymentGateway.cs`); create it only when such
  dependencies exist.
- `Services` — Application Services and useful public service contracts
  (`ITaskService.cs`, `TaskService.cs`). No handler/CQRS/MediatR structures.
- `DTOs` — Application-level operation/data models when useful; not a generic
  dumping ground.
- `Validation` — FluentValidation validators for Application-level input and
  use-case validation when required.
- `DependencyInjection.cs` — registers Application-owned services and
  Application-level validation; never concrete Infrastructure implementations.

### Supporting type roles

Within a feature or service area, make each supporting type's responsibility
clear from its name, its immediate directory, or both. Useful suffixes:

- `Service` — use-case orchestration;
- `Dto` — data-transfer models;
- `Request` / `Response` — Application operation contracts (transport-specific
  HTTP contracts belong to the Api project);
- `Result` / `Outcome` — operation results;
- `Validator` — validation;
- `Rules` / `Policy` — decision or workflow rules;
- `Factory` — object creation;
- `Mapper` — mapping;
- `Adapter` — boundary adaptation.

Avoid ambiguous names such as `TaskWorkflow` when the role cannot be inferred
without opening the file; prefer `TaskWorkflowRules`, `TaskWorkflowPolicy`, or
`TaskWorkflowService` according to the actual responsibility. Add
responsibility-specific subdirectories when a feature accumulates enough
heterogeneous supporting types that a flat directory is hard to navigate, not to
classify one or two obvious files. Avoid generic `Models`, `Helpers`, `Common`,
or `Utils` buckets when a more specific responsibility can be named.

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
- `Repositories` — concrete repository implementations (an Infrastructure-only
  generic base is allowed when it removes real duplication).
- `Migrations` — EF Core migrations.
- `Seeding` — Development database initialization (`ef-core` skill).
- `Services` — technical/external implementations of Application abstractions
  (`EmailSender.cs`, `FileStorage.cs`, `PaymentGateway.cs`); add
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

- `Controllers` — ASP.NET Core Controllers, kept thin.
- `Contracts` — transport-specific request/response contracts, when used
  (`.claude/rules/architecture.md` § Boundary Contracts).
- `Middleware` — only when custom middleware actually exists.
- `Extensions` — cohesive API/composition extension methods; do not move
  arbitrary code out of `Program.cs` solely to make it shorter.
- `Program.cs` — the composition root:

```csharp
builder.Services.AddApplication();
builder.Services.AddInfrastructure(builder.Configuration);
```

### Development configuration

API configuration includes `appsettings.json` and `appsettings.Development.json`.
A suitable Windows Development default for SQL Server LocalDB, which contains no
secret credentials:

```json
{
  "ConnectionStrings": {
    "DefaultConnection": "Server=(localdb)\\MSSQLLocalDB;Database=ProjectName;Trusted_Connection=True;TrustServerCertificate=True;"
  }
}
```

Adapt the database name to the project. When local SQL Server requires
credentials, keep the non-secret structure in configuration and supply the
secret through user-secrets (policy: `.claude/rules/persistence.md` and
`.claude/rules/security.md`).

Configure Swagger generation and Swagger UI so a Development run exposes
`/swagger` (`swagger` skill).

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

Which optional test projects to create: `project-structure` step 7.

## Project References

The production and test reference graph is owned by
`.claude/rules/architecture.md` § Project References. Add references with the
CLI and check the result:

```bash
dotnet add backend/ProjectName.Application/ProjectName.Application.csproj reference backend/ProjectName.Domain/ProjectName.Domain.csproj
node .claude/scripts/check-manifests.mjs
```

Integration tests reference the Api project and may transitively exercise
Application, Infrastructure, EF Core, routing, DI, serialization, and
persistence through the API host.
