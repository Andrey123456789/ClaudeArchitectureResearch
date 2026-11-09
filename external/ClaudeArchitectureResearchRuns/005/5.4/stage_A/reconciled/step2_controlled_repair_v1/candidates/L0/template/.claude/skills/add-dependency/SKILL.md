---
name: add-dependency
description: >
  Run before adding, updating, or removing any NuGet or npm package (dotnet add
  package, npm install <pkg>, ng add, manifest edits): stable version, license,
  vulnerability checks.
---

> Level: 3 Project · Owns: dependency change procedure — version selection, due diligence, license approval, conditional package bindings, peer-dependency handling (workflow) · Scope: common · Loads: on invocation (routed from CLAUDE.md and the project hook) · Depends on: CLAUDE.md, .claude/rules/0-core/dependency-hygiene.md, .claude/rules/3-project/package-management.md, .claude/rules/3-project/decisions.md

# Add Dependency

## 1. Justify the dependency

Read `.claude/rules/0-core/dependency-hygiene.md` and `.claude/rules/3-project/package-management.md` (they may not have loaded). Confirm that the change needs the package now, that the approved stack (`3-project/decisions.md`) does not already cover the need, and that it is not a Reserved addition (CLAUDE.md → Decision control). Approved conditional packages are added only when their trigger condition holds.

## 2. Select the version

For every NuGet or npm addition or update:

1. Determine the latest **stable** version compatible with the target framework/runtime and peer dependencies — verify it from the package registry rather than from memory or examples.
2. Do not select preview, alpha, beta, RC, dev, nightly, or other prerelease versions, and do not use floating versions such as `*`, unless the user explicitly requests it.

**Explicit exception.** A floating or prerelease version is allowed only on an explicit, bounded user request that names the package and the version or range; a general wish such as "keep it current" is not one. Record it as one entry in the file dependency-version-exceptions.json at the repository root (created on first use) with `ecosystem` (`npm` or `nuget`), `package`, `version`, `manifest` (repository-relative path), `requested_by` (`user`), `request` (the request text), and `date`. The manifest checks accept exactly that entry and keep rejecting every other floating or prerelease version; there is no global switch. Confirm compatibility with the target framework and peer dependencies, and report the exact version the install resolved. The entry covers the version only, not any other dependency rule.

## 3. Due diligence before installation

Check that the exact selected version is not deprecated, review known vulnerability information for it, and verify its license from official registry metadata (and the upstream license when necessary). Permissive licenses commonly suitable for commercial use — MIT, Apache-2.0, BSD-family — may normally be accepted; a free download does not by itself make a package acceptable.

## 4. Commercial and risky licenses

Do not install a paid/commercial dependency, or one whose license is materially restrictive or cannot be confidently classified (strong copyleft, dual licensing that may require a commercial license, source-available/custom, unclear or missing), automatically. Explain the concern and present the options without silently substituting:

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

If no reasonable free alternative exists, say so. Do not make legal conclusions beyond what the published license supports.

## 5. Conditional package bindings

- **API versioning:** when Controller API versioning is explicitly adopted, use the Controller integration of `Asp.Versioning` (`Asp.Versioning.Mvc`, plus `Asp.Versioning.Mvc.ApiExplorer` for documentation); do not add it before the project actually adopts versioning (default).
- **Resilience:** when resilience is required, prefer `Microsoft.Extensions.Http.Resilience` for `HttpClient` and `Microsoft.Extensions.Resilience` for general pipelines; a direct Polly reference or Polly API configuration is an explicit, documented exception rather than the default (default). Do not add the deprecated `Microsoft.Extensions.Http.Polly` or `Polly.Extensions.Http`.

## 6. Install

- NuGet: add the version to `Directory.Packages.props` and a versionless `PackageReference` to the narrowest project that needs it, e.g. `dotnet add backend/<Name>.Infrastructure package <Id>` (CPM writes the version centrally).
- npm: install from the workspace directory with the correct category (`npm install <pkg>` or `npm install -D <pkg>`), keeping `package-lock.json` consistent.
- Never use `npm --force` or `--legacy-peer-deps` merely to bypass incompatible peer dependencies; resolve the actual compatibility problem (the project hook blocks these flags). No confirmation, comment marker, or approval opens this route.

## 7. Verify and report

Build and test the affected scope (`verify`); for security-relevant changes run `dotnet package list --vulnerable --include-transitive` or `npm audit`. Scanner output needs context — do not replace or upgrade unrelated packages merely because a scanner reports something. Report: package · version · license · reason · checks performed.

## Removing a dependency

Remove the reference (and its central version when no project uses it any more), rebuild, and run the affected tests.
