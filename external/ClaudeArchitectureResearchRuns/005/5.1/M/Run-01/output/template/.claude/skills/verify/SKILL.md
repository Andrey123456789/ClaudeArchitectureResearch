---
name: verify
description: >
  Run before declaring any implementation, bug fix, refactor, or PR complete.
  Inspects the final diff, builds and tests affected areas, preserves behavioral
  probes as tests, runs risk-scoped architecture/format/dependency/security
  checks, and reports PASS / NOT RUN / NOT APPLICABLE.
---

> Owns: completion verification procedure, probe-to-test preservation, regression-coverage check, verification reporting | Scope: common | Loads: workflow (mandatory before completion per CLAUDE.md)

# Verify Changes

Produce evidence that the requested change is complete and introduced no obvious
regressions. Match verification to the scope and risk of the change; do not
require optional tooling the repository has not configured. Verification is not
a substitute for `code-review`.

## 1. Inspect the Change

Review the final changed-file set and diff before choosing any check. Confirm:

- changes match the requested scope and contain no accidental unrelated
  refactoring;
- no generated/build artifacts were added accidentally;
- no secrets or environment-specific credentials were introduced (`security.md`);
- temporary diagnostics and probes are removed only after step 4 is satisfied.

Then determine the affected areas: backend-only → affected .NET projects;
frontend-only → the Angular application; contract/full-stack → both;
documentation-only → no unrelated builds without a reason.

## 2. Build

Build the affected solution or projects (for example `dotnet build`, or the
frontend's configured script such as `npm run build`). Use targeted commands
when appropriate; do not use `--no-restore` unless restore is known to be
complete. A build failure means the implementation is not complete — repair it
with `build-fix`.

## 3. Run Relevant Tests

Run tests covering the changed area (for example `dotnet test --no-build`; for
Angular, the test script actually defined in `package.json`). For small
solutions run the complete suite; for large ones run affected projects first,
then any broader suite the risk requires. Investigate every newly failing
relevant test; do not dismiss a failure as unrelated without checking it.

### Runtime smoke check

For a new runnable application or substantial startup, configuration,
persistence, or full-stack composition changes, verify by default that the
intended Development configuration actually starts: API host starts and its
Development endpoint is reachable; Swagger UI loads when expected; required
configuration binds; database connectivity/initialization succeeds; the
frontend development server starts; frontend API base URL and backend CORS are
compatible. A successful build alone does not prove composition.

## 4. Preserve Behavioral Verification

- If an ad-hoc or manual behavioral probe (temporary HTTP/curl/PowerShell
  request, script, database check, throwaway test, or regression probe)
  uniquely demonstrated that the behavior works, that behavior must be
  represented by maintained automated test coverage before completion, unless
  equivalent coverage already exists (confirm that the existing test actually
  exercises it). The temporary mechanism itself need not remain.
- For a meaningful bug with plausible recurrence, add a regression test by
  default unless equivalent coverage already exists.
- Builds, compiler, formatter, and static-analysis runs do not by themselves
  require new tests.

## 5. Architecture Check

When the change touches architectural boundaries, read and check against
`.claude/rules/architecture.md` (project references, Api → Application flow,
repository abstractions, EF Core boundary, Unit of Work). When Domain or
persistence changes affect seeded entities or add migrations, read and check
`.claude/rules/persistence.md`. Run `node .claude/scripts/check-manifests.mjs`
when project or package manifests changed. Skip a full architecture audit for
documentation-only or unrelated changes.

## 6. Formatting and Static Analysis

If the repository configures formatting or analyzers, run them (for example
`dotnet format --verify-no-changes`). Do not add a formatter/analyzer dependency
solely to complete ordinary verification. Analyzer output is evidence that
still needs context.

## 7. Dependency and Security Checks

For dependency changes or security-sensitive work, inspect vulnerabilities (for
example `dotnet package list --vulnerable --include-transitive`, `npm audit`)
and check changed code against `.claude/rules/security.md` (secrets,
authorization, raw SQL, CORS/TLS, sensitive logging, certificate validation).
Use `security-scan` only when the risk justifies it.

## 8. Final Diff Review

After all fixes, review the final diff once more:

- [ ] no accidental unrelated edits, commented-out code, temporary logging,
      unintended TODO/FIXME markers, or stale temporary tests/scripts;
- [ ] no architecture drift (rules above);
- [ ] no unapproved drift from `SPECIFICATION.md` or `CUSTOM_SETTINGS.md`, and no
      stale code/tests/docs/config after a settings change (`CLAUDE.md`,
      Product Sources; `custom-settings`);
- [ ] changed C# files have clean `using` directives (`coding-style.md`);
- [ ] no behavior verified only manually (step 4).

## Fix-and-Retry

When a check fails: identify the concrete failure, make the smallest appropriate
fix, rerun the affected check (and build/tests when code changed), and repeat
until green or until genuine user input is required. Never hide a known failure
and declare completion.

## Report

Report only what was actually run:

```text
Backend build: PASS / NOT APPLICABLE
Frontend build: PASS / NOT APPLICABLE
Tests: PASS / NOT RUN / NOT APPLICABLE
Runtime smoke: PASS / NOT RUN / NOT APPLICABLE
Formatting/analyzers: PASS / NOT RUN
Dependency/security checks: PASS / NOT RUN / NOT APPLICABLE
Diff review: PASS
Open Decision Requests: none / <list>
```

Use `NOT RUN` or `NOT APPLICABLE` rather than implying an unchecked area passed.
