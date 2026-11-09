Kind: DEC | Scope: backend-tests | Capability: backend-testing (slot contract) | Loading: on demand (workflows, maintainers)

# Capability Contract: backend-testing

Required **leaf**. Provides the .NET automated-test framework and its technique.

- binds: architecture (test-project placement and test-project reference rules belong to the frame).

## An implementation must provide

| Kind | Facet | Location |
|---|---|---|
| DEC | selection and declared test stack | decision register → Capability selection |
| STD | role bindings (explicit case mechanism, fixture lifecycle, assertions) and the framework standard | `.claude/rules/backend-tests/test-framework.md` |
| KNW | testing technique with the framework's syntax | knowledge skill named in the register |
| WF | creating test projects, packages, running and filtering tests, build-fix cues | `workflow-facet.md` in the module directory |
| ENF | adapter that runs the neutral architecture checks (`.claude/scripts/check-architecture.mjs`) inside the backend test suite | `.claude/scripts/facets/backend-testing/` |

Neutral testing policy stays in `.claude/rules/backend-tests/testing.md` and must keep holding after a replacement.

## Replacement

Replacing the test framework is Reserved. After approval, follow `template-maintenance`: provide every facet above for the new framework (including an equivalent architecture-check adapter), update the register, remove the old module and its facets, and run the instruction-structure checker.
