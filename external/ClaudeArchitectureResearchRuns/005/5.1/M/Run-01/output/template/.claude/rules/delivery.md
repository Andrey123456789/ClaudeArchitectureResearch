---
paths:
  - "**/Dockerfile*"
  - "**/.dockerignore"
  - "**/*compose*.yml"
  - "**/*compose*.yaml"
  - ".github/**/*"
  - "**/azure-pipelines*.yml"
  - "**/.gitlab-ci.yml"
---

> Owns: container runtime image policy, CI truthfulness, frontend CI install/scripts | Scope: delivery | Loads: path

# Delivery Rules

Whether Docker is used at all: `docs/technology-stack.md`. Production database
migrations and Development seeding: `persistence.md`. Secrets in images and
pipelines: `security.md`. Technique: `docker`, `ci-cd` skills.

## Containers

For production containers, use an appropriate runtime image (ASP.NET runtime for
ASP.NET Core apps) rather than the SDK image for convenience by default, and do
not switch to root merely to bypass a filesystem permission problem.

## Continuous Integration

- CI definitions stay in source control, reproduce the repository's supported
  build and test commands, and must never hide or suppress build/test failures.
- Frontend CI uses scripts that actually exist in `package.json` and installs
  with `npm ci` when a maintained lockfile supports it; do not invent npm
  scripts or reflexively replace lockfile-based installs.
