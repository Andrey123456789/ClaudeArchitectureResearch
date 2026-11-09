---
name: build-fix
description: Use when a .NET or Angular build fails, tests break, an upgrade introduces errors, or the user asks to make the repository green. Bounded reproduce-diagnose-fix loop.
---

> Kind: WF | Scope: common | Owner: build and test repair procedure | Loading: workflow (model- or user-invoked)

# Build Fix

Goal: restore the affected scope to a green build/test state without hiding failures, weakening behavior or introducing unrelated changes. Use `code-review` to inspect completed changes, `verify` to prove completion, and `build-fix` when a build or test failure already exists and must be repaired.

## Principles

- Reproduce and diagnose the actual failure before editing; do not guess at fixes. Fix root causes before downstream symptoms.
- Work in small, bounded iterations: re-run the narrowest failing verification after each meaningful fix, and expand verification only after the focused failure is resolved.
- Never weaken, delete, skip or suppress relevant tests, compiler, TypeScript, lint or analyzer failures merely to make verification pass.
- Preserve architecture and project conventions while fixing; stop when progress has clearly stalled instead of making speculative edits.

## 1. Determine the affected scope

Decide whether the failure concerns the .NET backend, the Angular frontend, both, an API contract or client generation, package/dependency changes, or repository/toolchain configuration. Do not run unrelated build systems merely because they exist.

```text
backend-only compile failure      -> start with the affected .NET project
Angular template/TypeScript error -> start with the Angular workspace
changed API contract used by UI   -> inspect and verify both sides
documentation-only failure        -> no application builds without a reason
```

## 2. Reproduce

Start with the narrowest command that reliably reproduces the problem, using the repository's actual `.slnx`, project paths and configuration.

```bash
dotnet build backend/MyApp.Api/MyApp.Api.csproj
dotnet build
dotnet test backend/MyApp.Application.Tests/MyApp.Application.Tests.csproj
```

For Angular, inspect the workspace `package.json` first and use scripts that actually exist (for example `npm run build`, `npm test`). Do not invent script names or assume a test runner; the stack decision (D-09) names the default runner for new workspaces, but an existing project may deliberately use another.

## 3. Capture the actual error

Read the complete relevant output, not only the first line, and group errors by likely root cause. One root cause often produces many secondary failures; fix the highest-leverage cause first.

```text
.NET: missing project/package reference, namespace/type resolution, changed API
signature, nullability, generic/type mismatch, interface contract change, package
version/API change, source generation, MSBuild configuration, target framework or
SDK mismatch

Angular: TypeScript type error, template compilation, DI/provider error, invalid
standalone import, route configuration, signal/RxJS typing, missing package,
Angular/TypeScript peer mismatch, generated API client mismatch, build configuration
```

## 4. Repair loop

### Backend

1. Reproduce the narrowest failure.
2. Identify the probable root cause.
3. Inspect the relevant source, project references and package configuration.
4. Make the smallest correct change.
5. Re-run the same build or test.
6. Compare the new failure set with the previous one.
7. Expand verification only after the focused failure is resolved.

Never solve a dependency problem with an invalid project reference (for example Application → Infrastructure); follow `rules/backend/architecture.md`.

### Frontend

1. Inspect `package.json` and the relevant Angular configuration.
2. Reproduce the failing build or test command.
3. Read the TypeScript/Angular diagnostic in context.
4. Inspect the affected component, service, route, template or configuration.
5. Make the smallest correct change.
6. Re-run the same command.
7. Expand to broader frontend verification after the focused failure is fixed.

Follow `rules/frontend/angular.md`. Do not convert code to `any` to silence TypeScript, disable strict mode, suppress template diagnostics without understanding them, add NgModules to work around a standalone configuration problem, replace framework APIs speculatively, or add another state-management or HTTP library to bypass a local issue.

### Full-stack and contract failures

Typical triggers: a changed response contract, endpoint path or HTTP method, nullability, enum or value semantics or authentication contract, or a generated client that no longer matches the OpenAPI document. Determine which contract is authoritative; do not patch both sides into inconsistent shapes merely to make both compile. With OpenAPI client generation: verify the backend contract, regenerate the client with the project's normal workflow, review the generated changes, then fix handwritten frontend code against the result. Technique: `swagger`, `http-api`.

### Test failures

1. Read the failing test.
2. Read the relevant production behavior.
3. Decide whether the defect is in production code, test setup, test expectation, environment/configuration, or an intentionally changed contract.
4. Make the smallest correct change.
5. Re-run the affected test or test project.
6. Run broader relevant tests after the focused failure is fixed.

Do not weaken a strong assertion or delete/skip a failing test because fixing it is inconvenient. If expected behavior intentionally changed, update the test to express the new contract and confirm the change was actually requested. Test technique: `dotnet-testing`, `angular`.

### Dependency and package failures

1. Inspect the exact installed or requested version.
2. Confirm framework/runtime compatibility.
3. Inspect peer dependencies where applicable.
4. Read the actual compiler/build diagnostics.
5. Check official migration or release documentation when necessary.
6. Update usage deliberately.

Any package addition, replacement or version change goes through `add-dependency` (including its npm peer-conflict handling); respect Central Package Management (`rules/common/dependencies.md`) and do not delete `package-lock.json` reflexively.

### Framework or API upgrades

Inspect the installed version, distinguish compilation errors from changed runtime behavior, check official migration documentation, update obsolete API usage deliberately, and preserve architecture and behavior where the upgrade does not require change. Do not fabricate replacement APIs from memory when they can be verified, and do not perform an additional unrelated upgrade.

### Toolchain problems

Check whether the failure comes from source or toolchain (`dotnet --info`, `dotnet --version`, `node --version`, `npm --version`; `global.json`, target framework, Angular package versions, `package-lock.json`, CI runtime configuration). Do not change the repository's declared SDK, Node, framework or language version merely because the local machine differs; report an unavailable toolchain instead of editing source to compensate.

### Generated code

When generated output is wrong, or its source contract or configuration changed, fix or update the authoritative source — OpenAPI document, source generator input, EF Core model, build configuration — and regenerate. Do not manually patch disposable generated output unless the repository or its generation workflow intentionally treats that output as maintained source.

## 5. Iteration limits

Use bounded iteration — several focused attempts, not an unlimited edit/build loop. Stop and reassess when the same root failure survives materially different fixes, fixes create growing unrelated failures, the toolchain is incompatible, required external infrastructure is unavailable, package compatibility cannot be resolved safely, or the correct behavior cannot be determined. Do not repeat variants of the same failed guess.

If a fix introduces new failures, decide whether they reveal a legitimate dependency of the change; otherwise revert or correct that fix before continuing. Never leave the repository knowingly worse than where the repair started. Do not clean up unrelated pre-existing failures unless they block verification of the requested repair or the user asks.

A green build obtained by violating architecture is not a successful repair (for example Application → Infrastructure references, `DbContext` in Application, business logic moved into a Controller, Angular-only authorization, HTTP calls scattered into components).

## 6. Complete

The repair is complete when the affected scope is green: the relevant builds pass, affected tests pass, cross-stack contracts are consistent, no known new regression remains and the diff contains no accidental workaround. Behavioral probes created during diagnosis follow `verify` § 4. Then run `verify` for the final completion pass when appropriate.

## Report

```text
Initial failure: <failure>
Root cause: <cause>
Changes made: <changes>
Backend build: PASS / NOT RUN / NOT APPLICABLE
Frontend build: PASS / NOT RUN / NOT APPLICABLE
Tests: PASS / NOT RUN / NOT APPLICABLE
Remaining issues: None / <details>
```

Do not claim the problem is fixed while a known relevant failure remains.
