---
paths:
  - "frontend/**/*"
---

> Level: 3-project · Capability: frontend/angular · Facet: frontend.stack · Owns: selected frontend technology decisions · Scope: frontend · Loading: always (imported by CLAUDE.md)

# Frontend Stack

- Decided: current stable Angular (latest release supported by the selected Node.js environment at scaffolding time) created with the current Angular CLI, which selects mutually compatible TypeScript and RxJS versions; standalone APIs, strict mode, routing, zoneless mode when the selected stable version supports it, SCSS, Angular Material and Angular CDK, and Vitest as the unit-test runner.
- Do not add NgRx, Axios, Lodash, Bootstrap, Tailwind, or additional form, component, or state-management libraries by default; use built-in Angular capabilities first and add an overlapping library only for a concrete need.
- Default: Playwright is the approved E2E tool when frontend E2E coverage is required; it is not part of the minimal baseline scaffold.
