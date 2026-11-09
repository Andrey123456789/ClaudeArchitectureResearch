---
name: template-maintenance
description: >
  User-invoked maintenance of this instruction system: add, move, split or
  retire a rule, workflow, knowledge skill, hook or map entry while preserving
  the level model, single ownership and loading reliability.
disable-model-invocation: true
---

> Level: 3 Project · Owns: instruction-system maintenance procedure · Scope: repo/meta · Loads: user-invoked only

# Template Maintenance

Invoked by the user only. Map of the system: `.claude/INSTRUCTION-MAP.md`.

## 1. Classify the new or changed statement

Apply the level tests in order — the level is set by the most volatile thing the statement depends on:

1. Depends on project-specific selection, layout or defaults? → **3 Project** (`.claude/rules/3-project/`)
2. Names a technology other than the fixed platform (.NET, C#, TypeScript)? → **2 Technology** (`.claude/rules/2-technology/`)
3. Presupposes the adopted architecture, a role or a boundary? → **1 Architecture** (`.claude/rules/1-architecture/`)
4. Otherwise → **0 Core** (`.claude/rules/0-core/`)

Split mixed statements: keep the neutral part at the stable level and put the concrete binding at the Technology or Project level (example: "Domain does not depend on a persistence framework" → Level 1; "`DbContext` and `DbSet<T>` are persistence-framework types" → Level 2). Record the split in the map.

## 2. Classify the responsibility

| Content | Artifact |
|---|---|
| Normative constraint (must / default / requires approval) | rule module under `.claude/rules/<level>/` |
| Planning-time decision (adopted/not adopted architecture; stack, conditional technology, project default) | `1-architecture/overview.md` or `3-project/decisions.md` — never a merged cross-level register |
| Multi-step procedure with stop conditions and output shape | workflow skill |
| Technique, examples, depth | knowledge skill (Level 2) or a skill-private reference |
| Mechanically checkable obligation | hook or script under `.claude/hooks/` or `.claude/scripts/`, with the rule still stated concisely |
| Product behavior or tunable value | `SPECIFICATION.md` / `CUSTOM_SETTINGS.md` — not instructions |

## 3. Keep one owner

- Search the rules for the same semantics before writing. Extend the existing owner instead of restating it elsewhere.
- Other artifacts may only point to the owner ("see …", "run …") or carry a short yes/no check that names it.
- A must/must-not rule never lives only in a skill or a skill-private reference.
- Workflow-triggered obligations live in a rule module that the workflow explicitly reads.

## 4. Choose loading

- Needed at planning time for every task → import from `CLAUDE.md` (keep the always-loaded surface compact).
- Needed when certain files are touched → path-scoped rule; `paths:` covers at least the scope (common, backend, backend-tests, frontend, delivery, repo/meta) and every rule file declares `paths`.
- Needed during a procedure → the workflow's "Read first" list names the module.
- A new module is created only when trigger, ownership, dependency, scope or change driver justify it — not for symmetry.

## 5. Write the artifact

- First body line: the classification header `> Level: <n> <Name> · Owns: … · Scope: … · Loads: …`.
- Conformance references point only to the same or a more stable level; Levels 0 and 1 name no concrete technology outside the fixed platform.
- Use the vocabulary from `CLAUDE.md` (must / must not, default, prefer / avoid, requires approval).
- Skills: `name` equals the directory; descriptions are short and trigger-first with concrete cues.

## 6. Update the map and check

1. Update `.claude/INSTRUCTION-MAP.md`: module row (owner, scope, loading, enforcement, extension guidance), topic index, split-statement table.
2. Run:

   ```bash
   node .claude/scripts/check-instructions.mjs
   ```

3. Fix every reported failure before finishing.

## Replacing an embedded technology

Technologies are embedded by design. Replacing one (for example NUnit → xUnit) means editing: the Level 3 selection (`decisions.md`, `conventions.md`), the Level 2 module and knowledge skill that name it, workflows and scaffold commands that use it, hook package lists, and the map. Record the decision through `architecture-decision`.

## Report

Files changed with their levels, owners added or moved, loading changes, checker result.
