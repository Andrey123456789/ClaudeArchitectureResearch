---
name: verify
description: >
  Run before declaring any change complete: diff and scope check, builds, tests,
  runtime smoke, probe-to-test, risk-scoped checks, PASS/NOT RUN report.
---
> Level: 0-core | Owns: completion verification procedure and verification reporting | Scope: common | Loads: on demand (skill)

# Verify Changes

Produce evidence that the requested change is complete and introduced no
obvious regression. Match verification to scope and risk; do not require
tooling the repository has not configured. Verification proves that required
checks pass; `code-review` looks for defects that checks miss.

## 1. Inspect the change

Review the final changed-file set and diff before choosing checks. Confirm that:

- the changes match the requested scope and contain no accidental refactoring;
- temporary diagnostics and probes are removed only after any behavior they
  uniquely verified is preserved (step 5);
- no generated or build artifacts were added;
- no secrets or environment-specific credentials were introduced.

Then determine the affected areas: backend-only → affected .NET projects;
frontend-only → the frontend workspace; contract or full-stack change → both;
documentation-only → no unrelated builds.

## 2. Build

- Backend: build the affected solution or projects (`dotnet build`, or a
  targeted project). Do not use `--no-restore` unless restore is known to be
  complete.
- Frontend (when the slot is selected and affected): the build command from
  `frontend.commands`.

A build failure means the implementation is not complete.

## 3. Run relevant tests

- Backend: the commands in `backend-testing.commands` — the whole suite for a
  small solution; affected test projects first, then the broader suite the risk
  requires, for a large one.
- Frontend: the configured test script from `frontend.commands`.

Investigate every newly failing relevant test; do not dismiss a failure as
unrelated without checking it.

## 4. Runtime smoke (new or recomposed applications)

Default: for a new runnable application or a substantial startup,
configuration, persistence, composition, or full-stack change, verify the
intended Development startup — the API host starts, the Development endpoint is
reachable, the Development API documentation UI is reachable when the project
exposes it, required configuration binds, database connectivity and
initialization succeed, the frontend development server starts, and the
frontend API base URL matches the backend CORS configuration. A successful build
alone does not prove runtime composition.

## 5. Preserve behavioral verification

If a new behavioral check — an ad-hoc HTTP request, `curl` or PowerShell
script, manual database check, temporary test, regression probe, or runtime
smoke — uniquely demonstrated that the behavior works, preserve that behavior in
maintained automated test coverage before completion, unless equivalent
coverage already exists (confirm that the existing test actually exercises it).
The temporary mechanism itself does not need to remain. Builds, compiler checks,
formatting, static analysis, and running the existing suite do not by
themselves require new tests.

## 6. Risk-scoped checks

Run these when relevant to the change, not indiscriminately:

- Architecture — when boundaries, project references, persistence, or the
  seeded model change: `node .claude/scripts/check-architecture.cjs`, the
  role-boundary rules for the changed areas, and seed consistency per
  `persistence.workflow` (a freshly recreated Development database must still
  seed validly).
- Formatting/analyzers — when configured: `dotnet format --verify-no-changes`.
  Do not add a formatter or analyzer dependency just to complete verification.
- Dependencies and security — after dependency changes or security-sensitive
  work: `dotnet package list --vulnerable --include-transitive`, the frontend
  audit from `frontend.commands`, `node .claude/scripts/check-packages.cjs`, and
  a review of secrets, authorization, raw SQL safety, CORS/TLS changes,
  sensitive logging, and disabled certificate validation. A full
  `security-scan` is not needed for small business-logic changes.

Treat tool output as evidence that still needs context.

## 7. Final diff review

Review the final diff after all fixes for accidental unrelated edits,
commented-out code, temporary logging, unintended TODO/FIXME markers, stale
temporary tests or scripts, architecture drift, unapproved drift from
`SPECIFICATION.md` or `CUSTOM_SETTINGS.md`, stale code/tests/docs/configuration
after a `CUSTOM_SETTINGS.md` change, and behavior verified manually but never
preserved as a test.

For every C# file created or modified by the task, remove unused or redundant
`using` directives — including imports already provided by implicit or global
usings unless needed for clarity or disambiguation — and verify the changed
files rather than assuming tooling removed them. Do not perform an unrelated
repository-wide using cleanup.

## Fix and retry

When verification fails: identify the concrete failure, make the smallest
appropriate fix, re-run the affected verification (and build/tests when code
changed), and repeat until green or until genuine user input is required. Never
hide a known failure and declare completion; use `build-fix` for stubborn build
or test failures.

## Reporting

Report what was actually run, using `PASS`, `NOT RUN`, or `NOT APPLICABLE`;
never imply that an unchecked area passed.

```text
Backend build: PASS / NOT APPLICABLE
Frontend build: PASS / NOT APPLICABLE
Tests: PASS / NOT RUN / NOT APPLICABLE
Runtime smoke: PASS / NOT RUN / NOT APPLICABLE
Formatting: PASS / NOT RUN
Architecture / dependency / security checks: ...
Diff review: PASS
Unresolved Decision Requests: none / <list>
```
