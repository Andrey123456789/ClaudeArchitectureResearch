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

> Level: 0 Core | Owns: physical structure follows actual responsibilities | Scope: common | Loads: path | Depends on: none

# Structure Principles

- Do not create speculative projects, infrastructure, empty directory trees, or
  generic `Common`, `Helpers`, or `Utils` buckets solely to make the repository
  look architectural. Create a project, directory, or shared location only when
  it holds real code with a cohesive, nameable responsibility.

New projects or structural reorganization: → run `project-structure`.
