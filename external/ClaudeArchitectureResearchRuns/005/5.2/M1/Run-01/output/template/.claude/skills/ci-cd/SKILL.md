---
name: ci-cd
description: >
  CI/CD pipelines (GitHub Actions or equivalent): dotnet restore/build/test, npm
  ci, artifacts, security checks, container publishing, deployment secrets,
  migration steps.
---

> **Knowledge skill** · Owns: CI/CD technique and examples · Scope: common · Loading: on demand

# CI/CD

## Rules

Pipeline obligations (source-controlled definitions reproducing the supported
commands, visible failures, frontend scripts and `npm ci`, production migrations
as deliberate deployment steps): `development-workflow` → Change-Specific
Obligations. Secrets: `security.md` → Secrets.

1. Build deployable artifacts reproducibly.
2. Keep deployment/environment configuration outside compiled artifacts where
   practical.
3. Add pipeline stages according to the actual project, not generic boilerplate.

## Repository Discovery

Before writing a pipeline, inspect the repository.

Determine whether it contains:

```text
.NET backend
frontend workspace
test projects
Dockerfiles
database/provider-specific integration tests
generated clients
deployment artifacts
```

Do not assume PostgreSQL, Redis, Docker, or frontend tooling exists.

## Backend CI

Typical .NET flow:

```bash
dotnet restore
dotnet build --no-restore --configuration Release
dotnet test --no-build --configuration Release
```

Run formatting/analyzers when the repository has adopted them as enforced checks.

For example:

```bash
dotnet format --verify-no-changes --no-restore
```

Do not turn an optional local formatter into a mandatory CI gate without the
project adopting that policy.

## Frontend CI

When a frontend workspace exists, use the lockfile-based package installation:

```bash
npm ci
```

Then run the scripts defined by that frontend project, normally covering:

```text
build
unit tests when configured
lint when configured
```

Frontend-specific commands: the frontend knowledge facet.

## GitHub Actions Shape

A typical workflow can separate backend and frontend verification:

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

Add frontend test/lint commands only when the project defines them.

## Integration-Test Infrastructure

Provide external services in CI only when tests actually require them.

Examples may include:

```text
the project's database server
Redis
message broker
```

Do not hardcode a database provider into a generic pipeline; use the provider
the project actually selected.

The integration test environment must be isolated from Development and
Production data.

Follow the `dotnet-testing` skill.

## Dependency Security

For .NET 10, package vulnerability inspection may use:

```bash
dotnet package list --vulnerable --include-transitive
```

NuGet auditing is also integrated into restore for modern .NET SDKs.

Treat dependency findings according to the project's security policy.

Do not automatically upgrade packages in CI unless the project has explicitly
adopted automated dependency updates.

## Build Artifacts

When a deployment artifact is required, produce it deliberately:

```bash
dotnet publish \
  backend/MyApp.Api/MyApp.Api.csproj \
  --configuration Release \
  --output ./artifacts/api \
  --no-build
```

For the frontend:

```bash
npm run build
```

Store or publish only artifacts required by later stages.

## Docker

When the project deploys containers, follow the `docker` skill.

Build and publish the image from CI only when container deployment is part of
the project.

Do not introduce Docker into the pipeline merely because the skill supports it.

## Build Once, Promote

For a deployment model that supports artifact promotion, prefer promoting the
same tested artifact/image through environments rather than recompiling
different production code for every environment.

Environment-specific behavior should normally come from runtime configuration.

## Secrets

Use the CI platform's secret/identity mechanism.

Prefer workload/federated identity over long-lived deployment credentials when
the chosen platform supports it.

## Database Migrations

Policy: `development-workflow` → Change-Specific Obligations. When deployment
performs migrations, make the step explicit, use the project's approved
credentials, run it at a controlled point, and fail visibly on migration failure.
Migration scripts/artifacts may be generated earlier in CI and executed during
deployment.

## Deployment

CI and CD may be separate workflows.

A successful CI build does not automatically imply that every branch should
deploy.

Use environment protection/approval where appropriate to the actual hosting
platform.

## Verification

Before considering a pipeline complete, verify that it:

```text
restores from a clean environment
builds backend
builds frontend when present
runs configured tests
does not depend on developer-machine state
does not expose secrets
produces expected artifacts
```

## Anti-Patterns

Avoid:

- project-specific database infrastructure in a generic pipeline;
- rebuilding different source for every environment without a reason;
- assuming Docker deployment;
- assuming frontend scripts that the repository does not define.
