---
paths:
  - "backend/**"
  - "frontend/**"
  - "*.slnx"
  - "*.props"
  - "global.json"
  - "**/*.yml"
  - "**/*.yaml"
  - "**/Dockerfile*"
  - "**/.env*"
---
<!-- Kind: STD | Scope: common | Owns: dependency need and package-manifest conventions (NuGet, npm) | Loads: path-scoped (common globs) -->
# Dependency Standards

Approved and conditional technologies: decision register. Build and package files: DEC-BUILD-01.

## Need

- Every dependency **must** serve a concrete current requirement; **never** install packages for hypothetical future use.

## NuGet

- **Must** use NuGet Central Package Management: package versions live in `Directory.Packages.props`; project `PackageReference` entries are versionless by default (a centrally managed version is never duplicated in a `.csproj` file; a `VersionOverride` needs a concrete, reported reason) and sit in the narrowest project that actually needs the package — not in every project of the solution.

## npm

- **Must** use npm for the Angular workspace unless the project deliberately adopts another package manager; keep `package.json` and `package-lock.json` committed and consistent, and put build/test tooling in `devDependencies` rather than runtime `dependencies` unless there is a reason.

Workflow: adding, updating or removing a package — `add-dependency`.
