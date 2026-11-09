---
name: delivery
description: >
  Run when creating or changing CI/CD pipelines, container builds, release
  artifacts, deployment steps, or production migration steps.
---
> Level: 0-core | Owns: delivery procedure — CI definitions, frontend CI install, deployment-time database migration | Scope: common, backend, frontend | Loads: on demand (skill)

# Delivery

## 1. Discover the repository

Before writing a pipeline, determine what exists: .NET backend, frontend
workspace (the `frontend` slot), test projects, container files,
provider-specific integration tests, generated clients, deployment artifacts.
Do not assume containers, a frontend, or a particular database exist; add
stages for the actual project, not generic boilerplate.

## 2. CI definitions

- CI definitions stay in source control and reproduce the repository's
  supported build and test commands (backend: restore, build, and test in
  Release; tests per `backend-testing.commands`).
- CI must never hide build or test failures — no suppressed or skipped failing
  tests to permit deployment.
- Run formatting or analyzers in CI only when the project adopted them as
  enforced checks.

## 3. Frontend CI

When the `frontend` slot is selected: use only scripts that actually exist in
the workspace manifest, and install with the lockfile-based clean install from
`frontend.commands` whenever a maintained lockfile supports it. Do not invent
scripts or reflexively replace the lockfile-based install with an ordinary
install.

## 4. Test infrastructure and secrets

Provide external services in CI only when tests require them; integration-test
environments stay isolated from Development and Production data, and use the
persistence slot's declared relational test fidelity. Use the CI platform's
secret or identity mechanism (prefer workload/federated identity); never put
secrets in pipeline definitions.

## 5. Containers and artifacts

Build and publish container images only when container deployment is part of
the project (project stack). Produce deployable artifacts deliberately and
reproducibly; technique: `ci-cd`, `docker`.

## 6. Database migrations in deployment

- Do not automatically apply production database migrations from normal
  application startup by default. Production migration is an explicit
  deployment operation: run it at a controlled point with the project's
  approved credentials, and make a failure visible (script generation:
  `persistence.workflow`).
- Never run Development seeding in Production.

## 7. Verify the pipeline

Before considering it complete, confirm it restores from a clean environment,
builds the backend (and frontend when present), runs the configured tests, does
not depend on developer-machine state, exposes no secrets, and produces the
expected artifacts. A successful CI build does not by itself imply deployment
of every branch; use environment protection where the platform supports it.
