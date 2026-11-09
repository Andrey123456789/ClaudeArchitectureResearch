---
paths:
  - "frontend/**/*"
---

> Level: 1 Architecture · Owns: frontend structural boundary — feature organization, presentation responsibility, HTTP boundary, state, error contract, validation role · Scope: frontend · Loads: path rule · Depends on: CLAUDE.md, .claude/rules/1-architecture/entry-points.md

# Frontend Structure

Framework bindings live in `.claude/rules/2-technology/`. Server-side authorization stays authoritative (`0-core/security-principles.md`).

## Organization

- Organize application code primarily by feature. Avoid application-wide technical buckets and empty architecture folders; keep feature-specific code within its feature and keep `core`/`shared` relatively small.
- Use route-level lazy loading for meaningful features; do not lazy-load every tiny component (default).

## Responsibilities

- Pages and components stay focused on presentation and UI orchestration; do not move trivial presentation logic into services merely to shrink components.
- Keep backend communication in explicit feature data-access services or another explicit HTTP boundary. Do not scatter HTTP calls through presentation components, and never import backend Domain types into the frontend; use frontend API models that match the published HTTP contract.
- Prefer simple local, component, or service state before introducing a state-management library (default).

## Errors and validation

- Frontend code follows the documented API error contract. Centralize reusable problem-details parsing when practical, and never infer business behavior from arbitrary human-readable exception messages.
- Frontend validation improves user experience but never replaces backend validation or data-integrity and security enforcement.
