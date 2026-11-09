> Level: 2-technology | Capability: frontend/angular (frontend.commands) | Owns: Angular workspace commands and framework-specific build-fix notes | Scope: frontend | Loads: read when a workflow step names frontend.commands

# Frontend Commands — Angular

Run inside `frontend/<Name>.Web/`. Inspect `package.json` first and use only
scripts that actually exist; do not invent script names or assume a test runner
because the framework is in use (Vitest is the baseline for new workspaces; an
existing workspace may deliberately use another configured runner).

| Purpose | Command |
|---|---|
| Clean, lockfile-based install (CI, fresh clone) | `npm ci` |
| Build | `npm run build` |
| Unit tests | `npm test` (or the configured test script) |
| Lint, when configured | `npm run lint` |
| Development server | `npm start` (proxying API calls per the workspace proxy configuration) |
| Dependency audit | `npm audit` |
| Toolchain facts | `node --version`, `npm --version`, `npx ng version` |

## Build-fix notes

Typical failure categories: TypeScript type errors, template compilation
errors, dependency-injection/provider errors, invalid standalone imports, route
configuration errors, signal/RxJS typing issues, missing packages,
Angular/TypeScript peer-version mismatches, generated API-client mismatches,
build configuration problems.

Angular-specific inspection for the `build-fix` loop: `package.json` and
`angular.json` first, then the affected component, service, route, template, or
configuration; read template diagnostics in the context of the component.

Do not:

- convert code to `any` merely to silence TypeScript;
- disable strict mode or suppress template diagnostics without understanding them;
- add NgModules to work around a standalone configuration problem;
- replace framework APIs speculatively;
- add another state-management or HTTP library to bypass a local issue;
- delete `package-lock.json` reflexively;
- upgrade TypeScript beyond the range Angular supports.

## Generated API clients

When OpenAPI client generation is adopted, regenerate with the workspace's
generation script from `package.json`; the repair order for contract failures is
in `build-fix`.
