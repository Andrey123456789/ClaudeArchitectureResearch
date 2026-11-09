---
name: ci-cd
description: >
  Use when creating or reviewing CI/CD pipelines: .NET restore/build/test, npm
  ci and frontend scripts, test services, dependency scans, artifacts,
  containers, secrets, deployment steps.
---

> Owns: CI/CD technique and examples (no policy) | Scope: backend, frontend | Loads: on demand (knowledge skill)

# CI/CD

Policy owners: CI truthfulness, frontend CI commands, and production migrations —
`development-workflow` § CI/CD and deployment; secrets —
`.claude/rules/security.md`; Development-only seeding —
`.claude/rules/persistence.md`.

Build deployable artifacts reproducibly, keep deployment and environment
configuration outside compiled artifacts where practical, and add pipeline
stages for the actual project rather than generic boilerplate.

## Repository Discovery

Before writing a pipeline, inspect the repository for: .NET backend, Angular
frontend, test projects, Dockerfiles, database/provider-specific integration
tests, generated clients, deployment artifacts. Do not assume PostgreSQL,
Redis, Docker, or frontend tooling exists.

## Backend CI

```bash
dotnet restore
dotnet build --no-restore --configuration Release
dotnet test --no-build --configuration Release
```

Run formatting/analyzers when the repository has adopted them as enforced
checks, for example:

```bash
dotnet format --verify-no-changes --no-restore
```

Do not turn an optional local formatter into a mandatory CI gate unless the
project adopts that policy.

## Frontend CI

When an Angular frontend exists:

```bash
npm ci
```

then the scripts the frontend project defines — typically build, unit tests
when configured, lint when configured. Frontend conventions: `angular` skill.

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

Adapt action and runtime versions to the repository's supported versions, and
add frontend test/lint commands only when the project defines them.

## Integration-Test Infrastructure

Provide external services in CI (SQL Server, PostgreSQL, Redis, a message
broker) only when tests actually require them; do not hardcode one database
provider into a generic pipeline. The integration environment stays isolated
from Development and Production data (`.claude/rules/testing.md`).

## Dependency Security

```bash
dotnet package list --vulnerable --include-transitive
```

NuGet auditing is also integrated into restore for modern .NET SDKs. Treat
findings according to the project's security policy, and do not upgrade
packages automatically in CI unless the project has adopted automated dependency
updates.

## Build Artifacts

```bash
dotnet publish \
  backend/MyApp.Api/MyApp.Api.csproj \
  --configuration Release \
  --output ./artifacts/api \
  --no-build
```

For Angular, `npm run build`. Store or publish only the artifacts later stages
need.

## Docker

When the project deploys containers, follow the `docker` skill and build/publish
the image from CI. Do not add Docker to the pipeline merely because this skill
covers it.

## Build Once, Promote

When the deployment model supports artifact promotion, prefer promoting the same
tested artifact or image through environments instead of recompiling for each
environment; environment-specific behavior comes from runtime configuration.

## Secrets

Use the CI platform's secret/identity mechanism instead of values in pipeline
YAML, and prefer workload/federated identity over long-lived deployment
credentials when the platform supports it.

## Database Migrations

A deployment that performs migrations makes the step explicit, uses the
project's approved credentials, runs it at a controlled point, and fails visibly.
Migration scripts or bundles may be generated in CI and executed during
deployment.

## Deployment

CI and CD may be separate workflows; a green CI build does not mean every branch
deploys. Use environment protection or approval appropriate to the hosting
platform.

## Verification

Before considering a pipeline complete, verify that it restores from a clean
environment, builds the backend, builds the frontend when present, runs the
configured tests, does not depend on developer-machine state, does not expose
secrets, and produces the expected artifacts.

## Anti-Patterns

Avoid project-specific database infrastructure in a generic pipeline,
rebuilding different source for every environment without a reason, and assuming
Docker deployment.
