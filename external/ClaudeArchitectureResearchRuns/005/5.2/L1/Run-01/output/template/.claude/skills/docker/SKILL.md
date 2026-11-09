---
name: docker
description: >
  Use for Dockerfiles, .dockerignore, or Compose files: multi-stage .NET builds,
  restore caching, runtime images, non-root users, config and secrets, health
  probes.
---
> Level: 2-technology | Owns: container technique for the backend and frontend | Scope: backend, frontend | Loads: on demand (skill)

# Docker

Policy: project stack (whether containers are used at all),
`backend-technologies.md` (runtime image, non-root), `security.md` (secrets),
`delivery` (deployment-time migrations). Keep container concerns out of
application code.

## ASP.NET Core Dockerfile

```dockerfile
FROM mcr.microsoft.com/dotnet/sdk:10.0 AS build
WORKDIR /src

COPY Directory.Build.props ./
COPY Directory.Packages.props ./

# One line per backend production project (architecture.layout):
COPY backend/MyApp.Orders/MyApp.Orders.csproj backend/MyApp.Orders/
COPY backend/MyApp.Host/MyApp.Host.csproj backend/MyApp.Host/

RUN dotnet restore backend/MyApp.Host/MyApp.Host.csproj

COPY . .

RUN dotnet publish backend/MyApp.Host/MyApp.Host.csproj \
    --configuration Release \
    --output /app/publish \
    --no-restore

FROM mcr.microsoft.com/dotnet/aspnet:10.0 AS runtime
WORKDIR /app
COPY --from=build /app/publish .
USER app
EXPOSE 8080
ENTRYPOINT ["dotnet", "MyApp.Host.dll"]
```

`MyApp.Host` stands for the composition-root host project and `MyApp.Orders`
for each other backend project; take the real list from `architecture.layout`.
Copy only repository-level build files that exist and restore needs, copy
project files explicitly (no wildcard tricks that flatten the directory
structure), and update the project-copy section when the solution structure
changes. Restore caching must never come at the cost of restoring the wrong
project graph.

## Runtime image and user

Use the ASP.NET Core runtime image for web apps and the .NET runtime image for
workers. Modern .NET images provide the non-root `app` user (`USER app`); make
sure directories the app writes to have the right ownership instead of switching
to root.

## Configuration and secrets

Pass environment-specific configuration at runtime (`ASPNETCORE_ENVIRONMENT`,
`ConnectionStrings__DefaultConnection`, `Authentication__Authority`). Never put
real credentials in a Dockerfile, committed Compose files, build arguments
(visible in image metadata), or copied appsettings files; use platform/container
secret mechanisms.

## Compose for development

```yaml
services:
  api:
    build:
      context: .
      dockerfile: backend/MyApp.Host/Dockerfile
    ports:
      - "5000:8080"
    environment:
      ASPNETCORE_ENVIRONMENT: Development
      ConnectionStrings__DefaultConnection: ${DB_CONNECTION_STRING}
```

Add only infrastructure the project uses (no PostgreSQL, Redis, or RabbitMQ
because examples show them); keep local passwords in an ignored `.env`.

## Health probes

Expose liveness/readiness via ASP.NET Core health checks (`health-check`) and
prefer the orchestrator's native HTTP probes. Runtime images may lack `curl`,
`wget`, or a shell; verify an in-container probe executable exists or add an
explicit probe mechanism, weighing image size.

## Frontend container

For a static frontend, build assets in a Node build stage with the build command
from `frontend.commands` and serve them with the selected hosting strategy
(Nginx is not mandatory; the platform may host static files). Keep API base URLs
compatible with the deployment.

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

Do not exclude files restore or build needs, or tests the build intentionally
runs.

## Image optimization

Start with standard supported images. Consider Alpine, chiseled images,
trimming, or Native AOT only when compatibility and deployment requirements
justify it, and verify globalization, native dependencies, reflection, and
diagnostics.

## Verification

Build the image; verify startup, port and configuration, non-root behavior,
health-probe integration; review the image for accidental secrets or files. Run
meaningful tests outside or as part of the build pipeline.

## Anti-patterns

SDK image as runtime; root without a reason; baked-in secrets; arbitrary Compose
services; assuming `curl`/`wget`; automatic production migrations; unverified
specialized images; container concerns leaking into application code.
