---
paths:
  - "**/*"
---
Kind: STD | Scope: common | Capability: — | Loading: path-scoped (all files)

# Dependency Standards

Adding or updating any NuGet or npm dependency runs the `add-dependency` workflow, which owns version, license, vulnerability and approval checks. Approved and conditional technologies: decision register.

## Need

- Add a dependency only for a concrete current requirement. Do not install packages for hypothetical future use; an approved conditional technology is added when its capability is needed, not by default.
- Prefer removing a dependency that the current change makes unused when that is safe to verify. Do not perform unrelated dependency cleanup during a narrowly scoped task.

## NuGet (backend)

- Use NuGet Central Package Management: package versions live in `Directory.Packages.props`. Project `PackageReference` entries are versionless by default (a `VersionOverride` needs a concrete reason) and never duplicate a centrally managed version. Keep each reference in the narrowest project that needs it, not in every project of the solution.

## npm (frontend)

- Use npm for the frontend workspace unless the project deliberately adopts another package manager. Keep `package.json` and `package-lock.json` committed and consistent, and put build and test tooling in `devDependencies`, not runtime `dependencies`, unless there is a reason.
