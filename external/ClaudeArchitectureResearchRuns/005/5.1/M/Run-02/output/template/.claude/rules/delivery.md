---
paths:
  - ".github/**"
  - "**/*.yml"
  - "**/*.yaml"
  - "**/Dockerfile*"
  - "**/.dockerignore"
---

> Owner: CI pipeline truthfulness, frontend CI installs, production container images | Scope: delivery (CI/CD and container files) | Loads: path (pipeline, Compose, and container files); read explicitly by `verify` for delivery changes | Enforced: `verify` delivery check

# Delivery Rules

Technique: `ci-cd` and `docker` skills. Whether to containerize at all:
`docs/technology-stack.md` § Conditional Technologies.

## CI

- CI definitions stay in source control, reproduce the repository's supported
  build and test commands, and must not hide build or test failures.
- Frontend CI must run only npm scripts that actually exist and install with
  `npm ci` when a maintained lockfile supports it; do not invent scripts or
  reflexively replace lockfile-based installs.
- A pipeline step that applies database migrations follows
  `.claude/rules/persistence.md` § Migrations; read it before adding one.

## Containers

- Default: production containers use an appropriate runtime image (the ASP.NET
  runtime image for ASP.NET Core) rather than the SDK image for convenience, and
  do not switch to root merely to bypass filesystem permission problems.
