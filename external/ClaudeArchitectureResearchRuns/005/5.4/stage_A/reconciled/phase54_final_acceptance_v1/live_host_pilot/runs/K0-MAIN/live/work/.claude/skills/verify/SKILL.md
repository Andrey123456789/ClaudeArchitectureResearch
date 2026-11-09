---
name: verify
description: Use before declaring any implementation work complete (feature, fix, refactor, scaffold, repair, PR). Diff review, affected builds and tests, probe preservation, risk-scoped checks, PASS/NOT RUN report.
---

> Kind: WF | Scope: common | Owner: completion verification procedure and verification reporting | Loading: workflow (model- or user-invoked)

# Verify

Goal: evidence that the requested change is complete without obvious regressions. Match verification to the scope and risk of the change, and do not require tooling the repository has not configured. Verification proves required checks pass; see also: `code-review`, which independently looks for defects automation misses.

## 1. Inspect the change

Before choosing checks, review the final changed-file set and diff, confirm scope, remove accidental artifacts and secrets, and determine the affected repository areas:

- changes match the requested scope and contain no accidental unrelated refactoring;
- temporary diagnostics and probes are removed only after step 4 preserved what they uniquely verified;
- no generated or build artifacts were added;
- no secrets or environment-specific credentials were introduced.

Affected areas decide the checks: backend-only → affected .NET projects; frontend-only → the Angular application; contract or full-stack → both sides; documentation-only → no unrelated builds.

## 2. Build

Build the affected projects; a build failure means the implementation is not complete.

```bash
dotnet build
npm run build
```

Prefer the targeted project or `.slnx` when appropriate. Do not use `--no-restore` unless restore is known to be complete. For Angular, use the build script `package.json` actually defines.

## 3. Test

Run the relevant tests and investigate every new relevant failure; do not dismiss a failure as unrelated without checking it.

```bash
dotnet test --no-build
```

For Angular, inspect `package.json` and run the configured test script rather than assuming a runner. Small solutions: run the complete suite. Large solutions: affected test projects first, then the broader suite the risk requires.

### Runtime smoke

Default: for a new runnable application or substantial startup, configuration, persistence or full-stack change, verify the intended local Development startup — as applicable: the API host starts; the Development endpoint is reachable; Swagger UI loads when the API exposes it; required configuration binds; database connectivity and initialization succeed; the frontend dev server starts; the frontend API base URL and backend CORS configuration are compatible. A successful build alone does not prove runtime composition.

API behavior change: when a change alters API behavior and the project exposes the Development Swagger UI in Development, also start the API in Development, open the Development Swagger UI and confirm it loads, even when startup and composition did not change. The step does not apply when the project exposes no such UI. If the application cannot run in this environment, report the check as NOT RUN with the reason; never report it as passed.

## 4. Preserve behavioral verification

If an ad-hoc or manual behavioral probe — a temporary curl, PowerShell or HTTP request, script, ad-hoc test, manual database check or regression probe — uniquely demonstrated that the behavior works, that behavior must be represented by maintained automated coverage before completion, unless equivalent coverage already exists (confirm the existing test really exercises it). The temporary mechanism itself need not remain; builds, compiler, formatter and static-analysis commands and runs of existing suites do not require new tests. Technique: `dotnet-testing`.

## 5. Risk-scoped checks

Run architecture, formatting/analyzer, dependency and security checks when they are relevant to the change, not indiscriminately.

- **Architecture** — when boundaries, project references, repositories, the EF Core boundary or Unit of Work behavior changed: `node "$(git rev-parse --show-toplevel)/.claude/scripts/check-dependencies.cjs"`, then review against `rules/backend/architecture.md`. A `NOT_RUN` line or exit code 3 from the manifest check means the MSBuild proof of effective Central Package Management did not run: report it as NOT RUN, never as passed. When the model changed, confirm the seeder obligation in `development-workflow` § Persistence or model change.
- **Formatting and analyzers** — when configured: `dotnet format --verify-no-changes`. Do not add a formatter or analyzer just to complete verification. Analyzer output is evidence that still needs context.
- **Dependencies and security** — for dependency changes or security-sensitive work: `dotnet package list --vulnerable --include-transitive`, `npm audit`; inspect changed code for secrets, authorization, SQL/raw query safety, CORS/TLS changes, sensitive logging and disabled certificate validation. Run the full `security-scan` only when the change warrants it.

## 6. Final diff review

- For every C# file created or modified by the task, remove unused or redundant `using` directives, including imports already supplied by implicit/global usings unless needed for clarity or disambiguation. Do not perform an unrelated repository-wide using cleanup. Tooling such as `dotnet format style --verify-no-changes --diagnostics IDE0005 --include <changed files>` helps, but check the changed files rather than assuming the tool removed every import.
- Also check for: accidental unrelated edits; commented-out code; temporary logging; unintended TODO/FIXME markers; stale temporary tests or scripts; architecture drift; unapproved drift from `SPECIFICATION.md` or `CUSTOM_SETTINGS.md` (CLAUDE.md § Product sources); stale code, tests, docs or configuration after a `CUSTOM_SETTINGS.md` change (`custom-settings`); behavior verified manually but never preserved (step 4).

## Fix and retry

When verification fails:

1. Identify the concrete failure.
2. Make the smallest appropriate fix.
3. Re-run the affected verification, and build/tests whenever the fix changed code.
4. Repeat until green or until genuine user input is required.

Never hide a known failure or declare completion while one remains. For a stubborn build or test failure switch to `build-fix`.

## Report

Report what was actually run. Use PASS, FAIL, NOT RUN or NOT APPLICABLE; never imply that an unchecked area passed.

```text
Backend build: PASS / NOT APPLICABLE
Frontend build: PASS / NOT APPLICABLE
Tests: PASS / NOT RUN / NOT APPLICABLE
Runtime smoke: PASS / NOT RUN / NOT APPLICABLE
Formatting/analyzers: PASS / NOT RUN
Architecture check: PASS / NOT APPLICABLE
Security/dependency scan: PASS / NOT RUN / NOT APPLICABLE
Diff review: PASS
```
