---
name: template-maintenance
description: >
  User-invoked procedure for changing this instruction system: adding or moving
  policy, standards, workflows, knowledge, hooks, or capability modules, and
  keeping MAP, manifests, and the structure checker green.
disable-model-invocation: true
---

> Kind: WF | Scope: repo/meta | Capability: — | Loading: user-invoked workflow only

# Template Maintenance

Use only when the user explicitly asks to change the instruction system. Maintainer overview: `.claude/MAP.md`.

## 1. Classify the content (in this order)

1. **Capability** — is it specific to the selected implementation of a slot (architecture, persistence, backend-testing, frontend)? Yes → the module owns it: it becomes a facet listed in that module's manifest (`.claude/capabilities/<slot>/<implementation>/MODULE.md`), and its header declares `Capability: <slot>/<implementation>`. No → non-slot content with `Capability: —`. Implementation-independent policy for a slot concern stays in the neutral standard; only implementation-specific rules go to the facet. Placement belongs to the architecture frame; technique belongs to leaves, which declare unavoidable frame bindings in `Binds:`.
2. **Kind** — determines mechanism and location:

   | Kind | Content | Location / mechanism |
   |---|---|---|
   | OP | Operating policy, approval and stop boundaries | `CLAUDE.md` (always loaded) |
   | DEC | Project decisions, stack, defaults, capability selection | `docs/architecture/decision-register.md` (imported) |
   | STD | Path-scoped normative standards | `.claude/rules/<scope>/<topic>.md` with `paths:` |
   | KNW | Technique, examples, depth | `.claude/skills/<name>/SKILL.md` (+ private `references/`) |
   | WF | Multi-step procedures, stop conditions, report shape | `.claude/skills/<name>/SKILL.md`, `.claude/agents/` |
   | ENF | Deterministic enforcement/delivery | `.claude/hooks/`, `.claude/scripts/`, `.claude/settings.json`, root build/editor config |
   | IN | Product inputs | `SPECIFICATION.md`, `CUSTOM_SETTINGS.md` |

3. **Scope** — `common`, `backend`, `backend-tests`, `frontend`, `delivery`, `repo/meta`. A rule's `paths:` must include its scope's canonical glob (`**/*`, `backend/**/*`, `backend/**/*Tests/**/*`, `frontend/**/*`); no other directory hierarchy under `.claude/rules/`.

## 2. Ownership rules

- Every normative statement has exactly one owner. Elsewhere use only a routing pointer ("run `x`"), a check-by-reference item pointing at the owner, or a decision summary in the decision register.
- Vocabulary: must / must not, Default, prefer / avoid, requires approval (`CLAUDE.md`).
- Trigger role is part of the content: always-loaded policy stays in OP/DEC, path policy in STD, procedure obligations in WF. Do not move content between roles to save tokens or to make loading easier; never place critical must-policy only in a skill.
- Dependency direction: WF → KNW → STD → DEC → OP, and ENF → STD/DEC. References to invocable skills are routing pointers and may point anywhere; references to non-invocable files are conformance dependencies, must follow this direction, and a skill-private reference is used only by its owning skill. Product inputs never override policy.
- Leak rule: outside a module's facets, its manifest, the decision register's capability-selection block, and the maintainer map, never name the selected implementation; refer to slot and facet roles instead. Facet file names are role-based (`test-framework.md`, not the implementation's name).

## 3. Make the change

1. Start each artifact with the one-line header `Kind | Scope | Capability | Loading` (after frontmatter where frontmatter is required).
2. Skills: frontmatter `name` equal to the directory, a concise trigger-first `description` with concrete cues; WF bodies own procedure and output shape; KNW bodies own technique and point to standards for policy.
3. Capability changes: follow `architecture-decision` (contract coverage, single implementation per slot, no unselected implementations at runtime).
4. Update the module manifest's facet table and `.claude/MAP.md` (both views) for every added, moved, or removed artifact.
5. Hooks: exec form only (`"command": "node"`, `"args": ["${CLAUDE_PROJECT_DIR}/.claude/hooks/dispatch.cjs", "<event>"]`); `${CLAUDE_PROJECT_DIR}` only locates the hook code, while every check uses the active repository or worktree derived from the hook input `cwd`. The dependency and reference guard (PreToolUse) keeps `"onFailure": "block"`; post-tool and Stop hooks stay advisory. Hook messages point to the owner instead of restating it.
6. Enforcement artifacts (ENF) declare their policy owners on the line after the header: `Conforms: <STD or DEC owner>, …` or `Conforms: —`; every standard or register path an ENF artifact cites must be declared. Slot binding obligations (persistence and backend-testing bind architecture) and the contract's facet roles are fixed; keep `Binds:` in the contract and the manifest in agreement.

## 4. Check

Run `node "<root>/.claude/scripts/check-instructions.cjs"` (`<root>`: the active repository root; command form in `verify`, Risk-scoped checks) and fix every error. Review the reported always-loaded size; keep it compact without moving required planning-time policy out of the always-loaded surface.
