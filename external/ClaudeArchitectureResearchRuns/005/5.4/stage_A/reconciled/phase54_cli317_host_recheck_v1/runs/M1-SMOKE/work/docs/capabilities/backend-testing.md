> Capability: backend-testing/nunit · Always-loaded planning decisions (imported by `CLAUDE.md`) · Owns the backend test stack decision

# Backend Testing: NUnit

- Backend test stack (Decided): NUnit with its test adapter for .NET automated
  tests; `Microsoft.AspNetCore.Mvc.Testing` with `WebApplicationFactory<Program>`
  is the baseline for ASP.NET Core integration tests; Testcontainers is
  conditional and is added only when isolated real-provider tests justify it.
- Backend test projects are placed by the architecture frame
  (`docs/capabilities/architecture.md`).
- Rules: `.claude/rules/test-framework.md` (framework-specific) and
  `.claude/rules/testing.md` (framework-independent).
- Knowledge skill: `dotnet-testing`.
