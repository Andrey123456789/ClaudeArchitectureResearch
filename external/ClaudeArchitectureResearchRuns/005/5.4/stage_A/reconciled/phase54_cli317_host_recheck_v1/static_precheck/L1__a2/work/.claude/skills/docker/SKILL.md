---
name: docker
description: Docker technique for ASP.NET Core APIs and static frontends. Use when adding or reviewing Dockerfiles, multi-stage builds, restore-layer caching, non-root USER, .dockerignore, Docker Compose for local infrastructure, container configuration and secrets, or container health probes.
---

> Level: 2-technology · Owns: container technique · Loading: on demand

# Docker

Rules: Docker is optional (decisions file); runtime-image rule (`.claude/rules/2-technology/backend-libraries.md`); secrets (`.claude/rules/0-core/security.md`); production migrations and seeding in containers follow `development-workflow` delivery steps. Keep Docker concerns out of use-case and domain code.

## API image (multi-stage)

```dockerfile
FROM mcr.microsoft.com/dotnet/sdk:10.0 AS build
WORKDIR /src

COPY Directory.Build.props Directory.Packages.props ./
# Copy every project file of the entry-point project's reference graph (architecture.layout), preserving paths:
COPY backend/<EntryPoint>/<EntryPoint>.csproj backend/<EntryPoint>/
# COPY backend/<OtherProject>/<OtherProject>.csproj backend/<OtherProject>/
RUN dotnet restore backend/<EntryPoint>/<EntryPoint>.csproj

COPY . .
RUN dotnet publish backend/<EntryPoint>/<EntryPoint>.csproj --configuration Release --output /app/publish --no-restore

FROM mcr.microsoft.com/dotnet/aspnet:10.0 AS runtime
WORKDIR /app
COPY --from=build /app/publish .
USER app
EXPOSE 8080
ENTRYPOINT ["dotnet", "<EntryPoint>.dll"]
```

- Copy only repository build files that exist and restore needs; do not add them just for the Dockerfile.
- Copy project files explicitly before the source tree so source edits do not invalidate the restore layer; update this section when the solution structure changes; avoid wildcard tricks that flatten the directory structure.
- Workers without ASP.NET Core use the plain .NET runtime image.
- `USER app` is the built-in non-root user of current .NET images; give writable directories correct ownership.

## Configuration and secrets

Pass environment-specific configuration at runtime (`ASPNETCORE_ENVIRONMENT`, `ConnectionStrings__Default`, `Authentication__Authority`). Never put real credentials in the Dockerfile, committed Compose files, build arguments (visible in image metadata), or copied settings files; use platform/container secret mechanisms.

## Compose for local development

```yaml
services:
  api:
    build:
      context: .
      dockerfile: backend/<EntryPoint>/Dockerfile
    ports:
      - "5000:8080"
    environment:
      ASPNETCORE_ENVIRONMENT: Development
      ConnectionStrings__Default: ${DB_CONNECTION_STRING}
```

Add only infrastructure the project uses; keep local passwords in an ignored `.env` or similar.

## Health probes

Expose liveness/readiness through ASP.NET Core health checks (`health-check`) and prefer the orchestrator's native HTTP probes. Runtime images may lack `curl`, `wget`, or a shell — verify any in-container probe command exists or add an explicit probe mechanism, weighing image size.

## Frontend container

Build static frontend assets in a Node build stage and serve them with the selected hosting strategy (a dedicated web server is not mandatory). Keep API base URLs compatible with the deployment.

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

Do not exclude files restore/build needs, or tests when the image build intentionally runs them.

## Image optimization

Start with standard supported images. Alpine, chiseled images, trimming, or Native AOT only when compatibility and deployment justify them — verify globalization, native dependencies, reflection, and diagnostics.

## Verification

Build the image, verify startup, port, and configuration, non-root behavior when relevant, health-probe integration, and that no secrets or stray files landed in the image; run tests outside or inside the pipeline as chosen.

## Anti-patterns

SDK image at runtime; root execution without reason; baked-in secrets; arbitrary Compose services; assuming `curl`/`wget`; automatic production migrations; unverified specialized images; Docker concerns leaking into use-case or domain code.
