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

- Use NuGet Central Package Management (D-17): the effective `ManagePackageVersionsCentrally` is true wherever the MSBuild chain sets it, no project or later file disables it, and package versions belong in `Directory.Packages.props`. Project `PackageReference` entries are versionless by default — a `VersionOverride` needs a concrete, reported reason — and must not duplicate centrally managed versions.
- Keep each package reference in the narrowest project that actually requires it; do not add a package to every project merely because the projects share a solution.

## npm

- npm is the package manager for the Angular workspace (D-09) unless the project deliberately adopts another.
- Commit `package.json` and `package-lock.json`, and keep the lockfile consistent with every dependency change.
- Put build and test tooling in `devDependencies`, not runtime `dependencies`, unless there is a concrete reason.
