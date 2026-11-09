---
name: add-dependency
description: >
  Use before adding, updating, or removing a NuGet or npm package (dotnet add
  package, npm install <pkg>, ng add, PackageVersion or package.json edits):
  version, license, and manifest checks.
---

> Workflow skill. Owns: the dependency procedure — stable version selection, deprecation/vulnerability/license due diligence, the license approval gate, conditional package choices, peer-dependency handling, removal · Scope: common, backend, frontend · Loads: on invocation; routed by CLAUDE.md and by the dependency-command hook · Depends on: CLAUDE.md, docs/technology-stack.md, .claude/rules/dependencies.md · Enforced by: .claude/hooks/pre-tool.mjs, .claude/hooks/post-tool.mjs, .claude/scripts/check-manifests.mjs

# Add Dependency

## 1. Confirm the Need

- [ ] The dependency solves a concrete current requirement (`dependencies.md`,
  Need).

## 2. Check the Approved Stack

- An approved technology in `docs/technology-stack.md` is used instead of an
  alternative. Selecting an alternative, replacing a baseline technology, or
  adding a major library, framework, or infrastructure category is Reserved:
  run `architecture-decision` first.
- A conditional technology is added only when its capability is needed now.

Package choices for conditional capabilities:

- **Resilience** — default: `Microsoft.Extensions.Http.Resilience` for
  `HttpClient` and `Microsoft.Extensions.Resilience` for general, non-HTTP
  pipelines. Do not add the deprecated `Microsoft.Extensions.Http.Polly` or
  `Polly.Extensions.Http`. Direct Polly usage is an explicit exception: use it
  only when a concrete requirement cannot be expressed through the Microsoft
  packages, and document why.
- **API versioning** — default: once Controller API versioning has been
  adopted, use the Controller (MVC) integration of `Asp.Versioning`. Do not add
  the package before the project actually adopts versioning.

## 3. Select the Version

For every NuGet or npm addition or update:

1. Determine the latest stable version compatible with the project's target
   framework/runtime and peer dependencies, verified from the package registry
   — not from memory, examples, or historical template content.
2. Do not select prerelease versions (preview, alpha, beta, RC, dev, nightly)
   or floating versions such as `*` unless explicitly requested.

"Latest" means latest stable compatible version, not the latest version of any
release channel.

## 4. Due Diligence

Before installing, check:

- whether the selected package/version is deprecated;
- known vulnerabilities from the ecosystem's advisory information;
- the license of the exact selected version, from the official registry
  metadata and, when necessary, the upstream license.

Permissive licenses commonly suitable for commercial use (MIT, Apache-2.0,
BSD-family) may be accepted. A package that can be downloaded without payment
is not automatically acceptable.

## 5. License Gate

Do not install automatically a dependency that requires payment or a
commercial license, or whose license is materially restrictive or cannot be
classified confidently — strong copyleft, dual licensing that may require a
commercial license, source-available or custom licenses, unclear or missing
license information; installing it requires approval. Stop, explain the
concern, and present choices without silently substituting:

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

Offer reasonable free alternatives when they exist, or say explicitly that none
exists. Do not draw legal conclusions beyond what the published license
information supports.

## 6. Install

- **NuGet:** add or update the `PackageVersion` in `Directory.Packages.props`
  and a versionless `PackageReference` in the narrowest project that needs it
  (`dependencies.md`, NuGet).
- **npm:** install from the Angular workspace with npm into the correct
  dependency category and keep `package-lock.json` consistent
  (`dependencies.md`, npm).
- **Peer-dependency conflicts:** do not use `--force` or `--legacy-peer-deps`
  to bypass incompatible peer dependencies; resolve the actual compatibility
  problem — choose compatible versions, upgrade the peer deliberately, or report
  the conflict. The pre-tool hook blocks these flags.

## 7. Check

- Run `node .claude/scripts/check-manifests.mjs` (the post-tool hook also runs
  it after manifest edits and dependency commands).
- For security-relevant dependency changes, inspect vulnerability data, for
  example `dotnet package list --vulnerable --include-transitive` or
  `npm audit`. Scanner output requires context; do not replace or upgrade
  unrelated packages merely because a scanner reports a finding.

## Removing a Dependency

Remove dependencies that are no longer used when that is part of the current
change and safe to verify; do not leave dead package references behind, and do
not perform unrelated dependency cleanup during a narrowly scoped task.

## Output

Report the package, selected version and how it was verified, license,
deprecation and vulnerability results, the projects or workspace that reference
it, and the manifest-check result.
