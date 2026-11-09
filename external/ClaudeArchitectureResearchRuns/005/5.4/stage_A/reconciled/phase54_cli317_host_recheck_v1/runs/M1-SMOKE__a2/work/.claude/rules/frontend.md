---
paths:
  - "frontend/**/*"
---

> Path rule · Scope: frontend · Owns framework-independent frontend structure, presentation, HTTP boundary, error-contract, state, routing, and form-validation policy

# Frontend Rules

Framework-specific rules and role bindings: `.claude/rules/frontend-framework.md`.
Server-side authorization: `.claude/rules/security.md`.

## Structure

- Frontend structure stays feature-oriented: a feature owns its UI and its
  frontend-specific data-access logic. Avoid application-wide technical buckets
  (one global `components/`, `services/`, `models/` tree) and empty
  architecture folders; keep feature-specific code within its feature and keep
  `core` and `shared` relatively small.
- Use `shared` only for UI primitives or behavior that genuinely cross
  features; do not move feature code into `shared` merely because two
  components of one feature use it.

## Presentation

Keep pages and components focused on presentation and UI orchestration. Do not
move trivial presentation logic into services merely to make components
smaller.

## HTTP Boundary

Keep backend communication in explicit feature data-access services (the HTTP
boundary bound in `frontend-framework.md`); do not scatter HTTP calls through
presentation components. Use frontend API models that match the published HTTP
contract, and do not import backend Domain entities into the frontend.

## API Errors

Frontend code follows the documented API error contract. Centralize reusable
`ProblemDetails` parsing and mapping when practical, and do not infer business
behavior from arbitrary human-readable exception messages.

## State and Routing

- Prefer simple local component or service state before introducing a
  state-management library.
- By default, use route-level lazy loading for meaningful features; do not
  lazy-load every tiny component.

## Forms and Validation

Use the explicit form model bound in `frontend-framework.md` for non-trivial
forms when explicit state, validation, and testability are useful. Frontend
validation improves user experience but does not replace backend validation or
data-integrity and security enforcement.
