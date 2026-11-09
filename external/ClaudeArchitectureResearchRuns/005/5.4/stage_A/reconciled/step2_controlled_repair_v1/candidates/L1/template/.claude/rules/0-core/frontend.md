---
paths:
  - "frontend/**/*"
---

> Level: 0-core · Owns: framework-neutral frontend structure, HTTP boundary, state, error contract, form validation · Scope: frontend · Loading: path

# Frontend Rules

- Keep pages and components focused on presentation and UI orchestration; do not move trivial presentation logic into services merely to shrink components.
- Keep backend communication in explicit feature data-access services; do not scatter HTTP client calls through presentation components, and never import backend domain or persistence types into the frontend.
- Frontend structure stays feature-oriented: avoid application-wide technical buckets and empty architecture folders, keep feature-specific code inside its feature, and keep `core`/`shared` small.
- Default: use route-level lazy loading for meaningful features; do not lazy-load every tiny component.
- Default: prefer simple local, component, or service state before introducing a state-management library.
- Follow the documented API error contract: centralize reusable problem-details parsing when practical and never infer business behavior from human-readable exception messages.
- Use reactive forms for non-trivial forms when explicit state, validation, and testability help. Frontend validation improves UX but must never replace backend validation or data-integrity and security enforcement.

Framework binding: `frontend.framework` (when a frontend implementation is selected). Server-side authorization: security rules.
