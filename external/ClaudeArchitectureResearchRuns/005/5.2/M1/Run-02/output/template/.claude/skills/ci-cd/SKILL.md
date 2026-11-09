---
name: ci-cd
description: >
  Use for CI/CD pipelines: GitHub Actions or equivalent, restore/build/test
  steps, npm ci, artifacts, dependency checks, container publishing, CI
  secrets, deployment and migration steps.
---

> Knowledge skill · CI/CD technique · Pipeline obligations: `verify` § Delivery Changes · Secrets: `.claude/rules/security.md` § Secrets

# CI/CD

Build deployable artifacts reproducibly, keep deployment/environment
configuration outside compiled artifacts where practical, and add pipeline
stages according to the actual project rather than generic boilerplate.

## Repository Discovery

Before writing a pipeline, inspect the repository: .NET backend, frontend
workspace, test projects, Dockerfiles, provider-specific integration tests,
generated clients, deployment artifacts. Do not assume a particular database,
Redis, Docker, or frontend tooling exists.

## Backend CI

```bash
dotnet restore
dotnet build --no-restore --configuration Release
dotnet test --no-build --configuration Release
```

Run formatting or analyzers when the repository has adopted them as enforced
checks, for example `dotnet format --verify-no-changes --no-restore`; do not
turn an optional local formatter into a mandatory CI gate without the project
adopting that policy.

## Frontend CI

Install from the lockfile with `npm ci`, then run the scripts the frontend
project defines — typically build, unit tests when configured, and lint when
configured. Frontend specifics: the frontend knowledge skill.

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

Adapt action and runtime versions to the repository's supported versions, and
add frontend test/lint commands only when the project defines them.

## Integration-Test Infrastructure

Provide external services (a database server, Redis, a message broker) in CI
only when tests require them, and do not hardcode one database provider into a
generic pipeline. The integration-test environment is isolated from Development
and Production data (`dotnet-testing` skill).

## Dependency Security

```bash
dotnet package list --vulnerable --include-transitive
```

NuGet auditing is also integrated into restore for modern .NET SDKs. Treat
findings according to the project's security policy, and do not upgrade
packages automatically in CI unless the project adopted automated dependency
updates.

## Build Artifacts

```bash
dotnet publish \
  backend/MyApp.Api/MyApp.Api.csproj \
  --configuration Release \
  --output ./artifacts/api \
  --no-build
```

For the frontend, run its build script (for example `npm run build`). Store or
publish only artifacts required by later stages.

## Docker

When the project deploys containers, follow the `docker` skill and build and
publish the image from CI. Do not add Docker to the pipeline merely because the
skill supports it.

## Build Once, Promote

For a deployment model that supports artifact promotion, prefer promoting the
same tested artifact or image through environments over recompiling different
production code per environment; environment-specific behavior comes from
runtime configuration.

## Secrets

Use the CI platform's secret/identity mechanism, never real secrets in pipeline
YAML, and prefer workload/federated identity over long-lived deployment
credentials when the platform supports it.

## Database Migrations

If deployment performs migrations, make the migration step explicit, use the
project's approved credentials, run it at a controlled point in the deployment,
and fail visibly when it fails. Migration scripts or artifacts may be generated
earlier in CI and executed during deployment (persistence knowledge skill
§ Migrations).

## Deployment

CI and CD may be separate workflows. A successful CI build does not imply that
every branch deploys; use environment protection/approval where appropriate to
the hosting platform.

## Pipeline Verification

Before considering a pipeline complete, confirm that it restores from a clean
environment, builds the backend, builds the frontend when present, runs
configured tests, does not depend on developer-machine state, does not expose
secrets, and produces the expected artifacts.

## Review Checks

Check-by-reference against `verify` § Delivery Changes and `security.md`:
project-specific database infrastructure in a generic pipeline; deployment
secrets in YAML; different source rebuilt per environment without a reason;
failing tests suppressed to permit deployment; automatic production seeding or
startup migrations; assumed Docker deployment; assumed frontend scripts.
