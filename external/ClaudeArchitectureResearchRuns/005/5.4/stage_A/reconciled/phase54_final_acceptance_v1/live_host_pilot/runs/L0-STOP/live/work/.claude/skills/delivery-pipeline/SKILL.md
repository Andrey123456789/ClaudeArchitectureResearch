---
name: delivery-pipeline
description: >
  Use when creating or changing CI/CD pipelines, Dockerfiles, Compose files, or
  deployment steps, including production database migrations.
---

> Level: 3 Project · Owns: delivery-definition procedure — CI truthfulness, frontend CI commands, production migration handling (workflow) · Scope: common, backend, frontend, delivery · Loads: on invocation (path rule `containers-ci.md` routes here) · Depends on: CLAUDE.md, .claude/rules/** (owner reads)

# Delivery Pipeline

Docker adoption is a project decision (`3-project/decisions.md`); container image bindings are in `.claude/rules/2-technology/containers-ci.md`; secrets policy is in `.claude/rules/0-core/security-principles.md` — read them first. Technique and YAML/Dockerfile examples: `ci-cd` and `docker` skills.

## 1. Discover the repository

Before writing a pipeline or container definition, inspect what actually exists: .NET backend, Angular frontend, test projects, Dockerfiles, provider-specific integration tests, generated clients, deployment artifacts. Do not assume PostgreSQL, Redis, Docker, or frontend tooling exists; add stages only for the actual project.

## 2. CI obligations

- CI definitions stay in source control, reproduce the repository's supported build and test commands, and must never hide build or test failures (no `continue-on-error` on build/test steps, no suppressed exit codes, no skipped failing tests to permit deployment).
- Backend flow: `dotnet restore` → `dotnet build --no-restore --configuration Release` → `dotnet test --no-build --configuration Release`. Run formatting/analyzer gates only when the project has adopted them as enforced checks.
- Frontend flow: install with `npm ci` when a maintained lockfile supports it — do not reflexively replace it with `npm install` — then run only scripts that actually exist in the workspace `package.json` (build, and test/lint when configured); never invent npm scripts.
- Provide external services (database, cache, broker) in CI only when tests actually require them, isolated from Development and Production data.
- Supply credentials through the CI platform's secret/identity mechanism (secrets policy: `0-core/security-principles.md`); prefer workload/federated identity over long-lived deployment credentials where supported.
- Do not let CI upgrade packages automatically unless the project adopted automated dependency updates.

## 3. Containers

When the project deploys containers, follow `containers-ci.md` and the `docker` skill: multi-stage build, explicit project-file copy for restore caching, runtime configuration passed at run time, health probes per the `health-check` skill. Build and publish images from CI only when container deployment is part of the project.

## 4. Production database migrations

- Do not apply production database migrations automatically from normal application startup by default — in containers or anywhere else. An exception needs the user's explicit request naming it and its scope, recorded through `architecture-decision`; a generic workflow approval is not one, and it never allows Development seeding in Production.
- Production migration is an explicit deployment operation: a deliberate step at a controlled point, using the project's approved credentials, failing visibly on error. Migration scripts or bundles may be generated earlier in CI and executed during deployment.
- Deployment never runs Development seeding in Production (`3-project/data-lifecycle.md`).

## 5. Deployment

CI and CD may be separate workflows; a green CI build does not imply every branch deploys. Use environment protection/approval where the hosting platform supports it. Prefer promoting the same tested artifact or image through environments, with environment differences supplied by runtime configuration (prefer).

## 6. Verify

Confirm the pipeline restores from a clean environment, builds the backend, builds the frontend when present, runs the configured tests, does not depend on developer-machine state, exposes no secrets, and produces the expected artifacts. For container changes: build the image, verify startup, port/configuration, non-root behavior when relevant, health-probe integration, and that no secrets or stray files were copied. Then run `verify`.
