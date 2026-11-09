---
name: docker
description: Use when adding or reviewing Dockerfiles, Docker Compose files or container deployment configuration for the .NET backend or the frontend — multi-stage builds, restore-layer caching, non-root execution, .dockerignore, configuration and secrets, health probes and image verification.
---
Kind: KNW | Scope: delivery | Capability: — | Loading: on invocation

# Docker

Rules: decision register → Conditional technologies (containers only when needed), `.claude/rules/backend/operations.md` → Containers (runtime image, root), `.claude/rules/common/security.md` (secrets). Production migration and seeding behavior: `verify` → Delivery and deployment changes. Keep Docker concerns separate from application architecture, images reproducible and configuration external.

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

Copy only the repository-level build files that exist and that restore needs. Copy project files explicitly; avoid fragile wildcard tricks that flatten or rearrange a multi-project structure.

## Restore caching

Copy project and build files before the full source tree so source changes do not invalidate the restore layer, and update the project-copy section when the solution structure changes. Layer caching never justifies a Dockerfile that no longer restores the real project graph.

## Runtime image and user

Rules: `operations.md` → Containers. Image names: `mcr.microsoft.com/dotnet/aspnet` for ASP.NET Core applications, `mcr.microsoft.com/dotnet/runtime` for workers without ASP.NET Core. Modern .NET images include a non-root `app` user (`USER app`) when it fits the deployment; give directories the application writes to appropriate ownership and permissions.

## Configuration and secrets

Pass environment-specific configuration at runtime, for example `ASPNETCORE_ENVIRONMENT`, `ConnectionStrings__Default`, `Authentication__Authority`. Real credentials never go into a Dockerfile, a committed Compose file, build arguments that stay visible in image metadata, or copied appsettings files with production secrets; use platform or container secret mechanisms.

## Docker Compose for development

Compose helps run local infrastructure such as a database when the project benefits from it:

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

Add only infrastructure the project actually uses, and keep local passwords in an ignored `.env` file or another ignored developer configuration.

## Health probes

Application health behavior: `health-check` skill. Prefer native HTTP probes from the orchestrator. Do not assume the runtime image contains `curl`, `wget` or shell utilities; if Compose must run an in-container health command, verify the image provides it or add an appropriate probe mechanism, weighing the size and attack-surface trade-off.

## Frontend container

A static frontend builds in a Node stage and is served by the selected hosting strategy; frontend specifics: the frontend knowledge facet (decision register).

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

Do not exclude files restore or build need, and do not exclude tests blindly when the image build intentionally runs them.

## Image optimization

Start with the standard supported .NET images. Consider Alpine, chiseled images, trimming or Native AOT only when compatibility and deployment requirements justify them, and verify globalization, native dependencies, reflection and diagnostics when you do.

## Verification

Build the image, verify startup, the required port and configuration, non-root behavior when relevant and health-probe integration, and review the image for accidental secrets or files. Run the application tests outside or as part of the selected pipeline.

## Anti-patterns

Review checks; the named standard owns each rule:

- The SDK image as production runtime, or root execution without a reason? (`operations.md`)
- Secrets baked into images or Compose files? (`.claude/rules/common/security.md`)
- Arbitrary infrastructure services in Compose, or Docker added without a need? (decision register)
- `curl`/`wget` assumed in runtime images?
- Automatic production migrations at startup? (`verify` → Delivery and deployment changes)
- Docker-specific code leaking into Domain or Application?
