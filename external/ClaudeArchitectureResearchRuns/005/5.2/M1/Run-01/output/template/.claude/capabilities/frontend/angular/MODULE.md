> **Capability manifest** · Capability: frontend/angular · Owns: facet list and declared properties of the Angular implementation · Scope: frontend · Loading: maintainer-only (read by `template-maintenance` and the checkers)

# Module: frontend/angular

Angular (standalone, strict, routing, SCSS, Material/CDK, Vitest) in
`frontend/<Name>.Web/`, managed with npm.

| Facet role | File | Loading |
|---|---|---|
| frontend-stack | `docs/frontend-stack.md` | always (imported by `docs/capability-selection.md`) |
| frontend-framework-rule | `.claude/rules/frontend-framework.md` | path (frontend workspace) |
| frontend-knowledge | `.claude/skills/angular/SKILL.md` | on demand |

```json
{
  "capability": "frontend/angular",
  "facets": [
    { "role": "frontend-stack", "path": "docs/frontend-stack.md", "loading": "always" },
    { "role": "frontend-framework-rule", "path": ".claude/rules/frontend-framework.md", "loading": "path" },
    { "role": "frontend-knowledge", "path": ".claude/skills/angular/SKILL.md", "loading": "on-demand" }
  ],
  "properties": {
    "workspace": "frontend/<Name>.Web",
    "packageManager": "npm",
    "commands": {
      "scaffold": "npx @angular/cli@latest new <Name>.Web --directory frontend/<Name>.Web --routing --style=scss --strict",
      "build": "npm run build",
      "test": "npm test"
    },
    "notByDefaultPackages": ["@ngrx/*", "axios", "lodash", "lodash-es", "bootstrap", "tailwindcss"],
    "dependencyCommands": ["ng add", "ng update"]
  },
  "usesRoles": [],
  "binds": [],
  "leakTerms": ["Angular", "angular", "NgModule", "RxJS", "Vitest"],
  "allowList": []
}
```
