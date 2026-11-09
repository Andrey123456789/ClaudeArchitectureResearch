---
name: add-dependency
description: >
  Use before any NuGet or npm package add, update, or removal (dotnet add
  package, npm install <pkg>, framework CLI add commands): need check, stable
  version, deprecation, vulnerability and license checks, manifest update.
---

> Workflow · Owns dependency due diligence, version selection, license approval, package-choice procedure, and peer-dependency handling · Manifest policy: `.claude/rules/dependencies.md`

# Add Dependency

## 1. Confirm the Need

- The dependency must solve a concrete current requirement
  (`.claude/rules/dependencies.md` § General Principle).
- Use the approved technology when one exists (`docs/technology-stack.md`,
  `docs/capabilities/`). A major library or framework, or a replacement for an
  approved technology, is Reserved (`CLAUDE.md` § Decision Control).

## 2. Choose the Package

Prefer the approved package for the capability. Package-choice notes:

- **API versioning** — add a versioning package only after the project has
  explicitly adopted Controller API versioning; then use the Controller
  integration of `Asp.Versioning` (`Asp.Versioning.Mvc`, plus
  `Asp.Versioning.Mvc.ApiExplorer` for documentation grouping).
- **Resilience** — when resilience is required, prefer
  `Microsoft.Extensions.Http.Resilience` for `HttpClient` and
  `Microsoft.Extensions.Resilience` for general pipelines. Never add the
  deprecated `Microsoft.Extensions.Http.Polly` or `Polly.Extensions.Http`
  integrations. Direct Polly usage is an explicit exception: use it only when a
  concrete requirement cannot be expressed through the Microsoft resilience
  APIs, and document why.
- **Validation** — do not add deprecated or legacy ASP.NET automatic-validation
  integration packages merely to connect FluentValidation to the pipeline.

## 3. Select the Version

For every NuGet or npm addition or update:

1. determine the latest stable version compatible with the project's target
   framework/runtime and peer dependencies;
2. verify the current version from the package registry rather than relying on
   a remembered version;
3. do not select preview, alpha, beta, RC, dev, nightly, or other prerelease
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

"Latest" means latest stable compatible version, not latest version of any
release channel.

## 4. Due Diligence Before Installation

Before installing, check:

- whether the selected package/version is deprecated;
- known vulnerability information available from the package ecosystem;
- the license of the exact selected version, from official registry metadata
  and, when necessary, the upstream license.

Do not assume a package is acceptable merely because it can be downloaded
without payment.

## 5. License Decisions

Permissive open-source licenses commonly suitable for commercial use — MIT,
Apache-2.0, BSD-family — may be accepted.

Do not install automatically a dependency that requires payment or a
commercial license, or whose license has material obligations or cannot be
confidently classified (strong copyleft, dual licensing that may require a
commercial license, source-available/custom licenses, unclear or missing
license information). Explain the concern and present reasonable alternatives;
do not silently substitute another package, and say so explicitly when no
reasonable free alternative exists.

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

Do not make legal conclusions beyond what the published license information
supports.

## 6. Install

- **NuGet** — add or update the `PackageVersion` in `Directory.Packages.props`
  and a versionless `PackageReference` in the narrowest project that needs it
  (`.claude/rules/dependencies.md` § NuGet).
- **npm** — install into the correct dependency category and keep
  `package-lock.json` consistent (`.claude/rules/dependencies.md` § npm). Do not
  use `--force` or `--legacy-peer-deps` merely to bypass incompatible peer
  dependencies; resolve the actual compatibility problem instead.

The pre-tool hook stops package commands until this workflow has been applied.
After completing steps 1–5, re-run the same command with the trailing comment
`# add-dependency: checked`. That comment never applies to `--force` or
`--legacy-peer-deps`: the hook denies them. No confirmation, comment marker, or
approval opens this route.

## 7. Verify

Run `node "$(git rev-parse --show-toplevel)/.claude/scripts/check-manifests.js"`
(from any directory of the active repository or worktree), then the
ecosystem's vulnerability information when the change is security-relevant or
when verifying the dependency:

```bash
dotnet package list --vulnerable --include-transitive
npm audit
```

Scanner output requires context. Do not automatically replace or upgrade
unrelated packages merely because a scanner reports a finding.

## Removal

Remove dependencies that are no longer used when doing so is part of the
current change and safe to verify; do not leave dead package references, and
do not perform unrelated dependency cleanup during a narrowly scoped task.
