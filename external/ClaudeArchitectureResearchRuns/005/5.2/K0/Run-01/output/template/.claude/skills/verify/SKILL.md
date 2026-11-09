---
name: verify
description: Use before declaring any implementation, fix or refactor complete, or before preparing a PR. Checks diff scope, builds, tests, runtime smoke, preserved behavioral tests, risk-scoped architecture/security/dependency checks, and reports actual results.
---
<!-- Kind: WF | Scope: common | Owns: completion verification procedure, behavioral-probe preservation, changed-file using cleanup, verification reporting | Loads: workflow invocation -->
# Verify Changes

Produce evidence that the requested change is complete and has not introduced obvious regressions. Match verification to the scope and risk of the change, and do not require tooling the repository has not configured. Verification proves required checks pass; `code-review` independently looks for defects that automated verification may miss.

## 1. Inspect the Change

**Must** first review the final changed-file set and diff, and confirm:

- changes match the requested scope; no unrelated refactoring slipped in;
- temporary diagnostics and probes are removed only after any behavior they uniquely verified is preserved as maintained test coverage (step 4);
- no generated or build artifacts were added accidentally;
- no secrets or environment-specific credentials were introduced (`rules/common/security.md`).

Then determine the affected areas before choosing checks: backend-only change → affected .NET projects; frontend-only → the Angular application; contract or full-stack change → both sides; documentation-only → no unrelated builds without a reason.

## 2. Build

**Must** build the affected solution or projects — typically `dotnet build` (or a targeted project/solution) and, for Angular, the configured build script, typically `npm run build`. Do not use `--no-restore` unless restore is known to be complete. A build failure means the implementation is not complete.

## 3. Run Relevant Tests

**Must** run tests covering the changed area — typically `dotnet test`; for Angular, the test script defined in `package.json` (inspect it rather than assuming a runner). For small solutions run the complete suite; for large ones run affected test projects first, then any broader suite the change risk requires. Investigate every newly failing relevant test; do not dismiss a failure as unrelated without checking it.

### Runtime Smoke Verification

**Default:** for a new runnable application or a substantial composition, startup, configuration, persistence or full-stack change, verify that the application starts with its intended Development configuration:

- the API host starts and the configured Development endpoint is reachable;
- Swagger UI loads when the API is expected to expose it; exercise representative endpoints through it when that is a meaningful behavioral check;
- required configuration binds; database connectivity and initialization succeed;
- the frontend development application starts; the frontend API base URL and backend CORS configuration are compatible.

A successful build alone does not prove runtime composition. Behavior established here and not yet covered by tests falls under step 4.

## 4. Preserve Behavioral Verification

- If an ad-hoc or manual behavioral probe uniquely demonstrated that the implementation works — temporary HTTP/curl/PowerShell requests or scripts, ad-hoc test methods, manual database checks, temporary regression probes — that behavior **must** be represented by maintained automated test coverage before completion, unless equivalent coverage already exists (then confirm the existing test really exercises it).
- The temporary mechanism itself need not remain: for example, an ad-hoc request becomes an NUnit integration test using `WebApplicationFactory`.
- Builds, compiler checks, static analysis, formatting and running an existing suite are verification activities that do not by themselves require new tests. Never declare completion on a behavioral check that exists only outside the maintained test suite.

## 5. Risk-Scoped Checks

**Must** run architecture, formatting/analyzer, dependency and security checks when relevant to the change, not indiscriminately:

- **Architecture** — when the change touches boundaries, read and check `rules/backend/architecture.md` and `rules/backend/persistence.md`: project references, Api → Application flow, repository abstractions, EF Core boundary, Unit of Work, and a valid representative development seeder for a freshly recreated database when the seeded model changed. `node .claude/scripts/check-manifests.mjs` checks project references and package manifests. No full architecture audit for documentation-only or unrelated changes.
- **Formatting and analyzers** — when configured, for example `dotnet format --verify-no-changes`. Do not add a formatter or analyzer dependency solely for ordinary verification; analyzer output is evidence that still needs context.
- **Dependencies and security** — for dependency changes or security-sensitive work: `dotnet package list --vulnerable --include-transitive` (when the SDK supports it), `npm audit`, and inspection of secrets, authorization, SQL/raw query safety, CORS/TLS changes, sensitive logging and disabled certificate validation. A full `security-scan` is not needed for every small business-logic change.

## 6. Final Diff Review

Review the final diff after all fixes for:

- accidental unrelated edits, commented-out code, temporary logging, unintended TODO/FIXME markers, stale temporary tests or scripts, architecture drift;
- unapproved drift from `SPECIFICATION.md` or `CUSTOM_SETTINGS.md`, and stale code, tests, docs or configuration after a settings change;
- behavior verified manually but never preserved as a test.

For every C# file created or modified by the task, **must** remove unused or redundant `using` directives — including imports already provided by implicit or global usings unless an explicit import is needed for clarity or disambiguation — without an unrelated repository-wide cleanup. Use compiler, analyzer, IDE or formatter support when available, but verify the changed files rather than assuming tooling removed every redundant import.

## Fix and Retry

When verification fails, **must** identify the concrete failure, make the smallest appropriate fix, and rerun the affected checks (and build/tests when code changed) until green or until genuine user input is required. **Never** hide a known failure and declare completion. Failures that need diagnosis: `build-fix`.

## Report

**Must** report what was actually run, using PASS / NOT RUN / NOT APPLICABLE, and never imply that an unchecked area passed:

    Backend build: PASS / NOT APPLICABLE
    Frontend build: PASS / NOT APPLICABLE
    Tests: PASS / NOT RUN / NOT APPLICABLE
    Runtime smoke: PASS / NOT RUN / NOT APPLICABLE
    Formatting/analyzers: PASS / NOT RUN
    Dependency/security checks: PASS / NOT RUN / NOT APPLICABLE
    Diff review: PASS
