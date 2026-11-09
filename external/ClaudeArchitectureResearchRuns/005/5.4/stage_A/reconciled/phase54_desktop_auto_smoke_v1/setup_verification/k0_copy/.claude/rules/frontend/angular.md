---
paths:
  - "frontend/**/*.ts"
  - "frontend/**/*.html"
  - "frontend/**/*.scss"
  - "frontend/**/*.css"
---

> Kind: STD | Scope: frontend | Owner: Angular application standards — structure, components, HTTP boundary, state, routing, forms, errors, RxJS, browser authentication security | Loading: path-scoped

# Angular Standard

Frontend stack: D-09. Libraries not added by default: D-10.

See also: `rules/common/security.md` (server-side authorization authority).

## Structure

- Default: modern standalone Angular APIs for new code (no NgModules for ordinary new features unless an integration or legacy dependency requires them), with application code organized primarily by feature.
- Structure must stay feature-oriented: no application-wide technical buckets (`components/`, `services/`, `models/`) that spread a feature across directories, no empty architecture folders; feature-specific code stays in its feature and `core`/`shared` stay small. Do not move code to `shared` merely because two components of the same feature use it.

## Components and data access

- Pages and components must stay focused on presentation and UI orchestration; do not move trivial presentation logic into services merely to shrink components.
- Backend communication must live in explicit feature data-access services or another explicit HTTP boundary: do not scatter `HttpClient` calls through presentation components, and never import backend Domain entities into Angular — frontend API models follow the published HTTP contract.
- Default: functional interceptors for new code, limited to cross-cutting concerns; never put feature business logic in an interceptor.

## State and reactivity

- Default: Signals for naturally synchronous, local UI state; RxJS when asynchronous streams, HTTP composition, cancellation or event pipelines express the behavior more clearly. Avoid mechanical conversions between them.
- Default: simple component, signal or feature-service state before any state-management library.
- Default: avoid manual nested RxJS subscriptions; prefer composition operators when they express the behavior clearly.
- A manual subscription from framework-managed code must have its lifetime tied to the component or service lifecycle using the project's current Angular facilities.

## Routing

- Default: route-level lazy loading for meaningful features; do not lazy-load every tiny component.

## Errors and forms

- Frontend code must follow the documented API error contract: centralize reusable `ProblemDetails` parsing when practical, and never infer business behavior from arbitrary human-readable exception messages.
- Use reactive forms for non-trivial forms when useful. Frontend validation is UX: backend validation, data integrity and security enforcement remain authoritative.

## Browser authentication security

- When browser cookies carry authentication credentials automatically, the design must include CSRF protection; do not assume an Angular frontend removes the risk.
- Choose browser token storage according to the application's threat model; never claim one storage mechanism is universally secure. Tokens are never logged (`rules/common/security.md` § Logging and sensitive data).
