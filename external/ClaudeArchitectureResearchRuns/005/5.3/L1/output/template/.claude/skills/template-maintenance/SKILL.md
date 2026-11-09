---
name: template-maintenance
description: User-invoked only. Maintain this instruction system — add or move a rule, workflow, or knowledge skill, replace or remove a capability module, or check instruction structure.
disable-model-invocation: true
---

> Level: 0-core · Owns: instruction-system maintenance procedure · Loading: user invocation only (never invoked automatically)

# Template Maintenance

Map of every artifact, owner, scope, and loading mechanism: `.claude/INSTRUCTION_MAP.md`.

## Where new content belongs

1. **Kind of content** — normative constraint → rule; multi-step procedure → workflow skill; technique/examples → knowledge skill or private reference; product facts → `SPECIFICATION.md` / `CUSTOM_SETTINGS.md`; mechanical check → hook, script, or configuration.
2. **Level** (first match wins): project-specific selection, layout, or default → `3-project`; concrete non-platform technology → `2-technology`; adopted architecture, role, or boundary → `1-architecture`; otherwise → `0-core`. Core and Architecture name no concrete technology beyond the fixed platform vocabulary (the platform names .NET, C#, ASP.NET Core, NuGet, HTTP, Git; their CLIs, project-file conventions, and base-runtime types; protocol terms); framework APIs, types, packages, and named framework features become Level 2 bindings (`.claude/rules/2-technology/backend-libraries.md` § Platform bindings or a module facet) that the neutral rule's wording maps onto.
3. **Capability** — content specific to a selected slot implementation goes into that module's facets (`.claude/capabilities/<slot>/<implementation>/MODULE.md` lists them) and declares `Capability:`; everything else uses roles and `<slot>.<facet>` references, never implementation names.
4. **Trigger** — always-needed planning policy goes into `CLAUDE.md` or an imported always rule; path-specific policy into a rule whose `paths` cover at least its scope; procedure obligations into the owning workflow.
5. **One owner** — add the rule once; elsewhere use a pointer or a yes/no check that names the owner.

## Steps

1. Draft the change and place it with the decision list above; keep the header line (`Level`, `Capability` when module-owned, `Owns`, `Scope`, `Loading`).
2. Update `.claude/INSTRUCTION_MAP.md` (level tables, capability view, policy locator).
3. For a capability replacement or removal, follow the slot `CONTRACT.md` and module `MODULE.md`; record the ADR with `architecture-decision`.
4. Run the checker and fix every reported item:

   ```bash
   node "$(git rev-parse --show-toplevel)/.claude/scripts/check-instructions.mjs"
   ```

5. Keep the always-loaded surface compact (`CLAUDE.md` plus its imports and skill descriptions); do not move path or workflow policy into it to simplify loading, and do not move always-needed policy out of it to save tokens.
