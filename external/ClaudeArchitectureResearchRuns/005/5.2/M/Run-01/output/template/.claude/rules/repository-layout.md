---
paths:
  - "backend/**"
  - "frontend/**"
  - "docs/**"
  - "*.slnx"
  - "*.sln"
---

> Path-scoped rule. Owns: proportional physical structure · Scope: common · Loads: when files under backend/, frontend/, docs/, or solution files are in context · Depends on: CLAUDE.md, docs/technology-stack.md

# Repository Layout Rules

The default layout is `docs/technology-stack.md` (Solution Layout); scaffolding
and reorganization follow the `project-structure` workflow.

- Physical structure must follow actual responsibilities: do not create
  speculative projects, infrastructure, empty directory trees, or generic
  `Common`, `Helpers`, or `Utils` buckets solely to make the repository look
  architectural. Create a project or directory when it holds real code or
  documentation with a cohesive responsibility.
