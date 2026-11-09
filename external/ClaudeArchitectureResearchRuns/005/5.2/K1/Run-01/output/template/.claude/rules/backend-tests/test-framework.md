---
paths:
  - "backend/**/*Tests/**"
---
Kind: STD | Scope: backend-tests | Capability: backend-testing/nunit | Loading: path-scoped (backend test projects)

# Test Framework Standards: NUnit

## Role bindings

- Explicit case mechanism: one `[TestCase(...)]` per case. Generated case machinery: `TestCaseSource`, loops or LINQ in the test body.
- Fixture lifecycle: `[TestFixture]`, `[SetUp]`/`[TearDown]`, `[OneTimeSetUp]`/`[OneTimeTearDown]`. Assertions: the `Assert.That` constraint model.

## Framework

- Default: NUnit is the .NET automated test framework. Do not introduce a second test framework without a concrete reason. An established project that deliberately uses another framework keeps its convention.
