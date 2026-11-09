---
name: verify
description: Use before declaring an implementation, bug fix, refactor or scaffold complete, or before preparing a PR. Runs scope-appropriate build, tests, behavioral-coverage, architecture, dependency/security, delivery and final-diff checks and reports actual results.
---
Kind: WF | Scope: common | Capability: — | Loading: on invocation (routed from CLAUDE.md and development-workflow)

# Verify

Goal: evidence that the requested change is complete and has not introduced obvious regressions. Match verification to the scope and risk of the change, and do not require tooling the repository has not configured. Verification proves that required checks pass; `code-review` independently looks for defects that automated checks miss.

Owner reads: when a step checks a standard that is not loaded, read it from `.claude/rules/<scope>/`. Slot-specific commands come from the selected modules' `workflow-facet.md` (decision register → Capability selection).

## 1. Inspect the change

Review the final changed-file set and diff before choosing checks. Confirm that:

- the changes match the requested scope and no unrelated refactoring slipped in;
- temporary diagnostics and probes are removed only after any behavior they uniquely verified is preserved as maintained tests (step 4);
- no generated or build artifacts were added by accident;
- no secrets or environment-specific credentials were introduced.

Then determine the affected areas: backend-only changes verify the affected .NET projects; frontend-only changes verify the frontend workspace; contract or full-stack changes verify both sides; documentation-only changes do not run unrelated builds without a reason.

## 2. Build

- Backend: `dotnet build`, or a targeted project or solution build. Do not use `--no-restore` unless restore is known to be complete.
- Frontend: the build command from the frontend workflow facet, using scripts that exist in `package.json`.

Build and run the relevant tests for the affected areas. A build failure means the implementation is not complete; continue with `build-fix`.

## 3. Run the relevant tests

- Backend: the test commands from the backend-testing workflow facet. Frontend: the frontend workflow facet's test command when one is configured.
- For small solutions run the complete suite; for large ones run the affected test projects first, then any broader suite the repository or the change risk requires.
- Investigate every newly failing relevant test. Do not dismiss a failure as unrelated without checking it.

## Runtime smoke verification

Default: for a new runnable application or a substantial composition, startup, configuration, persistence or full-stack change, verify that the application starts with its intended local Development configuration. As applicable:

- the API host starts and the configured Development endpoint is reachable;
- Swagger UI is reachable when the API is expected to expose it;
- required configuration binds;
- database connectivity and initialization succeed (persistence workflow facet → Verification commands);
- the frontend development application starts, and its API base URL is compatible with the backend CORS configuration.

A successful build alone does not prove that runtime composition works. Behavior established only by this check goes through step 4.

## 4. Preserve behavioral verification

- If a new behavioral probe (a temporary HTTP request, curl or PowerShell script, ad-hoc test, manual database check or regression probe) demonstrated that the implementation works, the verified behavior must be represented by maintained automated tests before completion, unless equivalent coverage already exists. The temporary mechanism itself does not need to remain, and a probe is not a substitute for a maintained test. Builds, compiler checks, formatters, static analysis and runs of the existing suite do not by themselves require new tests.
- Default: a fix for a meaningful bug with plausible recurrence gets a regression test, unless equivalent coverage already exists.

## 5. Architecture, formatting, dependency and security checks

Run these checks when they are relevant to the change, not indiscriminately:

- Architecture boundaries touched (project references, Api-to-Application flow, persistence ports, persistence boundary, commit boundary, dependency direction): check the change against `.claude/rules/backend/architecture.md` and `architecture-style.md`, and run `node .claude/scripts/check-architecture.mjs` after project-reference or package changes. When a model change affects seeded entities, confirm that the seeder was updated and stays valid for a freshly recreated Development database.
- Formatting and analyzers, when the repository configures them: for example `dotnet format --verify-no-changes`. Do not add a formatter or analyzer dependency just to finish verification; analyzer output is evidence that still needs context.
- Dependency changes or security-sensitive work: `node .claude/scripts/check-manifests.mjs`, `dotnet package list --vulnerable --include-transitive`, `npm audit`, and a review of secrets, authorization, raw query safety, CORS and TLS changes, sensitive logging and disabled certificate validation. A full `security-scan` is not needed for every small change.
- Do not run a full architecture or security audit for documentation-only or unrelated changes.

## 6. Delivery and deployment changes

When the change creates or edits CI/CD definitions, deployment scripts, container files or startup migration behavior:

- CI definitions stay in source control, reproduce the repository's supported build and test commands, and must not hide build or test failures.
- Frontend CI uses scripts that actually exist and `npm ci` when a maintained lockfile supports it. Never invent npm scripts or reflexively replace lockfile-based installs.
- Production database migrations are not applied automatically from normal application startup by default; they are an explicit deployment operation with approved credentials. Development seeding never runs in Production.

Technique: `ci-cd` and `docker` knowledge skills; migration artifacts: the persistence workflow facet.

## 7. Final diff review

After all fixes, review the final diff for:

- accidental unrelated edits, commented-out code, temporary logging, unintended TODO/FIXME markers, stale temporary tests or scripts;
- architecture drift;
- unapproved drift from `SPECIFICATION.md` or `CUSTOM_SETTINGS.md`, and stale code, tests, documentation or configuration after a `CUSTOM_SETTINGS.md` change;
- behavior that was verified manually but never preserved as a test.

For every C# file created or modified by the task, remove unused or redundant `using` directives before completion, including imports already provided by implicit or global usings unless an explicit import is needed for clarity or disambiguation. Verify the changed files rather than assuming tooling removed every redundant import, and do not perform an unrelated repository-wide cleanup.

## Fix and retry

When verification fails:

1. identify the concrete failure;
2. make the smallest appropriate fix (`build-fix` for build and test failures);
3. rerun the affected verification, and rerun build and tests when the fix changed code;
4. repeat until the change is green or genuine user input is required.

Never hide a known failure and declare completion.

## Report

Report what actually ran:

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

Use NOT RUN or NOT APPLICABLE instead of implying that an unchecked area passed.
