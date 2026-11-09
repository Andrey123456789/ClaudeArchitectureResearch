---
name: verify
description: >
  Use before declaring a .NET/Angular change complete or preparing a PR: diff
  and scope review, builds, tests, probe-to-test preservation, smoke and
  risk-scoped checks, fix-and-retry, PASS/NOT RUN report.
---

> Owns: verification procedure, completion evidence, verification reporting | Scope: common | Loads: workflow (routed from CLAUDE.md and development-workflow)

# Verify Changes

## Goal

Produce evidence that the requested change is complete and has not introduced
obvious regressions. Match verification to the scope and risk of the change, and
do not require optional tooling the repository has not configured.

Verification does not replace review: it proves that required checks pass;
`code-review` independently looks for defects automation may miss.

## 1. Inspect the Change

Review the final changed-file set and diff before choosing any checks. Confirm:

- changes match the requested scope and no unrelated refactoring slipped in;
- no generated or build artifacts were added accidentally;
- no secrets or environment-specific credentials were introduced;
- temporary diagnostics and probes are removed only after step 4 preserved any
  behavior they uniquely verified.

Determine the affected repository areas, then choose checks:

- backend-only change → affected .NET projects;
- frontend-only change → the Angular application;
- contract or full-stack change → both sides;
- documentation-only change → no unrelated builds without a reason.

## 2. Build

Build the affected solution or projects, typically:

```bash
dotnet build
```

For Angular changes, run the frontend's configured build command, typically
`npm run build`. Use a more targeted project or solution command when
appropriate, and do not use `--no-restore` unless restore is known to be
complete. A build failure means the implementation is not complete.

## 3. Run Relevant Tests

Run the tests covering the changed area, typically:

```bash
dotnet test --no-build
```

For Angular changes, run the test command configured in `package.json` —
inspect it rather than assuming a runner. For small solutions run the complete
suite; for large solutions run affected test projects first, then any broader
suite the repository or change risk requires.

Investigate every newly failing relevant test; do not dismiss a failure as
unrelated without checking it.

## Runtime Smoke Verification

For a new runnable application, or a substantial composition, startup,
configuration, persistence, or full-stack change, verify that the application
starts with its intended local Development configuration. As applicable:

- the API host starts and the configured Development endpoint is reachable;
- Swagger UI loads when the API is expected to expose it;
- required configuration binds;
- database connectivity and initialization succeed;
- the frontend development application starts;
- the frontend API base URL and backend CORS configuration are compatible.

A successful build alone does not prove runtime composition.

API behavior change: when a change alters API behavior and the project exposes
the Development Swagger UI in Development, also start the API in Development,
open the Development Swagger UI and confirm it loads, even when startup and
composition did not change. The step does not apply when the project exposes no
such UI. If the application cannot run in this environment, report the check as
NOT RUN with the reason; never report it as passed.

## 4. Preserve Behavioral Verification

If an ad-hoc or manual behavioral probe uniquely demonstrated that the
implementation works — a temporary curl/PowerShell/HTTP request, a temporary
script, an ad-hoc test method, a manual database check, a temporary regression
probe — represent that behavior in maintained automated test coverage before
completion, unless equivalent coverage already exists (confirm that the
existing test really exercises the behavior). The probe mechanism itself does
not need to remain; an ad-hoc request can become an NUnit
`WebApplicationFactory` test.

Builds, compiler, formatter, and static-analysis runs, and runs of the existing
test suite, do not by themselves require new tests.

## Risk-Scoped Checks (steps 5–7)

Run architecture, formatting/analyzer, dependency, and security checks when they
are relevant to the change, not indiscriminately.

## 5. Architecture Check

When the change touches architectural boundaries, read
`.claude/rules/architecture.md` (and `.claude/rules/persistence.md` for
persistence changes) and check project references, API → Application flow,
repository abstractions, the EF Core boundary, Unit of Work behavior, and
dependency direction. When project files changed, run from the repository root
— the top level of the current checkout or worktree, printed by
`git rev-parse --show-toplevel`; change to it first if the shell is elsewhere:

```bash
node .claude/scripts/check-manifests.mjs
```

When a Domain or persistence change affects the development seed graph, confirm
that `DbSeeder` remains valid and representative for a freshly recreated
Development database. Skip this step for documentation-only or unrelated
changes.

## 6. Formatting and Static Analysis

If the repository configures formatting or analyzers, run them, for example:

```bash
dotnet format --verify-no-changes
```

Do not add a formatter or analyzer dependency solely to complete ordinary
verification. Treat analyzer output as evidence that still needs context.

## 7. Dependency and Security Verification

For dependency changes or security-sensitive work, inspect package
vulnerabilities, for example `dotnet package list --vulnerable
--include-transitive` and `npm audit`, and inspect changed secrets,
authorization, SQL/raw query safety, CORS/TLS settings, sensitive logging, and
certificate validation. A full `security-scan` is not necessary for every small
business-logic change.

## 8. Final Diff Review

Review the final diff after all fixes. Check for:

- accidental unrelated edits, commented-out code, temporary logging,
  unintentional TODO/FIXME markers, stale temporary tests or scripts;
- architecture drift;
- unapproved drift from `SPECIFICATION.md` or `CUSTOM_SETTINGS.md`, and stale
  code, tests, docs, or configuration after a `CUSTOM_SETTINGS.md` change;
- behavior that was verified manually but never preserved as a test.

Before completion, remove unused or redundant `using` directives from every C#
file created or modified by the task — including imports already provided by
implicit or global usings, unless an explicit import is needed for clarity or
disambiguation. Do not turn this into an unrelated repository-wide cleanup, and
verify the changed files rather than assuming tooling removed every redundant
import.

## Fix-and-Retry

When verification fails:

1. Identify the concrete failure.
2. Make the smallest appropriate fix.
3. Rerun the affected verification.
4. Rerun build and tests when the fix changed code.
5. Repeat until the change is green or genuine user input is required.

Never hide a known failure and declare completion. Failures that need
diagnosis go through `build-fix`.

## Reporting

Report what was actually run, for example:

```text
Backend build: PASS / NOT APPLICABLE
Frontend build: PASS / NOT APPLICABLE
Tests: PASS / NOT RUN / NOT APPLICABLE
Formatting: PASS / NOT RUN
Security/dependency scan: ...
Diff review: PASS
```

Use `NOT RUN` or `NOT APPLICABLE` instead of implying that an unchecked area
passed.
