---
paths:
  - "backend/**"
  - "frontend/**"
  - "docs/**"
  - "*.slnx"
---

> Owner: proportional physical repository structure | Scope: common | Loads: path (any backend, frontend, or docs file); read explicitly by `project-structure` | Enforced: `code-review` structure check

# Repository Structure Rules

- Do not create speculative projects, infrastructure, empty directory trees, or
  generic `Common`, `Helpers`, or `Utils` buckets solely to make the repository
  look architectural; create a project or directory when it holds code with a
  cohesive responsibility.

Default layout: `CLAUDE.md` § Architecture Decisions. Adding a production
project beyond the default Clean Architecture projects is a Reserved decision
(`CLAUDE.md` § Decision Control); the procedure is the `project-structure`
workflow.
