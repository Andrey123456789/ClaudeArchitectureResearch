---
name: add-dependency
description: >
  Use before adding or updating any NuGet or npm package: need, approved tech, stable version, vulnerabilities, license approval, install.
---

> Level: 3 Project | Owns: dependency selection and installation procedure, version and due-diligence checks, license approval gate, conditional package bindings, peer-conflict handling | Scope: common | Loads: workflow skill (model-invoked; routed from CLAUDE.md and the dependency-guard hook) | Depends on: CLAUDE.md, 0-core/dependency-hygiene.md, 2-technology/package-management.md, 3-project/decisions.md

# Add Dependency

## 1. Justify the Package

1. Confirm a concrete current requirement (`0-core/dependency-hygiene.md`).
2. Use the approved technology for the capability (`3-project/decisions.md`).
   A package that adds a major library, framework, or infrastructure capability,
   or replaces an approved one, is Reserved: run `architecture-decision` first.
3. Conditional bindings:
   - API versioning, once approved: use the Controller integration of
     `Asp.Versioning` (`Asp.Versioning.Mvc`, plus `Asp.Versioning.Mvc.ApiExplorer`
     for OpenAPI); do not add it before the project actually adopts versioning.
   - Resilience, when an integration needs it: prefer
     `Microsoft.Extensions.Http.Resilience` for `HttpClient` and
     `Microsoft.Extensions.Resilience` for general pipelines. Direct Polly usage
     is an explicit, documented exception; do not add the deprecated
     `Microsoft.Extensions.Http.Polly` or `Polly.Extensions.Http`.

## 2. Select the Version

For every NuGet or npm addition or update, verify the current latest **stable
compatible** version from the registry — compatible with the target framework,
runtime, and peer dependencies — rather than a remembered version. Avoid
prerelease (preview, alpha, beta, RC, dev, nightly) and floating versions (`*`,
ranges used to float) unless explicitly requested.

## 3. Due Diligence

Before installing, check:

- deprecation status of the package and selected version;
- known vulnerabilities (registry advisories; `dotnet package list --vulnerable
  --include-transitive`, `npm audit`);
- the license of the exact selected version, from official registry metadata
  and, when necessary, the upstream license.

Permissive licenses commonly suitable for commercial use (MIT, Apache-2.0,
BSD-family) may normally be accepted. Do not assume a package is acceptable
merely because it downloads without payment, and do not draw legal conclusions
beyond the published license information.

## 4. License Approval Gate

Do not install automatically when the package is paid or commercial, or when
its license is materially restrictive or unclear (strong copyleft, dual
licensing that may require a commercial license, source-available or custom
licenses, missing license data). Explain the concern and present choices
without silently substituting an alternative:

```text
Package: Example.Package
Version: <selected stable compatible version>
License: Commercial
Reason: <capability it was selected for>

Options:
1. Install the requested package.
2. Use free alternative A — <license and important trade-off>.
3. Use free alternative B — <license and important trade-off>.
```

If no reasonable free alternative exists, say so explicitly.

## 5. Install

- NuGet: add the version to `Directory.Packages.props` and a versionless
  `PackageReference` to the narrowest project that needs it
  (`2-technology/package-management.md`).
- npm: install into the correct category (`dependencies` vs.
  `devDependencies`) and keep `package-lock.json` consistent.
- Do not use `npm --force` or `--legacy-peer-deps` merely to bypass
  incompatible peer dependencies; resolve the actual compatibility problem.
- After completing steps 1–4, append the marker comment
  `# add-dependency:checked` to the install command (it is a comment in Bash
  and PowerShell); the dependency-guard hook blocks unmarked dependency
  commands.

## 6. Verify and Report

Build and test the affected projects, then report: package, version, license,
reason, vulnerability status, and any approval obtained. Scanner findings need
context — do not upgrade or replace unrelated packages merely because a scanner
reports something.
