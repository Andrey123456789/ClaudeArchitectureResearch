> Capability: backend-testing/nunit · Module manifest · Maintainer metadata · Not auto-loaded

# Module: backend-testing/nunit

The selected backend test framework: NUnit. Replacing it (for example with
xUnit) replaces this module's facets — the planning facet, the
`test-framework.md` rule, the `dotnet-testing` knowledge content, and the
adapter data below — without touching the framework-independent testing rule.

`binds`: none; test-project placement is taken from the frame's placement
reference by pointer.

## Manifest

```json
{
  "slot": "backend-testing",
  "implementation": "nunit",
  "facets": {
    "planning": ["docs/capabilities/backend-testing.md"],
    "rules": [".claude/rules/test-framework.md"],
    "knowledge": [".claude/skills/dotnet-testing/SKILL.md"]
  },
  "properties": {
    "framework": "NUnit",
    "packages": "NUnit, NUnit3TestAdapter, Microsoft.NET.Test.Sdk",
    "caseMechanism": "[TestCase] rows",
    "fixtureLifecycle": "[SetUp]/[TearDown], [OneTimeSetUp]/[OneTimeTearDown]",
    "filterCommand": "dotnet test --filter \"FullyQualifiedName~<Name>\""
  },
  "binds": [],
  "leakTokens": ["NUnit", "nunit", "[TestCase", "[TestFixture", "TestCaseSource", "OneTimeSetUp", "Assert.That"],
  "enforcement": {
    "testFrameworkPackages": ["NUnit", "NUnit3TestAdapter"],
    "competingFrameworkPackages": ["xunit", "xunit.v3", "xunit.runner.visualstudio", "MSTest", "MSTest.TestFramework", "MSTest.TestAdapter", "TUnit"]
  }
}
```
