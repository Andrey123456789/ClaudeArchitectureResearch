---
paths:
  - "frontend/**/*"
---

> **Policy rule** · Owns: framework-independent frontend structure, presentation focus, HTTP boundary, routing granularity, state, API error handling, forms and validation authority · Scope: frontend · Loading: path (frontend workspace)

# Frontend Rules

Framework-specific rules: the frontend rule facet; technique: the frontend
knowledge facet (both resolved in `docs/capability-selection.md`).

## Structure

- Organize frontend code around features; avoid application-wide technical
  buckets (global `components/`, `services/`, `models/`) and empty architecture
  folders. Keep feature-specific code inside its feature and keep `core` and
  `shared` relatively small; do not move feature code to `shared` merely because
  two components of the same feature use it.
- Default: use route-level lazy loading for meaningful features; do not lazy-load
  every tiny component.

## Presentation and Data Access

- Keep pages and components focused on presentation and UI orchestration; do not
  move trivial presentation logic into services merely to shrink components.
- Keep backend communication in explicit feature data-access services or another
  explicit HTTP boundary; do not scatter HTTP client calls through presentation
  components, and do not import backend Domain entities into the frontend —
  frontend API models follow the published HTTP contract.
- Default: prefer simple local, component, or service state (or a small feature
  store) before introducing a state-management library.

## API Errors

Frontend code follows the API's documented error contract; centralize reusable
`ProblemDetails` parsing/mapping when practical, and do not infer business
behavior from arbitrary human-readable exception messages.

## Forms and Validation

Use reactive (model-driven) forms for non-trivial forms when explicit state,
validation, and testability are useful. Frontend validation improves user
experience but does not replace backend validation or data-integrity/security
enforcement.
