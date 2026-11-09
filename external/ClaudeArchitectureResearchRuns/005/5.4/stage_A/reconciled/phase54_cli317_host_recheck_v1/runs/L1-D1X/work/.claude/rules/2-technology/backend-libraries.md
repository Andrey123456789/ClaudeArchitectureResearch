---
paths:
  - "backend/**/*"
---

> Level: 2-technology · Owns: usage rules for approved non-slot backend libraries — FluentValidation, Swagger, Serilog, container images · Scope: backend · Loading: path

# Backend Library Rules

- Use FluentValidation for explicit request and use-case validation where appropriate, and keep each rule at its owning boundary: transport/request concerns at the entry point, use-case and straightforward workflow rules in the use-case layer, genuine domain invariants in the domain model. Do not move domain invariants into validators or duplicate one rule mechanically across layers.
- Swagger/OpenAPI metadata must describe the API that actually runs — routes, important response statuses (including those produced by the pipeline), schemas, and authentication behavior; never document speculative responses.
- Default: enable Swagger UI in Development; exposure in other environments follows the Swagger decision in the decisions file.
- Default: when Serilog is configured, use the DI-integrated `AddSerilog` approach with provider configuration in environment-aware configuration; application code keeps depending on `ILogger<T>`.
- Default: production containers use an appropriate runtime image rather than the SDK image for convenience, and do not switch to root merely to bypass filesystem permission problems.

Technique: `swagger`, `logging`, `docker`, `aspnet-error-handling` skills.
