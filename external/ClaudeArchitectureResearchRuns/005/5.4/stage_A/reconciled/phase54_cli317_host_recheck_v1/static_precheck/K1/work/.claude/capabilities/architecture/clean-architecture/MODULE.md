> Kind: — (module manifest) | Scope: repo/meta | Capability: architecture/clean-architecture | Loading: not loaded (read by `architecture-decision`, `template-maintenance`, and the structure checker)

# Module: architecture / clean-architecture

- Slot: architecture
- Implementation: clean-architecture
- Variant: —
- Names: Clean Architecture, clean-architecture, CleanArchitecture
- Binds: —

## Facets

| Kind | Scope | File | Loading | Provides |
|---|---|---|---|---|
| DEC | common | `docs/architecture/decision-register.md` | always (capability-selection block) | selection, role summary, not-adopted styles |
| STD | backend | `.claude/rules/backend/architecture-style.md` | path-scoped | role map, dependency direction, domain modeling, orchestration, commit-boundary placement, composition, transport contracts |
| STD | backend-tests | `.claude/rules/backend-tests/test-projects.md` | path-scoped | test-project references |
| WF | backend | `.claude/skills/project-structure/references/backend-layout.md` | read by `project-structure` | backend scaffold layout and references |
| ENF | backend | `.claude/scripts/facets/architecture-style.cjs` | manifest hook, `verify` | project-reference and inner-layer framework checks |

## Contract coverage

| Item | Provided by |
|---|---|
| `role-map` | STD `architecture-style.md`; WF `backend-layout.md` |
| `dependency-direction` | STD `architecture-style.md` |
| `domain-modeling` | STD `architecture-style.md` |
| `use-case-orchestration` | STD `architecture-style.md` |
| `commit-boundary-placement` | STD `architecture-style.md` |
| `composition-root` | STD `architecture-style.md` |
| `transport-contracts` | STD `architecture-style.md` |
| `test-project-placement` | STD `test-projects.md`; WF `backend-layout.md` |
| `not-adopted-styles` | DEC capability selection |
| `scaffold-layout` | WF `backend-layout.md` |
| `reference-check` | ENF `architecture-style.cjs` |
