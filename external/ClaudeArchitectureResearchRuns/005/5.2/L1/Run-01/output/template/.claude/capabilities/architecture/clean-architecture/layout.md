> Level: 1-architecture | Capability: architecture/clean-architecture (architecture.layout) | Owns: physical backend layout and placement used when scaffolding or adding code | Scope: backend | Loads: read when a workflow step names architecture.layout

# Clean Architecture — Physical Layout

Boundaries and references are governed by `layering.md` and
`role-boundaries.md`; this facet describes where things go. Create only
directories that contain real code — every tree below is a target shape, not a
list to pre-create.

## Domain — `backend/<Name>.Domain/`

```text
<Name>.Domain/
├── Entities/
└── Enums/
```

Later additions only when an approved design needs them: `ValueObjects/`,
`DomainServices/`, `Events/`, `Exceptions/`. Do not create DDD-oriented
directories merely because the domain contains business rules; DDD tactical
patterns follow decision control.

## Application — `backend/<Name>.Application/`

```text
<Name>.Application/
├── Abstractions/
│   ├── Persistence/          # I<Entity>Repository, IUnitOfWork
│   └── ExternalServices/     # IEmailSender, ICurrentUser, IFileStorage, ...
├── Services/                 # I<Feature>Service, <Feature>Service
├── DTOs/
├── Validation/               # request/use-case validators
└── DependencyInjection.cs    # AddApplication(): Application services + validators
```

- `Abstractions/Persistence` holds inward-facing persistence contracts;
  `Abstractions/ExternalServices` exists only once such dependencies exist.
- `Services` holds Application Services, the default use-case orchestration.
  Do not create handler/CQRS/mediator structures.
- `DTOs` holds Application-level operation and data models when useful — not a
  dumping ground.
- `DependencyInjection.cs` registers Application-owned services only, never
  concrete Infrastructure implementations.

### Supporting type roles

Within a feature or service area, make each supporting type's role clear from
its name, its directory, or both. Useful suffixes: `Service` (use-case
orchestration), `Dto`, `Request`/`Response` (Application operation contracts;
HTTP contracts belong to Api), `Result`/`Outcome`, `Validator`,
`Rules`/`Policy` (decision or workflow rules), `Factory`, `Mapper`, `Adapter`.
Prefer `TaskWorkflowRules`, `TaskWorkflowPolicy`, or `TaskWorkflowService` over
an ambiguous `TaskWorkflow`. Add responsibility-specific subdirectories only
when a feature accumulates enough heterogeneous types that a flat directory is
hard to navigate; avoid generic `Models`, `Helpers`, `Common`, or `Utils`.

## Infrastructure — `backend/<Name>.Infrastructure/`

```text
<Name>.Infrastructure/
├── Persistence/              # persistence implementation (internal structure: persistence.scaffold)
├── Services/                 # external-service adapters: EmailSender, FileStorage, ...
└── DependencyInjection.cs    # AddInfrastructure(configuration)
```

`Persistence/` is the named location `persistence implementation` that the
persistence capability fills. `DependencyInjection.cs` registers
Infrastructure-owned implementations: persistence registrations, repository
implementations, `IUnitOfWork`, external adapters, outbound HTTP clients, and
resilience handlers when used. Create capability-specific subdirectories under
`Services/` when they improve cohesion.

## Api — `backend/<Name>.Api/`

```text
<Name>.Api/
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

- Controllers are the HTTP endpoint mechanism; do not create Minimal API
  endpoint groups unless explicitly requested.
- `Contracts` holds transport request/response contracts when
  `role-boundaries.md` calls for them.
- Do not move arbitrary code out of `Program.cs` solely to shorten it.
- Typical composition:

```csharp
builder.Services.AddApplication();
builder.Services.AddInfrastructure(builder.Configuration);
```

## Backend test projects

```text
backend/
├── <Name>.Domain/
├── <Name>.Application/
├── <Name>.Application.Tests/      # use-case behavior
├── <Name>.Infrastructure/
├── <Name>.Api/
└── <Name>.IntegrationTests/       # host-level: Api + Application + Infrastructure
```

- `<Name>.Domain.Tests` only when the domain has non-trivial behavior worth
  testing independently; `<Name>.Infrastructure.Tests` only when infrastructure
  has non-trivial behavior that benefits from its own assembly.
- Integration tests reference the Api host (for `WebApplicationFactory<Program>`)
  and exercise Application and Infrastructure through it.
- Test-framework project setup: `backend-testing.scaffold`.

## Adding a project later

Procedure: `project-structure` ("Adding a project later"); classify the new
project in `check.json` so the architecture check recognizes it.
