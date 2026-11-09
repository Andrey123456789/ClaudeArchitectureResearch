---
paths:
  - "backend/**/*"
  - "frontend/**/*"
  - "docs/**/*"
  - "*.slnx"
  - "*.sln"
  - "Directory.*.props"
  - "global.json"
---

> **Policy rule** · Owns: physical structure follows actual responsibilities · Scope: common · Loading: path (backend, frontend, docs, solution and build files)

# Repository Structure Rules

Approved layout: `docs/technology-stack.md` → Repository Layout. Scaffolding and
restructuring procedure: `project-structure`.

Do not create speculative projects or infrastructure, empty directory trees, or
generic `Common`/`Helpers`/`Utils` buckets solely to make the repository look
architectural — for example `SharedKernel` or `BuildingBlocks` projects, an
`EventBus`, or deployment manifests without a requirement. Create a project,
directory, or document tree only when it holds a real, cohesive responsibility.
