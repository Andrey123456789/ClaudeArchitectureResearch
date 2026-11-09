---
paths:
  - "backend/**/*Tests/**/*.cs"
  - "backend/**/*Tests/*.csproj"
---

> Capability: backend-testing/nunit · Path rule · Scope: backend-tests · Owns the backend test-framework default and framework conventions

# Test Framework Rules: NUnit

Framework-independent test policy: `.claude/rules/testing.md`.

- NUnit is the default framework for .NET automated tests. In an established
  project that deliberately uses another framework, follow that convention. Do
  not introduce a second test framework without a concrete reason.
- Use normal NUnit conventions: `[TestFixture]` classes, `[Test]` for single
  scenarios, `[SetUp]`/`[OneTimeSetUp]` with matching teardown for fixture
  lifetime, and `Assert.That` constraint assertions. The explicit case tables
  required by `testing.md` § Test Readability are written as `[TestCase]` rows
  rather than `TestCaseSource` generators.
