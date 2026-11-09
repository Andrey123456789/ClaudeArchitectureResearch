> Level: 3-project | Capability: frontend/angular (frontend.scaffold) | Owns: creation of the Angular workspace | Scope: frontend | Loads: read when project-structure names frontend.scaffold

# Frontend Scaffold — Angular

1. Resolve the current stable Angular CLI version compatible with the installed
   Node.js (`add-dependency` version rules) and check the options it supports:
   `npx @angular/cli@<version> new --help`.
2. Create the workspace outside the backend tree:

   ```bash
   npx @angular/cli@<version> new <Name>.Web --directory frontend/<Name>.Web --routing --style=scss --strict --skip-git
   ```

   Add the zoneless option when the selected stable version supports it, and
   select Vitest as the unit-test runner when the CLI asks or offers the option.
   Let the CLI choose mutually compatible TypeScript and RxJS versions; do not
   impose an obsolete directory structure the current CLI no longer generates.
3. Add Angular Material and CDK with an explicit verified version:
   `npx ng add @angular/material@<version>`.
4. Keep the manifest and lockfile per `package-management.md`.
5. Configure the API base URL and a development proxy (`proxy.conf.json`)
   compatible with the backend's Development endpoint and CORS policy.
6. Create feature directories only when they contain code (structure:
   `frontend-structure.md`, technique: `angular`).
7. E2E with Playwright only when E2E coverage is required, inside
   `frontend/<Name>.Web/e2e/`.
8. Verify with `frontend.commands` (install, build, test).
