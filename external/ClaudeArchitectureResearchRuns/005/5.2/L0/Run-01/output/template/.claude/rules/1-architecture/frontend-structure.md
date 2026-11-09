---
paths:
  - "frontend/**"
---

> Level: 1 Architecture | Owns: frontend structural boundary (presentation, data access, feature organization, state, error contract, validation authority) | Scope: frontend | Loads: path | Depends on: 1-architecture/overview.md

# Frontend Structure

- Pages and components stay focused on presentation and UI orchestration; do
  not move trivial presentation logic into services merely to shrink
  components.
- Keep backend communication in explicit feature data-access services or
  another explicit HTTP boundary; do not scatter HTTP calls through
  presentation components, and do not import backend Domain types into the
  frontend. Frontend API models match the published HTTP contract.
- Keep the structure feature-oriented: avoid application-wide technical
  buckets and empty architecture folders, keep feature-specific code inside its
  feature, and keep `core` and `shared` small.
- Default: prefer simple local, component, or feature-service state before
  introducing a state-management library.
- Frontend code follows the documented API error contract; centralize reusable
  `ProblemDetails` parsing when practical, and do not infer business behavior
  from human-readable exception messages.
- Frontend validation improves user experience but does not replace backend
  validation or data-integrity and security enforcement.

Do not apply backend project-boundary rules mechanically to frontend code.

Frontend technology bindings: → `2-technology/angular.md`.
