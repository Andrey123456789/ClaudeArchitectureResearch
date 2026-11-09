---
paths:
  - "backend/**/*Tests/**/*.cs"
  - "backend/**/*Tests/*.csproj"
---

> Level: 2 Technology · Owns: backend test-technology bindings — NUnit, ASP.NET Core integration testing, EF Core test providers · Scope: backend-tests · Loads: path rule · Depends on: CLAUDE.md, .claude/rules/0-core/testing-principles.md

# Backend Test Technology

Framework-neutral principles: `0-core/testing-principles.md`. Technique: the `dotnet-testing` skill.

- Use NUnit as the default .NET automated test framework; do not introduce a second test framework without a concrete reason. In an established project that deliberately uses another framework, follow its convention (default).
- Use `WebApplicationFactory<Program>`-based integration tests when routing, binding, middleware, authentication/authorization, dependency injection, repositories, EF Core, or database persistence is what the test must prove (default). The `Testing` environment uses isolated test resources.
- EF Core InMemory is not a relational provider: never use it while claiming to verify relational or SQL Server behavior.
