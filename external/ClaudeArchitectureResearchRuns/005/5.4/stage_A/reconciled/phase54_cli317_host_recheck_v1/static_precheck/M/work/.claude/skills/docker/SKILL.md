---
name: docker
description: >
  Use when adding or reviewing Dockerfiles, Compose files, or container
  deployment: multi-stage .NET images, restore caching, non-root users,
  .dockerignore, runtime configuration, probes.
---

> Owns: container technique and examples (no policy) | Scope: backend, frontend | Loads: on demand (knowledge skill)

# Docker

Policy owners: Docker is optional — `docs/technology-stack.md`; runtime image and
root user — `.claude/rules/security.md` § Containers; secrets —
`.claude/rules/security.md` § Secrets; production migrations and seeding —
`development-workflow` (CI/CD and deployment) and
`.claude/rules/persistence.md`.

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

Copy only repository-level build files that exist and are required by restore.
Copy project files required for restore explicitly; avoid fragile wildcard
tricks that flatten or rearrange a multi-project structure.

## Restore Caching

Copy project and build dependency files before the full source tree so source
changes do not invalidate NuGet restore layers. Update the project-copy section
when the solution structure changes; do not optimize caching at the cost of a
Dockerfile that no longer restores the actual project graph.

## Runtime Image

Use the ASP.NET runtime image for ASP.NET Core applications and an appropriate
.NET runtime image for workers that do not need ASP.NET Core.

## Non-Root

Use the built-in non-root user of modern .NET images when it fits:

```dockerfile
USER app
```

Ensure directories the application writes to have the right ownership and
permissions, and find out why permissions are wrong instead of switching users.

## Configuration and Secrets

Pass environment-specific configuration at runtime, for example
`ASPNETCORE_ENVIRONMENT`, `ConnectionStrings__Default`,
`Authentication__Authority`. Places where real credentials must never go: the
Dockerfile, committed Compose files, build arguments that remain visible in
image metadata, and copied appsettings files containing production secrets. Use
platform/container secret mechanisms where appropriate.

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

Add only infrastructure the project actually uses — not PostgreSQL, Redis,
RabbitMQ, or other services because they are common in examples. Keep local
passwords in an ignored `.env` or another local developer mechanism.

## Health Probes

Expose liveness/readiness endpoints through ASP.NET Core health checks
(`health-check` skill) and prefer native HTTP probes supplied by the
orchestrator. Do not assume the runtime image contains `curl`, `wget`, or shell
utilities; if Compose must run an in-container health command, verify the
executable exists or add an appropriate probe mechanism, weighing the cost of
installing debugging packages into a production image.

## Angular Container

When the Angular frontend is deployed as a static application, build it in a Node
build stage and serve the generated assets with the selected hosting strategy.
Nginx is not mandatory; the platform may provide static hosting directly. Keep
API base URLs and environment configuration compatible with the deployment
strategy.

## `.dockerignore`

Exclude files that do not belong in the build context:

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
exclude files required by restore/build.

## Image Optimization

Start with standard supported .NET runtime images. Consider Alpine, chiseled
images, trimming, Native AOT, or other size optimizations only when
compatibility and deployment requirements justify them, and verify
globalization, native dependencies, reflection, diagnostics, and other runtime
behavior when using specialized images.

## Verification

For Docker changes: build the image; verify application startup, required ports
and configuration, non-root behavior when relevant, and health-probe
integration; review the image for accidental secrets or files. Run meaningful
application tests outside or as part of the selected build pipeline.

## Anti-Patterns

Avoid arbitrary infrastructure services in Compose, assuming curl/wget in
runtime images, specialized image variants without compatibility verification,
and Docker-specific changes leaking into Domain or Application code.
