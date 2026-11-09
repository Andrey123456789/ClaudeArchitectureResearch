---
paths:
  - "frontend/**/*"
---
> Level: 2-technology | Capability: frontend/angular (frontend.rules) | Owns: Angular framework rules | Scope: frontend | Loads: path (frontend files)

# Frontend Framework — Angular

- Default: modern standalone Angular APIs for new code, organized primarily by
  feature; do not introduce NgModules for ordinary new feature development
  unless an integration or legacy dependency genuinely requires them.
- Default: Signals for naturally synchronous, local UI state (`computed` for
  derived state) and RxJS where asynchronous streams, HTTP composition,
  cancellation, or event pipelines are clearer; do not convert between them
  mechanically.
- Default: functional interceptors for new code; interceptors stay
  cross-cutting and never carry feature business logic.
- Use reactive forms for non-trivial forms when explicit state, validation, and
  testability are useful. Frontend validation improves UX; it never replaces
  backend validation or data-integrity and security enforcement.
- Default: avoid manual nested RxJS subscriptions; use composition operators
  when they express the behavior clearly.
- A manual subscription from framework-managed code must be tied to the
  component or service lifecycle with the project's current Angular facilities
  (for example `takeUntilDestroyed` with `DestroyRef`).

Commands: `frontend.commands`. Technique: `angular`.
