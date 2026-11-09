---
name: template-maintenance
description: Maintain the instruction system itself (add or move a rule, workflow, knowledge skill or hook; replace a capability implementation or provider variant; update the map). User-invoked only.
disable-model-invocation: true
---
Kind: WF | Scope: repo/meta | Capability: — | Loading: user-invoked only (/template-maintenance); never invoked automatically

# Template Maintenance

Procedure for changing the instruction system. The human map is `.claude/MAP.md`; the structural checker is `node .claude/scripts/check-instructions.mjs`.

## 1. Classify new content

Ask, in order:

1. **Capability**: is the content specific to a selected implementation (architecture frame, persistence, backend testing, frontend)? If yes, the selected module owns it; place it in the facet of the matching Kind and add the facet to the module's `MODULE.md`. Otherwise it belongs to the non-slot system.
2. **Kind**: what responsibility does it have?
   - `OP`: always-needed operating policy → `CLAUDE.md` (keep it compact).
   - `DEC`: a decided project choice needed at planning time → `docs/architecture/decision-register.md`.
   - `STD`: a normative rule that applies to files in a scope → `.claude/rules/<scope>/<topic>.md` with `paths:`.
   - `KNW`: technique, examples, depth → a knowledge skill (`.claude/skills/<name>/SKILL.md`), never the only home of a must-rule.
   - `WF`: a multi-step procedure with stop conditions and output shape → a workflow skill, or the module's `workflow-facet.md` for slot-specific steps.
   - `ENF`: a mechanical check → `.claude/hooks/`, `.claude/scripts/` (slot data in `.claude/scripts/facets/<slot>/`), `.editorconfig`, `Directory.*.props`.
   - `IN`: product input → `SPECIFICATION.md`, `CUSTOM_SETTINGS.md`; never instructions.
3. **Scope**: `common`, `backend`, `backend-tests`, `frontend`, `delivery` or `repo/meta`; this decides the rules directory and the `paths:` globs, which must cover at least the scope.

## 2. Authoring rules

- Each rule has exactly one owner. Elsewhere use only a routing pointer ("run X", "see Y"), a short check-by-reference item that names the owner, or a decision summary in the decision register.
- Start every instruction file with the one-line header `Kind: <K> | Scope: <S> | Capability: <slot/implementation or —> | Loading: <mechanism>` (after YAML frontmatter where present).
- Dependency direction for conformance: WF → KNW → STD → DEC → OP, and ENF → STD/DEC. Product inputs may request a decision change but never override policy. A skill-private reference (`references/`) is used only by its own skill.
- Never write a selected implementation's name or aliases (listed in its `MODULE.md`) outside that module's facets, the decision register's Capability selection section and this map; refer to slot and facet roles instead. Facet file names are role-based.
- Do not move path or workflow policy into the always-loaded surface to make loading easier, or always-loaded policy into on-demand material to save tokens. Keep `CLAUDE.md` and the register compact.
- Use the normative vocabulary of `CLAUDE.md` (must / must not, default, prefer / avoid, requires approval).
- Prefer enforceable tooling configuration over restating mechanical formatting rules in instructions.
- Hook commands are shell-neutral `node` invocations without `$`, `%` or backticks (the `node -e` bootstrap in `.claude/settings.json` finds `.claude/hooks/` from the current directory upward); scripts resolve the project directory themselves and fail with a clear message when an assumption does not hold.

## 3. Replace a capability implementation or variant

Only after the decision is approved and recorded (`architecture-decision`):

1. Read the slot's `CONTRACT.md` and the current module's `MODULE.md`.
2. Create `.claude/capabilities/<slot>/<new-implementation>/MODULE.md` with slot, implementation, aliases, binds and the facet table.
3. Provide every facet the contract requires, reusing role-based file names (`architecture-style.md`, `persistence-technology.md`, `test-framework.md`, `frontend-framework.md`, `workflow-facet.md`, `.claude/scripts/facets/<slot>/...`); a knowledge facet uses the shared skill name for materially identical content.
4. Remove the old module directory and every facet it listed, so unselected implementations do not remain at runtime.
5. Update the register's Capability selection row and section, and the capability view of `.claude/MAP.md`.
6. For a provider variant change, update the variant, declared properties and provider bindings in the existing facets instead of creating a module.
7. For an optional slot set to `none`, remove the module and its facets and keep the neutral standards.

## 4. Check

1. Update `.claude/MAP.md` (Kind × Scope view, capability view, topic index).
2. Run `node .claude/scripts/check-instructions.mjs` and fix every reported defect.
3. Run `node .claude/scripts/check-architecture.mjs` and `node .claude/scripts/check-manifests.mjs` when facets or enforcement data changed.

## Output

List the changed files, the owner of each moved or added rule, and the checker results.
