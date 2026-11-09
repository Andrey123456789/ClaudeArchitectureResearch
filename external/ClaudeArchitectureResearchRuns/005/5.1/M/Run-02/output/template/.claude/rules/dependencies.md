---
paths:
  - "**/*.csproj"
  - "**/Directory.Packages.props"
  - "**/Directory.Build.props"
  - "**/package.json"
  - "**/package-lock.json"
---

> Owner: dependency necessity, NuGet Central Package Management, npm package-manager and lockfile discipline | Scope: common (NuGet: backend; npm: frontend) | Loads: path (package and project manifests); read explicitly by `add-dependency`, `build-fix` | Enforced: PreToolUse hook routes dependency commands to `add-dependency`; `.claude/scripts/check-dependencies.mjs` on manifest changes; NuGet `NU1008`

# Dependency Rules

Approved technologies: `docs/technology-stack.md`. Version selection, license,
deprecation, and vulnerability checks: `add-dependency` workflow.

## Necessity

- Add a dependency only when it solves a concrete current requirement; do not
  install packages for hypothetical future use.

## NuGet

- Use NuGet Central Package Management: package versions belong in
  `Directory.Packages.props`, and individual projects must not duplicate them.
- Default: project `PackageReference` entries are versionless and live in the
  narrowest project that actually requires the package; do not add a package to
  every project merely because they share a solution.

## npm

- Use npm for the Angular workspace unless the project deliberately adopts
  another package manager. Commit `package.json` and `package-lock.json`, keep
  the lockfile consistent when packages change, and put build and test tooling in
  `devDependencies` rather than runtime `dependencies` without a reason.
