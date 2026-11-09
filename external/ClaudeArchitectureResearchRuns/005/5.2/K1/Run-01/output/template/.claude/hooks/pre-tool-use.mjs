// Kind: ENF | Scope: common | Capability: — | Loading: PreToolUse hook for Bash and PowerShell (.claude/settings.json) | Routes dependency commands to the add-dependency workflow by holding each distinct command once per session
import { readFileSync, writeFileSync, existsSync } from 'node:fs';
import { tmpdir } from 'node:os';
import path from 'node:path';
import { EnforcementError, projectRoot, readStdinJson, loadEnforcement, stableHash } from '../scripts/lib/common.mjs';
import { classifyCommand } from './lib/dependency-commands.mjs';

function seenCommands(stateFile) {
  if (!existsSync(stateFile)) {
    return [];
  }
  try {
    return JSON.parse(readFileSync(stateFile, 'utf8'));
  } catch {
    return [];
  }
}

async function main() {
  const input = await readStdinJson();
  const command = input?.tool_input?.command;
  if (typeof command !== 'string' || command.trim() === '') {
    return 0;
  }

  const root = projectRoot();
  const enforcement = loadEnforcement(root);
  const { dependency, force } = classifyCommand(command, enforcement);
  if (!dependency && !force) {
    return 0;
  }

  // Hold each distinct dependency command once per session; repeating it after the workflow ran proceeds.
  const stateFile = path.join(tmpdir(), `claude-dependency-gate-${stableHash(`${root}|${input.session_id ?? 'no-session'}`)}.json`);
  const seen = seenCommands(stateFile);
  const key = stableHash(command.trim().replace(/\s+/g, ' '));
  if (seen.includes(key)) {
    return 0;
  }
  writeFileSync(stateFile, JSON.stringify([...seen, key]));

  const messages = [];
  if (dependency) {
    messages.push(enforcement.policy.messages.dependencyCommand);
  }
  if (force) {
    messages.push(enforcement.policy.messages.npmForceFlag);
  }
  process.stderr.write(`${messages.join('\n')}\n`);
  return 2;
}

main().then(
  (code) => process.exit(code),
  (error) => {
    const detail = error instanceof EnforcementError ? error.message : error.stack;
    process.stderr.write(`Dependency routing hook failed (dependency commands are not being routed): ${detail}\n`);
    process.exit(1);
  },
);
