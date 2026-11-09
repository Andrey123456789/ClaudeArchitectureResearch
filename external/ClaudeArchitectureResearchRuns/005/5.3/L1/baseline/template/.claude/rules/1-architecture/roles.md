---
paths:
  - "backend/**/*"
---

> Level: 1-architecture · Owns: stable role vocabulary and frame-independent boundary rules · Scope: backend · Loading: path

# Architecture Roles and Boundaries

## Role vocabulary

The selected architecture frame maps each role to a concrete project (imported adopted-architecture rule). Instructions outside the frame use these roles instead of frame-specific layer names.

| Role | Meaning |
| --- | --- |
| domain model | business concepts and genuinely domain-owned invariants; the innermost role |
| use-case layer | coordinates application use cases and owns the abstractions they need |
| use-case unit | the default orchestration unit for one use case |
| persistence-access contract | inward-facing persistence interface shaped by use-case needs (repository) |
| commit boundary | the use-case-layer abstraction through which a use case commits its changes |
| implementation layer | implements use-case abstractions with concrete technology: persistence, external adapters, caches |
| entry point | HTTP-facing adapter that binds input, invokes use-case units, and maps outcomes to HTTP |
| composition root | startup code that registers implementations |
| test-project role | the purpose of a test project (use-case tests, host integration tests), which bounds its references |

## Boundaries

- HTTP status codes and transport response semantics belong to the entry point; the use-case layer and domain model must not return `IActionResult` or ASP.NET Core status codes.
- Default: represent common expected outcomes explicitly when useful (`null`, `bool`, a typed outcome), but do not force a generic `Result<T>` pattern and do not name use-case outcome categories after HTTP (`BadRequest`, `Unauthorized`, `Forbidden`); the entry point maps outcomes such as `Validation`, `NotFound`, or `Conflict` to HTTP.
- Keep cache technology out of the domain model, and do not leak infrastructure cache APIs into the use-case layer without a deliberate boundary abstraction.
- The implementation layer translates remote HTTP responses into use-case-layer abstractions; `HttpResponseMessage` and other remote transport concerns must not leak into the use-case layer.
- Do not create separate domain or persistence models merely because the public API has several versions; isolate version-specific transport contracts at the entry point when practical.
