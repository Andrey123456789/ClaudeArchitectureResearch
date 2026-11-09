---
paths:
  - "backend/**/*Tests/**/*"
---
> Level: 2-technology | Capability: backend-testing/nunit (backend-testing.rules) | Owns: NUnit framework rules | Scope: backend-tests | Loads: path (backend test projects)

# Test Framework — NUnit

- Default: NUnit is the .NET automated test framework. Do not introduce a
  second test framework without a concrete reason; in an established project
  that deliberately uses another framework, follow that convention.
- Test projects reference NUnit, NUnit3TestAdapter, and Microsoft.NET.Test.Sdk
  (versions centrally managed); the architecture check verifies this and flags
  competing framework packages.

Commands: `backend-testing.commands`. Technique and examples: `dotnet-testing`.
