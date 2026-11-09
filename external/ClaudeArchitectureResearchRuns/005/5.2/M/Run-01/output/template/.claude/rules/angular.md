---
paths:
  - "frontend/**"
---

> Path-scoped rule. Owns: Angular structure, component responsibility, the frontend HTTP boundary, interceptors, API error-contract use, state and reactivity, routing, forms · Scope: frontend · Loads: when files in the frontend workspace are in context · Depends on: CLAUDE.md, docs/technology-stack.md

# Angular Rules

Server-authoritative authorization and browser-credential rules: `security.md`.
Technique and examples: `angular` skill.

## Structure

- Default: modern standalone Angular APIs for new code — no new NgModules
  unless an integration or legacy dependency genuinely requires them — with
  application code organized primarily by feature.
- Frontend structure must stay feature-oriented: avoid application-wide
  technical buckets (`components/`, `services/`, `models/` for the whole app)
  and empty architecture folders; keep feature-specific code inside its feature
  and keep `core` and `shared` small. Do not move feature-specific code into
  `shared` merely because two components of the same feature use it.

## Components

- Pages and components must stay focused on presentation and UI orchestration;
  do not move trivial presentation logic into services merely to make
  components smaller.

## HTTP Boundary

- Keep backend communication in explicit feature data-access services or
  another explicit HTTP boundary. Do not scatter `HttpClient` calls through
  presentation components, and do not import backend Domain entities into the
  Angular project; frontend API models match the published HTTP contract.
- Default: functional interceptors for new code, with cross-cutting
  responsibilities only; do not put feature business logic in an interceptor.
- Frontend code must follow the documented API error contract: centralize
  reusable `ProblemDetails` parsing when practical, and do not infer business
  behavior from arbitrary human-readable exception messages.

## State and Reactivity

- Default: Signals for naturally synchronous, local UI state; RxJS when
  asynchronous streams, HTTP composition, cancellation, or event pipelines are
  the clearer model. Avoid mechanical conversions between the two.
- Default: simple component, signal, or feature-service state before
  introducing a state-management library.
- Default: avoid manual nested RxJS subscriptions; compose with operators when
  stream composition expresses the behavior clearly.
- When subscribing manually from framework-managed code, tie the subscription
  lifetime to the component or service lifecycle using the project's current
  Angular facilities.

## Routing

- Default: route-level lazy loading for meaningful features; do not lazy-load
  every tiny component.

## Forms

- Frontend validation improves user experience but must not replace backend
  validation or data-integrity and security enforcement. Use reactive forms for
  non-trivial forms when explicit state, validation, and testability are useful.
