---
name: build-fix
description: >
  Use when a .NET or Angular build or test run fails, after a breaking upgrade,
  or when asked to make the repository green: bounded reproduce-diagnose-fix
  loop and repair report.
---

> Level: 3 Project · Owns: repair procedure, iteration limits and repair report · Scope: common · Loads: on demand (model- or user-invoked)

# Build Fix

Restore the affected scope to green without hiding failures, weakening behavior or introducing unrelated changes.

    code-review -> inspect completed changes for defects
    verify      -> prove a completed change is ready
    build-fix   -> repair a build/test failure that already exists

## Read first

- `.claude/rules/0-core/completion-contract.md` (Repair) — diagnosis first, bounded iteration, never weakening verification, generated output.
- `.claude/rules/0-core/testing-principles.md` — when tests or probes are created during diagnosis.

## 1. Determine the affected scope

Classify the failure: .NET backend, Angular frontend, backend + frontend, API contract or client generation, package/dependency change, repository or toolchain configuration. Do not run unrelated build systems merely because they exist (backend-only compile failure → start with the affected .NET project; Angular template error → the workspace; changed API contract consumed by Angular → both sides).

## 2. Reproduce

Use the narrowest command that reliably reproduces the failure.

```bash
dotnet build backend/<Name>.Api/<Name>.Api.csproj
dotnet test backend/<Name>.Application.Tests/<Name>.Application.Tests.csproj
dotnet build <Name>.slnx                      # broader scope when required
```

For Angular, inspect `package.json` first and use scripts that exist (`npm run build`, `npm test`). Do not invent script names or assume a test runner: Vitest is the baseline for new workspaces, but an existing workspace may deliberately use another.

## 3. Capture the actual error

Read the complete relevant output, not just the first line, and group errors by likely root cause.

- .NET: missing project/package reference, namespace/type resolution, changed API signature, nullability, generic/type mismatch, interface contract change, package API change, source generation, MSBuild configuration, target framework or SDK mismatch.
- Angular: TypeScript type error, template compilation, DI/provider error, invalid standalone import, route configuration, signal/RxJS typing, missing package, Angular/TypeScript peer-version mismatch, generated client mismatch, build configuration.

One root cause can produce many secondary errors — fix the highest-leverage cause first.

## 4. Repair loop

Backend:

1. Reproduce the narrowest failure.
2. Identify the probable root cause; inspect source, project references and package configuration.
3. Make the smallest correct change.
4. Rerun the same build or test and compare the new failure set with the previous one.
5. Expand verification only after the focused failure is resolved.

Frontend: inspect `package.json` and Angular configuration, reproduce, read the TypeScript/Angular diagnostic in context, inspect the affected component, service, route, template or configuration, make the smallest correct change, rerun, then broaden.

Invalid shortcuts — a green build obtained this way is not a repair:

    Application -> Infrastructure project reference         (backend-layers.md)
    persistence-framework types leaking into Application   (persistence-boundary.md)
    business logic moved into a controller                  (entry-points.md)
    server authorization replaced by Angular guards        (security-principles.md)
    HTTP calls scattered into components                   (frontend-structure.md)
    `any`, disabled strict mode, suppressed template diagnostics, NgModules added to dodge standalone configuration
    another state-management or HTTP library added to bypass a local issue

## 5. Full-stack and contract failures

Determine which contract is authoritative; never patch both sides into inconsistent shapes just to compile. With OpenAPI client generation: verify the backend contract, regenerate the client through the project's normal workflow, review the generated changes, then fix handwritten frontend code against the result (`swagger`, `http-api` skills).

## 6. Test failures

1. Read the failing test and the relevant production behavior.
2. Decide where the defect is: production code, test setup, test expectation, environment/configuration, or an intentionally changed contract.
3. Make the smallest correct change and rerun the affected test, then the broader relevant tests.

If expected behavior intentionally changed, update the test to express the new contract and confirm the change was actually requested. Backend test technique: `dotnet-testing`; frontend: `angular`.

## 7. Dependency and package failures

Inspect the exact requested and installed versions, framework/runtime compatibility and peer dependencies; read the diagnostics and the official migration notes when needed; update usage deliberately. Any added, replaced or upgraded package goes through `add-dependency`. Resolve version conflicts in `Directory.Packages.props` (`conventions.md`). Do not delete `package-lock.json` reflexively as a troubleshooting step.

## 8. Framework upgrades and toolchain problems

Distinguish compile errors from changed runtime behavior; verify replacement APIs instead of fabricating them from memory; do not perform an additional unrelated upgrade. Check the toolchain (`dotnet --info`, `node --version`, `npm --version`, `global.json`, target framework, Angular versions, CI runtime settings). Do not change the repository's declared SDK, Node, framework or language version because the local machine differs — report an unavailable toolchain instead of editing source to compensate.

## 9. Generated code

Identify the generator and its input first (OpenAPI clients, source generators, EF Core migrations, Angular build output), fix the source or configuration, and regenerate.

## Iteration limits

Several focused attempts — not an unlimited loop. Stop and reassess when the same root failure survives materially different fixes, fixes cause growing unrelated failures, the toolchain is incompatible, required infrastructure is unavailable, package compatibility cannot be resolved safely, or the correct behavior cannot be determined from the project or request. Never repeat variants of the same failed guess.

If a fix introduces new failures, decide whether they reveal a legitimate dependency of the change; otherwise revert or correct that fix. Never leave the repository knowingly worse than the starting state. Leave unrelated pre-existing failures alone unless they block verification of the repair or the user asks.

## Completion and report

Complete when the affected scope is green (backend build, frontend build, affected tests, consistent cross-stack contract, no known new regression, no workaround in the diff). Do not require an unrelated frontend build for a backend-only repair, or vice versa. Then run `verify` when appropriate.

```text
Initial failure:   <failure>
Root cause:        <cause>
Changes made:      <changes>
Backend build:     PASS / NOT RUN / NOT APPLICABLE
Frontend build:    PASS / NOT RUN / NOT APPLICABLE
Tests:             PASS / NOT RUN / NOT APPLICABLE
Remaining issues:  none / <details>
```
