---
paths:
  - "backend/**"
  - "frontend/**"
  - "docs/**"
  - "*.slnx"
  - "*.sln"
  - "Directory.Build.props"
  - "Directory.Packages.props"
---

> Owns: restraint in physical repository structure | Scope: common | Loads: path-scoped (files under backend/, frontend/, docs/, and solution or build files)

# Repository Structure Rules

The approved layout is in CLAUDE.md § Architecture Defaults. Scaffolding and
reorganization procedure: `project-structure`.

Physical structure follows actual responsibilities. Do not create speculative
projects, infrastructure, empty directory trees, or generic `Common`, `Helpers`,
or `Utils` buckets solely to make the repository look architectural. Create a
project, directory, or shared area when it contains real code with a cohesive
responsibility — for example, not a `SharedKernel`, `BuildingBlocks`, or
`EventBus` project without an actual requirement, an empty `ValueObjects/` or
`Events/` folder, or a test project without a concrete testing need.
