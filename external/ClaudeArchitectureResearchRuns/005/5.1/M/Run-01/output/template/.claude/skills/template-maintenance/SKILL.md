---
name: template-maintenance
description: >
  User-invoked only. Maintain this instruction system: add or change a rule,
  workflow, knowledge skill, hook, or checker while keeping one owner per
  policy, correct loading, an updated MAP, and a passing structure check.
disable-model-invocation: true
---

> Owns: instruction-system maintenance procedure | Scope: repo/meta | Loads: user-invoked only (/template-maintenance); never invoked automatically

# Template Maintenance

Use `.claude/MAP.md` as the index of instruction files and their owners.

## 1. Classify the Change

Decide what the new or changed content is, and where it belongs:

| Content | Home |
|---|---|
| Must/default constraint needed while planning any work (product authority, architecture defaults, approval gate, Git safety) | `CLAUDE.md` |
| Approved or conditional technology, layout default | `docs/technology-stack.md` |
| Constraint needed while editing certain files | a topical rule in `.claude/rules/` (flat; extend the matching topic before creating a file) |
| Multi-step procedure, stop conditions, output shape | a workflow skill |
| Technique, examples, decision guides | a knowledge skill (or its private `references/` file) |
| Mechanically checkable obligation | `.editorconfig`, `Directory.*.props`, a hook, or a script in `.claude/scripts/` |
| Product behavior or tunable value | `SPECIFICATION.md` / `CUSTOM_SETTINGS.md` — product inputs, not instructions |

Challenge the request first if it duplicates an owner, weakens a trigger, or
adds context cost without need (`CLAUDE.md`, Challenge Before Implementing).

## 2. Keep One Owner

- Search for existing wording of the same rule (`grep -ri "<key phrase>" .claude
  CLAUDE.md docs`). Extend the existing owner instead of restating it.
- Other files may only point to the owner ("see `persistence.md`") or carry a
  short check-by-reference item; never reword the rule elsewhere.
- Must/must-not policy never lives only in a knowledge skill or a private
  reference.
- A private `references/` file is read only by its owning skill.
- Normative content depends only on reliably loaded owners; engineering policy
  never depends on product or task inputs.

## 3. Get Loading Right

- Every rule declares `paths` covering at least the scope where it applies.
- Always-needed planning policy goes in `CLAUDE.md` or the imported
  `docs/technology-stack.md`; keep that surface compact.
- A workflow that depends on a path rule which may not have loaded must read it
  explicitly.
- Knowledge-skill descriptions start with concrete triggers ("Use when ...").
- Workflows that must never be model-invoked set
  `disable-model-invocation: true`.

## 4. Format

- The first line after any frontmatter is the header:
  `> Owns: <responsibility> | Scope: <scopes> | Loads: <mechanism>`.
- Use the vocabulary defined in `CLAUDE.md` (must / default / prefer /
  requires approval).
- Hook and script messages point to the owner; they do not restate policy.

## 5. Update the Map and Check

1. Add or update the file's row in `.claude/MAP.md` and the policy-topic index.
2. Run `node .claude/scripts/check-instructions.mjs` and fix every reported
   problem.
3. Summarize what changed, the owner chosen, and its loading mechanism.
