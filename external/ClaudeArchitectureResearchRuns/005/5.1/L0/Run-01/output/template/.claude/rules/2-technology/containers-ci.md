---
paths:
  - "**/Dockerfile*"
  - "**/*.dockerfile"
  - "**/.dockerignore"
  - "**/docker-compose*.yml"
  - "**/docker-compose*.yaml"
  - "**/compose*.yml"
  - "**/compose*.yaml"
  - ".github/workflows/**"
  - "**/*pipeline*.yml"
  - "**/*pipeline*.yaml"
  - "**/.gitlab-ci.yml"
---

> Level: 2 Technology · Owns: container image and CI command rules · Scope: delivery (backend containers, frontend CI) · Loads: path

# Containers and CI

- **Default:** production container images use the appropriate runtime image — the ASP.NET Core runtime image for ASP.NET Core applications, the .NET runtime image for workers — never the SDK image merely for convenience. Run as the image's non-root user where supported, and do not switch to root merely to bypass a filesystem permission problem.
- **Must**, in CI, run only frontend scripts that actually exist in `package.json`, and install with `npm ci` when a maintained lockfile supports it; never invent npm scripts or reflexively replace lockfile-based installs with `npm install`.

Technique: `docker`, `ci-cd` skills.
