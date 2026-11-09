---
name: ci-cd
description: >
  Use when creating or reviewing CI/CD pipelines for .NET and Angular:
  restore/build/test jobs, npm ci, formatting gates, dependency audits,
  artifacts, container publishing, deployment stages, pipeline secrets,
  migration steps.
---

> Owner: CI/CD pipeline technique and examples (normative policy lives in rules) | Scope: delivery | Loads: on demand — knowledge | Enforced: none

# CI/CD

Policy: `.claude/rules/delivery.md` § CI (pipeline truthfulness, frontend
installs), `.claude/rules/persistence.md` § Migrations,
`.claude/rules/security.md` § Secrets.

Add pipeline stages according to the actual project rather than generic
boilerplate, and keep deployment/environment configuration outside compiled
artifacts where practical.

## Repository Discovery

Before writing a pipeline, inspect what exists: .NET backend, Angular frontend,
test projects, Dockerfiles, provider-specific integration tests, generated
clients, deployment artifacts. Do not assume PostgreSQL, Redis, Docker, or
frontend tooling.

## Backend CI

```bash
dotnet restore
dotnet build --no-restore --configuration Release
dotnet test --no-build --configuration Release
```

Run formatting or analyzers when the repository adopted them as enforced checks,
for example:

```bash
dotnet format --verify-no-changes --no-restore
```

An optional local formatter is not a CI gate until the project adopts that
policy.

## Frontend CI

```bash
npm ci
npm run build
```

Add `npm test` or lint only when `package.json` defines them. Frontend
conventions: `angular` skill.

## GitHub Actions Shape

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
          global-json-file: global.json

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

Adapt action and runtime versions to the repository's supported versions; reading
the SDK from `global.json` keeps CI aligned with local builds.

## Integration-Test Infrastructure

Provide services in CI (SQL Server, Redis, a message broker) only when tests
actually require them, isolated from Development and Production data
(`dotnet-testing` skill). A generic pipeline does not hardcode a database
provider.

## Dependency Security

```bash
dotnet package list --vulnerable --include-transitive
npm audit --omit=dev
```

NuGet auditing also runs during restore in modern .NET SDKs. Treat findings
according to the project's security policy, and do not upgrade packages
automatically in CI unless the project adopted automated dependency updates.

## Build Artifacts

```bash
dotnet publish \
  backend/MyApp.Api/MyApp.Api.csproj \
  --configuration Release \
  --output ./artifacts/api \
  --no-build
```

For Angular, `npm run build`. Store or publish only artifacts later stages need.

## Docker

Build and publish images from CI only when container deployment is part of the
project (`docker` skill).

## Build Once, Promote

Where the deployment model supports it, prefer promoting the same tested
artifact or image through environments over recompiling per environment;
environment-specific behavior comes from runtime configuration.

## Secrets

Use the CI platform's secret and identity mechanisms rather than values in YAML,
and prefer workload/federated identity over long-lived deployment credentials
when the platform supports it.

## Database Migrations in Deployment

Requirements for a migration step: `.claude/rules/persistence.md` § Migrations.
A common shape produces an idempotent script (or a migrations bundle) in CI and
executes it in the deployment stage, failing the deployment visibly when the
migration fails:

```bash
dotnet ef migrations script --idempotent --project backend/MyApp.Infrastructure --startup-project backend/MyApp.Api --output artifacts/migrations.sql
```

## Deployment

CI and CD may be separate workflows; a green CI build does not mean every branch
deploys. Use environment protection or approvals appropriate to the hosting
platform.

## Verification

Before considering a pipeline complete, confirm that it restores from a clean
environment, builds the backend, builds the frontend when present, runs the
configured tests, does not depend on developer-machine state, does not expose
secrets, and produces the expected artifacts.

## Common Mistakes

- project-specific database infrastructure in a generic pipeline;
- rebuilding different source for every environment without a reason;
- assuming Docker deployment.
