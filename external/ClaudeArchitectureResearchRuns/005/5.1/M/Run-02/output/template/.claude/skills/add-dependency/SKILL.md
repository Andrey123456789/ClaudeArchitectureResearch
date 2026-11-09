---
name: add-dependency
description: >
  Use before any NuGet or npm change: dotnet add/remove package, dotnet
  package add, npm install <pkg>, npm uninstall, ng add/update, a version
  bump, or a manual package edit in a .csproj, Directory.Packages.props, or
  package.json.
---

> Owner: dependency change procedure — version selection, due diligence, license approval, npm peer-conflict handling, removal | Scope: common | Loads: on demand — workflow (routed by `CLAUDE.md` § Development Workflow and the PreToolUse hook) | Enforced: PreToolUse hook (routes dependency commands here, blocks npm peer-bypass flags), `.claude/scripts/check-dependencies.mjs`

# Add Dependency

## Read First

- `.claude/rules/dependencies.md` — necessity, Central Package Management, npm
  lockfile and dependency categories.
- `docs/technology-stack.md` (already loaded) — approved, conditional, and
  not-by-default technologies.

## 1. Justify

- Name the concrete current requirement the package serves; without one, stop.
- Is it the approved technology for this capability? A package outside the
  stack, a replacement for an approved technology, or a new major library or
  framework is Reserved → Decision Request (`architecture-decision` workflow).
- A conditional technology is added only when its capability is needed now.

## 2. Select the Version

For every NuGet or npm addition or update:

1. determine the latest **stable** version compatible with the project's target
   framework/runtime and peer dependencies;
2. verify it from the package registry, not from memory or an example;
3. never select preview, alpha, beta, RC, dev, nightly, or other prerelease
   versions, or floating versions such as `*`, unless explicitly requested.

"Latest" means latest stable compatible version, not the latest version of any
release channel.

```bash
dotnet package search <PackageId> --exact-match   # NuGet versions
npm view <package> versions dist-tags peerDependencies engines
```

## 3. Due Diligence (Before Installation)

Check the selected version for:

- deprecation (NuGet deprecation metadata, `npm view <package> deprecated`);
- known vulnerabilities from the ecosystem's advisory data;
- the license of the exact selected version — registry metadata and, when
  necessary, the upstream license file.

Permissive licenses commonly suitable for commercial use (MIT, Apache-2.0,
BSD-family) may be accepted. Being free to download does not make a package
acceptable.

## 4. License Approval

Do not install automatically when the package needs payment or a commercial
license, or when its license is materially restrictive or cannot be confidently
classified — strong copyleft, dual licensing that may require a commercial
license, source-available or custom terms, missing or unclear information.
Explain the concern, offer reasonable alternatives, and never substitute one
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

Say explicitly when no reasonable free alternative exists, and draw no legal
conclusions beyond what the published license information supports.

## 5. Apply

### NuGet

```xml
<!-- Directory.Packages.props -->
<ItemGroup>
  <PackageVersion Include="FluentValidation" Version="x.y.z" />
</ItemGroup>
```

```xml
<!-- backend/ProjectName.Application/ProjectName.Application.csproj -->
<ItemGroup>
  <PackageReference Include="FluentValidation" />
</ItemGroup>
```

`dotnet add <project> package <id> --version <x.y.z>` respects Central Package
Management when it is enabled; confirm afterwards that the version landed in
`Directory.Packages.props` and the project reference is versionless. Add the
reference only to the narrowest project that needs it.

### npm

```bash
npm install <package>@<version>              # runtime dependency
npm install --save-dev <package>@<version>   # build/test tooling
ng add <package>                             # packages that ship Angular schematics
```

Keep `package-lock.json` consistent and commit it with `package.json`.

### npm Peer Conflicts

Do not use `--force` or `--legacy-peer-deps` merely to bypass incompatible peer
dependencies; resolve the actual compatibility problem (choose a compatible
version, align the peer packages, or report the incompatibility). Do not delete
`package-lock.json` as a troubleshooting reflex. The PreToolUse hook blocks these
flags; if the user explicitly wants one for another reason, ask them to run the
command themselves.

## 6. Removal

Remove dependencies that the current change made unused when doing so is safe to
verify; do not leave dead package references behind, and do not perform
unrelated dependency cleanup during a narrowly scoped task.

## 7. Verify

```bash
node .claude/scripts/check-dependencies.mjs
dotnet restore
dotnet package list --vulnerable --include-transitive
npm audit
```

Then build the affected projects. Scanner output needs context: do not upgrade or
replace unrelated packages merely because a scanner reports a finding.

## Output

```text
Package | Version | License | Deprecated | Known vulnerabilities | Reason | Approval needed
```

Plus any open Decision Request.
