// Level 3 Project · enforcement asset: Claude Code hook entry point.
// Usage (from .claude/settings.json): node .claude/hooks/claude-hook.mjs <pre-bash|post-bash|post-edit|stop>
// The project root is resolved from this script's location, so no shell-specific variable expansion is
// needed in the hook command. Exit 0 = nothing to report, 2 = feedback for Claude (blocks the tool call
// for pre-bash; asks Claude to continue for stop), 1 = the check could not run (shown to the user).
// Messages point to the owning workflow or rule; they never restate policy.
import { readFileSync, writeFileSync, existsSync } from 'node:fs';
import path from 'node:path';
import { createHash } from 'node:crypto';
import { execFileSync } from 'node:child_process';
import { fileURLToPath, pathToFileURL } from 'node:url';
import { checkManifestFile, declaredPackages, isManifest, scanManifests } from './manifest-checks.mjs';

const EXIT_FEEDBACK = 2;
const EXIT_UNAVAILABLE = 1;

const ADD_DEPENDENCY = '.claude/skills/add-dependency/SKILL.md';
const DEVELOPMENT = '.claude/skills/development-workflow/SKILL.md';
const CUSTOM_SETTINGS = '.claude/skills/custom-settings/SKILL.md';
const TEMPLATE_MAINTENANCE = '.claude/skills/template-maintenance/SKILL.md';

function say(lines) {
  process.stderr.write(lines.map(line => `[project hook] ${line}`).join('\n') + '\n');
}

function unavailable(message) {
  say([message]);
  process.exit(EXIT_UNAVAILABLE);
}

function feedback(lines) {
  say(lines);
  process.exit(EXIT_FEEDBACK);
}

function resolveRoot() {
  const scriptDir = path.dirname(fileURLToPath(import.meta.url));
  const root = path.resolve(scriptDir, '..', '..');
  if (!existsSync(path.join(root, '.claude', 'settings.json')) || !existsSync(path.join(root, 'CLAUDE.md'))) {
    unavailable(`cannot locate the project root from ${scriptDir} (expected CLAUDE.md and .claude/settings.json two levels up).`);
  }
  return root;
}

function readInput() {
  let raw;
  try {
    raw = readFileSync(0, 'utf8');
  } catch (error) {
    unavailable(`cannot read the hook payload from stdin: ${error.message}`);
  }
  raw = raw ?? '';
  if (raw.charCodeAt(0) === 0xfeff) raw = raw.slice(1); // some Windows shells prepend a UTF-8 byte-order mark when piping
  if (!raw.trim()) unavailable('empty hook payload on stdin; expected the Claude Code hook JSON.');
  try {
    return JSON.parse(raw);
  } catch (error) {
    unavailable(`hook payload is not valid JSON: ${error.message}`);
  }
}

function git(root, args) {
  return execFileSync('git', ['-C', root, ...args], { encoding: 'utf8', stdio: ['ignore', 'pipe', 'ignore'] });
}

function inGitWorkTree(root) {
  try {
    return git(root, ['rev-parse', '--is-inside-work-tree']).trim() === 'true';
  } catch {
    return false;
  }
}

function relativeInside(root, file) {
  const abs = path.resolve(root, file);
  const relative = path.relative(root, abs);
  if (!relative || relative.startsWith('..') || path.isAbsolute(relative)) return null;
  return relative.split(path.sep).join('/');
}

// ---------- shell commands ----------

function segments(command) {
  return command
    .split(/&&|\|\||[;|\n]/)
    .map(part => part.trim().split(/\s+/).filter(Boolean).map(token => token.replace(/^["']|["']$/g, '')))
    .filter(tokens => tokens.length > 0);
}

function managerIndex(tokens) {
  return tokens.findIndex(token => /^(npm|pnpm|yarn)(\.cmd|\.exe)?$/i.test(path.basename(token)));
}

function subcommand(tokens, start) {
  return tokens.slice(start + 1).find(token => !token.startsWith('-'))?.toLowerCase();
}

const NPM_CHANGE = new Set(['install', 'i', 'add', 'uninstall', 'un', 'remove', 'rm', 'update', 'up', 'upgrade']);
const NPM_WITH_FLAGS = new Set([...NPM_CHANGE, 'ci', 'dedupe', 'audit']);

function forcedPeerBypass(tokens) {
  const index = managerIndex(tokens);
  if (index < 0 || !NPM_WITH_FLAGS.has(subcommand(tokens, index) ?? '')) return false;
  const rest = tokens.slice(index + 1);
  return rest.some(token => /^(--force|-f|--legacy-peer-deps)(=true)?$/i.test(token));
}

function dependencyChange(tokens) {
  const lower = tokens.map(token => token.toLowerCase());
  const dotnet = lower.findIndex(token => /^dotnet(\.exe)?$/.test(path.basename(token)));
  if (dotnet >= 0) {
    const rest = lower.slice(dotnet + 1);
    if ((rest[0] === 'add' || rest[0] === 'remove') && rest.includes('package')) return 'package';
    if (rest[0] === 'package' && ['add', 'remove', 'update'].includes(rest[1])) return 'package';
    if ((rest[0] === 'add' || rest[0] === 'remove') && rest.includes('reference')) return 'reference';
    if (rest[0] === 'reference' && ['add', 'remove'].includes(rest[1])) return 'reference';
  }
  const ng = lower.findIndex(token => /^ng(\.cmd)?$/.test(path.basename(token)));
  if (ng >= 0 && lower[ng + 1] === 'add') return 'package';
  const manager = managerIndex(tokens);
  if (manager >= 0) {
    const sub = subcommand(tokens, manager);
    if (!NPM_CHANGE.has(sub ?? '')) return null;
    if (['update', 'up', 'upgrade', 'uninstall', 'un', 'remove', 'rm'].includes(sub)) return 'package';
    const subIndex = tokens.findIndex((token, i) => i > manager && token.toLowerCase() === sub);
    const packageArgs = tokens.slice(subIndex + 1).filter(token => !token.startsWith('-'));
    if (packageArgs.length > 0) return 'package';
  }
  return null;
}

function preBash(input) {
  const command = input?.tool_input?.command;
  if (typeof command !== 'string') return;
  const forced = segments(command).find(forcedPeerBypass);
  if (forced) {
    feedback([
      `Blocked: '${forced.join(' ')}' bypasses peer-dependency compatibility.`,
      `Resolve the conflict as ${ADD_DEPENDENCY} (Install) describes. If the user explicitly decides to override, the user runs the command.`,
    ]);
  }
}

function postBash(root, input) {
  const command = input?.tool_input?.command;
  if (typeof command !== 'string') return;
  const changes = segments(command).map(tokens => ({ tokens, kind: dependencyChange(tokens) })).filter(item => item.kind);
  if (changes.length === 0) return;
  const lines = [];
  if (changes.some(change => change.kind === 'package')) {
    lines.push(`Dependency change detected: '${changes.find(c => c.kind === 'package').tokens.join(' ')}'.`);
    lines.push(`This change is owned by ${ADD_DEPENDENCY}: confirm its version, deprecation, vulnerability, and license steps were completed and report them.`);
  }
  const problems = scanManifests(root);
  if (problems.length > 0) lines.push('Manifest check findings:', ...problems.map(problem => `  - ${problem}`));
  if (lines.length > 0) feedback(lines);
}

// ---------- file edits ----------

function changedPackages(root, relative) {
  if (!inGitWorkTree(root)) return null;
  let previous = '';
  try {
    previous = git(root, ['show', `HEAD:${relative}`]);
  } catch {
    previous = ''; // new file or no commits yet
  }
  const current = readFileSync(path.join(root, relative), 'utf8');
  const before = declaredPackages(relative, previous);
  const after = declaredPackages(relative, current);
  const changed = [];
  for (const [id, version] of after) {
    if (!before.has(id)) changed.push(`added ${id}`);
    else if (before.get(id) !== version) changed.push(`changed ${id}`);
  }
  for (const id of before.keys()) if (!after.has(id)) changed.push(`removed ${id}`);
  return changed;
}

async function postEdit(root, input) {
  const target = input?.tool_input?.file_path ?? input?.tool_input?.path;
  if (typeof target !== 'string' || !target) return;
  const relative = relativeInside(root, target);
  if (!relative) return;

  if (relative === 'SPECIFICATION.md' || relative === 'CUSTOM_SETTINGS.md') {
    feedback([
      `${relative} changed (product input).`,
      `Keep SPECIFICATION.md and CUSTOM_SETTINGS.md consistent (CLAUDE.md → Product governance). CUSTOM_SETTINGS.md changes run ${CUSTOM_SETTINGS}; approved behavior changes follow ${DEVELOPMENT} (Implement → approved product decisions).`,
    ]);
  }

  if (isManifest(relative) && !/(^|\/)(node_modules|bin|obj)\//.test(relative)) {
    const lines = checkManifestFile(root, path.join(root, relative)).map(problem => `  - ${problem}`);
    const changed = relative.endsWith('.npmrc') ? [] : changedPackages(root, relative);
    if (changed && changed.length > 0) {
      lines.unshift(`Dependency change in ${relative}: ${changed.join(', ')} → follow ${ADD_DEPENDENCY} and report its checks.`);
    }
    if (lines.length > 0) {
      if (changed === null) lines.push('  - (dependency-change detection unavailable: not a Git work tree)');
      feedback([`Manifest check for ${relative}:`, ...lines]);
    }
    if (changed === null) {
      unavailable(`dependency-change detection for ${relative} is unavailable (not a Git work tree); static manifest checks passed.`);
    }
    return;
  }

  if (relative === 'CLAUDE.md' || (relative.startsWith('.claude/') && /\.(md|json|mjs)$/.test(relative) && !relative.startsWith('.claude/settings.local'))) {
    const checker = pathToFileURL(path.join(root, '.claude', 'tools', 'check-instructions.mjs')).href;
    const { checkInstructions } = await import(checker);
    const result = checkInstructions(root);
    if (result.errors.length > 0) {
      feedback([
        `Instruction-structure check failed after editing ${relative} (${TEMPLATE_MAINTENANCE}):`,
        ...result.errors.map(error => `  - ${error}`),
      ]);
    }
  }
}

// ---------- stop ----------

const PATTERNS = {
  model: /^backend\/[^/]+\.Domain\/.+\.cs$|^backend\/[^/]+\.Infrastructure\/(.+\/)?Persistence\/(Configurations\/.+\.cs|[^/]*DbContext\.cs)$/,
  seeder: /^backend\/[^/]+\.Infrastructure\/(.+\/)?Seeding\/.+\.cs$/,
  migration: /^backend\/[^/]+\.Infrastructure\/(.+\/)?Migrations\/.+\.cs$/,
  backendTest: /^backend\/[^/]*Tests\/.+\.cs$/,
  backendCode: /^backend\/[^/]+\/.+\.cs$/,
  frontendTest: /^frontend\/.+\.spec\.ts$/,
  frontendCode: /^frontend\/[^/]+\/src\/.+\.ts$/,
};

function changedFiles(root) {
  const output = git(root, ['status', '--porcelain=v1', '-uall', '-z']);
  const entries = output.split('\0').filter(Boolean);
  const files = [];
  for (let i = 0; i < entries.length; i += 1) {
    const status = entries[i].slice(0, 2);
    files.push({ status, file: entries[i].slice(3) });
    if (status.includes('R') || status.includes('C')) i += 1; // skip the rename/copy source path
  }
  return files;
}

function stop(root, input) {
  if (input?.stop_hook_active) return; // Claude is already continuing because of a Stop hook: never loop.
  if (!inGitWorkTree(root)) unavailable('co-change reminders are unavailable: the project is not a Git work tree.');

  const files = changedFiles(root);
  const paths = files.map(entry => entry.file);
  const has = pattern => paths.some(file => pattern.test(file));
  const productionBackend = paths.some(file => PATTERNS.backendCode.test(file) && !PATTERNS.backendTest.test(file) && !PATTERNS.migration.test(file));
  const productionFrontend = paths.some(file => PATTERNS.frontendCode.test(file) && !PATTERNS.frontendTest.test(file));

  const reminders = [];
  if (has(PATTERNS.model) && !has(PATTERNS.seeder)) {
    reminders.push(`Domain/persistence model files changed without a seeder change: confirm seeded entities are unaffected or update the seeder (${DEVELOPMENT} → Co-changes).`);
  }
  if (has(PATTERNS.migration)) {
    reminders.push(`Migration files changed: review each generated migration before committing (${DEVELOPMENT} → Co-changes).`);
  }
  if ((productionBackend || productionFrontend) && !has(PATTERNS.backendTest) && !has(PATTERNS.frontendTest)) {
    reminders.push(`Production code changed without test changes: confirm equivalent coverage exists or add tests (${DEVELOPMENT} → Implement; verify step 4).`);
  }
  if (paths.includes('CUSTOM_SETTINGS.md')) {
    reminders.push(`CUSTOM_SETTINGS.md changed: run ${CUSTOM_SETTINGS} to synchronize every affected surface.`);
  }
  if (reminders.length === 0) return;

  const fingerprint = createHash('sha256')
    .update(JSON.stringify({ files: files.map(entry => `${entry.status} ${entry.file}`).sort(), reminders }))
    .digest('hex');
  const stateFile = path.resolve(root, git(root, ['rev-parse', '--git-path', 'claude-stop-reminders.json']).trim());
  try {
    if (existsSync(stateFile) && JSON.parse(readFileSync(stateFile, 'utf8')).fingerprint === fingerprint) return;
  } catch {
    // An unreadable state file is replaced below.
  }
  try {
    writeFileSync(stateFile, JSON.stringify({ fingerprint, at: new Date().toISOString() }));
  } catch (error) {
    unavailable(`cannot record the reminder state in ${stateFile}: ${error.message}`);
  }
  feedback([
    'Before finishing, check these co-change reminders:',
    ...reminders.map(reminder => `  - ${reminder}`),
    'Address each one or state why it does not apply; this reminder is not repeated for the same set of changes.',
  ]);
}

// ---------- main ----------

const event = process.argv[2];
const handlers = {
  'pre-bash': (root, input) => preBash(input),
  'post-bash': postBash,
  'post-edit': postEdit,
  stop,
};

if (!handlers[event]) {
  unavailable(`unknown hook event '${event ?? ''}'; expected one of: ${Object.keys(handlers).join(', ')}.`);
}

const projectRoot = resolveRoot();
const payload = readInput();
await handlers[event](projectRoot, payload);
process.exit(0);
