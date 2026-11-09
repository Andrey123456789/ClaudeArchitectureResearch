---
name: template-maintenance
description: >
  User-invoked only: maintain the instruction system (rules, workflows, skills,
  hooks, checkers) or replace a capability implementation.
disable-model-invocation: true
---

> **Workflow skill** · Owns: instruction-system maintenance and capability replacement procedure · Scope: repo/meta · Loading: user-invoked only (never invoked automatically)

# Template Maintenance

Read `.claude/MAP.md` first: it lists every artifact with its owner, scope,
loading, enforcement, and where new content belongs.

## Add or Change Instruction Content

1. Classify the content: normative constraint → rule (`.claude/rules/`, flat, with
   `paths:`) or always-loaded policy (`CLAUDE.md` / `docs/` planning records only
   when it is needed at planning time); multi-step procedure → workflow skill;
   technique/examples → knowledge skill or its private reference; product values
   → product inputs; mechanical check → hook/script.
2. Capability check first: content specific to one of the four capability slots
   belongs to the selected implementation's facets; everything else follows the
   map's normal ownership.
3. Give every policy exactly one owner. Elsewhere use only a routing pointer
   ("run X", "see Y") or a short check-by-reference item; never reword the same
   rule in a second place.
4. Start each instruction file with the one-line header used throughout
   (`> **<role>** · [Capability: <slot>/<implementation> ·] Owns: … · Scope: … ·
   Loading: …`).
5. Outside capability facets, refer to slots by role, not by implementation name.
6. Update `.claude/MAP.md`, then run the checker (step "Check").

## Replace, Add, or Remove a Capability Implementation

Changing a selection is Reserved: record the approval with `architecture-decision`.

1. Read `.claude/capabilities/<slot>/CONTRACT.md` (roles, required facets,
   required properties, replacement obligations) and the current
   `<implementation>/MODULE.md`.
2. Create `.claude/capabilities/<slot>/<new-implementation>/MODULE.md` with the
   manifest block, and author every required facet under its role-based file name
   (for example `.claude/rules/test-framework.md`), each declaring
   `Capability: <slot>/<new-implementation>` in its header.
3. Preserve every semantic the contract marks as required (for persistence:
   migration and seeding semantics, string-comparison property, relational
   testing binding). A required facet or property that cannot be supplied is a
   Decision Request, not a silent gap.
4. Remove the old implementation's facets listed in its manifest (and its module
   directory), so no unselected implementation remains in the runtime.
5. Update `docs/capability-selection.md`: the selection row, declared properties,
   the facet table, and the `@` import of any always-loaded facet.
6. Optional frontend slot: to remove it, set its selection row to
   `none (disabled)`, delete its facet-table row and its `@` import line, delete
   the facets and the module directory listed in its manifest, remove its entries
   from `.claude/MAP.md`, and keep the framework-independent `frontend.md`.

## Check

```bash
node .claude/scripts/check-instructions.mjs
```

The checker validates headers, rule `paths`, import resolution and the
always-loaded set, internal references, skill metadata, the thin reviewer agent,
capability selections, manifests, required facets and properties, unselected
implementations, implementation-name leaks, and declared bindings. It also
prints the always-loaded size estimate; keep it near the budget it reports.
