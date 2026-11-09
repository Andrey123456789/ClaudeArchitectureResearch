---
name: template-maintenance
description: User-invoked only. Change the instruction system itself — standards, workflows, knowledge skills, decisions, hooks, scripts or the map — while keeping Kind/Scope placement, single ownership and structural checks green.
disable-model-invocation: true
---
<!-- Kind: WF | Scope: repo/meta | Owns: instruction-system maintenance procedure | Loads: user invocation only -->
# Template Maintenance

## 1. Classify the Content

Answer two questions; together they fix location, loading and owner (`.claude/MAP.md` § Placement):

1. What is it — operating policy (OP), decision (DEC), standard (STD), knowledge (KNW), workflow (WF), enforcement (ENF) or product input (IN)?
2. Where does it apply — `common`, `backend`, `backend-tests`, `frontend`, `delivery` or `repo/meta`?

## 2. Find the Existing Owner

Search `.claude/MAP.md` § Policy Locator and the decision register. If an owner exists, change the content there; anywhere else add only a routing pointer or a check-by-reference item. Never reword the same rule in a second file.

## 3. Place the Content

- **OP** → `CLAUDE.md`. Keep it short: policy, stop/approval boundaries and routing only; procedures go to workflows.
- **DEC** → a register row (stable ID, summary, `Details in`, `Affects`) in `docs/architecture/decision-register.md`; detailed policy goes to its owner. Follow `architecture-decision`.
- **STD** → `.claude/rules/<scope>/<responsibility>.md`, one cohesive responsibility per file, with the scope's canonical `paths:` (MAP.md § Scopes). Cite DEC IDs instead of restating decisions; no procedures (no numbered steps); skill references only on `Technique:` or `Workflow:` lines.
- **KNW** → `.claude/skills/<name>/SKILL.md` with a trigger-first description ("Use when …"). Technique, examples and trade-offs only — normative statements belong to a standard; depth goes to `references/` used only by that skill.
- **WF** → `.claude/skills/<name>/SKILL.md`: steps, stop conditions, output; standards appear as check-by-reference items. A workflow that relies on a standard reads it explicitly.
- **ENF** → `.claude/hooks/` (event entry points) or `.claude/scripts/` (checkers). Hook commands are `node <relative script path>` with no shell variable expansion; scripts resolve paths from `CLAUDE_PROJECT_DIR` or the hook input and fail clearly when they cannot. Messages point to the owner; they do not restate policy.
- **IN** → `SPECIFICATION.md`, `CUSTOM_SETTINGS.md` or feature specifications: product content only.

Every instruction file starts (after any frontmatter) with a one-line header: `<!-- Kind: … | Scope: … | Owns: … | Loads: … -->`. Create a file only for a real responsibility, never to fill a Kind × Scope cell.

## 4. Update the Map

Update `.claude/MAP.md`: catalog row, Kind × Scope cell, policy locator entry, and the decision → Affects list when a register entry changed.

## 5. Check

Run `node .claude/scripts/check-instructions.mjs` and fix every failure. Keep the always-loaded surface (`CLAUDE.md`, the register and skill descriptions) compact — the checker prints its estimate — without moving planning-time policy out of it.

## Output

Files changed, Kind/Scope of each, owners affected, checker result, always-loaded estimate.
