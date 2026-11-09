---
name: build-fix
description: >
  Use when a .NET or Angular build fails, tests are broken after a change, a
  package/framework upgrade introduces errors, or the user asks to make the
  repository green. Bounded, evidence-driven repair loop for backend, frontend,
  contract, dependency, and toolchain failures.
---

> Owns: build/test repair procedure, iteration limits, generated-code handling, repair reporting | Scope: common | Loads: workflow (CLAUDE.md routing)

# Build Fix

Restore the affected scope to a green build/test state without hiding failures,
weakening behavior, or introducing unrelated changes. `code-review` inspects
completed changes; `verify` proves a change is ready; `build-fix` repairs an
existing build/test failure.

## Principles

- Reproduce and diagnose the actual failure before editing; fix root causes
  before downstream symptoms.
- Keep each iteration small; rerun the narrowest failing verification after each
  meaningful fix, and expand verification only after that focused failure is
  resolved.
- Never weaken verification to get green (CLAUDE.md, Development Workflow):
  no strong-to-weak assertion swaps, deleted/skipped tests, or suppressed
  compiler/TypeScript/lint/analyzer errors you do not understand.
- Preserve architecture while fixing: read the rules for the affected area
  (`architecture.md`, `angular.md`, `dependencies.md`, ...) if they are not
  already loaded. A green build obtained by violating
  `architecture.md`, `angular.md`, or `security.md` is not a repair — for
  example an `Application -> Infrastructure` reference, `DbContext` leaking into
  Application, business logic moved into a Controller, server authorization
  replaced by Angular guards, or HTTP calls scattered into components.
- Stop when progress has clearly stalled rather than making speculative edits.

## 1. Determine the Affected Scope

Classify the failure: .NET backend, Angular frontend, both, API
contract/client generation, package/dependency change, or repository/toolchain
configuration. Do not run unrelated build systems merely because they exist
(backend compile failure → start with the affected .NET project; Angular
template/TypeScript failure → the Angular workspace; changed contract consumed
by Angular → both sides; documentation-only → no application builds).

## 2. Reproduce

Start with the narrowest reliable command, using the repository's actual
`.slnx`, project paths, and configuration:

```bash
dotnet build backend/MyApp.Api/MyApp.Api.csproj
dotnet test backend/MyApp.Application.Tests/MyApp.Application.Tests.csproj
```

For Angular, inspect `package.json` first and run only scripts that exist (for
example `npm run build`, `npm test`). Vitest is the baseline for new projects,
but an existing project may deliberately use another configured runner.

## 3. Capture the Actual Error

Read the complete relevant output, not just the first line, and group errors by
likely root cause. One root cause can produce many secondary failures; fix the
highest-leverage cause first.

Common .NET causes: missing project/package reference, namespace/type
resolution, changed signature, nullability, generic/type mismatch, interface
contract change, package API change, source generation, MSBuild configuration,
target framework/SDK mismatch. Common Angular causes: TypeScript type error,
template compilation, DI/provider error, invalid standalone import, route
configuration, signal/RxJS typing, missing package, Angular/TypeScript peer
mismatch, generated API client mismatch, build configuration.

## 4. Repair Loop

1. Inspect the relevant source, project references, package configuration, or
   Angular configuration.
2. Make the smallest correct change.
3. Rerun the same failing command and compare the new failure set with the
   previous one.
4. Expand verification only after the focused failure is resolved.

Angular-specific shortcuts that are not repairs: converting code to `any` to
silence TypeScript, disabling strict mode, suppressing template diagnostics,
adding NgModules to work around standalone configuration, speculative framework
API replacement, or adding another state/HTTP library to bypass a local issue.

## Test Failures

When the build succeeds but tests fail: read the failing test and the relevant
production behavior; decide whether the defect is in production code, test
setup, test expectation, environment/configuration, or an intentionally changed
contract; make the smallest correct change; rerun the test, then broader
relevant tests. If expected behavior intentionally changed, update the test to
express the new contract and confirm the change was actually requested.

## Full-Stack and Contract Failures

Determine which contract is authoritative; never patch both sides into
inconsistent shapes just to compile. With OpenAPI client generation: verify the
backend contract, regenerate the client with the project's normal workflow,
review the generated diff, then fix handwritten frontend code.

## Generated Code

When generated output is wrong or its source contract/configuration changed,
fix or update the authoritative source (OpenAPI document, source generator
input, migration model, build configuration) and regenerate. Do not manually
patch disposable generated output unless the repository or generation workflow
intentionally treats it as maintained source.

## Dependency, Upgrade, and Toolchain Failures

- After adding or upgrading a package: inspect the exact version, framework and
  peer compatibility, and the actual diagnostics; consult official migration
  notes; update usage deliberately. Any package addition, replacement, or
  version change goes through `add-dependency` — do not add or swap a package
  merely to get green, keep Central Package Management intact
  (`dependencies.md`), and do not delete `package-lock.json` as a reflexive
  troubleshooting step.
- Framework upgrades: distinguish compilation errors from runtime behavior
  changes, verify replacement APIs rather than inventing them, and do not start
  another unrelated upgrade.
- Toolchain: check `dotnet --info`, `node --version`, `npm --version`,
  `global.json`, target frameworks, and CI runtime configuration. Do not change
  the declared SDK, Node, framework, or language version merely because the
  local machine differs; if the required toolchain is unavailable, report the
  limitation instead of editing source to compensate.

## Iteration Limits

Use bounded iteration — several focused attempts, not an unlimited loop. Stop
and reassess when the same root failure survives materially different fixes,
fixes create growing unrelated failures, the toolchain is incompatible, required
infrastructure is unavailable, package compatibility cannot be resolved safely,
or the correct behavior cannot be determined. Do not repeat variants of a failed
guess.

## Regressions

If a fix introduces new failures, decide whether they reveal a legitimate
dependency of the change; otherwise revert or correct the fix before
continuing. Never leave the repository knowingly worse than the starting state.
Do not clean up unrelated pre-existing failures unless they block verification
or the user asks.

## Tests Created During Diagnosis

Behavior established by a new test or temporary probe must remain covered by
maintained automated tests (`verify`, step 4).

## Completion and Report

The repair is complete when the affected scope is green: relevant builds pass,
affected tests pass, the cross-stack contract is consistent, no known new
regression remains, and the diff contains no workaround. Do not require an
unrelated frontend build for a backend-only repair or vice versa. Then run
`verify` for the final completion pass when appropriate.

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
