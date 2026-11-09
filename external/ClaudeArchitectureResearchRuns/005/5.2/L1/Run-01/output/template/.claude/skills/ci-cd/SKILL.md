---
name: ci-cd
description: >
  Use for CI/CD pipelines (GitHub Actions or equivalent): restore/build/test
  jobs, frontend jobs, artifacts, audits, secrets, deployment and migration
  stages.
---
> Level: 2-technology | Owns: CI/CD pipeline technique and examples | Scope: common | Loads: on demand (skill)

# CI/CD

Procedure and obligations: `delivery`. This skill is the technique reference.

## Backend job

```bash
dotnet restore
dotnet build --no-restore --configuration Release
dotnet test --no-build --configuration Release
```

Optional enforced check, only when the project adopted it:
`dotnet format --verify-no-changes --no-restore`.

## Frontend job

Use the commands in `frontend.commands`: the lockfile-based clean install, then
the build, configured unit tests, and lint when configured.

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
      - uses: actions/checkout@v4
      - uses: actions/setup-dotnet@v4
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
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: 24
          cache: npm
          cache-dependency-path: frontend/MyApp.Web/package-lock.json
      - run: npm ci
      - run: npm run build
```

Adapt action and runtime versions to the repository's supported versions; omit
the frontend job when no frontend exists and add test/lint steps only for
scripts the workspace defines.

## Integration-test services

Provision a database or other service only when tests require it, isolated from
Development and Production data, matching the persistence slot's declared
relational test fidelity; do not hardcode one provider into a generic template.

## Dependency security

`dotnet package list --vulnerable --include-transitive`; NuGet auditing also
runs during restore on modern SDKs. Frontend audit: `frontend.commands`. Do not
upgrade packages automatically in CI unless the project adopted automated
dependency updates.

## Artifacts

```bash
dotnet publish backend/MyApp.Host/MyApp.Host.csproj --configuration Release --output ./artifacts/api --no-build
```

(`MyApp.Host` stands for the composition-root host project.)

Publish only artifacts later stages need. Where the deployment model supports
it, build once and promote the same tested artifact or image through
environments; environment differences come from runtime configuration.

## Containers

Build and publish images from CI only when the project deploys containers
(`docker`).

## Secrets and identity

Use the CI platform's secret store; prefer workload/federated identity over
long-lived deployment credentials.

## Database migrations

Generate migration scripts or bundles in CI (`persistence.workflow`) and execute
them as an explicit, controlled, visibly failing deployment step (`delivery`).

## Deployment

CI and CD may be separate workflows; a green CI build does not imply every
branch deploys. Use environment protection/approval where the platform offers
it.

## Anti-patterns

Project-specific database infrastructure in a generic pipeline; secrets in
YAML; rebuilding different source per environment without a reason;
suppressed failing tests; automatic production seeding or startup migrations;
assuming containers; assuming frontend scripts the workspace does not define.
