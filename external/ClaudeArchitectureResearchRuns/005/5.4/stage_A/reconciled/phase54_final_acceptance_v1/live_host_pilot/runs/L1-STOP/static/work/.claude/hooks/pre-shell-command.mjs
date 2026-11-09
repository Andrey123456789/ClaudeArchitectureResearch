#!/usr/bin/env node
// PreToolUse (Bash|PowerShell), critical, fail-closed (settings: onFailure "block"):
// - peer-dependency bypass flags (--force, -f, --legacy-peer-deps) and npm_config_* equivalents → denied (add-dependency);
// - project-reference graph changes (dotnet add/remove ... reference, dotnet reference add/remove) → ask:
//   a Reserved decision unless it implements the approved layout (project-structure, architecture-decision);
// - dependency changes (dotnet/NuGet packages and tools, npm/pnpm/yarn, and the selected frontend module's CLI
//   dependency commands from frontend.enforcement) → denied once with a
//   pointer to add-dependency; the identical command is allowed when retried within the grace window.
// - repository-changing Git commands → ask (read-only Git runs without a prompt); a deny always wins;
// Empty, malformed, or incomplete input and any internal failure block the command (exit 2).
import { existsSync, mkdirSync, readFileSync, writeFileSync } from 'node:fs';
import path from 'node:path';
import { hookStateDir, loadJsonFacet, parseSelection, readStdinJson, resolveRoots } from '../scripts/lib/project.mjs';

const GRACE_MS = 30 * 60 * 1000;

// Options that consume the following token when written without '='.
const VALUE_OPTIONS = {
  dotnet: new Set(['--additionalprobingpath', '--additional-deps', '--depsfile', '--runtimeconfig', '--fx-version', '--roll-forward', '--roll-forward-on-no-candidate-fx']),
  npm: new Set(['--prefix', '-C', '--workspace', '-w', '--registry', '--cache', '--userconfig', '--globalconfig', '--loglevel', '--tag', '--omit', '--include', '--install-strategy', '--save-prefix', '--otp', '--scope', '--location']),
  pnpm: new Set(['--dir', '-C', '--filter', '-F', '--workspace-dir', '--reporter', '--store-dir', '--virtual-store-dir', '--loglevel', '--registry']),
  yarn: new Set(['--cwd', '--registry', '--cache-folder', '--modules-folder', '--mutex', '--network-timeout']),
};
const FORCE_FLAGS = new Set(['--force', '-f', '--legacy-peer-deps', '--legacy-peer-deps=true']);
const NODE_DEPENDENCY = {
  npm: { add: ['install', 'i', 'in', 'ins', 'inst', 'add', 'isnt'], always: ['uninstall', 'un', 'unlink', 'remove', 'rm', 'r', 'update', 'up', 'upgrade', 'udpate'] },
  pnpm: { add: ['install', 'i'], always: ['add', 'remove', 'rm', 'un', 'uninstall', 'update', 'up', 'upgrade'] },
  yarn: { add: [], always: ['add', 'remove', 'upgrade', 'up', 'upgrade-interactive'] },
};
const INSTALL_LIKE = new Set(['install', 'i', 'in', 'add', 'ci', 'update', 'up', 'upgrade', 'uninstall', 'remove', 'rm', 'un']);

// Splits on unquoted &&, ||, ;, |, & and newlines.
function segments(command) {
  const out = [];
  let cur = '';
  let quote = null;
  for (let i = 0; i < command.length; i++) {
    const c = command[i];
    if (quote) { cur += c; if (c === quote) quote = null; continue; }
    if (c === '"' || c === "'") { quote = c; cur += c; continue; }
    if (c === ';' || c === '\n' || c === '\r' || c === '|' || c === '&') {
      if (c === '&' && cur.trim() === '') { cur += c; continue; } // PowerShell call operator
      out.push(cur); cur = '';
      if ((c === '&' || c === '|') && command[i + 1] === c) i++;
      continue;
    }
    cur += c;
  }
  out.push(cur);
  return out.map((s) => s.trim()).filter(Boolean);
}

function tokens(segment) {
  const out = [];
  const re = /"([^"]*)"|'([^']*)'|(\S+)/g;
  let m;
  while ((m = re.exec(segment))) out.push(m[1] !== undefined ? m[1] : m[2] !== undefined ? m[2] : m[3]);
  return out;
}

function exeName(token) {
  return String(token || '').split(/[\\/]/).pop().toLowerCase().replace(/\.(exe|cmd|bat|ps1)$/, '');
}

function splitArgs(kind, args) {
  const flags = [];
  const positionals = [];
  for (let i = 0; i < args.length; i++) {
    const a = args[i];
    if (a.startsWith('-')) {
      const flag = a.startsWith('--') ? a.toLowerCase() : a; // short options are case-sensitive (-F filter vs -f force)
      flags.push(flag);
      if (!flag.includes('=') && VALUE_OPTIONS[kind] && VALUE_OPTIONS[kind].has(flag)) i++;
    } else positionals.push(a);
  }
  return { flags, positionals };
}

function dotnetVerdict(args, out) {
  const { positionals } = splitArgs('dotnet', args);
  const [sub, a1, a2] = positionals.map((p) => p.toLowerCase());
  if (sub === 'add' || sub === 'remove') {
    const noun = a1 === 'package' || a1 === 'reference' ? a1 : a2;
    if (noun === 'package') out.dependency = true;
    if (noun === 'reference') out.reference = true;
  } else if (sub === 'package' && ['add', 'remove', 'update'].includes(a1)) out.dependency = true;
  else if (sub === 'reference' && ['add', 'remove'].includes(a1)) out.reference = true;
  else if (sub === 'tool' && ['install', 'update', 'uninstall'].includes(a1)) out.dependency = true;
}

function nodeVerdict(kind, args, out) {
  const { flags, positionals } = splitArgs(kind, args);
  let pos = positionals.map((p) => p.toLowerCase());
  if (kind === 'yarn' && pos[0] === 'workspace') pos = pos.slice(2);
  if (kind === 'yarn' && pos[0] === 'global') pos = pos.slice(1);
  const sub = pos[0] || (kind === 'yarn' ? 'install' : '');
  if (kind === 'npm' && sub === 'config' && pos[1] === 'set' && /^(legacy-peer-deps|force)(=true)?$/.test(pos[2] || '') && (pos[2].includes('=') || pos[3] === 'true')) out.force = true;
  if (flags.some((f) => FORCE_FLAGS.has(f)) && (INSTALL_LIKE.has(sub) || (kind === 'yarn' && !pos[0]))) out.force = true;
  const table = NODE_DEPENDENCY[kind];
  if (table.always.includes(sub)) out.dependency = true;
  if (table.add.includes(sub) && pos.length > 1) out.dependency = true;
  if (kind === 'npm' && sub === 'audit' && pos[1] === 'fix') out.dependency = true;
}

function analyze(tks, out, cli, depth = 0) {
  let t = [...tks];
  while (t.length && (/^[A-Za-z_][A-Za-z0-9_]*=/.test(t[0]) || ['&', 'sudo', 'env', 'time', 'call', 'exec', 'command'].includes(t[0].toLowerCase()))) t.shift();
  if (!t.length || depth > 3) return;
  const exe = exeName(t[0]);
  const rest = t.slice(1);
  if (['bash', 'sh', 'zsh', 'pwsh', 'powershell'].includes(exe)) {
    const i = rest.findIndex((a) => /^-(c|command)$/i.test(a));
    if (i >= 0) for (const seg of segments(rest.slice(i + 1).join(' '))) analyze(tokens(seg), out, cli, depth + 1);
    return;
  }
  if (exe === 'cmd') {
    const i = rest.findIndex((a) => /^\/[ck]$/i.test(a));
    if (i >= 0) analyze(rest.slice(i + 1), out, cli, depth + 1);
    return;
  }
  if (exe === 'npx' || exe === 'corepack') {
    const pkg = rest.filter((a) => !a.startsWith('-'));
    analyze(pkg.length && cli.packages[pkg[0].toLowerCase()] ? [cli.packages[pkg[0].toLowerCase()], ...pkg.slice(1)] : pkg, out, cli, depth + 1);
    return;
  }
  if (exe === 'git') {
    const sub = classifyGit(rest);
    if (sub) out.git.push({ sub, text: t.join(' ') });
    return;
  }
  if (exe === 'dotnet') dotnetVerdict(rest, out);
  else if (exe === 'npm' || exe === 'pnpm' || exe === 'yarn') nodeVerdict(exe, rest, out);
  else if (cli.commands[exe] && cli.commands[exe].includes((rest[0] || '').toLowerCase())) out.dependency = true;
  else if (['install-package', 'update-package', 'uninstall-package'].includes(exe)) out.dependency = true;
}

// Framework CLI dependency commands come from the selected frontend module (none when the slot is cleared).
function frontendCli(config) {
  const facet = loadJsonFacet(config, parseSelection(config), 'frontend', 'enforcement');
  const lower = (obj) => Object.fromEntries(Object.entries(obj || {}).map(([k, v]) => [k.toLowerCase(), v]));
  return { commands: lower(facet && facet.dependencyCommands), packages: lower(facet && facet.cliPackages) };
}

// ---------- Git: repository-changing vs read-only (PV2-01) ----------
// The same table as K0's pre-command hook. Read-only commands such as git status, git diff or git log run
// without a Git prompt; any other subcommand, unrecognized ones included, is repository-changing and asks the
// user to confirm. Global options (-C <path>, -c <key=value>, --git-dir ...) are skipped first. The ask is not
// authorization: the Git rule in CLAUDE.md still decides whether the operation may run at all.
const GIT_GLOBAL_VALUE_OPTIONS = new Set(['-C', '-c', '--git-dir', '--work-tree', '--namespace', '--config-env', '--exec-path']);
const GIT_READ_ONLY = new Set([
  'status', 'diff', 'log', 'show', 'blame', 'annotate', 'grep', 'ls-files', 'ls-tree', 'ls-remote', 'rev-parse', 'rev-list',
  'describe', 'shortlog', 'cat-file', 'show-ref', 'for-each-ref', 'merge-base', 'name-rev', 'help', 'version', 'var',
  'check-ignore', 'check-attr', 'check-ref-format', 'check-mailmap', 'count-objects', 'fsck', 'whatchanged', 'range-diff',
  'difftool', 'format-patch', 'archive', 'verify-commit', 'verify-tag', 'cherry', 'show-branch', 'diff-tree', 'diff-files',
  'diff-index', 'request-pull', 'patch-id',
]);
// Commands whose effect depends on their arguments: read-only only in the listed forms.
const GIT_CONDITIONAL = {
  branch: (args) => !gitHasAny(args, ['-d', '-D', '--delete', '-m', '-M', '--move', '-c', '-C', '--copy', '-u', '--set-upstream-to', '--unset-upstream', '--edit-description', '-f', '--force', '-t', '--track', '--no-track'])
    && (gitHasAny(args, ['-l', '--list', '-a', '--all', '-r', '--remotes', '--contains', '--no-contains', '--merged', '--no-merged', '--points-at', '--show-current', '-v', '-vv', '--verbose', '--format', '--sort'])
      || gitPositionals(args, new Set()).length === 0),
  tag: (args) => !gitHasAny(args, ['-d', '--delete', '-a', '--annotate', '-s', '--sign', '-u', '--local-user', '-f', '--force', '-m', '--message', '-F', '--file'])
    && (gitHasAny(args, ['-l', '--list', '-n', '--contains', '--no-contains', '--merged', '--no-merged', '--points-at', '--sort', '--format', '-v', '--verify'])
      || gitPositionals(args, new Set()).length === 0),
  stash: (args) => ['list', 'show'].includes(gitPositionals(args, new Set())[0]),
  worktree: (args) => gitPositionals(args, new Set())[0] === 'list',
  remote: (args) => { const [sub] = gitPositionals(args, new Set()); return sub === undefined || ['show', 'get-url'].includes(sub); },
  config: (args) => gitHasAny(args, ['--get', '--get-all', '--get-regexp', '--get-urlmatch', '--list', '-l'])
    || (['get', 'list'].includes(gitPositionals(args, new Set())[0]))
    || (!gitHasAny(args, ['--unset', '--unset-all', '--add', '--replace-all', '--rename-section', '--remove-section', '-e', '--edit'])
      && gitPositionals(args, new Set(['--file', '-f', '--type', '--default'])).length === 1),
  notes: (args) => { const [sub] = gitPositionals(args, new Set()); return sub === undefined || ['list', 'show'].includes(sub); },
  reflog: (args) => { const [sub] = gitPositionals(args, new Set()); return sub === undefined || !['expire', 'delete'].includes(sub); },
  submodule: (args) => { const [sub] = gitPositionals(args, new Set()); return sub === undefined || ['status', 'summary'].includes(sub); },
  'symbolic-ref': (args) => !gitHasAny(args, ['-d', '--delete']) && gitPositionals(args, new Set(['-m'])).length <= 1,
  bisect: (args) => ['log', 'visualize', 'view', 'terms'].includes(gitPositionals(args, new Set())[0]),
  'sparse-checkout': (args) => gitPositionals(args, new Set())[0] === 'list',
  apply: (args) => gitHasAny(args, ['--check', '--stat', '--numstat', '--summary']) && !gitHasAny(args, ['--index', '--cached', '--apply', '-3', '--3way']),
  checkout: (args) => args.length === 0,
  'hash-object': (args) => !gitHasAny(args, ['-w']),
};

function gitHasAny(args, flags) {
  return args.some((a) => flags.includes(a) || flags.some((f) => f.startsWith('--') && a.startsWith(`${f}=`)));
}

// Positional arguments, skipping options and the values of options that take one.
function gitPositionals(args, valueOptions) {
  const positionals = [];
  for (let i = 0; i < args.length; i += 1) {
    const arg = args[i];
    if (arg === '--') { positionals.push(...args.slice(i + 1)); break; }
    if (arg.startsWith('-')) {
      if (valueOptions.has(arg)) i += 1;
      continue;
    }
    positionals.push(arg);
  }
  return positionals;
}

// args: the words after `git`. Returns the repository-changing subcommand, or null when the command is read-only.
function classifyGit(args) {
  let i = 0;
  while (i < args.length && args[i].startsWith('-')) {
    if (['--version', '--help', '-h', '--html-path', '--man-path', '--info-path'].includes(args[i])) return null;
    i += GIT_GLOBAL_VALUE_OPTIONS.has(args[i]) ? 2 : 1;
  }
  const sub = (args[i] ?? '').toLowerCase();
  if (!sub || GIT_READ_ONLY.has(sub)) return null;
  const rest = args.slice(i + 1);
  if (GIT_CONDITIONAL[sub] && GIT_CONDITIONAL[sub](rest)) return null;
  return sub;
}

// The ask reason for repository-changing Git commands: hits are [{ sub, text }].
function gitAskReason(hits) {
  return `Repository-changing Git command (${[...new Set(hits.map((h) => h.sub))].join(', ')}): ${hits.map((h) => h.text).join(' | ')}. ` +
    'Run it only when the user explicitly requested it or pre-approved this operation and scope (CLAUDE.md, Git); this prompt is not that authority. Procedure: git-workflow.';
}
// ---------- end of Git table (PV2-01) ----------

export function classify(command, cli = { commands: {}, packages: {} }) {
  const out = { dependency: false, reference: false, force: false, git: [] };
  for (const seg of segments(String(command || ''))) analyze(tokens(seg), out, cli);
  return out;
}

function decide(decision, reason) {
  process.stdout.write(JSON.stringify({
    hookSpecificOutput: { hookEventName: 'PreToolUse', permissionDecision: decision, permissionDecisionReason: reason },
  }));
  process.exit(0);
}

function block(reason) {
  process.stderr.write(`Blocked by the critical dependency/project-graph hook (fails closed): ${reason}\n`);
  process.exit(2);
}

async function main() {
  let input;
  try {
    input = await readStdinJson();
  } catch (error) {
    block(error.message);
  }
  const command = input.tool_input && input.tool_input.command;
  if (typeof command !== 'string' || !command.trim()) block('Hook input has no tool_input.command.');

  const { active, config } = resolveRoots(input.cwd);
  const verdict = classify(command, frontendCli(config));
  if (verdict.force || (/\bnpm_config_(force|legacy_peer_deps)\s*=\s*['\"]?(true|1)\b/i.test(command) && /\bnpm(\.cmd)?\s/i.test(command))) {
    decide('deny', 'Peer-dependency bypass (--force / -f / --legacy-peer-deps or an npm_config_* equivalent) detected. The add-dependency workflow requires resolving the actual compatibility problem. No confirmation, comment marker, or approval opens this route.');
  }
  const gitReason = verdict.git.length ? gitAskReason(verdict.git) : null;
  if (verdict.reference) {
    decide('ask', ['Project-reference graph change detected. Changing the project reference graph is Reserved (CLAUDE.md § Decision control) unless it implements the approved layout (architecture.layout via project-structure); confirm only with that approval. The architecture check validates the resulting graph.', gitReason].filter(Boolean).join(' '));
  }
  if (!verdict.dependency) {
    if (gitReason) decide('ask', gitReason);
    process.exit(0);
  }

  const stateDir = hookStateDir(active);
  const stateFile = path.join(stateDir, 'dependency-commands.json');
  const now = Date.now();
  let state = {};
  if (existsSync(stateFile)) {
    try { state = JSON.parse(readFileSync(stateFile, 'utf8')); } catch { state = {}; }
  }
  for (const [key, ts] of Object.entries(state)) if (now - ts > GRACE_MS) delete state[key];

  const key = command.trim().replace(/\s+/g, ' ');
  mkdirSync(stateDir, { recursive: true });
  if (state[key]) {
    delete state[key];
    writeFileSync(stateFile, JSON.stringify(state, null, 2));
    if (gitReason) decide('ask', gitReason);
    process.exit(0);
  }
  state[key] = now;
  writeFileSync(stateFile, JSON.stringify(state, null, 2));
  decide('deny', 'Dependency change detected. Run the add-dependency workflow first (need, approved technology, latest stable compatible version, deprecation, vulnerability and license checks, approval for commercial or unclear licenses). After completing it, re-run the identical command within 30 minutes.');
}

main().catch((error) => block(`internal failure: ${error.message}`));
