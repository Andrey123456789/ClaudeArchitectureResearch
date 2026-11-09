> Capability: frontend/angular · Module manifest · Optional slot · Maintainer metadata · Not auto-loaded

# Module: frontend/angular

The selected frontend implementation: Angular with standalone APIs. It owns the
Angular planning decisions, the Angular-specific rule facet with its bindings
for `.claude/rules/frontend.md`, and the `angular` knowledge skill, which also
holds the scaffolding notes and the security-review notes for sanitizer
bypasses.

## Manifest

```json
{
  "slot": "frontend",
  "implementation": "angular",
  "facets": {
    "planning": ["docs/capabilities/frontend.md"],
    "rules": [".claude/rules/frontend-framework.md"],
    "knowledge": [".claude/skills/angular/SKILL.md"]
  },
  "properties": {
    "testRunner": "Vitest (Angular CLI setup)",
    "e2eTool": "Playwright, only when E2E coverage is required",
    "scaffoldCommand": "ng new under frontend/<Name>.Web (angular skill, Scaffolding)",
    "bindings": ".claude/rules/frontend-framework.md#bindings-for-frontendmd"
  },
  "binds": [],
  "leakTokens": ["Angular", "angular", "RxJS", "NgRx", "NgModule", "Vitest", "@angular", "ng add", "ng new", "provideHttpClient"],
  "enforcement": {
    "notByDefaultPackages": ["@ngrx/store", "@ngrx/effects", "@ngrx/signals", "axios", "lodash", "lodash-es", "bootstrap", "tailwindcss"],
    "devOnlyPackages": ["@angular/cli", "@angular/build", "@angular-devkit/build-angular", "@angular/compiler-cli", "vitest"]
  }
}
```
