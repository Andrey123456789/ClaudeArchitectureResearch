---
name: docker
description: >
  Use for Dockerfiles, Compose files, .dockerignore, and container deployment:
  multi-stage builds, restore caching, non-root users, runtime configuration,
  health probes.
---

> Knowledge skill. Owns: container technique and examples · Scope: delivery, backend, frontend · Loads: on demand · Depends on: CLAUDE.md, docs/technology-stack.md, .claude/rules/security.md

# Docker

Whether to containerize at all: `docs/technology-stack.md` (Conditional
Technologies). Rules: `security.md` (secrets, runtime image, root). Production
migrations and Development seeding in deployment: `development-workflow`
(Database deployment). Keep Docker concerns out of Domain and Application code,
keep images reproducible, and keep configuration external.

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

Copy only repository-level build files that exist and are required by restore,
and copy project files explicitly; avoid wildcard tricks that flatten or
rearrange a multi-project structure.

## Restore Caching

Copy project and build-dependency files before the full source tree so source
changes do not invalidate the NuGet restore layer. Update the project-copy
section when the solution structure changes; layer caching never justifies a
Dockerfile that no longer restores the real project graph.

## Runtime Images and Non-Root

Use the ASP.NET runtime image for ASP.NET Core applications and an appropriate
.NET runtime image for workers. The built-in non-root user of modern .NET images
(`USER app`) fits most deployments; give directories the application writes to
the right ownership and permissions instead of switching to root.

## Configuration and Secrets

Pass environment-specific configuration at runtime, for example
`ASPNETCORE_ENVIRONMENT`, `ConnectionStrings__Default`,
`Authentication__Authority`. Places where real credentials leak: the
Dockerfile, committed Compose files, build arguments that remain in image
metadata, and copied appsettings files; use platform/container secret
mechanisms instead (`security.md`, Secrets).

## Docker Compose for Development

Compose is useful for local infrastructure such as a database when the project
benefits from it:

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

Add only infrastructure the project actually uses, and keep local passwords in a
local `.env` or another ignored developer configuration instead of committed
files.

## Health Probes

Application health behavior: `health-check` skill. Prefer the orchestrator's
native HTTP probes. Runtime images may lack `curl`, `wget`, or shell utilities;
if Compose must run an in-container health command, verify the executable
exists or add an appropriate probe mechanism, weighing the cost of extra
packages in a production image.

## Angular Container

When the frontend is deployed as a static application, build it in a Node stage
and serve the generated assets with the selected hosting strategy; Nginx is not
mandatory if the platform provides static hosting. Keep the API base URL and
environment configuration compatible with the deployment strategy.

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

Do not exclude files needed by restore/build, or tests that the image build
intentionally runs.

## Image Optimization

Start with the standard supported .NET runtime images. Alpine, chiseled images,
trimming, or Native AOT are options when compatibility and deployment
requirements justify them; verify globalization, native dependencies,
reflection, and diagnostics when using them.

## Verification

```text
build the image
verify application startup
verify required port/configuration
verify non-root behavior when relevant
verify health probe integration
review the image for accidental secrets/files
```

Run meaningful application tests outside or as part of the build pipeline.
