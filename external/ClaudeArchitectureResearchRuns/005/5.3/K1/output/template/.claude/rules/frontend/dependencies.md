---
paths:
  - "frontend/**/*"
---

> Kind: STD | Scope: frontend | Capability: — | Loading: path-scoped (frontmatter paths)

# npm Dependency Standard

- npm is the frontend package manager unless the project deliberately adopts another. `package.json` and `package-lock.json` must be committed and kept consistent, and build/test tooling belongs in `devDependencies`, not runtime `dependencies`, unless there is a concrete reason.

Procedure: `add-dependency`. Enforced by: `.claude/scripts/check-manifests.cjs` (manifest hook and `verify`).
