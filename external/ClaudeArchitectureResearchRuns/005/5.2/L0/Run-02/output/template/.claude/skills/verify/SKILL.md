---
name: verify
description: >
  Run before declaring any implementation complete or preparing a PR: diff review,
  affected builds and tests, smoke and risk-scoped checks, PASS/NOT RUN report.
---

> Level: 3 Project · Owns: verification procedure, fix-and-retry loop, verification reporting (workflow) · Scope: common · Loads: on invocation · Depends on: CLAUDE.md, .claude/rules/** (owner reads)

# Verify

Produce evidence that the requested change is complete and has not introduced obvious regressions. Verification matches the scope and risk of the change; do not require optional tooling the repository has not configured. Verification is not code review: `code-review` independently looks for defects that checks cannot detect.

## 1. Inspect the change

Review the final changed-file set and diff before choosing checks. Confirm that:

- the changes match the requested scope and contain no accidental unrelated refactoring;
- no generated or build artifacts, secrets, or environment-specific credentials were added;
- temporary diagnostics and probes are removed only after any behavior they uniquely verified is preserved (step 4).

Determine the affected areas: backend-only → affected .NET projects; frontend-only → the Angular workspace; contract or full-stack change → both sides; documentation-only → no unrelated builds without a reason.

## 2. Build

- Backend: `dotnet build` on the solution or the affected projects (do not use `--no-restore` unless restore is known to be complete).
- Frontend: the workspace's configured build script, typically `npm run build` — inspect `package.json` first.
- A build failure means the implementation is not complete; repair it with `build-fix`.

## 3. Run relevant tests

- Backend: `dotnet test` for the affected test projects; for small solutions run the whole suite, for large ones run affected projects first and then any broader suite the change risk requires.
- Frontend: the configured test script, when the workspace has one.
- Investigate every newly failing relevant test; do not dismiss a failure as unrelated without checking it.

## Runtime smoke check

For a new runnable application or substantial startup, configuration, persistence, or full-stack changes, verify the intended Development startup and key composition surfaces, as applicable: the API host starts; the Development endpoint is reachable; Swagger UI loads when the API exposes it; required configuration binds; database connectivity and initialization succeed; the frontend dev server starts; the frontend API base URL and backend CORS configuration are compatible. A successful build alone does not prove runtime composition.

## 4. Preserve behavioral verification

If an ad-hoc or manual behavioral probe (temporary HTTP request, script, database check, ad-hoc test, smoke check) uniquely demonstrated behavior, preserve that behavior in maintained automated coverage before completion unless equivalent coverage already exists — for example replace an ad-hoc request with an NUnit `WebApplicationFactory` integration test. The temporary mechanism itself need not remain. Builds, compiler checks, analyzers, formatting, and running the existing suite do not by themselves require new tests.

## 5. Risk-scoped checks

Run these when relevant to the change rather than indiscriminately:

- **Architecture** — when the change touches boundaries, re-read and check the owning rules: project references and dependency direction (`1-architecture/backend-layers.md`), repository and Unit of Work boundary (`persistence-boundary.md`), entry points (`entry-points.md`). When a Domain or persistence change affects seeded entities, confirm the seeder was updated and stays valid for a freshly recreated Development database (`3-project/data-lifecycle.md`) and that new migrations were reviewed (`development-workflow` → Co-changes).
- **Formatting and analyzers** — when configured, for example `dotnet format --verify-no-changes`; do not add a formatter or analyzer dependency just to verify. Analyzer output is evidence that still needs context.
- **Dependencies and security** — for dependency changes or security-sensitive work: `dotnet package list --vulnerable --include-transitive`, `npm audit`, and inspection of secrets, authorization, raw SQL, CORS/TLS, sensitive logging, and certificate validation (`0-core/security-principles.md`). A full `security-scan` is not needed for every small change.

## 6. Final diff review

After all fixes, review the final diff again for: accidental unrelated edits; commented-out code; temporary logging; unintended TODO/FIXME markers; stale temporary tests or scripts; architecture drift; unapproved drift from `SPECIFICATION.md` or `CUSTOM_SETTINGS.md`; stale code, tests, docs, or configuration after a `CUSTOM_SETTINGS.md` change; behavior verified manually but never preserved as a test.

For every C# file created or modified by the task, remove unused or redundant `using` directives (including imports already provided by implicit/global usings, unless needed for clarity or disambiguation). Verify the changed files themselves rather than assuming tooling did it, and do not perform an unrelated repository-wide cleanup.

## Fix and retry

When verification fails: identify the concrete failure, make the smallest appropriate fix, re-run the affected verification (and build/tests when code changed), and repeat until green or genuine user input is required. Never hide a known failure and declare completion.

## Report

Report only what was actually run:

```text
Backend build: PASS / NOT APPLICABLE
Frontend build: PASS / NOT APPLICABLE
Tests: PASS / NOT RUN / NOT APPLICABLE
Runtime smoke: PASS / NOT RUN / NOT APPLICABLE
Formatting/analyzers: PASS / NOT RUN
Security/dependency checks: PASS / NOT RUN / NOT APPLICABLE
Diff review: PASS
```

Use `NOT RUN` or `NOT APPLICABLE` rather than implying that an unchecked area passed.
