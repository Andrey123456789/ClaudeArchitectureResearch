---
name: template-maintenance
description: >
  User-invoked only. Maintain the instruction system itself: add, change, split,
  merge, move, or retire a rule, skill, private reference, agent, hook, script,
  or map entry while keeping one owner per policy and a reliable trigger.
disable-model-invocation: true
---

> Owner: instruction-system maintenance procedure and structural conventions | Scope: repo/meta | Loads: user-invoked only (`/template-maintenance`) | Enforced: `.claude/scripts/check-instructions.mjs` (also run by the PostToolUse hook after instruction edits)

# Template Maintenance

The challenge obligation in `CLAUDE.md` § Core Defaults applies to maintenance
requests too: name duplication, cohesion, trigger, context-cost, or complexity
concerns before changing the instruction system.

## Placement

Put each piece of content where its trigger is reliable:

| Content | Home |
| --- | --- |
| Needed at planning time for any task | `CLAUDE.md` (operating policy, decisions) or `docs/technology-stack.md` (stack) |
| Constraint tied to a file area | a flat rule in `.claude/rules/` with `paths` covering at least the policy's scope |
| Multi-step procedure with stop conditions and output | a workflow skill |
| Technique, examples, depth | a knowledge skill, or a private reference file inside one skill |
| Mechanically checkable or co-change obligation | `.claude/scripts/`, `.claude/hooks/`, `.claude/settings.json`, `.editorconfig`, `Directory.*.props` — keeping critical generation-time boundaries in a rule as well |
| Product behavior and tunable values | `SPECIFICATION.md`, `CUSTOM_SETTINGS.md` (inputs, never instruction layers) |
| Accepted project decisions | `docs/decisions/` via the `architecture-decision` workflow |

A must or must-not rule never lives only in a knowledge skill or a private
reference. A workflow that depends on a rule which may not have loaded names that
rule in its "Read First" step.

## Conventions

- **One owner.** Each normative rule is stated in exactly one file. Elsewhere use
  a routing pointer ("run `verify`", "see `<path>` § Heading") or a short yes/no
  check that names the owner; never reword the rule.
- **Header.** Every instruction file begins (after any YAML front matter) with
  one line:
  `> Owner: <what it owns> | Scope: <common, backend, backend-tests, frontend, delivery, repo/meta> | Loads: <mechanism> | Enforced: <mechanism or none>`.
- **Rules.** Flat `.claude/rules/*.md`, no subdirectories; every rule has a
  non-empty `paths` list; content is normative only (technique goes to skills).
- **Skills.** `name` equals the directory name; descriptions are trigger-first
  ("Use when …") with concrete cues. Knowledge-skill names stay stable;
  provider-specific depth (for example Serilog, resilience pipelines) is a
  private reference of the owning skill, not a competing skill.
- **Private references.** `skills/<name>/references/*` are read only by
  `<name>`; other files point to the skill, never into its references.
- **Pointers.** Write section pointers as `` `<path>` § <Heading> `` with the
  exact heading text; the checker resolves them.
- **Vocabulary.** must / must not, default, prefer / avoid, requires approval —
  as defined in `CLAUDE.md` § Vocabulary.
- **Parity.** No model IDs, effort levels, or environment-specific identifiers in
  skills or agents; tool restrictions follow the artifact's responsibility.
- **Budget.** Keep `CLAUDE.md` plus imports compact (the checker prints an
  estimate); move depth to path rules or skills instead of growing the
  always-loaded surface, but never move planning-time policy out of it to save
  tokens.

## Procedure

1. Locate the current owner in `.claude/MAP.md`.
2. Choose the change type — keep, fix in place, split, merge, move, or new — and
   justify any new file by a trigger, ownership, scope, or enforcement need.
3. Edit the owner; replace any duplicate statement elsewhere with a pointer.
4. Update `.claude/MAP.md`: the artifact row (owner, scope, loading,
   enforcement, extension guidance) and the policy index.
5. Update hooks or scripts when a mechanical check changes; keep hook messages
   as pointers to the owner.
6. Run `node .claude/scripts/check-instructions.mjs` and fix every error.
7. Report changed files, ownership moves, and the always-loaded estimate.
