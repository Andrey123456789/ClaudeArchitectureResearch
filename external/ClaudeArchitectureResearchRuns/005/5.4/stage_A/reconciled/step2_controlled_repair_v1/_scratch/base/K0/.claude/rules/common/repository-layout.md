---
paths:
  - "backend/**"
  - "frontend/**"
  - "docs/**"
  - "*.slnx"
---

> Kind: STD | Scope: common | Owner: physical repository structure | Loading: path-scoped

# Repository Layout Standard

Layout, solution format and shared build files: D-16, D-17, D-18.

Workflow: creating or changing projects or top-level structure → `project-structure`.

- Physical structure must follow actual responsibilities: do not create speculative projects, infrastructure, empty directory trees, or generic `Common`, `Helpers` or `Utils` buckets solely to make the repository look architectural.
- Create a project, directory or documentation folder when it holds real content with a cohesive, nameable responsibility.
