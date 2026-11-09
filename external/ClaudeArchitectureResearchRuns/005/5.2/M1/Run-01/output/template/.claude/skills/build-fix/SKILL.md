---
name: build-fix
description: >
  Run when a .NET or frontend build fails, tests break after a change or
  upgrade, or the user asks to make the repository green: reproduce, diagnose,
  bounded fix loop.
---

> **Workflow skill** · Owns: build/test repair procedure — reproduce and diagnose first, bounded focused iteration, no weakened verification, fix generated output at its source · Scope: common · Loading: on demand (routed from `CLAUDE.md` → Procedures)

# Build Fix

## Goal

Restore the affected repository scope to a green build/test state without hiding
failures, weakening behavior, or introducing unrelated changes.

`build-fix` is a repair workflow.

Use:

    code-review
        -> to inspect completed changes for defects

    verify
        -> to prove a completed change is ready

    build-fix
        -> when a build/test failure already exists and must be repaired

## Principles

- Diagnose before editing.
- Reproduce the failure before guessing at a fix.
- Fix root causes before downstream symptoms.
- Keep each iteration small.
- Re-run the narrowest failing verification after each meaningful fix.
- Expand verification only after the focused failure is fixed.
- Do not weaken tests merely to make them pass.
- Do not suppress compiler, TypeScript, lint, or analyzer errors without
  understanding them.
- Preserve architecture and project conventions while fixing the failure.
- Stop when progress has clearly stalled rather than making speculative edits.

## Determine the Affected Scope

Before running commands, determine whether the failure concerns:

    .NET backend
    frontend workspace
    backend + frontend
    API contract/client generation
    package/dependency changes
    repository/toolchain configuration

Do not run unrelated build systems merely because they exist in the repository.

Examples:

    backend-only compile failure
        -> start with the affected .NET project

    frontend template/TypeScript failure
        -> start with the frontend workspace

    changed API contract consumed by the frontend
        -> inspect and verify both sides

    documentation-only failure
        -> do not run application builds without a reason

## Reproduce the Failure

Start with the narrowest command that reliably reproduces the problem.

### .NET

Typical commands include:

    dotnet build backend/MyApp.Api/MyApp.Api.csproj

or, when broader scope is required:

    dotnet build

For a failing test project:

    dotnet test backend/MyApp.Application.Tests/MyApp.Application.Tests.csproj

Use the repository's actual `.slnx`, project path, and configuration where
appropriate.

### Frontend

First inspect the frontend workspace's `package.json`.

Use scripts that actually exist.

Typical examples may include:

    npm run build
    npm test

Do not invent script names.

Do not assume a particular test runner merely because a frontend framework is in
use; the frontend capability's baseline runner is recorded in its stack decision,
and an existing project may deliberately use another configured runner.

## Capture the Actual Error

Read the complete relevant failure output.

Do not fix only the first visible line when the surrounding diagnostic provides
important context.

Group related errors by likely root cause.

Common .NET categories include:

    missing project/package reference
    namespace/type resolution
    changed API signature
    nullability
    generic/type mismatch
    interface contract change
    package version/API change
    source-generation problem
    project/MSBuild configuration
    target framework or SDK mismatch

Common frontend categories include:

    TypeScript type error
    template compilation error
    dependency injection/provider error
    route configuration error
    missing package/module
    framework/TypeScript peer-version mismatch
    generated API client mismatch
    build configuration problem

Framework-specific categories: the frontend knowledge facet.

One root cause may produce many secondary failures.

Fix the highest-leverage cause first.

## Backend Build-Fix Loop

For .NET failures:

1. Reproduce the narrowest failure.
2. Identify the probable root cause.
3. Inspect the relevant source, project references, and package configuration.
4. Make the smallest correct change.
5. Re-run the same failing build/test.
6. Compare the new failure set to the previous one.
7. Expand verification only after the focused failure is resolved.

Do not solve architectural dependency problems by adding invalid project
references.

For example, do not make Application reference Infrastructure merely because
that makes a missing type compile.

Follow `architecture-style.md`.

## Frontend Build-Fix Loop

For frontend failures:

1. Inspect `package.json` and the relevant framework configuration.
2. Reproduce the failing build/test command.
3. Read the TypeScript/framework diagnostic in context.
4. Inspect the affected component, service, route, template, or configuration.
5. Make the smallest correct change.
6. Re-run the same command.
7. Expand to broader frontend verification after the focused failure is fixed.

Follow `frontend.md`, the frontend rule facet, and the frontend knowledge facet
for frontend conventions.

Do not:

    convert code to `any` merely to silence TypeScript
    disable strict mode to make code compile
    suppress template diagnostics without understanding them
    apply a framework-specific workaround the frontend knowledge facet rules out
    replace framework APIs speculatively
    introduce another state-management or HTTP library just to bypass a local issue

## Full-Stack and Contract Failures

Some failures cross the backend/frontend boundary.

Examples:

    response contract changed
    generated TypeScript client no longer matches OpenAPI
    enum/value semantics changed
    endpoint path or HTTP method changed
    nullability changed
    authentication contract changed

Determine which contract is authoritative.

Do not independently patch both sides into inconsistent shapes merely to make
both compile.

When OpenAPI/client generation is used:

1. verify the backend contract;
2. regenerate the client using the project's normal workflow;
3. review generated changes;
4. fix handwritten frontend code against the resulting contract.

Do not manually patch generated files unless the project's generation workflow
explicitly requires that.

Follow the `swagger` and `http-api` skills where relevant.

## Test-Fix Flow

When the build succeeds but tests fail:

1. Read the failing test.
2. Read the relevant production behavior.
3. Determine whether the defect is in:
   - production code;
   - test setup;
   - test expectation;
   - environment/configuration;
   - intentionally changed contract.
4. Make the smallest correct change.
5. Re-run the affected test or test project.
6. Run broader relevant tests after the focused failure is fixed.

Do not change:

    strong assertion
    -> weak assertion

merely to obtain a green test.

Do not delete or skip a failing test solely because fixing it is inconvenient.

If expected behavior intentionally changed, update the test to express the new
contract and confirm that the behavioral change was actually requested.

Backend testing guidance belongs to the `dotnet-testing` skill.

Frontend testing guidance belongs to the frontend knowledge facet.

## Dependency and Package Failures

When a failure follows adding or upgrading a NuGet or npm dependency:

1. Inspect the exact installed/requested version.
2. Confirm framework/runtime compatibility.
3. Inspect peer dependencies where applicable.
4. Read the actual compiler/build diagnostics.
5. Check official migration/release documentation when necessary.
6. Update usage deliberately.

All dependency additions or version changes must follow the `add-dependency`
workflow and:

    .claude/rules/dependencies.md

This includes:

    stable-compatible version selection
    license verification
    deprecation checks
    vulnerability checks
    commercial/license approval rules

Do not replace a package or add another dependency merely to make the build
green without applying the dependency policy.

### NuGet

Central Package Management applies (`dependencies.md`): resolve version
conflicts in `Directory.Packages.props`, not by adding versions to individual
`.csproj` files.

### npm

Preserve the repository's lockfile and dependency model. Peer-dependency
conflicts are resolved as `add-dependency` describes, never bypassed with force
flags merely to get a green build.

Do not delete `package-lock.json` reflexively as a troubleshooting technique.

## Framework/API Upgrades

When failures follow a .NET, frontend framework, TypeScript, persistence
technology, or other framework
upgrade:

- inspect the actual installed version;
- distinguish compilation errors from changed runtime behavior;
- check official migration documentation when needed;
- update obsolete API usage deliberately;
- preserve project architecture and behavior where the upgrade does not require
  change.

Do not fabricate replacement APIs from memory when they can be verified.

Do not perform an additional unrelated framework upgrade while repairing the
current one.

## Toolchain Problems

Determine whether the failure originates from source code or from the local
toolchain.

Relevant checks may include:

    dotnet --info
    dotnet --version
    node --version
    npm --version

Also inspect:

    global.json
    target framework
    frontend framework package versions
    package-lock.json
    CI/runtime version configuration

Do not change the repository's declared SDK, Node, framework, or language
version merely because the local machine has a different version installed.

If the required toolchain is unavailable and cannot be resolved safely within
the requested task, report that limitation instead of editing source code to
compensate for it.

## Generated Code

When the error occurs in generated output, identify the generator/input first.

Examples include:

    OpenAPI clients
    source generators
    persistence migrations
    frontend generated build output

Default: fix the source configuration or input and regenerate.

Do not manually patch disposable generated output unless the repository treats
that output as maintained source.

## Iteration Limits

Use bounded iteration.

A reasonable default is several focused attempts, not an unlimited edit/build
loop.

Stop and reassess when:

- the same root failure survives repeated materially different fixes;
- fixes create increasing unrelated failures;
- the installed toolchain is incompatible;
- required external infrastructure is unavailable;
- package compatibility cannot be resolved safely;
- the correct behavior cannot be determined from the project or request.

Do not repeatedly apply variants of the same failed guess.

## Regressions

If a fix introduces new failures:

- determine whether they reveal a legitimate dependency of the change;
- otherwise revert or correct that fix before continuing.

Do not leave the repository knowingly worse than the state from which the repair
started.

Do not clean up unrelated pre-existing failures unless they block verification
of the requested repair or the user asks for them to be fixed.

## Architecture

A build fix must not bypass architecture merely to compile.

For backend code, follow `architecture-style.md`.

For frontend code, follow `frontend.md` and the frontend rule facet.

Examples of invalid repair shortcuts include:

    Application -> Infrastructure reference
    persistence context leaking into Application
    business logic moved into Controller
    server authorization replaced by frontend-only guards
    HTTP calls scattered into components to bypass a data-access service

A green build obtained by violating project architecture is not a successful
repair.

## Tests Created During Diagnosis

If a new behavioral test or temporary probe is used to establish correct
behavior, apply `verify` → Preserve Behavioral Verification before removing the
temporary diagnostics or probes.

## Completion

A build-fix task is complete when the relevant affected scope is green.

Depending on the task, this may mean:

    backend build passes
    frontend build passes
    affected tests pass
    cross-stack contract is consistent
    no known new regression remains
    final diff contains no accidental workaround

Do not require an unrelated frontend build for a backend-only repair or vice
versa.

After the focused repair succeeds, use the `verify` skill for the final
completion pass when appropriate.

## Reporting

Report what was actually repaired and verified.

Example:

    Initial failure:
    <failure>

    Root cause:
    <cause>

    Changes made:
    <changes>

    Backend build:
    PASS / NOT RUN / NOT APPLICABLE

    Frontend build:
    PASS / NOT RUN / NOT APPLICABLE

    Tests:
    PASS / NOT RUN / NOT APPLICABLE

    Remaining issues:
    None / <details>

Do not claim the problem is fixed while a known relevant failure remains.
