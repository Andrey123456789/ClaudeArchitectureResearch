---
paths:
  - "backend/**/*Tests/**/*.cs"
  - "backend/**/*Tests/*.csproj"
---

> **Policy rule** · Capability: backend-testing/nunit · Owns: default backend test framework, its packages, and its binding of the neutral testing vocabulary · Scope: backend-tests · Loading: path (backend test projects)

# Test Framework Rules

Framework-independent test policy: `testing.md`. Technique and examples: the
`dotnet-testing` skill → `references/test-framework.md`.

## Framework

- Default: use NUnit as the .NET automated test framework. Do not introduce a
  second test framework without a concrete reason.
- In an established project that deliberately uses another framework, follow
  that project's convention.
- Packages: `NUnit`, `NUnit3TestAdapter`, `Microsoft.NET.Test.Sdk`, and
  `NUnit.Analyzers`; versions are resolved through `add-dependency` and managed
  centrally.

## Vocabulary Binding

The neutral terms used by `testing.md` map to NUnit as follows:

| Neutral term | NUnit form |
|---|---|
| explicit declarative test case | `[TestCase(...)]` on a parameterized `[Test]` |
| generated case machinery | `TestCaseSource`, `ValueSource`, `[Values]` combinations, loops |
| test fixture and setup | `[TestFixture]`, `[SetUp]` / `[TearDown]`, `[OneTimeSetUp]` / `[OneTimeTearDown]` |
| assertion | constraint model: `Assert.That(actual, Is.EqualTo(expected))` |
