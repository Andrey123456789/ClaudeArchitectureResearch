---
name: ci-cd
description: >
  Use when writing or reviewing CI/CD pipelines: GitHub Actions jobs, dotnet
  restore/build/test, npm ci, formatting gates, test service containers,
  vulnerability scans, artifacts, image publishing, deployment steps.
---

> Kind: KNW | Scope: delivery | Capability: — | Loading: on-demand knowledge

# CI/CD

Procedure and obligations: `delivery-change`. Build deployable artifacts reproducibly and keep deployment/environment configuration outside compiled artifacts where practical.

## Backend CI

```bash
dotnet restore
dotnet build --no-restore --configuration Release
dotnet test --no-build --configuration Release
dotnet format --verify-no-changes --no-restore   # only when the project adopted formatting as an enforced gate
```

## Frontend CI

```bash
npm ci
npm run build
```

Add unit-test and lint steps only when the workspace's `package.json` defines those scripts.

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

Adapt action and runtime versions to the repository's supported versions.

## Integration-test infrastructure

Provide services (the selected database server, cache, broker) only when tests require them, as CI service containers or Testcontainers, isolated from Development and Production data; do not hardcode a database provider into a generic pipeline. Testing technique: the backend-testing knowledge facet named in the decision register.

## Dependency security

`dotnet package list --vulnerable --include-transitive`; NuGet auditing also runs during restore on modern SDKs; `npm audit` for the frontend. Treat findings per the project's security policy.

## Artifacts

```bash
dotnet publish backend/MyApp.Api/MyApp.Api.csproj --configuration Release --output ./artifacts/api --no-build
npm run build
```

Store or publish only artifacts later stages need. Build and publish container images only when container deployment is part of the project (`docker`).

## Build once, promote

Where the deployment model supports promotion, promote the same tested artifact/image through environments instead of recompiling per environment; environment-specific behavior comes from runtime configuration.

## Secrets

Use the CI platform's secret/identity mechanism; prefer workload or federated identity over long-lived deployment credentials.

## Database migrations in deployment

Generate migration scripts/artifacts in CI and execute them at a controlled deployment step with approved credentials, failing visibly on error. Migration technique: the persistence knowledge facet named in the decision register.

## Deployment

CI and CD may be separate workflows; use environment protection/approval appropriate to the hosting platform.

## Anti-patterns

Project-specific database infrastructure in a generic pipeline, rebuilding different source per environment, assuming container deployment. Pipeline obligations (visible failures, declared scripts, lockfile installs, deliberate production migrations): `delivery-change`.
