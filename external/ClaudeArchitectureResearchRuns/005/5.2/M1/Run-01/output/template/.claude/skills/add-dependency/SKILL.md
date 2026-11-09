---
name: add-dependency
description: >
  Run before adding, updating, or removing any NuGet or npm package (dotnet add
  package, Directory.Packages.props edits, npm install/update): version,
  deprecation, vulnerability, and license checks.
---

> **Workflow skill** · Owns: dependency change procedure — version selection, due diligence, license approval, conditional package choice, peer-dependency resolution, removal · Scope: common · Loading: on demand (routed from `CLAUDE.md` → Procedures; reminded by the dependency hook)

# Add Dependency

Governing rules: `dependencies.md` (need, Central Package Management, npm) — read
it now if no manifest has been opened yet — and `docs/technology-stack.md`
(approved and conditional technologies). Adding a
major library/framework or replacing an approved technology is Reserved.

## 1. Confirm the Need and the Choice

1. Confirm a concrete current requirement for the package.
2. Prefer the approved technology for the capability; a conditional technology is
   added only when its capability is actually needed.
3. Conditional package choices:
   - API versioning, once explicitly adopted for the Controller API: the Controller
     integration of `Asp.Versioning` (`Asp.Versioning.Mvc`, plus
     `Asp.Versioning.Mvc.ApiExplorer` for Swagger grouping); do not add it before
     the project adopts versioning.
   - Resilience, once required: by default use `Microsoft.Extensions.Http.Resilience` for
     `HttpClient` and `Microsoft.Extensions.Resilience` for general pipelines. Do
     not add `Microsoft.Extensions.Http.Polly` or `Polly.Extensions.Http`; a direct
     Polly reference is an explicit exception that requires a documented reason
     the Microsoft integration cannot meet.

## 2. Select the Version

For every NuGet or npm addition or update:

1. Determine the latest stable version compatible with the project's target
   framework/runtime and peer dependencies.
2. Verify the current version from the package registry rather than relying on
   a remembered version.
3. Do not select preview, alpha, beta, RC, dev, nightly, or other prerelease
   versions unless explicitly requested.
4. Do not use floating versions such as `*`.

"Latest" means the latest stable compatible version, not the latest version of
any release channel.

## 3. Due Diligence Before Installation

1. Check whether the selected package/version is deprecated.
2. Check known vulnerability information from the package ecosystem, for example:

   ```bash
   dotnet package list --vulnerable --include-transitive
   npm audit
   ```

   Scanner output requires context; do not automatically replace or upgrade
   unrelated packages because a scanner reports a finding.
3. Verify the license of the exact selected version from its official registry
   metadata and, when necessary, the upstream license. Permissive licenses
   commonly suitable for commercial use (MIT, Apache-2.0, BSD-family) may
   normally be accepted. Do not assume a package is acceptable merely because it
   can be downloaded without payment, and do not draw legal conclusions beyond
   the published license information.

## 4. Commercial, Restrictive, or Unclear Licenses

Do not install automatically a dependency that requires payment or a commercial
license, or whose license has material obligations or cannot be confidently
classified (strong copyleft, dual licensing that may require a commercial
license, source-available/custom licenses, missing license information). Explain
the concern and present explicit choices; never substitute an alternative
silently:

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

- Place the package as `dependencies.md` requires: NuGet → `PackageVersion` in
  `Directory.Packages.props` plus a `PackageReference` in the project that needs
  it; npm → the right dependency category with the lockfile updated.
- Do not use `npm --force` or `--legacy-peer-deps` merely to bypass incompatible
  peer dependencies; resolve the actual compatibility problem instead.
- Run `node .claude/scripts/check-dependencies.mjs` (the manifest hook also runs
  it after edits).

## 6. Removal

Remove dependencies that are no longer used when doing so is part of the current
change and safe to verify; do not leave dead package references. Do not perform
unrelated dependency cleanup during a narrowly scoped task.

## Output

Report the package, selected version and how it was verified, license,
deprecation and vulnerability results, and any approval still required.
