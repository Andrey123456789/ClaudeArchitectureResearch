---
name: template-maintenance
description: >
  User-invoked only (/template-maintenance): change the instruction system
  itself — CLAUDE.md, the technology stack, rules, skills, agents, hooks,
  scripts, settings, MAP.md.
disable-model-invocation: true
---

> Workflow skill (user-invoked only). Owns: the procedure for changing the instruction system and keeping the map, checkers, and hook data consistent · Scope: repo/meta · Loads: only when the user runs /template-maintenance · Depends on: CLAUDE.md

# Template Maintenance

## 1. Locate the Owner

Open `.claude/MAP.md` and find the authoritative owner of the topic (Policy
Locator) and the placement guidance (Where New Content Goes). Change the owner;
do not add a second copy elsewhere.

## 2. Place New Content by Trigger and Responsibility

| Content | Place |
|---|---|
| Policy needed while planning any task | `CLAUDE.md` (keep it compact) |
| Approved or conditional technology, layout default | `docs/technology-stack.md` |
| Constraint that applies when certain files are edited | the topical rule in `.claude/rules/` whose `paths` cover those files; a new flat rule file only for a new topic or scope |
| Multi-step procedure, stop conditions, output shape | a workflow skill |
| Technique, examples, depth | a knowledge skill, or its `references/` file |
| Mechanically checkable obligation | `.claude/scripts/` or `.claude/hooks/`, keeping the critical boundary in the owning rule or workflow |
| Product behavior or tunable values | `SPECIFICATION.md` / `CUSTOM_SETTINGS.md` (product inputs, not instructions) |

## 3. Preserve the Structure

- One authoritative owner per rule. Elsewhere use a routing pointer ("see X")
  or a check-by-reference item; the only decision summary is CLAUDE.md
  (Architecture Decisions).
- Keep each policy at its trigger: do not move path-scoped or workflow policy
  into CLAUDE.md for convenience, and do not move always-needed planning policy
  into path rules or skills to save tokens.
- Critical must / must not rules never live only in a knowledge skill or a
  private reference.
- Keep `.claude/rules/` flat; every rule declares `paths`.
- Every instruction file starts with its one-line header (`Owns`, `Scope`,
  `Loads`, `Depends on`). Dependencies of CLAUDE.md, the technology stack, and
  rules point only to always-loaded or path-scoped files; private references
  are used only by their owning skill; the dependency graph stays acyclic.
- Hook and script commands stay shell-neutral: `node .claude/<dir>/<file>.mjs`,
  with no shell variable expansion; scripts resolve paths and environment
  themselves and fail with a clear message.

## 4. Update Co-Maintained Data

- `.claude/MAP.md` — artifact rows and Policy Locator entries.
- `.claude/scripts/check-manifests.mjs` — the deprecated and review package
  lists mirror `docs/technology-stack.md` and `add-dependency`.
- `.claude/scripts/check-instructions.mjs` — the required workflow and
  knowledge skill lists.
- `.claude/settings.json` — hook registrations.

## 5. Check

Run `node .claude/scripts/check-instructions.mjs` and fix every reported
violation. Review the always-loaded size estimate it prints and keep the
always-loaded surface compact without moving policy away from its trigger.

## Output

Summarize the changed owners, any moved content with its reason, and the
checker result.
