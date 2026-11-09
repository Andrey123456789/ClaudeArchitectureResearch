---
paths:
  - "**/Dockerfile*"
  - "**/.dockerignore"
  - "**/docker-compose*.yml"
  - "**/docker-compose*.yaml"
  - "**/compose*.yml"
  - "**/compose*.yaml"
---

> Level: 2 Technology | Owns: production container image rules | Scope: backend, delivery | Loads: path (container files) | Depends on: 0-core/security-principles.md

# Containers

- Default: production containers use an appropriate runtime image
  (`mcr.microsoft.com/dotnet/aspnet` for ASP.NET Core) rather than the SDK image
  solely for convenience; do not switch to root merely to bypass a filesystem
  permission problem.

Technique: → `docker` skill. Pipelines and deployment: → `develop` (CI/CD and deployment), `ci-cd` skill.
