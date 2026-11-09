---
name: docker
description: Use when adding or reviewing Dockerfiles, Compose files or container deployment configuration for the .NET API or Angular frontend — multi-stage builds, restore-layer caching, runtime images, non-root users, .dockerignore, runtime configuration, health probes, image size.
---
<!-- Kind: KNW | Scope: delivery | Owns: container technique and examples | Loads: on demand (model-invoked) -->
# Docker

Adoption: DEC-OPS-01 (optional). Standards: `rules/backend/operations.md` § Containers (runtime image, root) and `rules/common/security.md` § Secrets. Container build/publish and verification procedure: `delivery-pipeline`.

Keep build tooling out of production runtime images, run production containers as a non-root user where supported, keep images reproducible with configuration supplied externally, and keep Docker concerns out of the application architecture (no Docker-specific changes in Domain/Application).

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

The example assumes the repository-level build files exist; copy only build files that are present and required by restore rather than adding them to satisfy the example. Copy the project files restore needs explicitly; avoid fragile wildcard tricks that flatten or rearrange a multi-project structure.

## Restore Caching

Copy project/build dependency files before the full source tree so source changes do not invalidate the NuGet restore layer. When the solution structure changes, update the project-copy section — layer caching never justifies a Dockerfile that no longer restores the real project graph.

## Runtime Image

Image choice (standard: `rules/backend/operations.md` § Containers): `mcr.microsoft.com/dotnet/aspnet` for ASP.NET Core applications, `mcr.microsoft.com/dotnet/runtime` for workers that do not need ASP.NET Core.

## Non-Root

Use the built-in non-root user of modern .NET images when it fits the image and deployment environment:

```dockerfile
USER app
```

Give directories the application writes to appropriate ownership and permissions; find out why permissions are wrong instead of switching to root.

## Configuration and Secrets

Pass environment-specific configuration at runtime, for example:

```text
ASPNETCORE_ENVIRONMENT
ConnectionStrings__Default
Authentication__Authority
```

Container-specific places to keep free of real credentials (`rules/common/security.md` § Secrets): the Dockerfile, committed Compose files, build arguments (visible in image metadata), and appsettings files copied into the image. Supply secrets through platform/container secret mechanisms.

## Docker Compose Development

Compose is useful for local infrastructure such as databases when the project benefits from it:

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

Add only infrastructure the project actually uses — not PostgreSQL, Redis, RabbitMQ or other services because examples commonly include them. Keep local passwords in a local `.env` or another ignored developer configuration mechanism.

## Health Probes

Application health behavior: `health-check` skill. Expose liveness/readiness through ASP.NET Core health checks and prefer native HTTP probes supplied by the orchestrator. Runtime images may lack `curl`, `wget` or shell utilities: if Compose itself runs an in-container health command, verify the executable exists or add an appropriate probe mechanism, weighing the cost of installing debugging packages into a production image.

## Angular Container

For a statically deployed Angular frontend, build it in a Node stage and serve the generated assets with the selected hosting strategy — Nginx is not mandatory; the platform may provide static hosting. Keep API base URLs and environment configuration compatible with the deployment strategy (frontend architecture: `angular` skill).

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

Keep tests in the context when the Docker build or CI intentionally runs them inside the image build, and keep every file restore/build needs.

## Image Optimization

Start with standard supported .NET runtime images. Alpine, chiseled images, trimming, Native AOT or other size optimizations fit only when compatibility and deployment requirements justify them — verify globalization, native dependencies, reflection and diagnostics behavior when using specialized images.

## Database Migrations

Container deployment does not change the migration policy: production migrations follow `delivery-pipeline`, and development seeding stays Development-only (`rules/backend/persistence.md`).

## Anti-Patterns

Avoid the SDK image as production runtime, production root execution without a concrete reason, secrets baked into images, arbitrary infrastructure services in Compose, assuming `curl`/`wget` exist in runtime images, automatic production database migration, specialized image variants without compatibility verification, and Docker-specific changes leaking into Domain/Application code.
