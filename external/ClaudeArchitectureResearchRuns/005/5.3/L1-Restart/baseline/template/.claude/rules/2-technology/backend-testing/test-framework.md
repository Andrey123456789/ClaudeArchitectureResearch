---
paths:
  - "backend/**/*Tests/**/*"
---

> Level: 2-technology · Capability: backend-testing/nunit · Facet: backend-testing.framework · Owns: backend test framework selection rule and NUnit bindings · Scope: backend-tests · Loading: path

# NUnit Test Framework

- Default: NUnit is the .NET automated test framework. In an established project that deliberately uses another framework, follow that convention; do not introduce a second test framework without a concrete reason.

## Bindings

These bind the framework-neutral test rules to NUnit; they add no separate policy.

- Explicit case = an NUnit `[TestCase]` row; `TestCaseSource` counts as generated case machinery.
- Fixture lifetime: a `WebApplicationFactory<Program>` host is created in `[OneTimeSetUp]` and disposed in `[OneTimeTearDown]`.

Technique: `dotnet-testing`. Commands: `backend-testing.commands`.
