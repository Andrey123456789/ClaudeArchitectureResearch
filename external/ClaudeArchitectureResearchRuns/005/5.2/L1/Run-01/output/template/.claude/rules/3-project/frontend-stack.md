---
paths:
  - "frontend/**/*"
---
> Level: 3-project | Capability: frontend/angular (frontend.decision) | Owns: selected frontend stack and default library limits | Scope: frontend | Loads: always (imported by CLAUDE.md)

# Frontend Stack

- Use the current stable Angular release supported by the selected Node.js
  environment, created with the current Angular CLI, with the TypeScript and
  RxJS versions the CLI selects as compatible; standalone APIs, strict mode,
  routing, zoneless mode when the selected stable version supports it, SCSS,
  Angular Material and Angular CDK, and Vitest as the test runner.
- Do not add NgRx, Axios, Lodash, Bootstrap, Tailwind, or additional form,
  component, or state-management libraries by default. Use built-in Angular
  capabilities first and add an extra library only for a concrete requirement.
- Playwright is the approved default when frontend E2E coverage is required; it
  is not part of the minimal baseline scaffold.
