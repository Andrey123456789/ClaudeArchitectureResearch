---
name: verify
description: >
  Use before declaring a feature, fix or refactor complete or preparing a PR:
  final diff review, affected builds and tests, runtime smoke, coverage
  preservation, architecture, format and dependency checks, report.
---

> Level: 3 Project · Owns: verification procedure and report shape · Scope: common · Loads: on demand (model- or user-invoked)

# Verify

Produce evidence that the requested change is complete without obvious regressions. Verification proves required checks pass; `code-review` independently looks for defects that checks miss.

## Read first

- `.claude/rules/0-core/completion-contract.md` — the obligations this procedure satisfies.
- `.claude/rules/0-core/testing-principles.md` (Behavioral verification) — whenever behavior was demonstrated with an ad-hoc request, script, database check or throwaway test.
- `.claude/rules/2-technology/csharp.md` (Style and scope) — when C# files changed.
- `.claude/rules/3-project/data-lifecycle.md` (Development seeding) — when Domain or persistence changed.

## 1. Inspect the change

Review the final changed-file set and diff (`git status`, `git diff`, `git diff --cached` when Git is available). Confirm:

- the change matches the requested scope; no accidental refactoring;
- temporary diagnostics and probes are removed only after any behavior they uniquely verified is preserved as maintained coverage;
- no generated or build artifacts, secrets or environment-specific credentials were added.

Map the affected areas before choosing commands: backend-only → affected .NET projects; frontend-only → the Angular workspace; contract or full-stack → both; documentation-only → no unrelated builds.

## 2. Build

```bash
dotnet build <Name>.slnx            # or a narrower project path
npm run build                        # in frontend/<Name>.Web, when frontend changed
```

Inspect `package.json` for the actual scripts. Do not pass `--no-restore` unless restore is known to be complete.

## 3. Run relevant tests

```bash
dotnet test <Name>.slnx --no-build   # or the affected test projects first
npm test                             # only when the workspace defines it
```

Small solutions: run the full suite. Large solutions: affected test projects first, then the broader suite the risk requires.

## 4. Runtime smoke (new applications and substantial composition changes)

As applicable: the API host starts with Development configuration; the Development endpoint answers; Swagger UI loads at `/swagger`; required configuration binds; database connectivity and Development initialization succeed; the frontend dev server starts; the frontend API base URL and backend CORS configuration agree. Behavior established only by this smoke run is then preserved as maintained tests (testing principles).

## 5. Preserve behavioral verification

Replace ad-hoc probes with maintained automated tests — for example an NUnit `WebApplicationFactory` integration test instead of a `curl` or PowerShell request — unless an existing test already exercises the behavior.

## 6. Architecture check (when boundaries were touched)

```bash
node .claude/scripts/check-architecture.mjs
```

Then confirm by reading the code: API → Application flow, repository abstractions, persistence-framework boundary, unit-of-work commits, project references, and — when Domain or persistence changed — that the development seeder still produces valid representative data for a freshly recreated Development database. Skip for documentation-only or unrelated changes.

## 7. Formatting and static analysis (when configured)

```bash
dotnet format <Name>.slnx --verify-no-changes
```

Do not add a formatter or analyzer solely to complete verification. Analyzer output is evidence that still needs context.

## 8. Dependency and security checks (dependency or security-sensitive changes)

```bash
dotnet package list --vulnerable --include-transitive
npm audit                            # in the Angular workspace
```

Also inspect changed secrets handling, authorization, raw SQL, CORS/TLS settings, sensitive logging and certificate validation. A full `security-scan` is not needed for every small business-logic change.

## 9. Final diff review

After all fixes, check for: unrelated edits; commented-out code; temporary logging; unintended TODO/FIXME markers; stale temporary tests or scripts; architecture drift; unapproved drift from `SPECIFICATION.md` or `CUSTOM_SETTINGS.md`; stale code, tests, docs or configuration after a `CUSTOM_SETTINGS.md` change; unused or redundant `using` directives in C# files the change created or modified; behavior verified manually but never preserved as a test.

## Fix and retry

1. Identify the concrete failure.
2. Make the smallest appropriate fix (use `build-fix` for non-trivial build or test failures).
3. Rerun the affected verification; rerun build and tests when code changed.
4. Repeat until green or until user input is genuinely required.

## Report

```text
Backend build:            PASS / NOT RUN / NOT APPLICABLE
Frontend build:           PASS / NOT RUN / NOT APPLICABLE
Tests:                    PASS / NOT RUN / NOT APPLICABLE
Runtime smoke:            PASS / NOT RUN / NOT APPLICABLE
Architecture check:       PASS / NOT RUN / NOT APPLICABLE
Formatting/analyzers:     PASS / NOT RUN / NOT APPLICABLE
Dependency/security:      PASS / NOT RUN / NOT APPLICABLE
Diff review:              PASS
Open Decision Requests:   none / <list>
```
