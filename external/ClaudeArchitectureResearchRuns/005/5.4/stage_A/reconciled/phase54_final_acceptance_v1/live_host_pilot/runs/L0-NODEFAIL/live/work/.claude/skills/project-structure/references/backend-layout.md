> Level: 3 Project · Owns: backend directory examples and type-role naming heuristics for `project-structure` (private reference) · Scope: backend · Loads: read by `project-structure` only · Depends on: .claude/skills/project-structure/SKILL.md

# Backend Layout

Boundaries are owned by `.claude/rules/1-architecture/` (`backend-layers.md`, `persistence-boundary.md`, `entry-points.md`, `code-organization.md`); project mapping and test references by `.claude/rules/3-project/layout.md`; seeding by `.claude/rules/3-project/data-lifecycle.md`. Create only directories that contain real code.

## Domain

```text
backend/<Name>.Domain/
├── Entities/
└── Enums/
```

Later, only when an approved design needs them: `ValueObjects/`, `DomainServices/`, `Events/`, `Exceptions/`. Business rules or workflow behavior alone do not justify DDD-oriented directories.

## Application

```text
backend/<Name>.Application/
├── Abstractions/
│   ├── Persistence/          # ITaskRepository.cs, IOrderRepository.cs, IUnitOfWork.cs
│   └── ExternalServices/     # IEmailSender.cs, ICurrentUser.cs, IFileStorage.cs — only when needed
├── Services/                 # ITaskService.cs, TaskService.cs
├── DTOs/                     # operation/data models when useful — not a dumping ground
├── Validation/               # validators for Application input when needed
└── DependencyInjection.cs    # AddApplication(): Application services and validation only
```

### Supporting type roles

Make each supporting type's responsibility clear from its name, its directory, or both. Established suffixes:

- `Service` — use-case orchestration;
- `Dto` — data-transfer model;
- `Request` / `Response` — Application operation contracts (HTTP-specific contracts belong to Api);
- `Result` / `Outcome` — operation results;
- `Validator` — validation;
- `Rules` / `Policy` — decision or workflow rules;
- `Factory`, `Mapper`, `Adapter` — creation, mapping, boundary adaptation.

Prefer `TaskWorkflowRules`, `TaskWorkflowPolicy`, or `TaskWorkflowService` over an ambiguous `TaskWorkflow`. Introduce responsibility subdirectories only when a feature accumulates enough heterogeneous types that a flat directory is hard to navigate; avoid generic `Models`, `Helpers`, `Common`, `Utils` buckets.

## Infrastructure

```text
backend/<Name>.Infrastructure/
├── Persistence/
│   ├── AppDbContext.cs
│   ├── UnitOfWork.cs
│   ├── Configurations/       # IEntityTypeConfiguration<T> mappings
│   ├── Repositories/         # concrete repositories (+ optional Infrastructure-only base)
│   ├── Migrations/
│   └── Seeding/
│       ├── DbSeeder.cs
│       └── DatabaseInitializationExtensions.cs
├── Services/                 # EmailSender.cs, FileStorage.cs, PaymentGateway.cs
└── DependencyInjection.cs    # AddInfrastructure(configuration)
```

`AddInfrastructure` registers `AppDbContext`, repository implementations, `IUnitOfWork`, external adapters, the SQL Server provider, `HttpClient` integrations, and resilience handlers when used. Create capability-specific subdirectories under `Services/` when they improve cohesion.

## Api

```text
backend/<Name>.Api/
├── Controllers/
├── Contracts/
│   ├── Requests/
│   └── Responses/
├── Middleware/               # only when custom middleware exists
├── Extensions/               # cohesive composition extensions only
├── Program.cs
├── appsettings.json
└── appsettings.Development.json
```

Composition in `Program.cs`:

```csharp
builder.Services.AddApplication();
builder.Services.AddInfrastructure(builder.Configuration);
```

Use `Contracts/` only when transport-specific contracts provide a concrete boundary benefit. Do not move arbitrary code out of `Program.cs` only to make it shorter.

## Tests

```text
backend/
├── <Name>.Application.Tests/
└── <Name>.IntegrationTests/
```

Integration tests may transitively exercise Application, Infrastructure, EF Core, routing, DI, serialization, and persistence through the API host.
