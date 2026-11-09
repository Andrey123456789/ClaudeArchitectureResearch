---
paths:
  - "**/*"
---
> Level: 0-core | Owns: dependency necessity and responsibility-driven physical structure | Scope: common | Loads: path (all files)

# Minimal Dependencies and Structure

## Dependencies

- Add a dependency only when it solves a concrete current requirement; do not
  install packages for hypothetical future use. An approved technology is still
  conditional until its capability is needed.
- Remove a dependency that is no longer used when doing so is part of the
  current change and safe to verify; do not perform unrelated dependency cleanup
  during a narrowly scoped task.
- Procedure for every addition, update, or removal: `add-dependency`.

## Physical structure

Physical structure follows actual responsibilities. Do not create speculative
projects, infrastructure, empty directory trees, or generic `Common`, `Helpers`,
or `Utils` buckets solely to make the repository look architectural.
