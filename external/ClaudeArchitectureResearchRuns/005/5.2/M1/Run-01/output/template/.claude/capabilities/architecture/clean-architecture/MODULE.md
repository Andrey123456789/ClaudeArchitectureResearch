> **Capability manifest** · Capability: architecture/clean-architecture · Owns: facet list, declared properties, architecture-check specification · Scope: backend, backend-tests · Loading: maintainer-only (read by `template-maintenance` and the checkers)

# Module: architecture/clean-architecture

Clean Architecture with four backend projects — Domain, Application,
Infrastructure, Api — and inward dependencies. The manifest block is the
architecture-check specification used by `.claude/scripts/check-architecture.mjs`.

| Facet role | File | Loading |
|---|---|---|
| architecture-decision | `docs/architecture.md` | always (imported by `docs/capability-selection.md`) |
| architecture-rule | `.claude/rules/architecture-style.md` | path (backend code and project files) |
| backend-layout | `.claude/skills/project-structure/references/backend-layout.md` | workflow read (`project-structure`) |

```json
{
  "capability": "architecture/clean-architecture",
  "facets": [
    { "role": "architecture-decision", "path": "docs/architecture.md", "loading": "always" },
    { "role": "architecture-rule", "path": ".claude/rules/architecture-style.md", "loading": "path" },
    { "role": "backend-layout", "path": ".claude/skills/project-structure/references/backend-layout.md", "loading": "workflow" }
  ],
  "properties": {
    "roleMapping": {
      "domain layer": "Domain",
      "use-case layer": "Application",
      "use-case unit": "Application Service",
      "persistence-access contract": "specific repository interface in Application",
      "commit boundary": "IUnitOfWork (Application) implemented in Infrastructure",
      "adapter layer": "Infrastructure",
      "entry point": "ASP.NET Core Controller in Api",
      "composition root": "Program.cs in Api",
      "test-project role": "backend/<Name>.<Layer>.Tests and backend/<Name>.IntegrationTests"
    },
    "layers": [
      { "name": "Domain", "suffix": ".Domain", "role": "domain layer", "allowedReferences": [] },
      { "name": "Application", "suffix": ".Application", "role": "use-case layer", "allowedReferences": ["Domain"] },
      { "name": "Infrastructure", "suffix": ".Infrastructure", "role": "adapter layer", "allowedReferences": ["Application", "Domain"] },
      { "name": "Api", "suffix": ".Api", "role": "composition root", "allowedReferences": ["Application", "Infrastructure"] }
    ],
    "compositionRootLayer": "Api",
    "testProjects": [
      { "suffix": ".Domain.Tests", "allowedReferences": ["Domain"] },
      { "suffix": ".Application.Tests", "allowedReferences": ["Application", "Domain"] },
      { "suffix": ".Infrastructure.Tests", "allowedReferences": ["Infrastructure", "Application", "Domain"] },
      { "suffix": ".IntegrationTests", "allowedReferences": ["Api"] }
    ]
  },
  "usesRoles": [],
  "binds": [],
  "leakTerms": ["Clean Architecture", "clean-architecture"],
  "allowList": []
}
```
