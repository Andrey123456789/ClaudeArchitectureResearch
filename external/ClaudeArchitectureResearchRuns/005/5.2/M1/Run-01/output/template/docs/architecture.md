> **Planning-time decision record** · Capability: architecture/clean-architecture · Owns: adopted architecture, stable-role mapping, patterns not adopted · Scope: backend · Loading: always (imported by `capability-selection.md`)

# Architecture

Adopted architecture (Decided): Clean Architecture is the default architectural
style for the backend. Layer rules live in `.claude/rules/architecture-style.md`
(loaded with backend code); the physical layout lives in the `project-structure`
workflow's `references/backend-layout.md`.

## Stable Role Mapping

Other capabilities and workflows use the stable role names; this frame binds them:

| Stable role | Binding in this architecture |
|---|---|
| domain layer | `backend/<Name>.Domain` |
| use-case layer | `backend/<Name>.Application` |
| use-case unit | Application Service |
| persistence-access contract | specific repository interface defined in Application |
| commit boundary | `IUnitOfWork` defined in Application, implemented in Infrastructure |
| adapter layer | `backend/<Name>.Infrastructure` (persistence and external-service implementations) |
| entry point | ASP.NET Core Controller in `backend/<Name>.Api` |
| composition root | `Program.cs` of `backend/<Name>.Api` |
| test-project role | `backend/<Name>.<Layer>.Tests`, `backend/<Name>.IntegrationTests` |

## Patterns Not Adopted

Do not introduce CQRS handlers, MediatR, Kommand, Vertical Slice Architecture, or
similar mediator-based organization unless explicitly approved (Reserved). A
service becoming too large is a signal to reconsider its responsibilities, not an
automatic reason to introduce another architectural pattern.
