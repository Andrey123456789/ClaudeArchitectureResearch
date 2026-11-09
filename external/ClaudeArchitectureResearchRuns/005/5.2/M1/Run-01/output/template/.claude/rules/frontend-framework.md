---
paths:
  - "frontend/**/*"
---

> **Policy rule** · Capability: frontend/angular · Owns: Angular API style, Signals vs. RxJS, interceptors, RxJS subscription discipline · Scope: frontend · Loading: path (frontend workspace)

# Frontend Framework Rules

Framework-independent frontend rules: `frontend.md`. Technique, scaffold and
verify commands: the `angular` skill. Stack decisions: `docs/frontend-stack.md`.

## Angular APIs

- Default: use modern standalone Angular APIs (standalone components,
  provider-based configuration) for new code, and organize application code
  primarily by feature. Do not introduce NgModules for ordinary new feature work
  unless an integration or legacy dependency genuinely requires them.

## Signals and RxJS

- Default: use Signals for naturally synchronous, local UI state (with `computed`
  for derived state) and RxJS when asynchronous streams, HTTP composition,
  cancellation/switching, or event pipelines are clearer; avoid mechanical
  conversions between them.
- Default: avoid manual nested RxJS subscriptions; prefer composition operators
  when stream composition expresses the behavior clearly.
- When manually subscribing from Angular framework-managed code, tie the
  subscription lifetime to the component/service lifecycle using the project's
  current Angular facilities (for example `takeUntilDestroyed`).

## HTTP Interceptors

Default: prefer functional interceptors (`withInterceptors`) for new code and keep
interceptor responsibilities cross-cutting; do not put feature business logic in
an interceptor.
