---
paths:
  - "backend/**"
  - "frontend/**"
  - "docs/**"
  - ".github/**"
  - "**/*.json"
  - "**/*.yml"
  - "**/*.yaml"
  - "**/*.props"
  - "**/*.targets"
  - "**/*.config"
  - "**/*.csproj"
  - "**/*.slnx"
  - "**/.env*"
  - "**/Dockerfile*"
  - "**/*.ps1"
  - "**/*.sh"
---

> Level: 0 Core | Owns: dependency necessity | Scope: common | Loads: path | Depends on: none

# Dependency Hygiene

- Add a dependency only for a concrete current requirement; do not install
  packages for hypothetical future use. "Approved" does not mean "install by
  default".
- Prefer removing a dependency that the current change made unused when the
  removal is safe to verify; do not perform unrelated dependency cleanup during
  a narrowly scoped task.

Adding or updating any package: → run `add-dependency`.
