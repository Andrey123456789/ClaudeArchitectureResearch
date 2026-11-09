---
name: docker
description: Use when adding or reviewing Dockerfiles, .dockerignore or Compose — multi-stage builds, restore caching, non-root runtime, runtime configuration and secrets, probes, image size.
---

> Kind: KNW | Scope: delivery | Owner: container technique with examples | Loading: on demand (model-invoked knowledge)

# Docker

Rules: `rules/backend/hosting.md` § Containers, `rules/common/security.md` § Secrets. Decision: D-14 (containers are optional). Workflow: `delivery-pipeline` (container and deployment changes).

Keep build tooling out of production runtime images, configuration external, images reproducible and Docker concerns out of the application architecture; prefer the deployment platform's health-probe capabilities.

## ASP.NET Core Dockerfile

Multi-stage build:

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

Copy only the repository-level build files that exist and restore needs, and copy project files explicitly — wildcard tricks can flatten or rearrange the multi-project structure. Use the .NET runtime image (not `aspnet`) for workers that do not need ASP.NET Core.

## Restore caching

Copy project and build files before the full source so source changes do not invalidate the NuGet restore layer. When the solution structure changes, update the project-copy section; a correct restore graph matters more than layer caching.

## Non-root execution

Modern .NET images provide a built-in non-root user (`USER app`). Give directories the application writes to the right ownership and permissions, and understand a permission problem before reaching for root.

## Configuration and secrets

Pass environment-specific configuration at runtime:

```text
ASPNETCORE_ENVIRONMENT
ConnectionStrings__Default
Authentication__Authority
```

Real credentials stay out of the Dockerfile, committed Compose files, build arguments visible in image metadata and copied appsettings files (`rules/common/security.md` § Secrets); use platform/container secret mechanisms.

## Docker Compose for development

Compose helps run local infrastructure (a database, Redis) when the project benefits from it:

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

Add only the infrastructure the project actually uses — not PostgreSQL, Redis or RabbitMQ because they are common in examples — and keep local passwords in an ignored `.env` or similar developer configuration.

## Health probes

Expose liveness/readiness through ASP.NET Core health checks (`health-check`) and prefer the orchestrator's native HTTP probes. Runtime images may lack `curl`, `wget` or a shell: if Compose itself runs an in-container health command, verify the executable exists or add a deliberate probe mechanism, weighing the cost of debugging packages in a production image.

## Angular container

For a static Angular deployment, build in a Node stage and serve the generated assets with the chosen hosting strategy; Nginx is not mandatory when the platform hosts static files. Keep API base URLs and environment configuration compatible with that strategy.

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

Keep files required by restore/build, and keep tests when the image build intentionally runs them.

## Image optimization

Start from standard supported .NET images. Alpine, chiseled images, trimming or Native AOT come in only when compatibility and deployment requirements justify them — verify globalization, native dependencies, reflection and diagnostics when using them.

## Verification

Build the image; verify application startup, required port and configuration, non-root behavior when relevant and health-probe integration; review the image for accidental secrets or files. Run meaningful application tests outside the image or as part of the build pipeline.

## Common mistakes

SDK image as production runtime; root execution without reason; secrets baked into images; arbitrary infrastructure in Compose; assuming `curl`/`wget` exist; production migrations at application startup (see also: `delivery-pipeline` § 3); specialized image variants without compatibility checks; Docker concerns leaking into Domain/Application code.
