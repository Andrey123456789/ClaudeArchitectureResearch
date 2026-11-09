---
name: build-fix
description: Use when a .NET or Angular build fails, tests break after a change, a package or framework upgrade introduces errors, or the user asks to make the repository green. Bounded, evidence-driven repair loop.
---
<!-- Kind: WF | Scope: common | Owns: build/test repair procedure, iteration limits, generated-output repair, repair reporting | Loads: workflow invocation -->
# Build Fix

## Goal

Restore the affected repository scope to a green build/test state without hiding failures, weakening behavior or introducing unrelated changes.

    code-review -> inspect completed changes for defects
    verify      -> prove a completed change is ready
    build-fix   -> repair a build/test failure that already exists

## Principles

- **Must** reproduce and diagnose the actual failure before editing, and fix root causes before downstream symptoms.
- **Must** iterate in small, bounded steps: rerun the narrowest failing verification after each meaningful fix and expand verification only after the focused failure is resolved.
- **Must not** weaken, delete, skip or suppress relevant tests or compiler, TypeScript, lint or analyzer failures merely to make verification pass.
- **Default:** fix generated output at its source — when generated output is wrong or its source contract or configuration changed, fix or update the authoritative source and regenerate; do not hand-patch disposable generated output unless the repository or generation workflow intentionally treats it as maintained source.
- Preserve architecture and project conventions while fixing; stop when progress has clearly stalled instead of making speculative edits.

## Determine the Affected Scope

Before running commands, determine whether the failure concerns the .NET backend, the Angular frontend, both, an API contract/client generation, package or dependency changes, or repository/toolchain configuration. Do not run unrelated build systems merely because they exist.

    backend-only compile failure       -> start with the affected .NET project
    Angular template/TypeScript failure -> start with the Angular workspace
    API contract consumed by Angular    -> inspect and verify both sides
    documentation-only failure          -> no application builds without a reason

## Reproduce the Failure

Start with the narrowest command that reliably reproduces the problem.

### .NET

    dotnet build backend/MyApp.Api/MyApp.Api.csproj
    dotnet build                     # when broader scope is required
    dotnet test backend/MyApp.Application.Tests/MyApp.Application.Tests.csproj

Use the repository's actual `.slnx`, project paths and configuration.

### Angular

Inspect the workspace `package.json` first and use scripts that actually exist (typically `npm run build`, `npm test`). Do not invent script names or assume a test runner merely because Angular is in use; Vitest is the baseline for newly scaffolded workspaces, but an existing project may deliberately configure another runner.

## Capture the Actual Error

Read the complete relevant output, not only the first visible line, and group related errors by likely root cause. One root cause may produce many secondary failures — fix the highest-leverage cause first.

    .NET:    missing project/package reference, namespace/type resolution, changed API signature,
             nullability, generic/type mismatch, interface contract change, package version/API
             change, source generation, project/MSBuild configuration, target framework/SDK mismatch
    Angular: TypeScript type error, template compilation, DI/provider error, invalid standalone
             import, route configuration, signal/RxJS typing, missing package/module,
             Angular/TypeScript peer mismatch, generated API client mismatch, build configuration

## Backend Build-Fix Loop

1. Reproduce the narrowest failure.
2. Identify the probable root cause.
3. Inspect the relevant source, project references and package configuration.
4. Make the smallest correct change.
5. Re-run the same failing build/test.
6. Compare the new failure set with the previous one.
7. Expand verification only after the focused failure is resolved.

Do not resolve a dependency problem with a project reference that violates `rules/backend/architecture.md` § Dependency Direction (for example an Application → Infrastructure reference added to make a missing type compile).

## Frontend Build-Fix Loop

1. Inspect `package.json` and the relevant Angular configuration.
2. Reproduce the failing build/test command.
3. Read the TypeScript/Angular diagnostic in context.
4. Inspect the affected component, service, route, template or configuration.
5. Make the smallest correct change.
6. Re-run the same command.
7. Expand to broader frontend verification after the focused failure is fixed.

Invalid shortcuts: converting code to `any` to silence TypeScript, disabling strict mode, suppressing template diagnostics without understanding them, adding NgModules to work around a standalone configuration problem, speculatively replacing framework APIs, or adding another state-management or HTTP library to bypass a local issue (`rules/frontend/angular.md`).

## Full-Stack and Contract Failures

Failures crossing the backend/frontend boundary (changed response contract, generated client out of date, changed enum/value semantics, endpoint path or method, nullability, authentication contract): determine which contract is authoritative, and do not patch both sides into inconsistent shapes merely to make both compile. With OpenAPI client generation:

1. verify the backend contract;
2. regenerate the client through the project's normal workflow;
3. review the generated changes;
4. fix handwritten frontend code against the resulting contract.

## Test-Fix Flow

When the build succeeds but tests fail:

1. Read the failing test.
2. Read the relevant production behavior.
3. Decide whether the defect is in production code, test setup, test expectation, environment/configuration, or an intentionally changed contract.
4. Make the smallest correct change.
5. Re-run the affected test or test project.
6. Run broader relevant tests after the focused failure is fixed.

If expected behavior intentionally changed, update the test to express the new contract and confirm the behavioral change was actually requested. Test standards: `rules/backend-tests/testing.md`; frontend tests: `angular` skill.

## Dependency and Package Failures

When a failure follows adding or upgrading a NuGet or npm package:

1. Inspect the exact installed or requested version.
2. Confirm framework/runtime compatibility.
3. Inspect peer dependencies where applicable.
4. Read the actual compiler/build diagnostics.
5. Check official migration or release documentation when necessary.
6. Update usage deliberately.

Any package addition, replacement or version change goes through `add-dependency` — do not add or swap packages merely to make the build green. Respect Central Package Management (`rules/common/dependencies.md`): do not work around conflicts by duplicating versions in `.csproj` files. Preserve the npm lockfile and dependency model; peer conflicts follow `add-dependency` § 5, and do not delete `package-lock.json` reflexively as a troubleshooting step.

## Framework/API Upgrades

When failures follow a .NET, Angular, TypeScript, EF Core or other framework upgrade: inspect the actual installed version; distinguish compilation errors from changed runtime behavior; check official migration documentation when needed; update obsolete API usage deliberately; preserve architecture and behavior where the upgrade does not require change. Do not fabricate replacement APIs from memory when they can be verified, and do not perform an unrelated additional upgrade while repairing the current one.

## Toolchain Problems

Determine whether the failure comes from source code or the local toolchain (`dotnet --info`, `dotnet --version`, `node --version`, `npm --version`; `global.json`, target framework, Angular package versions, `package-lock.json`, CI runtime configuration). Do not change the repository's declared SDK, Node, framework or language version merely because the local machine differs. If the required toolchain is unavailable and cannot be resolved safely within the task, report the limitation instead of editing source code to compensate.

## Generated Code

When the error is in generated output (OpenAPI clients, source generators, EF Core migrations, Angular build output), identify the generator and its input first, then fix the source configuration or input and regenerate (Principles).

## Iteration Limits

Several focused attempts is a reasonable default, not an unlimited edit/build loop. Stop and reassess when the same root failure survives materially different fixes, fixes create increasing unrelated failures, the installed toolchain is incompatible, required external infrastructure is unavailable, package compatibility cannot be resolved safely, or the correct behavior cannot be determined from the project or request. Do not repeat variants of the same failed guess.

## Regressions

If a fix introduces new failures, determine whether they reveal a legitimate dependency of the change; otherwise revert or correct that fix before continuing. Do not leave the repository knowingly worse than the starting state. Do not clean up unrelated pre-existing failures unless they block verification of the requested repair or the user asks.

## Architecture

A green build obtained by violating project architecture is not a successful repair. Invalid shortcuts include an Application → Infrastructure reference, `DbContext` leaking into Application, business logic moved into a controller, server authorization replaced by Angular-only guards, and HTTP calls scattered into components to bypass a data-access service.

## Tests Created During Diagnosis

A new behavioral test or temporary probe used to establish correct behavior follows `verify` § 4. Build, compiler and static-analysis commands themselves do not require new tests.

## Completion

The task is complete when the affected scope is green — backend build, frontend build, affected tests, consistent cross-stack contract as applicable — with no known new regression and no accidental workaround in the final diff. Do not require an unrelated frontend build for a backend-only repair or vice versa. Then run `verify` for the final completion pass when appropriate.

## Reporting

Report what was actually repaired and verified; never claim the problem is fixed while a known relevant failure remains.

    Initial failure:  <failure>
    Root cause:       <cause>
    Changes made:     <changes>
    Backend build:    PASS / NOT RUN / NOT APPLICABLE
    Frontend build:   PASS / NOT RUN / NOT APPLICABLE
    Tests:            PASS / NOT RUN / NOT APPLICABLE
    Remaining issues: None / <details>
