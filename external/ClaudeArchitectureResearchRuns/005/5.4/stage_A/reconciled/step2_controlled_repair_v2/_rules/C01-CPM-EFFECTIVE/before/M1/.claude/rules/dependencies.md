---
paths:
  - "**/*.csproj"
  - "**/Directory.Packages.props"
  - "**/Directory.Build.props"
  - "**/package.json"
  - "**/package-lock.json"
---

> Path rule · Scope: common (dependency manifests) · Owns dependency need, NuGet Central Package Management, and npm manifest policy · Procedure: `add-dependency` workflow

# Dependency Rules

Adding, updating, or removing a NuGet or npm dependency follows the
`add-dependency` workflow (version selection, deprecation, vulnerability, and
license checks). Approved technologies: `docs/technology-stack.md` and
`docs/capabilities/`.

## General Principle

Add a dependency only when it solves a concrete current requirement. Do not
install packages for hypothetical future use.

## NuGet

Use NuGet Central Package Management. Package versions belong in
`Directory.Packages.props`; project `PackageReference` entries are versionless
by default, and a `VersionOverride` needs a concrete, documented reason. Do not
duplicate centrally managed versions in individual `.csproj` files.

```xml
<!-- Directory.Packages.props -->
<ItemGroup>
  <PackageVersion Include="FluentValidation" Version="..." />
</ItemGroup>

<!-- Project.csproj -->
<ItemGroup>
  <PackageReference Include="FluentValidation" />
</ItemGroup>
```

Keep package references in the narrowest project that actually requires them;
do not add a package to every project merely because several projects belong
to the same solution.

## npm

Use npm as the default package manager for the frontend workspace unless the
project deliberately adopts another package manager. Maintain and commit
`package.json` and `package-lock.json`, and keep the lockfile consistent when
adding packages. Put build and test tooling in `devDependencies`, not runtime
`dependencies`, unless there is a reason.
