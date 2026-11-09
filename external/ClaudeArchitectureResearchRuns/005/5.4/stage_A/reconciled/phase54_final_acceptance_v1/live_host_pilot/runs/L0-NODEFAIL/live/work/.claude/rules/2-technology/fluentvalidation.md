---
paths:
  - "backend/**/*.cs"
---

> Level: 2 Technology · Owns: FluentValidation binding of the validation boundaries · Scope: backend · Loads: path rule · Depends on: CLAUDE.md, .claude/rules/1-architecture/outcomes.md

# FluentValidation Binding

- Use FluentValidation for explicit request and use-case validation where validation is needed — required application input, string and collection constraints, ranges, cross-property and conditional rules — while each rule stays at the owning boundary defined in `1-architecture/outcomes.md`.
- Application-level validators live in Application and are registered with `FluentValidation.DependencyInjectionExtensions` from Application's own registration.
- Follow the project's established validation invocation pattern rather than adding a second competing mechanism; do not adopt a deprecated or legacy ASP.NET automatic-validation integration package unless a concrete project requirement justifies it (default).

Technique: the `aspnet-error-handling` skill.
