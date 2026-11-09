---
name: ci-cd
description: >
  Use for build, test, release, or deployment pipelines (GitHub Actions or
  similar): restore/build/test steps, npm ci, artifacts, dependency audits, CI
  secrets, migration steps.
---

> Knowledge skill. Owns: CI/CD pipeline technique and examples · Scope: delivery · Loads: on demand · Depends on: CLAUDE.md, .claude/rules/security.md

# CI/CD

CI/CD obligations (pipelines in source control, supported commands, visible
failures, repository-declared frontend scripts and `npm ci`, production
migrations as explicit deployment work): `development-workflow`. Secrets:
`security.md`. Add pipeline stages according to the actual project, not generic
boilerplate.

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

Run formatting or analyzers when the repository has adopted them as enforced
checks, for example `dotnet format --verify-no-changes --no-restore`; an
optional local formatter does not become a mandatory CI gate without that
decision.

## Frontend CI

```bash
npm ci
```

Then run the frontend's own scripts — typically build, unit tests when
configured, lint when configured (`angular` skill).

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
add frontend test/lint steps only when the project defines those scripts.

## Integration-Test Infrastructure

Provide external services (SQL Server, PostgreSQL, Redis, a message broker) only
when tests require them, without hardcoding one provider into a generic
template; the CI test environment stays isolated from Development and
Production data (`testing.md`).

## Dependency Security

`dotnet package list --vulnerable --include-transitive` inspects .NET
vulnerabilities, and NuGet auditing is integrated into restore in modern SDKs.
Treat findings according to the project's security policy; automatic package
upgrades in CI require an explicit project decision.

## Build Artifacts

```bash
dotnet publish \
  backend/MyApp.Api/MyApp.Api.csproj \
  --configuration Release \
  --output ./artifacts/api \
  --no-build
```

For Angular, `npm run build`. Store or publish only artifacts required by later
stages.

## Containers

Build and publish images from CI only when container deployment is part of the
project (`docker` skill).

## Build Once, Promote

When the deployment model supports artifact promotion, prefer promoting the
same tested artifact or image through environments over recompiling per
environment; environment-specific behavior comes from runtime configuration.

## Secrets and Identity

Use the CI platform's secret and identity mechanisms; prefer workload/federated
identity over long-lived deployment credentials when the platform supports it.

## Database Migrations in Deployment

Rule: `development-workflow` (Database deployment). Pipeline technique: a
dedicated migration step at a controlled point in the deployment that fails
visibly when the migration fails; migration scripts or bundles may be generated
in CI and executed during deployment.

## Deployment

CI and CD may be separate workflows; a green CI build does not imply that every
branch deploys. Use environment protection and approvals where appropriate to
the hosting platform.

## Verification

A pipeline is ready when it restores from a clean environment, builds the
backend, builds the frontend when present, runs configured tests, does not
depend on developer-machine state, does not expose secrets, and produces the
expected artifacts.

## Anti-Patterns

- project-specific database infrastructure in a generic pipeline;
- deployment secrets in YAML;
- rebuilding different source for every environment without a reason;
- suppressing failing tests to permit deployment;
- assuming Docker deployment or frontend scripts the repository does not define.
