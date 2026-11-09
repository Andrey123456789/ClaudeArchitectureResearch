---
name: add-dependency
description: >
  Procedure for adding, updating, or removing any NuGet or npm package: need
  check, approved-stack check, latest stable compatible version from the
  registry, deprecation/vulnerability/license due diligence, commercial-license
  approval, central versions and lockfile. Use before any dotnet add package,
  npm install <pkg>, or manifest edit.
---

> Kind: WF | Scope: common | Capability: — | Loading: on-demand workflow

# Add, Update, or Remove a Dependency

Read first: `.claude/rules/common/dependencies.md` plus the ecosystem standard (`.claude/rules/backend/dependencies.md` for NuGet, `.claude/rules/frontend/dependencies.md` for npm). Approved and conditional technologies: the decision register.

## 1. Need and selection

- [ ] A concrete current requirement exists (common dependency standard).
- [ ] The choice matches the decision register's approved stack; anything else goes through `architecture-decision` first.
- Conditional packages are added only when their capability is actually adopted:
  - Default: API versioning uses the Controller integration of `Asp.Versioning` (`Asp.Versioning.Mvc`, plus `Asp.Versioning.Mvc.ApiExplorer` for documentation) — added only after the project has adopted API versioning, never before.
  - Default: when resilience is required, `Microsoft.Extensions.Http.Resilience` for `HttpClient` and `Microsoft.Extensions.Resilience` for general pipelines. Direct Polly usage is an explicit, documented exception; never add the deprecated `Microsoft.Extensions.Http.Polly` or `Polly.Extensions.Http`.
  - Mapping: `Mapster` with `Mapster.DependencyInjection` once mapping volume warrants it (never referenced from Domain); Testcontainers, Playwright, and similar conditional packages: per the decision register.

## 2. Version selection

For every NuGet or npm addition or update:

1. Determine the latest **stable** version compatible with the project's target framework/runtime and peer dependencies.
2. Verify it from the package registry rather than from memory.
3. Never select preview, alpha, beta, RC, dev, nightly, or other prerelease versions, or floating versions such as `*`, unless the user explicitly requested them.

**Explicit exception.** A floating or prerelease version is allowed only on an explicit, bounded user request that names the package and the version or range; a general wish such as "keep it current" is not one. Record it as one entry in the file dependency-version-exceptions.json at the repository root (created on first use) with `ecosystem` (`npm` or `nuget`), `package`, `version`, `manifest` (repository-relative path), `requested_by` (`user`), `request` (the request text), and `date`. The manifest checks accept exactly that entry and keep rejecting every other floating or prerelease version; there is no global switch. For a floating NuGet version, also set `CentralPackageFloatingVersionsEnabled` to true in `Directory.Packages.props`, because restore rejects the version otherwise (NU1011); that NuGet property does not widen the exception, and the manifest checks keep rejecting every other floating version. Confirm compatibility with the target framework and peer dependencies, and report the exact version the install resolved. The entry covers the version only, not any other dependency rule.

"Latest" means latest stable compatible version, not latest version of any release channel.

## 3. Due diligence before installation

- [ ] The selected package/version is not deprecated.
- [ ] Known vulnerability information from the ecosystem has been checked (`dotnet package list --vulnerable --include-transitive`, `npm audit`, registry advisories). Scanner output needs context; do not upgrade or replace unrelated packages because of a finding.
- [ ] The license of the exact selected version is verified from official registry metadata (and the upstream license when necessary). Permissive licenses such as MIT, Apache-2.0, and BSD-family licenses may normally be accepted; free download does not imply an acceptable license.

## 4. Paid, commercial, or risky licenses — approval required

Do not automatically install a dependency that requires payment or a commercial license, or whose license has material obligations or cannot be confidently classified (strong copyleft, dual licensing that may require a commercial license, source-available/custom licenses, unclear or missing license information). Explain the concern and present choices without silently substituting an alternative:

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

If no reasonable free alternative exists, say so. Do not draw legal conclusions beyond what the published license supports.

## 5. Install

- **NuGet:** add or update the `PackageVersion` in `Directory.Packages.props`; reference the package without a version only from the narrowest project that needs it (`dotnet add <project> package <id> --version <version>` writes the central version under Central Package Management).
  ```xml
  <!-- Directory.Packages.props -->
  <PackageVersion Include="FluentValidation" Version="<verified version>" />

  <!-- backend/ProjectName.Application/ProjectName.Application.csproj -->
  <PackageReference Include="FluentValidation" />
  ```

- **npm:** `npm install <name>@<version>` (`--save-dev` for build/test tooling); keep `package.json` and `package-lock.json` together and consistent; when an authorized commit is part of this task, include both files, and otherwise do not create a Git commit.
- **Peer-dependency conflicts:** resolve the actual compatibility problem; never use `npm --force` or `--legacy-peer-deps` merely to bypass incompatible peer dependencies. No confirmation, comment marker, or approval opens this route.

## 6. Removal

Remove dependencies that are no longer used when doing so is part of the current change and safe to verify; do not leave dead package references behind, and do not perform unrelated dependency cleanup during a narrowly scoped task.

The dependency-command hook blocks removal commands (`npm uninstall`, `dotnet remove … package`, and equivalents) so that removals pass this checklist: remove the entry from the manifest (the project `PackageReference`, plus the central `PackageVersion` when no project uses it any more; the `package.json` entry), then restore (`dotnet restore`, `npm install`) so the lockfile stays consistent.

## 7. Verify and report

Build and run the affected tests (`verify`). Report: package, version, license, due-diligence results, and any approval obtained or pending.

Enforcement: before execution, the dependency-command hook routes additions and updates without an exact version, bulk updates, removals, and `--force`/`--legacy-peer-deps` here (updates re-run the install command with the exact selected version); after edits and shell commands, the manifest hook runs `.claude/scripts/check-manifests.cjs` on the files that actually changed.
