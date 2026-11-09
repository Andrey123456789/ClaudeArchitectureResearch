---
paths:
  - "frontend/**"
---

> Level: 1 Architecture · Owns: frontend structural boundary — features, presentation, data access, errors, validation role · Scope: frontend · Loads: path; read explicitly by `project-structure`

# Frontend Structure

- **Must** organize the application primarily by feature: a feature owns its UI and its frontend data access. Avoid application-wide technical buckets (`components/`, `services/`, `models/` for the whole app) and empty architecture folders; keep `core` and `shared` small, and use `shared` only for UI primitives or behavior that genuinely cross features — not as a dumping ground.
- **Must** keep pages and components focused on presentation and UI orchestration. Route-level pages coordinate; reusable presentation components receive data through explicit inputs and emit meaningful UI events. Do not move trivial presentation logic into services merely to shrink components.
- **Must** keep backend communication in explicit feature data-access services. Do not scatter HTTP calls through presentation components; use frontend API models that match the published HTTP contract and never import backend Domain entities into the frontend.
- **Must** follow the API's documented error contract: centralize reusable problem-details parsing where practical, and never infer business behavior by parsing human-readable error messages.
- **Must** treat frontend validation as user experience: it never replaces backend validation, data-integrity or security enforcement. Keep shared constraints synchronized with the backend for consistent messages.
- **Default:** lazy-load meaningful route-level features; do not lazy-load every small component.
- **Default:** start with component state, feature services and reactive composition before introducing a state-management library.
