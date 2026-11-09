// Owner: hook dispatcher — routes dependency and Git commands, blocks npm peer-bypass flags, runs mechanical checks after edits, issues co-change reminders at stop | Scope: common | Loads: Claude Code hooks (`node .claude/hooks/hooks.mjs <pre-tool-use|post-tool-use|stop>` from .claude/settings.json) | Enforced: exit code 2 feeds the message back to Claude
// Messages point to the owning rule or workflow; they do not restate policy.

import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import crypto from 'node:crypto';
import { execFileSync } from 'node:child_process';
import { projectRoot, rel, walk, readText, exists, formatFindings } from '../scripts/lib.mjs';
import { checkDependencies } from '../scripts/check-dependencies.mjs';
import { checkArchitecture } from '../scripts/check-architecture.mjs';
import { checkInstructions } from '../scripts/check-instructions.mjs';

const ADD_DEPENDENCY = '.claude/skills/add-dependency/SKILL.md';
const GIT_WORKFLOW = '.claude/skills/git-workflow/SKILL.md';
const CUSTOM_SETTINGS = '.claude/skills/custom-settings/SKILL.md';

// ---------- input, output, state ----------

async function readInput() {
  let raw = '';
  for await (const chunk of process.stdin) raw += chunk;
  try {
    return JSON.parse(raw || '{}');
  } catch {
    return {};
  }
}

/** Exit code 2: the hook output reaches Claude (blocks PreToolUse calls and Stop; informs after PostToolUse). */
function tellClaude(message) {
  process.stderr.write(`${message.trim()}\n`);
  process.exit(2);
}

function stateFile(sessionId) {
  const dir = path.join(os.tmpdir(), 'claude-instruction-hooks');
  fs.mkdirSync(dir, { recursive: true });
  const safe = String(sessionId || 'no-session').replace(/[^A-Za-z0-9_-]/g, '_');
  return path.join(dir, `${safe}.json`);
}

function loadState(sessionId) {
  try {
    return JSON.parse(fs.readFileSync(stateFile(sessionId), 'utf8'));
  } catch {
    return {};
  }
}

function saveState(sessionId, state) {
  try {
    fs.writeFileSync(stateFile(sessionId), JSON.stringify(state));
  } catch {
    // State only suppresses repeated reminders; losing it is harmless.
  }
}

const hash = (value) => crypto.createHash('sha256').update(value).digest('hex').slice(0, 16);

// ---------- command classification ----------

function segments(command) {
  return String(command || '')
    .split(/&&|\|\||;|\||\r?\n/)
    .map((segment) => segment.trim().replace(/^(sudo|npx)\s+/, ''))
    .filter(Boolean);
}

function hasPackageArgument(args) {
  return args.split(/\s+/).some((arg) => arg && !arg.startsWith('-'));
}

export function isDependencyCommand(segment) {
  if (/^dotnet\s+(add|remove)\b.*\bpackage\b/i.test(segment)) return true;
  if (/^dotnet\s+package\s+(add|remove|update)\b/i.test(segment)) return true;
  if (/^dotnet\s+tool\s+(install|update|uninstall)\b/i.test(segment) && !/\s(-g|--global)\b/.test(segment)) return true;
  const npm = /^(npm|pnpm|yarn)\s+(install|i|add|uninstall|remove|rm|un|update|up|upgrade)\b(.*)$/i.exec(segment);
  if (npm) {
    const verb = npm[2].toLowerCase();
    return !['install', 'i'].includes(verb) || hasPackageArgument(npm[3]);
  }
  const ng = /^ng\s+(add|update)\b(.*)$/i.exec(segment);
  return Boolean(ng && hasPackageArgument(ng[2]));
}

export function isNpmPeerBypass(segment) {
  if (!/^(npm|pnpm|yarn)\b/i.test(segment) || /^npm\s+cache\b/i.test(segment)) return false;
  return /--force\b|--legacy-peer-deps\b/.test(segment) ||
    (/^npm\s+(install|i|ci|add|update)\b/i.test(segment) && /\s-f\b/.test(segment));
}

/** Returns 'destructive', 'changing', or null for a Git command segment. */
export function gitOperation(segment) {
  const match = /^git\s+(?:-C\s+\S+\s+|-c\s+\S+\s+)*([\w-]+)(.*)$/i.exec(segment);
  if (!match) return null;
  const [, sub, rest] = match;
  const args = ` ${rest} `;
  switch (sub) {
    case 'reset':
      return /\s--hard\s/.test(args) ? 'destructive' : 'changing';
    case 'clean':
      return 'destructive';
    case 'push':
      return /\s(--force|-f|--force-with-lease\S*|--delete|-d)\s/.test(args) ? 'destructive' : 'changing';
    case 'branch':
      if (/\s(-D|--delete\s+--force|--force\s+--delete)\s/.test(args)) return 'destructive';
      return /\s(-d|--delete|-m|-M|--move)\s/.test(args) ? 'changing' : null;
    case 'checkout':
      return /\s--\s|\s\.\s/.test(args) ? 'destructive' : null;
    case 'restore':
      return /\s(--staged|-S)\s/.test(args) && !/\s(--worktree|-W)\s/.test(args) ? null : 'destructive';
    case 'stash':
      if (/^\s*(list|show)\b/.test(rest)) return null;
      return /^\s*(drop|clear)\b/.test(rest) ? 'destructive' : 'changing';
    case 'worktree':
      return /^\s*remove\b/.test(rest) ? 'destructive' : null;
    case 'filter-branch':
    case 'filter-repo':
      return 'destructive';
    case 'commit':
    case 'merge':
    case 'rebase':
    case 'pull':
    case 'cherry-pick':
    case 'revert':
    case 'am':
      return 'changing';
    case 'tag':
      return rest.trim() === '' || /^\s*(-l|--list)\b/.test(rest) ? null : 'changing';
    default:
      return null;
  }
}

// ---------- PreToolUse ----------

async function preToolUse(input) {
  const command = input.tool_input?.command;
  if (!command) return;
  const state = loadState(input.session_id);
  state.allowedOnce ??= [];
  const pending = [];

  for (const segment of segments(command)) {
    if (isNpmPeerBypass(segment)) {
      tellClaude(
        `Blocked: \`${segment}\` uses an npm peer-dependency bypass flag. ` +
        `Resolve the compatibility problem instead (${ADD_DEPENDENCY} § npm Peer Conflicts). ` +
        'If the user explicitly wants this flag for another reason, ask them to run the command themselves.',
      );
    }
    const key = hash(segment.replace(/\s+/g, ' '));
    if (state.allowedOnce.includes(key)) continue;
    if (isDependencyCommand(segment)) {
      pending.push({ key, message:
        `Dependency change: \`${segment}\`. Follow the add-dependency workflow (${ADD_DEPENDENCY}) before installing. ` +
        'When its checks are complete, run the same command again.' });
      continue;
    }
    const git = gitOperation(segment);
    if (git === 'destructive') {
      pending.push({ key, message:
        `Destructive Git command: \`${segment}\`. Run it only if the user explicitly requested it (CLAUDE.md § Git), ` +
        `after inspecting what will be lost (${GIT_WORKFLOW} § Destructive Operations). If so, run the same command again.` });
    } else if (git === 'changing') {
      pending.push({ key, message:
        `Repository-changing Git command: \`${segment}\`. Run it only if the user explicitly requested it (CLAUDE.md § Git), ` +
        `after the state checks in ${GIT_WORKFLOW} § Safety. If so, run the same command again.` });
    }
  }

  if (pending.length > 0) {
    state.allowedOnce.push(...pending.map((p) => p.key));
    saveState(input.session_id, state);
    tellClaude(pending.map((p) => p.message).join('\n'));
  }
}

// ---------- PostToolUse ----------

const isManifest = (r) => r.endsWith('.csproj') || /(^|\/)Directory\.Packages\.props$/.test(r) || (/(^|\/)package\.json$/.test(r) && !r.includes('node_modules/'));
const isInstructionFile = (r) => r === 'CLAUDE.md' || r === 'docs/technology-stack.md' || (/^\.claude\//.test(r) && /\.(md|json|mjs)$/.test(r) && !r.endsWith('settings.local.json'));

async function postToolUse(input) {
  const root = projectRoot();
  const tool = input.tool_name ?? '';
  const messages = [];
  let findings = [];

  if (/^(Edit|Write|MultiEdit)$/.test(tool)) {
    const file = input.tool_input?.file_path;
    if (!file) return;
    const r = rel(root, file);
    if (r.startsWith('..')) return;

    if (isManifest(r)) {
      findings.push(...checkDependencies(root, [r]));
      if (r.endsWith('.csproj')) findings.push(...checkArchitecture(root, [r]));
    } else if (r.endsWith('.cs') && /(^|\/)backend\//.test(r)) {
      findings.push(...checkArchitecture(root, [r]));
    }
    if (r === 'SPECIFICATION.md') {
      messages.push('SPECIFICATION.md changed: confirm the change was approved, check CUSTOM_SETTINGS.md for conflicts, and update affected implementation and tests (CLAUDE.md § Product Sources).');
    }
    if (r === 'CUSTOM_SETTINGS.md') {
      messages.push(`CUSTOM_SETTINGS.md changed: run the custom-settings workflow (${CUSTOM_SETTINGS}).`);
    }
    if (isInstructionFile(r)) {
      findings.push(...checkInstructions(root).filter((f) => f.level === 'error'));
    }
  } else if (/^(Bash|PowerShell)$/.test(tool)) {
    const parts = segments(input.tool_input?.command);
    const structural = parts.some((s) => isDependencyCommand(s) || /^dotnet\s+(new|sln)\b/i.test(s) || /^dotnet\s+add\b.*\breference\b/i.test(s) || /^dotnet\s+reference\s+add\b/i.test(s));
    if (!structural) return;
    findings = [
      ...checkDependencies(root),
      ...checkArchitecture(root, walk(root, 'backend', (f) => f.endsWith('.csproj'))),
    ].filter((f) => f.level === 'error');
  } else {
    return;
  }

  if (findings.length > 0) {
    messages.push(`Mechanical check findings (fix errors; confirm warnings are intended):\n${formatFindings(findings)}`);
  }
  if (messages.length > 0) tellClaude(messages.join('\n'));
}

// ---------- Stop ----------

function changedPaths(root) {
  try {
    const output = execFileSync('git', ['status', '--porcelain=v1', '--untracked-files=all'], {
      cwd: root, encoding: 'utf8', timeout: 5000, stdio: ['ignore', 'pipe', 'ignore'],
    });
    return output.split(/\r?\n/).filter(Boolean).map((line) => {
      let p = line.slice(3);
      if (p.includes(' -> ')) p = p.split(' -> ').pop();
      return p.replace(/^"|"$/g, '');
    });
  } catch {
    return null; // not a Git repository or Git unavailable
  }
}

async function stop(input) {
  if (input.stop_hook_active) return;
  const root = projectRoot();
  const changed = changedPaths(root);
  if (!changed || changed.length === 0) return;

  const state = loadState(input.session_id);
  state.reminded ??= {};
  const reminders = [];
  const newTriggers = (kind, files) => {
    const previous = new Set(state.reminded[kind] ?? []);
    const fresh = files.filter((f) => !previous.has(f));
    if (fresh.length > 0) state.reminded[kind] = [...previous, ...fresh];
    return fresh.length > 0;
  };

  const domain = changed.filter((p) => /(^|\/)backend\/[^/]+\.Domain\/.*\.cs$/.test(p));
  const persistence = changed.filter((p) => /(^|\/)backend\/[^/]+\.Infrastructure\/(.*\/)?Persistence\/.*\.cs$/.test(p) && !/\/(Migrations|Seeding)\//.test(p));
  const mapping = changed.filter((p) => /\/Configurations\/.*\.cs$|DbContext\.cs$/.test(p) && /(^|\/)backend\//.test(p));
  const seederChanged = changed.some((p) => /\/Seeding\/|DbSeeder/.test(p));
  const migrationsChanged = changed.some((p) => /(^|\/)backend\/.*\/Migrations\//.test(p));
  const testsChanged = changed.some((p) => /(^|\/)backend\/[^/]*Tests?\//.test(p));
  const production = changed.filter((p) => /(^|\/)backend\/[^/]+\.(Domain|Application|Infrastructure|Api)\/.*\.cs$/.test(p) && !/\/Migrations\//.test(p));

  const backendFiles = walk(root, 'backend', (f) => f.endsWith('.cs') || f.endsWith('.csproj'));
  const seederExists = backendFiles.some((f) => /\/Seeding\/.*\.cs$/.test(f));
  const migrationsExist = backendFiles.some((f) => /\/Migrations\/.*\.cs$/.test(f));
  const testProjectsExist = backendFiles.some((f) => /Tests?\.csproj$/.test(f));

  if (seederExists && !seederChanged && newTriggers('seed', [...domain, ...persistence])) {
    reminders.push('- Domain or persistence code changed without a development seeder change: review the seeder (.claude/rules/persistence.md § Development Seeding).');
  }
  if (migrationsExist && !migrationsChanged && newTriggers('migration', [...domain, ...mapping])) {
    reminders.push('- Entity or mapping code changed without a migration change: decide whether a migration is needed (.claude/rules/persistence.md § Migrations).');
  }
  if (testProjectsExist && !testsChanged && production.length > 0 && !state.reminded.tests) {
    state.reminded.tests = true;
    reminders.push('- Backend production code changed with no test changes: confirm the changed behavior has maintained coverage (.claude/rules/testing.md § Regression and Behavioral Verification).');
  }
  if (changed.includes('CUSTOM_SETTINGS.md')) {
    const contentHash = hash(readText(root, 'CUSTOM_SETTINGS.md') ?? '');
    if (state.reminded.customSettings !== contentHash) {
      state.reminded.customSettings = contentHash;
      reminders.push(`- CUSTOM_SETTINGS.md changed: complete the custom-settings verification (${CUSTOM_SETTINGS} § Verification).`);
    }
  }

  if (reminders.length > 0) {
    saveState(input.session_id, state);
    tellClaude(`Co-change check before finishing:\n${reminders.join('\n')}\nIf an item does not apply, say so briefly and finish.`);
  }
}

// ---------- entry point ----------

const handlers = { 'pre-tool-use': preToolUse, 'post-tool-use': postToolUse, stop };
const handler = handlers[process.argv[2]];

if (handler && exists(projectRoot(), 'CLAUDE.md')) {
  try {
    await handler(await readInput());
  } catch (error) {
    process.stderr.write(`instruction hook error (${process.argv[2]}): ${error.message}\n`);
    process.exit(1);
  }
}
