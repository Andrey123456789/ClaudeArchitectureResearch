> Level: 1-architecture · Capability: architecture/clean-architecture · Owns: implementation manifest (maintainer metadata) · Scope: backend · Loading: never auto-loaded

# Module: architecture/clean-architecture

Clean Architecture frame implementation: maps roles to `Domain` / `Application` / `Infrastructure` / `Api` projects, owns placement, Clean Architecture-specific layout and patterns not adopted, and supplies the architecture-check specification.

- binds: none
- leak-tokens: Clean Architecture
- frame-terms: Domain, Application, Infrastructure, Api, IUnitOfWork, IGenericRepository, Application Services, AddApplication, AddInfrastructure, Persistence/
- placement-examples: ExternalServices/, ValueObjects/, DomainServices/, DependencyInjection, ITaskService, TaskService, IEmailSender, ICurrentUser, IFileStorage, EmailSender, FileStorage, PaymentGateway, TaskWorkflow, TaskWorkflowRules, TaskWorkflowService

## Facets

| Facet | File | Level | Loading |
| --- | --- | --- | --- |
| `architecture.style` | `.claude/rules/1-architecture/frame/adopted-style.md` | 1-architecture | always (imported by `CLAUDE.md`) |
| `architecture.boundaries` | `.claude/rules/1-architecture/frame/boundaries.md` | 1-architecture | path |
| `architecture.layout` | `.claude/capabilities/architecture/clean-architecture/layout.md` | 1-architecture | workflow-read |
| `architecture.check` | `.claude/capabilities/architecture/clean-architecture/check.json` | 1-architecture | enforcement data |
| `architecture.enforcement` | `.claude/capabilities/architecture/clean-architecture/enforcement.json` | 2-technology | enforcement data |

## Replacement notes

Replace all facets together, keep `.claude/rules/1-architecture/roles.md` unchanged unless the role vocabulary itself changes (Reserved), and update the selection record row. `frame-terms` lists the vocabulary that only this frame defines: a leaf module whose artifacts use any of it must declare `binds: architecture/clean-architecture`, and a replacement frame lists its own terms. `placement-examples` lists the illustrative project-owned names (folders, registration file, example types) used by the placement examples; they are accepted only where the layout facet places them, and never as technology vocabulary.
