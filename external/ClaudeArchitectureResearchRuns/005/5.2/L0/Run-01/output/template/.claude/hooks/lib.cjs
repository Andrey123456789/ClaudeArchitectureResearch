// Level: 3 Project | Shared helpers for Claude Code hooks (enforcement asset).
// Hooks are launched shell-neutrally from .claude/settings.json; the project directory is resolved
// here from process.env.CLAUDE_PROJECT_DIR (fallback: current directory), never by shell expansion.
'use strict';

const fs = require('fs');
const path = require('path');

function projectRoot() {
  const root = path.resolve(process.env.CLAUDE_PROJECT_DIR || process.cwd());
  if (!fs.existsSync(path.join(root, '.claude'))) {
    fail(`hook: cannot locate the project root (no .claude directory in "${root}"); enforcement did not run. ` +
      'Start Claude Code from the repository root or set CLAUDE_PROJECT_DIR.');
  }
  return root;
}

function readInput() {
  let raw = '';
  try {
    raw = fs.readFileSync(0, 'utf8');
  } catch (error) {
    fail(`hook: could not read hook input from stdin (${error.message}); enforcement did not run.`);
  }
  if (!raw.trim()) return {};
  try {
    return JSON.parse(raw);
  } catch (error) {
    fail(`hook: hook input is not valid JSON (${error.message}); enforcement did not run.`);
  }
  return {};
}

function relativeToRoot(root, file) {
  if (!file) return '';
  const absolute = path.resolve(root, file);
  return path.relative(root, absolute).split(path.sep).join('/');
}

// Exit 2: the message is shown to Claude (blocks a PreToolUse call; feedback for PostToolUse/Stop).
function feedback(message) {
  process.stderr.write(message.trim() + '\n');
  process.exit(2);
}

// Exit 1: non-blocking error shown to the user; used when enforcement could not run.
function fail(message) {
  process.stderr.write(message.trim() + '\n');
  process.exit(1);
}

function splitCommands(command) {
  return String(command || '')
    .split(/&&|\|\||;|\||\r?\n/)
    .map(part => part.trim())
    .filter(Boolean);
}

function stripComment(segment) {
  const index = segment.indexOf('#');
  return index >= 0 ? segment.slice(0, index).trim() : segment;
}

// Classifies package-changing commands. Returns { kind, segment } or null.
function classifyDependencyCommand(segment) {
  const s = stripComment(segment);
  const tokens = s.split(/\s+/);
  const lower = tokens.map(t => t.toLowerCase());
  const at = name => lower.indexOf(name);

  const dotnet = at('dotnet');
  if (dotnet >= 0) {
    const rest = lower.slice(dotnet + 1);
    if (rest[0] === 'add' && (rest[1] === 'package' || rest[2] === 'package')) return { kind: 'package', segment };
    if (rest[0] === 'package' && ['add', 'update'].includes(rest[1])) return { kind: 'package', segment };
    if (['add', 'remove'].includes(rest[0]) && (rest[1] === 'reference' || rest[2] === 'reference')) return { kind: 'reference', segment };
    if (rest[0] === 'reference' && ['add', 'remove'].includes(rest[1])) return { kind: 'reference', segment };
  }

  for (const manager of ['npm', 'pnpm', 'yarn']) {
    const index = at(manager);
    if (index < 0) continue;
    const sub = lower[index + 1];
    const args = tokens.slice(index + 2);
    const forced = args.some(a => /^--(force|legacy-peer-deps)$/i.test(a));
    const positional = args.filter(a => a && !a.startsWith('-'));
    const installs = ['install', 'i', 'add', 'update', 'up', 'upgrade'];
    if (!installs.includes(sub)) continue;
    if (forced) return { kind: 'force', segment };
    const restoreOnly = (sub === 'install' || sub === 'i') && positional.length === 0;
    if (!restoreOnly) return { kind: 'package', segment };
  }
  return null;
}

module.exports = { projectRoot, readInput, relativeToRoot, feedback, fail, splitCommands, classifyDependencyCommand };
