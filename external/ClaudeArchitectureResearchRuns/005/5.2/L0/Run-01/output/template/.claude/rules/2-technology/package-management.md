---
paths:
  - "**/*.csproj"
  - "**/Directory.Packages.props"
  - "**/Directory.Build.props"
  - "**/package.json"
  - "**/package-lock.json"
---

> Level: 2 Technology | Owns: NuGet Central Package Management and npm lockfile/category rules | Scope: backend, frontend | Loads: path (package manifests) | Depends on: 0-core/dependency-hygiene.md

# Package Management

## NuGet

- Use NuGet Central Package Management: versions belong in
  `Directory.Packages.props`; project `PackageReference` entries are normally
  versionless and live in the narrowest project that needs the package. Do not
  duplicate centrally managed versions in `.csproj` files.

## npm

- Use npm for the frontend workspace unless the project deliberately adopts
  another package manager; keep `package.json` and `package-lock.json`
  committed and consistent, and put build and test tooling in
  `devDependencies`, not runtime `dependencies`, unless there is a reason.

Adding or updating packages: → run `add-dependency` (checked by the manifest hook).
