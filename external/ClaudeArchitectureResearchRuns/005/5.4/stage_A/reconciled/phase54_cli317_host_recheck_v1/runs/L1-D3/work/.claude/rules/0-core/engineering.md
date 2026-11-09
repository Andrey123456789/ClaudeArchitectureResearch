---
paths:
  - "**/*"
---

> Level: 0-core · Owns: dependency necessity and physical-structure discipline · Scope: common · Loading: path

# Engineering Discipline

- Add a dependency only for a concrete current requirement; never install packages for hypothetical future use. Procedure: `add-dependency`.
- Physical structure follows actual responsibilities: do not create speculative projects, infrastructure, empty directory trees, or generic `Common`/`Helpers`/`Utils` buckets to make the repository look architectural.
