---
name: ci-cd
description: >
  Use when creating or reviewing build, test, release, or deployment pipelines
  (GitHub Actions or equivalent) for the .NET backend and Angular frontend:
  restore/build/test steps, frontend CI, artifacts, dependency checks,
  container publishing, deployment separation, pipeline secrets, and migration
  steps.
---

> Owns: CI/CD pipeline technique | Scope: delivery | Loads: on demand (knowledge skill)

# CI/CD

Policy owners: CI truthfulness and frontend CI commands →
`.claude/rules/delivery.md`; production migrations and seeding →
`.claude/rules/persistence.md`; pipeline secrets → `.claude/rules/security.md`;
Docker adoption → `docs/technology-stack.md`.

## Repository Discovery

Before writing a pipeline, inspect what exists: .NET backend, Angular frontend,
test projects, Dockerfiles, provider-specific integration tests, generated
clients, deployment artifacts. Do not assume PostgreSQL, Redis, Docker, or
frontend tooling; add stages for the actual project, not boilerplate.

## Backend

```bash
dotnet restore
dotnet build --no-restore --configuration Release
dotnet test --no-build --configuration Release
```

Add `dotnet format --verify-no-changes --no-restore` or analyzer gates only when
the project has adopted them as enforced checks.

## Frontend

```bash
npm ci
npm run build
# plus test/lint scripts only when package.json defines them
```

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

## Integration-Test Infrastructure

Provide services (SQL Server, a message broker, ...) only when tests require
them, isolated from Development and Production data. Do not hardcode one
database provider into a generic pipeline.

## Dependency Checks

`dotnet package list --vulnerable --include-transitive` and `npm audit`; NuGet
audit also runs during restore on modern SDKs. Handle findings per the security
policy; do not auto-upgrade packages in CI unless the project adopted automated
dependency updates.

## Artifacts

```bash
dotnet publish backend/MyApp.Api/MyApp.Api.csproj --configuration Release --output ./artifacts/api --no-build
```

Publish only artifacts later stages need. Where the deployment model allows,
build once and promote the same tested artifact/image through environments;
environment differences come from runtime configuration.

## Containers

Build and publish images from CI only when container deployment is part of the
project (`docker`).

## Secrets and Identity

Use the CI platform's secret store; prefer workload/federated identity over
long-lived deployment credentials when supported.

## Database Migrations in Deployment

Implement the explicit migration step required by `persistence.md` as its own
deployment job: generate the script in CI
(`dotnet ef migrations script --idempotent`), publish it as an artifact, run it
at a controlled point with the deployment's approved credentials, and let a
migration error fail the deployment.

## Deployment

CI and CD may be separate workflows; a green CI build does not imply every branch
deploys. Use environment protection/approvals appropriate to the platform.

## Pipeline Verification

Before considering a pipeline complete, confirm it restores from a clean
environment, builds backend and (when present) frontend, runs configured tests,
does not depend on developer-machine state, exposes no secrets, and produces the
expected artifacts.
