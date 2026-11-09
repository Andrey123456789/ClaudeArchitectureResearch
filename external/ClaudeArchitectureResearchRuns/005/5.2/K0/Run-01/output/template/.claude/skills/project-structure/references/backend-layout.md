<!-- Kind: WF | Scope: backend | Owns: backend project layout reference (private to project-structure) | Loads: read by project-structure -->
# Backend Layout

Default physical structure of the ASP.NET Core backend. Architectural rules: `rules/backend/architecture.md` and `rules/backend/persistence.md`; this reference only shows where things go.

# Domain

```text
backend/
└── ProjectName.Domain/
    ├── Entities/
    └── Enums/
```

Possible later additions when an approved design justifies them: `ValueObjects/`, `DomainServices/`, `Events/`, `Exceptions/`. DDD-oriented directories are not created merely because the Domain contains business rules or workflow behavior (DDD adoption: CLAUDE.md § Decisions).

# Application

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

## `Abstractions/Persistence`

Inward-facing persistence contracts, for example `ITaskRepository.cs`, `IOrderRepository.cs`, `IUnitOfWork.cs` — no EF Core types.

## `Abstractions/ExternalServices`

Application-owned abstractions implemented by outer layers when needed, for example `IEmailSender.cs`, `ICurrentUser.cs`, `IFileStorage.cs`, `IPaymentGateway.cs`. Created only once such dependencies exist.

## `Services`

Application Services and useful public service contracts, for example `ITaskService.cs`, `TaskService.cs`. No handler/CQRS/MediatR structures (DEC-ARCH-02).

### Supporting Type Roles

Within a feature or service area, a supporting type's responsibility should be clear from its name, its immediate directory, or both. Established suffixes:

- `Service` — use-case orchestration;
- `Dto` — data-transfer models;
- `Request` / `Response` — Application operation contracts (transport-specific HTTP contracts belong to Api);
- `Result` / `Outcome` — operation results;
- `Validator` — validation;
- `Rules` / `Policy` — decision or workflow rules;
- `Factory` — object creation;
- `Mapper` — mapping;
- `Adapter` — boundary adaptation.

Prefer `TaskWorkflowRules`, `TaskWorkflowPolicy` or `TaskWorkflowService` over an ambiguous `TaskWorkflow` whose role cannot be inferred without opening the file. Use responsibility-specific subdirectories once a feature accumulates enough heterogeneous supporting types that a flat directory is hard to navigate — not to classify one or two obvious files. Avoid generic `Models`, `Helpers`, `Common` or `Utils` buckets when a more specific responsibility can be named.

## `DTOs`

Application-level operation/data models when useful; not a dumping ground.

## `Validation`

FluentValidation validators for Application-level input/use-case validation when required. Domain invariants stay in Domain (`rules/backend/error-handling.md` § Validation Boundaries).

## `DependencyInjection.cs`

Registers Application-owned services and Application-level validation infrastructure — not concrete Infrastructure implementations.

# Infrastructure

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
- `Repositories` — concrete repository implementations, optionally on an Infrastructure-only generic base that removes real duplication.
- `Migrations` — EF Core migrations.
- `Seeding` — Development database initialization (`rules/backend/persistence.md` § Development Seeding; example code in the `ef-core` skill).
- `Services` — technical/external implementations of Application abstractions, for example `EmailSender.cs`, `FileStorage.cs`, `PaymentGateway.cs`; capability-specific subdirectories when they improve cohesion.
- `DependencyInjection.cs` — registers `AppDbContext`, repository implementations, `IUnitOfWork`, external adapters, the SQL Server provider, `HttpClient` integrations and resilience handlers when used.

# API

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

- `Controllers` — ASP.NET Core Controllers (thin; `rules/backend/architecture.md` § API). No Minimal API endpoint groups unless explicitly requested (DEC-ARCH-02).
- `Contracts` — transport-specific request/response contracts; when to introduce them: `rules/backend/architecture.md` § Boundary Leaks.
- `Middleware` — only when custom middleware actually exists.
- `Extensions` — cohesive API/composition extension methods; do not move arbitrary code out of `Program.cs` merely to shorten it.
- `Program.cs` — composition root:

```csharp
builder.Services.AddApplication();
builder.Services.AddInfrastructure(builder.Configuration);
```

# Backend Test Projects

```text
backend/
├── ProjectName.Domain/
├── ProjectName.Application/
├── ProjectName.Application.Tests/
├── ProjectName.Infrastructure/
├── ProjectName.Api/
└── ProjectName.IntegrationTests/
```

`ProjectName.Domain.Tests` when Domain has non-trivial behavior worth testing independently; `ProjectName.Infrastructure.Tests` when Infrastructure has non-trivial behavior that benefits from a dedicated test assembly. No separate top-level `tests/` directory (DEC-LAYOUT-01).

# Project References

The allowed graph is `rules/backend/architecture.md` § Dependency Direction. Scaffolding commands:

```bash
dotnet add backend/ProjectName.Application reference backend/ProjectName.Domain
dotnet add backend/ProjectName.Infrastructure reference backend/ProjectName.Application backend/ProjectName.Domain
dotnet add backend/ProjectName.Api reference backend/ProjectName.Application backend/ProjectName.Infrastructure
```

If a feature seems to require another reference, reconsider the abstraction boundary instead. `node .claude/scripts/check-manifests.mjs` reports reference-direction violations.

# Test References

Typical test references, kept as narrow as the test scope (`rules/backend-tests/testing.md` § Test Project References):

```text
ProjectName.Domain.Tests              # optional
    -> ProjectName.Domain

ProjectName.Application.Tests
    -> ProjectName.Application
    -> ProjectName.Domain as needed

ProjectName.IntegrationTests
    -> ProjectName.Api

ProjectName.Infrastructure.Tests      # optional
    -> ProjectName.Infrastructure
    -> narrower references as required
```

Integration tests may transitively exercise Application, Infrastructure, EF Core, routing, DI, serialization and persistence through the API host.
