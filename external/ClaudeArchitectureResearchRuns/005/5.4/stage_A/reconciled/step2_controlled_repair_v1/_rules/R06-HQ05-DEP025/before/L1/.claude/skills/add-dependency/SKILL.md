---
name: add-dependency
description: Use before adding, updating, or removing any NuGet or npm package (dotnet add package, npm install, ng add, version bumps). Covers stable version selection, deprecation, vulnerability and license checks, commercial-license approval, conditional packages, and peer-dependency conflicts.
---

> Level: 3-project · Owns: dependency procedure — version selection, due diligence, license approval, conditional package choices, peer-conflict handling · Loading: on invocation (also routed by the dependency-command hook)

# Add Dependency

Necessity (`.claude/rules/0-core/engineering.md`), approved technologies (decisions file), and package-management conventions (`.claude/rules/3-project/package-management.md`) govern what may be added. This workflow governs how.

## 1. Confirm the need and the approved choice

State the concrete current requirement. Use the approved technology when one exists; replacing an approved technology or adding a major library is Reserved. Conditional technologies (decisions file) are added only when their capability is needed; package choices:

- mapping: `Mapster` + `Mapster.DependencyInjection`;
- `Microsoft.Extensions.Http.Resilience` (outbound `HttpClient`) or `Microsoft.Extensions.Resilience` (other pipelines) — Default: these are the resilience packages when resilience is required; direct Polly usage is an explicit, documented exception, and the deprecated `Microsoft.Extensions.Http.Polly` / `Polly.Extensions.Http` integrations are never added;
- `Asp.Versioning` Controller integration (`Asp.Versioning.Mvc`, `Asp.Versioning.Mvc.ApiExplorer`) — Default: only once Controller API versioning has actually been adopted;
- slot-specific conditional packages (real-provider test containers, E2E tooling) — see the module command facets.

## 2. Select the version

For every NuGet or npm addition or update:

1. Determine the latest **stable** version compatible with the project's target framework/runtime and peer dependencies, verified from the package registry — never from memory.
2. Do not select preview, alpha, beta, RC, dev, nightly, or other prerelease versions, and never floating versions such as `*`, unless explicitly requested.

**Explicit exception.** A floating or prerelease version is allowed only on an explicit, bounded user request that names the package and the version or range; a general wish such as "keep it current" is not one. Record it as one entry in the file dependency-version-exceptions.json at the repository root (created on first use) with `ecosystem` (`npm` or `nuget`), `package`, `version`, `manifest` (repository-relative path), `requested_by` (`user`), `request` (the request text), and `date`. The manifest checks accept exactly that entry and keep rejecting every other floating or prerelease version; there is no global switch. Confirm compatibility with the target framework and peer dependencies, and report the exact version the install resolved. The entry covers the version only, not any other dependency rule.

## 3. Due diligence before installing

- Check whether the exact package/version is deprecated.
- Check known vulnerability information from the ecosystem (`dotnet package list --vulnerable --include-transitive`, the frontend audit command in `frontend.commands`).
- Verify the license of the exact selected version from official registry metadata and, when necessary, the upstream license. Permissive licenses commonly suitable for commercial use (MIT, Apache-2.0, BSD family) are acceptable without approval; being free to download does not make a package acceptable.

## 4. Approval for commercial or risky licenses

Do not install automatically when the package requires payment or a commercial license, or when its license has material obligations or cannot be confidently classified (strong copyleft, dual licensing that may require a commercial license, source-available/custom terms, unclear or missing license). Present the concern and reasonable alternatives, never substitute silently, and make no legal conclusions beyond the published license information:

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

If no reasonable free alternative exists, say so explicitly.

## 5. Install

- NuGet and npm placement: as the package-management rule requires (the manifest hook checks it), for example:

  ```xml
  <!-- Directory.Packages.props -->
  <PackageVersion Include="FluentValidation" Version="<selected version>" />

  <!-- <Project>.csproj -->
  <PackageReference Include="FluentValidation" />
  ```

- npm: never use `--force` or `--legacy-peer-deps` merely to bypass incompatible peer dependencies — resolve the actual compatibility problem.
- After a scanner finding, do not automatically replace or upgrade unrelated packages.

## 6. Removal

Remove dependencies that are no longer used when that is part of the current change and safe to verify; do not leave dead references, and do not perform unrelated dependency cleanup during a narrow task.

## Report

Package, version, license, vulnerability/deprecation result, target project, and approvals obtained or still pending. Then continue the calling workflow (`verify` covers the build).
