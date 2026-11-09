---
name: verify
description: >
  Run before declaring any implementation, bug fix, refactor, or PR complete:
  diff and scope, builds, tests, runtime smoke, probe preservation, relevant
  checks, honest PASS/NOT RUN report.
---

> **Workflow skill** · Owns: completion verification procedure, behavioral-probe preservation, changed-file import hygiene, verification reporting · Scope: common · Loading: on demand (routed from `development-workflow`)

# Verify Changes

## Goal

Produce evidence that the requested change is complete and has not introduced
obvious regressions.

Verification should match the scope and risk of the change.

Do not require optional tooling that the repository has not configured.

Verification is not a substitute for code review: it proves that required checks
pass; `code-review` independently looks for defects that automated verification
may not detect.

## 1. Inspect the Change

Review the final changed-file set and diff.

Confirm:

- changes match the requested scope;
- unrelated refactoring was not introduced accidentally;
- temporary diagnostics and probes are removed only after any behavior they
  uniquely verified has been preserved as maintained automated test coverage;
- no generated/build artifacts were accidentally added;
- no secrets or environment-specific credentials were introduced.

Determine which parts of the repository were affected before choosing
verification commands.

For example:

- backend-only change → verify affected .NET projects;
- frontend-only change → verify the frontend application;
- contract/full-stack change → verify both sides;
- documentation-only change → do not run unrelated builds without a reason.

## 2. Build

Build the affected solution or projects.

Typical command:

```bash
dotnet build
```

For frontend changes, run the frontend's configured build command, typically:

```bash
npm run build
```

Use a more targeted project/solution command when appropriate.

Do not use `--no-restore` unless restore is already known to be complete.

A build failure means the implementation is not complete.

## 3. Run Relevant Tests

Run tests covering the changed area.

Typical command:

```bash
dotnet test --no-build
```

For frontend changes, run the relevant frontend test command when the project
has one configured.

Inspect `package.json` rather than assuming a particular test runner or command.

Frontend test commands and conventions: the frontend knowledge facet (see
`docs/capability-selection.md`).

For small solutions, running the complete suite is appropriate.

For large solutions, affected test projects may be run first, followed by any
broader suite required by the repository or change risk.

Any newly failing relevant test must be investigated.

Do not ignore a failure merely because it appears unrelated without checking it.

## Runtime Smoke Verification for New Applications

When creating a new runnable application or making substantial composition,
startup, configuration, persistence, or full-stack changes, verify that the
application can actually start with its intended local Development configuration.

As applicable, verify:

- the API host starts successfully;
- the configured Development endpoint is reachable;
- Swagger UI is reachable when the API is expected to expose Swagger;
- required configuration binds successfully;
- database connectivity/initialization succeeds;
- the frontend development application can start;
- frontend API base URL and backend CORS configuration are compatible.

A successful build alone does not prove runtime composition is valid.

If this runtime check establishes behavior not already covered by maintained
automated tests, preserve it as described in step 4.

## 4. Preserve Behavioral Verification

If an ad-hoc or manual behavioral probe uniquely demonstrated that the
implementation works — for example temporary curl, PowerShell, or HTTP requests,
temporary scripts exercising application behavior, ad-hoc test methods, manual
database checks, or temporary regression probes — preserve that behavior in
maintained automated test coverage before completion, unless equivalent coverage
already exists. When relying on existing coverage, confirm that the existing test
actually exercises the behavior.

The permanent test need not keep the temporary mechanism; for example, an ad-hoc
HTTP request may become an integration test using `WebApplicationFactory`.

Build, compiler, formatter, and static-analysis commands, and running an existing
test suite, are verification activities that do not themselves require new tests.

Do not declare an implementation complete based on a behavioral check that exists
only outside the maintained automated test suite.

## 5. Architecture Check

When the change touches architectural boundaries, verify the relevant
`architecture-style.md` and `persistence-technology.md` rules, and run:

```bash
node .claude/scripts/check-architecture.mjs
```

Examples:

- project references;
- API → Application flow;
- repository abstractions;
- persistence-technology boundary;
- Unit of Work behavior;
- dependency direction;
- development seed-data consistency when model changes affect seeded entities.

When a Domain or persistence change affects the development seed graph, verify
that the development seeder remains valid and representative for a freshly
recreated Development database (`development-workflow` → Change-Specific
Obligations).

Do not perform a full architecture audit for a documentation-only or unrelated
change.

## 6. Formatting and Static Analysis

If the repository configures formatting or analyzers, run the appropriate checks.

For example:

```bash
dotnet format --verify-no-changes
```

Do not add a formatter/analyzer dependency solely in order to complete ordinary
verification unless requested.

Treat analyzer output as evidence that still requires context.

## 7. Dependency and Security Verification

For dependency changes or security-sensitive work, inspect package
vulnerabilities and changed security behavior.

For example, when supported by the installed SDK:

```bash
dotnet package list --vulnerable --include-transitive
node .claude/scripts/check-dependencies.mjs
```

Also inspect relevant changes for:

- secrets;
- authorization;
- SQL/raw query safety;
- CORS/TLS changes;
- sensitive logging;
- disabled certificate validation.

A full security scan is not necessary for every small business-logic change.

## 8. Final Diff Review

Review the final diff after all fixes.

Check for:

- accidental unrelated edits;
- commented-out code;
- temporary logging;
- TODO/FIXME markers introduced unintentionally;
- stale temporary tests or scripts;
- architecture drift;
- unapproved drift from `SPECIFICATION.md` or `CUSTOM_SETTINGS.md`;
- stale code/tests/docs/config after a `CUSTOM_SETTINGS.md` change;
- `using` directives in every C# file created or modified by the task: remove
  unused or redundant directives, including imports already provided by
  implicit/global usings unless an explicit import is needed for clarity or
  disambiguation; do not perform an unrelated repository-wide using cleanup. Use
  compiler/analyzer/IDE support (for example IDE0005 with `dotnet format`) when
  available, but verify the changed files rather than assuming the tooling
  removed every redundant import;
- behavior that was verified manually but never preserved as a test;
- instruction-system changes (`CLAUDE.md`, `docs/`, `.claude/`): run
  `node .claude/scripts/check-instructions.mjs`.

## Fix-and-Retry

When verification fails:

1. Identify the concrete failure.
2. Make the smallest appropriate fix.
3. Re-run the affected verification.
4. Re-run build/tests when the fix changed code.
5. Repeat until the change is green or user input is required.

Do not hide a known failure and declare completion.

## Reporting

Report what was actually run.

Example:

```text
Backend build: PASS / NOT APPLICABLE
Frontend build: PASS / NOT APPLICABLE
Tests: PASS / NOT RUN / NOT APPLICABLE
Formatting: PASS / NOT RUN
Security/dependency scan: ...
Diff review: PASS
```

Use `NOT RUN` or `NOT APPLICABLE` rather than pretending an unchecked area passed.
