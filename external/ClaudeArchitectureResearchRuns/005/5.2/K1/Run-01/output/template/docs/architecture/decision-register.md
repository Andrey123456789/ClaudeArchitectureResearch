Kind: DEC | Scope: common | Capability: — (capability entries name their module) | Loading: always (imported by CLAUDE.md)

# Decision Register

Every entry is **Decided**. Changing an entry, including a capability selection or provider variant, is Reserved: run `architecture-decision`, then record the accepted change here and in `docs/decisions/`.

## Approved stack

- Use the approved technologies listed in this register instead of silently selecting alternatives. Replacing one is Reserved.
- Backend platform: .NET 10 LTS on its latest stable servicing release, C# 14, ASP.NET Core and ASP.NET Core Controllers. Moving to a preview or RC .NET or C# release requires approval.
- Validation: FluentValidation with FluentValidation.DependencyInjectionExtensions is the standard library for explicit request and use-case validation.
- Logging: application code logs through `ILogger<T>`; Serilog (Serilog.AspNetCore) is the logging provider.
- API documentation and interactive testing: Swashbuckle.AspNetCore Swagger UI, served at `/swagger` in Development, is the default surface (not built-in `AddOpenApi()`/`MapOpenApi()`). Expose it outside Development only when deployment requirements justify it.

## Repository defaults

- Layout: `backend/<Name>.<Layer>/` holds the backend production projects and, beside them, the backend test projects. `frontend/<Name>.Web/` holds the frontend workspace, including its tests. `docs/` holds maintained documentation. Keep these clearly separated, do not create a top-level `tests/` directory, and create only what the project needs.
- Solution format: `.slnx`. Use a legacy `.sln` only when an external tool or project requirement needs it.
- Shared .NET build configuration: a repository-level `Directory.Build.props` for genuinely shared build settings and `Directory.Packages.props` for central package versions. Project-specific settings stay in their own projects.

## Conditional technologies

These are approved but added only when their capability is actually needed. Approved does not mean installed by default.

- Mapping: manual mapping for simple cases; Mapster with Mapster.DependencyInjection when mapping volume makes it worthwhile. Another mapping framework requires approval.
- Resilience: the Microsoft resilience packages, only when a real integration needs resilience behavior.
- Containers: Docker and container artifacts only when the project or its deployment actually needs them, never merely because the application can be containerized.
- Further conditional choices are listed per capability below.

## Capability selection

Static composition: exactly one implementation per required slot and zero or one for the optional slot. Unselected implementations are not present.

| Slot | Type | Selected (variant) | Knowledge facet | Module |
|---|---|---|---|---|
| architecture | required frame | clean-architecture | — | `.claude/capabilities/architecture/clean-architecture/` |
| persistence | required leaf | ef-core (sqlserver) | `ef-core` | `.claude/capabilities/persistence/ef-core/` |
| backend-testing | required leaf | nunit | `dotnet-testing` | `.claude/capabilities/backend-testing/nunit/` |
| frontend | optional leaf | angular | `angular` | `.claude/capabilities/frontend/angular/` |

Each module's `MODULE.md` lists all of its facets. Its workflow facet is `workflow-facet.md` in the module directory.

### architecture → clean-architecture

Capability: architecture/clean-architecture | Kind: DEC

- Adopted style: Clean Architecture with the layer roles Domain, Application, Infrastructure and Api. Declared properties: use-case orchestration through Application Services; commit boundary `IUnitOfWork`. Standards: `.claude/rules/backend/architecture-style.md`.
- Not adopted (introducing any of them requires approval): CQRS handlers, MediatR, Kommand, Vertical Slice Architecture or similar mediator-based organization.

### persistence → ef-core (sqlserver)

Capability: persistence/ef-core | Kind: DEC

- Persistence: EF Core with Microsoft SQL Server (`Microsoft.EntityFrameworkCore.SqlServer`). Provider-specific concerns stay out of Application and Domain.
- Declared properties: migration mechanism is EF Core migrations; Development seeding uses a dedicated Infrastructure seeder; database string comparison follows the column/database collation (the usual SQL Server default collations are case-insensitive), which is observable behavior. Binds the architecture frame (Infrastructure layer, commit boundary).

### backend-testing → nunit

Capability: backend-testing/nunit | Kind: DEC

- Backend tests use NUnit. ASP.NET Core integration tests use `WebApplicationFactory<Program>` (Microsoft.AspNetCore.Mvc.Testing) as the baseline. Testcontainers is conditional. Test projects follow the repository layout; the architecture frame places them.

### frontend → angular

Capability: frontend/angular | Kind: DEC

- Stack: current stable Angular with the CLI-selected compatible TypeScript and RxJS, standalone APIs, strict mode, routing, zoneless mode when the selected stable version supports it, SCSS, Angular Material and Angular CDK, and Vitest.
- Not added by default: NgRx, Axios, Lodash, Bootstrap, Tailwind, or additional form, component or state-management libraries. Use built-in Angular capabilities first and add an extra library only for a concrete need.
- Playwright is the approved tool when frontend E2E coverage is required. It is not part of the minimal scaffold.
