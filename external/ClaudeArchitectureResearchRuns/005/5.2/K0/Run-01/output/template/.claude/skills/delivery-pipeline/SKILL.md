---
name: delivery-pipeline
description: Use when creating or changing CI/CD pipelines (GitHub Actions or equivalent), build artifacts, container builds or publishing, deployment steps, or production database migration handling.
---
<!-- Kind: WF | Scope: delivery | Owns: CI/CD and deployment procedure, CI truthfulness, frontend CI installs, production migration handling | Loads: workflow invocation -->
# Delivery Pipeline

Docker adoption: DEC-OPS-01. Secrets: `rules/common/security.md`. Container runtime image: `rules/backend/operations.md` § Containers. Technique and examples: `ci-cd` and `docker` knowledge skills.

## Obligations

- CI definitions **must** stay in source control, reproduce the repository's supported build and test commands, and keep build/test failures visible — **never** suppress failing tests to permit deployment.
- Frontend CI **must** run npm scripts that actually exist in the workspace and use `npm ci` when a maintained lockfile supports it; **never** invent npm scripts or reflexively replace a lockfile-based install with `npm install`.
- **Must not** apply production database migrations automatically from normal application startup by default: a production migration is an explicit deployment operation, run at a controlled point with the project's approved credentials and failing visibly; Development seeding **never** runs in Production.

## 1. Discover the Repository

Before writing a pipeline, determine what exists: .NET backend, Angular frontend, test projects, Dockerfiles, database/provider-specific integration tests, generated clients, deployment artifacts. Do not assume PostgreSQL, Redis, Docker or frontend tooling exists. Add stages for the actual project, not generic boilerplate.

## 2. Backend Stage

Restore, build and test with the repository's supported commands, for example:

```bash
dotnet restore
dotnet build --no-restore --configuration Release
dotnet test --no-build --configuration Release
```

Run formatting/analyzer gates only when the repository has adopted them as enforced checks (for example `dotnet format --verify-no-changes --no-restore`); do not turn an optional local formatter into a mandatory CI gate without that decision.

## 3. Frontend Stage

When an Angular workspace exists: `npm ci`, then the workspace's own scripts — typically build, plus unit tests and lint when configured.

## 4. Integration-Test Infrastructure

Provide external services (SQL Server, other databases, Redis, message brokers) only when tests actually require them; do not hardcode one database provider into a generic pipeline. Keep the integration-test environment isolated from Development and Production data (`rules/backend-tests/testing.md`).

## 5. Secrets and Identity

Use the CI platform's secret/identity mechanism; no real secrets in pipeline YAML. Prefer workload/federated identity over long-lived deployment credentials when the platform supports it.

## 6. Dependency Checks

Use `dotnet package list --vulnerable --include-transitive` (NuGet auditing is also part of restore in modern SDKs) and `npm audit` as evidence according to the project's security policy. Do not upgrade packages automatically in CI unless the project has adopted automated dependency updates.

## 7. Artifacts and Containers

Produce deployment artifacts deliberately and store only what later stages need (examples: `ci-cd` skill). Build and publish images only when container deployment is part of the project (DEC-OPS-01), following the `docker` skill. CI and CD may be separate workflows; a successful CI build does not imply every branch deploys — use environment protection or approval where the hosting platform supports it.

## 8. Database Migrations

Generate migration scripts or bundles in CI when useful, execute them as an explicit deployment step, and fail the deployment visibly on migration failure (Obligations).

## 9. Verify the Pipeline

Before considering a pipeline complete, verify that it restores from a clean environment, builds the backend, builds the frontend when present, runs configured tests, does not depend on developer-machine state, does not expose secrets, and produces the expected artifacts.

For Docker changes also: build the image; verify application startup, required port and configuration; verify non-root behavior when relevant; verify health-probe integration; review the image for accidental secrets or files. Run meaningful application tests outside the image or as part of the selected pipeline.

## Output

Pipeline/deployment files changed, stages and commands, secrets mechanism used, migration handling, verification performed (PASS / NOT RUN / NOT APPLICABLE).
