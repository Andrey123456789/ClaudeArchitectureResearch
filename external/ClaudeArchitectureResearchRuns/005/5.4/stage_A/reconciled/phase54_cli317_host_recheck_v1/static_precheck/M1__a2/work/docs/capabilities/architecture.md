> Capability: architecture/clean-architecture · Always-loaded planning decisions (imported by `CLAUDE.md`) · Owns the adopted architecture, the role map, the repository layout, and the patterns not adopted

# Architecture Frame: Clean Architecture

Clean Architecture is the adopted architectural style (Decided). Layer and
boundary rules: `.claude/rules/architecture.md` (loads for backend code).
Physical placement for scaffolding: `project-structure` workflow.

## Role Map

Other instructions use these stable roles; this frame maps them to layers.

| Role | Mapping |
|---|---|
| core model | `<Name>.Domain` — entities, enums, genuine domain invariants |
| use-case layer | `<Name>.Application` — use-case orchestration and inward-facing contracts |
| use-case unit | Application Service |
| persistence-access contract | specific repository interface defined in `<Name>.Application` |
| commit boundary | `IUnitOfWork` defined in `<Name>.Application`, implemented in `<Name>.Infrastructure` |
| adapter layer | `<Name>.Infrastructure` — persistence and external-service implementations |
| entry point | ASP.NET Core Controller in `<Name>.Api` |
| composition root | `Program.cs` in `<Name>.Api` |
| test projects | `<Name>.Application.Tests` and `<Name>.IntegrationTests`; `<Name>.Domain.Tests` or `<Name>.Infrastructure.Tests` only when justified |

## Repository Layout

```text
backend/<Name>.<Layer>/     production projects and backend test projects
frontend/<Name>.Web/        frontend workspace (when the frontend slot is selected)
docs/                       maintained documentation and decision records
<repository root>           solution file, shared build files, instruction files
```

Keep backend production and test projects, the frontend workspace, and
documentation separated according to this layout. Backend test projects live
under `backend/` beside the production projects; do not create a separate
top-level `tests/` directory.

## Patterns Not Adopted

Not adopted (Decided); introducing any of them requires explicit approval:

- CQRS handlers, MediatR, Kommand, Vertical Slice Architecture, or similar
  mediator-based organization.

Other consequential patterns are Reserved through `CLAUDE.md` § Decision
Control.
