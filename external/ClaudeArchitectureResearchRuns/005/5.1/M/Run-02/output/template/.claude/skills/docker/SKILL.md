---
name: docker
description: >
  Use when writing or reviewing a Dockerfile, .dockerignore, or Compose file
  for ASP.NET Core or Angular: multi-stage builds, restore caching, non-root
  user, runtime configuration, health probes, image variants.
---

> Owner: container technique and examples (normative policy lives in rules) | Scope: delivery | Loads: on demand — knowledge | Enforced: none

# Docker

Policy: `.claude/rules/delivery.md` § Containers (runtime image, no root
shortcut), `docs/technology-stack.md` § Conditional Technologies (Docker only
when needed), `.claude/rules/security.md` § Secrets,
`.claude/rules/persistence.md` § Migrations. Keep Docker concerns out of
application architecture.

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

Copy only repository-level build files that exist and that restore needs (also
`global.json` when present). Copy project files explicitly; avoid wildcard tricks
that flatten or rearrange the multi-project structure. Use the .NET runtime image
(not ASP.NET) for workers that do not need ASP.NET Core.

## Restore Caching

Copy project and build files before the full source tree so source changes do not
invalidate the restore layer. Update the project-copy section when the solution
structure changes; a cache-friendly Dockerfile that no longer restores the real
project graph is broken.

## Non-Root

Modern .NET images ship a non-root `app` user (`USER app`). Give directories the
application writes to the right ownership and permissions; understand a
permission error before changing the user.

## Configuration and Secrets

Pass environment-specific configuration at runtime:

```text
ASPNETCORE_ENVIRONMENT
ConnectionStrings__Default
Authentication__Authority
```

Keep real credentials out of the Dockerfile, committed Compose files, build
arguments (they persist in image metadata), and copied appsettings files; use
platform or container secret mechanisms.

## Docker Compose for Development

Useful for local infrastructure such as a database when the project benefits:

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

Add only infrastructure the project actually uses, and keep local passwords in an
ignored `.env` or another ignored developer configuration mechanism.

## Health Probes

Application health behavior: `health-check` skill. Prefer the orchestrator's
native HTTP probes. Runtime images may lack `curl`, `wget`, or a shell; if Compose
must run an in-container health command, verify the executable exists or add an
appropriate probe mechanism, weighing the cost of adding debugging packages to a
production image.

## Angular Container

For static deployment, build in a Node stage and serve the generated assets with
the chosen hosting strategy; Nginx is one option, not a requirement — the
platform may host static files directly. Keep the API base URL and environment
configuration compatible with that strategy (`angular` skill).

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

Do not exclude files restore or build needs, and do not exclude tests if the image
build intentionally runs them.

## Image Optimization

Start with the standard supported runtime images. Consider Alpine, chiseled
images, trimming, or Native AOT only when compatibility and deployment
requirements justify them, and then verify globalization, native dependencies,
reflection, and diagnostics behavior.

## Verification

```text
build the image
verify application startup
verify the required port and configuration
verify non-root behavior when relevant
verify health-probe integration
review the image for accidental secrets or files
```

Run meaningful application tests outside the image or as part of the selected
pipeline.

## Common Mistakes

- arbitrary infrastructure services in Compose;
- assuming curl or wget exists in runtime images;
- specialized image variants without compatibility verification;
- Docker-specific code leaking into Domain or Application.
