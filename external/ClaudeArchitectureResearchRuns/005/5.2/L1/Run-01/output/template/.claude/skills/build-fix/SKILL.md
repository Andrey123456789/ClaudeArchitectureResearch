---
name: build-fix
description: >
  Repair failing builds or tests: compile errors, broken tests, package or
  framework upgrade breakage, toolchain issues, make-it-green requests; bounded
  fix loop.
---
> Level: 1-architecture | Owns: build/test repair procedure | Scope: common | Loads: on demand (skill)

# Build Fix

Restore the affected scope to a green build/test state without hiding failures,
weakening behavior, or introducing unrelated changes. Use `code-review` to find
defects in completed changes, `verify` to prove a change is ready, and
`build-fix` when a build or test failure already exists.

## Principles

- Reproduce and diagnose the actual failure before editing; fix root causes
  before downstream symptoms.
- Use small, bounded repair iterations: after each meaningful fix re-run the
  narrowest failing verification, and expand verification only after the
  focused failure is resolved.
- Do not weaken, delete, skip, or suppress relevant tests or compiler, lint, or
  analyzer failures merely to make verification pass.
- Preserve architecture and project conventions; stop when progress has clearly
  stalled instead of making speculative edits.

## 1. Determine the affected scope

.NET backend, frontend, both, API contract/client generation, package changes,
or repository/toolchain configuration. Do not run unrelated build systems:
backend compile failure → the affected .NET project; frontend failure → the
frontend workspace; changed API contract consumed by the frontend → both sides;
documentation-only failure → no application builds.

## 2. Reproduce

- .NET: the narrowest reliable command, e.g.
  `dotnet build backend/<Project>/<Project>.csproj` for the affected project, or
  `dotnet build` when broader scope is needed; failing tests via
  `backend-testing.commands`. Use the repository's actual `.slnx`, project
  paths, and configuration.
- Frontend: the failing script from the workspace manifest, per
  `frontend.commands`.

## 3. Capture the actual error

Read the complete relevant output, not only the first line, and group errors by
probable root cause; one root cause often produces many secondary failures.
Common .NET categories: missing project/package reference, namespace/type
resolution, changed API signature, nullability, generic/type mismatch,
interface contract change, package version/API change, source generation,
project/MSBuild configuration, target framework or SDK mismatch. Frontend
categories and framework-specific repair notes: `frontend.commands`.

## 4. Repair loop

1. Reproduce the narrowest failure.
2. Identify the probable root cause.
3. Inspect the relevant source, project references, and package configuration.
4. Make the smallest correct change.
5. Re-run the same failing build or test.
6. Compare the new failure set with the previous one.
7. Expand verification only after the focused failure is resolved.

Never repair by violating architecture: no project reference from the use-case
project to the adapter project, no persistence-technology types in use-case
units, no business logic moved into entry points, no server authorization
replaced by frontend guards, no HTTP calls scattered into presentation
components to bypass a data-access service. A green build obtained by violating
project architecture is not a successful repair.

## 5. Test failures

When the build succeeds but tests fail: read the failing test and the relevant
production behavior; decide whether the defect lies in production code, test
setup, test expectation, environment/configuration, or an intentionally changed
contract; make the smallest correct change; re-run the affected test, then the
broader relevant tests. Never turn a strong assertion into a weak one, or delete
or skip a failing test because fixing it is inconvenient. When expected behavior
intentionally changed, update the test to express the new contract and confirm
that the change was actually requested.

## 6. Contract failures across backend and frontend

Determine which contract is authoritative; do not patch both sides into
inconsistent shapes merely to compile. With OpenAPI client generation: verify
the backend contract, regenerate the client with the project's workflow, review
the generated changes, then fix handwritten frontend code.

## 7. Generated code

Default: when generated output is wrong or its source contract or configuration
changed, fix or update the authoritative source (OpenAPI document, generator
configuration, source-generator input, model behind a migration) and
regenerate. Do not manually patch disposable generated output unless the
repository or generation workflow intentionally treats that output as
maintained source.

## 8. Package, framework, and toolchain failures

- Inspect the exact installed/requested version, framework compatibility, peer
  dependencies, and the actual diagnostics; check official migration notes when
  needed. Every package addition, update, or replacement follows
  `add-dependency` — never add or swap a package just to make the build green.
- Respect the package-management conventions (`package-management.md`).
- After a framework upgrade, distinguish compile errors from runtime behavior
  changes, update obsolete APIs deliberately, do not fabricate replacement APIs
  from memory, and do not perform a second unrelated upgrade.
- Toolchain: check `dotnet --info`, `global.json`, target frameworks, and the
  frontend toolchain versions. Do not change the repository's declared SDK,
  runtime, or language version because the local machine differs; report an
  unavailable required toolchain instead of editing code to compensate.

## 9. Iteration limits and regressions

Use a bounded number of focused attempts. Stop and reassess when the same root
failure survives materially different fixes, fixes create growing unrelated
failures, the toolchain is incompatible, required infrastructure is
unavailable, package compatibility cannot be resolved safely, or correct
behavior cannot be determined. Do not repeat variants of a failed guess. If a
fix introduces new failures, decide whether they reveal a legitimate dependency
of the change; otherwise revert or correct it. Never leave the repository
knowingly worse than before, and do not fix unrelated pre-existing failures
unless they block the requested repair or the user asks.

Probes or new tests created during diagnosis follow `verify` (preserve
behavioral verification).

## Completion and reporting

The task is complete when the affected scope is green: relevant builds pass,
affected tests pass, cross-stack contracts are consistent, no known new
regression remains, and the diff contains no accidental workaround. Do not
require an unrelated frontend build for a backend-only repair or vice versa.
Run `verify` for the final completion pass when appropriate.

```text
Initial failure: <failure>
Root cause: <cause>
Changes made: <changes>
Backend build: PASS / NOT RUN / NOT APPLICABLE
Frontend build: PASS / NOT RUN / NOT APPLICABLE
Tests: PASS / NOT RUN / NOT APPLICABLE
Remaining issues: none / <details>
```

Never claim the problem is fixed while a known relevant failure remains.
