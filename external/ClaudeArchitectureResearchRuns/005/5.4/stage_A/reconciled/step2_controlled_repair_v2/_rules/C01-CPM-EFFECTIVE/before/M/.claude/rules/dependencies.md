---
paths:
  - "**/*.csproj"
  - "**/Directory.Packages.props"
  - "**/package.json"
  - "**/package-lock.json"
---

> Owns: dependency need, NuGet Central Package Management, npm package manager, lockfile, and dependency categories | Scope: common (package manifests) | Loads: path-scoped (manifest files)

# Dependency Rules

Adding, updating, or removing a dependency follows `add-dependency` (version
selection, due diligence, license approval). Approved technologies:
`docs/technology-stack.md`. Manifests are checked by
`.claude/scripts/check-manifests.mjs` through the manifest hook.

## Need

Add a dependency only when it solves a concrete current requirement; do not
install packages for hypothetical future use. "Approved" does not mean "install
by default".

## NuGet

Use NuGet Central Package Management: package versions belong in
`Directory.Packages.props`, and project `PackageReference` entries are
versionless by default — do not duplicate centrally managed versions in
individual `.csproj` files. Keep each package reference in the narrowest project
that actually requires it rather than adding it to every project.

## npm

Use npm for the Angular workspace unless the project deliberately adopts another
package manager. Maintain and commit `package.json` and `package-lock.json` and
keep the lockfile consistent when packages change. Put build and test tooling in
`devDependencies`, not runtime `dependencies`, unless there is a reason.
