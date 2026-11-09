> Level: 1-architecture | Capability: architecture/clean-architecture (module manifest) | Owns: facet list and declared properties of the Clean Architecture frame | Scope: backend | Loads: never (maintainer metadata)

# Module — `architecture/clean-architecture`

- Slot: `architecture` (required frame) — selected.
- binds: none (the frame is the binding target of the leaves).
- leak terms: `Clean Architecture`, `clean-architecture`
- binding terms (allowed only here and in modules that bind `architecture`):
  `IUnitOfWork`, `Application Service`, and the layer project names from
  `check.json`

## Facets

| Facet | File | Level | Loading |
|---|---|---|---|
| `architecture.decision` | `.claude/rules/1-architecture/adopted-architecture.md` | 1 | always (CLAUDE.md import) |
| `architecture.boundaries` | `.claude/rules/1-architecture/layering.md` | 1 | path `backend/**/*` |
| `architecture.layout` | `.claude/capabilities/architecture/clean-architecture/layout.md` | 1 | read by `project-structure` |
| `architecture.check` | `.claude/capabilities/architecture/clean-architecture/check.json` | — | read by scripts and hooks |

## Declared properties

- Backend layers: Domain, Application, Infrastructure, Api (`backend/<Name>.<Layer>/`).
- Role mapping: `layering.md`.
- Named location for leaves: `persistence implementation` →
  `backend/<Name>.Infrastructure/Persistence/`.

## Replacement notes

A replacement frame must map the same roles and expose the same named
locations, or the dependent leaves must declare new `binds:` couplings.
