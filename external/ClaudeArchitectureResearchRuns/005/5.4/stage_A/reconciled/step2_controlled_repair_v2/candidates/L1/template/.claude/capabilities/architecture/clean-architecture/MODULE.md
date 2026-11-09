> Level: 1-architecture · Capability: architecture/clean-architecture · Owns: implementation manifest (maintainer metadata) · Scope: backend · Loading: never auto-loaded

# Module: architecture/clean-architecture

Frame implementation: maps roles to `Domain` / `Application` / `Infrastructure` / `Api` projects, owns placement, Clean Architecture-specific layout and patterns not adopted, and supplies the architecture-check specification.

- binds: none
- leak-tokens: Clean Architecture
- frame-terms: Domain, Application, Infrastructure, Api, Tests, IntegrationTests, IUnitOfWork, IGenericRepository<T>, AddApplication, AddInfrastructure
- placement-examples: ITaskService, TaskService, TaskWorkflowRules, TaskWorkflowService, TaskWorkflow, IEmailSender, ICurrentUser, IFileStorage, EmailSender, FileStorage, PaymentGateway

## Facets

| Facet | File | Level | Loading |
| --- | --- | --- | --- |
| `architecture.style` | `.claude/rules/1-architecture/frame/adopted-style.md` | 1-architecture | always (imported by `CLAUDE.md`) |
| `architecture.boundaries` | `.claude/rules/1-architecture/frame/boundaries.md` | 1-architecture | path |
| `architecture.layout` | `.claude/capabilities/architecture/clean-architecture/layout.md` | 1-architecture | workflow-read |
| `architecture.check` | `.claude/capabilities/architecture/clean-architecture/check.json` | 1-architecture | enforcement data |

## Replacement notes

Replace all four facets together, keep `.claude/rules/1-architecture/roles.md` unchanged unless the role vocabulary itself changes (Reserved), and update the selection record row.
