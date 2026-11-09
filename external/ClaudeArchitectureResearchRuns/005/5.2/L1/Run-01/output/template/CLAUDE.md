> Level: 0-core | Owns: entry point — always-loaded imports and workflow routing | Scope: common | Loads: always (project memory)

# Project Instructions

Instruction template for an ASP.NET Core backend with an optional browser frontend.
Policy is organized by stability level (0 Core → 1 Architecture → 2 Technology →
3 Project). Replaceable concerns are capability modules; the capability selection
record names the selected implementation of each slot.

## Always-loaded policy

@.claude/rules/0-core/operating-policy.md
@.claude/rules/0-core/product-governance.md
@.claude/rules/0-core/decision-control.md
@.claude/rules/1-architecture/roles.md
@.claude/rules/3-project/stack.md
@.claude/rules/3-project/capability-selection.md

## Selected capability decisions

One import per selected module decision facet; keep this list identical to the
capability selection record.

@.claude/rules/1-architecture/adopted-architecture.md
@.claude/rules/3-project/persistence-stack.md
@.claude/rules/3-project/backend-testing-stack.md
@.claude/rules/3-project/frontend-stack.md

Path-scoped rules under `.claude/rules/` load automatically for matching files.

## Workflow routing

| Situation | Run |
|---|---|
| Implementation work of any kind (feature, bug fix, refactor, new application) | `develop` |
| Completion check of a change | `verify` |
| Review of a diff, PR, or completed work | `code-review` (agent `code-reviewer`) |
| Repair of an existing build or test failure | `build-fix` |
| Adding, updating, or removing a package dependency | `add-dependency` |
| A `CUSTOM_SETTINGS.md` value is added, changed, or removed | `custom-settings` |
| Creating a solution, adding/removing projects, reorganizing structure | `project-structure` |
| CI/CD pipelines, container builds, deployment steps | `delivery` |
| A Reserved decision, Decision Request, or recording an approved decision | `architecture-decision` |
| A requested Git operation | `git-workflow` |
| Security audit or materially security-sensitive change | `security-scan` |

Instruction-system maintenance is user-invoked only (`/template-maintenance`).
Maintainer map (not loaded): `.claude/INSTRUCTION-MAP.md`.
