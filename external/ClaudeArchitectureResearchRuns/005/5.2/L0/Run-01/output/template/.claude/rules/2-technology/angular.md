---
paths:
  - "frontend/**"
---

> Level: 2 Technology | Owns: Angular API style, reactivity, routing, interceptors, subscription lifetime | Scope: frontend | Loads: path | Depends on: 1-architecture/frontend-structure.md, 0-core/security-principles.md

# Angular

- Default: use modern standalone Angular APIs for new code and organize
  application code primarily by feature; do not add NgModules for ordinary new
  features.
- Default: use Signals for naturally synchronous or local UI state and RxJS when
  asynchronous streams, HTTP composition, cancellation, or event pipelines are
  clearer; avoid mechanical conversions between them.
- Default: lazy-load meaningful route-level features; do not lazy-load every
  tiny component.
- Default: prefer functional interceptors for new code and keep interceptors
  cross-cutting; do not put feature business logic in interceptors.
- Default: avoid manual nested RxJS subscriptions; prefer composition operators
  when they express the behavior clearly.
- When manually subscribing from framework-managed code, tie the subscription
  lifetime to the component or service lifecycle using the project's current
  Angular facilities (for example `takeUntilDestroyed`).

## Bindings to Architecture and Security Rules

- `HttpClient` calls live in feature data-access services (the explicit HTTP
  boundary of `1-architecture/frontend-structure.md`).
- Route guards and hidden or disabled actions are UX only; server authorization
  stays authoritative.
- Default: use reactive forms for non-trivial forms when explicit state,
  validation, and testability are useful; they remain UX validation.

Technique: → `angular` skill.
