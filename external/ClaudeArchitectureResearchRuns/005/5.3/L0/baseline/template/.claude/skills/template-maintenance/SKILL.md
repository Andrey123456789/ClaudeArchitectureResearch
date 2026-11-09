---
name: template-maintenance
description: >
  User-only. Maintain this instruction system: add, move, split, or retire rules,
  workflows, skills, hooks, or decision summaries, then run the structure checker.
disable-model-invocation: true
---

> Level: 0 Core · Owns: instruction-system maintenance procedure (workflow, user-invoked only) · Scope: repo/meta · Loads: on explicit user invocation only · Depends on: CLAUDE.md

# Template Maintenance

Run only when the user invokes it. Never start it automatically.

## 1. Place new content by stability

For each new statement ask: **how fundamental and stable is it?** Apply the tests in order:

1. Depends on project-specific selection, layout, defaults, or concrete commands? → **Level 3 Project** (`.claude/rules/3-project/`, project workflows).
2. Names a technology other than the fixed platform (.NET, C#, TypeScript; Git for repository safety)? → **Level 2 Technology** (`.claude/rules/2-technology/`, knowledge skills).
3. Presupposes the adopted architecture, a layer, role, or boundary? → **Level 1 Architecture** (`.claude/rules/1-architecture/`).
4. Otherwise → **Level 0 Core** (CLAUDE.md or `.claude/rules/0-core/`).

A statement's level is set by the most volatile thing it depends on. Split mixed statements: the neutral rule goes to the stable level, the technology binding to Level 2, the project selection to Level 3 (see the split-statement table in `.claude/INSTRUCTION_MAP.md`).

## 2. Choose the artifact by responsibility

- Normative constraint → a rule module. Trigger: always-loaded only if it must be known at planning time (CLAUDE.md, or the two imported decision summaries); otherwise a path rule whose `paths` cover at least the scope where it applies.
- Multi-step procedure → a workflow skill; it explicitly reads the rule files it depends on.
- Technique, examples, depth → a knowledge skill (or its private `references/`), never the sole owner of a must-rule.
- Mechanically checkable obligation → a hook or script in `.claude/hooks/` or `.claude/tools/`, with the rule kept as concise runtime policy.
- Product behavior or values → `SPECIFICATION.md` / `CUSTOM_SETTINGS.md`, which are inputs, not instruction layers.

## 3. Keep one owner

State each rule once, in its owner. Elsewhere use only a routing pointer ("run `verify`", "see `backend-layers.md`") or a short check-by-reference item. Decision summaries appear only in `1-architecture/overview.md` and `3-project/decisions.md`.

## 4. Keep the structure valid

- Every artifact starts with the one-line header (`Level · Owns · Scope · Loads · Depends on`); every rule file declares `paths`.
- `Depends on` lists conformance dependencies only, and each must be the same level or more stable; routing pointers may point anywhere.
- Levels 0 and 1 must not name concrete technologies beyond the fixed platform.
- Update `.claude/INSTRUCTION_MAP.md` for every added, moved, or removed artifact.

## 5. Check

Run the instruction-structure checker `.claude/tools/check-instructions.mjs` (command in `.claude/INSTRUCTION_MAP.md` → Enforcement) and fix every reported error. Keep the always-loaded surface compact (the checker prints its estimate).
