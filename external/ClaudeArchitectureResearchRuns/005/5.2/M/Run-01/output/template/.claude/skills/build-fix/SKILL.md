---
name: build-fix
description: >
  Use when a .NET or Angular build fails, tests break after a change, a package
  or framework upgrade introduces errors, or the user asks to make the
  repository green.
---

> Workflow skill. Owns: the build/test repair procedure — reproduction and diagnosis first, bounded focused iteration, no weakening of verification, generated-output repair at the source · Scope: common · Loads: on invocation · Depends on: CLAUDE.md, .claude/rules/

# Build Fix

Restore the affected scope to a green build/test state without hiding failures,
weakening behavior, or introducing unrelated changes.

| Workflow | Use |
|---|---|
| `code-review` | inspect completed changes for defects |
| `verify` | prove a completed change is ready |
| `build-fix` | repair an existing build or test failure |

## Principles

- When repairing a build or test failure, reproduce and diagnose the actual
  failure before editing, and fix root causes before downstream symptoms.
- Use small, bounded repair iterations: rerun the narrowest failing
  verification after each meaningful fix, and expand verification only after
  the focused failure is resolved.
- Do not weaken, delete, skip, or suppress relevant tests, compiler errors, or
  analyzer failures merely to make verification pass.
- Preserve architecture and project conventions while fixing (see
  Architecture below).
- Stop when progress has clearly stalled instead of making speculative edits.

## Determine the Affected Scope

Before running commands, decide whether the failure concerns the .NET backend,
the Angular frontend, both, an API contract or generated client, a
package/dependency change, or repository/toolchain configuration. Do not run
unrelated build systems merely because they exist.

```text
backend-only compile failure        -> start with the affected .NET project
Angular template/TypeScript failure -> start with the Angular workspace
changed API contract used by Angular -> inspect and verify both sides
documentation-only failure          -> no application builds without a reason
```

## Reproduce the Failure

Start with the narrowest command that reliably reproduces the problem.

- .NET: `dotnet build backend/MyApp.Api/MyApp.Api.csproj`, or `dotnet build`
  for broader scope; for a failing test project
  `dotnet test backend/MyApp.Application.Tests/MyApp.Application.Tests.csproj`.
  Use the repository's actual `.slnx`, project paths, and configuration.
- Angular: inspect the workspace `package.json` first and use scripts that
  actually exist (for example `npm run build`, `npm test`). Do not invent script
  names or assume a test runner; Vitest is the baseline for new projects, but an
  existing project may deliberately use another runner.

## Capture the Actual Error

Read the complete relevant output, not only the first visible line, and group
related errors by likely root cause; one root cause may produce many secondary
failures, so fix the highest-leverage cause first.

Common .NET categories: missing project/package reference; namespace/type
resolution; changed API signature; nullability; generic/type mismatch;
interface contract change; package version/API change; source-generation
problem; project/MSBuild configuration; target framework or SDK mismatch.

Common Angular categories: TypeScript type error; template compilation error;
dependency-injection/provider error; invalid standalone import; route
configuration error; signal/RxJS typing issue; missing package/module;
Angular/TypeScript peer-version mismatch; generated API client mismatch; build
configuration problem.

## Backend Loop

1. Reproduce the narrowest failure.
2. Identify the probable root cause.
3. Inspect the relevant source, project references, and package configuration.
4. Make the smallest correct change.
5. Rerun the same failing build/test.
6. Compare the new failure set with the previous one.
7. Expand verification only after the focused failure is resolved.

## Frontend Loop

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
speculatively, or add another state-management or HTTP library to bypass a
local issue.

## Full-Stack and Contract Failures

Failures such as a changed response contract, a generated TypeScript client out
of sync with OpenAPI, changed enum/value semantics, a changed endpoint path or
method, changed nullability, or a changed authentication contract cross the
boundary. Determine which contract is authoritative; do not patch both sides
into inconsistent shapes merely to make both compile. When OpenAPI client
generation is used: verify the backend contract, regenerate the client with the
project's workflow, review the generated changes, then fix handwritten frontend
code against the result (`swagger`, `http-api` skills).

## Test-Fix Flow

When the build succeeds but tests fail:

1. read the failing test;
2. read the relevant production behavior;
3. decide whether the defect is in production code, test setup, the test
   expectation, environment/configuration, or an intentionally changed
   contract;
4. make the smallest correct change;
5. rerun the affected test or test project;
6. run broader relevant tests after the focused failure is fixed.

Turning a strong assertion into a weak one, or deleting or skipping a failing
test because fixing it is inconvenient, is weakening verification. If expected
behavior changed intentionally, update the test to express the new contract
and confirm the behavioral change was actually requested. Technique:
`dotnet-testing` and `angular` skills.

## Dependency and Package Failures

When a failure follows a NuGet or npm addition or upgrade: inspect the exact
installed/requested version, confirm framework/runtime and peer compatibility,
read the actual diagnostics, check official migration or release documentation
when necessary, and update usage deliberately. Any dependency addition or
version change goes through `add-dependency`; do not replace a package or add
another one merely to make the build green. Respect Central Package Management
(`dependencies.md`) instead of duplicating conflicting versions in `.csproj`
files, and do not delete `package-lock.json` reflexively as a troubleshooting
technique. Peer-dependency conflicts: `add-dependency` (Install).

## Framework and API Upgrades

Inspect the actual installed version, distinguish compilation errors from
changed runtime behavior, check official migration documentation, update
obsolete API usage deliberately, and preserve architecture and behavior where
the upgrade does not require change. Do not fabricate replacement APIs from
memory when they can be verified, and do not perform an additional unrelated
upgrade while repairing the current one.

## Toolchain Problems

Decide whether the failure comes from source or the local toolchain (`dotnet
--info`, `dotnet --version`, `node --version`, `npm --version`; `global.json`,
target framework, Angular package versions, `package-lock.json`, CI runtime
configuration). Do not change the repository's declared SDK, Node, framework,
or language version because the local machine differs. If the required
toolchain is unavailable and cannot be resolved safely within the task, report
the limitation instead of editing source to compensate.

## Generated Code

Default: when generated output is wrong, or its source contract or
configuration changes, fix or update the authoritative source (OpenAPI
contract, generator configuration, model, migration input) and regenerate; do
not manually patch disposable generated output unless the repository or
generation workflow intentionally treats that output as maintained source.

## Iteration Limits

Use several focused attempts, not an unlimited edit/build loop. Stop and
reassess when the same root failure survives materially different fixes, fixes
create increasing unrelated failures, the installed toolchain is incompatible,
required external infrastructure is unavailable, package compatibility cannot
be resolved safely, or the correct behavior cannot be determined from the
project or request. Do not repeatedly apply variants of the same failed guess.

## Regressions

If a fix introduces new failures, determine whether they reveal a legitimate
dependency of the change; otherwise revert or correct that fix before
continuing. Do not leave the repository knowingly worse than the starting state,
and do not clean up unrelated pre-existing failures unless they block
verification of the requested repair or the user asks.

## Architecture

A green build obtained by violating project architecture is not a successful
repair. Invalid shortcuts include an `Application -> Infrastructure` reference,
`DbContext` leaking into Application, business logic moved into a Controller,
server authorization replaced by Angular-only guards, and HTTP calls scattered
into components to bypass a data-access service (`architecture.md`,
`persistence.md`, `angular.md`, `security.md`).

## Tests Created During Diagnosis

Behavior established by a new probe or diagnostic test follows `verify`
(Preserve Behavioral Verification). Temporary diagnostics may be removed only
after uniquely verified behavior is preserved.

## Completion

The task is complete when the affected scope is green: backend build, frontend
build, affected tests, and cross-stack contract as applicable, with no known new
regression and no accidental workaround in the final diff. Do not require an
unrelated frontend build for a backend-only repair or vice versa. After the
focused repair, run `verify` for the final completion pass when appropriate.

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
