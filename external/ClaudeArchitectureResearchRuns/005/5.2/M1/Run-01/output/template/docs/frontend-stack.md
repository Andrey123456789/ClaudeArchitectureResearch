> **Planning-time decision record** · Capability: frontend/angular · Owns: selected frontend technology baseline, default-excluded libraries, conditional E2E · Scope: frontend · Loading: always (imported by `capability-selection.md`)

# Frontend Stack

## Angular Baseline

Use the latest stable Angular release supported by the selected Node.js
environment at scaffolding time, created with the current Angular CLI:

- standalone APIs, strict mode, routing;
- zoneless mode when supported by the selected stable Angular version;
- SCSS;
- TypeScript and RxJS versions selected by the Angular CLI as mutually compatible
  (do not upgrade TypeScript beyond Angular's supported range);
- Angular Material and Angular CDK as the UI component baseline;
- Vitest as the unit/component test runner for new projects.

## Libraries Not Added by Default

Do not add NgRx, Axios, Lodash, Bootstrap, Tailwind, additional form frameworks,
additional component libraries, or additional state-management libraries by
default. Use built-in Angular capabilities first and add an overlapping library
only for a concrete requirement.

## Conditional E2E

Playwright is the approved default when frontend E2E coverage is required. It is
not part of the minimal baseline scaffold.
