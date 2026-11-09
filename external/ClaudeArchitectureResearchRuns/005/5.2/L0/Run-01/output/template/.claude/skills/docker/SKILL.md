---
name: docker
description: >
  Use for Dockerfiles, Compose, or container deployment: multi-stage builds, runtime images, non-root, configuration and secrets, probes.
---

> Level: 2 Technology | Owns: container technique | Scope: delivery, backend | Loads: knowledge skill (on demand) | Depends on: 2-technology/containers.md

# Docker Technique

Policy owners (routing): Docker is optional → `3-project/decisions.md`; runtime
image and root use → `2-technology/containers.md`; secrets →
`0-core/security-principles.md`; production migrations and seeding → `develop`
(CI/CD and deployment), `3-project/data-lifecycle.md`; health semantics →
`0-core/health-principles.md`.

Keep build tooling out of runtime images, configuration external, and Docker
concerns out of Domain and Application code.

## ASP.NET Core Dockerfile

```dockerfile
FROM mcr.microsoft.com/dotnet/sdk:10.0 AS build
WORKDIR /src

COPY Directory.Build.props ./
COPY Directory.Packages.props ./
COPY backend/MyApp.Domain/MyApp.Domain.csproj backend/MyApp.Domain/
COPY backend/MyApp.Application/MyApp.Application.csproj backend/MyApp.Application/
COPY backend/MyApp.Infrastructure/MyApp.Infrastructure.csproj backend/MyApp.Infrastructure/
COPY backend/MyApp.Api/MyApp.Api.csproj backend/MyApp.Api/
RUN dotnet restore backend/MyApp.Api/MyApp.Api.csproj

COPY . .
RUN dotnet publish backend/MyApp.Api/MyApp.Api.csproj \
    --configuration Release --output /app/publish --no-restore

FROM mcr.microsoft.com/dotnet/aspnet:10.0 AS runtime
WORKDIR /app
COPY --from=build /app/publish .
USER app
EXPOSE 8080
ENTRYPOINT ["dotnet", "MyApp.Api.dll"]
```

- Copy project and build files before the full source so source edits do not
  invalidate the restore layer; copy only build files that exist, and update
  the project-copy section when the solution structure changes. Avoid wildcard
  tricks that flatten the multi-project layout.
- Workers that do not need ASP.NET Core use the plain .NET runtime image.
- `USER app` uses the built-in non-root user of modern .NET images; make
  writable directories owned appropriately.

## Configuration and Secrets

Pass environment-specific values at runtime (`ASPNETCORE_ENVIRONMENT`,
`ConnectionStrings__DefaultConnection`, `Authentication__Authority`). Typical
credential leaks in container builds are Dockerfiles, committed Compose files,
build arguments visible in image metadata, and copied appsettings files; supply
secrets through platform or container secret mechanisms instead.

## Compose for Local Development

```yaml
services:
  api:
    build:
      context: .
      dockerfile: backend/MyApp.Api/Dockerfile
    ports:
      - "5000:8080"
    environment:
      ASPNETCORE_ENVIRONMENT: Development
      ConnectionStrings__DefaultConnection: ${DB_CONNECTION_STRING}
```

Add only services the project uses (no speculative PostgreSQL, Redis,
RabbitMQ); keep local passwords in an ignored `.env` file.

## Health Probes

Prefer the orchestrator's native HTTP probes against the liveness/readiness
endpoints (`health-check` skill). Runtime images may lack `curl`, `wget`, or a
shell; verify an in-container probe command exists before using it, and weigh
adding debugging packages to a production image.

## Angular Container

Build static assets in a Node stage and serve them with the selected hosting
strategy (Nginx is not mandatory; the platform may host static files); keep the
API base URL compatible with the deployment.

## .dockerignore

```text
.git
.vs
**/bin
**/obj
**/node_modules
TestResults
coverage
```

Do not exclude files restore or build needs, or tests the image build runs.

## Image Optimization

Start with standard supported images. Alpine, chiseled images, trimming, or
Native AOT only when requirements justify them, after verifying globalization,
native dependencies, reflection, and diagnostics.

## Verification

Build the image, verify startup, required port and configuration, non-root
behavior, and probe integration, and review the image for accidental secrets or
files; run application tests outside or within the pipeline.
