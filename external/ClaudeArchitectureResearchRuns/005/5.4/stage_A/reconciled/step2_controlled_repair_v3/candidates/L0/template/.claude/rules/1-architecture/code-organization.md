---
paths:
  - "backend/**/*"
  - "frontend/**/*"
  - "docs/**/*"
  - "*.slnx"
---

> Level: 1 Architecture · Owns: physical code organization by responsibility, test-project reference discipline · Scope: common, backend-tests · Loads: path rule · Depends on: CLAUDE.md, .claude/rules/1-architecture/backend-layers.md

# Code Organization

Concrete layout and project names: `3-project/layout.md`. Directory examples: the `project-structure` workflow references.

- Physical structure follows actual responsibilities. Do not create speculative projects, infrastructure, empty directory trees, or generic `Common`/`Helpers`/`Utils` buckets solely to make the repository look architectural.
- Name supporting types so their architectural role is clear from the type name, its immediate directory, or both (prefer). Split a feature into responsibility-specific subdirectories only when a flat directory has become hard to navigate.
- Backend test projects must not receive broader production-project references than their test scope requires; they follow the same inward dependency discipline as the production architecture.
