Kind: WF | Scope: frontend | Capability: frontend/angular | Loading: read by workflows at frontend steps

# Workflow Facet: frontend / angular

Frontend procedures for Angular. Before using them, read `.claude/rules/frontend/frontend.md` and `.claude/rules/frontend/frontend-framework.md` if they are not loaded. Technique and code: `angular` knowledge skill.

## Scaffold the workspace

1. Use the current Angular CLI and let it select mutually compatible Angular, TypeScript and RxJS versions; do not upgrade TypeScript beyond Angular's supported range independently.
2. Create the workspace under `frontend/<Name>.Web/`, for example `npx @angular/cli@latest new <Name>.Web --directory frontend/<Name>.Web --routing --style=scss --skip-git`. Check `ng new --help` of the selected version and enable the baseline options the decision register lists (frontend → angular).
3. Add Angular Material and CDK through `add-dependency` (`ng add @angular/material`).
4. Keep the CLI's generated structure; do not impose an obsolete Angular directory structure. Feature code goes under `src/app/features/<feature>/` (see the `angular` skill), created only when a feature exists.
5. Configure the API base URL (or a development proxy, `proxy.conf.json`) so it is compatible with the backend's Development URL and CORS policy.

## Build, test and serve

Inspect `frontend/<Name>.Web/package.json` and use only scripts that exist. Typical scripts:

```bash
npm ci
npm run build
npm test
npm start
```

Do not assume a test runner from the framework alone; an existing project may deliberately use another configured runner.

## E2E tests (when E2E coverage is required)

Playwright tests live in `frontend/<Name>.Web/e2e/` and cover a small number of important user workflows. Add Playwright through `add-dependency`.

## API client generation (when adopted)

Keep generated clients separate from handwritten feature code, regenerate them from the backend contract when it changes, review the generated diff, then fix handwritten code against the result.

## Build-fix diagnostics

Typical Angular failure categories: TypeScript type errors, template compilation errors, dependency-injection/provider errors, invalid standalone imports, route configuration errors, Signal/RxJS typing issues, missing packages, Angular/TypeScript peer-version mismatches, generated API-client mismatches, build configuration problems.

Loop: inspect `package.json` and the Angular configuration, reproduce the failing command, read the diagnostic in context, inspect the affected component, service, route, template or configuration, make the smallest correct change, rerun the same command, then broaden.

Invalid shortcuts:

- converting code to `any` to silence TypeScript;
- disabling strict mode;
- suppressing template diagnostics without understanding them;
- adding NgModules to work around a standalone configuration problem;
- replacing framework APIs speculatively;
- adding another state-management or HTTP library to bypass a local issue.

## Security review cues

- Sanitizer bypasses (`bypassSecurityTrustHtml`, `bypassSecurityTrustScript`, `bypassSecurityTrustResourceUrl`) and direct DOM manipulation with untrusted content are XSS candidates. Ordinary Angular template binding is escaped and sanitized by the framework.
- Route guards and hidden buttons are UX; verify that the backend protects the operation.
- Token-handling interceptors and token storage: check against `frontend.md` → Browser security.
