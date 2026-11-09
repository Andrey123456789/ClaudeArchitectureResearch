> Level: 1-architecture · Capability: architecture/clean-architecture · Facet: architecture.layout · Owns: backend physical layout and project-reference graph (placement technique) · Scope: backend · Loading: read by `project-structure` and other workflows

# Clean Architecture Layout

Boundary rules: `.claude/rules/1-architecture/frame/boundaries.md`. This file shows where things go. Create only directories that contain real code; every tree below is a target, not a checklist.

## Projects

```text
backend/
├── <Name>.Domain/
├── <Name>.Application/
├── <Name>.Application.Tests/
├── <Name>.Infrastructure/
├── <Name>.Api/
└── <Name>.IntegrationTests/
```

## Domain

```text
<Name>.Domain/
├── Entities/
└── Enums/
```

Later additions such as `ValueObjects/`, `DomainServices/`, `Events/`, `Exceptions/` appear only when an approved design needs them; business rules or workflow behavior alone do not justify DDD-oriented directories.

## Application

```text
<Name>.Application/
├── Abstractions/
│   ├── Persistence/        # repository interfaces, IUnitOfWork — no persistence-implementation types
│   └── ExternalServices/   # IEmailSender, ICurrentUser, IFileStorage ... only once such dependencies exist
├── Services/               # Application Services (ITaskService, TaskService)
├── DTOs/                   # operation/data models when useful; not a dumping ground
├── Validation/             # request/use-case validators when required
└── DependencyInjection.cs  # AddApplication(): Application services and validation only
```

Supporting type roles should be clear from the type name, its directory, or both. Useful suffixes: `Service` (use-case orchestration), `Dto`, `Request`/`Response` (Application operation contracts; HTTP contracts belong to Api), `Result`/`Outcome`, `Validator`, `Rules`/`Policy` (decision or workflow rules), `Factory`, `Mapper`, `Adapter`. Prefer `TaskWorkflowRules` or `TaskWorkflowService` over an ambiguous `TaskWorkflow`. Add responsibility subdirectories only when a feature accumulates enough heterogeneous types; avoid generic `Models`/`Helpers`/`Common`/`Utils` buckets.

## Infrastructure

```text
<Name>.Infrastructure/
├── Persistence/
│   ├── <persistence context and commit-boundary implementation>
│   ├── Configurations/     # entity mappings
│   ├── Repositories/       # concrete repositories (optional internal generic base)
│   ├── Migrations/
│   └── Seeding/            # Development seeding (persistence.seeding)
├── Services/               # implementations of Application abstractions (EmailSender, FileStorage, PaymentGateway)
└── DependencyInjection.cs  # AddInfrastructure(configuration): persistence, repositories, IUnitOfWork, adapters, HttpClient integrations, resilience handlers when used
```

Create capability-specific subdirectories under `Services/` when they improve cohesion.

## Api

```text
<Name>.Api/
├── <entry points>/         # entry-point code; folder and type conventions: platform bindings
├── Contracts/
│   ├── Requests/
│   └── Responses/
├── Middleware/             # only when custom middleware exists
├── Extensions/             # cohesive composition extensions; not merely to shorten Program.cs
├── Program.cs
├── appsettings.json
└── appsettings.Development.json
```

Entry-point code lives in Api; its folder and type conventions follow the platform bindings (`.claude/rules/2-technology/backend-libraries.md` § Platform bindings). `Program.cs` composes the application by calling each layer's registration extension — `AddApplication()`, then `AddInfrastructure(configuration)`.

## Project-reference graph

```text
<Name>.Domain          -> (no application project references)
<Name>.Application     -> <Name>.Domain
<Name>.Infrastructure  -> <Name>.Application, <Name>.Domain
<Name>.Api             -> <Name>.Application, <Name>.Infrastructure
```

Never `Domain -> Application`, `Domain -> Infrastructure`, or `Application -> Infrastructure`.

## Test projects

| Project | Create when | Typical references |
| --- | --- | --- |
| `<Name>.Application.Tests` | use-case behavior worth isolated tests | Application (+ Domain as needed) |
| `<Name>.IntegrationTests` | API + Application + Infrastructure behavior through the in-memory test host | Api |
| `<Name>.Domain.Tests` (optional) | Domain holds non-trivial behavior worth testing independently | Domain |
| `<Name>.Infrastructure.Tests` (optional) | non-trivial Infrastructure behavior benefits from its own assembly | Infrastructure (+ narrower as required) |

A simple Domain of entities and enums needs no dedicated test project. Integration tests may exercise Application, Infrastructure, persistence, routing, DI, and serialization transitively through the host. Frontend tests stay inside the frontend workspace.
