> Kind: — (module manifest) | Scope: repo/meta | Capability: backend-testing/nunit | Loading: not loaded (read by `architecture-decision`, `template-maintenance`, and the structure checker)

# Module: backend-testing / nunit

- Slot: backend-testing
- Implementation: nunit
- Variant: —
- Names: NUnit, nunit
- Binds: architecture — test projects follow the frame's placement and reference rules (`.claude/rules/backend-tests/test-projects.md`).

## Facets

| Kind | Scope | File | Loading | Provides |
|---|---|---|---|---|
| DEC | common | `docs/architecture/decision-register.md` | always (capability-selection block) | selection, integration-host property |
| STD | backend-tests | `.claude/rules/backend-tests/test-framework.md` | path-scoped | default framework standard |
| KNW | backend-tests | `.claude/skills/dotnet-testing/SKILL.md` | on-demand | NUnit test technique |
| WF | backend-tests | `.claude/skills/project-structure/references/test-setup.md` | read by `project-structure` | test project scaffolding |
| ENF | backend-tests | `.claude/scripts/facets/test-framework.cjs` | manifest hook, `verify` | additional-framework detection |

## Contract coverage

| Item | Provided by |
|---|---|
| `framework-standard` | STD `test-framework.md` |
| `integration-host-binding` | DEC capability selection (`WebApplicationFactory<Program>`); KNW `dotnet-testing` |
| `knowledge` | KNW `dotnet-testing` |
| `test-scaffold` | WF `test-setup.md` |
| `framework-consistency-check` | ENF `test-framework.cjs` |
