> Kind: WF | Scope: frontend | Capability: frontend/angular | Loading: read by `project-structure` when its step says so

# Frontend Setup — Angular

Scaffolding facet of the frontend capability. Stack: decision register (frontend row); standards: `.claude/rules/frontend/`; technique: `angular`.

1. Use the latest stable Angular release supported by the selected Node.js environment, through the current Angular CLI. Let the CLI select mutually compatible Angular/TypeScript/RxJS versions; do not upgrade TypeScript beyond Angular's supported range independently.
2. Create the workspace in the shared frontend location:

   ```bash
   npx @angular/cli@<verified stable version> new ProjectName.Web --directory frontend/ProjectName.Web --routing --style=scss --strict
   ```

   Accept zoneless mode when the selected stable version supports it; keep the CLI's default test runner when it is Vitest, otherwise configure Vitest as the baseline for new projects.
3. Add Angular Material/CDK with the version matching the workspace (`ng add @angular/material`), following `add-dependency` for version and license checks.
4. Configure the API base URL for the Development backend and keep it compatible with the backend's CORS configuration.
5. Create feature directories only when they contain code; no empty `core/`, `shared/`, or `features/` trees.
6. Verify with the workspace's declared scripts (`npm run build`, `npm test`) and commit `package-lock.json`.

Playwright E2E is added only when E2E coverage is required (decision register: Conditional technologies), inside `frontend/ProjectName.Web/e2e/`.
