---
paths:
  - "frontend/**/*"
---

> Kind: STD | Scope: frontend | Capability: — | Loading: path-scoped (frontmatter paths)

# npm Dependency Standard

- npm is the frontend package manager unless the project deliberately adopts another. `package.json` and `package-lock.json` must stay together and consistent (when an authorized commit is part of this task, include both files; otherwise update them without creating a Git commit), and build/test tooling belongs in `devDependencies`, not runtime `dependencies`, unless there is a concrete reason.

Procedure: `add-dependency`. Enforced by: `.claude/scripts/check-manifests.cjs` (manifest hook and `verify`).
