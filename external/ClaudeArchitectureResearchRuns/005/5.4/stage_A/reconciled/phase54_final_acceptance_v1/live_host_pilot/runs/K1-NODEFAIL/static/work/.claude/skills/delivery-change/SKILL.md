---
name: delivery-change
description: >
  Procedure for creating or changing CI/CD pipelines, container builds, and
  deployment steps: discover surfaces, reproduce supported commands, keep
  failures visible, lockfile-based frontend CI, deliberate production
  migrations, secrets, pipeline verification. Use for GitHub Actions or other CI
  files, Dockerfiles, Compose files, or release workflows.
---

> Kind: WF | Scope: delivery | Capability: — | Loading: on-demand workflow

# Delivery Change

Read first: `.claude/rules/common/security.md` and, for container images, `.claude/rules/backend/operations.md`. Technique: `ci-cd`, `docker`. Containers are optional infrastructure (decision register).

## 1. Discover

Inspect the repository before writing a pipeline or container file: .NET backend, frontend workspace, test projects, Dockerfiles, provider-specific integration tests, generated clients, deployment artifacts. Do not assume a database provider, cache, container tooling, or frontend tooling exists, and add stages for the actual project, not generic boilerplate.

## 2. Continuous integration

- CI definitions must live in source control, reproduce the repository's supported build and test commands, and never hide build or test failures (no suppressed tests, ignored exit codes, or continue-on-error for required checks).
- Frontend CI must use scripts that actually exist in the workspace's `package.json` and must use `npm ci` when a maintained lockfile supports it; never invent npm scripts and never reflexively replace a lockfile-based install with `npm install`.
- Enforced formatting/analyzer gates only when the project has adopted them; dependency vulnerability inspection per the project's security policy; no automatic package upgrades unless the project adopted automated updates.
- Integration-test infrastructure: per `ci-cd` (Integration-test infrastructure).

## 3. Containers and artifacts

Build images and deployable artifacts only when the project deploys them; publish only artifacts later stages need, reproducibly. Runtime images: `.claude/rules/backend/operations.md`. Images, build arguments, and committed Compose files are source-controlled surfaces for `.claude/rules/common/security.md` (Secrets).

## 4. Production database migrations

- Production database migrations must not run automatically from normal application startup by default. An exception needs the user's explicit request naming it and its scope, recorded through `architecture-decision`; a generic workflow approval is not one, and it never allows Development seeding in Production. A production migration is an explicit deployment operation: make the step explicit, use the project's approved credentials, run it at a controlled point, and fail visibly on error.
- Development seeding never runs in Production.

## 5. Secrets and deployment

Pipeline secrets come from the CI platform's secret/identity mechanism (prefer workload or federated identity over long-lived credentials), per `.claude/rules/common/security.md`. A green CI build does not imply every branch deploys; use environment protection or approval where the hosting platform supports it.

## 6. Verify

Before considering the pipeline complete, verify that it restores from a clean environment, builds the backend, builds the frontend when present, runs the configured tests, does not depend on developer-machine state, does not expose secrets, and produces the expected artifacts. Report each item as PASS / NOT RUN / NOT APPLICABLE.
