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

- Use NuGet Central Package Management: package versions live only in `Directory.Packages.props`; project `PackageReference` entries are versionless — never duplicate a centrally managed version in a project file, and use a `VersionOverride` only for a concrete, reported reason — and sit in the narrowest project that actually needs the package.
- Use npm for the frontend workspace unless the project deliberately adopts another package manager: commit `package.json` and `package-lock.json`, keep the lockfile consistent, and place build/test tooling in `devDependencies` rather than runtime `dependencies` without a reason.

Mechanical check: manifest hook (`.claude/hooks/post-edit-checks.mjs`). Adding or updating packages: `add-dependency`.
