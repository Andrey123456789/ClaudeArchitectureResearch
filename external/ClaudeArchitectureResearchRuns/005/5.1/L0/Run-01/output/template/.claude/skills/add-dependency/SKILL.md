---
name: add-dependency
description: >
  Use before adding, updating or removing any NuGet or npm package (`dotnet add
  package`, `npm install <pkg>`, `ng add`, manifest edits): need check, stable
  version, due diligence, license approval, install.
---

> Level: 3 Project · Owns: dependency-change procedure and approval presentation · Scope: common · Loads: on demand (model- or user-invoked; routed by the pre-command hook)

# Add Dependency

## Read first

- `.claude/rules/0-core/dependency-hygiene.md` — need, version, due-diligence and license obligations.
- `.claude/rules/3-project/conventions.md` — Central Package Management and npm conventions.
- Project decisions (always loaded) — approved, conditional and not-by-default technologies.

## 1. Confirm need and decision class

- Name the concrete current requirement the package serves.
- Approved baseline technology for a capability the project now needs → proceed.
- Conditional technology (Mapster, resilience, Testcontainers, Playwright, Asp.Versioning, Docker) → proceed only when its condition holds.
- A major library or framework not in the project decisions, a replacement of an approved technology, a package on the not-by-default list, or a mediator library → Reserved: stop and raise a Decision Request (`architecture-decision`).
- Before adding anything, check whether built-in platform or framework capabilities already cover the need.

## 2. Select the version

Find the latest **stable** version compatible with the target framework/runtime and peer dependencies — from the registry, not from memory:

```bash
dotnet package search <PackageId> --exact-match          # versions on nuget.org
npm view <package> version                               # latest stable dist-tag
npm view <package> versions --json
npm view <package>@<version> peerDependencies engines
```

"Latest" means latest **stable** compatible (dependency hygiene) — skip `-preview`, `-alpha`, `-beta`, `-rc` and nightly entries in the listings. For Angular packages, let the Angular CLI choose mutually compatible versions (`ng add`, `ng update`); do not push TypeScript beyond Angular's supported range.

## 3. Due diligence on the exact version

- **Deprecation** — nuget.org deprecation notice; `npm view <package>@<version> deprecated`.
- **Vulnerabilities** — advisory data for that version; after installation, `dotnet package list --vulnerable --include-transitive` and `npm audit`.
- **License** — registry metadata (`npm view <package>@<version> license`; the nuget.org license field/expression) and the upstream license when the metadata is unclear.

Permissive licenses such as MIT, Apache-2.0 and BSD-family are usually suitable. A package that downloads for free is not automatically acceptable.

## 4. Licenses that need approval

For paid/commercial, strong-copyleft, possibly-commercial dual licensing, source-available/custom, or unclear/missing licenses, stop and present:

```text
Package: <PackageId>
Version: <selected stable compatible version>
License: <license>
Reason:  <capability for which it was selected>
Concern: <what the license obligation or uncertainty is>

Options:
1. Install the requested package.
2. Use free alternative A — <license and important trade-off>.
3. Use free alternative B — <license and important trade-off>.
```

If no reasonable free alternative exists, say so. Then wait for the user's decision.

## 5. Install

The pre-command hook blocks dependency commands that lack the workflow marker. After steps 1–4, run the install command with the trailing comment `# add-dependency`.

NuGet (Central Package Management):

```bash
dotnet add backend/<Project>/<Project>.csproj package <PackageId> --version <version>   # add-dependency
```

Or edit manually: add `<PackageVersion Include="<PackageId>" Version="<version>" />` to `Directory.Packages.props` and a versionless `<PackageReference Include="<PackageId>" />` to the narrowest project that needs it (`conventions.md`).

npm (run inside `frontend/<Name>.Web`):

```bash
npm install <package>@<version>              # add-dependency
npm install --save-dev <package>@<version>   # add-dependency — build/test tooling
ng add <angular-package>                     # add-dependency — schematics that configure the workspace
```

`package.json` and `package-lock.json` change together (`conventions.md`); peer-dependency conflicts: `angular.md`.

## 6. Removal and updates

- Remove packages that the current change stops using, when removal is part of the change and safe to verify; leave unrelated dependency cleanup out of narrowly scoped tasks.
- Updates follow steps 2–5 for the new version. Do not upgrade unrelated packages merely because a scanner reports a finding — assess it in context first.

## 7. Verify

Restore and build the affected projects, run relevant tests, rerun the vulnerability check, and confirm the post-edit manifest check reports nothing.

## Report

```text
Package:        <id>@<version> (<project or workspace>, <dependencies|devDependencies>)
Need:           <capability>
Decision class: Decided / conditional met / Reserved (approved by ...)
Deprecated:     no
Vulnerabilities: none known / <details>
License:        <license>
Verification:   restore/build/tests PASS / NOT RUN
```
