---
paths:
  - "backend/**"
  - "frontend/**"
  - "Directory.Packages.props"
---

> Level: 3 Project · Owns: package-management and test-framework conventions · Scope: backend, backend-tests, frontend · Loads: path; read explicitly by `add-dependency`, `project-structure`

# Project Conventions

## NuGet (backend)

- **Must** use NuGet Central Package Management: package versions live in `Directory.Packages.props`, and project files never duplicate centrally managed versions. `PackageReference` entries are versionless (default — an override needs a concrete reason that is reported) and live only in the narrowest project that actually requires the package.

## npm (frontend)

- **Default:** use npm for the Angular workspace unless the project deliberately adopts another package manager. Commit `package.json` and `package-lock.json`, keep the lockfile consistent when adding packages, and put build and test tooling in `devDependencies`, not runtime `dependencies`.

## Backend test framework

- **Default:** NUnit is the .NET automated test framework. In an established project that deliberately uses another framework, follow that convention; do not introduce a second .NET test framework without a concrete reason.

Mechanical check: the manifest hook (`.claude/hooks/post-edit.mjs`) reports versioned project references, floating or prerelease versions, and packages that are not added by default.
