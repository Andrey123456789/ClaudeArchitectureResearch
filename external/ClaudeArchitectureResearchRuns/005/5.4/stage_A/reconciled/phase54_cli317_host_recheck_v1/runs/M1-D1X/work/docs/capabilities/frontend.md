> Capability: frontend/angular · Optional slot · Always-loaded planning decisions (imported by `CLAUDE.md`) · Owns the frontend technology decisions

# Frontend: Angular

- Baseline (Decided): the latest stable Angular release supported by the
  selected Node.js environment, created with the current Angular CLI; TypeScript
  and RxJS at the versions the CLI selects as mutually compatible (do not
  upgrade TypeScript beyond Angular's supported range); standalone APIs; strict
  mode; routing; zoneless change detection when supported by the selected
  stable version; SCSS; Angular Material and Angular CDK; Vitest.
- Not added by default: NgRx, Axios, Lodash, Bootstrap, Tailwind, or additional
  form, component, or state-management libraries. Use built-in Angular
  capabilities first and add an extra library only for a concrete requirement.
- Conditional: Playwright is the approved default when frontend E2E coverage is
  required; it is not part of the minimal baseline scaffold.
- Rules: `.claude/rules/frontend.md` (framework-independent) and
  `.claude/rules/frontend-framework.md` (Angular-specific).
- Knowledge skill: `angular`.
