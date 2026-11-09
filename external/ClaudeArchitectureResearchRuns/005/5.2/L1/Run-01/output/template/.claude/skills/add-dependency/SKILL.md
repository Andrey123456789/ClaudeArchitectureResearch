---
name: add-dependency
description: >
  Run before adding, updating, or removing a NuGet or npm package: approved
  stack, latest stable version, deprecation, vulnerabilities, license approval,
  CPM.
---
> Level: 3-project | Owns: dependency addition/update/removal procedure — version selection, due diligence, license approval, package commands | Scope: common | Loads: on demand (skill; routed by the dependency hook)

# Add or Update a Dependency

Necessity (`minimalism.md`), approved technologies (project stack and decision
facets), and package-management conventions (`package-management.md`) are owned
by rules; this workflow is the procedure.

## 1. Confirm the need and the technology

- Confirm a concrete current requirement.
- If the project has an approved technology for the capability, use it. A
  conditional technology (project stack conditional list, decision facets) is
  added only when its condition is met; for example, add the API-versioning
  package only once the project has adopted API versioning, and then use its
  Controller integration (`Asp.Versioning.Mvc`).
- Resilience: default to `Microsoft.Extensions.Http.Resilience` for `HttpClient`
  and `Microsoft.Extensions.Resilience` for general pipelines. Direct Polly usage
  is an explicit, documented exception; never add the deprecated
  `Microsoft.Extensions.Http.Polly` or `Polly.Extensions.Http`.
- A new major library or a replacement of an approved technology is Reserved.

## 2. Select the version

For every NuGet or npm addition or update:

1. Determine the latest **stable** version compatible with the project's target
   framework/runtime and peer dependencies.
2. Verify it from the package registry, not from memory or old examples.
3. Do not select preview, alpha, beta, RC, dev, nightly, or other prerelease
   versions, or floating versions such as `*` or `latest`, unless the user
   explicitly requested them.

## 3. Due diligence before installing

Check that the selected package/version is not deprecated, review known
vulnerability information from the ecosystem, and verify the license of the
exact selected version from official registry metadata (and the upstream
license when necessary). Permissive licenses such as MIT, Apache-2.0, and
BSD-family licenses can be accepted for ordinary commercial use; being
downloadable without payment does not make a package acceptable.

## 4. License approval

Do not install automatically — explain the concern and the reasonable
alternatives, and wait for approval — when the dependency requires payment or a
commercial license, or its license has material obligations or cannot be
confidently classified (strong copyleft, dual licensing that may require a
commercial license, source-available/custom licenses, unclear or missing
license information). Never silently substitute an alternative; if no
reasonable free alternative exists, say so. Do not draw legal conclusions
beyond what the published license supports.

```text
Package: Example.Package
Version: <selected stable compatible version>
License: Commercial
Reason: <capability for which it was selected>

Options:
1. Install the requested commercial package.
2. Use free alternative A — <license and important trade-off>.
3. Use free alternative B — <license and important trade-off>.
```

## 5. Install

The dependency hook blocks package commands without an explicit version; pass
the verified version.

- NuGet (Central Package Management): add or update
  `<PackageVersion Include="Id" Version="x.y.z" />` in `Directory.Packages.props`
  and a versionless `<PackageReference Include="Id" />` in the narrowest project
  that needs it, or run
  `dotnet add <project> package <Id> --version <x.y.z>` and confirm the version
  landed in `Directory.Packages.props`.
- npm: `npm install <name>@<x.y.z>` (add `--save-dev` for build/test tooling)
  inside the frontend workspace; framework-specific add commands are in
  `frontend.commands`. Keep `package-lock.json` consistent and committed.
- Never use `npm --force` or `--legacy-peer-deps` to bypass incompatible peer
  dependencies; resolve the actual compatibility problem.

## 6. Verify

- `node .claude/scripts/check-packages.cjs` (central versions, no floating
  versions, deny list, packages not added by default).
- Vulnerabilities: `dotnet package list --vulnerable --include-transitive`; the
  frontend audit from `frontend.commands`. Scanner output requires context; do
  not upgrade or replace unrelated packages because a scanner reports a finding.
- Build and test the affected projects (`verify`).

## Removal

When `minimalism.md` calls for removing a package: delete the project
reference, then the central `PackageVersion` once no project uses it (or run
`npm uninstall <name>`), and verify.
