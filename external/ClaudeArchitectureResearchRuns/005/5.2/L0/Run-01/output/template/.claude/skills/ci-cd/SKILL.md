---
name: ci-cd
description: >
  Use for build, test, release, or deployment pipelines: GitHub Actions, dotnet/npm ci steps, artifacts, audits, secrets, migration steps.
---

> Level: 2 Technology | Owns: CI/CD technique | Scope: delivery | Loads: knowledge skill (on demand) | Depends on: 2-technology/containers.md

# CI/CD Technique

Policy owners (routing): pipeline truthfulness, frontend scripts and lockfile,
production migrations → `develop` (CI/CD and deployment); secrets →
`0-core/security-principles.md`; Docker optionality → `3-project/decisions.md`.

## Discover the Repository First

Check for the .NET backend, Angular frontend, test projects, Dockerfiles,
provider-specific integration tests, generated clients, and deployment
artifacts. Do not assume PostgreSQL, Redis, Docker, or frontend tooling exists;
add stages for the actual project, not generic boilerplate.

## Backend

```bash
dotnet restore
dotnet build --no-restore --configuration Release
dotnet test --no-build --configuration Release
```

Run formatting or analyzers (e.g. `dotnet format --verify-no-changes
--no-restore`) only when the repository adopted them as enforced checks.

## Frontend

```bash
npm ci
npm run build
```

Then the test and lint scripts the workspace defines.

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

Adapt action and runtime versions to the repository's supported versions
(resolve current major versions when writing the workflow).

## Integration-Test Services

Provide services (SQL Server, Redis, brokers) in CI only when tests need them,
isolated from Development and Production data; do not hardcode one provider
into a generic pipeline.

## Dependency Security

`dotnet package list --vulnerable --include-transitive`; NuGet audit also runs
during restore on modern SDKs; `npm audit` for the frontend. Do not upgrade
packages automatically in CI unless the project adopted automated updates.

## Artifacts

```bash
dotnet publish backend/MyApp.Api/MyApp.Api.csproj --configuration Release --output ./artifacts/api --no-build
```

Publish only artifacts later stages need. Where the deployment model supports
it, prefer building once and promoting the same tested artifact or image
through environments, with environment behavior from runtime configuration.

## Containers

Build and publish images only when container deployment is part of the project
(`docker` skill).

## Secrets and Identity

Keep every credential in the CI platform's secret store and reference it from
the workflow. Prefer
workload or federated identity over long-lived deployment credentials when the
platform supports it.

## Migrations and Deployment

When deployment performs migrations: generate the script or bundle earlier in
CI, run it as an explicit step at a controlled point with approved credentials,
and fail visibly. CI and CD may be separate workflows; not every green branch
deploys; use environment protection or approvals that fit the platform.

## Verification

A pipeline is complete when it restores from a clean environment, builds the
backend and (when present) the frontend, runs the configured tests, does not
depend on developer-machine state, exposes no secrets, and produces the
expected artifacts.
