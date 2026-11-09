---
name: template-maintenance
description: Maintain the Claude instruction system of this repository — add, move, split or retire rules, skills, decisions, hooks or checks. User-invoked only.
disable-model-invocation: true
---

> Kind: WF | Scope: repo/meta | Owner: instruction-system maintenance procedure | Loading: workflow (user-invoked only; never model-invoked)

# Template Maintenance

Map of the instruction system: `.claude/MAP.md`. Structural checker: `node .claude/scripts/check-instructions.cjs`.

## 1. Classify the content

Answer two questions; together they determine location, loading and owner.

1. **What is it?** Operating policy → OP; project/architecture decision → DEC; normative rule for a scope → STD; technique or examples → KNW; multi-step procedure → WF; mechanical check or delivery asset → ENF; product requirement or tunable value → IN (product input, not an instruction).
2. **Where does it apply?** `common`, `backend`, `backend-tests`, `frontend`, `delivery` or `repo/meta`.

| Kind | Location | Loading |
|---|---|---|
| OP | `CLAUDE.md` | always |
| DEC | `docs/architecture/decision-register.md` (+ ADRs in `docs/decisions/`) | always (imported) |
| STD | `.claude/rules/<scope>/<topic>.md` with `paths:` inside the scope's territory | path-scoped |
| KNW | `.claude/skills/<name>/SKILL.md` (+ private `references/`) | on demand |
| WF | `.claude/skills/<name>/SKILL.md`, `.claude/agents/<name>.md` | workflow |
| ENF | `.claude/settings.json`, `.claude/hooks/`, `.claude/scripts/`, root build/format files | event/check |
| IN | `SPECIFICATION.md`, `CUSTOM_SETTINGS.md`, feature/task inputs | read as input |

## 2. Keep one owner

1. Search for an existing owner of the same rule (`.claude/MAP.md` topic index, then a repository search). Extend that owner instead of adding a second statement.
2. Other artifacts may only point to the owner (routing pointer) or check against it (a short check-by-reference item); never reword the same rule elsewhere.
3. A critical must/must-not rule never lives only in a knowledge skill or a skill-private reference.
4. Keep the trigger role: always-loaded policy stays in OP/DEC, path rules stay path-scoped with at least their current scope, workflow obligations stay in workflow steps. Do not move content between roles to save tokens.

## 3. Respect dependency direction

Conformance dependencies run WF → KNW → STD → DEC → OP; ENF → STD/DEC. Standards cite decision IDs (`D-xx`) instead of restating decisions; decision summaries exist only in the register. Routing pointers may point anywhere reliably invocable. A skill's `references/` files are read only by that skill.

## 4. Apply the change

1. Write the artifact with its one-line header: `> Kind: … | Scope: … | Owner: … | Loading: …` (after any frontmatter).
2. Decision added or changed: follow `architecture-decision` § 3–4 (ID, Details in, Affects, propagation).
3. Knowledge skill descriptions stay concise and trigger-first ("Use when …" with concrete cues).
4. Update `.claude/MAP.md`: artifact table, Kind × Scope view, topic index and decision → Affects view.
5. Keep the always-loaded surface (CLAUDE.md, the register, skill descriptions) compact; move detail to the owner it belongs to.

## 5. Check

1. Run `node .claude/scripts/check-instructions.cjs` and fix every reported problem.
2. When hooks or scripts changed, exercise them with a sample payload, for example:

```bash
echo '{"tool_name":"Bash","tool_input":{"command":"npm install lodash"}}' | node .claude/hooks/hook.cjs pre-tool-use
```

3. Summarize what moved, the new owners and the checker result.
