---
name: ci-cd
description: CI/CD technique for .NET backends and frontend workspaces. Use when creating or reviewing GitHub Actions or other pipelines — restore/build/test jobs, frontend jobs, artifacts, dependency audits, container publishing, deployment separation, pipeline secrets, production migration steps.
---

> Level: 2-technology · Owns: pipeline technique · Loading: on demand

# CI/CD

Obligations for pipeline changes (source control, supported commands, visible failures, frontend scripts and lockfile installs, production migrations): `development-workflow` § CI/CD. Secrets: security rules. Add stages for the actual project, not generic boilerplate.

## Discover first

Check which parts exist: .NET backend, frontend workspace, test projects, Dockerfiles, provider-specific integration tests, generated clients, deployment artifacts. Do not assume a database provider, cache, container, or frontend tooling that is not there.

## Backend job

```bash
dotnet restore
dotnet build --no-restore --configuration Release
dotnet test --no-build --configuration Release
dotnet format --verify-no-changes --no-restore   # only if the project enforces formatting
```

Do not turn an optional local formatter into a mandatory gate without the project adopting that policy.

## Frontend job

Use the commands in `frontend.commands`: lockfile-based clean install, then the `build`, `test`, and `lint` scripts that the manifest defines.

## GitHub Actions shape

```yaml
name: CI
on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  backend:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v7
      - uses: actions/setup-dotnet@v6
        with:
          dotnet-version: 10.0.x
      - run: dotnet restore
      - run: dotnet build --no-restore --configuration Release
      - run: dotnet test --no-build --configuration Release

  frontend:
    runs-on: ubuntu-latest
    defaults:
      run:
        working-directory: frontend/MyApp.Web
    steps:
      - uses: actions/checkout@v7
      - uses: actions/setup-node@v7
        with:
          node-version: 24
          cache: npm
          cache-dependency-path: frontend/MyApp.Web/package-lock.json
      - run: npm ci
      - run: npm run build
```

Adapt action and runtime versions to the repository's supported versions; add frontend test/lint steps only when the scripts exist.

## Integration-test infrastructure

Provide external services in CI only when tests require them, matching the selected database provider; keep the environment isolated from Development and Production data (backend test rules).

## Dependency security

`dotnet package list --vulnerable --include-transitive` (NuGet auditing also runs during restore on modern SDKs) and the frontend audit command. Treat findings per the security rules; do not auto-upgrade packages in CI unless automated updates were adopted.

## Artifacts and promotion

```bash
dotnet publish backend/<EntryPoint>/<EntryPoint>.csproj --configuration Release --output ./artifacts/api --no-build
```

Publish only artifacts later stages need. Where the deployment model allows, build once and promote the same tested artifact or image, with environment behavior from runtime configuration. Build and publish container images only when container deployment is part of the project (`docker`).

## Secrets and deployment

Use the CI platform's secret or identity mechanism, preferring workload/federated identity over long-lived deployment credentials. CI and CD may be separate workflows; a green CI build does not mean every branch deploys — use environment protection and approvals suited to the platform.

## Production migrations

When deployment migrates the database: an explicit step at a controlled point, approved credentials, visible failure; migration scripts may be generated in CI and executed during deployment (`persistence.commands`).

## Pipeline verification

Restores from a clean environment, builds backend and frontend (when present), runs configured tests, does not depend on developer-machine state, exposes no secrets, produces the expected artifacts.

## Anti-patterns

Project-specific database infrastructure in a generic pipeline; deployment secrets in YAML; rebuilding different source per environment without reason; suppressed failing tests; automatic production seeding or startup migrations; assuming Docker; assuming frontend scripts the repository does not define.
