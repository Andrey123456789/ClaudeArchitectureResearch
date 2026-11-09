> **Private reference** of `project-structure` · Capability: architecture/clean-architecture · Owns: backend project layout technique, directory trees, type-role naming heuristics · Scope: backend, backend-tests · Loading: on demand (read by `project-structure`)

# Backend Layout

This reference defines the default physical structure of the ASP.NET Core
backend.

Architectural behavior is governed by `.claude/rules/architecture-style.md`.

# Domain

```text
backend/
└── ProjectName.Domain/
    ├── Entities/
    └── Enums/
```

Create additional directories only when the Domain actually needs them.

Possible later additions, when justified by the approved design, include:

```text
ValueObjects/
DomainServices/
Events/
Exceptions/
```

Do not create DDD-oriented directories merely because the Domain contains
business rules or workflow behavior.

Introducing DDD tactical patterns is Reserved (`CLAUDE.md` → Decision Control).

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

Contains inward-facing persistence contracts:

```text
ITaskRepository.cs
IOrderRepository.cs
IUnitOfWork.cs
```

Do not expose persistence-technology types here.

## `Abstractions/ExternalServices`

Contains Application-owned abstractions implemented by outer layers when needed:

```text
IEmailSender.cs
ICurrentUser.cs
IFileStorage.cs
IPaymentGateway.cs
```

Do not create this directory before such dependencies exist.

## `Services`

Contains Application Services and useful public service contracts:

```text
ITaskService.cs
TaskService.cs
```

Application Services are the default use-case orchestration mechanism.

Do not create handler/CQRS/MediatR structures by default.

### Supporting Type Roles

Within a feature/service area, the responsibility of each supporting type should
be clear from its type name, its immediate directory, or both.

Prefer established responsibility suffixes where applicable, for example:

- `Service` for use-case orchestration services;
- `Dto` for data-transfer models;
- `Request` / `Response` for Application operation contracts; transport-specific
  HTTP contracts belong to the API layer;
- `Result` / `Outcome` for operation results;
- `Validator` for validation;
- `Rules` / `Policy` for decision or workflow rules;
- `Factory` for object creation;
- `Mapper` for mapping;
- `Adapter` for boundary adaptation.

Avoid ambiguous names such as `TaskWorkflow` when the type's architectural role
cannot be inferred without opening the file. Prefer a more explicit name such as
`TaskWorkflowRules`, `TaskWorkflowPolicy`, or `TaskWorkflowService` according to
its actual responsibility.

Use responsibility-specific subdirectories when a feature accumulates enough
heterogeneous supporting types that a flat directory becomes difficult to
navigate.

Do not create subdirectories merely to classify one or two files when their
roles are already obvious from their names.

Avoid generic `Models`, `Helpers`, `Common`, or `Utils` buckets when a more
specific responsibility can be named.

## `DTOs`

Contains Application-level operation/data models when useful.

Do not make this a generic dumping ground.

## `Validation`

Contains FluentValidation validators for Application-level input/use-case
validation when such validators are required.

Do not move Domain invariants into FluentValidation merely because the library
is part of the approved stack.

## `DependencyInjection.cs`

Registers Application-owned services and Application-level validation
infrastructure (`architecture-style.md` → Registration).

# Infrastructure

```text
backend/
└── ProjectName.Infrastructure/
    ├── Persistence/
    │   ├── Repositories/
    │   └── ...            persistence-technology artifacts (persistence knowledge facet)
    ├── Services/
    └── DependencyInjection.cs
```

## Persistence

`Persistence/` contains the commit-boundary implementation (`UnitOfWork.cs`),
concrete repository implementations (`Repositories/`), and the persistence
technology's own artifacts — context, mappings, migrations, and development
seeding — laid out as the persistence knowledge facet describes.

An Infrastructure-only generic repository base is allowed when it removes real
duplication.

## Services

Contains technical/external implementations of Application abstractions.

Examples:

```text
EmailSender.cs
FileStorage.cs
PaymentGateway.cs
```

Create capability-specific subdirectories when they improve cohesion.

## `DependencyInjection.cs`

Registers Infrastructure-owned implementations and technical dependencies such
as:

```text
persistence context and provider
repository implementations
IUnitOfWork
external adapters
HttpClient integrations
resilience handlers when used
```

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

## Controllers

ASP.NET Core Controllers are the default HTTP endpoint mechanism.

Keep Controllers thin.

Do not create Minimal API endpoint groups unless explicitly requested.

## Contracts

Use transport-specific request/response contracts when separation from
Application models provides value.

Duplication limits: `architecture-style.md` → Transport Contracts.

## Middleware

Create only when custom middleware actually exists.

## Extensions

Use for cohesive API/composition extension methods.

Do not move arbitrary code out of `Program.cs` solely to make `Program.cs`
shorter.

## Program.cs

API is the composition root.

Typical composition includes:

```csharp
builder.Services.AddApplication();
builder.Services.AddInfrastructure(builder.Configuration);
```

Reference and Controller boundaries: `architecture-style.md` → Dependency
Direction and API.

# Backend Test Projects

Backend tests live under `backend/` alongside production projects.

Typical structure:

```text
backend/
├── ProjectName.Domain/
├── ProjectName.Application/
├── ProjectName.Application.Tests/
├── ProjectName.Infrastructure/
├── ProjectName.Api/
└── ProjectName.IntegrationTests/
```
Create only useful test projects.

`ProjectName.Domain.Tests` may be added when Domain contains non-trivial behavior
worth testing independently.

`ProjectName.Infrastructure.Tests` may be added when Infrastructure contains
non-trivial behavior that benefits from a dedicated test assembly.

The repository layout decision (`docs/technology-stack.md`) keeps backend tests
under `backend/`.

# Project References

The project-reference graph is defined in `architecture-style.md` → Dependency
Direction and checked by `node .claude/scripts/check-architecture.mjs`.

# Test References

Test-project references: `architecture-style.md` → Test Projects.
