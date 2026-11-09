---
paths:
  - "backend/**/*Tests/**/*"
---
> Level: 3-project | Capability: backend-testing/nunit (backend-testing.decision) | Owns: selected backend testing stack | Scope: backend-tests | Loads: always (imported by CLAUDE.md)

# Backend Testing Stack

Backend automated tests use NUnit. Backend test projects live under `backend/`
alongside the production projects. ASP.NET Core integration tests use
Microsoft.AspNetCore.Mvc.Testing with `WebApplicationFactory<Program>` as the
baseline. Testcontainers is conditional: add it only when isolated
real-provider tests justify it.
