> Level: 3 Project | Owns: backend directory and reference layout examples (private to `project-structure`) | Scope: backend | Loads: on demand by `project-structure` | Depends on: 1-architecture/backend-layers.md, 3-project/data-lifecycle.md

# Backend Layout

Illustrative structure; create a directory only when it contains real code.

## Domain

```text
backend/<Name>.Domain/
├── Entities/
└── Enums/
```

`ValueObjects/`, `DomainServices/`, `Events/`, `Exceptions/` appear only when an
approved design needs them.

## Application

```text
backend/<Name>.Application/
├── Abstractions/
│   ├── Persistence/          ITaskRepository.cs, IUnitOfWork.cs
│   └── ExternalServices/     IEmailSender.cs, ICurrentUser.cs (only when needed)
├── Services/                 ITaskService.cs, TaskService.cs
├── DTOs/
├── Validation/               FluentValidation validators
└── DependencyInjection.cs    AddApplication(): Application services + validators
```

Naming heuristics: make each supporting type's role clear from its name or
directory — `Service`, `Dto`, `Request`/`Response` (Application operation
contracts; HTTP contracts belong to the Api), `Result`/`Outcome`, `Validator`,
`Rules`/`Policy`, `Factory`, `Mapper`, `Adapter`. Prefer `TaskWorkflowRules`
or `TaskWorkflowService` over an ambiguous `TaskWorkflow`. Add
responsibility-specific subdirectories only when a flat feature directory
becomes hard to navigate; avoid `Models`, `Helpers`, `Common`, `Utils`.

## Infrastructure

```text
backend/<Name>.Infrastructure/
├── Persistence/
│   ├── AppDbContext.cs
│   ├── UnitOfWork.cs
│   ├── Configurations/       IEntityTypeConfiguration<T> mappings
│   ├── Repositories/         concrete repositories (optional internal base)
│   ├── Migrations/
│   └── Seeding/              DbSeeder.cs, DatabaseInitializationExtensions.cs
├── Services/                 EmailSender.cs, FileStorage.cs, ...
└── DependencyInjection.cs    AddInfrastructure(configuration)
```

`AddInfrastructure` registers `AppDbContext` with the SQL Server provider,
repositories, `IUnitOfWork`, external adapters, `HttpClient` integrations, and
resilience handlers when used.

## Api

```text
backend/<Name>.Api/
├── Controllers/
├── Contracts/Requests/  Contracts/Responses/   (when separation adds value)
├── Middleware/                                 (only for real middleware)
├── Extensions/                                 (cohesive composition helpers)
├── Program.cs
├── appsettings.json
└── appsettings.Development.json
```

```csharp
builder.Services.AddApplication();
builder.Services.AddInfrastructure(builder.Configuration);
```

Do not move code out of `Program.cs` solely to shorten it. Controllers do not
consume Infrastructure types even though the Api project references
Infrastructure for composition.

## Project References

```text
<Name>.Domain          -> (no application project references)
<Name>.Application     -> <Name>.Domain
<Name>.Infrastructure  -> <Name>.Application, <Name>.Domain
<Name>.Api             -> <Name>.Application, <Name>.Infrastructure
```

Never: Domain → Application, Domain → Infrastructure, Application →
Infrastructure. `check-manifests.cjs` reports these mechanically.

## Test References

```text
<Name>.Domain.Tests          -> <Name>.Domain                      (optional)
<Name>.Application.Tests     -> <Name>.Application (+ Domain as needed)
<Name>.IntegrationTests      -> <Name>.Api
<Name>.Infrastructure.Tests  -> <Name>.Infrastructure (+ narrower as needed; optional)
```

Integration tests exercise Application, Infrastructure, EF Core, routing, DI,
serialization, and persistence transitively through the Api host. No top-level
`tests/` directory.
