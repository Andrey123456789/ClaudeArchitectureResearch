---
paths:
  - "frontend/**/*"
---

> Kind: STD | Scope: frontend | Capability: — | Loading: path-scoped (frontmatter paths)

# Frontend Standard (framework-neutral)

The selected frontend framework adds its rules in `frontend-framework.md`.

## Structure

- Frontend structure must stay feature-oriented: no application-wide technical buckets (global `components/`, `services/`, `models/`) or empty architecture folders; feature-specific code stays inside its feature, and `core`/`shared` stay small.
- Pages and components must stay focused on presentation and UI orchestration; do not move trivial presentation logic into services merely to make components smaller.
- Default: route-level lazy loading for meaningful features; do not lazy-load every tiny component.
- Default: simple local, component, or feature-service state before introducing a state-management library.

## Backend communication

- Backend communication must live in explicit feature data-access services or another explicit HTTP boundary; never scatter HTTP calls through presentation components, and never import backend Domain types into the frontend — use frontend API models that match the published HTTP contract.
- Frontend code must follow the documented API error contract: centralize reusable `ProblemDetails` parsing when practical and never infer business behavior from arbitrary human-readable exception messages.

Technique: the frontend knowledge facet named in the decision register.
