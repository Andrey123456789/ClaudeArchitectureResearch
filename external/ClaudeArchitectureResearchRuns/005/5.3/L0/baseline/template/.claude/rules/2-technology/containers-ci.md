---
paths:
  - "Dockerfile*"
  - "**/Dockerfile*"
  - "backend/**/Dockerfile*"
  - "**/.dockerignore"
  - "**/compose*.y*ml"
  - "**/docker-compose*.y*ml"
  - ".github/workflows/**"
  - "**/azure-pipelines*.yml"
  - "**/.gitlab-ci.yml"
---

> Level: 2 Technology · Owns: container image bindings · Scope: backend, delivery · Loads: path rule · Depends on: CLAUDE.md, .claude/rules/0-core/security-principles.md

# Containers and CI Bindings

Docker is optional infrastructure (`3-project/decisions.md`). Creating or changing CI/CD, container, or deployment definitions follows `delivery-pipeline`. Technique: `docker` and `ci-cd` skills.

- Production containers use an appropriate runtime image (the ASP.NET runtime image for ASP.NET Core applications) rather than the SDK image solely for convenience, and run as the image's non-root user where supported; do not switch to root merely to bypass filesystem-permission problems (default).
- Keep build tooling out of production runtime images and keep environment configuration external; real secrets never go into Dockerfiles, committed Compose files, or build arguments (`0-core/security-principles.md`).
