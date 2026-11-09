> Level: 2-technology | Capability: backend-testing/nunit (module manifest) | Owns: facet list and declared properties of the NUnit backend-testing implementation | Scope: backend-tests | Loads: never (maintainer metadata)

# Module — `backend-testing/nunit`

- Slot: `backend-testing` (required leaf) — selected.
- binds: `architecture` — examples in `dotnet-testing`, `commands.md`, and
  `scaffold.md` use the current frame's test-project names
  (`<Name>.Application.Tests`, `<Name>.IntegrationTests`) and the Api host's
  `Program` for `WebApplicationFactory<Program>`. Persistence fidelity is taken
  from the persistence slot's declared properties, never named here.

- leak terms: `NUnit`

## Facets

| Facet | File | Level | Loading |
|---|---|---|---|
| `backend-testing.decision` | `.claude/rules/3-project/backend-testing-stack.md` | 3 | always (CLAUDE.md import) |
| `backend-testing.rules` | `.claude/rules/2-technology/test-framework.md` | 2 | path `backend/**/*Tests/**/*` |
| `backend-testing.knowledge` | `.claude/skills/dotnet-testing/SKILL.md` | 2 | on demand |
| `backend-testing.commands` | `.claude/capabilities/backend-testing/nunit/commands.md` | 2 | read by workflows |
| `backend-testing.scaffold` | `.claude/capabilities/backend-testing/nunit/scaffold.md` | 3 | read by `project-structure` |
| `backend-testing.check` | `.claude/capabilities/backend-testing/nunit/check.json` | — | `check-architecture.cjs` |

## Declared properties

| Property | Value |
|---|---|
| framework packages | NUnit, NUnit3TestAdapter, Microsoft.NET.Test.Sdk (NUnit.Analyzers optional) |
| integration-test host | Microsoft.AspNetCore.Mvc.Testing, `WebApplicationFactory<Program>` |
| explicit-case mechanism | `[TestCase]` rows |
