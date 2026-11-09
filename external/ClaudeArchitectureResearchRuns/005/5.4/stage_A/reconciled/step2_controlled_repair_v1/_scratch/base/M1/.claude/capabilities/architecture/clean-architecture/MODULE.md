> Capability: architecture/clean-architecture · Module manifest · Maintainer metadata · Not auto-loaded

# Module: architecture/clean-architecture

The selected architecture frame. It maps the contract roles to the
`Domain`, `Application`, `Infrastructure`, and `Api` projects, owns placement
and the patterns not adopted, and supplies the project-reference and
namespace-boundary specification used by `.claude/scripts/check-architecture.js`.

Runtime facets live in the normal flat locations listed in the manifest; this
file only ties them to the module.

## Manifest

```json
{
  "slot": "architecture",
  "implementation": "clean-architecture",
  "facets": {
    "planning": ["docs/capabilities/architecture.md"],
    "rules": [".claude/rules/architecture.md"],
    "placement": [".claude/skills/project-structure/references/backend-layout.md"]
  },
  "properties": {
    "adoptedStyle": "Clean Architecture",
    "roleMap": "docs/capabilities/architecture.md#role-map",
    "patternsNotAdopted": "docs/capabilities/architecture.md#patterns-not-adopted",
    "repositoryLayout": "docs/capabilities/architecture.md#repository-layout"
  },
  "binds": [],
  "leakTokens": ["Clean Architecture", "clean-architecture"],
  "enforcement": {
    "detailTokens": ["Infrastructure", ".Domain", ".Application", ".Api"],
    "reservedPackages": ["MediatR", "Kommand"],
    "architecture": {
      "projectRoot": "backend",
      "layers": [
        { "role": "core model", "suffix": ".Domain", "mayReference": [] },
        { "role": "use-case layer", "suffix": ".Application", "mayReference": ["core model"] },
        { "role": "adapter layer", "suffix": ".Infrastructure", "mayReference": ["use-case layer", "core model"] },
        { "role": "entry point", "suffix": ".Api", "mayReference": ["use-case layer", "adapter layer", "core model"] }
      ],
      "testProjects": [
        { "suffix": ".Domain.Tests", "mayReference": ["core model"] },
        { "suffix": ".Application.Tests", "mayReference": ["use-case layer", "core model"] },
        { "suffix": ".Infrastructure.Tests", "mayReference": ["adapter layer", "use-case layer", "core model"] },
        { "suffix": ".IntegrationTests", "mayReference": ["entry point"] }
      ],
      "forbiddenNamespaces": {
        "core model": ["Microsoft.AspNetCore", "{persistence.technologyNamespaces}"],
        "use-case layer": ["Microsoft.AspNetCore", "{persistence.technologyNamespaces}"]
      },
      "owner": ".claude/rules/architecture.md"
    }
  }
}
```
