> **Capability manifest** · Capability: backend-testing/nunit · Owns: facet list and declared properties of the NUnit implementation · Scope: backend-tests · Loading: maintainer-only (read by `template-maintenance` and the checkers)

# Module: backend-testing/nunit

NUnit with `NUnit3TestAdapter`, `Microsoft.NET.Test.Sdk`, and `NUnit.Analyzers`.

| Facet role | File | Loading |
|---|---|---|
| test-framework-rule | `.claude/rules/test-framework.md` | path (backend test projects) |
| test-framework-reference | `.claude/skills/dotnet-testing/references/test-framework.md` | on demand (read by `dotnet-testing`) |

```json
{
  "capability": "backend-testing/nunit",
  "facets": [
    { "role": "test-framework-rule", "path": ".claude/rules/test-framework.md", "loading": "path" },
    { "role": "test-framework-reference", "path": ".claude/skills/dotnet-testing/references/test-framework.md", "loading": "on-demand" }
  ],
  "properties": {
    "packages": ["NUnit", "NUnit3TestAdapter", "Microsoft.NET.Test.Sdk", "NUnit.Analyzers"],
    "testProjectMarkers": ["NUnit", "NUnit3TestAdapter"],
    "commands": {
      "scaffold": "dotnet new nunit -n <Name>.<Layer>.Tests -o backend/<Name>.<Layer>.Tests",
      "run": "dotnet test"
    },
    "vocabularyBinding": {
      "explicit declarative test case": "[TestCase(...)]",
      "generated case machinery": "TestCaseSource, ValueSource, [Values]",
      "test fixture and setup": "[TestFixture], [SetUp], [OneTimeSetUp]",
      "assertion": "Assert.That(actual, Is.EqualTo(expected))"
    }
  },
  "usesRoles": ["test-project role"],
  "binds": [],
  "leakTerms": ["NUnit", "nunit", "TestCaseSource", "[TestCase", "[TestFixture", "OneTimeSetUp"],
  "allowList": []
}
```
