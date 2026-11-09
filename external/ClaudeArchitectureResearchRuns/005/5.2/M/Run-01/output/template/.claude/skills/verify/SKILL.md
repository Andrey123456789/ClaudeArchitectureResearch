---
name: verify
description: >
  Use before declaring any change complete: diff review, build, tests,
  behavioral-probe preservation, risk-scoped architecture/dependency/security
  checks, PASS / NOT RUN reporting.
---

> Workflow skill. Owns: completion verification — diff and scope inspection, build and test, runtime smoke checks, preservation of behavioral probes, risk-scoped checks, changed-file import hygiene, fix-and-retry, verification reporting · Scope: common · Loads: on invocation, required by development-workflow · Depends on: CLAUDE.md, .claude/rules/

# Verify Changes

Produce evidence that the requested change is complete and has not introduced
obvious regressions. Match verification to the scope and risk of the change,
and do not require optional tooling the repository has not configured.

Verification proves that required checks pass; it does not replace
`code-review`, which looks for defects automated checks may miss.

## 1. Inspect the Change

Review the final changed-file set and diff before choosing checks. Confirm:

- the changes match the requested scope and no unrelated refactoring slipped
  in;
- temporary diagnostics and probes are removed only after any behavior they
  uniquely verified is preserved (step 4);
- no generated or build artifacts were added accidentally;
- no secrets or environment-specific credentials were introduced.

Determine the affected areas before choosing commands: backend-only → affected
.NET projects; frontend-only → the Angular application; contract or full-stack
→ both sides; documentation-only → no unrelated builds. Read the rule files for
the affected areas (CLAUDE.md, Workflows) when they are not already in context.

## 2. Build

Build the affected solution or projects, for example `dotnet build` (or a
targeted project command) and the frontend's configured build script, for
example `npm run build`. Do not use `--no-restore` unless restore is known to be
complete. A build failure means the implementation is not complete.

## 3. Run Relevant Tests

Run the tests covering the changed area, for example `dotnet test --no-build`
and the frontend test script defined in `package.json` (inspect it rather than
assuming a runner). For small solutions run the full suite; for large ones run
affected test projects first, then any broader suite the risk requires.
Investigate every newly failing relevant test; do not dismiss a failure as
unrelated without checking it.

## Runtime Smoke Check

Default: for a new runnable application or substantial startup, configuration,
persistence, or full-stack changes, verify that the application starts with its
intended local Development configuration. As applicable: the API host starts;
the Development endpoint is reachable; Swagger UI loads when expected; required
configuration binds; database connectivity and initialization succeed; the
frontend development server starts; the frontend API base URL and backend CORS
configuration are compatible. A successful build alone does not prove runtime
composition.

## 4. Preserve Behavioral Verification

If an ad-hoc or manual behavioral probe — a temporary HTTP request, PowerShell
or shell script, ad-hoc test method, manual database check, or temporary
regression probe — uniquely demonstrated that the implementation works, that
behavior must be represented by maintained automated test coverage before
completion, unless equivalent coverage already exists (confirm the existing
test actually exercises it). The maintained test need not keep the probe's
mechanism; for example an ad-hoc `curl` call becomes a `WebApplicationFactory`
integration test. Builds, compiler, analyzer, and formatter runs, and runs of
the existing suite, do not by themselves require new tests.

## 5. Risk-Scoped Checks

Run architecture, formatting/analyzer, dependency, and security checks when
they are relevant to the change, not indiscriminately.

- **Architecture boundaries touched:** run
  `node .claude/scripts/check-architecture.mjs`, then check by reference:
  - [ ] project references and layer boundaries — `architecture.md`;
  - [ ] repositories, Unit of Work, EF Core boundary — `persistence.md`;
  - [ ] the seeder is still valid and representative for a freshly recreated
    Development database when seeded entities changed — `development-workflow`
    (Seed data).
- **Manifests or dependencies changed:** run
  `node .claude/scripts/check-manifests.mjs`; for dependency changes also
  inspect vulnerabilities, for example
  `dotnet package list --vulnerable --include-transitive` or `npm audit`.
- **Security-sensitive change:** inspect secrets, authorization, raw SQL, CORS
  and TLS changes, sensitive logging, and disabled certificate validation —
  `security.md`. A full audit (`security-scan`) is not needed for every small
  change.
- **Instruction files changed:** run `node .claude/scripts/check-instructions.mjs`.

## 6. Formatting and Static Analysis

When the repository configures formatting or analyzers, run them, for example
`dotnet format --verify-no-changes`. Do not add a formatter or analyzer
dependency solely to complete ordinary verification. Treat analyzer output as
evidence that still needs context.

## 7. Final Diff Review

After all fixes, review the final diff for: accidental unrelated edits;
commented-out code; temporary logging; unintended TODO/FIXME markers; stale
temporary tests or scripts; architecture drift; unapproved drift from
`SPECIFICATION.md` or `CUSTOM_SETTINGS.md`; stale code, tests, docs, or
configuration after a `CUSTOM_SETTINGS.md` change; behavior verified manually
but never preserved as a test.

For every C# file created or modified by the task, remove unused or redundant
`using` directives, including imports already provided by implicit or global
usings unless an explicit import is needed for clarity or disambiguation. Do not
perform an unrelated repository-wide cleanup. Use compiler, IDE, or formatter
support when available, but verify the changed files rather than assuming the
tooling removed every redundant import.

## Fix-and-Retry

When verification fails:

1. identify the concrete failure;
2. make the smallest appropriate fix (use `build-fix` for a broken build or
   failing tests);
3. rerun the affected verification, and rerun build and tests when the fix
   changed code;
4. repeat until the change is green or genuine user input is required.

Do not hide a known failure and declare completion.

## Reporting

Report what was actually run:

```text
Backend build: PASS / NOT APPLICABLE
Frontend build: PASS / NOT APPLICABLE
Tests: PASS / NOT RUN / NOT APPLICABLE
Runtime smoke: PASS / NOT RUN / NOT APPLICABLE
Architecture/dependency checks: PASS / NOT RUN / NOT APPLICABLE
Formatting: PASS / NOT RUN
Security/dependency scan: PASS / NOT RUN / NOT APPLICABLE
Diff review: PASS
```

Use `NOT RUN` or `NOT APPLICABLE` rather than implying that an unchecked area
passed.
