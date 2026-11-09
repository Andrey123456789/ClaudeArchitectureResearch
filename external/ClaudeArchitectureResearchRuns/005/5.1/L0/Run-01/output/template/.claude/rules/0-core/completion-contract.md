---
paths:
  - "backend/**"
  - "frontend/**"
  - ".github/workflows/**"
  - "**/*pipeline*.yml"
  - "**/*pipeline*.yaml"
  - "**/.gitlab-ci.yml"
---

> Level: 0 Core · Owns: verification, review, repair and pipeline obligations · Scope: common, delivery · Loads: path; read explicitly by `verify`, `code-review`, `build-fix`

# Completion Contract

The work loop in `CLAUDE.md` decides *when* review and verification run. This module owns *what they must guarantee*. Procedures live in the named workflows.

## Verification (procedure: `verify`)

- **Must** start from the final changed-file set and diff: confirm the change matches the requested scope, remove accidental artifacts, build output and secrets, and determine the affected repository areas before choosing checks.
- **Must** build the affected projects and run the relevant tests. A build failure means the implementation is not complete; every newly failing relevant test is investigated — never dismissed as unrelated without checking.
- **Default:** for a new runnable application or a substantial startup, configuration, persistence or full-stack change, verify that the intended Development startup and key composition surfaces actually work. A successful build alone does not prove runtime composition.
- **Must** run architecture, formatting/analyzer, dependency and security checks when they are relevant to the change — not indiscriminately, and without adding tooling solely to complete ordinary verification.
- **Must**, when verification fails, make the smallest appropriate fix and rerun the affected checks until they pass or genuine user input is required. A known failure is never hidden.
- **Must** report what actually ran as PASS, NOT RUN or NOT APPLICABLE; never imply that an unchecked area passed.
- Check: behavior demonstrated only by an ad-hoc probe is preserved as maintained automated coverage — owner: `.claude/rules/0-core/testing-principles.md` (Behavioral verification).

## Review (procedure: `code-review`, agent `code-reviewer`)

- **Must** perform review as an independent, read-only pass that uses the `code-review` workflow as its canonical procedure instead of redefining policy.
- **Must** prioritize correctness, security and authorization, data integrity, architectural boundaries, concurrency and integration behavior, meaningful test coverage, maintainability, and credible performance problems; style preferences never outrank defects.
- **Must not** manufacture findings to populate categories. When there are no meaningful findings, say so and name the important areas that could not be verified.

## Repair (procedure: `build-fix`)

- **Must** reproduce and diagnose the actual failure before editing, and fix root causes before downstream symptoms.
- **Must** iterate in small, bounded steps: rerun the narrowest failing check after each meaningful fix, expand verification only after the focused failure is resolved, and stop to reassess when progress stalls.
- **Must not** weaken, delete, skip or suppress relevant tests, compiler errors or analyzer findings merely to make verification pass.
- **Default:** when generated output is wrong, or its source contract or configuration changes, fix the authoritative source and regenerate. Do not hand-patch disposable generated output unless the repository or its generation workflow intentionally treats that output as maintained source.

## Pipelines

- **Must** keep CI definitions in source control, make them reproduce the repository's supported build and test commands, and never hide build or test failures.
