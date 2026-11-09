---
paths:
  - "**/*"
---
Kind: STD | Scope: common | Capability: — | Loading: path-scoped (all files)

# Repository Structure Standards

Repository layout decision: decision register → Repository defaults. Scaffolding procedure: `project-structure`.

- Physical structure follows actual responsibilities. Do not create speculative projects, infrastructure, empty directory trees, or generic `Common`, `Helpers` or `Utils` buckets merely to make the repository look architectural. Create a directory when it holds real content with a cohesive responsibility that can be named.
