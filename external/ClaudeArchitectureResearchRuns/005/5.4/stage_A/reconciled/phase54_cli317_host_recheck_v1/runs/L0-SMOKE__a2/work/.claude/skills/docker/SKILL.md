---
name: docker
description: >
  Use for Dockerfiles, .dockerignore, or Compose: multi-stage .NET/Angular images,
  restore caching, runtime image, non-root, runtime configuration, health probes.
---

> Level: 2 Technology · Owns: container technique and examples (knowledge) · Scope: backend, frontend, delivery · Loads: on invocation · Depends on: .claude/rules/2-technology/containers-ci.md

# Docker

Policy owners: Docker is optional → `3-project/decisions.md`; runtime image, non-root, no baked secrets → `.claude/rules/2-technology/containers-ci.md`; secrets → `0-core/security-principles.md`; production migrations and seeding → `delivery-pipeline`; procedure for container changes → `delivery-pipeline`. Keep Docker concerns out of Domain/Application code. This skill is technique only.

## ASP.NET Core multi-stage Dockerfile

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
    --configuration Release \
    --output /app/publish \
    --no-restore

FROM mcr.microsoft.com/dotnet/aspnet:10.0 AS runtime
WORKDIR /app
COPY --from=build /app/publish .
USER app
EXPOSE 8080
ENTRYPOINT ["dotnet", "MyApp.Api.dll"]
```

Copy only the repository-level build files that exist and are needed by restore. Copy project files explicitly before the source tree so source changes do not invalidate the NuGet restore layer; update this section when the solution structure changes. Avoid wildcard tricks that flatten or rearrange a multi-project tree. Workers without ASP.NET Core use the plain .NET runtime image.

## Non-root

`USER app` uses the built-in non-root user of modern .NET images. Make directories the application writes to owned and permitted correctly instead of switching to root.

## Configuration and secrets

Pass environment-specific configuration at run time (`ASPNETCORE_ENVIRONMENT`, `ConnectionStrings__Default`, `Authentication__Authority`). Where secrets must never go is owned by `containers-ci.md`; remember that build arguments stay visible in image metadata and copied appsettings files ship inside the image, so supply secrets through the platform/container secret mechanism.

## Compose for local development

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
      ConnectionStrings__Default: ${DB_CONNECTION_STRING}
```

Add only the infrastructure the project actually uses (no PostgreSQL, Redis, or RabbitMQ because examples have them); keep local passwords in an ignored `.env` file.

## Health probes

Expose liveness/readiness through ASP.NET Core health checks (`health-check` skill) and prefer the orchestrator's native HTTP probes. Runtime images may not contain `curl`, `wget`, or a shell — verify before using an in-container health command, and weigh adding debugging packages to a production image.

## Angular container

For static deployment build in a Node stage and serve the output with the chosen hosting strategy; Nginx is not mandatory when the platform hosts static files. Keep API base URLs compatible with the deployment.

## `.dockerignore`

```text
.git
.vs
**/bin
**/obj
**/node_modules
TestResults
coverage
```

Do not exclude tests if the image build intentionally runs them, or files restore/build needs.

## Image optimization

Start with standard supported images. Consider Alpine, chiseled images, trimming, or Native AOT only when compatibility and deployment requirements justify them, and verify globalization, native dependencies, reflection, and diagnostics afterwards.

## Verification

Container verification steps: `delivery-pipeline` → Verify. Run meaningful application tests outside or as part of the selected pipeline.
