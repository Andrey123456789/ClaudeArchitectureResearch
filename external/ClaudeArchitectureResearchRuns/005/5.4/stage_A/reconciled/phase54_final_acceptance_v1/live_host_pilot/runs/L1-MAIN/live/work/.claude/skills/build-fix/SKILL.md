---
name: build-fix
description: Use when a build or automated tests are broken — compile errors, failing tests after a change, errors after package or framework upgrades, toolchain issues, cross-stack contract breaks — or when asked to make the repository green. Bounded, evidence-driven repair loop.
---

> Level: 0-core · Owns: build/test repair procedure — reproduction-first diagnosis, bounded iteration, no weakened verification, source-first fixes for generated output · Loading: on invocation

# Build Fix

Restore the affected scope to a green build/test state without hiding failures, weakening behavior, or adding unrelated changes. `code-review` inspects completed changes; `verify` proves readiness; `build-fix` repairs an existing build/test failure.

## Principles

- Reproduce and diagnose the actual failure before editing; fix root causes before downstream symptoms.
- Work in small, bounded iterations: after each meaningful fix rerun the narrowest failing check, and widen verification only after the focused failure is resolved.
- Preserve architecture and project conventions while fixing.
- Stop when progress has clearly stalled instead of making speculative edits.

## 1. Determine the affected scope

Classify the failure: backend, frontend, both, API contract/client generation, package/dependency change, or repository/toolchain configuration. Do not run unrelated build systems: start a backend compile failure with the affected .NET project, a frontend template or compile failure with the frontend workspace, a changed API contract with both sides, and do not build applications for a documentation-only failure.

## 2. Reproduce

Use the narrowest command that reliably reproduces the problem:

```bash
dotnet build backend/<Project>/<Project>.csproj
dotnet test backend/<TestProject>/<TestProject>.csproj
```

Use the repository's actual `.slnx`, project paths, and configuration. For the frontend, inspect `package.json` and use the scripts that exist (`frontend.commands`); never invent script names or assume a test runner. Backend test commands: `backend-testing.commands`.

## 3. Capture the actual error

Read the complete relevant output, not just the first line, and group errors by likely root cause. Typical .NET categories: missing project/package reference, namespace/type resolution, changed API signature, nullability, generic/type mismatch, interface contract change, package version/API change, source generation, MSBuild configuration, target framework or SDK mismatch. Frontend categories and invalid shortcuts: `frontend.commands` § Build-fix notes. One root cause can produce many secondary failures — fix the highest-leverage cause first.

## 4. Repair loop

1. Reproduce the narrowest failure.
2. Identify the probable root cause.
3. Inspect the relevant source, project references, and package configuration.
4. Make the smallest correct change.
5. Rerun the same failing build/test.
6. Compare the new failure set with the previous one.
7. Expand verification only after the focused failure is resolved.

Never solve a dependency-direction problem with an invalid project reference (for example the use-case layer referencing the implementation layer to make a type compile); follow the boundary rules in `.claude/rules/1-architecture/`.

## 5. Failing tests

When the build succeeds but tests fail: read the failing test and the production behavior, decide whether the defect lies in production code, test setup, test expectation, environment/configuration, or an intentionally changed contract, make the smallest correct change, rerun the affected tests, then broader relevant tests.

Never weaken, delete, skip, or suppress a relevant test, compiler error, or analyzer failure merely to make verification pass — no strong-to-weak assertion swaps, no skipping inconvenient tests. When expected behavior intentionally changed, update the test to express the new contract and confirm the change was actually requested.

## 6. Full-stack and contract failures

Determine which contract is authoritative (response shape, generated client vs. API description, enum semantics, route or method, nullability, authentication contract); never patch both sides into inconsistent shapes just to compile. With generated API clients: verify the backend contract, regenerate the client with the project's workflow, review generated changes, then fix handwritten frontend code. Technique: `http-api` and the Level-2 API-description technique.

## 7. Generated code

Default: when generated output is wrong (generated API clients, source generators, migrations, frontend build output) or its source contract or configuration changed, fix the authoritative source or generator input and regenerate; do not manually patch disposable generated output unless the repository or generation workflow treats it as maintained source.

## 8. Dependency, upgrade, and toolchain failures

- After adding or upgrading a package: inspect the exact version, confirm framework/runtime and peer compatibility, read the diagnostics, consult official migration notes when needed, and update usage deliberately. Every dependency change follows `add-dependency`; never swap or add packages just to get green, never duplicate versions in project files to dodge Central Package Management, never delete the lockfile as a troubleshooting reflex.
- After a framework upgrade: distinguish compile errors from changed runtime behavior; update obsolete APIs deliberately; never fabricate replacement APIs that can be verified; no additional unrelated upgrades.
- Toolchain: check `dotnet --info`, `dotnet --version`, `node --version`, the frontend package manager's version, `global.json`, target frameworks, and CI runtime versions. Do not change the declared SDK, Node, framework, or language version because the local machine differs; if the required toolchain is unavailable, report the limitation instead of editing source to compensate.

## 9. Iteration limits and regressions

Use several focused attempts, not an unlimited loop. Stop and reassess when the same root failure survives materially different fixes, fixes create growing unrelated failures, the toolchain is incompatible, required infrastructure is unavailable, package compatibility cannot be resolved safely, or correct behavior cannot be determined. Never repeat variants of a failed guess. If a fix introduces new failures, keep it only when they reveal a legitimate dependency of the change; otherwise revert or correct it. Never leave the repository knowingly worse than before; leave unrelated pre-existing failures alone unless they block verification or the user asks.

## 10. Probes created during diagnosis

A behavioral probe that establishes correct behavior follows `verify` step 4; build/compiler/static-analysis runs do not require new tests.

## Completion and report

Complete when the affected scope is green: relevant builds pass, affected tests pass, the cross-stack contract is consistent, no known new regression remains, and the diff contains no workaround that bypasses architecture (outward references, persistence types in the use-case layer, business logic in entry points, client-only authorization, HTTP calls scattered into components). Then use `verify` for the completion pass when appropriate.

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
