---
name: build-fix
description: >
  Use when a .NET or Angular build or test run fails, an upgrade breaks the
  build, or the user asks to make the repository green: reproduce, diagnose, and
  repair in bounded iterations.
---

> Owns: build/test repair procedure, iteration bounds, repair-completion criteria | Scope: common | Loads: workflow (routed from CLAUDE.md, development-workflow, and verify)

# Build Fix

## Goal

Restore the affected repository scope to a green build/test state without
hiding failures, weakening behavior, or introducing unrelated changes.

`build-fix` is a repair workflow:

```text
code-review -> inspect completed changes for defects
verify      -> prove a completed change is ready
build-fix   -> repair a build/test failure that already exists
```

## Principles

- Reproduce and diagnose the actual failure before editing; do not guess at a
  fix.
- Fix root causes before downstream symptoms.
- Use small, bounded repair iterations: rerun the narrowest failing
  verification after each meaningful fix and expand verification only after the
  focused failure is resolved.
- Do not weaken, delete, skip, or suppress relevant tests or compiler, TypeScript,
  lint, or analyzer failures merely to make verification pass.
- Preserve architecture and project conventions while fixing the failure.
- Stop when progress has clearly stalled rather than making speculative edits.

## Determine the Affected Scope

Before running commands, determine whether the failure concerns the .NET
backend, the Angular frontend, both, API contract/client generation,
package/dependency changes, or repository/toolchain configuration. Read the
`.claude/rules/*.md` files whose `paths` match the failing area before editing —
they may not have loaded yet. Do not run unrelated build systems merely because
they exist.

```text
backend-only compile failure        -> start with the affected .NET project
Angular template/TypeScript failure -> start with the Angular workspace
changed API contract used by Angular -> inspect and verify both sides
documentation-only failure          -> no application builds without a reason
```

## Reproduce the Failure

Start with the narrowest command that reliably reproduces the problem.

### .NET

```bash
dotnet build backend/MyApp.Api/MyApp.Api.csproj
dotnet build
dotnet test backend/MyApp.Application.Tests/MyApp.Application.Tests.csproj
```

Use the repository's actual `.slnx`, project paths, and configuration.

### Angular

Inspect the workspace's `package.json` first and use scripts that actually
exist (typically `npm run build`, `npm test`). Do not invent script names or
assume a test runner merely because Angular is in use; Vitest is the baseline
for newly scaffolded projects, but an existing project may deliberately use
another configured runner.

## Capture the Actual Error

Read the complete relevant output, not only the first visible line, and group
related errors by likely root cause. One root cause may produce many secondary
failures; fix the highest-leverage cause first.

Common .NET categories: missing project/package reference, namespace/type
resolution, changed API signature, nullability, generic/type mismatch,
interface contract change, package version/API change, source-generation
problem, project/MSBuild configuration, target framework or SDK mismatch.

Common Angular categories: TypeScript type error, template compilation error,
dependency injection/provider error, invalid standalone import, route
configuration error, signal/RxJS typing issue, missing package/module,
Angular/TypeScript peer-version mismatch, generated API client mismatch, build
configuration problem.

## Backend Build-Fix Loop

1. Reproduce the narrowest failure.
2. Identify the probable root cause.
3. Inspect the relevant source, project references, and package configuration.
4. Make the smallest correct change.
5. Rerun the same failing build/test.
6. Compare the new failure set to the previous one.
7. Expand verification only after the focused failure is resolved.

Do not solve dependency-direction problems with invalid project references —
for example, never make Application reference Infrastructure because a missing
type would then compile (`.claude/rules/architecture.md`).

## Frontend Build-Fix Loop

1. Inspect `package.json` and the relevant Angular configuration.
2. Reproduce the failing build/test command.
3. Read the TypeScript/Angular diagnostic in context.
4. Inspect the affected component, service, route, template, or configuration.
5. Make the smallest correct change.
6. Rerun the same command.
7. Expand to broader frontend verification after the focused failure is fixed.

Do not convert code to `any` to silence TypeScript, disable strict mode,
suppress template diagnostics without understanding them, add NgModules to work
around a standalone configuration problem, replace framework APIs
speculatively, or introduce another state-management or HTTP library to bypass
a local issue (`.claude/rules/angular.md`).

## Full-Stack and Contract Failures

Some failures cross the backend/frontend boundary: a changed response contract,
a generated TypeScript client that no longer matches OpenAPI, changed
enum/value semantics, endpoint path or method, nullability, or authentication
contract. Determine which contract is authoritative; do not patch both sides
into inconsistent shapes merely to make both compile. Generated clients and
other generated output follow the generated-output step in
`development-workflow`; HTTP and documentation technique: `http-api`,
`swagger`.

## Test-Fix Flow

When the build succeeds but tests fail:

1. Read the failing test.
2. Read the relevant production behavior.
3. Decide whether the defect is in production code, test setup, the test
   expectation, environment/configuration, or an intentionally changed
   contract.
4. Make the smallest correct change.
5. Rerun the affected test or test project.
6. Run broader relevant tests after the focused failure is fixed.

Do not turn a strong assertion into a weak one to obtain a green test, and do not
delete or skip a failing test because fixing it is inconvenient. If expected
behavior intentionally changed, update the test to express the new contract and
confirm that the change was actually requested. Test technique:
`dotnet-testing` and `angular`.

## Dependency and Package Failures

When a failure follows adding or upgrading a NuGet or npm dependency:

1. Inspect the exact installed/requested version.
2. Confirm framework/runtime compatibility.
3. Inspect peer dependencies where applicable.
4. Read the actual compiler/build diagnostics.
5. Check official migration or release documentation when necessary.
6. Update usage deliberately.

Any dependency addition, replacement, or version change made during the repair
goes through `add-dependency`; do not add or swap packages merely to make the
build green. Respect Central Package Management — do not work around conflicts
by duplicating versions in `.csproj` files. Preserve the npm lockfile and
dependency model: do not use peer-dependency force flags and do not delete
`package-lock.json` reflexively as a troubleshooting technique.

## Framework/API Upgrades

When failures follow a .NET, Angular, TypeScript, EF Core, or other framework
upgrade: inspect the actual installed version, distinguish compilation errors
from changed runtime behavior, check official migration documentation when
needed, update obsolete API usage deliberately, and preserve architecture and
behavior where the upgrade does not require change. Do not fabricate
replacement APIs from memory when they can be verified, and do not perform an
additional unrelated upgrade while repairing the current one.

## Toolchain Problems

Determine whether the failure comes from source code or the local toolchain
(`dotnet --info`, `dotnet --version`, `node --version`, `npm --version`;
`global.json`, target framework, Angular package versions,
`package-lock.json`, CI/runtime version configuration). Do not change the
repository's declared SDK, Node, framework, or language version because the
local machine has a different version installed. If the required toolchain is
unavailable and cannot be resolved safely within the task, report that
limitation instead of editing source code to compensate.

## Iteration Limits

Use bounded iteration — several focused attempts, not an unlimited edit/build
loop. Stop and reassess when:

- the same root failure survives repeated, materially different fixes;
- fixes create increasing unrelated failures;
- the installed toolchain is incompatible;
- required external infrastructure is unavailable;
- package compatibility cannot be resolved safely;
- the correct behavior cannot be determined from the project or request.

Do not repeatedly apply variants of the same failed guess.

## Regressions

If a fix introduces new failures, determine whether they reveal a legitimate
dependency of the change; otherwise revert or correct that fix before
continuing. Do not leave the repository knowingly worse than when the repair
started, and do not clean up unrelated pre-existing failures unless they block
verification of the requested repair or the user asks.

## Architecture

A build fix must not bypass architecture to compile. Invalid shortcuts include
an Application → Infrastructure reference, `DbContext` leaking into
Application, business logic moved into a Controller, server authorization
replaced by Angular-only guards, or HTTP calls scattered into components to
bypass a data-access service. A green build obtained by violating project
architecture is not a successful repair.

## Tests Created During Diagnosis

A temporary probe or new behavioral test used to establish correct behavior is
handled by `verify` step 4: the behavior stays covered by maintained automated
tests before the probe is removed. Build, compiler, and static-analysis
commands do not themselves require new tests.

## Completion

A build-fix task is complete when the relevant affected scope is green:
backend build passes, frontend build passes, affected tests pass, the
cross-stack contract is consistent, no known new regression remains, and the
final diff contains no accidental workaround — as applicable to the task. Do not
require an unrelated frontend build for a backend-only repair, or vice versa.
After the focused repair succeeds, run `verify` for the final completion pass
when appropriate.

## Reporting

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
