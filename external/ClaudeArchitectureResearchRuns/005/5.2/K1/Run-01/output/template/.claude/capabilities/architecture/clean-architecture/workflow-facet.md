Kind: WF | Scope: backend | Capability: architecture/clean-architecture | Loading: read by `project-structure` and `development-workflow` when placing backend code

# Workflow Facet: architecture / clean-architecture

Placement procedures for the Clean Architecture frame. Before using them, read `.claude/rules/backend/architecture-style.md` and `.claude/rules/backend/architecture.md` if they are not loaded. Create only projects and directories that hold real code.

## Backend projects

Target organization (not a requirement to create every project immediately):

```text
backend/
    <Name>.Domain/
    <Name>.Application/
    <Name>.Application.Tests/
    <Name>.Infrastructure/
    <Name>.Api/
    <Name>.IntegrationTests/
```

### Create the production projects

```bash
dotnet new classlib -n <Name>.Domain -o backend/<Name>.Domain
dotnet new classlib -n <Name>.Application -o backend/<Name>.Application
dotnet new classlib -n <Name>.Infrastructure -o backend/<Name>.Infrastructure
dotnet new webapi --use-controllers -n <Name>.Api -o backend/<Name>.Api
dotnet sln <Name>.slnx add backend/<Name>.Domain backend/<Name>.Application backend/<Name>.Infrastructure backend/<Name>.Api
```

- Remove properties from the generated project files that `Directory.Build.props` already provides (`TargetFramework`, `Nullable`, `ImplicitUsings`), and remove generated placeholder classes.
- Do not create Minimal API endpoint groups unless explicitly requested.

### Add project references

Add only the references that the dependency-direction standard allows (`architecture-style.md` → Dependency direction), for example:

```bash
dotnet add backend/<Name>.Application reference backend/<Name>.Domain
dotnet add backend/<Name>.Infrastructure reference backend/<Name>.Application backend/<Name>.Domain
dotnet add backend/<Name>.Api reference backend/<Name>.Application backend/<Name>.Infrastructure
```

After any project-reference change, run `node .claude/scripts/check-architecture.mjs`. The machine-readable reference rules are in `.claude/scripts/facets/architecture/enforcement.json`.

## Directories per layer

Create a directory only when it contains real code.

### Domain

```text
<Name>.Domain/
    Entities/
    Enums/
```

`ValueObjects/`, `DomainServices/`, `Events/` or `Exceptions/` appear only when an approved design justifies them. DDD-oriented directories are not created merely because the Domain has business rules.

### Application

```text
<Name>.Application/
    Abstractions/
        Persistence/          repository contracts and IUnitOfWork (persistence port, commit boundary)
        ExternalServices/     Application-owned abstractions such as IEmailSender, ICurrentUser, IFileStorage
    Services/                 Application Services and their public contracts (ITaskService, TaskService)
    DTOs/                     Application-level operation/data models, when useful
    Validation/               FluentValidation validators for Application input and use-case rules
    DependencyInjection.cs    AddApplication(): Application services and validation only
```

`Abstractions/ExternalServices/` is created only when such a dependency exists. `DependencyInjection.cs` never registers concrete Infrastructure implementations. `DTOs/` is not a dumping ground.

### Infrastructure

```text
<Name>.Infrastructure/
    Persistence/              persistence area: internal layout from the persistence workflow facet;
        Repositories/         concrete repository implementations live here
    Services/                 external adapters implementing Application abstractions (EmailSender, FileStorage)
    DependencyInjection.cs    AddInfrastructure(configuration): persistence, repositories, IUnitOfWork, adapters, HttpClient integrations
```

Use capability-specific subdirectories under `Services/` when they improve cohesion.

### Api

```text
<Name>.Api/
    Controllers/
    Contracts/
        Requests/
        Responses/
    Middleware/               only when custom middleware exists
    Extensions/               cohesive API/composition extension methods
    Program.cs
    appsettings.json
    appsettings.Development.json
```

`Contracts/` is used when transport-specific contracts give a boundary benefit. Do not move arbitrary code out of `Program.cs` merely to make it shorter. Typical composition:

```csharp
builder.Services.AddApplication();
builder.Services.AddInfrastructure(builder.Configuration);
```

## Port templates

```csharp
public interface IOrderRepository
{
    Task<Order?> GetByIdAsync(Guid id, CancellationToken cancellationToken);

    Task AddAsync(Order order, CancellationToken cancellationToken);
}

public interface IUnitOfWork
{
    Task<int> SaveChangesAsync(CancellationToken cancellationToken = default);
}
```

The persistence knowledge facet shows how the persistence leaf implements these ports.

## Supporting type roles

Within a feature or service area, the responsibility of each supporting type should be clear from its name, its directory, or both. Established suffixes:

- `Service` for use-case orchestration;
- `Dto` for data-transfer models;
- `Request` / `Response` for Application operation contracts (transport-specific HTTP contracts belong to Api);
- `Result` / `Outcome` for operation results;
- `Validator` for validation;
- `Rules` / `Policy` for decision or workflow rules;
- `Factory` for object creation, `Mapper` for mapping, `Adapter` for boundary adaptation.

Avoid names whose architectural role cannot be inferred without opening the file (prefer `TaskWorkflowRules` or `TaskWorkflowService` over `TaskWorkflow`). Add responsibility-specific subdirectories only when a feature accumulates enough heterogeneous types that a flat directory becomes hard to navigate.

## Test-project placement

Backend test projects live in `backend/` beside the production projects.

| Project | References | Purpose |
|---|---|---|
| `<Name>.Application.Tests` | Application (Domain as needed) | application-service and use-case behavior |
| `<Name>.IntegrationTests` | Api | API + Application + Infrastructure through the host (`WebApplicationFactory<Program>`) |
| `<Name>.Domain.Tests` (optional) | Domain | only when Domain contains non-trivial behavior worth testing independently |
| `<Name>.Infrastructure.Tests` (optional) | Infrastructure, narrower as required | only when Infrastructure has non-trivial behavior that benefits from its own assembly |

Create test projects with the backend-testing workflow facet. Place its architecture-conformance adapter in `<Name>.IntegrationTests/Architecture/`.

## Adding a project later

1. Determine whether a new assembly is justified; adding a production project is Reserved.
2. Identify its architectural or technical responsibility.
3. Add only the minimum references, preserving the dependency direction.
4. Extend the role map in `.claude/scripts/facets/architecture/enforcement.json` only as part of the approved decision.
5. Update shared build or package configuration when needed.
6. Build, test and run `node .claude/scripts/check-architecture.mjs`.

## Reorganizing an existing solution

1. Inspect the current tree and project references.
2. Identify a concrete structural problem; do not force an established project to match this layout without concrete value.
3. Preserve behavior and move code in small, reviewable steps.
4. Update namespaces and references consistently, without unrelated feature work.
5. Verify after restructuring.
