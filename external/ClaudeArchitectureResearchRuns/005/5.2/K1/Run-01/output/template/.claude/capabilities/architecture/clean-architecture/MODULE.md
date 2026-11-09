Kind: DEC | Scope: backend | Capability: architecture/clean-architecture | Loading: module manifest, read on demand

# Module: architecture/clean-architecture

- slot: architecture (required frame)
- implementation: clean-architecture
- aliases: Clean Architecture, clean-architecture
- binds: —

## Facets

| Kind | Facet | Scope | Loading |
|---|---|---|---|
| DEC | `docs/architecture/decision-register.md` (section "architecture → clean-architecture") | common | always (imported by CLAUDE.md) |
| STD | `.claude/rules/backend/architecture-style.md` | backend | path-scoped (backend/**) |
| WF | `.claude/capabilities/architecture/clean-architecture/workflow-facet.md` | backend | read by `project-structure`, `development-workflow` |
| ENF | `.claude/scripts/facets/architecture/enforcement.json` | backend | read by `check-architecture.mjs` and the Stop hook |

## Declared properties

Decided properties (style, layer roles, orchestration, commit boundary, styles not adopted) are recorded in the decision register section of this module. Implementation facts:

- Layer projects: `backend/<Name>.Domain`, `backend/<Name>.Application`, `backend/<Name>.Infrastructure`, `backend/<Name>.Api`.
- Persistence area: `backend/<Name>.Infrastructure/Persistence/`.
- Test projects: `backend/<Name>.<Layer>.Tests` and `backend/<Name>.IntegrationTests` (workflow facet → Test-project placement).
