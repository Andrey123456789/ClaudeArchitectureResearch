---
name: build-fix
description: >
  Use when a .NET or Angular build fails, tests break after a change or upgrade, or
  the user asks to make the repository green: bounded diagnose-and-repair loop.
---

> Level: 3 Project · Owns: build/test repair procedure (workflow) · Scope: common · Loads: on invocation · Depends on: CLAUDE.md, .claude/rules/** (owner reads)

# Build Fix

Restore the affected scope to a green build/test state without hiding failures, weakening behavior, or introducing unrelated changes. `code-review` inspects completed changes; `verify` proves a change is ready; `build-fix` repairs a failure that already exists.

## Principles

- Reproduce and diagnose the actual failure before editing; fix root causes before downstream symptoms.
- Keep iterations small and bounded; re-run the narrowest failing verification after each meaningful fix, and expand verification only after the focused failure is resolved.
- Never weaken, delete, skip, or suppress relevant tests or compiler, TypeScript, lint, or analyzer failures merely to make verification pass — no strong-to-weak assertion swaps, no deleting an inconvenient failing test.
- Preserve architecture and project conventions while fixing; stop when progress has clearly stalled rather than making speculative edits.

## Determine the affected scope

Decide whether the failure concerns the .NET backend, the Angular frontend, both, an API contract or generated client, package changes, or repository/toolchain configuration. Do not run unrelated build systems merely because they exist: a backend-only compile failure starts with the affected .NET project; an Angular template/TypeScript failure starts with the workspace; a changed API contract consumed by Angular needs both sides.

## Reproduce

- .NET: the narrowest command that reproduces it, e.g. `dotnet build backend/<Name>.Api/<Name>.Api.csproj` or `dotnet test backend/<Name>.Application.Tests/<Name>.Application.Tests.csproj`; use the repository's actual `.slnx` and configuration.
- Angular: inspect the workspace `package.json` first and use scripts that exist (`npm run build`, `npm test`); never invent script names or assume a runner.

## Capture the actual error

Read the complete relevant output, not just the first line, and group errors by likely root cause. Typical .NET causes: missing project/package reference, namespace/type resolution, changed signatures or interface contracts, nullability, generic mismatches, package API changes, source generation, MSBuild configuration, target framework or SDK mismatch. Typical Angular causes: TypeScript or template errors, DI/provider errors, invalid standalone imports, route configuration, signal/RxJS typing, missing packages, Angular/TypeScript peer mismatch, generated client mismatch, build configuration. Fix the highest-leverage cause first.

## Backend loop

1. Reproduce the narrowest failure. 2. Identify the probable root cause. 3. Inspect the relevant source, project references, and package configuration. 4. Make the smallest correct change. 5. Re-run the same build/test. 6. Compare the new failure set with the previous one. 7. Expand verification only after the focused failure is resolved.

Never fix a dependency problem with an invalid project reference (for example Application → Infrastructure); re-read `.claude/rules/1-architecture/backend-layers.md`.

## Frontend loop

1. Inspect `package.json` and Angular configuration. 2. Reproduce the failing command. 3. Read the diagnostic in context. 4. Inspect the affected component, service, route, template, or configuration. 5. Make the smallest correct change. 6. Re-run the same command. 7. Broaden frontend verification afterwards.

Do not convert code to `any` to silence TypeScript, disable strict mode, suppress template diagnostics without understanding them, add NgModules to work around standalone configuration, replace framework APIs speculatively, or add another state-management or HTTP library to bypass a local issue (`.claude/rules/2-technology/angular.md`).

## Full-stack and contract failures

Determine which contract is authoritative; do not patch both sides into inconsistent shapes just to compile. With OpenAPI client generation: verify the backend contract, regenerate the client through the normal workflow, review the generated changes, then fix handwritten frontend code against the result.

## Test failures

When the build succeeds but tests fail: read the failing test and the production behavior; decide whether the defect is in production code, test setup, test expectation, environment/configuration, or an intentionally changed contract; make the smallest correct change; re-run the affected test, then broader relevant tests. If expected behavior intentionally changed, update the test to express the new contract and confirm the change was actually requested.

## Dependency, framework, and toolchain failures

- After a package change: inspect the exact installed/requested version, framework/runtime compatibility, and peer dependencies; read the real diagnostics and official migration notes; update usage deliberately. Any package addition or version change goes through `add-dependency` — never add or swap a package just to get green. Work within `.claude/rules/3-project/package-management.md` instead of around it (central versions, lockfile), resolve peer conflicts as `add-dependency` requires, and do not delete `package-lock.json` reflexively as a troubleshooting technique.
- After a framework upgrade: distinguish compile errors from runtime behavior changes, update obsolete APIs from verified documentation (never invent replacement APIs from memory), and do not perform another unrelated upgrade at the same time.
- Toolchain: check `dotnet --info`, `node --version`, `npm --version`, `global.json`, target frameworks, Angular versions, lockfile, and CI runtime versions. Never change the declared SDK, Node, framework, or language version just because the local machine differs; if the required toolchain is unavailable, report the limitation instead of editing source to compensate.

## Generated code

When generated output is wrong or its source contract/configuration changed, fix or update the authoritative source and regenerate (OpenAPI clients, source generators, migrations, build output). Do not manually patch disposable generated output unless the repository or its generation workflow intentionally treats that output as maintained source (default).

## Iteration limits and regressions

Use several focused attempts, not an unlimited loop. Stop and reassess when the same root failure survives materially different fixes, fixes create increasing unrelated failures, the toolchain is incompatible, required infrastructure is unavailable, package compatibility cannot be resolved safely, or correct behavior cannot be determined. If a fix introduces new failures, decide whether they reveal a legitimate dependency of the change; otherwise revert or correct the fix. Never leave the repository knowingly worse than before, and leave unrelated pre-existing failures alone unless they block verification or the user asks.

A green build obtained by violating the architecture (outward references, persistence types in Application, business logic in Controllers, Angular-only authorization, HTTP calls scattered into components) is not a successful repair. Behavior established with a temporary probe during diagnosis is preserved as `verify` step 4 requires.

## Completion and report

The task is complete when the affected scope is green: relevant builds pass, affected tests pass, cross-stack contracts are consistent, no known new regression remains, and the diff contains no accidental workaround. Do not require an unrelated frontend build for a backend-only repair or vice versa. Then run `verify` when appropriate.

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
