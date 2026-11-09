---
paths:
  - "frontend/**"
---
Kind: STD | Scope: frontend | Capability: — | Loading: path-scoped (frontend/**)

# Frontend Standards (framework-neutral)

Framework bindings (data-access services, form mechanism, HTTP pipeline, lazy loading, reactive primitives): `.claude/rules/frontend/frontend-framework.md`. Technique: the frontend knowledge facet (decision register → Capability selection).

## Structure

- Frontend structure stays feature-oriented. Avoid application-wide technical buckets (`components/`, `services/`, `models/` for the whole application) and empty architecture folders. Feature-specific code stays inside its feature, and `core` and `shared` stay relatively small, holding only genuinely cross-feature code.
- Pages and components stay focused on presentation and UI orchestration. Do not move trivial presentation logic into services merely to make components smaller.
- Default: lazy-load meaningful route-level features. Do not lazy-load every tiny component.
- Default: prefer simple local, component or service state before introducing a state-management library.

## Backend communication

- Keep backend communication in explicit feature data-access services. Do not scatter HTTP client calls through presentation components, and do not import backend Domain entities; use frontend API models that match the published HTTP contract.
- Frontend code follows the documented API error contract. Centralize reusable `ProblemDetails` parsing when practical, and never infer business behavior from arbitrary human-readable exception messages.
- Use the framework's structured form mechanism for non-trivial forms when it is useful. Frontend validation improves user experience but never replaces backend validation, data-integrity or security enforcement.

## Browser security

- When browser cookies automatically carry authentication credentials, include CSRF protection in the design. A single-page frontend does not remove that risk.
- Do not claim that any browser token-storage mechanism is universally secure. Choose storage according to the application's threat model, and never log tokens.
