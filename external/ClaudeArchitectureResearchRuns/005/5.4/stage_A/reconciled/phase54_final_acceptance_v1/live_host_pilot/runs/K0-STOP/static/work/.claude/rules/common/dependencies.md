---
paths:
  - "**/*.csproj"
  - "**/Directory.Packages.props"
  - "**/Directory.Build.props"
  - "**/package.json"
  - "**/package-lock.json"
---

> Kind: STD | Scope: common | Owner: dependency manifests — need, NuGet Central Package Management, npm manifests | Loading: path-scoped

# Dependency Standard

Workflow: adding, updating or removing a package → `add-dependency` (version, deprecation, vulnerability and license checks). Approved and conditional technologies: decision register.

## Need

- Add a dependency only for a concrete current requirement; do not install packages for hypothetical future use. An approved conditional technology is added only when its capability is actually needed.

## NuGet

- Use NuGet Central Package Management (D-17): what counts is the value MSBuild evaluates, so the effective `ManagePackageVersionsCentrally` must be true for each project wherever the MSBuild chain sets it, no project, condition or later file may turn it off, and package versions belong in `Directory.Packages.props` (typically at the repository root; a nested one that MSBuild imports for each project is equally valid). Project `PackageReference` entries are versionless by default — a `VersionOverride` needs a concrete, reported reason — and must not duplicate centrally managed versions.
- Keep each package reference in the narrowest project that actually requires it; do not add a package to every project merely because the projects share a solution.

## npm

- npm is the package manager for the Angular workspace (D-09) unless the project deliberately adopts another.
- Keep `package.json` and `package-lock.json` together and the lockfile consistent with every dependency change; when an authorized commit is part of this task, include both files, and otherwise update them without creating a Git commit.
- Put build and test tooling in `devDependencies`, not runtime `dependencies`, unless there is a concrete reason.
