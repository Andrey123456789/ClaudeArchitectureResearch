---
paths:
  - "**/*.csproj"
  - "**/Directory.Packages.props"
  - "**/Directory.Build.props"
  - "**/package.json"
  - "**/package-lock.json"
---

> Level: 3 Project · Owns: package-manager selection — NuGet Central Package Management, npm lockfile and dependency categories · Scope: backend, frontend · Loads: path rule · Depends on: CLAUDE.md, .claude/rules/0-core/dependency-hygiene.md

# Package Management

Adding, updating, or removing a package follows `add-dependency`. Manifest edits are checked by the project hook (central versions, deny-list, project references).

## NuGet

- Use NuGet Central Package Management: package versions belong in `Directory.Packages.props`, and project `PackageReference` entries are versionless and scoped as `0-core/dependency-hygiene.md` requires (default: a `VersionOverride` needs a concrete reason and must be reported).
- Do not duplicate centrally managed versions in individual `.csproj` files.

## npm

- Use npm for the Angular workspace unless the project deliberately adopts another package manager; commit `package.json` and `package-lock.json` and keep the lockfile consistent with every change.
- Put build and test tooling in `devDependencies`, not runtime `dependencies`, unless there is a reason.
