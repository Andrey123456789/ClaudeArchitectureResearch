---
name: docker
description: >
  Use for Dockerfiles, .dockerignore, Compose files, or container deployment:
  multi-stage builds, restore caching, non-root execution, runtime
  configuration and secrets, health probes.
---

> Knowledge skill · Container technique · Policy: `docs/technology-stack.md` § Conditional Technologies (Docker is optional), `.claude/rules/security.md` § Containers and § Secrets · Delivery checks: `verify` § Delivery Changes

# Docker

Keep build tooling out of production runtime images, keep images reproducible
and configuration external, keep Docker concerns separate from application
architecture, and use the deployment platform's health-probe capabilities when
practical.

## ASP.NET Core Dockerfile

Use a multi-stage build:

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

The example assumes the repository-level build files exist; copy only build
files that are present and required by restore, and do not add them merely to
satisfy the Dockerfile. Copy project files required for restore explicitly; do
not use wildcard tricks that flatten or rearrange the multi-project structure.

## Restore Caching

Copy project and build-dependency files before the full source tree so source
changes do not invalidate NuGet restore layers. Update the project-copy section
when the solution structure changes; never optimize layer caching at the cost of
a Dockerfile that no longer restores the real project graph.

## Runtime Image

Use the ASP.NET runtime image for ASP.NET Core applications and an appropriate
.NET runtime image for workers that do not require ASP.NET Core.

## Non-Root

Use the built-in non-root user of modern .NET images when it fits the image and
deployment environment (`USER app`), and give directories the application
writes to appropriate ownership and permissions.

## Configuration and Secrets

Pass environment-specific configuration at runtime, for example
`ASPNETCORE_ENVIRONMENT`, `ConnectionStrings__Default`,
`Authentication__Authority`. Real credentials never go into a Dockerfile,
committed Compose files, build arguments visible in image metadata, or copied
appsettings files; use platform or container secret mechanisms.

## Docker Compose for Development

Compose helps run local infrastructure such as a database or Redis when the
project benefits from it:

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

Add only the infrastructure the project actually uses — not PostgreSQL, Redis,
RabbitMQ, or another service merely because examples commonly include it. Keep
local passwords in a local `.env` or another ignored developer mechanism.

## Health Probes

Expose liveness/readiness endpoints through ASP.NET Core health checks
(`health-check` skill) and prefer the orchestrator's native HTTP probes. Do not
assume the runtime image contains `curl`, `wget`, or shell utilities; when
Compose must run an in-container health command, verify the executable exists or
add an appropriate probe mechanism, weighing the cost of installing debugging
packages into a production image.

## Frontend Container

When the frontend is deployed as a static application, build it in a Node build
stage and serve the generated assets with the selected hosting strategy; Nginx
is not mandatory, since the platform may provide static hosting. Keep API base
URLs and environment configuration compatible with that strategy.

## `.dockerignore`

Exclude what does not belong in the build context:

```text
.git
.vs
**/bin
**/obj
**/node_modules
TestResults
coverage
```

Do not exclude tests when the image build intentionally runs them, and never
exclude files required by restore or build.

## Image Optimization

Start with standard supported .NET runtime images. Consider Alpine, chiseled
images, trimming, Native AOT, or other size optimizations only when
compatibility and deployment requirements justify them, and verify
globalization, native dependencies, reflection, and diagnostics when using
specialized images.

## Verification

For Docker changes: build the image, verify application startup, required
port/configuration, non-root behavior when relevant, and health-probe
integration, and review the image for accidental secrets or files. Run
meaningful application tests outside or as part of the build pipeline.

## Review Checks

Check-by-reference against `security.md` § Containers and `verify` § Delivery
Changes: SDK image as production runtime; root execution without a concrete
reason; secrets baked into images; arbitrary infrastructure in Compose; assumed
`curl`/`wget`; automatic production database migration; specialized image
variants without compatibility verification; Docker-specific changes leaking
into Domain or Application code.
