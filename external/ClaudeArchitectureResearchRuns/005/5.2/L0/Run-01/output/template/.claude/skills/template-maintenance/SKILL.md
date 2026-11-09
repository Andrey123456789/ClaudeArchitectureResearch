---
name: template-maintenance
description: >
  User-only procedure for changing this instruction system — adding, moving,
  splitting, or removing rules, workflows, knowledge skills, hooks, or decision
  summaries. Never invoked automatically.
disable-model-invocation: true
---

> Level: 0 Core | Owns: instruction-system change procedure, level assignment, extension guidance | Scope: repo/meta | Loads: user-only workflow (`/template-maintenance`) | Depends on: CLAUDE.md

# Template Maintenance

Run only when the user invokes `/template-maintenance`.

## 1. Classify the Content

| Content | Artifact |
|---|---|
| Normative constraint (must, default, requires approval) | rule module in `.claude/rules/<level>/` |
| Multi-step procedure, stop conditions, output shape | workflow skill |
| Technique, examples, depth | knowledge skill (private depth in its `references/`) |
| Product behavior or tunable value | `SPECIFICATION.md` / `CUSTOM_SETTINGS.md` (input, not instruction) |
| Mechanical check or delivery | hook, script, or configuration asset |

## 2. Assign the Level

Apply in order; the first yes wins:

1. Depends on project-specific selection, layout, defaults, or commands? → `3-project`
2. Names a concrete technology other than the fixed platform (.NET, C#,
   TypeScript)? → `2-technology`
3. Presupposes the adopted architecture, a layer role, or a boundary? →
   `1-architecture`
4. Otherwise → `0-core`

A statement's level is set by the most volatile thing it depends on. Split a
mixed statement: keep the neutral rule at the stable level and put the binding
("type X is a persistence-framework type") at the technology or project level.
`0-core` and `1-architecture` never name concrete technologies; the structure
checker holds the deny-list.

## 3. Choose the Trigger

- Needed at planning time → always-loaded surface: CLAUDE.md (Core), the
  architecture summary (`1-architecture/overview.md`), or the project summary
  (`3-project/decisions.md`). Keep these compact; never make a file
  always-loaded just because of its level.
- Applies to a file area → path-scoped rule; `paths` must cover at least the
  rule's scope (common, backend, backend-tests, frontend, delivery, repo/meta).
- Applies at a workflow step → the owning workflow; if the step needs a rule
  that may not be loaded, the workflow reads it explicitly.

## 4. Keep One Owner

- Each rule has exactly one owner. Elsewhere use a routing pointer (`→ run X`,
  `→ see Y`) or a check-by-reference item; do not reword the rule.
- A conformance dependency points to the same or a more stable level only
  (Project → Technology → Architecture → Core) and is declared in the header's
  `Depends on:` field; a pointer to a more volatile level is written as a `→`
  routing line.
- A skill's `references/` files are read only by that skill.
- Engineering rules never depend on product, feature, or task inputs.

## 5. Change and Validate

1. Edit or add the artifact with its one-line header
   (`> Level: … | Owns: … | Scope: … | Loads: … | Depends on: …`).
2. Update `.claude/INSTRUCTION_MAP.md` (owner, scope, loading, enforcement,
   extension guidance, split statements).
3. Run `node .claude/scripts/check-instructions.cjs` and fix every error.
4. Replacing an embedded technology (for example the test framework) means
   editing its technology module, the project decisions, and every workflow,
   knowledge skill, hook, or asset that names it; search the repository for
   the old name.
