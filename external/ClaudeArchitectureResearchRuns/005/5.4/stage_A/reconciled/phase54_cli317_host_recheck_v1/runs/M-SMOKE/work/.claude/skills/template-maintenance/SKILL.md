---
name: template-maintenance
description: >
  Maintain the instruction system itself: add, change, move, or remove rules,
  workflows, knowledge skills, private references, hooks, scripts, or the map
  while keeping one owner per policy.
disable-model-invocation: true
---

> Owns: instruction-system maintenance procedure and structural invariants | Scope: repo/meta | Loads: user-invoked only (/template-maintenance); never invoked automatically

# Template Maintenance

This workflow runs only when the user invokes it. Claude must not start it
automatically.

## Invariants

- One authoritative owner per policy. Elsewhere use a routing pointer ("run
  workflow X", "see file Y") or a yes/no check-by-reference — never a reworded
  copy. Decision summaries appear only in CLAUDE.md § Architecture Defaults and
  `docs/technology-stack.md`.
- Keep each policy at its trigger: CLAUDE.md and `docs/technology-stack.md` only
  for planning-time policy; a flat path-scoped rule for constraints on files of
  an area; a workflow skill for procedure steps, stop conditions, and output
  shape. Do not promote content into CLAUDE.md to make loading easier, and do not
  demote planning-time policy to save tokens.
- Knowledge skills and private references hold technique only; they never own a
  must/must-not policy. A private reference is read only by its owning skill.
- Every instruction file starts with the one-line
  `> Owns: ... | Scope: ... | Loads: ...` header; every rule declares `paths`;
  `.claude/rules/` stays flat. CLAUDE.md imports only
  `docs/technology-stack.md`.
- Keep CLAUDE.md, `docs/technology-stack.md`, and skill descriptions compact;
  descriptions start with concrete triggers.
- Hooks are registered in exec form — `"command": "node"` with
  `"args": ["${CLAUDE_PROJECT_DIR}/.claude/hooks/<script>.mjs"]`, never a shell
  command string. The placeholder only locates the script; hooks derive the
  repository root they inspect from the hook input (`cwd`, or the edited file's
  location) and checkers from the current directory
  (`.claude/scripts/repo-root.mjs`). Hooks fail visibly and point messages at
  the owning file instead of restating policy. The dependency guard runs on
  PreToolUse, PostToolUse, and PostToolUseFailure for Bash and PowerShell, so a
  shell call that fails after changing a manifest is still checked. The
  PreToolUse guard also sets `"onFailure": "block"`, so a guard that cannot run
  blocks the tool call, and the guard itself blocks (exit 2) shell hook input it
  cannot read or classify, including a call with no command; advisory post-tool
  and Stop hooks do not block.
- Product inputs (`SPECIFICATION.md`, `CUSTOM_SETTINGS.md`) stay inputs; they do
  not carry instructions.

## Procedure

1. Find the current owner and the right location with `.claude/MAP.md`
   ("Where is the rule for…" and "Where new content goes").
2. Edit the owner in place; replace any other copy with a pointer.
3. Update `.claude/MAP.md` (file table and topic index).
4. From the repository root (`git rev-parse --show-toplevel`), run the
   structure checker and fix every failure:

   ```bash
   node .claude/scripts/check-instructions.mjs
   ```

5. For hook or script changes, run the changed script with sample input (usage
   is documented in each script's header) and confirm both the pass and the
   failure paths.
6. Report the files changed, owners added or moved, and the checker result.
