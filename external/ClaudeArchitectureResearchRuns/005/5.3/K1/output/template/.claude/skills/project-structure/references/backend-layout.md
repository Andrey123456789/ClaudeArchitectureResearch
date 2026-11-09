> Kind: WF | Scope: backend | Capability: architecture/clean-architecture | Loading: read by `project-structure` when its step says so

# Backend Layout — Clean Architecture Frame

Scaffolding facet of the architecture frame. Role and dependency rules: `.claude/rules/backend/architecture-style.md`; test-project references: `.claude/rules/backend-tests/test-projects.md`. Create only directories that contain real code.

## Domain

```text
backend/ProjectName.Domain/
├── Entities/
└── Enums/
```

Later additions such as `ValueObjects/`, `DomainServices/`, `Events/`, or `Exceptions/` appear only when an approved design needs them; business rules or workflow behavior alone do not justify DDD-oriented directories.

## Application

```text
backend/ProjectName.Application/
├── Abstractions/
│   ├── Persistence/          # IOrderRepository.cs, IUnitOfWork.cs — no persistence-technology types
│   └── ExternalServices/     # IEmailSender.cs, ICurrentUser.cs ... — only once such dependencies exist
├── Services/                 # IOrderService.cs, OrderService.cs (Application Services)
├── DTOs/                     # Application operation/data models when useful; not a dumping ground
├── Validation/               # FluentValidation validators for Application input/use-case rules
└── DependencyInjection.cs    # AddApplication(): Application services and validation only
```

Supporting type roles should be clear from the type name, its directory, or both. Prefer established suffixes: `Service` (use-case orchestration), `Dto`, `Request`/`Response` (Application operation contracts; HTTP contracts belong to Api), `Result`/`Outcome`, `Validator`, `Rules`/`Policy` (decision or workflow rules), `Factory`, `Mapper`, `Adapter`. Avoid ambiguous names such as `TaskWorkflow` when the role cannot be inferred (`TaskWorkflowRules`, `TaskWorkflowPolicy`, or `TaskWorkflowService` instead). Add responsibility-specific subdirectories only when a flat feature directory becomes hard to navigate, and avoid generic `Models`, `Helpers`, `Common`, or `Utils` buckets.

## Infrastructure

```text
backend/ProjectName.Infrastructure/
├── Persistence/              # persistence implementation; internal layout: persistence-change
├── Services/                 # EmailSender.cs, FileStorage.cs ... implementations of Application abstractions
└── DependencyInjection.cs    # AddInfrastructure(configuration): persistence, repositories, IUnitOfWork, adapters, HttpClient integrations, resilience handlers when used
```

Create capability-specific subdirectories under `Services/` when they improve cohesion.

## Api

```text
backend/ProjectName.Api/
├── Controllers/
├── Contracts/
│   ├── Requests/
│   └── Responses/
├── Middleware/               # only when custom middleware exists
├── Extensions/               # cohesive composition extensions; do not move code just to shorten Program.cs
├── Program.cs                # composition root: AddApplication(); AddInfrastructure(builder.Configuration)
├── appsettings.json
└── appsettings.Development.json
```

Controllers are the HTTP endpoint mechanism; create Minimal API endpoint groups only when explicitly requested. Api references Infrastructure only for composition — controllers never consume Infrastructure implementation types directly. Use `Contracts/` for transport-specific contracts only when separation from Application models provides value.

## Project references

```text
ProjectName.Domain          -> (no application project references)
ProjectName.Application     -> ProjectName.Domain
ProjectName.Infrastructure  -> ProjectName.Application, ProjectName.Domain
ProjectName.Api             -> ProjectName.Application, ProjectName.Infrastructure
```

Never add Domain → Application, Domain → Infrastructure, or Application → Infrastructure; reconsider the abstraction boundary instead.

## Backend test projects

Test projects live beside production projects under `backend/`; create only useful ones:

```text
backend/
├── ProjectName.Application.Tests/   # application-service/use-case behavior -> Application (+ Domain)
├── ProjectName.IntegrationTests/    # Api + Application + Infrastructure through the host -> Api
├── ProjectName.Domain.Tests/        # optional: only for non-trivial Domain behavior -> Domain
└── ProjectName.Infrastructure.Tests/ # optional: only for non-trivial Infrastructure behavior
```

A simple Domain of entities and enums needs no dedicated test project. Integration tests reference Api for `WebApplicationFactory<Program>` and exercise the other layers transitively. Test framework setup is the backend-testing facet's scaffolding step in `project-structure`.
