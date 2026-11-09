---
paths:
  - "**/*.csproj"
  - "**/Directory.Packages.props"
  - "**/package.json"
  - "**/package-lock.json"
---

> Owns: dependency necessity, NuGet Central Package Management, npm lockfile and dependency categories, peer-dependency conflict handling | Scope: common (backend and frontend manifests) | Loads: path; enforced by the manifest hook and Bash guard

# Dependency Rules

Approved and conditional technologies: `docs/technology-stack.md`. Version
selection, deprecation/vulnerability/license checks, and commercial-license
approval for any addition or update: `add-dependency` workflow.

## General Principle

Add a dependency only for a concrete current requirement; never install packages
for hypothetical future use. "Approved" does not mean "install by default".

## NuGet

Use NuGet Central Package Management: versions belong in
`Directory.Packages.props`, project files contain versionless `PackageReference`
entries by default, and centrally managed versions are not duplicated in
individual `.csproj` files. Keep each package reference in the narrowest
project that actually requires it.

```xml
<!-- Directory.Packages.props -->
<PackageVersion Include="FluentValidation" Version="..." />

<!-- Project.csproj -->
<PackageReference Include="FluentValidation" />
```

## npm

- Use npm by default for the Angular workspace unless the project deliberately
  adopts another package manager. Commit `package.json` and `package-lock.json`
  and keep the lockfile consistent.
- Put build/test tooling in `devDependencies`, not runtime `dependencies`,
  unless there is a reason.
- Never use `--force` or `--legacy-peer-deps` merely to bypass incompatible peer
  dependencies; resolve the actual compatibility problem.

## Removal

Remove dependencies that become unused when that is part of the current change
and safe to verify; do not perform unrelated dependency cleanup during a
narrowly scoped task.
