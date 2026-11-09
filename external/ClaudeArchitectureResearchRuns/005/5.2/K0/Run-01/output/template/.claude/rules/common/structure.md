---
paths:
  - "backend/**"
  - "frontend/**"
  - "*.slnx"
  - "*.props"
  - "global.json"
  - "**/*.yml"
  - "**/*.yaml"
  - "**/Dockerfile*"
  - "**/.env*"
---
<!-- Kind: STD | Scope: common | Owns: physical repository structure | Loads: path-scoped (common globs) -->
# Repository Structure Standards

Default layout: DEC-LAYOUT-01. A new production project or layer: CLAUDE.md § Decisions.

- Physical structure **must** follow actual responsibilities: **must not** create speculative projects, infrastructure, empty directory trees, or generic `Common`, `Helpers` or `Utils` buckets solely to make the repository look architectural. Create a directory when it holds meaningful code or documentation, and name it after a cohesive responsibility.

Workflow: scaffolding or reorganizing — `project-structure`.
