---
name: add-dependency
description: Use before adding, updating or replacing any NuGet or npm package or .NET tool (dotnet add package, dotnet package add, npm install <pkg>, frontend CLI add commands). Selects the latest stable compatible version and checks deprecation, vulnerabilities and license, with approval for commercial or unclear licenses.
---
Kind: WF | Scope: common | Capability: — | Loading: on invocation (routed from CLAUDE.md; dependency commands are held by a hook until it runs)

# Add Dependency

Whether a dependency is needed at all, and package-management conventions: `.claude/rules/common/dependencies.md`. Approved and conditional technologies: decision register. A new major library or framework, or replacing approved technology, is Reserved (`CLAUDE.md` → Decision control).

## 1. Confirm the need and the approved choice

- Confirm a concrete current requirement and that the package is the approved technology for the capability (decision register), not a silent alternative.
- Package choices for conditional capabilities:
  - API versioning: when Controller API versioning is explicitly adopted, use the Controller integration of Asp.Versioning (`Asp.Versioning.Mvc`, plus `Asp.Versioning.Mvc.ApiExplorer` for documentation). Do not add the package before the project actually adopts versioning.
  - Resilience: when resilience is required, prefer `Microsoft.Extensions.Http.Resilience` for `HttpClient` and `Microsoft.Extensions.Resilience` for general pipelines. A direct Polly dependency is an explicit, documented exception, not the default. Never add the deprecated `Microsoft.Extensions.Http.Polly` or `Polly.Extensions.Http`.
  - Mapping, containers and slot-specific conditional tools: decision register.

## 2. Select the version

For every NuGet or npm addition or update:

1. Determine the latest **stable** version compatible with the project's target framework or runtime and its peer dependencies; "latest" means latest stable compatible version, not latest of any release channel.
2. Verify the current version from the package registry rather than relying on a remembered version.
3. Do not select preview, alpha, beta, RC, dev, nightly or other prerelease versions, or floating versions such as `*`, unless explicitly requested.

## 3. Due diligence before installation

1. Check whether the selected package or version is deprecated.
2. Check known vulnerability information from the package ecosystem.
3. Verify the license of the exact selected version from the official registry metadata and, when necessary, the upstream license. Permissive licenses commonly suitable for commercial use (MIT, Apache-2.0, BSD-family) are normally acceptable; do not assume a package is acceptable merely because it can be downloaded without payment.

## 4. Approval gates

- Do not automatically install a package that requires payment or a commercial license, or one whose license has material obligations or cannot be confidently classified (strong copyleft, dual licensing that may require a commercial license, source-available or custom licenses, unclear or missing license information). Explain the concern, present reasonable alternatives, and do not silently substitute one. If no reasonable free alternative exists, say so. Do not draw legal conclusions beyond what the published license supports. Presentation:

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

- NuGet: add or update `<PackageVersion Include="..." Version="..." />` in `Directory.Packages.props` and the `<PackageReference Include="..." />` in the consuming project, following `.claude/rules/common/dependencies.md` → NuGet; `dotnet add <project> package <id>` writes both under Central Package Management.
- .NET tools: use a local tool manifest (`dotnet new tool-manifest`, `dotnet tool install <tool>`).
- npm: run the install from the frontend workspace with the correct category (`npm install <pkg>` or `npm install -D <pkg>`), and keep `package-lock.json` consistent. Never use `--force` or `--legacy-peer-deps` merely to bypass incompatible peer dependencies; resolve the actual compatibility problem.
- Slot-specific installers (for example the frontend CLI's add command): the selected module's workflow facet.

## 6. Verify

- `node .claude/scripts/check-manifests.mjs` (Central Package Management, prerelease and floating versions, deprecated and approval-watch packages) and, for project-reference changes, `node .claude/scripts/check-architecture.mjs`.
- `dotnet package list --vulnerable --include-transitive` and `npm audit`. Scanner output needs context; do not automatically upgrade or replace unrelated packages because a scanner reports a finding.
- Build and test the affected projects (`verify`).

## Report

State the package, the selected version and why it is the latest stable compatible one, the license, deprecation and vulnerability results, and any approval that is still pending.
