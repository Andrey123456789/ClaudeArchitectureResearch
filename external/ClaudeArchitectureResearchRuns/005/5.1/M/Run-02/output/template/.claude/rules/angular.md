---
paths:
  - "frontend/**/*"
---

> Owner: Angular application structure, component responsibility, HTTP boundary, reactive state, routing, interceptors, frontend error and form handling | Scope: frontend | Loads: path (frontend workspace); read explicitly by `project-structure`, `code-review`, `build-fix` | Enforced: `code-review` frontend checks

# Angular Rules

Technique and examples: `angular` skill. Server-side authorization, CSRF, and
token storage: `.claude/rules/security.md`.

## Structure

- Default: use modern standalone Angular APIs for new code and organize
  application code primarily by feature.
- Avoid application-wide technical buckets (global `components/`, `services/`,
  `models/` folders) and empty architecture folders; keep feature-specific code
  inside its feature and keep `core` and `shared` relatively small.

## Components

- Keep pages and components focused on presentation and UI orchestration; do not
  move trivial presentation logic into services merely to make components
  smaller.

## HTTP and Errors

- Keep backend communication in explicit feature data-access services or another
  explicit HTTP boundary; do not scatter `HttpClient` calls through presentation
  components, and do not import backend Domain entities into the Angular project.
- Default: functional interceptors for new code, with cross-cutting
  responsibilities only; no feature business logic in interceptors.
- Follow the documented API error contract: centralize reusable `ProblemDetails`
  parsing where practical, and do not infer business behavior from arbitrary
  human-readable error messages.

## Reactive State

- Default: Signals for naturally synchronous, local UI state; RxJS where
  asynchronous streams, HTTP composition, cancellation, or event pipelines make
  it clearer; no mechanical conversion between the two.
- Default: avoid manual nested subscriptions; prefer composition operators where
  they express the behavior clearly.
- When subscribing manually from framework-managed code, tie the subscription
  lifetime to the component or service lifecycle using the project's current
  Angular facilities.
- Default: simple component, signal, or feature-service state before introducing
  a state-management library.

## Routing and Forms

- Default: route-level lazy loading for meaningful features; do not lazy-load
  every tiny component.
- Use reactive forms for non-trivial forms when useful. Frontend validation
  improves UX but does not replace backend validation or data-integrity and
  security enforcement.
