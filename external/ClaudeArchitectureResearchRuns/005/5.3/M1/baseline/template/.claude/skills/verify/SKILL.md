---
name: verify
description: >
  Use before declaring implementation complete or preparing a PR: diff and
  scope review, builds, tests, probe preservation, smoke checks, architecture,
  dependency, security and delivery checks, reporting.
---

> Workflow · Owns the verification procedure and completion gates, behavioral-probe preservation, changed-file using cleanup, and delivery-pipeline checks

# Verify Changes

Before declaring implementation work complete, run this workflow at a depth
appropriate to the scope and risk of the change. Verification proves that the
required checks pass; `code-review` independently looks for defects that checks
may not detect. Do not require optional tooling the repository has not
configured.

## 1. Inspect the Change

Review the final changed-file set and diff before choosing checks. Confirm
that:

- the changes match the requested scope and no unrelated refactoring slipped in;
- temporary diagnostics and probes are removed only after any behavior they
  uniquely verified is preserved as maintained automated test coverage
  (step 4);
- no generated or build artifacts were added accidentally;
- no secrets or environment-specific credentials were introduced.

Determine the affected repository areas: backend-only → affected .NET
projects; frontend-only → the frontend workspace; contract or full-stack →
both; documentation-only → no unrelated builds without a reason.

## 2. Build

Build the affected solution or projects (for example `dotnet build`, or the
frontend's configured build script such as `npm run build`). Do not use
`--no-restore` unless restore is known to be complete. A build failure means
the implementation is not complete.

## 3. Run Relevant Tests

Run the tests covering the changed area (for example `dotnet test --no-build`,
and the frontend test script when `package.json` defines one — inspect
`package.json` rather than assuming a runner). For small solutions run the
complete suite; for large ones run affected test projects first, then any
broader suite the change risk requires. Investigate every newly failing
relevant test; do not dismiss a failure as unrelated without checking it.

## Runtime Smoke Verification

For a new runnable application, or for substantial startup, composition,
configuration, persistence, or full-stack changes, verify the intended
Development startup and key composition surfaces as applicable: the API host
starts; the Development endpoint is reachable; Swagger UI is reachable when
expected; required configuration binds; database connectivity and
initialization succeed; the frontend development server starts; the frontend
API base URL and backend CORS configuration are compatible. A successful build
alone does not prove runtime composition.

## 4. Preserve Behavioral Verification

If an ad-hoc or manual behavioral probe — a temporary HTTP request, curl or
PowerShell script, ad-hoc test, or manual database check — uniquely
demonstrated that the implementation works, preserve that behavior in
maintained automated test coverage before completion unless equivalent coverage
already exists (verify that the existing test really exercises it). The
temporary mechanism itself does not need to remain. Builds, compiler checks,
static analysis, formatting, and running existing suites do not by themselves
require new tests.

Steps 5–8 are risk-scoped: run each check when the change makes it relevant,
not indiscriminately.

## 5. Architecture Check

When the change touches architectural boundaries, verify the relevant rules in
`.claude/rules/architecture.md` (read it if it has not loaded): project
references, entry point → use-case flow, persistence-access contracts, the
persistence-technology boundary, commit-boundary behavior, and dependency
direction. Run the deterministic check:

```text
node .claude/scripts/check-architecture.js
```

When a model or persistence change affects seeded entities, confirm the
`persistence-change` workflow § Seed Data was applied. Skip the architecture
audit for documentation-only or unrelated changes.

## 6. Formatting and Static Analysis

If the repository configures formatting or analyzers, run them (for example
`dotnet format --verify-no-changes`). Do not add a formatter or analyzer
dependency solely to complete ordinary verification. Analyzer output is
evidence that still requires context.

## 7. Dependency and Security Verification

For dependency changes, run `node .claude/scripts/check-manifests.js` and the
vulnerability commands of `add-dependency` § Verify. For security-sensitive
work, inspect changed secrets handling, authorization, SQL/raw-query safety,
CORS/TLS changes, sensitive logging, and certificate validation. A full
`security-scan` is not required for every small business-logic change.

## 8. Delivery Changes

When CI/CD definitions, container files, or deployment configuration changed:

- CI definitions stay in source control, reproduce the repository's supported
  build and test commands, and must not hide build or test failures;
- frontend CI uses scripts that actually exist in `package.json` and installs
  with `npm ci` when a maintained lockfile supports it; do not invent npm
  scripts or reflexively replace the lockfile-based install;
- production database migrations are not applied automatically from normal
  application startup by default; production migration is an explicit
  deployment operation that uses approved credentials, and Development seeding
  never runs in Production.

## 9. Final Diff Review

Review the final diff after all fixes for: accidental unrelated edits;
commented-out code; temporary logging; unintended TODO/FIXME markers; stale
temporary tests or scripts; architecture drift; unapproved drift from
`SPECIFICATION.md` or `CUSTOM_SETTINGS.md`; stale code, tests, docs, or
configuration after a `CUSTOM_SETTINGS.md` change; behavior verified manually
but never preserved as a test.

For every C# file created or modified by the task, remove unused or redundant
`using` directives (including imports already provided by implicit/global
usings, unless needed for clarity or disambiguation). Verify the changed files
rather than assuming tooling removed them, and do not perform an unrelated
repository-wide using cleanup.

When instruction files changed, run `node .claude/scripts/check-instructions.js`.

## Fix-and-Retry

When verification fails:

1. identify the concrete failure;
2. make the smallest appropriate fix (`build-fix` for build or test failures);
3. re-run the affected verification, and re-run builds/tests when code changed;
4. repeat until green or until genuine user input is required.

Do not hide a known failure and declare completion.

## Reporting

Report what was actually run, using `PASS`, `NOT RUN`, or `NOT APPLICABLE`;
never imply that an unchecked area passed.

```text
Backend build: PASS / NOT APPLICABLE
Frontend build: PASS / NOT APPLICABLE
Tests: PASS / NOT RUN / NOT APPLICABLE
Formatting: PASS / NOT RUN
Architecture check: PASS / NOT RUN / NOT APPLICABLE
Security/dependency checks: ...
Diff review: PASS
Unresolved Decision Requests: none / <list>
```
