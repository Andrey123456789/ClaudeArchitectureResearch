---
paths:
  - "**/*.csproj"
  - "**/Directory.Packages.props"
  - "**/package.json"
  - "**/package-lock.json"
---

> Level: 0 Core · Owns: technology-neutral dependency hygiene · Scope: common · Loads: path rule · Depends on: CLAUDE.md

# Dependency Hygiene

The procedure for adding, updating, or removing a dependency is `add-dependency`; package-manager bindings are in `3-project/package-management.md`; the approved stack is in `3-project/decisions.md`.

- Add a dependency only for a concrete current requirement of the change at hand; do not install packages for hypothetical future use. "Approved" or "conditional" in the project decisions does not mean "install by default".
- Keep each dependency in the narrowest project or workspace that actually requires it.
- Remove a dependency that the current change makes unused when doing so is safe to verify; do not perform unrelated dependency cleanup during a narrowly scoped task (prefer).
