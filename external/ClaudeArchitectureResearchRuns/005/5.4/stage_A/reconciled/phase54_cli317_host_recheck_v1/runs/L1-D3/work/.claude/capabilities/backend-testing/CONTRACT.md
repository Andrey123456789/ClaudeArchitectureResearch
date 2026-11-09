> Level: 2-technology · Owns: backend-testing slot contract (maintainer metadata) · Scope: backend-tests · Loading: never auto-loaded

# Slot Contract: backend-testing (required leaf)

Implementation-independent test policy stays outside the module in `.claude/rules/0-core/testing.md`: test levels, behavior focus, determinism, isolation, relational fidelity, probe-to-test preservation (owned by `verify`), and framework-neutral naming. Test-project placement and references belong to the architecture frame.

## Required facets

| Facet | Form | Level | Loading | Must provide |
| --- | --- | --- | --- | --- |
| `backend-testing.framework` | rule | 2 | path: backend-tests | framework selection rule and bindings of neutral rules to framework constructs |
| `backend-testing.commands` | workflow-read reference | 2 | read by workflows | test-project scaffold packages and commands, test run/filter commands |
| `backend-testing.enforcement` | enforcement data (JSON) | 2 | scripts | adapter for neutral architecture checks: packages that mark a test project, approval-required second frameworks |
| knowledge skill | skill | 2 | on demand | framework technique and examples |

## Replacement

Replacing the framework (for example with another .NET test framework) replaces this module: new rule facet, commands, enforcement data, knowledge content, and the selection-record row. Workflows refer only to `backend-testing.*` facets and need no edits. Changing the selection is Reserved and requires an ADR.
