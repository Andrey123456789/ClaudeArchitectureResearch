---
name: add-dependency
description: >
  Use before adding, updating, or removing a NuGet or npm package (dotnet add
  package, npm install <pkg>, ng add, manifest version edits): version
  selection, due diligence, license gate, CPM and lockfile.
---

> Owns: dependency selection procedure, version selection, due diligence, license approval gate, package-choice defaults | Scope: common | Loads: workflow (routed from CLAUDE.md; reminded by the dependency hooks)

# Add Dependency

Read `.claude/rules/dependencies.md` first — it owns dependency need, Central
Package Management, and npm conventions, and it loads only when a manifest is
opened. Approved technologies: `docs/technology-stack.md`.

## 1. Confirm Need and Approval

- Is there a concrete current requirement? Does the approved stack already
  define a technology for this capability? If so, use it.
- A major library or framework, a new infrastructure capability, or the
  replacement of an approved technology is Reserved (CLAUDE.md § Decision
  Control): stop and run `architecture-decision`.
- Package choices:
  - Resilience: when resilience is required, prefer
    `Microsoft.Extensions.Http.Resilience` for `HttpClient` and
    `Microsoft.Extensions.Resilience` for general resilience pipelines. Direct
    Polly usage is an explicit exception rather than the default — use it only
    when a concrete requirement cannot be expressed through those packages, and
    document why. Do not add the deprecated `Microsoft.Extensions.Http.Polly` or
    `Polly.Extensions.Http`.
  - API versioning: when Controller API versioning has been explicitly adopted,
    use the Controller integration of `Asp.Versioning` (`Asp.Versioning.Mvc`,
    plus `Asp.Versioning.Mvc.ApiExplorer` for versioned OpenAPI); do not add the
    package before the project actually adopts versioning.

## 2. Select the Version

For every NuGet or npm addition or update:

1. Determine the latest stable version compatible with the project's target
   framework/runtime and peer dependencies.
2. Verify the current version from the package registry rather than relying on
   a remembered version or an example.
3. Do not select preview, alpha, beta, RC, dev, nightly, or other prerelease
   versions, and do not use floating versions such as `*`, unless explicitly
   requested.

**Explicit exception.** A floating or prerelease version is allowed only on an
explicit, bounded user request that names the package and the version or range;
a general wish such as "keep it current" is not one. Record it as one entry in
the file dependency-version-exceptions.json at the repository root (created on
first use) with `ecosystem` (`npm` or `nuget`), `package`, `version`, `manifest`
(repository-relative path), `requested_by` (`user`), `request` (the request
text), and `date`. The manifest checks accept exactly that entry and keep
rejecting every other floating or prerelease version; there is no global switch.
For a floating NuGet version, also set `CentralPackageFloatingVersionsEnabled` to
true in `Directory.Packages.props`, because restore rejects the version otherwise
(NU1011); that NuGet property does not widen the exception, and the manifest
checks keep rejecting every other floating version.
Confirm compatibility with the target framework and peer dependencies, and
report the exact version the install resolved. The entry covers the version
only, not any other dependency rule.

"Latest" means the latest stable compatible version, not the latest version of
any release channel.

## 3. Due Diligence

Before installation:

1. Check whether the selected package/version is deprecated.
2. Check the known vulnerability information available from the relevant
   package ecosystem.
3. Verify the license of the exact selected version from the official registry
   metadata and, when necessary, the upstream license. Permissive licenses such
   as MIT, Apache-2.0, or the BSD family are generally suitable for normal
   commercial use; a package is not acceptable merely because it can be
   downloaded without payment.

## 4. License Approval Gate

Do not install automatically — explain the concern, present reasonable
alternatives, and wait for approval — when the dependency:

- requires payment or a commercial license; or
- has a license with material obligations or one that cannot be confidently
  classified (strong copyleft, dual licensing that may require a commercial
  license, source-available or custom licenses, unclear or missing license
  information).

Never silently replace the requested package with an alternative. If no
reasonable free alternative exists, say so explicitly. Do not draw legal
conclusions beyond what the published license information supports.

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

## 5. Apply

### NuGet

1. Add or update the `PackageVersion` in `Directory.Packages.props`.
2. Add a versionless `PackageReference` to the narrowest project that needs the
   package. `dotnet add <project> package <id> --version <version>` is
   Central-Package-Management aware; review both files afterwards.

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

### npm

1. In the Angular workspace run `npm install <package>@<version>`, adding
   `--save-dev` for build and test tooling.
2. Update `package.json` and `package-lock.json` together. When an authorized
   commit is part of this task, include both files; otherwise do not create a Git
   commit.
3. Do not use `--force` or `--legacy-peer-deps` merely to bypass incompatible
   peer dependencies; resolve the actual compatibility problem instead. The
   dependency hook blocks these flags. No confirmation, comment marker, or
   approval opens this route.

## 6. Verify

1. From the repository root (the current checkout or worktree top level,
   `git rev-parse --show-toplevel`), run
   `node .claude/scripts/check-manifests.mjs` (Central Package Management,
   version form, deprecated packages, project references).
2. Restore and build the affected projects.
3. Inspect vulnerability information for the changed dependency set:

```bash
dotnet package list --vulnerable --include-transitive
npm audit
```

Scanner output requires context. Do not automatically replace or upgrade
unrelated packages because a scanner reports a finding.

## Removal

Remove dependencies that are no longer used when doing so is part of the current
change and safe to verify; do not leave dead package references behind. Do not
perform unrelated dependency cleanup during a narrowly scoped task.

## Report

Report the package, selected version, license, checks performed, and approval
status (approved / awaiting approval / not needed).
