> Level: 2-technology · Capability: frontend/angular · Facet: frontend.commands · Owns: frontend scaffold, install, build, test, audit commands and build-fix notes · Scope: frontend · Loading: read by `project-structure`, `verify`, `build-fix`, `development-workflow`, `security-scan`

# Angular Commands

Workspace: `frontend/<Name>.Web/`. Run commands from the workspace directory. Install packages only through `add-dependency`.

## Scaffold

Create the workspace with the current Angular CLI using the baseline from the frontend stack rule: standalone APIs, routing, SCSS, strict mode, zoneless mode when supported. Confirm the exact flags of the installed CLI with `ng new --help` rather than from memory.

```bash
npx @angular/cli@latest new <Name>.Web --directory frontend/<Name>.Web --routing --style=scss --strict
ng add @angular/material
```

Let the CLI choose compatible TypeScript and RxJS versions; do not upgrade TypeScript beyond Angular's supported range independently.

## Everyday commands

| Purpose | Command |
| --- | --- |
| clean install from lockfile (CI, fresh clone) | `npm ci` |
| build | `npm run build` |
| unit tests | the `test` script in `package.json` (Vitest for new workspaces) |
| lint | the `lint` script, only when configured |
| dependency audit | `npm audit` |
| E2E (only when required) | Playwright inside the workspace, for example `frontend/<Name>.Web/e2e/` |

Inspect `package.json` before running anything: use scripts that exist and never invent script names.

## Build-fix notes

Common failure categories: TypeScript type error, template compilation error, DI/provider error, invalid standalone import, route configuration error, signal/RxJS typing issue, missing package, Angular/TypeScript peer-version mismatch, generated API client mismatch, build configuration problem.

Invalid shortcuts: converting code to `any` to silence TypeScript, disabling strict mode, suppressing template diagnostics without understanding them, adding NgModules to work around a standalone configuration problem, replacing framework APIs speculatively, adding another state-management or HTTP library to bypass a local issue.
