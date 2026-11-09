---
name: verify
description: >
  Completion verification before declaring work finished: final diff and scope
  review, affected builds and tests, runtime smoke checks, behavioral-probe
  preservation, risk-scoped architecture/format/dependency/security checks,
  fix-and-retry, truthful PASS/NOT RUN report. Use when finishing a feature, bug
  fix, refactor, or preparing a PR.
---

> Kind: WF | Scope: common | Capability: — | Loading: on-demand workflow

# Verify Changes

## Goal

Produce evidence that the requested change is complete and has not introduced obvious regressions. Match verification depth to the scope and risk of the change, and do not require optional tooling the repository has not configured. Verification proves that required checks pass; `code-review` independently looks for defects that automated checks miss.

## 1. Inspect the change

Review the final changed-file set and diff before choosing any check. Confirm that:

- changes match the requested scope and no unrelated refactoring slipped in;
- temporary diagnostics and probes are removed only after any behavior they uniquely verified is preserved as maintained automated test coverage (step 4);
- no generated/build artifacts were added accidentally, and no secrets or environment-specific credentials were introduced — remove any that were.

Determine the affected repository areas: backend-only → affected .NET projects; frontend-only → the frontend workspace; contract or full-stack → both sides; documentation-only → no unrelated builds without a reason.

## 2. Build

Build the affected solution or projects (`dotnet build`, or a targeted project/solution path). For frontend changes, inspect `package.json` and run the workspace's declared build script (typically `npm run build`). Do not use `--no-restore` unless restore is known to be complete. A build failure means the implementation is not complete.

## 3. Run relevant tests

Run tests covering the changed area (`dotnet test`, targeted where useful; the frontend's declared test script when one exists — inspect `package.json` rather than assuming a runner). Small solutions: run the full suite. Large solutions: affected test projects first, then the broader suite required by the repository or the change risk. Investigate every newly failing relevant test; never dismiss a failure as unrelated without checking it.

### Runtime smoke check

Default: for a new runnable application or substantial composition, startup, configuration, persistence, or full-stack changes, verify that the intended Development configuration actually starts, as applicable: the API host starts; the Development endpoint is reachable; Swagger UI loads when the API exposes it; required configuration binds; database connectivity and initialization succeed; the frontend dev server starts; the frontend API base URL and backend CORS configuration are compatible. A successful build alone does not prove runtime composition.

## 4. Preserve behavioral verification

If an ad-hoc or manual behavioral probe (curl/PowerShell/HTTP requests, temporary scripts or test methods, manual database checks, regression probes) uniquely demonstrated that the change works, the verified behavior must be represented by maintained automated test coverage before completion, unless equivalent coverage already exists — confirm that existing coverage really exercises the behavior. The temporary mechanism itself need not remain. Builds, compilers, formatters, static analysis, and running existing suites do not themselves require new tests.

## 5. Risk-scoped checks

Run architecture, formatting/analyzer, dependency, and security checks when they are relevant to the change, not indiscriminately:

- **Architecture** (project references, Api → Application flow, repository abstractions, persistence boundary, Unit of Work behavior): read `.claude/rules/backend/architecture-style.md`, `.claude/rules/backend/persistence.md`, and `.claude/rules/backend/persistence-technology.md`, then run `node .claude/scripts/check-manifests.cjs`. When the persistence model changed, confirm that `persistence-change` was completed, including the development seeder for a freshly recreated Development database.
- **Co-change reminders:** `node .claude/scripts/check-cochange.cjs` (seed, migration, and test reminders for the working tree).
- **Formatting/analyzers:** when configured, e.g. `dotnet format --verify-no-changes`; do not add a formatter or analyzer dependency just to complete verification. Analyzer output is evidence that still needs context.
- **Dependencies and security:** for dependency changes or security-sensitive work, inspect vulnerabilities (`dotnet package list --vulnerable --include-transitive`, `npm audit`) and changed secrets, authorization, raw SQL, CORS/TLS, sensitive logging, and certificate validation. A full `security-scan` is not required for every small change.
- **Instruction system:** when `.claude/`, `CLAUDE.md`, or the decision register changed, run `node .claude/scripts/check-instructions.cjs`.

## 6. Final diff review

Review the final diff after all fixes. Check for accidental unrelated edits, commented-out code, temporary logging, unintended TODO/FIXME markers, stale temporary tests or scripts, architecture drift, unapproved drift from `SPECIFICATION.md` or `CUSTOM_SETTINGS.md`, stale code/tests/docs/config after a settings change, and behavior verified manually but never preserved as a test.

For every C# file created or modified by the task, remove unused or redundant `using` directives (including imports already provided by implicit/global usings, unless needed for clarity or disambiguation) without performing an unrelated repository-wide cleanup. Verify the changed files rather than assuming tooling removed every redundant import.

## Fix and retry

When verification fails: identify the concrete failure, make the smallest appropriate fix, rerun the affected verification (and build/tests when code changed), and repeat until green or until genuine user input is required. Never hide a known failure and declare completion; persistent build/test failures go to `build-fix`.

## Report

Report what was actually run, using PASS / NOT RUN / NOT APPLICABLE — never imply that an unchecked area passed:

```text
Backend build: PASS / NOT APPLICABLE
Frontend build: PASS / NOT APPLICABLE
Tests: PASS / NOT RUN / NOT APPLICABLE
Runtime smoke: PASS / NOT RUN / NOT APPLICABLE
Architecture/manifests: PASS / NOT RUN / NOT APPLICABLE
Formatting: PASS / NOT RUN
Security/dependency checks: ...
Diff review: PASS
Open Decision Requests: none / <list>
```
