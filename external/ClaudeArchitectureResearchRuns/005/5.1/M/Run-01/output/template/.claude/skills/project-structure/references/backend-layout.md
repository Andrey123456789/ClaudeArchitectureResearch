> Owns: illustrative backend directory trees, type-role naming heuristics, project-reference examples | Scope: backend, backend-tests | Loads: private reference of project-structure (read on demand by that workflow only)

# Backend Layout — Examples

Boundaries and references are governed by `.claude/rules/architecture.md`.
Create only directories that contain real code.

## Domain

```text
backend/<Name>.Domain/
├── Entities/
└── Enums/
```

`ValueObjects/`, `DomainServices/`, `Events/`, `Exceptions/` appear only when an
approved design needs them; business rules alone do not justify DDD folders.

## Application

```text
backend/<Name>.Application/
├── Abstractions/
│   ├── Persistence/          # ITaskRepository.cs, IUnitOfWork.cs
│   └── ExternalServices/     # IEmailSender.cs, ICurrentUser.cs, IFileStorage.cs
├── Services/                 # ITaskService.cs, TaskService.cs
├── DTOs/
├── Validation/               # FluentValidation validators
└── DependencyInjection.cs    # AddApplication(): Application services only
```

`ExternalServices/` is created only when such dependencies exist. `DTOs/` is not
a dumping ground. `DependencyInjection.cs` never registers concrete
Infrastructure implementations.

### Supporting Type Roles

Make each supporting type's role clear from its name, its directory, or both.
Useful suffixes: `Service` (use-case orchestration), `Dto`, `Request`/`Response`
(Application operation contracts; HTTP contracts belong to Api),
`Result`/`Outcome`, `Validator`, `Rules`/`Policy` (decision or workflow rules),
`Factory`, `Mapper`, `Adapter`. Prefer `TaskWorkflowRules` or
`TaskWorkflowService` over an ambiguous `TaskWorkflow`. Add responsibility
subdirectories only when a feature accumulates enough heterogeneous types, and
name directories by the responsibility they hold (generic buckets:
`CLAUDE.md`, Core Defaults).

## Infrastructure

```text
backend/<Name>.Infrastructure/
├── Persistence/
│   ├── AppDbContext.cs
│   ├── UnitOfWork.cs
│   ├── Configurations/       # IEntityTypeConfiguration<T> mappings
│   ├── Repositories/         # concrete repositories (+ optional internal base)
│   ├── Migrations/
│   └── Seeding/
│       ├── DbSeeder.cs
│       └── DatabaseInitializationExtensions.cs
├── Services/                 # EmailSender.cs, FileStorage.cs, PaymentGateway.cs
└── DependencyInjection.cs    # AddInfrastructure(configuration)
```

`AddInfrastructure` registers `AppDbContext`, repositories, `IUnitOfWork`, the
SQL Server provider, external adapters, `HttpClient` integrations, and
resilience handlers when used.

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

Do not move arbitrary code out of `Program.cs` merely to shorten it.

## Project References

```text
<Name>.Domain          -> (none)
<Name>.Application     -> <Name>.Domain
<Name>.Infrastructure  -> <Name>.Application, <Name>.Domain
<Name>.Api             -> <Name>.Application, <Name>.Infrastructure

<Name>.Domain.Tests          (optional) -> <Name>.Domain
<Name>.Application.Tests     -> <Name>.Application (+ <Name>.Domain as needed)
<Name>.IntegrationTests      -> <Name>.Api
<Name>.Infrastructure.Tests  (optional) -> <Name>.Infrastructure (+ narrower as required)
```

Integration tests exercise Application, Infrastructure, EF Core, routing, DI,
serialization, and persistence transitively through the Api host.
