---
name: build-fix
description: >
  Use when a .NET or Angular build fails, tests break, or an upgrade introduces errors: reproduce, diagnose, bounded repair, report.
---

> Level: 3 Project | Owns: build/test repair procedure, iteration bounds, verification-integrity during repair, generated-output repair | Scope: common | Loads: workflow skill (model-invoked) | Depends on: CLAUDE.md, 0-core/*, 1-architecture/*, 2-technology/*, 3-project/*

# Build Fix

Restore the affected scope to a green build/test state without hiding failures,
weakening behavior, or introducing unrelated changes. `code-review` inspects
completed changes; `verify` proves readiness; `build-fix` repairs an existing
failure.

## Principles

- Reproduce and diagnose the actual failure before editing; fix root causes
  before downstream symptoms. Read the complete relevant diagnostic, group
  related errors, and fix the highest-leverage cause first.
- Work in small bounded iterations: after each meaningful fix rerun the
  narrowest failing verification, and expand verification only after the
  focused failure is resolved.
- Do not weaken, delete, skip, or suppress relevant tests or compiler,
  TypeScript, lint, or analyzer failures merely to make verification pass.
- Preserve architecture and conventions: a green build obtained by violating
  them (Application → Infrastructure reference, persistence context leaking
  into Application, business logic moved into a Controller, server
  authorization replaced by Angular guards, HTTP calls scattered into
  components) is not a repair.
- Default: when generated output is wrong or its source contract or
  configuration changed, fix the authoritative source and regenerate; do not
  hand-patch disposable generated output (OpenAPI clients, source generators,
  EF Core migrations, Angular build output) unless the repository deliberately
  treats it as maintained source.
- Stop and reassess instead of making speculative edits when progress stalls.

## 1. Determine the Affected Scope

Classify the failure: .NET backend, Angular frontend, both, API contract or
client generation, package/dependency change, or repository/toolchain
configuration. Do not run unrelated build systems merely because they exist.

## 2. Reproduce

- .NET: `dotnet build backend/<Name>.Api/<Name>.Api.csproj` (or `dotnet build`
  for broader scope); failing tests:
  `dotnet test backend/<Name>.Application.Tests/<Name>.Application.Tests.csproj`.
  Use the repository's actual `.slnx`, paths, and configuration.
- Angular: inspect `package.json` first and use scripts that exist (typically
  `npm run build`, `npm test`); do not invent script names or assume a test
  runner — Vitest is the baseline for new workspaces, but an existing project
  may use another.

Common .NET causes: missing project/package reference, namespace resolution,
changed signatures, nullability, generic mismatch, interface changes, package
API changes, source generation, MSBuild configuration, SDK/target mismatch.
Common Angular causes: TypeScript types, template compilation, DI providers,
standalone imports, routes, signal/RxJS typing, missing packages,
Angular/TypeScript peer versions, generated client mismatch, build config.

## 3. Repair Loops

**Backend:** reproduce → identify the probable root cause → inspect source,
references, and package configuration → smallest correct change → rerun the
same command → compare the failure set → expand verification.

**Frontend:** inspect `package.json` and Angular configuration → reproduce →
read the diagnostic in context → inspect the affected component, service, route,
template, or configuration → smallest correct change → rerun → expand. Do not
convert code to `any`, disable strict mode, suppress template diagnostics, add
NgModules to dodge a standalone problem, or add another state/HTTP library to
bypass a local issue.

**Full-stack contract:** determine which contract is authoritative; do not
patch both sides into inconsistent shapes. With OpenAPI client generation:
verify the backend contract, regenerate through the normal workflow, review the
generated changes, then fix handwritten code.

**Tests:** read the failing test and the production behavior; decide whether
the defect is in production code, test setup, expectation, environment, or an
intentionally changed contract; make the smallest correct change; rerun the
test, then broader tests. If expected behavior intentionally changed, update
the test to express the new contract and confirm the change was requested.

**Packages and upgrades:** inspect the installed/requested version,
framework compatibility, and peer dependencies; read the diagnostics and
official migration notes; update usage deliberately. Every package addition or
version change runs `add-dependency` (version, license, peer-conflict, and
central-version rules live there and in `2-technology/package-management.md`).
Do not replace a package or add another merely to get green, do not delete
`package-lock.json` reflexively, do not fabricate replacement APIs from memory,
and do not combine an unrelated upgrade with the repair.

**Toolchain:** check `dotnet --info`, `dotnet --version`, `node --version`,
`npm --version`, `global.json`, target frameworks, and CI runtime versions. Do
not change the declared SDK, Node, framework, or language version because the
local machine differs; report an unavailable toolchain instead of editing code
to compensate.

## 4. Iteration Limits and Regressions

Use several focused attempts, not an unlimited loop. Stop and reassess when the
same root failure survives materially different fixes, fixes create growing
unrelated failures, the toolchain is incompatible, required infrastructure is
unavailable, package compatibility cannot be resolved safely, or correct
behavior cannot be determined. If a fix introduces new failures, keep it only
when they reveal a legitimate dependency; otherwise revert or correct it. Do not
leave the repository knowingly worse, and do not clean up unrelated
pre-existing failures unless they block verification or the user asks.

Behavior proven by a new diagnostic test or probe follows `verify`, step 4.

## 5. Complete and Report

The repair is complete when the affected scope is green (backend build,
frontend build, affected tests, consistent cross-stack contract, no known new
regression, no accidental workaround in the diff); do not require an unrelated
frontend build for a backend-only repair or vice versa. Then run `verify` for
the completion pass when appropriate.

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
