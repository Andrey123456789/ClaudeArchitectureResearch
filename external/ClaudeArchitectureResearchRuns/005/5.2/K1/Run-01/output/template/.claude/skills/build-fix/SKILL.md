---
name: build-fix
description: Use when compilation or a build fails, tests break after a change, a package or framework upgrade introduces errors, or the user asks to make the repository green. Bounded, evidence-driven repair for backend, frontend, contract and toolchain failures.
---
Kind: WF | Scope: common | Capability: — | Loading: on invocation (routed from CLAUDE.md, development-workflow and verify)

# Build Fix

Goal: restore the affected scope to a green build and test state without hiding failures, weakening behavior or introducing unrelated changes. `code-review` inspects completed changes for defects, `verify` proves that a completed change is ready, and `build-fix` repairs an existing build or test failure.

## Principles

- Reproduce and diagnose the actual failure before editing; do not guess at a fix.
- Fix root causes before downstream symptoms; one root cause may produce many secondary failures, so fix the highest-leverage cause first.
- Use small, bounded repair iterations. Rerun the narrowest failing verification after each meaningful fix, and expand verification only after the focused failure is resolved.
- Never weaken, delete, skip or suppress relevant tests, compiler, TypeScript, lint or analyzer failures merely to make verification pass. Do not change a strong assertion into a weak one to get a green test. If expected behavior intentionally changed, update the test to express the new contract and confirm the change was actually requested.
- Preserve architecture and project conventions while fixing (see Architecture below).
- Stop when progress has clearly stalled instead of making speculative edits.

## 1. Determine the affected scope

Decide whether the failure concerns the .NET backend, the frontend, both, the API contract or client generation, package or dependency changes, or repository/toolchain configuration. Do not run unrelated build systems merely because they exist: a backend compile failure starts with the affected .NET project, a frontend failure with the frontend workspace, a changed API contract with both sides, and a documentation-only failure needs no application build.

## 2. Reproduce and capture the error

- .NET: start with the narrowest command, for example `dotnet build backend/<Name>.Api/<Name>.Api.csproj`, or the failing test project (backend-testing workflow facet → Run tests). Use the repository's actual `.slnx`, project paths and configuration.
- Frontend: inspect `package.json` and use scripts that exist (frontend workflow facet). Do not invent script names or assume a test runner.
- Read the complete relevant output, not only the first line, and group errors by likely root cause. Common .NET categories: missing project or package reference, namespace or type resolution, changed API signature, nullability, generic or type mismatch, interface contract change, package version or API change, source generation, project/MSBuild configuration, target framework or SDK mismatch. Frontend categories: frontend workflow facet → Build-fix diagnostics.

## 3. Repair loop

1. Identify the probable root cause.
2. Inspect the relevant source, project references, package configuration or frontend configuration.
3. Make the smallest correct change.
4. Rerun the same failing command and compare the new failure set with the previous one.
5. Expand to broader verification only after the focused failure is resolved.

Slot-specific cues: the persistence, backend-testing and frontend workflow facets (Build-fix sections).

## Test failures

When the build succeeds but tests fail: read the failing test and the relevant production behavior, decide whether the defect is in production code, test setup, test expectation, environment or configuration, or an intentionally changed contract, make the smallest correct change, rerun the affected test or project, then run the broader relevant tests.

## Full-stack and contract failures

For response-contract, enum, route, method, nullability or authentication-contract changes, determine which contract is authoritative. Do not patch both sides into inconsistent shapes merely to make both compile. With OpenAPI client generation: verify the backend contract, regenerate the client through the project's normal workflow, review the generated changes, then fix handwritten code against the result.

## Generated output

Default: when generated output is wrong, or its source contract or configuration changed, fix or update the authoritative source (OpenAPI document, source-generator input, model and migration configuration, build configuration) and regenerate. Do not manually patch disposable generated output unless the repository or its generation workflow intentionally treats that output as maintained source.

## Dependency and package failures

After adding or upgrading a NuGet or npm dependency: inspect the exact installed or requested version, confirm framework and runtime compatibility, inspect peer dependencies, read the diagnostics, check official migration notes when necessary, and update usage deliberately. Any dependency addition or version change, including one made to fix the build, follows `add-dependency`. Respect Central Package Management (no conflicting versions in individual `.csproj` files), keep the lockfile and dependency model, and do not delete `package-lock.json` as a reflexive troubleshooting step.

## Framework and API upgrades

Inspect the installed version, distinguish compile errors from changed runtime behavior, check official migration documentation, update obsolete API usage deliberately, and preserve architecture and behavior where the upgrade does not require change. Do not fabricate replacement APIs from memory when they can be verified, and do not perform an additional unrelated upgrade while repairing the current one.

## Toolchain problems

Check whether the failure comes from source code or the local toolchain (`dotnet --info`, `dotnet --version`, `node --version`, `npm --version`; `global.json`, target framework, package versions, lockfile, CI runtime configuration). Do not change the repository's declared SDK, Node, framework or language version merely because the local machine differs. If the required toolchain is unavailable and cannot be resolved safely, report the limitation instead of editing source code to compensate.

## Architecture

A build fix must not bypass architecture merely to compile; a green build obtained by violating the standards is not a successful repair. Invalid shortcuts include an Application → Infrastructure reference, persistence-technology types leaking into Application, business logic moved into a controller, server authorization replaced by frontend-only guards, and HTTP calls scattered into components to bypass a data-access service. Check against `.claude/rules/backend/` and `.claude/rules/frontend/`.

## Iteration limits and regressions

Use several focused attempts, not an unlimited edit/build loop. Stop and reassess when the same root failure survives materially different fixes, fixes create increasing unrelated failures, the toolchain is incompatible, required external infrastructure is unavailable, package compatibility cannot be resolved safely, or the correct behavior cannot be determined. Do not repeat variants of the same failed guess. If a fix introduces new failures, determine whether they reveal a legitimate dependency of the change; otherwise revert or correct that fix. Do not leave the repository knowingly worse than the starting state, and do not clean up unrelated pre-existing failures unless they block verification of the requested repair or the user asks.

## Tests created during diagnosis

Behavior proven by a new probe or test during diagnosis follows `verify` → step 4. Build, compiler and static-analysis commands do not themselves require new tests.

## Completion and report

The repair is complete when the affected scope is green: the relevant builds pass, the affected tests pass, the cross-stack contract is consistent, no known new regression remains, and the final diff contains no accidental workaround. Do not require an unrelated frontend build for a backend-only repair, or the reverse. Then run `verify` for the final pass when appropriate.

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
