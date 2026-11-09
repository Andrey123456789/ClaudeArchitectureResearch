---
name: build-fix
description: >
  Use when a .NET or frontend build fails, tests break, an upgrade introduces
  errors, or the user asks to make the repository green: bounded reproduce,
  diagnose, and fix loop.
---

> Workflow · Owns the build and test repair procedure: reproduction, diagnosis, bounded iteration, no weakened verification, and source-first regeneration

# Build Fix

## Goal

Restore the affected repository scope to a green build/test state without
hiding failures, weakening behavior, or introducing unrelated changes.

`code-review` inspects completed changes for defects, `verify` proves a
completed change is ready, and `build-fix` repairs an existing build or test
failure.

## Principles

- Reproduce and diagnose the actual failure before editing; do not guess.
- Fix root causes before downstream symptoms.
- Keep each repair iteration small and bounded; re-run the narrowest failing
  verification after each meaningful fix, and expand verification only after
  the focused failure is resolved.
- Do not weaken, delete, skip, or suppress relevant tests or compiler, analyzer,
  TypeScript, or lint failures merely to make verification pass.
- Preserve architecture and project conventions while fixing.
- Stop when progress has clearly stalled rather than making speculative edits.

## Determine the Affected Scope

Before running commands, decide whether the failure concerns the .NET backend,
the frontend, both, the API contract or client generation, package/dependency
changes, or repository/toolchain configuration. Do not run unrelated build
systems merely because they exist.

```text
backend-only compile failure          -> start with the affected .NET project
frontend template/TypeScript failure  -> start with the frontend workspace
changed API contract used by frontend -> inspect and verify both sides
documentation-only failure            -> no application builds without a reason
```

## Reproduce the Failure

Start with the narrowest command that reliably reproduces the problem.

```text
dotnet build backend/MyApp.Api/MyApp.Api.csproj
dotnet build
dotnet test backend/MyApp.Application.Tests/MyApp.Application.Tests.csproj
```

Use the repository's actual `.slnx`, project paths, and configuration.

For the frontend, inspect the workspace `package.json` first and use scripts
that actually exist (for example `npm run build`, `npm test`). Do not invent
script names and do not assume a test runner; the baseline runner is recorded in
`docs/capabilities/frontend.md`, but an existing project may deliberately use
another configured runner.

## Capture the Actual Error

Read the complete relevant failure output, not only the first visible line, and
group related errors by likely root cause. One root cause can produce many
secondary failures; fix the highest-leverage cause first.

Common .NET categories: missing project/package reference, namespace/type
resolution, changed API signature, nullability, generic/type mismatch,
interface contract change, package version/API change, source generation,
project/MSBuild configuration, target framework or SDK mismatch.

Common frontend categories: TypeScript type error, template compilation error,
dependency-injection/provider error, invalid component imports, route
configuration error, reactive-state typing issue, missing package/module,
framework/TypeScript peer-version mismatch, generated API client mismatch,
build configuration problem.

## Backend Build-Fix Loop

1. Reproduce the narrowest failure.
2. Identify the probable root cause.
3. Inspect the relevant source, project references, and package configuration.
4. Make the smallest correct change.
5. Re-run the same failing build or test.
6. Compare the new failure set with the previous one.
7. Expand verification only after the focused failure is resolved.

Do not solve architectural dependency problems by adding invalid project
references — for example, do not make Application reference Infrastructure to
make a missing type compile (`.claude/rules/architecture.md`).

## Frontend Build-Fix Loop

1. Inspect `package.json` and the relevant framework configuration.
2. Reproduce the failing build or test command.
3. Read the diagnostic in context.
4. Inspect the affected component, service, route, template, or configuration.
5. Make the smallest correct change.
6. Re-run the same command.
7. Expand to broader frontend verification after the focused failure is fixed.

Follow `.claude/rules/frontend.md`, `.claude/rules/frontend-framework.md`, and
the frontend knowledge skill named in `docs/capabilities/frontend.md`. Do not:

- convert code to `any` merely to silence TypeScript;
- disable strict mode to make code compile;
- suppress template diagnostics without understanding them;
- reintroduce legacy framework constructs that `frontend-framework.md` restricts
  merely to work around a configuration problem;
- replace framework APIs speculatively;
- introduce another state-management or HTTP library to bypass a local issue.

## Full-Stack and Contract Failures

Failures can cross the backend/frontend boundary: changed response contract,
generated client out of date with OpenAPI, changed enum/value semantics,
changed endpoint path or HTTP method, changed nullability, changed
authentication contract. Determine which contract is authoritative; do not patch
both sides into inconsistent shapes merely to make both compile.

When OpenAPI client generation is used: verify the backend contract, regenerate
the client with the project's normal workflow, review generated changes, then
fix handwritten frontend code against the resulting contract (`swagger` and
`http-api` skills).

## Test-Fix Flow

When the build succeeds but tests fail:

1. read the failing test;
2. read the relevant production behavior;
3. decide whether the defect is in production code, test setup, the test
   expectation, environment/configuration, or an intentionally changed
   contract;
4. make the smallest correct change;
5. re-run the affected test or project;
6. run broader relevant tests after the focused failure is fixed.

Do not turn a strong assertion into a weak one, and do not delete or skip a
failing test because fixing it is inconvenient. If expected behavior
intentionally changed, update the test to express the new contract and confirm
the change was actually requested. Testing technique: `dotnet-testing` skill
(backend) and the frontend knowledge skill.

## Dependency and Package Failures

When a failure follows adding or upgrading a NuGet or npm dependency: inspect
the exact installed/requested version, confirm framework/runtime compatibility,
inspect peer dependencies, read the actual diagnostics, check official migration
documentation when necessary, and update usage deliberately.

Every dependency addition or version change during a repair goes through
`add-dependency`; do not replace a package or add another dependency merely to
make the build green. Respect Central Package Management — do not work around
conflicts by duplicating versions in `.csproj` files — and preserve the
frontend lockfile and dependency model; do not delete `package-lock.json`
reflexively as a troubleshooting step.

## Framework and API Upgrades

After a .NET, frontend framework, TypeScript, persistence-library, or other
framework upgrade: inspect the actual installed version, distinguish
compilation errors from changed runtime behavior, check official migration
documentation, update obsolete API usage deliberately, and preserve
architecture and behavior where the upgrade does not require change. Do not
fabricate replacement APIs from memory when they can be verified, and do not
perform an unrelated additional upgrade while repairing the current one.

## Toolchain Problems

Determine whether the failure comes from source code or from the local
toolchain (`dotnet --info`, `dotnet --version`, `node --version`,
`npm --version`; `global.json`, target framework, framework package versions,
`package-lock.json`, CI/runtime version configuration). Do not change the
repository's declared SDK, Node, framework, or language version merely because
the local machine has a different version. If the required toolchain is
unavailable and cannot be resolved safely, report the limitation instead of
editing source code to compensate.

## Generated Code

When generated output is wrong, or its source contract or configuration
changed, identify the generator and its input first (OpenAPI clients, source
generators, database migrations, frontend build output). Fix or update the
authoritative source and regenerate; do not manually patch disposable generated
output unless the repository or generation workflow intentionally treats that
output as maintained source.

## Iteration Limits

Use bounded iteration — several focused attempts, not an unlimited edit/build
loop. Stop and reassess when the same root failure survives repeated materially
different fixes, fixes create increasing unrelated failures, the toolchain is
incompatible, required external infrastructure is unavailable, package
compatibility cannot be resolved safely, or the correct behavior cannot be
determined from the project or request. Do not repeat variants of the same
failed guess.

## Regressions

If a fix introduces new failures, determine whether they reveal a legitimate
dependency of the change; otherwise revert or correct that fix before
continuing. Do not leave the repository knowingly worse than the starting
state, and do not clean up unrelated pre-existing failures unless they block
verification of the requested repair or the user asks.

## Architecture

A build fix must not bypass architecture merely to compile. Invalid shortcuts
include an Application → Infrastructure reference, persistence-technology types
leaking into Application, business logic moved into a Controller, server
authorization replaced by frontend-only guards, and HTTP calls scattered into
components to bypass a data-access service. A green build obtained by violating
project architecture is not a successful repair.

## Tests Created During Diagnosis

If a new behavioral test or temporary probe establishes correct behavior,
`verify` § Preserve Behavioral Verification applies before the probe is
removed. Build, compiler, and static-analysis commands do not require new
tests.

## Completion

A build-fix task is complete when the affected scope is green: backend build,
frontend build, affected tests, a consistent cross-stack contract, no known new
regression, and no accidental workaround in the final diff — as applicable. Do
not require an unrelated frontend build for a backend-only repair or vice versa.
Run `verify` for the final completion pass when appropriate.

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
