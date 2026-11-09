---
name: ci-cd
description: Use when writing or reviewing CI/CD definitions — restore/build/test jobs, frontend install and scripts, test services, audits, artifacts, container publishing, promotion, pipeline secrets.
---

> Kind: KNW | Scope: delivery | Owner: CI/CD technique with examples | Loading: on demand (model-invoked knowledge)

# CI/CD

Procedure and pipeline obligations: `delivery-pipeline`. Secrets: `rules/common/security.md` § Secrets. Containers: D-14 and `docker`.

Build deployable artifacts reproducibly, and keep deployment and environment configuration outside compiled artifacts where practical.

## Backend CI

```bash
dotnet restore
dotnet build --no-restore --configuration Release
dotnet test --no-build --configuration Release
```

When the repository has adopted formatting or analyzers as enforced checks:

```bash
dotnet format --verify-no-changes --no-restore
```

An optional local formatter does not become a mandatory CI gate without the project adopting that policy.

## Frontend CI

```bash
npm ci
npm run build
```

Then run the unit-test and lint scripts the workspace actually defines. Frontend technique: `angular`.

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

Adapt action and runtime versions to the repository's supported versions, and add frontend test/lint steps only when the project defines them.

## Integration-test infrastructure

Provide services such as SQL Server, PostgreSQL, Redis or a message broker only when tests require them; the generic template hardcodes no database provider, and the test environment stays isolated from Development and Production data (`dotnet-testing`).

## Dependency security

```bash
dotnet package list --vulnerable --include-transitive
```

NuGet auditing also runs during restore with modern .NET SDKs. Treat findings according to the project's security policy; automatic dependency updates in CI need explicit adoption.

## Build artifacts

```bash
dotnet publish \
  backend/MyApp.Api/MyApp.Api.csproj \
  --configuration Release \
  --output ./artifacts/api \
  --no-build
```

Angular artifacts come from `npm run build`. Store or publish only artifacts that later stages need. Build and publish container images from CI only when container deployment is part of the project.

## Build once, promote

Where the deployment model supports promotion, promote the same tested artifact or image through environments instead of recompiling per environment; environment-specific behavior comes from runtime configuration.

## Secrets and identity

Use the CI platform's secret or identity mechanism; prefer workload/federated identity over long-lived deployment credentials when the platform supports it.

## Migrations and deployment

Migration scripts or bundles can be generated in CI and executed by an explicit deployment step (`delivery-pipeline` § 3). CI and CD may be separate workflows (deployment steps: `delivery-pipeline` § 4).

## Common mistakes

Project-specific database infrastructure in a generic pipeline; deployment secrets in YAML; different source rebuilt per environment without reason; failing tests suppressed to allow deployment; automatic production seeding or startup migrations; assumed Docker deployment; assumed frontend scripts.
