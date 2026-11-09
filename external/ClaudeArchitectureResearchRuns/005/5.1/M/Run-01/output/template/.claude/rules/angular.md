---
paths:
  - "frontend/**/*"
---

> Owns: Angular structure, component responsibility, HTTP boundary, state and reactivity, routing, forms, frontend error handling | Scope: frontend | Loads: path

# Angular Rules

Frontend stack and library limits: `docs/technology-stack.md`. Server-side
authorization and browser credential rules: `security.md`. Technique and
examples: `angular` skill.

## Structure

- By default, use modern standalone Angular APIs for new code (no new NgModules
  without an integration or legacy reason) and organize application code
  primarily by feature.
- Keep feature-specific code inside its feature. Avoid application-wide
  technical buckets (global `components/`, `services/`, `models/`) and empty
  architecture folders; keep `core` and `shared` relatively small, and do not
  move code into `shared` merely because two components of one feature use it.

## Components

Pages and components stay focused on presentation and UI orchestration. Do not
move trivial presentation logic into services merely to shrink components.

## HTTP Boundary

- Keep backend communication in explicit feature data-access services or another
  explicit HTTP boundary; do not scatter `HttpClient` calls through presentation
  components, and never import backend Domain entities into Angular. Frontend
  API models match the published HTTP contract.
- Prefer functional interceptors for new code and keep interceptors cross-cutting;
  never put feature business logic in an interceptor.
- Follow the documented API error contract: centralize reusable `ProblemDetails`
  parsing when practical and never infer business behavior from arbitrary
  human-readable exception messages.

## State and Reactivity

- By default, use Signals for naturally synchronous, local UI state and RxJS when
  asynchronous streams, HTTP composition, cancellation, or event pipelines are
  clearer; do not convert between them mechanically.
- Prefer simple component/service state before introducing a state-management
  library.
- Avoid manual nested subscriptions; prefer composition operators when they
  express the behavior clearly.
- When subscribing manually from framework-managed code, tie the subscription
  lifetime to the component/service lifecycle using the project's current
  Angular facilities.

## Routing

Use route-level lazy loading for meaningful features by default; do not
lazy-load every tiny component.

## Forms

Use reactive forms for non-trivial forms when useful. Frontend validation
improves user experience but never replaces backend validation, data-integrity,
or security enforcement.
