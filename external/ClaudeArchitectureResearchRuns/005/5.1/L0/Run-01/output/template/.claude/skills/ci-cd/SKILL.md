---
name: ci-cd
description: >
  Use when creating or reviewing build, test, release or deployment pipelines:
  backend and frontend jobs, npm ci, dependency audits, artifacts, secrets,
  migration steps.
---

> Level: 2 Technology · Owns: pipeline technique · Scope: delivery · Loads: on demand (knowledge skill)

# CI/CD

Policy owners: `.claude/rules/0-core/completion-contract.md` (Pipelines: source-controlled, reproduces supported commands, failures visible), `.claude/rules/2-technology/containers-ci.md` (frontend scripts and `npm ci`), `.claude/rules/0-core/security-principles.md` (secrets). Production migration and seeding policy: the project's data-lifecycle rule. Add stages for what the repository actually contains, not generic boilerplate.

## Repository discovery

Before writing a pipeline, check what exists: .NET backend, Angular frontend, test projects, Dockerfiles, provider-specific integration tests, generated clients, deployment artifacts. Do not assume PostgreSQL, Redis, Docker or frontend tooling.

## Backend job

```bash
dotnet restore
dotnet build --no-restore --configuration Release
dotnet test --no-build --configuration Release
dotnet format --verify-no-changes --no-restore     # only when the project enforces formatting in CI
```

## Frontend job

```bash
npm ci
npm run build
npm test -- --watch=false    # only when the script exists; adjust to the configured runner
npm run lint                 # only when the script exists
```

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
          dotnet-version: 10.0.x          # or global-json-file: global.json
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

Adapt action and runtime versions to the repository's supported versions; add frontend test or lint steps only when the project defines those scripts.

## Integration-test infrastructure

Provide services only when tests require them (for example a SQL Server service container for provider-fidelity tests). Keep the integration environment isolated from Development and Production data; do not hardcode one database provider into a generic pipeline.

## Dependency security

```bash
dotnet package list --vulnerable --include-transitive
npm audit --omit=dev        # runtime dependencies; run without --omit for the full supply chain view
```

NuGet audit also runs during restore. Treat findings with the project's security policy; do not upgrade packages automatically in CI unless automated dependency updates were adopted.

## Artifacts

```bash
dotnet publish backend/MyApp.Api/MyApp.Api.csproj --configuration Release --output ./artifacts/api --no-build
npm run build               # frontend dist output
```

Store only artifacts later stages need. Where artifact promotion is possible, build once and promote the same tested artifact or image through environments; environment differences come from runtime configuration.

## Containers

Build and publish images only when container deployment is part of the project (`docker` skill).

## Secrets and identity

Use the CI platform's secret store; prefer workload/federated identity (for example OIDC to the cloud provider) over long-lived deployment credentials.

## Database migrations in deployment

When deployment applies migrations: make it an explicit step at a controlled point, with approved credentials, failing visibly. Migration scripts (`dotnet ef migrations script --idempotent`) or bundles can be produced in CI and executed during deployment.

## Deployment

CI and CD may be separate workflows; a green CI run does not mean every branch deploys. Use environment protection and approvals where the platform supports them.

## Pipeline verification

Restores from a clean environment; builds backend and (when present) frontend; runs configured tests; does not depend on developer-machine state; exposes no secrets; produces the expected artifacts.

## Review cues

Project-specific database services in a generic pipeline, secrets in YAML, rebuilding different source per environment, suppressed failing tests, automatic production seeding or startup migrations, assumed Docker deployment, invented npm scripts.
