---
paths:
  - "backend/**/*"
---

> Level: 1-architecture · Capability: architecture/clean-architecture · Facet: architecture.style · Owns: adopted backend architecture, role-to-project mapping, patterns not adopted · Scope: backend · Loading: always (imported by CLAUDE.md)

# Adopted Architecture

The backend follows Clean Architecture. Role vocabulary: `.claude/rules/1-architecture/roles.md`.

| Role | Project |
| --- | --- |
| domain model | `backend/<Name>.Domain` |
| use-case layer — use-case units (Application Services), persistence-access contracts, commit boundary (`IUnitOfWork`) | `backend/<Name>.Application` |
| implementation layer — persistence and external adapters | `backend/<Name>.Infrastructure` |
| entry point and composition root (`Program.cs`) | `backend/<Name>.Api` |
| test projects — use-case tests, host integration tests | `backend/<Name>.Application.Tests`, `backend/<Name>.IntegrationTests` (optional `.Domain.Tests`, `.Infrastructure.Tests`) |

Boundary rules load with backend files (`.claude/rules/1-architecture/frame/boundaries.md`); placement details: `architecture.layout`.

## Not adopted

Do not introduce CQRS command/query handlers, mediator libraries or mediator-based request dispatch, Vertical Slice Architecture, or similar mediator-based organization unless explicitly approved. A service growing too large is a signal to reconsider its responsibilities, not a reason to adopt another pattern.
