---
name: delivery-pipeline
description: Use when creating or changing CI/CD pipelines, Dockerfiles or Compose files, deployment steps or production migration steps.
---

> Kind: WF | Scope: delivery | Owner: CI/CD, container and deployment change procedure | Loading: workflow (model- or user-invoked)

# Delivery Pipeline

Containers are optional (D-14). Technique: `ci-cd` (pipeline shapes, artifacts, secrets) and `docker` (images, Compose, probes). Container image rules: `rules/backend/hosting.md`; secrets: `rules/common/security.md`.

## 1. Discover the repository

Inspect what actually exists before writing anything: .NET backend, Angular frontend, test projects, Dockerfiles, provider-specific integration tests, generated clients, deployment artifacts. Do not assume PostgreSQL, Redis, Docker or frontend tooling exists; add stages for the actual project, not generic boilerplate. Introduce Docker or container publishing only when the project has adopted containers.

## 2. Pipeline definition

- Keep CI definitions in source control. They must reproduce the repository's supported build and test commands and must never hide build or test failures (no suppressed or skipped failing tests to permit deployment).
- Backend: restore, build and test with the repository's commands (technique: `ci-cd`). Run formatting or analyzer gates only when the project has adopted them as enforced checks.
- Frontend: use scripts that actually exist in the workspace `package.json` — never invent npm scripts — and install with `npm ci` whenever a maintained lockfile supports it; do not reflexively replace lockfile-based installs with `npm install`.
- Provide external services (databases, caches, brokers) only when tests actually require them, isolated from Development and Production data.
- Dependency auditing follows the project's security policy; do not enable automatic package upgrades unless the project adopted them.

## 3. Production database migrations

- Do not apply production database migrations automatically from normal application startup by default. A production migration is an explicit deployment operation: a dedicated step at a controlled point of the deployment, using the project's approved credentials, failing visibly. Migration scripts or bundles may be generated earlier in CI and executed during deployment.
- Development seeding never runs in Production (`rules/backend/persistence.md` § Development seeding).

## 4. Deployment

Keep CI and CD separable; a green CI build does not mean every branch deploys. Use the platform's secret or workload-identity mechanism — never real secrets in pipeline YAML, Dockerfiles, committed Compose files or image build arguments. Use environment protection or approvals where the hosting platform supports them.

## 5. Verify the pipeline

Confirm that it restores from a clean environment, builds the backend, builds the frontend when present, runs the configured tests, does not depend on developer-machine state, does not expose secrets and produces the expected artifacts. For container changes also build the image, start the application, and check port/configuration, non-root execution and health-probe integration.

## Output

Files changed, stages and the commands they run, what was verified, and any assumption about the hosting platform that still needs confirmation.
