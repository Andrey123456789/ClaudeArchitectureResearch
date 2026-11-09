> Kind: WF | Scope: backend | Owner: backend project layout reference for scaffolding (private to project-structure) | Loading: read by project-structure only

# Backend Layout

Default physical structure of the ASP.NET Core backend. Create only directories that contain real code.

# Domain

```text
backend/ProjectName.Domain/
├── Entities/
└── Enums/
```

Possible later additions when an approved design justifies them: `ValueObjects/`, `DomainServices/`, `Events/`, `Exceptions/`. Business rules or workflow behavior alone do not justify DDD-oriented directories.

# Application

```text
backend/ProjectName.Application/
├── Abstractions/
│   ├── Persistence/
│   └── ExternalServices/
├── Services/
├── DTOs/
├── Validation/
└── DependencyInjection.cs
```

- `Abstractions/Persistence` — inward-facing persistence contracts: `ITaskRepository.cs`, `IOrderRepository.cs`, `IUnitOfWork.cs`; no EF Core types.
- `Abstractions/ExternalServices` — Application-owned abstractions implemented by outer layers: `IEmailSender.cs`, `ICurrentUser.cs`, `IFileStorage.cs`, `IPaymentGateway.cs`. Create it when such a dependency exists.
- `Services` — Application Services and useful public service contracts: `ITaskService.cs`, `TaskService.cs`. No handler, CQRS or MediatR structures.
- `DTOs` — Application-level operation/data models when useful; not a dumping ground.
- `Validation` — FluentValidation validators for Application-level input and use-case validation.
- `DependencyInjection.cs` — registers Application services and Application-level validation infrastructure, never concrete Infrastructure implementations.

## Supporting type roles

Within a feature or service area, make each supporting type's responsibility clear from its name, its directory or both. Useful suffixes:

```text
Service            use-case orchestration
Dto                data-transfer model
Request/Response   Application operation contracts (HTTP contracts belong to Api)
Result/Outcome     operation results
Validator          validation
Rules/Policy       decision or workflow rules
Factory            object creation
Mapper             mapping
Adapter            boundary adaptation
```

Prefer `TaskWorkflowRules`, `TaskWorkflowPolicy` or `TaskWorkflowService` over an ambiguous `TaskWorkflow`. Add responsibility-specific subdirectories when a flat feature directory becomes hard to navigate, not to classify one or two obvious files. Avoid generic `Models`, `Helpers`, `Common` or `Utils` buckets when a specific responsibility can be named.

# Infrastructure

```text
backend/ProjectName.Infrastructure/
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

- `Configurations` — EF Core entity mappings; `Repositories` — concrete repositories (an Infrastructure-only generic base is allowed when it removes real duplication); `Migrations` — EF Core migrations; `Seeding` — Development database initialization (`ef-core` technique).
- `Services` — technical/external implementations of Application abstractions (`EmailSender.cs`, `FileStorage.cs`, `PaymentGateway.cs`); capability subdirectories when they improve cohesion.
- `DependencyInjection.cs` — registers `AppDbContext`, repositories, `IUnitOfWork`, external adapters, the SQL Server provider, HttpClient integrations and resilience handlers when used.

# Api

```text
backend/ProjectName.Api/
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

- `Controllers` — thin ASP.NET Core Controllers; no Minimal API endpoint groups unless explicitly requested.
- `Contracts` — API request/response contracts, when used (`rules/backend/architecture.md` § API layer).
- `Middleware` — only when custom middleware exists.
- `Extensions` — cohesive API/composition extension methods; do not move arbitrary code out of `Program.cs` just to shorten it.
- `Program.cs` — composition root:

```csharp
builder.Services.AddApplication();
builder.Services.AddInfrastructure(builder.Configuration);
```

# Project references

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

Never add `Domain -> Application`, `Domain -> Infrastructure` or `Application -> Infrastructure`; reconsider the abstraction boundary instead. `node .claude/scripts/check-dependencies.cjs` checks these references.

# Test references

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

Integration tests exercise Application, Infrastructure, EF Core, routing, DI, serialization and persistence transitively through the API host. Backend tests never go into a separate top-level `tests/` directory.
