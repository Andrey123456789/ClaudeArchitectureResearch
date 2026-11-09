---
paths:
  - "backend/**/*"
  - "frontend/**/*"
  - "**/*.csproj"
  - "**/Directory.Packages.props"
  - "**/Directory.Build.props"
  - "**/package.json"
  - "**/package-lock.json"
---

> Level: 3-project · Owns: package-management conventions (NuGet Central Package Management, npm) · Scope: backend, frontend · Loading: path

# Package Management

- Use NuGet Central Package Management: package versions live only in `Directory.Packages.props`; project `PackageReference` entries are versionless — never duplicate a centrally managed version in a project file, and use a `VersionOverride` only for a concrete, reported reason — and sit in the narrowest project that actually needs the package. What counts is the value MSBuild evaluates: the effective `ManagePackageVersionsCentrally` must be true for each project, whether it is set in `Directory.Packages.props` or inherited, and no project, condition, or later file may turn it off.
- Use npm for the frontend workspace unless the project deliberately adopts another package manager: keep `package.json` and `package-lock.json` together and the lockfile consistent (when an authorized commit is part of this task, include both files; otherwise update them without creating a Git commit), and place build/test tooling in `devDependencies` rather than runtime `dependencies` without a reason.

Mechanical check: manifest hook (`.claude/hooks/post-change-checks.mjs`, edits and shell calls). Adding or updating packages: `add-dependency`.
