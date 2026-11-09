---
paths:
  - "frontend/**"
---

> Level: 2 Technology · Owns: Angular, RxJS and npm workspace rules · Scope: frontend · Loads: path

# Angular

- **Default:** use modern standalone Angular APIs for new code — standalone components and provider-based configuration; do not introduce NgModules for ordinary new features unless an integration or legacy dependency genuinely requires them.
- **Default:** use Signals for naturally synchronous, local UI state (`computed` for derived state; avoid `effect()` when `computed`, template binding or explicit event handling is clearer), and RxJS where asynchronous streams, HTTP composition, cancellation or event pipelines are clearer. Do not convert between them mechanically.
- **Default:** use reactive forms for non-trivial forms where explicit state, validation and testability are useful.
- **Default:** prefer functional interceptors (`provideHttpClient(withInterceptors([...]))`) for new code; interceptors stay cross-cutting and never contain feature business logic.
- **Default:** avoid manual nested RxJS subscriptions; prefer composition operators.
- **Must** tie every manual subscription made from framework-managed code to the component or service lifecycle using the project's current Angular facilities (for example `takeUntilDestroyed`, `DestroyRef`, the `async` pipe).
- **Must not** use `npm --force` or `--legacy-peer-deps` merely to bypass incompatible peer dependencies; resolve the actual compatibility problem.

Technique: `angular` skill.
