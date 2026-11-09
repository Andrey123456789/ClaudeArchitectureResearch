---
paths:
  - "**/*.csproj"
  - "**/Directory.Packages.props"
  - "**/package.json"
  - "**/package-lock.json"
---

> Path-scoped rule. Owns: dependency need, NuGet Central Package Management, npm package management · Scope: common, backend, frontend · Loads: when package or project manifests are in context · Depends on: CLAUDE.md, docs/technology-stack.md · Enforced by: .claude/scripts/check-manifests.mjs (run by the manifest hook)

# Dependency Rules

Adding, updating, or removing a dependency follows the `add-dependency`
workflow (version selection, due diligence, licensing, peer conflicts).
Approved technologies: `docs/technology-stack.md`.

## Need

- Add a dependency only when it solves a concrete current requirement; do not
  install packages for hypothetical future use.

## NuGet

- Use NuGet Central Package Management: package versions belong in
  `Directory.Packages.props`. `PackageReference` entries in project files must
  not carry versions, and centrally managed versions must not be duplicated in
  individual `.csproj` files.
- Keep each package reference in the narrowest project that actually requires
  it; do not add a package to every project merely because the projects share a
  solution.

## npm

- Use npm for the Angular workspace unless the project deliberately adopts
  another package manager. Maintain and commit `package.json` and
  `package-lock.json`, and keep the lockfile consistent with every dependency
  change.
- Build and test tooling belongs in `devDependencies`; runtime `dependencies`
  hold what the application ships, unless there is a concrete reason otherwise.
