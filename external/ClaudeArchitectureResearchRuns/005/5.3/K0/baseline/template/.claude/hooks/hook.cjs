// Kind: ENF | Scope: repo/meta | Owner: Claude Code hook dispatcher — dependency-command routing, manifest and instruction checks after edits, product-input reminders, co-change reminders at stop | Loading: hook events configured in .claude/settings.json
//
// Usage: node .claude/hooks/hook.cjs <pre-tool-use|post-tool-use|stop>  (hook input JSON on stdin)
// Output: findings are returned as Claude Code hook JSON on stdout with exit code 0 (pre-tool-use:
// permissionDecision "deny"; post-tool-use and stop: decision "block" with a reason for Claude), so the
// result does not depend on how the launching shell (cmd, PowerShell, bash) propagates exit codes.
// Exit code 1 with a message on stderr means the hook itself could not run.
// Messages point to the owning workflow or standard; they do not restate policy.
'use strict';

const fs = require('fs');
const path = require('path');
const { spawnSync } = require('child_process');

const PROJECT_DIR = path.resolve(__dirname, '..', '..');
const EVENTS = ['pre-tool-use', 'post-tool-use', 'stop'];
const REVIEW_MARKER = /#\s*add-dependency:\s*reviewed\b/i;

function fail(message) {
  process.stderr.write(`[hook] ${message}\n`);
  process.exit(1);
}

function feedback(event, lines) {
  const reason = lines.join('\n');
  const output = event === 'pre-tool-use'
    ? { hookSpecificOutput: { hookEventName: 'PreToolUse', permissionDecision: 'deny', permissionDecisionReason: reason } }
    : { decision: 'block', reason };
  process.stdout.write(`${JSON.stringify(output)}\n`);
  process.exit(0);
}

function readInput() {
  let raw = '';
  try {
    raw = fs.readFileSync(0, 'utf8');
  } catch (error) {
    fail(`cannot read hook input from stdin: ${error.message}`);
  }
  if (!raw.trim()) return {};
  try {
    return JSON.parse(raw);
  } catch (error) {
    fail(`hook input is not valid JSON: ${error.message}`);
  }
  return {};
}

function loadScript(name) {
  const file = path.join(PROJECT_DIR, '.claude', 'scripts', name);
  if (!fs.existsSync(file)) fail(`required script is missing: ${path.relative(PROJECT_DIR, file)}`);
  return require(file);
}

// ---------------------------------------------------------------------------
// pre-tool-use: dependency-changing shell commands are routed to add-dependency
// ---------------------------------------------------------------------------

const NPM_VALUE_FLAGS = new Set(['--prefix', '--workspace', '-w', '--registry', '--cache', '--loglevel', '--userconfig', '--location', '--tag']);

function tokenize(segment) {
  const withoutComment = segment.replace(/(^|\s)#.*$/, '');
  return withoutComment.match(/"[^"]*"|'[^']*'|\S+/g)?.map((t) => t.replace(/^["']|["']$/g, '')) ?? [];
}

function baseName(token) {
  return token.toLowerCase().split(/[\\/]/).pop().replace(/\.(exe|cmd|ps1)$/, '');
}

function npmChangesPackages(args) {
  const sub = (args[0] ?? '').toLowerCase();
  if (['update', 'up', 'upgrade', 'udpate'].includes(sub)) return true;
  if (!['install', 'i', 'add', 'in', 'ins', 'inst', 'isntall'].includes(sub)) return false;
  for (let i = 1; i < args.length; i += 1) {
    const arg = args[i];
    if (NPM_VALUE_FLAGS.has(arg)) { i += 1; continue; }
    if (arg.startsWith('-')) continue;
    return true; // a package specifier
  }
  return false; // plain "npm install" restores from the lockfile
}

function detectDependencyCommands(command) {
  const hits = [];
  for (const segment of command.split(/&&|\|\||;|\||\r?\n/)) {
    const tokens = tokenize(segment);
    for (let i = 0; i < tokens.length; i += 1) {
      const t = baseName(tokens[i]);
      const next = (tokens[i + 1] ?? '').toLowerCase();
      const rest = tokens.slice(i + 1).map((x) => x.toLowerCase());
      if (t === 'dotnet') {
        if (next === 'add' && rest.slice(1, 3).includes('package')) hits.push(segment.trim());
        if (next === 'package' && ['add', 'update'].includes(rest[1])) hits.push(segment.trim());
      } else if (t === 'npm' && npmChangesPackages(tokens.slice(i + 1))) {
        hits.push(segment.trim());
      } else if (t === 'ng' && ['add', 'update'].includes(next)) {
        hits.push(segment.trim());
      } else if (t === 'npx' && next === 'ng' && ['add', 'update'].includes(rest[1])) {
        hits.push(segment.trim());
      } else if ((t === 'yarn' && ['add', 'upgrade', 'up'].includes(next)) || (t === 'pnpm' && ['add', 'update', 'up'].includes(next))) {
        hits.push(segment.trim());
      } else if (t === 'nuget' && ['install', 'update'].includes(next)) {
        hits.push(segment.trim());
      } else if (['install-package', 'update-package'].includes(t)) {
        hits.push(segment.trim());
      }
    }
  }
  return [...new Set(hits)];
}

function preToolUse(input) {
  if (!['Bash', 'PowerShell'].includes(input.tool_name)) return;
  const command = String(input.tool_input?.command ?? '');
  const hits = detectDependencyCommands(command);
  if (hits.length === 0 || REVIEW_MARKER.test(command)) return;
  feedback('pre-tool-use', [
    `Dependency change detected: ${hits.join(' | ')}`,
    'Run the `add-dependency` workflow first (.claude/skills/add-dependency/SKILL.md).',
    'When its checks are complete, re-run the command with the trailing comment `# add-dependency: reviewed`.',
  ]);
}

// ---------------------------------------------------------------------------
// post-tool-use: checks after a file was written or edited
// ---------------------------------------------------------------------------

function toProjectPath(filePath) {
  if (!filePath) return null;
  const absolute = path.resolve(PROJECT_DIR, String(filePath));
  const relative = path.relative(PROJECT_DIR, absolute);
  if (!relative || relative.startsWith('..') || path.isAbsolute(relative)) return null;
  return relative.split(path.sep).join('/');
}

function isInstructionPath(rel) {
  return rel === 'CLAUDE.md'
    || rel === 'docs/architecture/decision-register.md'
    || (rel.startsWith('.claude/') && !rel.startsWith('.claude/.hook-state/'));
}

function postToolUse(input) {
  if (!['Edit', 'Write', 'MultiEdit', 'NotebookEdit'].includes(input.tool_name)) return;
  const rel = toProjectPath(input.tool_input?.file_path ?? input.tool_input?.notebook_path);
  if (!rel) return;
  const messages = [];

  const manifests = loadScript('check-dependencies.cjs');
  if (manifests.isManifest(rel)) {
    const result = manifests.checkFile(PROJECT_DIR, rel);
    for (const e of result.errors) messages.push(`[manifest] ${e}`);
    for (const n of result.notices) messages.push(`[manifest notice] ${n}`);
  }

  if (rel === 'CUSTOM_SETTINGS.md') {
    messages.push('CUSTOM_SETTINGS.md changed: run the `custom-settings` workflow to synchronize every affected surface (rules: CLAUDE.md § Product sources).');
  }
  if (rel === 'SPECIFICATION.md') {
    messages.push('SPECIFICATION.md changed: confirm it stays consistent with CUSTOM_SETTINGS.md and records only approved behavior (CLAUDE.md § Product sources).');
  }

  if (isInstructionPath(rel)) {
    const result = loadScript('check-instructions.cjs').check(PROJECT_DIR);
    for (const e of result.errors) messages.push(`[instructions] ${e}`);
  }

  if (messages.length > 0) feedback('post-tool-use', messages);
}

// ---------------------------------------------------------------------------
// stop: co-change reminders (seed data, migrations, tests, custom settings)
// ---------------------------------------------------------------------------

function changedPaths() {
  const result = spawnSync('git', ['status', '--porcelain=v1', '-z', '--untracked-files=all'], {
    cwd: PROJECT_DIR,
    encoding: 'utf8',
    windowsHide: true,
  });
  if (result.error) fail(`co-change check could not run git: ${result.error.message}`);
  if (result.status !== 0) {
    fail(`co-change check skipped: ${PROJECT_DIR} is not a Git work tree (${(result.stderr || '').trim()}).`);
  }
  const entries = result.stdout.split('\0').filter(Boolean);
  const paths = [];
  for (let i = 0; i < entries.length; i += 1) {
    const status = entries[i].slice(0, 2);
    paths.push(entries[i].slice(3).replace(/\\/g, '/'));
    if (status.includes('R') || status.includes('C')) i += 1; // skip the original path of a rename/copy
  }
  return paths;
}

function findFile(dir, name, depth = 0) {
  if (depth > 6 || !fs.existsSync(dir)) return false;
  for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
    if (['bin', 'obj', 'node_modules', '.git'].includes(entry.name)) continue;
    const full = path.join(dir, entry.name);
    if (entry.isFile() && entry.name === name) return true;
    if (entry.isDirectory() && findFile(full, name, depth + 1)) return true;
  }
  return false;
}

function stop(input) {
  if (input.stop_hook_active) return; // never loop on our own continuation
  const paths = changedPaths();
  const isTest = (p) => /(^|\/)[^/]*Tests\//.test(p) || /\.spec\.ts$/.test(p);
  const reminders = [];

  const model = paths.filter((p) => /^backend\/[^/]+\.Domain\/.+\.cs$/.test(p)
    || /^backend\/[^/]+\.Infrastructure\/Persistence\/(Configurations\/.+|AppDbContext)\.cs$/.test(p));
  const seeder = paths.filter((p) => /\/Seeding\//.test(p) || /DbSeeder\.cs$/.test(p));
  if (model.length > 0 && seeder.length === 0 && findFile(path.join(PROJECT_DIR, 'backend'), 'DbSeeder.cs')) {
    reminders.push({ key: `seed:${model.join(',')}`, text: 'Domain/persistence model changed without a seeder change: confirm seeded entities are unaffected or update the development seeder (`development-workflow` § Persistence or model change).' });
  }

  const migrations = paths.filter((p) => /^backend\/.+\/Migrations\/[^/]+\.cs$/.test(p) && !/(\.Designer|ModelSnapshot)\.cs$/.test(p));
  if (migrations.length > 0) {
    reminders.push({ key: `migration:${migrations.join(',')}`, text: `Migration added or changed (${migrations.join(', ')}): review it before committing (\`development-workflow\` § Persistence or model change).` });
  }

  const production = paths.filter((p) => (/^backend\/.+\.cs$/.test(p) || /^frontend\/.+\.ts$/.test(p)) && !isTest(p) && !/\/Migrations\//.test(p));
  if (production.length > 0 && !paths.some(isTest)) {
    reminders.push({ key: `tests:${production.join(',')}`, text: 'Production code changed without test changes: confirm existing coverage or add tests (`development-workflow` § Bug fix, `verify` § 4).' });
  }

  if (paths.includes('CUSTOM_SETTINGS.md')) {
    reminders.push({ key: 'custom-settings', text: 'CUSTOM_SETTINGS.md changed: confirm the `custom-settings` workflow synchronized every affected surface.' });
  }

  if (reminders.length === 0) return;

  const fingerprint = reminders.map((r) => r.key).sort().join('|');
  const stateDir = path.join(PROJECT_DIR, '.claude', '.hook-state');
  const stateFile = path.join(stateDir, 'stop-reminders.txt');
  try {
    if (fs.existsSync(stateFile) && fs.readFileSync(stateFile, 'utf8') === fingerprint) return; // already reminded
    fs.mkdirSync(stateDir, { recursive: true });
    fs.writeFileSync(path.join(stateDir, '.gitignore'), '*\n');
    fs.writeFileSync(stateFile, fingerprint);
  } catch (error) {
    process.stderr.write(`[hook] could not persist reminder state: ${error.message}\n`);
  }
  feedback('stop', ['Co-change check before finishing:', ...reminders.map((r) => `- ${r.text}`)]);
}

// ---------------------------------------------------------------------------

function main() {
  const event = process.argv.slice(1).find((arg) => EVENTS.includes(arg));
  if (!event) fail(`missing or unknown hook event; expected one of: ${EVENTS.join(', ')}`);
  const input = readInput();
  if (event === 'pre-tool-use') preToolUse(input);
  else if (event === 'post-tool-use') postToolUse(input);
  else stop(input);
  process.exit(0);
}

if (require.main === module || process.argv.slice(1).some((arg) => EVENTS.includes(arg))) {
  main();
}

module.exports = { detectDependencyCommands };
