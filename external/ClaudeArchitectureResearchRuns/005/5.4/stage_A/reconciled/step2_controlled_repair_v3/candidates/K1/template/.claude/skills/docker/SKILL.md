---
name: docker
description: >
  Use when writing or reviewing Dockerfiles or Compose files: multi-stage .NET
  builds, restore caching, runtime images, non-root user, .dockerignore,
  container configuration and secrets, health probes, static frontend images.
---

> Kind: KNW | Scope: delivery | Capability: — | Loading: on-demand knowledge

# Docker

Containers are optional infrastructure (decision register). Policy: `.claude/rules/backend/operations.md` (runtime image, non-root), `.claude/rules/common/security.md` (secrets). Procedure: `delivery-change`. Keep build tooling out of production images, configuration external, images reproducible, and Docker concerns out of Domain/Application code.

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

Copy only repository-level build files that exist and are needed for restore; never add them just to satisfy the example. Copy project files explicitly — no wildcard tricks that flatten or rearrange the multi-project structure — and update this section when the solution structure changes. Never optimize layer caching at the cost of restoring the wrong project graph.

## Runtime image and user

Use the ASP.NET runtime image (`mcr.microsoft.com/dotnet/aspnet`) for ASP.NET Core and an appropriate .NET runtime image for workers. Use the built-in non-root `app` user of modern .NET images when it fits, and give directories the application writes to the right ownership and permissions.

## Configuration and secrets

Pass environment-specific configuration at runtime (`ASPNETCORE_ENVIRONMENT`, `ConnectionStrings__Default`, `Authentication__Authority`) and supply secrets through platform/container secret mechanisms. Surfaces to check for credentials: the Dockerfile, committed Compose files, build arguments (visible in image metadata), and copied appsettings files.

## Compose for local development

Useful for local infrastructure such as a database or cache when the project benefits from it; add only services the project uses, and keep local passwords in an ignored `.env` or similar mechanism.

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

## Health probes

Expose liveness/readiness through ASP.NET Core health checks (`health-check`) and prefer orchestrator-native HTTP probes. Runtime images may lack `curl`, `wget`, or a shell; if Compose must run an in-container health command, verify the executable exists or add an explicit probe mechanism, weighing the cost of extra packages in production images.

## Static frontend container

When the frontend is deployed as static assets, build it in a Node stage and serve the output with the selected hosting strategy (a web server image is not mandatory when the platform hosts static files). Keep API base URLs and environment configuration compatible with that strategy.

## .dockerignore

Exclude `.git`, `.vs`, `**/bin`, `**/obj`, `**/node_modules`, `TestResults`, `coverage`; do not exclude tests the image build intentionally runs or files restore/build needs.

## Image optimization

Start with standard supported images. Consider Alpine, chiseled images, trimming, or Native AOT only when compatibility and deployment requirements justify them, and verify globalization, native dependencies, reflection, and diagnostics when you do.

## Migrations and seeding

Container deployment does not change the production migration or Development-only seeding policies (`delivery-change`, `.claude/rules/backend/persistence.md`).

## Verification

Build the image, verify application startup, required port/configuration, non-root behavior when relevant, health-probe integration, and the absence of accidental secrets/files; run meaningful tests outside or as part of the pipeline.
