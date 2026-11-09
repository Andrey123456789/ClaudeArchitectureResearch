---
paths:
  - "frontend/**/*"
---
> Level: 1-architecture | Owns: framework-neutral frontend structure — features, HTTP boundary, state, routing, error contract | Scope: frontend | Loads: path (frontend files)

# Frontend Structure

Framework-specific rules come from the `frontend` selection (`frontend.rules`).

- Frontend structure must stay feature-oriented: do not organize the whole
  application into technical buckets (`components/`, `services/`, `models/`)
  that spread one feature across unrelated directories, and do not create empty
  architecture folders. Keep feature-specific code within its feature and keep
  `core`/`shared` small; do not move feature-specific code into `shared` merely
  because two components of the same feature use it.
- Pages and components must stay focused on presentation and UI orchestration;
  do not move trivial presentation logic into services merely to shrink
  components.
- Backend communication must stay in explicit feature data-access services or
  another explicit HTTP boundary; do not scatter HTTP calls through
  presentation components. Use frontend API models that match the published
  HTTP contract and never import backend domain-model types into the frontend.
- Frontend code follows the documented API error contract: centralize reusable
  `ProblemDetails` parsing when practical and never infer business behavior from
  arbitrary human-readable exception messages.
- Default: route-level lazy loading for meaningful features; do not lazy-load
  every tiny component.
- Default: simple local, component, or service state before introducing a
  state-management library.
