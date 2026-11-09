> Level: 2-technology | Capability: persistence (slot contract) | Owns: requirements every persistence implementation must satisfy | Scope: backend | Loads: never (maintainer metadata)

# Slot Contract — `persistence` (required leaf)

The persistence slot covers more than the data-access library: it owns how the
persistence-access and commit-boundary roles are implemented, how schema
evolves, how Development data is seeded, which provider is used, and what that
means for string semantics and relational tests. A provider change (switching to
another relational database) is a variant change inside this slot, not a new
slot.

Exactly one implementation is selected (static composition). It binds to roles
and to the frame's named location `persistence implementation`, never to frame
layer names in prose.

## Required facets

| Facet | Level | Location | Loading | Must provide |
|---|---|---|---|---|
| `persistence.decision` | 3 | `.claude/rules/3-project/` rule with `Capability:` header | always (CLAUDE.md import) | the selected stack and provider |
| `persistence.rules` | 2 | `.claude/rules/2-technology/` rule named by role, with `Capability:` header | path `backend/**/*` | persistence-technology type list; commit-boundary binding; seeding mechanism (environment restriction, empty-store behavior, schema/seed separation, dataset quality); Development connection configuration |
| `persistence.knowledge` | 2 | skill | on demand | implementation technique |
| `persistence.workflow` | 2 | `<module>/workflow.md` | read by `develop`, `custom-settings`, `verify` | model/schema change procedure; migration creation and review; seed co-change; local database recreation |
| `persistence.scaffold` | 3 | `<module>/scaffold.md` | read by `project-structure` | packages, internal structure of the persistence implementation, registration, startup seeding wiring |
| `persistence.co-change` | — | `<module>/co-change.json` | read by the stop hook | path rules for seed/migration co-change reminders |

## Required declared properties (capability selection record)

provider variant; migration mechanism; seeding mechanism; default string
comparison / case-sensitivity semantics when observable; relational test
fidelity (which real provider proves relational behavior).

## Conformance

A replacement must not silently lose migration or seeding semantics: every
topic listed for `persistence.rules` and `persistence.workflow` must be covered.
A missing required facet or declared property is a conformance failure and a
Decision Request. Changing the provider variant or a declared property that is
observable (for example string comparison) must not happen silently.
