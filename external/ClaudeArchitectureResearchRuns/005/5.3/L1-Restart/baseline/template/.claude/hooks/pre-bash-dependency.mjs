#!/usr/bin/env node
// PreToolUse (Bash|PowerShell): routes dependency commands to the add-dependency workflow.
// First attempt of a dependency command is denied with a pointer; the identical command is
// allowed when retried within the grace window (after the workflow ran). Force flags that
// bypass peer-dependency resolution always require user confirmation.
import { existsSync, mkdirSync, readFileSync, writeFileSync } from 'node:fs';
import path from 'node:path';
import { SetupError, readStdinJson, resolveRoot } from '../scripts/lib/project.mjs';

const GRACE_MS = 30 * 60 * 1000;

export function classify(command) {
  const cmd = String(command || '');
  const segments = cmd.split(/&&|\|\||;|\r?\n|\|/).map((s) => s.trim()).filter(Boolean);
  let dependency = false;
  let forceFlag = false;
  for (const seg of segments) {
    const tokens = seg.split(/\s+/);
    const lower = tokens.map((t) => t.toLowerCase());
    const at = (i) => lower[i] || '';
    for (let i = 0; i < lower.length; i++) {
      const t = lower[i].replace(/\.(exe|cmd)$/, '');
      if (t === 'dotnet' && ((at(i + 1) === 'add' && lower.slice(i + 2).includes('package')) ||
          (at(i + 1) === 'remove' && lower.slice(i + 2).includes('package')) ||
          (at(i + 1) === 'package' && ['add', 'update', 'remove'].includes(at(i + 2))))) {
        dependency = true;
      }
      if (['npm', 'pnpm', 'yarn'].includes(t)) {
        const verb = at(i + 1);
        const args = lower.slice(i + 2);
        if (['install', 'i', 'add', 'update', 'upgrade', 'up', 'uninstall', 'remove', 'rm', 'un'].includes(verb) &&
            args.some((a) => !a.startsWith('-'))) {
          dependency = true;
        }
        if (['install', 'i', 'ci', 'add', 'update'].includes(verb) &&
            args.some((a) => a === '--force' || a === '-f' || a === '--legacy-peer-deps')) {
          forceFlag = true;
        }
      }
      if (t === 'ng' && at(i + 1) === 'add') dependency = true;
      if (t === 'install-package' || t === 'update-package') dependency = true;
    }
  }
  return { dependency, forceFlag };
}

function decide(decision, reason) {
  process.stdout.write(JSON.stringify({
    hookSpecificOutput: { hookEventName: 'PreToolUse', permissionDecision: decision, permissionDecisionReason: reason },
  }));
  process.exit(0);
}

async function main() {
  const input = await readStdinJson();
  const command = input.tool_input && input.tool_input.command;
  const { dependency, forceFlag } = classify(command);
  if (!dependency && !forceFlag) process.exit(0);

  if (forceFlag) {
    decide('ask', 'npm --force / --legacy-peer-deps bypasses peer-dependency resolution. The add-dependency workflow requires resolving the actual compatibility problem instead; confirm only if the user explicitly wants this.');
  }

  let root;
  try {
    root = resolveRoot();
  } catch (error) {
    decide('ask', `Dependency command detected, but the hook cannot track workflow state (${error.message}). Run the add-dependency workflow before confirming.`);
  }

  const stateDir = path.join(root, '.claude', '.hook-state');
  const stateFile = path.join(stateDir, 'dependency-commands.json');
  const now = Date.now();
  let state = {};
  if (existsSync(stateFile)) {
    try { state = JSON.parse(readFileSync(stateFile, 'utf8')); } catch { state = {}; }
  }
  for (const [key, ts] of Object.entries(state)) if (now - ts > GRACE_MS) delete state[key];

  const key = String(command).trim().replace(/\s+/g, ' ');
  if (state[key]) {
    delete state[key];
    writeFileSync(stateFile, JSON.stringify(state, null, 2));
    process.exit(0);
  }

  mkdirSync(stateDir, { recursive: true });
  state[key] = now;
  writeFileSync(stateFile, JSON.stringify(state, null, 2));
  decide('deny', 'Dependency change detected. Run the add-dependency workflow first (need, approved technology, latest stable compatible version, deprecation, vulnerability and license checks, approval for commercial or unclear licenses). After completing it, re-run the identical command within 30 minutes.');
}

main().catch((error) => {
  const prefix = error instanceof SetupError ? 'Hook setup problem' : 'Hook failure';
  process.stderr.write(`${prefix} (pre-bash-dependency): ${error.message}\n`);
  process.exit(1);
});
