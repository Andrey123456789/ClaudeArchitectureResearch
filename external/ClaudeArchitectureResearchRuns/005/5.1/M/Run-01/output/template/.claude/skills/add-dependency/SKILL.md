---
name: add-dependency
description: >
  Use before adding, updating, replacing, or removing any NuGet or npm package
  (dotnet add package, npm install <pkg>, ng add, version bumps). Selects the
  latest stable compatible version and checks deprecation, vulnerabilities, and
  license before installing.
---

> Owns: dependency addition/update procedure, version selection, deprecation/vulnerability/license due diligence, commercial-license approval | Scope: common | Loads: workflow (CLAUDE.md routing; dependency commands are routed here by the Bash guard hook)

# Add or Update a Dependency

## 1. Read the Governing Policy

Read `.claude/rules/dependencies.md` (necessity, Central Package Management,
npm rules) — it may not be loaded yet. `docs/technology-stack.md` is already in
context.

## 2. Confirm the Need and the Technology

- [ ] A concrete current requirement exists (`dependencies.md`).
- [ ] The package is the approved technology for the capability, or a
      conditional technology whose trigger is now met
      (`docs/technology-stack.md`).
- [ ] If it adds a major library/framework, replaces an approved technology, or
      introduces an infrastructure category, it is Reserved — stop and run
      `architecture-decision` first.

## 3. Select the Version

For every NuGet or npm addition or update:

1. Determine the latest **stable** version compatible with the project's target
   framework/runtime and peer dependencies, verified against the package
   registry rather than remembered (`dotnet package search <id> --exact-match`,
   `npm view <pkg> versions dist-tags peerDependencies`).
2. Do not select preview, alpha, beta, RC, dev, nightly, or other prerelease
   versions, and never use floating versions such as `*`, unless the user
   explicitly requests it.

"Latest" means latest stable compatible version, not latest of any channel.

## 4. Due Diligence Before Installation

Check, for the exact selected version:

- deprecation status (registry metadata);
- known vulnerabilities, from the ecosystem's advisory data for that version
  (registry vulnerability metadata / GitHub Advisory Database); after
  installation confirm with `dotnet package list --vulnerable
  --include-transitive` or `npm audit`;
- license, from official registry metadata and, when needed, the upstream
  license for that version.

Permissive licenses commonly suitable for commercial use (MIT, Apache-2.0,
BSD-family) may normally be accepted. Do not assume a package is acceptable
merely because it is free to download, and do not draw legal conclusions beyond
what the published license supports.

## 5. Commercial, Restrictive, or Unclear Licenses

Do not install automatically when the dependency requires payment or a
commercial license, or its license is strong copyleft, dual-licensed in a way
that may require a commercial license, source-available/custom, or unclear or
missing. Explain the concern and present choices, then wait for approval:

```text
Package: Example.Package
Version: <selected stable compatible version>
License: <license and concern>
Reason: <capability for which it was selected>

Options:
1. Install the requested package.
2. Use free alternative A — <license and important trade-off>.
3. Use free alternative B — <license and important trade-off>.
```

Never silently substitute an alternative. If no reasonable free alternative
exists, say so.

## 6. Install

Mark the install command with the trailing comment `# add-dependency` so the
Bash guard hook recognizes that this workflow was followed:

```bash
dotnet add backend/MyApp.Infrastructure/MyApp.Infrastructure.csproj package <Id> --version <x.y.z>  # add-dependency
npm install <pkg>@<x.y.z> --save-dev  # add-dependency
```

- NuGet: with Central Package Management enabled, `dotnet add package` writes
  the version to `Directory.Packages.props`; target the project that actually
  needs the package (`dependencies.md`, NuGet).
- npm: run inside the Angular workspace with `--save-dev` for tooling; category,
  lockfile, and peer-conflict handling follow `dependencies.md` (npm).

## 7. Check and Report

1. Run `node .claude/scripts/check-manifests.mjs`.
2. Restore and build the affected projects; run relevant tests.
3. For removals, confirm nothing still uses the package.

Report: package, selected version and why, license, deprecation and
vulnerability results, target project/workspace, and verification results.
Updates of unrelated packages are out of scope unless requested.
