---
name: verify
description: >
  Use when finishing a change or preparing a PR: diff and scope, builds, tests, probe preservation, runtime smoke, risk-scoped checks, honest PASS/NOT RUN report.
---

> Level: 3 Project | Owns: verification procedure, behavioral-probe preservation, changed-file import hygiene, verification reporting | Scope: common | Loads: workflow skill (model-invoked; routed from `develop`) | Depends on: CLAUDE.md, 0-core/*, 1-architecture/*, 2-technology/*, 3-project/*

# Verify

Verification produces evidence that the requested change is complete and has
not introduced obvious regressions. It matches the scope and risk of the change
and does not require tooling the repository has not configured. It is not a
substitute for `code-review`.

## 1. Inspect the Change

Review the final changed-file set and diff before choosing checks. Confirm:

- the changes match the requested scope and contain no accidental unrelated
  refactoring;
- no generated or build artifacts, temporary diagnostics, secrets, or
  environment-specific credentials were added (remove any that were);
- which repository areas were affected: backend-only → affected .NET projects;
  frontend-only → the Angular application; contract or full-stack → both;
  documentation-only → no unrelated builds without a reason.

## 2. Build

Build the affected solution or projects (`dotnet build`, or a targeted
project/solution path); for Angular changes run the workspace's configured
build script (typically `npm run build`). Do not use `--no-restore` unless
restore is known to be complete. A build failure means the implementation is
not complete.

## 3. Run Relevant Tests

Run the tests covering the changed area (`dotnet test --no-build`; for Angular,
the test script that `package.json` actually defines). Small solutions run the
complete suite; large solutions run affected test projects first, then any
broader suite the repository or the change risk requires. Investigate every new
relevant failure — do not dismiss one as unrelated without checking it.

## 4. Preserve Behavioral Verification

If a temporary behavioral probe (ad-hoc HTTP request, curl or PowerShell
script, temporary test, manual database check) demonstrated that the change
works, represent that behavior in maintained automated tests before completion
unless equivalent coverage already exists; verify that the existing coverage
actually exercises it. The temporary mechanism itself need not remain, and it is
removed only after the behavior is preserved. Builds, compiler, formatter, and
static-analysis runs do not themselves require new tests.

## 5. Runtime Smoke (New or Recomposed Applications)

For a new runnable application or a substantial startup, configuration,
persistence, or full-stack change, verify the intended Development startup:
the API host starts; the Development endpoint is reachable; Swagger UI loads
when expected; required configuration binds; database connectivity and
initialization succeed; the frontend dev server starts; the frontend API base
URL and backend CORS configuration agree. A successful build alone does not
prove runtime composition. Behavior established here follows step 4.

## 6. Risk-Scoped Checks

Run these only when relevant to the change:

- **Architecture** — when boundaries are touched: project references, Api →
  Application flow, repository abstractions, persistence-framework boundary,
  Unit of Work (`1-architecture/` modules); `node .claude/scripts/check-manifests.cjs`
  checks reference direction mechanically. When a Domain or persistence change
  affects seeded entities, confirm the seeder is valid and representative for a
  freshly recreated Development database (`3-project/data-lifecycle.md`).
- **Formatting and analyzers** — when configured, e.g.
  `dotnet format --verify-no-changes`; do not add a formatter or analyzer just to
  complete verification. Analyzer output is evidence that still needs context.
- **Dependencies and security** — for dependency changes or security-sensitive
  work: `dotnet package list --vulnerable --include-transitive`, `npm audit`, and
  inspection of secrets, authorization, raw SQL, CORS/TLS, sensitive logging, and
  disabled certificate validation. A full `security-scan` is not needed for
  every small business-logic change.

## 7. Final Diff Review

After all fixes, review the final diff for: accidental edits, commented-out
code, temporary logging, unintended TODO/FIXME markers, stale temporary tests or
scripts, architecture drift, unapproved drift from `SPECIFICATION.md` or
`CUSTOM_SETTINGS.md`, stale code/tests/docs/config after a settings change, and
manually verified behavior never preserved as a test.

For every C# file created or modified by the task, remove unused or redundant
`using` directives (including imports already provided by implicit or global
usings, unless needed for clarity or disambiguation) and verify the changed
files rather than assuming tooling did it; do not run an unrelated
repository-wide using cleanup.

## Fix-and-Retry

When verification fails: identify the concrete failure, make the smallest
appropriate fix (use `build-fix` for non-trivial build or test repair), rerun
the affected checks, rerun build and tests when code changed, and repeat until
green or until genuine user input is required. Do not hide a known failure and
declare completion.

## Report

Report what was actually run; use `NOT RUN` or `NOT APPLICABLE` rather than
implying that an unchecked area passed.

```text
Backend build: PASS / NOT APPLICABLE
Frontend build: PASS / NOT APPLICABLE
Tests: PASS / NOT RUN / NOT APPLICABLE
Runtime smoke: PASS / NOT RUN / NOT APPLICABLE
Formatting/analyzers: PASS / NOT RUN
Security/dependency checks: PASS / NOT RUN / NOT APPLICABLE
Diff review: PASS
```
