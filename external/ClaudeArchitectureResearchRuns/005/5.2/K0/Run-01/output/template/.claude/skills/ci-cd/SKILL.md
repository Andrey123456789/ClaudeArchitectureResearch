---
name: ci-cd
description: Use for CI/CD technique and examples — GitHub Actions job shape for .NET and Angular, restore/build/test commands, frontend npm ci stages, artifacts and publishing, build-once-promote, deployment separation, secrets in pipelines, migration steps.
---
<!-- Kind: KNW | Scope: delivery | Owns: CI/CD technique and examples | Loads: on demand (model-invoked) -->
# CI/CD

Procedure and obligations for pipelines, deployment and production migrations: `delivery-pipeline`. Secrets: `rules/common/security.md`. This skill holds the examples.

## GitHub Actions Shape

A typical workflow separates backend and frontend verification:

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

Adapt action and runtime versions to the repository's supported versions, and add frontend test/lint commands only when the project defines them.

## Backend Commands

```bash
dotnet restore
dotnet build --no-restore --configuration Release
dotnet test --no-build --configuration Release
```

Formatting/analyzer gate, when the project adopted it:

```bash
dotnet format --verify-no-changes --no-restore
```

## Integration-Test Services

Examples of services a pipeline might provide when tests require them: SQL Server, PostgreSQL, Redis, a message broker. A generic pipeline does not hardcode one database provider.

## Dependency Security

For .NET 10 package vulnerability inspection:

```bash
dotnet package list --vulnerable --include-transitive
```

NuGet auditing is also integrated into restore for modern .NET SDKs; npm projects use `npm audit`.

## Build Artifacts

```bash
dotnet publish \
  backend/MyApp.Api/MyApp.Api.csproj \
  --configuration Release \
  --output ./artifacts/api \
  --no-build
```

For Angular, `npm run build` produces the static assets. Store or publish only artifacts later stages need.

## Build Once, Promote

For a deployment model that supports artifact promotion, prefer promoting the same tested artifact/image through environments over recompiling different production code per environment; environment-specific behavior comes from runtime configuration.

## Database Migration Steps

Migration scripts or bundles may be generated in CI and executed later as an explicit deployment step (policy: `delivery-pipeline`):

```bash
dotnet ef migrations script --idempotent --project backend/MyApp.Infrastructure --startup-project backend/MyApp.Api --output ./artifacts/migrations.sql
```

## Deployment

CI and CD may be separate workflows; a green CI build does not imply every branch deploys. Use environment protection/approval where appropriate to the hosting platform.

## Anti-Patterns

Avoid project-specific database infrastructure in a generic pipeline, deployment secrets in YAML, rebuilding different source for every environment without a reason, suppressing failing tests to permit deployment, automatic production seeding or startup migrations, assuming Docker deployment, and assuming frontend scripts the repository does not define.
