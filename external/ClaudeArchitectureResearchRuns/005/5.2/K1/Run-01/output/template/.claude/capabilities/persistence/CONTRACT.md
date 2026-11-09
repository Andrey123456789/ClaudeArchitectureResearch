Kind: DEC | Scope: backend | Capability: persistence (slot contract) | Loading: on demand (workflows, maintainers)

# Capability Contract: persistence

Required **leaf**. Provides the persistence technique behind the architecture frame's persistence port and commit boundary.

- binds: architecture (roles Infrastructure, Application, persistence port, commit boundary, persistence area).

## An implementation must provide

- **Commit-boundary binding**: how the frame's commit boundary and the shared per-use-case persistence session are implemented.
- **Migration mechanism**: how schema changes are created, reviewed and turned into deployment artifacts. Applying production migrations stays a deliberate deployment step.
- **Seeding mechanism**: the Development seeder, its placement inside the persistence area and its startup wiring.
- **Provider variant**: the selected database provider, declared in the register.
- **Declared observable properties**: string comparison and collation semantics and any other provider behavior that users can observe.
- **Testing implications**: what provider fidelity means for this implementation and how tests obtain it.
- **Facets**:

| Kind | Facet | Location |
|---|---|---|
| DEC | selection, variant, declared properties | decision register → Capability selection |
| STD | role bindings (persistence-technology types, session, provider-fidelity target), technology boundary, seeder placement, development configuration | `.claude/rules/backend/persistence-technology.md` |
| KNW | implementation technique | knowledge skill named in the register |
| WF | persistence-area layout, setup, model and schema changes, migrations, schema-affecting settings, production migration artifacts, review cues | `workflow-facet.md` in the module directory |
| ENF | infrastructure-only package prefixes, co-change patterns | `.claude/scripts/facets/persistence/enforcement.json` |

## Variants and replacement

- Changing the database provider is a **provider-variant change** inside this slot, not a new slot. It is Reserved. Update the register variant and declared properties, the provider bindings in the STD, WF and KNW facets, the development connection configuration and the provider-fidelity tests.
- Replacing the persistence technology is Reserved. When a replacement lacks a required mechanism (for example, it has no migration mechanism), the Decision Request must name the gap and the proposed alternative. Behavior must not be lost silently.
- Procedure: `template-maintenance`.
