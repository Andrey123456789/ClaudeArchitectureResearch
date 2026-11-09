#!/usr/bin/env node
// Owns: PreToolUse guard for shell commands — routes dependency changes to the
// add-dependency workflow and blocks npm peer-conflict bypass flags.
// Scope: common. Loads: PreToolUse hook (Bash|PowerShell) from .claude/settings.json.
//
// Exit 0 = allow. Exit 2 = block; stderr is shown to Claude.

const MARKER = '# add-dependency';
const VALUE_FLAGS = new Set(['--prefix', '--workspace', '-w', '--registry', '--cache', '--userconfig', '--tag']);
const NPM_CHANGE = new Set(['install', 'i', 'add', 'isntall', 'uninstall', 'un', 'remove', 'rm', 'r', 'update', 'up', 'upgrade']);
const NPM_ALWAYS_CHANGE = new Set(['update', 'up', 'upgrade']);

function readStdin() {
  return new Promise((resolve) => {
    let data = '';
    process.stdin.setEncoding('utf8');
    process.stdin.on('data', (chunk) => (data += chunk));
    process.stdin.on('end', () => resolve(data));
  });
}

function segments(command) {
  return command
    .split(/&&|\|\||;|\||\r?\n/)
    .map((s) => s.replace(/#.*$/, '').trim().split(/\s+/).filter(Boolean))
    .filter((tokens) => tokens.length > 0);
}

function hasPositional(tokens) {
  for (let i = 0; i < tokens.length; i++) {
    const t = tokens[i];
    if (VALUE_FLAGS.has(t)) { i++; continue; }
    if (!t.startsWith('-')) return true;
  }
  return false;
}

function firstPositional(tokens) {
  for (let i = 0; i < tokens.length; i++) {
    if (VALUE_FLAGS.has(tokens[i])) { i++; continue; }
    if (!tokens[i].startsWith('-')) return i;
  }
  return -1;
}

function isDependencyChange(tokens) {
  const lower = tokens.map((t) => t.toLowerCase());
  const npm = lower.indexOf('npm');
  if (npm >= 0) {
    const rest = lower.slice(npm + 1);
    const subIndex = firstPositional(rest);
    const sub = subIndex >= 0 ? rest[subIndex] : '';
    if (NPM_ALWAYS_CHANGE.has(sub)) return true;
    if (NPM_CHANGE.has(sub) && hasPositional(rest.slice(subIndex + 1))) return true;
  }
  const ng = lower.indexOf('ng');
  if (ng >= 0 && (lower[ng + 1] === 'add' || (lower[ng + 1] === 'update' && hasPositional(lower.slice(ng + 2))))) return true;
  const dotnet = lower.indexOf('dotnet');
  if (dotnet >= 0) {
    const rest = lower.slice(dotnet + 1);
    if ((rest[0] === 'add' || rest[0] === 'remove') && rest.includes('package')) return true;
    if (rest[0] === 'package' && ['add', 'update', 'remove'].includes(rest[1])) return true;
  }
  return false;
}

let input = {};
try { input = JSON.parse((await readStdin()) || '{}'); } catch { process.exit(0); } // never fail the tool call on bad input
const command = String(input?.tool_input?.command ?? '');

if (/\bnpm\b[^\n]*\s--(force|legacy-peer-deps)\b/i.test(command)) {
  process.stderr.write(
    'Blocked: npm --force / --legacy-peer-deps bypasses peer-dependency conflicts. ' +
      'Resolve the compatibility problem instead (see .claude/rules/dependencies.md, npm).\n',
  );
  process.exit(2);
}

if (!command.includes(MARKER) && segments(command).some(isDependencyChange)) {
  process.stderr.write(
    'Dependency change detected. Run the add-dependency workflow ' +
      '(.claude/skills/add-dependency/SKILL.md) first; its install step marks the command with ' +
      `"${MARKER}".\n`,
  );
  process.exit(2);
}

process.exit(0);
