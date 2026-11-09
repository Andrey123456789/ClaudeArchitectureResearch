---
name: docker
description: >
  Use when adding or reviewing Dockerfiles, .dockerignore, Docker Compose for
  local infrastructure, container configuration and secrets, non-root
  execution, container health probes, Angular static-asset images, or container
  build verification.
---

> Owns: container technique for .NET and Angular | Scope: delivery | Loads: on demand (knowledge skill)

# Docker

Policy owners: Docker is optional → `docs/technology-stack.md`; runtime image and
root usage → `.claude/rules/delivery.md`; no secrets in images or Compose →
`.claude/rules/security.md`; production migrations and seeding →
`.claude/rules/persistence.md`. Keep Docker concerns out of Domain and
Application code.

## ASP.NET Core Multi-Stage Dockerfile

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
    --configuration Release --output /app/publish --no-restore

FROM mcr.microsoft.com/dotnet/aspnet:10.0 AS runtime
WORKDIR /app
COPY --from=build /app/publish .
USER app
EXPOSE 8080
ENTRYPOINT ["dotnet", "MyApp.Api.dll"]
```

- Copy only repository-level build files that exist and restore needs.
- Copy project files explicitly before the full source so source edits do not
  invalidate the restore layer; update this section when projects change. Avoid
  wildcard tricks that flatten the multi-project tree.
- Workers without ASP.NET Core use the plain .NET runtime image.
- `USER app` is the built-in non-root user of modern .NET images; fix
  permission problems by giving writable directories the right ownership
  (`chown` in the build stage, volume ownership) — root usage: `delivery.md`.

## Configuration and Secrets

Pass environment-specific values at runtime (`ASPNETCORE_ENVIRONMENT`,
`ConnectionStrings__DefaultConnection`, `Authentication__Authority`). Secrets
policy: `security.md`. Container specifics: build arguments stay visible in image
metadata and copied appsettings files ship inside the image, so supply
credentials through platform/container secret mechanisms or an ignored local
`.env`.

## Docker Compose for Development

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

Add only infrastructure the project actually uses (no speculative PostgreSQL,
Redis, or RabbitMQ).

## Health Probes

Expose liveness/readiness through ASP.NET Core health checks (`health-check`)
and prefer the orchestrator's native HTTP probes. Runtime images may lack
`curl`, `wget`, or a shell; if Compose must run an in-container health command,
verify the executable exists or add a deliberate probe mechanism rather than
bloating the production image.

## Angular Container

Build static assets in a Node stage (`npm ci`, then the project's build script)
and serve them with the chosen hosting strategy; Nginx is not mandatory when the
platform hosts static files. Keep the API base URL compatible with the
deployment.

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

Do not exclude files restore/build needs, or tests if the image build runs them.

## Image Optimization

Start with standard supported images. Alpine, chiseled images, trimming, or
Native AOT only when compatibility and deployment requirements justify them —
then verify globalization, native dependencies, reflection, and diagnostics.

## Verification

Build the image; verify startup, ports and configuration, non-root behavior,
health-probe integration; inspect the image for accidental secrets or files.
Run meaningful tests in the build pipeline or outside the image.
