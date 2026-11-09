---
name: verify
description: >
  Use before declaring any feature, fix, refactor, or scaffolding complete, or
  before a PR. Scoped completion procedure: diff review, builds, tests,
  runtime smoke, probe preservation, architecture/dependency/security checks,
  PASS / NOT RUN report.
---

> Owner: completion verification procedure, its stop conditions, and its report | Scope: common | Loads: on demand — workflow (required by `CLAUDE.md` § Development Workflow) | Enforced: `.claude/scripts/check-architecture.mjs`, `.claude/scripts/check-dependencies.mjs`, Stop hook co-change reminders

# Verify Changes

## Goal

Produce evidence that the requested change is complete and introduced no obvious
regressions, at a depth that matches its scope and risk. Do not require optional
tooling the repository has not configured. Verification proves that required
checks pass; `code-review` separately looks for defects that checks miss.

## 1. Inspect the Change

Review the final changed-file set and diff before choosing checks:

- changes match the requested scope; no accidental unrelated refactoring;
- no generated or build artifacts were added by accident;
- no secrets or environment-specific credentials were introduced
  (`.claude/rules/security.md` § Secrets);
- temporary diagnostics and probes are removed only after any behavior they
  uniquely verified is preserved in maintained tests (step 4).

Then determine the affected areas: backend-only → affected .NET projects;
frontend-only → the Angular workspace; contract or full-stack → both sides;
documentation-only → no unrelated builds.

## 2. Build

Build the affected solution or projects, for example `dotnet build` (or a
targeted project or `.slnx`) and the frontend's configured build script,
typically `npm run build`. Avoid `--no-restore` unless restore is known to be
complete. A build failure means the implementation is not complete.

## 3. Run Relevant Tests

Run the tests covering the changed area, for example `dotnet test --no-build`,
and the frontend test script when `package.json` defines one (inspect it rather
than assuming a runner). For small solutions run the whole suite; for large ones
run affected test projects first, then whatever broader suite the change risk
requires. Investigate every newly failing relevant test; do not dismiss a failure
as unrelated without checking it.

## Runtime Smoke Verification

Default for a new runnable application or a substantial startup, composition,
configuration, persistence, or full-stack change: verify that the application
starts with its intended local Development configuration. As applicable:

- the API host starts and the Development endpoint is reachable;
- Swagger UI is reachable when the API exposes it;
- required configuration binds and database connectivity/initialization succeeds;
- the frontend development server starts, and its API base URL is compatible with
  the backend CORS configuration.

A successful build alone does not prove runtime composition.

## 4. Preserve Behavioral Verification

Read `.claude/rules/testing.md` § Regression and Behavioral Verification and
check:

- Did a temporary probe (curl, PowerShell, HTTP file, database query, throwaway
  test) establish behavior that no maintained test covers? Then add the test now.
- Is this a meaningful bug fix with plausible recurrence and no regression test?

## 5. Architecture and Persistence Check

When the change touches boundaries, run:

```bash
node .claude/scripts/check-architecture.mjs
```

and, because path rules may not have loaded for every changed file, read the
owners for the touched areas and confirm:

- project references and layer flow follow `.claude/rules/architecture.md`;
- Unit of Work, EF Core boundary, seeding, and migrations follow
  `.claude/rules/persistence.md` — in particular, when a Domain or persistence
  change affects seeded entities, the seeder was updated in the same change and a
  freshly recreated Development database still seeds validly, and any new
  migration was reviewed;
- HTTP behavior follows `.claude/rules/api.md` and
  `.claude/rules/error-handling.md`;
- a performance-motivated change followed `.claude/rules/performance.md`
  § Performance Changes;
- Angular changes follow `.claude/rules/angular.md`.

Skip the architecture audit for documentation-only or unrelated changes.

## 6. Formatting and Static Analysis

When the repository configures formatting or analyzers, run them, for example
`dotnet format --verify-no-changes`. For C# files created or modified by the
change, confirm `.claude/rules/coding-style.md` § Using Directives, for example:

```bash
dotnet format style --diagnostics IDE0005 --severity info --verify-no-changes --include <changed files>
```

(Command-line IDE0005 reporting can require
`<GenerateDocumentationFile>true</GenerateDocumentationFile>`; otherwise inspect
the changed files directly.) Do not add a formatter or analyzer dependency just to finish ordinary
verification. Treat analyzer output as evidence that still needs context.

## 7. Dependency, Security, and Delivery Checks

Run these when relevant to the change, not indiscriminately:

- dependency changes: `node .claude/scripts/check-dependencies.mjs`,
  `dotnet package list --vulnerable --include-transitive`, `npm audit`, and the
  `add-dependency` output for each package;
- security-sensitive changes: read `.claude/rules/security.md` and check secrets,
  authorization, SQL/raw query safety, CORS/TLS changes, sensitive logging, and
  disabled certificate validation; a full `security-scan` only when the change is
  materially security-sensitive or a finding justifies it;
- CI or container changes: read `.claude/rules/delivery.md` and confirm the
  pipeline uses existing commands and scripts and keeps failures visible;
- `CUSTOM_SETTINGS.md` changes: complete the `custom-settings` verification.

## 8. Final Diff Review

After all fixes, review the final diff once more for:

- accidental unrelated edits, commented-out code, temporary logging, stale
  temporary tests or scripts, unintended TODO/FIXME markers;
- architecture drift;
- unapproved drift from `SPECIFICATION.md` or `CUSTOM_SETTINGS.md`
  (`CLAUDE.md` § Product Sources), and stale code, tests, docs, or config after a
  settings change;
- unused or redundant `using` directives in changed C# files;
- behavior verified manually but never preserved as a test.

## Fix-and-Retry

When verification fails:

1. identify the concrete failure;
2. make the smallest appropriate fix;
3. re-run the affected verification, and builds/tests when the fix changed code;
4. repeat until green or until genuine user input is required.

Never hide a known failure and declare completion. If the failure is a broken
build or test that needs diagnosis, switch to the `build-fix` workflow.

## Reporting

Report only what was actually run; never imply that an unchecked area passed:

```text
Backend build:              PASS / NOT RUN / NOT APPLICABLE
Frontend build:             PASS / NOT RUN / NOT APPLICABLE
Tests:                      PASS / NOT RUN / NOT APPLICABLE
Runtime smoke:              PASS / NOT RUN / NOT APPLICABLE
Architecture/persistence:   PASS / NOT RUN / NOT APPLICABLE
Formatting/analyzers:       PASS / NOT RUN / NOT APPLICABLE
Dependency/security:        PASS / NOT RUN / NOT APPLICABLE
Diff review:                PASS
Open Decision Requests:     none / <list>
```
