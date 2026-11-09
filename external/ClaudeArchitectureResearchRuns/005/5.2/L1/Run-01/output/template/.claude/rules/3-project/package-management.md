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
> Level: 3-project | Owns: package-management conventions for NuGet and npm | Scope: backend, frontend | Loads: path (projects, manifests)

# Package Management

## NuGet

Use NuGet Central Package Management: versions live in
`Directory.Packages.props`, and project files contain versionless
`PackageReference` entries. Do not duplicate centrally managed versions in
`.csproj` files. Keep each package reference in the narrowest project that
requires it; do not add a package to every project merely because the projects
share a solution.

## npm

Use npm as the frontend package manager unless the project deliberately adopts
another. Commit `package.json` and `package-lock.json` and keep the lockfile
consistent; put build and test tooling in `devDependencies`, not runtime
`dependencies`, unless there is a reason.

The manifest hook and `node .claude/scripts/check-packages.cjs` check these
conventions. Procedure for changes: `add-dependency`.
