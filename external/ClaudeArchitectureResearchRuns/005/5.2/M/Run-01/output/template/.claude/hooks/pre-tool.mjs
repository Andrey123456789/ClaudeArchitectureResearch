// PreToolUse hook for shell tools (Bash, PowerShell).
// - Blocks npm/pnpm/yarn installs that bypass peer-dependency resolution (exit 2).
// - Asks for confirmation before Git commands that can discard work or rewrite history.
// Messages point to the owning workflow; policy text lives there, not here.
// Registered in .claude/settings.json as: node .claude/hooks/pre-tool.mjs

import { SetupError, readStdinJson, resolveProjectRoot } from '../scripts/lib/repo.mjs';
import { findDestructiveGit, findPeerBypass } from './commands.mjs';

async function main() {
  resolveProjectRoot(import.meta.url);
  const input = await readStdinJson();
  const command = input?.tool_input?.command;
  if (typeof command !== 'string' || command.trim() === '') return;

  const bypass = findPeerBypass(command);
  if (bypass) {
    process.stderr.write(
      `Blocked: \`${bypass.command}\` uses ${bypass.flag}. Peer-dependency conflicts are resolved, not bypassed — ` +
      'follow .claude/skills/add-dependency/SKILL.md (Install).\n');
    process.exit(2);
  }

  const destructive = findDestructiveGit(command);
  if (destructive) {
    process.stdout.write(JSON.stringify({
      hookSpecificOutput: {
        hookEventName: 'PreToolUse',
        permissionDecision: 'ask',
        permissionDecisionReason:
          `\`${destructive}\` can discard work or rewrite history. Confirm that it was explicitly requested ` +
          '(.claude/skills/git-workflow/SKILL.md, Destructive Operations).',
      },
    }));
  }
}

main().catch((error) => {
  const message = error instanceof SetupError ? error.message : (error?.stack ?? String(error));
  process.stderr.write(`pre-tool hook failed; shell-command checks were NOT run: ${message}\n`);
  process.exit(1);
});
