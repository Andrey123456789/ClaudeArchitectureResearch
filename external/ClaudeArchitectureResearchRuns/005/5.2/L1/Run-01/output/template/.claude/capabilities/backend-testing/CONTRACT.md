> Level: 2-technology | Capability: backend-testing (slot contract) | Owns: requirements every backend test-framework implementation must satisfy | Scope: backend-tests | Loads: never (maintainer metadata)

# Slot Contract — `backend-testing` (required leaf)

Implementation-independent test policy stays outside this slot in
`.claude/rules/0-core/testing.md`: test levels, behavior focus, determinism,
isolation, relational fidelity, naming, and (in `develop`/`verify`) regression
and probe-to-test duties. Test-project placement belongs to the architecture
frame. The implementation supplies only framework-specific material, so that
replacing the framework replaces this module instead of requiring
template-wide edits.

Exactly one implementation is selected (static composition).

## Required facets

| Facet | Level | Location | Loading | Must provide |
|---|---|---|---|---|
| `backend-testing.decision` | 3 | `.claude/rules/3-project/` rule with `Capability:` header | always (CLAUDE.md import) | selected framework and integration-test baseline |
| `backend-testing.rules` | 2 | `.claude/rules/2-technology/` rule named by role, with `Capability:` header | path `backend/**/*Tests/**/*` | framework-specific rules |
| `backend-testing.knowledge` | 2 | skill `dotnet-testing` | on demand | framework technique and examples |
| `backend-testing.commands` | 2 | `<module>/commands.md` | read by `verify`, `build-fix`, `develop` | run, filter, and list commands; discovery troubleshooting |
| `backend-testing.scaffold` | 3 | `<module>/scaffold.md` | read by `project-structure` | test-project creation and packages |
| `backend-testing.check` | — | `<module>/check.json` | read by `check-architecture.cjs` | framework packages and competing framework packages (adapter for the neutral architecture check) |

## Conformance

Facet file names describe roles, not the framework. Nothing outside the module
names the framework except the capability selection record. A missing required
facet is a conformance failure and a Decision Request.
