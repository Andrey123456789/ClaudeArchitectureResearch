---
name: ci-cd
description: Use when creating or reviewing build, test, release or deployment pipelines (GitHub Actions or equivalent) for the .NET backend and frontend — restore/build/test flows, frontend install and scripts, artifacts, dependency checks, container publishing, secrets and production migration steps.
---
Kind: KNW | Scope: delivery | Capability: — | Loading: on invocation

# CI/CD

Obligations for pipeline changes (source control, supported commands, visible failures, frontend lockfile installs, production migrations): `verify` → Delivery and deployment changes. Secrets: `.claude/rules/common/security.md`. Add pipeline stages according to the actual project, not generic boilerplate.

## Repository discovery

Before writing a pipeline, determine whether the repository contains a .NET backend, a frontend workspace, test projects, Dockerfiles, provider-specific integration tests, generated clients or deployment artifacts. Do not assume a particular database, Redis, Docker or frontend tooling exists.

## Backend CI

```bash
dotnet restore
dotnet build --no-restore --configuration Release
dotnet test --no-build --configuration Release
```

Run formatting or analyzers when the repository has adopted them as enforced checks, for example `dotnet format --verify-no-changes --no-restore`; do not turn an optional local formatter into a mandatory gate without the project adopting that policy. If the backend tests include the architecture-conformance test, the CI image needs Node.js.

## Frontend CI

Install with `npm ci` from the committed lockfile, then run the scripts the frontend's `package.json` defines (normally build, unit tests when configured, lint when configured). Frontend commands: the frontend workflow facet.

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

Adapt action and runtime versions to what the repository supports, and add frontend test or lint steps only when the project defines them.

## Integration-test infrastructure

Provide external services (a database, cache or message broker) in CI only when tests require them, keep the integration-test environment isolated from Development and Production data, and do not hardcode one database provider into a generic pipeline. Testing technique: the backend-testing knowledge facet.

## Dependency security

`dotnet package list --vulnerable --include-transitive` (NuGet auditing also runs during restore on modern SDKs) and `npm audit`. Treat findings by the project's security policy, and do not upgrade packages automatically in CI unless the project adopted automated dependency updates.

## Build artifacts

```bash
dotnet publish backend/MyApp.Api/MyApp.Api.csproj --configuration Release --output ./artifacts/api --no-build
npm run build
```

Store or publish only the artifacts later stages need. Build and publish container images from CI only when container deployment is part of the project (`docker` skill). For deployment models that support promotion, prefer promoting the same tested artifact or image through environments over recompiling per environment; environment differences come from runtime configuration.

## Secrets and identity

Use the CI platform's secret or identity mechanism and prefer workload or federated identity over long-lived deployment credentials where the platform supports it.

## Database migrations in deployment

When deployment applies migrations, make the step explicit, run it at a controlled point with the project's approved credentials, and let a migration failure fail the deployment visibly. Migration scripts or bundles may be generated in CI and executed during deployment (persistence workflow facet → Production migration artifacts).

## Deployment

CI and CD may be separate workflows. A green CI build does not mean every branch deploys; use environment protection or approvals appropriate to the hosting platform.

## Verification

A pipeline is complete when it restores from a clean environment, builds the backend, builds the frontend when present, runs the configured tests, does not depend on developer-machine state, does not expose secrets, and produces the expected artifacts.

## Anti-patterns

Review checks; the named owner holds each rule:

- Project-specific database infrastructure in a generic pipeline, or Docker assumed?
- Deployment secrets in YAML? (`.claude/rules/common/security.md`)
- Different source rebuilt per environment without a reason?
- Failing tests suppressed, invented npm scripts, or automatic production seeding or migration at startup? (`verify` → Delivery and deployment changes)
