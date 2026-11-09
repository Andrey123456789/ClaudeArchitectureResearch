---
paths:
  - "backend/**/*Tests/**"
---

> Level: 2 Technology | Owns: NUnit framework usage and ASP.NET Core integration-test binding | Scope: backend-tests | Loads: path | Depends on: 0-core/testing-principles.md

# Backend Test Technology

- Default: write .NET automated tests with NUnit; do not introduce a second test
  framework without a concrete reason. An established project that deliberately
  uses another framework keeps its convention.
- Default: use `WebApplicationFactory<Program>`-based integration tests when
  routing, model binding, middleware, authentication, DI, repositories, EF Core,
  or database persistence is what the test must prove; the `Testing`
  environment uses isolated test resources.

## Bindings to Core Testing Principles

- EF Core InMemory is not relational provider fidelity; SQL Server behavior is
  verified only against SQL Server.
- Testcontainers is one way to obtain an isolated real provider; it is not
  required for every integration test.
- `TimeProvider` with `FakeTimeProvider` makes time deterministic.

Technique: → `dotnet-testing` skill.
