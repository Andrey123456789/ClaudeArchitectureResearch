---
paths:
  - "**/*.csproj"
  - "**/Directory.Packages.props"
  - "**/package.json"
  - "**/package-lock.json"
---

> **Policy rule** · Owns: dependency need, NuGet Central Package Management, npm package-manager and lockfile policy · Scope: common, backend, frontend · Loading: path (package and project manifests)

# Dependency Rules

## General Principle

Add a dependency only when it solves a concrete current requirement.

Do not install packages for hypothetical future use.

Approved technologies are recorded in `docs/technology-stack.md` and the
capability selection (both always loaded).

Every addition, update, or removal of a NuGet or npm dependency follows the
`add-dependency` workflow (version selection, deprecation, vulnerability and
license checks, commercial/unclear-license approval, removal).

## NuGet

Use NuGet Central Package Management for this template.

Package versions belong in:

```text
Directory.Packages.props
```

Individual project files contain versionless `PackageReference` entries.

Example:

```xml
<!-- Directory.Packages.props -->
<ItemGroup>
  <PackageVersion Include="FluentValidation" Version="..." />
</ItemGroup>
```

```xml
<!-- Project.csproj -->
<ItemGroup>
  <PackageReference Include="FluentValidation" />
</ItemGroup>
```

Do not duplicate centrally managed versions in individual `.csproj` files.

Keep package references in the narrowest project that actually requires them.

Do not add a package to every project merely because several projects belong to
the same solution.

## npm

Use npm as the default package manager for the frontend workspace unless the
project deliberately adopts another package manager.

Maintain and commit:

```text
package.json
package-lock.json
```

Use the appropriate dependency category:

```text
dependencies
devDependencies
```

Do not put build/test tooling into runtime dependencies without a reason.

When adding packages, preserve a consistent lockfile.
