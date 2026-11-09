---
name: ci-cd
description: >
  Use for CI/CD definitions (GitHub Actions or equivalent): restore/build/test jobs,
  npm ci frontend jobs, test services, artifacts, image publishing, secrets,
  deployment.
---

> Level: 2 Technology · Owns: CI/CD technique and examples (knowledge) · Scope: delivery · Loads: on invocation · Depends on: .claude/rules/2-technology/containers-ci.md

# CI/CD

Policy owners: CI truthfulness, frontend CI commands, production migrations, and the procedure → `delivery-pipeline`; secrets → `.claude/rules/0-core/security-principles.md`; containers → `2-technology/containers-ci.md` and the `docker` skill. This skill is technique only; adapt every version below to what the repository supports.

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

Add frontend test/lint steps only for scripts the workspace defines. Add `dotnet format --verify-no-changes --no-restore` only when the project adopted formatting as an enforced gate.

## Integration-test services

Provide SQL Server, Redis, a broker, etc. only when tests require them; do not hardcode one provider into a generic pipeline. Keep the test environment isolated from Development and Production data (`dotnet-testing` skill).

## Dependency security

`dotnet package list --vulnerable --include-transitive`; NuGet auditing also runs during restore on modern SDKs. `npm audit` for the frontend. Treat findings per the project's security policy.

## Artifacts

```bash
dotnet publish backend/MyApp.Api/MyApp.Api.csproj --configuration Release --output ./artifacts/api --no-build
npm run build
```

Store or publish only the artifacts later stages need; promotion and deployment steps: `delivery-pipeline`.

## Containers

Whether CI builds and publishes images is decided in `delivery-pipeline` → Containers; image technique: `docker` skill.

## Secrets and identity

Use the CI platform's secret store; prefer workload/federated identity (for example OIDC to the cloud provider) over long-lived deployment credentials when supported.

## Migrations in deployment

Generate migration scripts or bundles in CI and execute them as an explicit, visible deployment step:

```bash
dotnet ef migrations bundle --project backend/MyApp.Infrastructure --startup-project backend/MyApp.Api --output ./artifacts/efbundle
```

## Anti-patterns

Project-specific database infrastructure in a generic pipeline; rebuilding different source per environment without a reason; assuming Docker deployment.
