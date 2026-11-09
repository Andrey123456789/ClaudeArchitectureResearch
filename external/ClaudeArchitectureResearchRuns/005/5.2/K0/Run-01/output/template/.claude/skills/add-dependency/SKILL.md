---
name: add-dependency
description: Use before adding, updating, replacing or removing any NuGet or npm package (dotnet add package, npm install, ng add, manifest edits), and when resolving peer-dependency conflicts. Version, license and due-diligence procedure.
---
<!-- Kind: WF | Scope: common | Owns: dependency selection, due diligence, license gate, installation and removal procedure, conditional package choices | Loads: workflow invocation; command-guard hook -->
# Add Dependency

Standards: `rules/common/dependencies.md` (need, Central Package Management, npm conventions). Approved and conditional technologies: decision register.

## 1. Confirm Need and Decision Class

- [ ] The package serves a concrete current requirement (`rules/common/dependencies.md` § Need).
- [ ] The register approves the technology, or the package is a minor local choice. A major library or framework, a replacement of an approved technology, or a new infrastructure category is Reserved — run `architecture-decision` first and do not install meanwhile.
- [ ] For a conditional technology, its register condition holds.

## 2. Select the Version

- **Must** determine the latest stable version compatible with the project's target framework/runtime and peer dependencies, verified from the package registry rather than from memory. "Latest" means the latest stable compatible version, not the latest version of any release channel.
- **Must not** select preview, alpha, beta, RC, dev, nightly or other prerelease versions, or floating versions such as `*`, unless explicitly requested.

## 3. Due Diligence

- Before installation, **must** check whether the selected package/version is deprecated, review the known vulnerability information available from its ecosystem, and verify the license of the exact selected version — official registry metadata first, the upstream license when necessary. Being downloadable without payment does not make a package acceptable.

## 4. License Gate

- Permissive open-source licenses commonly suitable for commercial use (MIT, Apache-2.0, BSD family) are acceptable without approval.
- Paid or commercial packages, and packages whose license has material obligations or cannot be classified confidently, **require approval**: do not install them automatically; explain the concern, present reasonable alternatives, and **never** substitute an alternative silently. If no reasonable free alternative exists, say so explicitly.

      Package: Example.Package
      Version: <selected stable compatible version>
      License: Commercial
      Reason: <capability for which it was selected>

      Options:
      1. Install the requested commercial package.
      2. Use free alternative A — <license and important trade-off>.
      3. Use free alternative B — <license and important trade-off>.

- Licenses needing review include strong copyleft, dual licensing that may require a commercial license, source-available/custom licenses, and unclear or missing license information. Do not draw legal conclusions beyond what the published license information supports.

## 5. Install

### NuGet

Add the version once in `Directory.Packages.props` and a versionless reference in the narrowest project that needs it (`rules/common/dependencies.md` § NuGet):

```xml
<!-- Directory.Packages.props -->
<ItemGroup>
  <PackageVersion Include="FluentValidation" Version="..." />
</ItemGroup>
```

```xml
<!-- Project.csproj -->
<ItemGroup>
  <PackageReference Include="FluentValidation" />
</ItemGroup>
```

### npm

Use the workspace's package manager, choose `dependencies` or `devDependencies` deliberately, and keep the lockfile consistent (`rules/common/dependencies.md` § npm).

- **Must not** use `--force` or `--legacy-peer-deps` merely to bypass incompatible peer dependencies; resolve the actual compatibility problem instead.

### Conditional Technology Packages

- **Default:** when resilience is required (DEC-RES-01), `Microsoft.Extensions.Http.Resilience` for `HttpClient` and `Microsoft.Extensions.Resilience` for general pipelines. Direct Polly usage is an explicit exception — only when a concrete requirement cannot be expressed through those APIs, with the reason documented. Do not add the deprecated `Microsoft.Extensions.Http.Polly` or `Polly.Extensions.Http` packages.
- **Default:** when Controller API versioning is explicitly adopted (DEC-VER-01), use the Controller integration of `Asp.Versioning` (`Asp.Versioning.Mvc`, plus `Asp.Versioning.Mvc.ApiExplorer` for OpenAPI grouping); do not add the package before the project actually adopts API versioning.
- Mapster, Testcontainers and Playwright: only when their register condition holds (DEC-MAP-01, DEC-TEST-01, DEC-WEB-03).

## 6. Remove

Remove dependencies that are no longer used when that is part of the current change and safe to verify; do not leave dead package references. Do not perform unrelated dependency cleanup during a narrowly scoped task.

## 7. Verify

- Run `node .claude/scripts/check-manifests.mjs` and build the affected projects.
- For security-relevant changes run `dotnet package list --vulnerable --include-transitive` (modern .NET SDKs) or `npm audit`. Scanner output needs context; do not replace or upgrade unrelated packages because a scanner reports a finding.
- The command-guard hook pauses package commands until this workflow has run: when steps 1–4 are complete, re-run the command with the trailing comment `# add-dependency: done`.

## Output

Package and version, license, deprecation and vulnerability result, projects or workspace changed, approvals obtained or Decision Requests pending.
