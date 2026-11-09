---
name: build-fix
description: >
  Bounded, evidence-driven repair of failing .NET or frontend builds and tests:
  reproduce, diagnose root cause, smallest fix, rerun narrowest check, expand.
  Use when compilation or tests fail, a package/framework upgrade breaks the
  build, or the user asks to make the repository green.
---

> Kind: WF | Scope: common | Capability: — | Loading: on-demand workflow

# Build Fix

## Goal

Restore the affected scope to a green build/test state without hiding failures, weakening behavior, or introducing unrelated changes. `build-fix` repairs an existing failure; `code-review` inspects completed changes; `verify` proves a completed change is ready.

## Principles

- Reproduce and diagnose the actual failure before editing; never guess at a fix first.
- Fix root causes before downstream symptoms; one root cause can produce many secondary errors, so fix the highest-leverage cause first.
- Work in small bounded iterations: rerun the narrowest failing verification after each meaningful fix and expand verification only after the focused failure is resolved.
- Must not weaken, delete, skip, or suppress relevant tests, compiler, TypeScript, lint, or analyzer failures merely to make verification pass; understand a diagnostic before changing how it is reported.
- Preserve architecture and project conventions while fixing; a green build obtained by violating them is not a successful repair.
- Stop when progress has clearly stalled instead of making speculative edits.

## Determine the affected scope

Classify the failure: .NET backend, frontend, backend + frontend, API contract/client generation, package/dependency change, or repository/toolchain configuration. Do not run unrelated build systems merely because they exist (backend-only failure → the affected .NET project; frontend template/TypeScript failure → the frontend workspace; changed API contract consumed by the frontend → both sides; documentation-only → no application builds without a reason).

## Reproduce and capture

Start with the narrowest command that reproduces the problem, e.g. `dotnet build backend/MyApp.Api/MyApp.Api.csproj` or `dotnet test backend/MyApp.Application.Tests/MyApp.Application.Tests.csproj`, broadening to `dotnet build` only when required; use the repository's actual `.slnx`, project paths, and configuration. For the frontend, inspect `package.json` and use scripts that actually exist — never invent script names or assume a test runner.

Read the complete relevant output, not only the first line, and group errors by likely root cause. Typical .NET categories: missing project/package reference, namespace/type resolution, changed API signature, nullability, generic/type mismatch, interface contract change, package version/API change, source generation, MSBuild configuration, target framework or SDK mismatch. Typical frontend categories: TypeScript type errors, template compilation, dependency-injection/provider errors, route configuration, reactive typing issues, missing packages, framework/TypeScript peer-version mismatch, generated API client mismatch, build configuration. Framework-specific failure patterns: the frontend knowledge facet named in the decision register.

## Repair loops

Backend and frontend loops follow the same shape:

1. Reproduce the narrowest failure (frontend: inspect `package.json` and the relevant workspace configuration first).
2. Identify the probable root cause.
3. Inspect the relevant source, configuration, project references, or package configuration.
4. Make the smallest correct change.
5. Rerun the same failing build/test and compare the new failure set with the previous one.
6. Expand verification only after the focused failure is resolved.

Never solve an architectural dependency problem with an invalid project reference (e.g. Application → Infrastructure to make a type compile). Invalid shortcuts also include leaking persistence-technology types into Application, moving business logic into controllers, replacing server authorization with frontend-only guards, and scattering HTTP calls into components to bypass a data-access service. Read `.claude/rules/backend/architecture-style.md` for backend repairs and `.claude/rules/frontend/` for frontend repairs. Frontend shortcuts to refuse: converting code to `any` to silence the compiler, disabling strict mode, suppressing template diagnostics without understanding them, replacing framework APIs speculatively, adding another state-management or HTTP library to bypass a local issue.

## Full-stack and contract failures

Determine which contract is authoritative (response shape, generated client vs. OpenAPI, enum/value semantics, endpoint path or method, nullability, authentication contract). Never patch both sides independently into inconsistent shapes merely to compile. With OpenAPI client generation: verify the backend contract, regenerate the client through the project's normal workflow, review the generated changes, then fix handwritten frontend code. Technique: `swagger`, `http-api`.

## Test failures

When the build succeeds but tests fail: read the failing test and the relevant production behavior; decide whether the defect lies in production code, test setup, the test expectation, environment/configuration, or an intentionally changed contract; make the smallest correct change; rerun the affected test, then broader relevant tests. Never turn a strong assertion into a weak one, and never delete or skip a failing test because fixing it is inconvenient. If expected behavior intentionally changed, update the test to express the new contract and confirm the change was actually requested.

## Dependency and package failures

After adding or upgrading a package: inspect the exact installed/requested version, confirm framework/runtime compatibility, inspect peer dependencies, read the actual diagnostics, consult official migration notes when necessary, and update usage deliberately. Every dependency addition or version change runs `add-dependency` (including its peer-dependency rules); never replace a package or add another merely to get a green build. Respect Central Package Management (never duplicate conflicting versions in `.csproj` files) and the lockfile (never delete `package-lock.json` reflexively).

## Framework/API upgrades and toolchain

For upgrade fallout, inspect the installed version, separate compile errors from changed runtime behavior, update obsolete APIs deliberately from verified documentation (never fabricate replacement APIs from memory), and do not perform an additional unrelated upgrade. For toolchain problems check `dotnet --info`, `dotnet --version`, `node --version`, `npm --version`, `global.json`, target frameworks, frontend package versions, `package-lock.json`, and CI runtime versions. Never change the repository's declared SDK, Node, framework, or language version merely because the local machine differs; if the required toolchain is unavailable, report the limitation instead of editing source code to compensate.

## Generated outputs

Default: when generated output is wrong or its source contract/configuration changed, identify the generator and its input, fix or update the authoritative source, and regenerate (OpenAPI clients, source generators, persistence migrations, frontend build output). Do not manually patch disposable generated output unless the repository or its generation workflow intentionally treats that output as maintained source.

## Iteration limits and regressions

Use bounded iteration — several focused attempts, not an unlimited edit/build loop. Stop and reassess when the same root failure survives materially different fixes, fixes create increasing unrelated failures, the toolchain is incompatible, required external infrastructure is unavailable, package compatibility cannot be resolved safely, or correct behavior cannot be determined. Never repeat variants of the same failed guess. If a fix introduces new failures, determine whether they reveal a legitimate dependency of the change; otherwise revert or correct the fix. Never leave the repository knowingly worse than where the repair started, and do not clean up unrelated pre-existing failures unless they block verification or the user asks.

## Tests created during diagnosis

A behavioral test or probe used to establish correct behavior follows `verify` step 4: preserve uniquely verified behavior in maintained tests before removing temporary diagnostics.

## Completion and report

The repair is complete when the affected scope is green: relevant builds pass, affected tests pass, cross-stack contracts are consistent, no known new regression remains, and the final diff contains no accidental workaround. Do not require an unrelated frontend build for a backend-only repair or vice versa. Then run `verify` for the final completion pass when appropriate.

```text
Initial failure: <failure>
Root cause: <cause>
Changes made: <changes>
Backend build: PASS / NOT RUN / NOT APPLICABLE
Frontend build: PASS / NOT RUN / NOT APPLICABLE
Tests: PASS / NOT RUN / NOT APPLICABLE
Remaining issues: None / <details>
```

Never claim the problem is fixed while a known relevant failure remains.
