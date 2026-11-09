---
paths:
  - "frontend/**"
---
<!-- Kind: STD | Scope: frontend | Owns: Angular structure, components, state, HTTP boundary, error contract use, forms, RxJS lifetime | Loads: path-scoped (frontend/**) -->
# Frontend Angular Standards

Frontend stack: DEC-WEB-01; libraries not added by default: DEC-WEB-02. Package manifests: `rules/common/dependencies.md`.

## Structure

- **Default:** modern standalone Angular APIs for new code (no new NgModules for ordinary feature work unless an integration or legacy dependency requires them), with application code organized primarily by feature.
- Frontend structure **must** stay feature-oriented: avoid application-wide technical buckets (`components/`, `services/`, `models/` for the whole app) and empty architecture folders; keep feature-specific code inside its feature and keep `core` and `shared` relatively small — `shared` holds reusable UI primitives or behavior that genuinely cross features.
- **Default:** route-level lazy loading for meaningful features; do not lazy-load every tiny component.

## Components and State

- Pages and components **must** stay focused on presentation and UI orchestration, and **must not** move trivial presentation logic into services merely to make components smaller.
- **Default:** Signals for naturally synchronous, local UI state; RxJS when asynchronous streams, HTTP composition, cancellation or event pipelines are clearer; avoid mechanical conversions between the two.
- **Default:** simple local, component or service state before introducing a state-management library.

## HTTP Boundary and Errors

- Backend communication **must** live in explicit feature data-access services or another explicit HTTP boundary: no `HttpClient` calls scattered through presentation components, and no backend Domain entities imported into the Angular project — frontend API models match the published HTTP contract.
- **Default:** functional interceptors for new code, limited to cross-cutting responsibilities; no feature business logic in interceptors.
- Frontend code **must** follow the documented API error contract: centralize reusable `ProblemDetails` parsing when practical, and **never** infer business behavior from arbitrary human-readable exception messages.

## Forms and Validation

- Frontend validation **must** be treated as user experience only: it does not replace backend validation or data-integrity and security enforcement. Use reactive forms for non-trivial forms when useful; do not duplicate complex Domain rules in TypeScript unless the UI genuinely needs an equivalent user-facing rule.

## RxJS

- **Default:** avoid manual nested subscriptions and prefer composition operators when they express the behavior clearly.
- Manual subscriptions from framework-managed code **must** tie their lifetime to the component or service lifecycle using the project's current Angular facilities.

Technique: `angular` knowledge skill.
