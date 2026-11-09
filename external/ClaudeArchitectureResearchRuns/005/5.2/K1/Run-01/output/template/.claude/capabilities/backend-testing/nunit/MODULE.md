Kind: DEC | Scope: backend-tests | Capability: backend-testing/nunit | Loading: module manifest, read on demand

# Module: backend-testing/nunit

- slot: backend-testing (required leaf)
- implementation: nunit
- aliases: NUnit, nunit, TestCaseSource, TestFixture, OneTimeSetUp
- binds: architecture (test-project placement and references)

## Facets

| Kind | Facet | Scope | Loading |
|---|---|---|---|
| DEC | `docs/architecture/decision-register.md` (section "backend-testing → nunit") | common | always (imported by CLAUDE.md) |
| STD | `.claude/rules/backend-tests/test-framework.md` | backend-tests | path-scoped (backend test projects) |
| KNW | `.claude/skills/dotnet-testing/SKILL.md` | backend-tests | on invocation |
| WF | `.claude/capabilities/backend-testing/nunit/workflow-facet.md` | backend-tests | read by `project-structure`, `verify`, `build-fix` |
| ENF | `.claude/scripts/facets/backend-testing/ArchitectureConformanceTests.cs` | backend-tests | scaffold asset; runs inside `dotnet test` |

## Declared properties

Decided properties (framework, integration-test host, conditional Testcontainers) are recorded in the decision register section of this module. Implementation facts:

- Packages: NUnit, NUnit3TestAdapter, NUnit.Analyzers, Microsoft.NET.Test.Sdk; Microsoft.AspNetCore.Mvc.Testing for integration tests; Microsoft.Extensions.TimeProvider.Testing when `FakeTimeProvider` is needed.
- Test-project template: `dotnet new nunit`.
