---
paths:
  - "backend/**/*"
  - "Directory.Packages.props"
  - "Directory.Build.props"
---

> Kind: STD | Scope: backend | Capability: — | Loading: path-scoped (frontmatter paths)

# NuGet Dependency Standard

- NuGet Central Package Management is mandatory: package versions live in `Directory.Packages.props`; project `PackageReference` entries carry no version (central versions are never duplicated in project files; a `VersionOverride` needs a recorded reason) and live in the narrowest project that actually requires the package. What counts is the value MSBuild evaluates: the effective `ManagePackageVersionsCentrally` must be true for each project, whether it is set in `Directory.Packages.props` or inherited, and no project, condition, or later file may turn it off.

Procedure: `add-dependency`. Enforced by: `.claude/scripts/check-manifests.cjs` (manifest hook and `verify`).
