---
name: template-maintenance
description: >
  User-invoked maintenance of the instruction system: where new instructions
  belong, changing rules, skills, hooks, and decision records, and replacing
  or removing a capability implementation.
disable-model-invocation: true
---

> Workflow · User-invoked only · Owns the procedure for changing the instruction system, capability modules, and the human map

# Template Maintenance

Read `.claude/MAP.md` first; it lists every instruction artifact, its owner,
scope, loading, and enforcement.

## Where New Content Belongs

| Content | Location |
|---|---|
| governance needed at planning time | `CLAUDE.md` (keep it compact) |
| approved stack or conditional technology outside the slots | `docs/technology-stack.md` |
| planning-time decision of a selected capability implementation | `docs/capabilities/<slot>.md` |
| path-scoped normative rule | `.claude/rules/<topic>.md` — flat, `paths:` required; implementation-specific content goes into the slot's role-named facet with a `Capability:` header |
| multi-step procedure | a workflow skill |
| technique, examples, reference depth | a knowledge skill or its private `references/` file |
| mechanical or co-change check | `.claude/hooks/` or `.claude/scripts/`, wired in `.claude/settings.json` |
| maintainer metadata for a slot | `.claude/capabilities/<slot>/CONTRACT.md` and `<implementation>/MODULE.md` |

## Change Procedure

1. Find the current authoritative owner in the map; change the rule there and
   use pointers elsewhere — never restate a rule in a second place.
2. Keep each policy's trigger role: planning-time policy stays on the
   always-loaded surface, path policy stays in a path rule covering its full
   scope, and procedural obligations stay in their workflow.
3. Do not hide a must/must-not rule only inside a knowledge skill or a private
   reference.
4. Outside a capability implementation, refer to slot names and facet roles,
   not to the selected implementation's name.
5. Keep the always-loaded surface (`CLAUDE.md`, its imports, skill
   descriptions) compact; do not load the whole corpus to solve reliability.
6. Update `.claude/MAP.md`.
7. Run `node "$(git rev-parse --show-toplevel)/.claude/scripts/check-instructions.js"`
   (from any directory of the repository or worktree being changed) and fix
   every error.

## Capability Replacement

Use after an ADR approved the change (`architecture-decision` § Capability
Selection Changes).

1. Read `.claude/capabilities/<slot>/CONTRACT.md` for the required facets,
   properties, and role vocabulary.
2. Read the current `<implementation>/MODULE.md`; its manifest lists every
   runtime facet and its physical location.
3. Create `.claude/capabilities/<slot>/<new-implementation>/MODULE.md` with a
   complete manifest (facets, properties, binds, leak tokens, enforcement
   data).
4. Rewrite each facet at the same role-named location (planning facet, rule
   facet, knowledge skill, workflow facet, scaffold notes) for the new
   implementation, and update each `Capability:` header.
5. Update the slot row in `docs/capability-selection.md` and remove the old
   implementation directory.
6. Review instructions that bind to the slot (`binds` in other manifests) and,
   for the architecture frame, the layer names used by embedded rules.
7. Run the instruction checker and update the capability view in the map.

### Provider Variant Change (persistence)

Edit the provider-variant sections listed in the persistence `MODULE.md`
manifest, the provider property in `docs/capability-selection.md`, and the
declared string-comparison property; record the ADR.

### Removing the Optional Frontend Slot

Set the frontend row to status `disabled` with implementation `—`; delete the
facet files listed in the frontend `MODULE.md` manifest and its module
directory; remove the `@docs/capabilities/frontend.md` import from
`CLAUDE.md`; update the frontend entry in the map's capability view; run the
checker. Other instructions need no edits: their references to the slot's
role-named facets apply only to frontend work and stay inactive while the slot
is disabled, and the framework-independent `.claude/rules/frontend.md` only
loads for `frontend/` files.
