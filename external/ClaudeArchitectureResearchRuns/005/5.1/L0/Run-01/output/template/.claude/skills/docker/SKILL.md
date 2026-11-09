---
name: docker
description: >
  Use when adding or reviewing Dockerfiles, Compose files or container
  deployment: multi-stage builds, runtime images, non-root user, .dockerignore,
  configuration and secrets, health probes.
---

> Level: 2 Technology · Owns: container technique · Scope: delivery · Loads: on demand (knowledge skill)

# Docker

Policy owners: `.claude/rules/2-technology/containers-ci.md` (runtime image, non-root), `.claude/rules/0-core/security-principles.md` (no secrets in images or committed files). Whether to containerize at all is a conditional-technology entry in the project decisions; production migrations and seeding follow the project's data-lifecycle rule. Keep Docker concerns out of Domain and Application code.

## ASP.NET Core multi-stage Dockerfile

```dockerfile
FROM mcr.microsoft.com/dotnet/sdk:10.0 AS build
WORKDIR /src

COPY Directory.Build.props Directory.Packages.props ./
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

- Copy only repository-level build files that exist and restore needs; do not create them just for the Dockerfile.
- Copy project files explicitly before the full source so source edits do not invalidate the restore layer; avoid wildcard tricks that flatten the multi-project tree. Update this section when the solution structure changes.
- Workers that do not need ASP.NET Core use `mcr.microsoft.com/dotnet/runtime`.

## Non-root

Modern .NET images ship a non-root `app` user (`USER app`, default port 8080). Make directories the application writes to owned by that user (`RUN mkdir /app/data && chown app /app/data` in a root stage, or a writable volume) instead of switching to root.

## Configuration and secrets

Pass environment-specific configuration at runtime (`ASPNETCORE_ENVIRONMENT`, `ConnectionStrings__DefaultConnection`, `Authentication__Authority`). Places where secrets typically leak into images: the Dockerfile, committed Compose files, build arguments (visible in image metadata) and copied appsettings files — supply them through platform or container secret mechanisms instead.

## Compose for local development

Useful for local infrastructure the project actually uses (for example SQL Server):

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

Keep local passwords in an ignored `.env` file. Do not add PostgreSQL, Redis, RabbitMQ or other services because examples commonly include them.

## Health probes

Expose ASP.NET Core liveness/readiness endpoints (`health-check` skill) and prefer the orchestrator's native HTTP probes. Runtime images may not contain `curl`, `wget` or a shell; if Compose must run an in-container health command, verify the executable exists or add a deliberate probe mechanism rather than large debugging packages.

## Angular container

Build in a Node stage and serve the generated static assets with the chosen hosting strategy — Nginx is not mandatory when the platform provides static hosting. Keep the API base URL and environment configuration compatible with that strategy.

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

Do not exclude files restore/build needs, or tests the image build intentionally runs.

## Image optimization

Start with the standard runtime images. Alpine, chiseled images, trimming or Native AOT are considered only when compatibility and deployment requirements justify them — verify globalization, native dependencies, reflection and diagnostics afterwards.

## Verification

Build the image; verify startup, port and configuration; non-root behavior when relevant; health-probe integration; and that no secrets or stray files were copied. Run application tests outside the image or within the selected pipeline.

## Review cues

SDK image as production runtime, root execution without reason, secrets baked into layers, arbitrary Compose services, assumed `curl`/`wget`, automatic production migration on startup, specialized images without compatibility checks, Docker specifics leaking into Domain/Application.
