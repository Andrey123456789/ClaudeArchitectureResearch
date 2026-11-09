> **Capability selection record** · Owns: static composition of the four capability slots and their declared properties · Scope: common · Loading: always (imported by `CLAUDE.md`)

# Capability Selection

Composition is static: each required slot has exactly one selected
implementation, the optional slot has zero or one, and unselected implementations
are not part of the runtime. Changing a selection, or changing an observable
declared property, is Reserved and requires an ADR (`architecture-decision`).

| Slot | Status | Selected | Declared properties |
|---|---|---|---|
| architecture | required frame | clean-architecture | layers Domain, Application, Infrastructure, Api; role mapping in `architecture.md` |
| persistence | required | ef-core | provider variant: sqlserver; observable string comparison follows the database collation (common SQL Server default collations are case-insensitive), so choosing it is a product decision |
| backend-testing | required | nunit | test projects follow the frame's test-project role |
| frontend | optional, enabled | angular | workspace `frontend/<Name>.Web/`; package manager npm |

## Facets of the Selected Implementations

| Slot | Rule facet (path-loaded) | Knowledge facet (on demand) | Other facets |
|---|---|---|---|
| architecture | `.claude/rules/architecture-style.md` | — | `architecture.md` (always); project-structure `references/backend-layout.md` |
| persistence | `.claude/rules/persistence-technology.md` | `ef-core` skill | — |
| backend-testing | `.claude/rules/test-framework.md` | `dotnet-testing` skill → `references/test-framework.md` | — |
| frontend | `.claude/rules/frontend-framework.md` | `angular` skill | `frontend-stack.md` (always) |

Workflows and other artifacts refer to these facets by role (for example "the
persistence knowledge facet"); this table resolves the role.

## Planning-Time Facets

@architecture.md
@frontend-stack.md

## Maintainer Metadata

Slot contracts (`.claude/capabilities/<slot>/CONTRACT.md`) and implementation
manifests (`.claude/capabilities/<slot>/<implementation>/MODULE.md`) are not
loaded in normal sessions; the user-run `template-maintenance` workflow reads them.
