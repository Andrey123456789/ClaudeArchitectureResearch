---
paths:
  - "frontend/**/*.ts"
  - "frontend/**/*.html"
  - "frontend/**/*.scss"
---

> Owns: Angular structure, component responsibility, HTTP boundary, state, routing, forms, interceptors, RxJS lifetime, API error handling | Scope: frontend | Loads: path-scoped (Angular source files)

# Angular Rules

Server-side authorization: `security.md`. Technique and examples: `angular`
skill.

## Structure

- Use modern standalone Angular APIs for new code and organize application code
  primarily by feature. Do not introduce NgModules for ordinary feature
  development unless an integration or legacy dependency genuinely requires
  them.
- Keep the structure feature-oriented: avoid application-wide technical buckets
  (global `components/`, `services/`, `models/`) and empty architecture
  folders, keep feature-specific code inside its feature, and keep `core` and
  `shared` relatively small.

## Components and State

- Keep pages and components focused on presentation and UI orchestration; do
  not move trivial presentation logic into services merely to shrink
  components.
- Use Signals for naturally synchronous, local UI state and RxJS when
  asynchronous streams, HTTP composition, cancellation, or event pipelines make
  it clearer; avoid mechanical conversions between them.
- Prefer simple component, signal, or feature-service state before introducing
  a state-management library.

## HTTP

- Keep backend communication in explicit feature data-access services or
  another explicit HTTP boundary. Do not scatter `HttpClient` calls through
  presentation components, and do not import backend Domain entities into the
  Angular project — use frontend API models that match the published HTTP
  contract.
- Prefer functional interceptors for new code; keep interceptor
  responsibilities cross-cutting and never put feature business logic in an
  interceptor.
- Follow the documented API error contract: centralize reusable `ProblemDetails`
  parsing where practical, and do not infer business behavior from arbitrary
  human-readable exception messages.

## Routing and Forms

- Use route-level lazy loading for meaningful features; do not lazy-load every
  tiny component.
- Use reactive forms for non-trivial forms when explicit state, validation, and
  testability are useful. Frontend validation improves the user experience but
  never replaces backend validation or data-integrity and security
  enforcement.

## RxJS

- Avoid manual nested subscriptions; prefer composition operators when stream
  composition expresses the behavior clearly.
- When manually subscribing from framework-managed code, tie the subscription
  lifetime to the component or service lifecycle using the project's current
  Angular facilities.
