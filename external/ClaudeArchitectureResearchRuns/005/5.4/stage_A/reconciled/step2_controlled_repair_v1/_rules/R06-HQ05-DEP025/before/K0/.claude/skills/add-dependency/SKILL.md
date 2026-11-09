---
name: add-dependency
description: Use before adding, updating or removing a NuGet or npm package (dotnet add package, npm install <pkg>, ng add, version bumps) — version, deprecation, vulnerability and license checks, install, verify.
---

> Kind: WF | Scope: common | Owner: dependency addition, update and removal procedure — version selection, due diligence, license approval, package-specific choices | Loading: workflow (model- or user-invoked; routed by the pre-command hook)

# Add Dependency

Manifest rules (need, Central Package Management, npm lockfile and categories): `rules/common/dependencies.md`. Approved and conditional technologies: decision register.

## 1. Confirm need and technology

1. Confirm a concrete current requirement (`rules/common/dependencies.md` § Need).
2. Use the approved technology from the decision register; a conditional technology only when its capability is now needed. A new major library or framework, or a replacement of an approved technology, is Reserved — stop with a Decision Request (CLAUDE.md § Decisions).
3. Apply the package-specific choices below.

### Package-specific choices

- **Resilience** — when resilience is required, prefer `Microsoft.Extensions.Http.Resilience` for HttpClient and `Microsoft.Extensions.Resilience` for general pipelines (D-12). Do not add the deprecated `Microsoft.Extensions.Http.Polly` or `Polly.Extensions.Http`; a direct Polly reference or Polly API configuration is an explicit exception that needs a documented reason why the Microsoft.Extensions APIs cannot express the requirement.
- **API versioning** — when Controller API versioning has been explicitly adopted (D-15), use the Controller integration of `Asp.Versioning` (for example `Asp.Versioning.Mvc` with `Asp.Versioning.Mvc.ApiExplorer`); do not add it before the project actually adopts versioning.
- **Validation** — `FluentValidation.DependencyInjectionExtensions` for registration; do not add a deprecated or legacy ASP.NET automatic-validation integration package without a concrete requirement (D-05).

## 2. Select the version

For every NuGet or npm addition or update:

1. Determine the latest **stable** version compatible with the project's target framework/runtime and peer dependencies.
2. Verify the current version from the package registry instead of relying on a remembered version; do not copy versions from examples or older content.
3. Do not select preview, alpha, beta, RC, dev, nightly or other prerelease versions, or floating versions such as `*`, unless explicitly requested.

**Explicit exception.** A floating or prerelease version is allowed only on an explicit, bounded user request that names the package and the version or range; a general wish such as "keep it current" is not one. Record it as one entry in the file dependency-version-exceptions.json at the repository root (created on first use) with `ecosystem` (`npm` or `nuget`), `package`, `version`, `manifest` (repository-relative path), `requested_by` (`user`), `request` (the request text), and `date`. The manifest checks accept exactly that entry and keep rejecting every other floating or prerelease version; there is no global switch. Confirm compatibility with the target framework and peer dependencies, and report the exact version the install resolved. The entry covers the version only, not any other dependency rule.

"Latest" means the latest stable compatible version, not the latest version of any release channel.

## 3. Due diligence before installation

Check, for the exact selected version:

1. deprecation status;
2. known vulnerabilities from the ecosystem's advisory data;
3. the license — from official registry metadata and, when necessary, the upstream license text.

Permissive licenses such as MIT, Apache-2.0 and the BSD family are generally suitable for commercial use. A package being free to download does not make it acceptable.

## 4. License approval

- **Paid or commercial license** — do not install automatically. Present explicit choices, offer reasonable free alternatives when they exist (say so when none exists), and never substitute an alternative silently:

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

- **License needing review** — strong copyleft, dual licensing that may require a commercial license, source-available/custom licenses, unclear or missing license information: do not adopt automatically; explain the concern and present alternatives when practical. Do not draw legal conclusions beyond what the published license supports.

## 5. Install

- **NuGet** — add the version to `Directory.Packages.props` and a versionless `PackageReference` to the narrowest project that needs it:

```xml
<!-- Directory.Packages.props -->
<PackageVersion Include="FluentValidation" Version="x.y.z" />

<!-- Project.csproj -->
<PackageReference Include="FluentValidation" />
```

- **npm** — install into the Angular workspace with the right category (`--save-dev` for build and test tooling) and keep `package-lock.json` consistent. Never use `--force` or `--legacy-peer-deps` merely to bypass incompatible peer dependencies; resolve the actual compatibility problem.
- The pre-command hook stops package-changing commands — additions, updates and removals, with or without global options such as `--prefix`, and any `--force` or `--legacy-peer-deps` install — until this workflow has run. After steps 1–4, run the command with the trailing marker comment `# add-dependency: reviewed`, for example:

```bash
dotnet add backend/MyApp.Api/MyApp.Api.csproj package Swashbuckle.AspNetCore # add-dependency: reviewed
npm install --save-dev @playwright/test # add-dependency: reviewed
```

## 6. Verify

1. Restore and build the affected projects.
2. Inspect vulnerability information: `dotnet package list --vulnerable --include-transitive`; `npm audit` for the frontend. Scanner output needs context; do not upgrade or replace unrelated packages because of a finding.
3. Run `node "$(git rev-parse --show-toplevel)/.claude/scripts/check-dependencies.cjs"` (works from any directory of the repository or worktree, in Bash and PowerShell).

## Removing a dependency

Remove a dependency that is no longer used when that is part of the current change and safe to verify; do not leave dead references behind, and do not perform unrelated dependency cleanup during a narrowly scoped task.

## Output

Package, selected version and why, license, deprecation and vulnerability status, approval obtained (if needed), files changed, verification result.
