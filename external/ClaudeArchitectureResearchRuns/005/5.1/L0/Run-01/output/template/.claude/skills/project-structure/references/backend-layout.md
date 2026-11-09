> Level: 3 Project · Owns: backend project layout technique (private reference of `project-structure`) · Scope: backend · Loads: read by `project-structure` only

# Backend Layout

Typical internal layout. Create a directory only when it contains real code. Boundary rules: `.claude/rules/1-architecture/`.

## Domain

```text
backend/<Name>.Domain/
├── Entities/
└── Enums/
```

`ValueObjects/`, `DomainServices/`, `Events/` or `Exceptions/` appear only when an approved design needs them; DDD-oriented directories are not created merely because the Domain has business rules (`backend-layers.md`).

## Application

```text
backend/<Name>.Application/
├── Abstractions/
│   ├── Persistence/          # ITaskRepository.cs, IUnitOfWork.cs
│   └── ExternalServices/     # IEmailSender.cs, ICurrentUser.cs, IFileStorage.cs — only when such dependencies exist
├── Services/                 # ITaskService.cs, TaskService.cs
├── DTOs/                     # Application operation and data models, when useful — not a dumping ground
├── Validation/               # FluentValidation validators, when explicit validators are required
└── DependencyInjection.cs    # AddApplication(): Application services and validator registration
```

`DependencyInjection.cs` holds the Application-owned registrations (registration placement: `backend-layers.md`). Use feature subdirectories or role-revealing names (`code-organization.md`) when a feature accumulates heterogeneous supporting types.

## Infrastructure

```text
backend/<Name>.Infrastructure/
├── Persistence/
│   ├── AppDbContext.cs
│   ├── UnitOfWork.cs
│   ├── Configurations/       # IEntityTypeConfiguration<T> mappings
│   ├── Repositories/         # concrete repositories (optional Infrastructure-only base class)
│   ├── Migrations/           # EF Core migrations
│   └── Seeding/
│       ├── DbSeeder.cs                          # internal
│       └── DatabaseInitializationExtensions.cs  # narrow public entry point
├── Services/                 # EmailSender.cs, FileStorage.cs — implementations of Application abstractions
└── DependencyInjection.cs    # AddInfrastructure(configuration)
```

`AddInfrastructure` registers `AppDbContext` with the SQL Server provider, repository implementations, `IUnitOfWork`, external adapters, `HttpClient` integrations and resilience handlers when used. Capability-specific subdirectories under `Services/` are fine when they improve cohesion.

## Api

```text
backend/<Name>.Api/
├── Controllers/
├── Contracts/
│   ├── Requests/
│   └── Responses/            # only when transport contracts add a boundary benefit (entry-points.md)
├── Middleware/               # only when custom middleware exists
├── Extensions/               # cohesive composition extensions — not a place to shorten Program.cs arbitrarily
├── Program.cs
├── appsettings.json
└── appsettings.Development.json
```

Typical composition in `Program.cs`:

```csharp
builder.Services.AddApplication();
builder.Services.AddInfrastructure(builder.Configuration);
```

## Project References

```text
<Name>.Domain          -> (no application project references)
<Name>.Application     -> <Name>.Domain
<Name>.Infrastructure  -> <Name>.Application, <Name>.Domain
<Name>.Api             -> <Name>.Application, <Name>.Infrastructure
```

`.claude/scripts/check-architecture.mjs` rejects any other production edge, for example `Domain -> Application`, `Domain -> Infrastructure` or `Application -> Infrastructure` (rule: `backend-layers.md`).

## Test References

```text
<Name>.Domain.Tests          -> <Name>.Domain                        (optional project)
<Name>.Application.Tests     -> <Name>.Application (+ <Name>.Domain as needed)
<Name>.IntegrationTests      -> <Name>.Api
<Name>.Infrastructure.Tests  -> <Name>.Infrastructure (+ narrower references as required; optional project)
```

Integration tests exercise Application, Infrastructure, EF Core, routing, DI, serialization and persistence transitively through the API host.
