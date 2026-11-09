---
name: docker
description: >
  Dockerfiles, .dockerignore, Compose: multi-stage .NET and frontend images,
  restore caching, runtime image, non-root USER, runtime configuration and
  secrets, health probes.
---

> **Knowledge skill** · Owns: container technique and examples · Scope: backend, frontend · Loading: on demand

# Docker

## Rules

Rules: `docs/technology-stack.md` → Conditional Technologies (Docker only when
needed), `security.md` → Containers and Secrets. Production migrations and
seeding in deployments: `development-workflow` → Change-Specific Obligations.

1. Keep images reproducible and configuration external.
2. Keep Docker concerns separate from application architecture.
3. Use the deployment platform's health-probe capabilities when practical.

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

The example assumes these repository-level build files exist.

Copy only repository-level build files that are actually present and required by
restore. Do not add `Directory.Build.props` or `Directory.Packages.props` merely
to satisfy the Dockerfile example.

Explicitly copy project files required for restore.

Do not use fragile wildcard tricks that flatten or accidentally rearrange
multi-project directory structure.

## Restore Caching

Copy project/build dependency files before the complete source tree so source
changes do not unnecessarily invalidate NuGet restore layers.

When the solution structure changes, update the Dockerfile's project-copy
section.

Do not optimize Docker layer caching at the cost of a Dockerfile that no longer
restores the actual project graph correctly.

## Runtime Image

Use the ASP.NET runtime image for ASP.NET Core applications and an appropriate
.NET runtime image for workers that do not require ASP.NET Core
(`security.md` → Containers).

## Non-Root

Use the built-in non-root user supported by modern .NET container images
(`security.md` → Containers):

```dockerfile
USER app
```

Ensure directories the application writes to have appropriate ownership and
permissions instead of switching to root.

## Configuration and Secrets

Pass environment-specific configuration at runtime.

Examples include:

```text
ASPNETCORE_ENVIRONMENT
ConnectionStrings__Default
Authentication__Authority
```

Supply credentials through platform/container secret mechanisms; build arguments
remain visible in image metadata and copied appsettings files travel with the
image (`security.md` → Containers).

## Docker Compose Development

Compose is useful for local infrastructure such as databases or Redis when the
project benefits from it.

Example shape:

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

Add only the infrastructure the project actually uses.

Do not add PostgreSQL, Redis, RabbitMQ, or another service merely because it is
common in examples.

Do not commit real local passwords when a local `.env` or another ignored
developer configuration mechanism is more appropriate.

## Health Probes

Application health behavior belongs to the `health-check` skill.

Expose appropriate liveness/readiness endpoints through ASP.NET Core health
checks.

Prefer native HTTP probes supplied by the orchestrator when available.

Do not assume the runtime image contains:

```text
curl
wget
shell utilities
```

If Docker Compose itself must execute an in-container health command, verify the
chosen runtime image actually provides the required executable or explicitly add
an appropriate probe mechanism.

Do not install large debugging packages into a production image solely for a
health check without considering the trade-off.

## Frontend Container

When the frontend is deployed as a static application, build it in a
Node build stage and serve the generated assets using the selected hosting
strategy.

Do not assume Nginx is mandatory; the deployment platform may provide static
hosting directly.

Keep API base URLs and environment configuration compatible with the selected
deployment strategy.

Frontend architecture belongs to `frontend.md` and the frontend knowledge facet.

## `.dockerignore`

Exclude files that do not belong in the build context, for example:

```text
.git
.vs
**/bin
**/obj
**/node_modules
TestResults
coverage
```

Do not blindly exclude tests if the Docker build or CI process intentionally
runs tests inside the image build.

Do not exclude files required by restore/build.

## Image Optimization

Start with standard supported .NET runtime images.

Consider Alpine, chiseled images, trimming, Native AOT, or other image-size
optimizations only when compatibility and deployment requirements justify them.

Do not make trimming or Alpine the default merely to minimize image size.

Verify globalization, native dependencies, reflection, diagnostics, and other
runtime behavior when using specialized images.

## Database Migrations

Container deployment does not change the project's migration and seeding policy
(`development-workflow` → Change-Specific Obligations).

## Verification

For Docker changes:

```text
build the image
verify application startup
verify required port/configuration
verify non-root behavior when relevant
verify health probe integration
review image for accidental secrets/files
```

Run meaningful application tests outside or as part of the selected build
pipeline.

## Anti-Patterns

Avoid:

- arbitrary infrastructure services in Compose;
- assuming curl/wget exists in runtime images;
- specialized image variants without compatibility verification;
- Docker-specific changes leaking into Domain/Application code.
