---
name: verify
description: Use before declaring any change finished — feature, bug fix, refactor, or PR preparation. Runs affected builds and tests, preserves behavioral probes as tests, runs risk-scoped architecture/format/dependency/security checks, reviews the final diff, reports PASS / NOT RUN / NOT APPLICABLE.
---

> Level: 0-core · Owns: completion verification procedure, probe-to-test preservation, changed-file import hygiene, verification reporting · Loading: on invocation

# Verify

Produce evidence that the requested change is complete and has not introduced obvious regressions, at the scope and risk of the change. Do not require optional tooling the repository has not configured. Verification proves required checks pass; `code-review` independently looks for defects automation misses.

## 1. Inspect the change

Review the final changed-file set and diff before choosing checks. Confirm that:

- changes match the requested scope and no unrelated refactoring slipped in;
- temporary diagnostics and probes are removed only after any behavior they uniquely verified is preserved as maintained automated tests (step 4);
- no generated/build artifacts were added accidentally;
- no secrets or environment-specific credentials were introduced.

Then determine the affected areas: backend-only → affected .NET projects; frontend-only → the frontend workspace; contract/full-stack → both sides; documentation-only → no unrelated builds.

## 2. Build

Build the affected solution or projects (`dotnet build`, or a targeted project/solution path); for frontend changes use the build command from `frontend.commands`. Do not use `--no-restore` unless restore is known to be complete. A build failure means the implementation is not complete.

## 3. Run relevant tests

Run tests covering the changed area (`backend-testing.commands`; frontend: the configured test script per `frontend.commands`). For small solutions run the full suite; for large ones run affected test projects first, then any broader suite the change risk requires. Investigate every newly failing relevant test — do not dismiss a failure as unrelated without checking it.

### Runtime smoke for new or recomposed applications

Default: for a new runnable application or substantial startup, configuration, persistence, or full-stack changes, verify that the application starts with its intended local Development configuration: the API host starts; the Development endpoint is reachable; the Development API documentation UI loads when the stack exposes one; required configuration binds; database connectivity and initialization succeed (`persistence.workflow` § Verification); the frontend development server starts; the frontend API base URL and backend CORS settings are compatible. A successful build alone does not prove runtime composition.

## 4. Preserve behavioral verification

If an ad-hoc or manual behavioral probe (temporary HTTP request, curl or PowerShell script, ad-hoc test method, manual database check, regression probe) uniquely demonstrated behavior, preserve that behavior in maintained automated tests before completion unless equivalent coverage already exists — for example, replace a curl call with a host integration test. The temporary mechanism itself need not remain. Builds, compiler, formatter, and static-analysis runs do not by themselves require new tests.

## 5. Architecture check

When the change touches architectural boundaries (project references, entry point → use-case flow, persistence-access contracts, persistence confinement, commit boundary, dependency direction), check the boundary rules under `.claude/rules/1-architecture/` and run `node "$(git rev-parse --show-toplevel)/.claude/scripts/check-architecture.mjs"` (`architecture.check`). When a domain or persistence change affects seeded entities, confirm the seed step of `persistence.workflow` was done. Skip the architecture audit for documentation-only or unrelated changes.

## 6. Formatting and static analysis

Run the repository's configured checks, for example `dotnet format --verify-no-changes`. Do not add a formatter or analyzer dependency just to complete ordinary verification. Treat analyzer output as evidence that still needs context.

## 7. Dependency and security checks

For dependency changes or security-sensitive work: `dotnet package list --vulnerable --include-transitive` (when the SDK supports it) and the frontend audit command from `frontend.commands`; inspect changes for secrets, authorization, raw SQL safety, CORS/TLS changes, sensitive logging, and disabled certificate validation. A full `security-scan` is not needed for every small business-logic change.

## 8. Final diff review

After all fixes, review the final diff for accidental unrelated edits, commented-out code, temporary logging, unintended TODO/FIXME markers, stale temporary tests or scripts, architecture drift, unapproved drift from `SPECIFICATION.md` or `CUSTOM_SETTINGS.md`, stale code/tests/docs/config after a settings change, and behavior verified manually but never preserved as a test.

For every C# file created or modified by the change, remove unused or redundant `using` directives (including imports already provided by implicit/global usings, unless needed for clarity or disambiguation); do not run an unrelated repository-wide cleanup. Verify the changed files rather than assuming tooling removed every redundant import.

## Fix and retry

When a check fails: identify the concrete failure, make the smallest appropriate fix, rerun the affected check (and build/tests when code changed), and repeat until green or until genuine user input is required. Use `build-fix` for non-trivial build/test repair. Never hide a known failure and declare completion.

## Report

Report what was actually run, using `NOT RUN` or `NOT APPLICABLE` rather than implying an unchecked area passed:

```text
Backend build: PASS / NOT APPLICABLE
Frontend build: PASS / NOT APPLICABLE
Tests: PASS / NOT RUN / NOT APPLICABLE
Runtime smoke: PASS / NOT RUN / NOT APPLICABLE
Architecture check: PASS / NOT RUN / NOT APPLICABLE
Formatting: PASS / NOT RUN
Security/dependency scan: PASS / NOT RUN / NOT APPLICABLE
Diff review: PASS
```
