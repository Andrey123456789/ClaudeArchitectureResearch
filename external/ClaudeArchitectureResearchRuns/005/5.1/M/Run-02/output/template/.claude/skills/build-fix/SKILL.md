---
name: build-fix
description: >
  Use when a .NET or Angular build fails, tests fail after a change, an
  upgrade breaks compilation, a generated client drifts, or the user asks to
  make the repository green. Bounded reproduce-diagnose-fix loop.
---

> Owner: build and test repair procedure — diagnosis-first repair, bounded iteration, no weakened verification, generated-output repair | Scope: common | Loads: on demand — workflow (routed by `CLAUDE.md` § Development Workflow) | Enforced: PreToolUse hook blocks npm peer-dependency bypass flags

# Build Fix

## Goal

Restore the affected scope to a green build/test state without hiding failures,
weakening behavior, or introducing unrelated changes.

```text
code-review -> inspect completed changes for defects
verify      -> prove a completed change is ready
build-fix   -> repair a build or test failure that already exists
```

## Principles

- Reproduce and diagnose the actual failure before editing; do not guess at a
  fix before reproducing it.
- Fix root causes before downstream symptoms.
- Keep each iteration small, re-run the narrowest failing verification after each
  meaningful fix, and expand verification only after the focused failure is
  resolved.
- Never weaken, delete, skip, or suppress relevant tests, compiler, TypeScript,
  lint, or analyzer failures merely to make verification pass.
- Preserve architecture and project conventions while repairing.
- Stop when progress has clearly stalled rather than making speculative edits.

## Read First

Read the owners for the failing area, since the repair must respect them:
`.claude/rules/architecture.md` (backend), `.claude/rules/angular.md` (frontend),
`.claude/rules/testing.md` (test failures), `.claude/rules/dependencies.md` and
the `add-dependency` workflow (package failures).

## Determine the Affected Scope

Classify the failure: .NET backend, Angular frontend, both, API contract or
client generation, package or dependency change, repository/toolchain
configuration. Do not run unrelated build systems merely because they exist:

```text
backend-only compile failure        -> start with the affected .NET project
Angular template/TypeScript failure -> start with the Angular workspace
changed API contract used by Angular -> inspect and verify both sides
documentation-only failure          -> no application builds without a reason
```

## Reproduce the Failure

Start with the narrowest command that reliably reproduces the problem.

.NET:

```bash
dotnet build backend/MyApp.Api/MyApp.Api.csproj
dotnet build                                   # when broader scope is needed
dotnet test backend/MyApp.Application.Tests/MyApp.Application.Tests.csproj
```

Use the repository's actual `.slnx`, project paths, and configuration.

Angular: inspect the workspace `package.json` first and use scripts that exist
(typically `npm run build`, `npm test`). Do not invent script names or assume a
runner; Vitest is the baseline for new projects, but an existing project may use
another configured runner.

## Capture the Actual Error

Read the complete relevant output, not only the first line, and group errors by
likely root cause.

Common .NET categories: missing project/package reference, namespace or type
resolution, changed API signature, nullability, generic/type mismatch, interface
contract change, package version/API change, source-generation problem,
project/MSBuild configuration, target framework or SDK mismatch.

Common Angular categories: TypeScript type error, template compilation error,
dependency injection/provider error, invalid standalone import, route
configuration error, signal/RxJS typing issue, missing package or module,
Angular/TypeScript peer-version mismatch, generated API client mismatch, build
configuration problem.

One root cause may produce many secondary failures; fix the highest-leverage
cause first.

## Backend Loop

1. Reproduce the narrowest failure.
2. Identify the probable root cause.
3. Inspect the relevant source, project references, and package configuration.
4. Make the smallest correct change.
5. Re-run the same failing build or test.
6. Compare the new failure set with the previous one.
7. Expand verification only after the focused failure is resolved.

Never repair a missing type by adding an outward project reference (for example
Application → Infrastructure); reconsider the abstraction instead.

## Frontend Loop

1. Inspect `package.json` and the relevant Angular configuration.
2. Reproduce the failing build or test command.
3. Read the TypeScript/Angular diagnostic in context.
4. Inspect the affected component, service, route, template, or configuration.
5. Make the smallest correct change and re-run the same command.
6. Expand to broader frontend verification after the focused failure is fixed.

Invalid shortcuts: converting code to `any` to silence TypeScript, disabling
strict mode, suppressing template diagnostics without understanding them, adding
NgModules to work around a standalone configuration problem, replacing framework
APIs speculatively, or adding another state-management or HTTP library to bypass
a local issue.

## Full-Stack and Contract Failures

Examples: changed response contract, generated TypeScript client out of date,
changed enum/value semantics, endpoint path or method change, nullability
change, authentication contract change. Determine which contract is
authoritative; do not patch both sides into inconsistent shapes just to compile.

With OpenAPI client generation:

1. verify the backend contract;
2. regenerate the client with the project's normal workflow;
3. review the generated changes;
4. fix handwritten frontend code against the resulting contract.

## Test-Fix Flow

When the build succeeds but tests fail:

1. read the failing test and the relevant production behavior;
2. decide whether the defect is in production code, test setup, the test
   expectation, environment/configuration, or an intentionally changed contract;
3. make the smallest correct change and re-run the affected test or project;
4. run broader relevant tests after the focused failure is fixed.

Do not turn a strong assertion into a weak one, or delete or skip a failing test
because fixing it is inconvenient. If expected behavior intentionally changed,
update the test to express the new contract and confirm the change was actually
requested.

## Dependency and Package Failures

After adding or upgrading a NuGet or npm dependency: inspect the exact installed
or requested version, confirm framework/runtime and peer compatibility, read the
actual diagnostics, consult official migration notes when needed, and update
usage deliberately. Any version change or replacement package goes through the
`add-dependency` workflow — including its Central Package Management and npm
peer-conflict steps; do not duplicate conflicting versions in individual
`.csproj` files or delete `package-lock.json` reflexively.

## Framework and API Upgrades

Inspect the installed version, distinguish compile errors from changed runtime
behavior, check official migration documentation, and update obsolete API usage
deliberately. Do not fabricate replacement APIs from memory when they can be
verified, and do not perform an additional unrelated upgrade while repairing the
current one.

## Toolchain Problems

Check whether the failure comes from source or toolchain: `dotnet --info`,
`dotnet --version`, `node --version`, `npm --version`, `global.json`, the target
framework, Angular package versions, `package-lock.json`, CI runtime versions.
Do not change the repository's declared SDK, Node.js, framework, or language
version because the local machine differs. If the required toolchain is
unavailable and cannot be resolved safely, report it instead of editing source to
compensate.

## Generated Code

When the error is in generated output (OpenAPI clients, source generators, EF
Core migrations, Angular build output), identify the generator and its input
first. Default: when generated output is wrong or its source contract or
configuration changed, fix or update the authoritative source and regenerate; do
not hand-patch disposable generated output unless the repository or generation
workflow intentionally treats that output as maintained source.

## Iteration Limits

Use several focused attempts, not an unlimited edit/build loop. Stop and
reassess when the same root failure survives materially different fixes, fixes
create increasing unrelated failures, the toolchain is incompatible, required
external infrastructure is unavailable, package compatibility cannot be resolved
safely, or the correct behavior cannot be determined from the project or the
request. Do not repeat variants of the same failed guess.

## Regressions

If a fix introduces new failures, decide whether they reveal a legitimate
dependency of the change; otherwise revert or correct the fix before continuing.
Do not leave the repository knowingly worse than where the repair started, and
do not clean up unrelated pre-existing failures unless they block the requested
repair or the user asks.

## Architecture Check

A green build obtained by violating project architecture is not a successful
repair. Before finishing, confirm the repair did not introduce an Application →
Infrastructure reference, leak `DbContext` into Application, move business logic
into a Controller, replace server authorization with Angular-only guards, or
scatter HTTP calls into components (`.claude/rules/architecture.md`,
`.claude/rules/angular.md`).

## Tests Created During Diagnosis

A probe or new behavioral test used to establish correct behavior falls under
`.claude/rules/testing.md` § Regression and Behavioral Verification. Remove
temporary diagnostics only after uniquely verified behavior is preserved. Build,
compiler, and static-analysis commands do not require new tests.

## Completion

Complete when the affected scope is green: the relevant builds pass, affected
tests pass, the cross-stack contract is consistent, no known new regression
remains, and the final diff contains no accidental workaround. Do not require an
unrelated frontend build for a backend-only repair, or vice versa. Then run the
`verify` workflow when appropriate.

## Reporting

```text
Initial failure:   <failure>
Root cause:        <cause>
Changes made:      <changes>
Backend build:     PASS / NOT RUN / NOT APPLICABLE
Frontend build:    PASS / NOT RUN / NOT APPLICABLE
Tests:             PASS / NOT RUN / NOT APPLICABLE
Remaining issues:  None / <details>
```

Do not claim the problem is fixed while a known relevant failure remains.
