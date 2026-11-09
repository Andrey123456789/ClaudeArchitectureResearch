// Level 3 Project · enforcement asset: Claude Code hook entry point.
// Launched in exec form from .claude/settings.json: command "node", args
// ["${CLAUDE_PROJECT_DIR}/.claude/hooks/claude-hook.mjs", "<pre-bash|post-bash|post-edit|stop>"]. The host
// substitutes the placeholder as a plain string, so the hook starts from any working directory and no
// shell expands variables.
// Two roots are kept apart. The launcher root (where this script lives) only locates tooling. The active
// root is the repository or worktree Claude is working in, resolved through Git from the hook input `cwd`
// (or from the edited file); every repository check runs against it.
// Exit codes: 0 = nothing to report; 2 = feedback for Claude (pre-bash: the shell call is blocked; post
// events: shown to Claude after the call; stop: Claude continues once); 1 = a check could not run (shown
// to the user, never blocking). pre-bash fails closed: whatever it cannot decide exits 2, and settings.json
// marks it onFailure "block" for launch failures, crashes, and timeouts. Post-event and Stop failures stay
// visible without blocking. Messages point to the owning workflow or rule; they never restate policy.
import { readFileSync, writeFileSync, existsSync, renameSync } from 'node:fs';
import path from 'node:path';
import { createHash } from 'node:crypto';
import { execFileSync } from 'node:child_process';
import { fileURLToPath, pathToFileURL } from 'node:url';
import {
  checkManifestFile, declaredDependencies, decodeText, dependencyDelta, inSkippedDir, isFile,
  isManifest, scanManifests,
} from './manifest-checks.mjs';

const EXIT_FEEDBACK = 2;
const EXIT_UNAVAILABLE = 1;

const ADD_DEPENDENCY = '.claude/skills/add-dependency/SKILL.md';
const PROJECT_STRUCTURE = '.claude/skills/project-structure/SKILL.md';
const ARCHITECTURE_DECISION = '.claude/skills/architecture-decision/SKILL.md';
const PACKAGE_MANAGEMENT = '.claude/rules/3-project/package-management.md';
const LAYOUT = '.claude/rules/3-project/layout.md';
const DEVELOPMENT = '.claude/skills/development-workflow/SKILL.md';
const CUSTOM_SETTINGS = '.claude/skills/custom-settings/SKILL.md';
const TEMPLATE_MAINTENANCE = '.claude/skills/template-maintenance/SKILL.md';
const CHECKER = '.claude/tools/check-instructions.mjs';

const MANIFEST_STATE = 'claude-manifest-state.json';
const STOP_STATE = 'claude-stop-reminders.json';
const STATE_VERSION = 1;
const STOP_DIGEST_LIMIT = 500;
const MANIFEST_PATHSPECS = [
  ':(glob)**/*.csproj', ':(glob)**/Directory.Packages.props', ':(glob)**/Directory.Build.props', ':(glob)**/Directory.Build.targets',
  ':(glob)**/package.json', ':(glob)**/.npmrc',
];

const event = process.argv[2];
const failClosed = event === 'pre-bash';
const launcherRoot = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..', '..');

function say(lines) {
  process.stderr.write(lines.map(line => `[project hook] ${line}`).join('\n') + '\n');
}

function unavailable(message) {
  if (failClosed) {
    say([`Blocked: the shell call could not be checked (${message}). Fix the cause and retry; the dependency guard does not let unchecked commands through.`]);
    process.exit(EXIT_FEEDBACK);
  }
  say([message]);
  process.exit(EXIT_UNAVAILABLE);
}

function feedback(lines) {
  say(lines);
  process.exit(EXIT_FEEDBACK);
}

function readInput() {
  let raw;
  try {
    raw = decodeText(readFileSync(0)); // also strips a UTF-8 byte-order mark that Windows pipelines may prepend
  } catch (error) {
    unavailable(`cannot read the hook payload from stdin: ${error.message}`);
  }
  if (!raw.trim()) unavailable('empty hook payload on stdin; expected the Claude Code hook JSON');
  let input;
  try {
    input = JSON.parse(raw);
  } catch (error) {
    unavailable(`hook payload is not valid JSON: ${error.message}`);
  }
  if (!input || typeof input !== 'object' || Array.isArray(input)) unavailable('hook payload is not a JSON object');
  return input;
}

// ---------- roots ----------

function git(dir, args, { buffer = false } = {}) {
  return execFileSync('git', ['-C', dir, ...args], {
    encoding: buffer ? 'buffer' : 'utf8',
    stdio: ['ignore', 'pipe', 'ignore'],
    maxBuffer: 64 * 1024 * 1024,
    windowsHide: true,
  });
}

function gitTopLevel(dir) {
  try {
    return path.resolve(git(dir, ['rev-parse', '--show-toplevel']).trim());
  } catch (error) {
    if (error.code === 'ENOENT') throw new Error('git is not available on PATH');
    return null;
  }
}

function isTemplateRoot(dir) {
  return existsSync(path.join(dir, 'CLAUDE.md')) && existsSync(path.join(dir, '.claude'));
}

function nearestExistingDir(start) {
  let current = path.resolve(start);
  while (!existsSync(current)) {
    const parent = path.dirname(current);
    if (parent === current) return null;
    current = parent;
  }
  return current;
}

function markerRoot(start) {
  for (let current = start; ; current = path.dirname(current)) {
    if (isTemplateRoot(current)) return current;
    if (path.dirname(current) === current) return null;
  }
}

// The active repository or worktree: the Git top level containing `start`, or — outside Git — the nearest
// ancestor holding CLAUDE.md and .claude/. `foreign` marks a repository that this instruction system does
// not govern (for example an unrelated nested clone).
function activeRoot(start) {
  const dir = nearestExistingDir(start);
  if (!dir) return null;
  const top = gitTopLevel(dir);
  if (top) return { root: top, git: true, foreign: !isTemplateRoot(top) };
  const marker = markerRoot(dir);
  return marker ? { root: marker, git: false, foreign: false } : null;
}

function inputCwd(input) {
  return typeof input?.cwd === 'string' && input.cwd ? input.cwd : process.cwd();
}

function relativeInside(root, file) {
  const relative = path.relative(root, path.resolve(root, file));
  if (!relative || relative.startsWith('..') || path.isAbsolute(relative)) return null;
  return relative.split(path.sep).join('/');
}

function statePath(root, name) {
  return path.resolve(root, git(root, ['rev-parse', '--git-path', name]).trim());
}

function headOf(root) {
  try {
    return git(root, ['rev-parse', '-q', '--verify', 'HEAD^{commit}']).trim() || null;
  } catch {
    return null; // unborn branch
  }
}

function readJson(file) {
  try {
    return existsSync(file) ? JSON.parse(readFileSync(file, 'utf8')) : null;
  } catch {
    return null;
  }
}

function usableState(stored) {
  return stored?.version === STATE_VERSION && stored.manifests !== null && typeof stored.manifests === 'object' && !Array.isArray(stored.manifests);
}

function writeJson(file, value) {
  const temp = `${file}.${process.pid}.tmp`;
  writeFileSync(temp, JSON.stringify(value));
  renameSync(temp, file);
}

// ---------- shell command classification (pre-execution routing and post-call context) ----------

const SEGMENT_BREAKS = new Set([';', '|', '&', '\n', '\r', '(', ')', '{', '}']);
const PREFIX_COMMANDS = new Set(['sudo', 'env', 'command', 'exec', 'nohup', 'time', 'call', 'cross-env', 'npx']);
const NODE_MANAGERS = new Set(['npm', 'pnpm', 'yarn']);
const BYPASS_FLAG = /^(--force|-f|--legacy-peer-deps)(=true)?$/;
const BYPASS_ENV = /^npm_config_(force|legacy_peer_deps)=(true|1)$/i;

// Global and command options that consume the next token as their value.
const NODE_VALUE_OPTIONS = {
  npm: ['--prefix', '-C', '--workspace', '-w', '--userconfig', '--globalconfig', '--cache', '--registry', '--loglevel',
    '--location', '--tag', '--omit', '--include', '--install-strategy', '--before', '--otp', '--scope',
    '--save-prefix', '--node-options', '--script-shell', '--access', '--fetch-retries', '--fetch-timeout'],
  pnpm: ['--dir', '-C', '--filter', '-F', '--workspace-dir', '--store-dir', '--virtual-store-dir', '--modules-dir',
    '--registry', '--reporter', '--loglevel', '--network-concurrency', '--child-concurrency', '--config'],
  yarn: ['--cwd', '--registry', '--modules-folder', '--cache-folder', '--global-folder', '--link-folder', '--mutex',
    '--network-timeout', '--network-concurrency', '--use-yarnrc'],
};

// Subcommand roles: install (adds when package arguments are given, otherwise restores), add, remove,
// update (always changes resolved versions), restore (never adds), other (bypass flags still matter).
const NODE_ROLES = {
  npm: {
    ...Object.fromEntries(['install', 'i', 'in', 'ins', 'inst', 'insta', 'instal', 'isnt', 'isnta', 'isntal', 'isntall',
      'add', 'install-test', 'it'].map(name => [name, 'install'])),
    ...Object.fromEntries(['uninstall', 'unlink', 'remove', 'rm', 'r', 'un'].map(name => [name, 'remove'])),
    ...Object.fromEntries(['update', 'up', 'upgrade', 'udpate'].map(name => [name, 'update'])),
    ...Object.fromEntries(['ci', 'clean-install', 'ic', 'install-clean', 'isntall-clean', 'install-ci-test', 'cit']
      .map(name => [name, 'restore'])),
    ...Object.fromEntries(['dedupe', 'ddp', 'audit'].map(name => [name, 'other'])),
  },
  pnpm: {
    install: 'install', i: 'install', 'install-test': 'install', it: 'install', add: 'add',
    remove: 'remove', rm: 'remove', uninstall: 'remove', un: 'remove',
    update: 'update', up: 'update', upgrade: 'update', dedupe: 'other', audit: 'other',
  },
  yarn: {
    install: 'install', add: 'add', remove: 'remove', upgrade: 'update', up: 'update', 'upgrade-interactive': 'update',
    dedupe: 'other', audit: 'other',
  },
};

function baseName(token) {
  return token.split(/[\\/]/).pop().toLowerCase().replace(/\.(exe|cmd|ps1|bat)$/, '');
}

// Quote-aware split into command segments (newline, ;, &&, ||, |, &, grouping) and tokens.
function tokenize(command) {
  const text = command.replace(/\\\r?\n|`\r?\n/g, ' ');
  const segments = [];
  let tokens = [];
  let current = '';
  let started = false;
  let quote = null;
  const endToken = () => {
    if (started) tokens.push(current);
    current = '';
    started = false;
  };
  const endSegment = () => {
    endToken();
    if (tokens.length > 0) segments.push(tokens);
    tokens = [];
  };
  for (let i = 0; i < text.length; i += 1) {
    const c = text[i];
    if (quote) {
      if (c === quote) quote = null;
      else if (quote === '"' && (c === '\\' || c === '`') && (text[i + 1] === '"' || text[i + 1] === c)) current += text[(i += 1)];
      else current += c;
    } else if (c === '"' || c === "'") {
      quote = c;
      started = true;
    } else if (c === '&' && text[i - 1] === '>') {
      current += c; // 2>&1 is a redirection, not a separator
    } else if (SEGMENT_BREAKS.has(c)) {
      endSegment();
    } else if (/\s/.test(c)) {
      endToken();
    } else {
      current += c;
      started = true;
    }
  }
  endSegment();
  return segments;
}

function withoutRedirections(tokens) {
  const result = [];
  for (let i = 0; i < tokens.length; i += 1) {
    if (/^(\d|\*)?(>>?|<)$/.test(tokens[i])) i += 1; // operator and its separate target
    else if (!/^(\d|\*)?(>>?|<)/.test(tokens[i])) result.push(tokens[i]);
  }
  return result;
}

function classifyDotnet(args) {
  const [verb, second, third] = args.filter(arg => !arg.startsWith('-')).map(arg => arg.toLowerCase());
  if (verb === 'add' || verb === 'remove') {
    const noun = second === 'package' || second === 'reference' ? second : third; // optional <PROJECT> argument
    if (noun === 'package' || noun === 'reference') return { kind: noun, bypass: false };
  }
  if (verb === 'package' && ['add', 'remove', 'update'].includes(second)) return { kind: 'package', bypass: false };
  if (verb === 'reference' && ['add', 'remove'].includes(second)) return { kind: 'reference', bypass: false };
  return null;
}

function classifyNodeManager(manager, args, env) {
  const valueOptions = new Set(NODE_VALUE_OPTIONS[manager]);
  const positional = [];
  const flags = [];
  for (let i = 0; i < args.length; i += 1) {
    const arg = args[i];
    if (arg === '--') break; // the rest belongs to a script, not to the package manager
    if (arg.startsWith('-') && arg.length > 1) {
      flags.push(arg);
      if (!arg.includes('=') && valueOptions.has(arg)) i += 1;
    } else {
      positional.push(arg);
    }
  }
  let [sub, ...rest] = positional.map(arg => arg.toLowerCase());
  if (manager === 'yarn' && sub === 'workspace' && rest.length > 0) [sub, ...rest] = rest.slice(1);
  const roles = NODE_ROLES[manager];
  const role = sub === undefined ? (manager === 'yarn' ? 'restore' : null) : Object.hasOwn(roles, sub) ? roles[sub] : null;
  if (manager === 'npm' && sub === 'config' && rest[0] === 'set' && /^(legacy-peer-deps|force)(=true)?$/.test(rest[1] ?? '') && ((rest[1] ?? '').includes('=') || rest[2] === 'true')) return { kind: null, bypass: true };
  if (!role) return null;
  const bypass = flags.some(flag => BYPASS_FLAG.test(flag)) || env.some(assignment => BYPASS_ENV.test(assignment));
  let kind = null;
  if (role === 'update') kind = 'package';
  else if ((role === 'install' || role === 'add' || role === 'remove') && rest.length > 0) kind = 'package';
  return { kind, bypass };
}

function classifySegment(rawTokens, depth, found) {
  const tokens = withoutRedirections(rawTokens);
  const env = [];
  let i = 0;
  while (i < tokens.length) {
    if (/^[A-Za-z_][A-Za-z0-9_]*=/.test(tokens[i])) {
      env.push(tokens[i]);
      i += 1;
    } else if (PREFIX_COMMANDS.has(baseName(tokens[i]))) {
      i += 1;
      while (i < tokens.length && tokens[i].startsWith('-')) i += 1;
    } else {
      break;
    }
  }
  if (i >= tokens.length) return;
  const program = baseName(tokens[i]);
  const args = tokens.slice(i + 1);
  if (depth < 3) {
    // Commands handed to another shell: cmd /c …, powershell|pwsh -Command …, bash|sh -c '…'.
    let inner = -1;
    if (program === 'cmd') inner = args.findIndex(arg => /^\/[ck]$/i.test(arg));
    else if (program === 'powershell' || program === 'pwsh') inner = args.findIndex(arg => /^-(c|command|commandwithargs)$/i.test(arg));
    else if (['bash', 'sh', 'zsh', 'dash'].includes(program)) inner = args.findIndex(arg => /^-[a-z]*c$/.test(arg));
    if (inner >= 0) {
      const rest = args.slice(inner + 1);
      if (rest.length === 1) for (const segment of tokenize(rest[0])) classifySegment(segment, depth + 1, found);
      else if (rest.length > 1) classifySegment(rest, depth + 1, found);
      return;
    }
  }
  let result = null;
  if (program === 'dotnet') result = classifyDotnet(args);
  else if (program === 'ng') result = args[0]?.toLowerCase() === 'add' ? { kind: 'package', bypass: false } : null;
  else if (NODE_MANAGERS.has(program)) result = classifyNodeManager(program, args, env);
  if (result && (result.kind || result.bypass)) found.push({ text: [...env, ...tokens.slice(i)].join(' '), ...result });
}

function classifyCommand(command) {
  const found = [];
  for (const segment of tokenize(command)) classifySegment(segment, 0, found);
  return found;
}

function preBash(input) {
  const command = input?.tool_input?.command;
  if (typeof command !== 'string') unavailable('the hook payload has no tool_input.command string');
  const found = classifyCommand(command);
  const lines = [];
  for (const item of found.filter(entry => entry.bypass)) {
    lines.push(`Blocked: '${item.text}' bypasses peer-dependency compatibility.`);
    lines.push(`Resolve the conflict as ${ADD_DEPENDENCY} (Install) describes. No confirmation, comment marker, or approval opens this route.`);
  }
  if (found.every(entry => !entry.bypass) && /\bnpm_config_(force|legacy_peer_deps)\s*=\s*['\"]?(true|1)\b/i.test(command) && /\bnpm(\.cmd)?\s/i.test(command)) {
    lines.push('Blocked: the command sets an npm_config_* peer-dependency bypass.');
    lines.push(`Resolve the conflict as ${ADD_DEPENDENCY} (Install) describes. No confirmation, comment marker, or approval opens this route.`);
  }
  for (const item of found.filter(entry => entry.kind === 'reference')) {
    lines.push(`Blocked: '${item.text}' changes the project reference graph, which requires approval (CLAUDE.md → Decision control).`);
    lines.push(`References mapped by ${LAYOUT} follow ${PROJECT_STRUCTURE} (Project references); any other graph change needs a Decision Request through ${ARCHITECTURE_DECISION}. Apply an approved change in the project file, where the manifest check reports it.`);
  }
  if (lines.length > 0) feedback(lines);
}

// ---------- actual manifest state (post-bash after successful and failed shell calls) ----------

function describeContent(relative, bytes) {
  const hash = createHash('sha256').update(bytes).digest('hex');
  try {
    const text = decodeText(bytes);
    const { packages, references } = declaredDependencies(relative, text);
    const normalized = createHash('sha256').update(text.replace(/\r/g, '')).digest('hex');
    return { hash, normalized, packages: [...packages], references: [...references] };
  } catch {
    return { hash, normalized: hash, packages: [], references: [], unreadable: true };
  }
}

function asDependencies(entry) {
  return { packages: new Map(entry.packages), references: new Set(entry.references) };
}

function listManifests(root) {
  const output = git(root, ['ls-files', '-z', '--cached', '--others', '--exclude-standard', '--', ...MANIFEST_PATHSPECS]);
  const files = new Set(output.split('\0').filter(file => file && isManifest(file) && !inSkippedDir(file)));
  return [...files].filter(file => isFile(path.join(root, file))).sort(); // the index also lists deleted files
}

function snapshot(root) {
  const manifests = {};
  for (const file of listManifests(root)) manifests[file] = describeContent(file, readFileSync(path.join(root, file)));
  return { version: STATE_VERSION, head: headOf(root), manifests };
}

// Without a previous observation, HEAD stands in for it: manifests that differ from HEAD (or were removed
// since) are compared with their committed content; everything else counts as unchanged.
function headBaseline(root, current) {
  const previous = {};
  for (const [file, entry] of Object.entries(current.manifests)) previous[file] = entry;
  if (!current.head) return previous;
  const relevant = file => file && isManifest(file) && !inSkippedDir(file);
  const untracked = git(root, ['ls-files', '-z', '--others', '--exclude-standard', '--', ...MANIFEST_PATHSPECS]).split('\0').filter(relevant);
  for (const file of untracked) delete previous[file];
  const changes = git(root, ['diff', '--name-status', '--no-renames', '-z', 'HEAD', '--', ...MANIFEST_PATHSPECS]).split('\0');
  for (let i = 0; i + 1 < changes.length; i += 2) {
    const [status, file] = [changes[i], changes[i + 1]];
    if (!relevant(file)) continue;
    if (status === 'A') delete previous[file]; // staged new file: not part of HEAD
    else previous[file] = describeContent(file, git(root, ['show', `HEAD:${file}`], { buffer: true }));
  }
  return previous;
}

function referenceChangeLine(file, changes) {
  return `Project reference graph change in ${file}: ${changes.join(', ')} → confirm it is the layout mapped by ${LAYOUT} (${PROJECT_STRUCTURE}) or an approved decision (${ARCHITECTURE_DECISION}; CLAUDE.md → Decision control), and report it.`;
}

function ownerFor(file) {
  return file.endsWith('.csproj')
    ? `${PROJECT_STRUCTURE} (a production project or reference-graph change outside the layout mapped by ${LAYOUT} requires approval — CLAUDE.md → Decision control); report it`
    : `${ADD_DEPENDENCY} / ${PACKAGE_MANAGEMENT}; report it`;
}

function compareStates(root, previous, current, fresh) {
  const lines = [];
  const validate = new Set(fresh ? Object.keys(current.manifests) : []);
  const added = Object.keys(current.manifests).filter(file => !previous[file]);
  const removed = Object.keys(previous).filter(file => !current.manifests[file]);
  for (const file of removed) {
    const target = added.find(candidate => current.manifests[candidate].normalized === previous[file].normalized);
    if (target) {
      added.splice(added.indexOf(target), 1);
      validate.add(target);
      lines.push(`Manifest moved: ${file} → ${target} → ${ownerFor(file)}.`);
    } else {
      lines.push(`Manifest removed: ${file} → ${ownerFor(file)}.`);
    }
  }
  for (const file of added) {
    validate.add(file);
    lines.push(`Manifest added: ${file} → ${ownerFor(file)}.`);
  }
  for (const [file, entry] of Object.entries(current.manifests)) {
    const before = previous[file];
    if (!before || before.hash === entry.hash) continue;
    validate.add(file);
    if (before.unreadable || entry.unreadable) continue;
    const delta = dependencyDelta(asDependencies(before), asDependencies(entry));
    if (delta.packages.length > 0) {
      lines.push(`Dependency change in ${file}: ${delta.packages.join(', ')} → ${ADD_DEPENDENCY}: confirm its version, deprecation, vulnerability, and license steps were completed and report them.`);
    }
    if (delta.references.length > 0) {
      lines.push(referenceChangeLine(file, delta.references));
    }
  }
  const reported = new Set();
  for (const file of [...validate].sort()) lines.push(...checkManifestFile(root, path.join(root, file), reported));
  return lines;
}

function observeManifests(root) {
  const stateFile = statePath(root, MANIFEST_STATE);
  const stored = readJson(stateFile);
  const fresh = !usableState(stored);
  const current = snapshot(root);
  const previous = fresh ? headBaseline(root, current) : stored.manifests;
  const lines = compareStates(root, previous, current, fresh);
  const notes = [];
  if (!fresh && stored.head !== current.head && lines.length > 0) {
    notes.push(`HEAD moved ${String(stored.head ?? 'none').slice(0, 12)} → ${String(current.head ?? 'none').slice(0, 12)}.`);
  }
  if (fresh && lines.length > 0) notes.push('First observation of this worktree: every manifest was validated.');
  try {
    writeJson(stateFile, current);
  } catch (error) {
    notes.push(`The manifest snapshot could not be saved to ${stateFile} (${error.message}); the next shell call validates every manifest again.`);
  }
  return { lines, notes, saved: notes.every(note => !note.startsWith('The manifest snapshot')) };
}

function commandLines(found) {
  return found.filter(item => item.kind === 'package')
    .map(item => `Dependency command: '${item.text}' → ${ADD_DEPENDENCY}: confirm its version, deprecation, vulnerability, and license steps were completed and report them.`);
}

function postBash(input) {
  const failed = input.hook_event_name === 'PostToolUseFailure';
  const command = typeof input?.tool_input?.command === 'string' ? input.tool_input.command : '';
  const found = command ? classifyCommand(command) : [];
  const active = activeRoot(inputCwd(input));
  if (!active || active.foreign) return; // the shell call ran outside this instruction system's repository
  const where = failed ? 'after the failed shell call' : 'after the shell call';

  if (!active.git) {
    // Outside Git there is no snapshot to compare with; recognized dependency commands still get a full scan.
    if (failed || !found.some(item => item.kind)) return;
    const problems = scanManifests(active.root).map(problem => `  - ${problem}`);
    feedback([
      `Manifest check ${where} (no Git work tree: actual-state tracking is unavailable, so the command text triggered a full scan):`,
      ...commandLines(found).map(line => `  - ${line}`),
      ...problems,
    ]);
  }

  const { lines, notes, saved } = observeManifests(active.root);
  const packageChanged = lines.some(line => line.startsWith('Dependency change in '));
  const context = failed || packageChanged ? [] : commandLines(found);
  const all = [...context, ...lines];
  if (all.length > 0) {
    feedback([`Manifest check ${where} (actual state of ${active.root}):`, ...notes.map(note => `  ${note}`), ...all.map(line => `  - ${line}`)]);
  }
  if (!saved) unavailable(notes.join(' '));
}

// ---------- file edits ----------

function headDependencies(root, relative) {
  try {
    return declaredDependencies(relative, decodeText(git(root, ['show', `HEAD:${relative}`], { buffer: true })));
  } catch {
    return declaredDependencies(relative, ''); // new file or no commits yet
  }
}

// Keeps the shell snapshot current after an edit the post-edit check already reported, so the next shell
// call does not report the same change again. Only an existing snapshot is updated.
function refreshSnapshotEntry(root, relative) {
  try {
    const stateFile = statePath(root, MANIFEST_STATE);
    const stored = readJson(stateFile);
    if (!usableState(stored)) return;
    const file = path.join(root, relative);
    if (isFile(file)) stored.manifests[relative] = describeContent(relative, readFileSync(file));
    else delete stored.manifests[relative];
    writeJson(stateFile, stored);
  } catch {
    // The next shell call re-validates this file instead; nothing is lost.
  }
}

async function postEdit(input) {
  const target = input?.tool_input?.file_path ?? input?.tool_input?.path;
  if (typeof target !== 'string' || !target) return;
  const absolute = path.resolve(inputCwd(input), target);
  const active = activeRoot(path.dirname(absolute));
  if (!active || active.foreign) return;
  const root = active.root;
  const relative = relativeInside(root, absolute);
  if (!relative) return;

  if (relative === 'SPECIFICATION.md' || relative === 'CUSTOM_SETTINGS.md') {
    feedback([
      `${relative} changed (product input).`,
      `Keep SPECIFICATION.md and CUSTOM_SETTINGS.md consistent (CLAUDE.md → Product governance). CUSTOM_SETTINGS.md changes run ${CUSTOM_SETTINGS}; approved behavior changes follow ${DEVELOPMENT} (Implement → approved product decisions).`,
    ]);
  }

  if (isManifest(relative) && !inSkippedDir(relative)) {
    const lines = checkManifestFile(root, absolute).map(problem => `  - ${problem}`);
    let detection = null;
    if (active.git && !relative.endsWith('.npmrc')) {
      let current = { packages: new Map(), references: new Set() };
      try {
        current = declaredDependencies(relative, decodeText(readFileSync(absolute)));
      } catch {
        // An unreadable file is already reported by checkManifestFile.
      }
      detection = dependencyDelta(headDependencies(root, relative), current);
      if (detection.references.length > 0) {
        lines.unshift(`  - ${referenceChangeLine(relative, detection.references)}`);
      }
      if (detection.packages.length > 0) {
        lines.unshift(`  - Dependency change in ${relative}: ${detection.packages.join(', ')} → follow ${ADD_DEPENDENCY} and report its checks.`);
      }
      refreshSnapshotEntry(root, relative);
    }
    if (lines.length > 0) {
      if (!active.git) lines.push('  - (dependency-change detection unavailable: not a Git work tree)');
      feedback([`Manifest check for ${relative}:`, ...lines]);
    }
    if (!active.git && !relative.endsWith('.npmrc')) {
      unavailable(`dependency-change detection for ${relative} is unavailable (not a Git work tree); static manifest checks passed.`);
    }
    return;
  }

  if (relative === 'CLAUDE.md' || (relative.startsWith('.claude/') && /\.(md|json|mjs)$/.test(relative) && !relative.startsWith('.claude/settings.local'))) {
    const checkerFile = [path.join(root, CHECKER), path.join(launcherRoot, CHECKER)].find(file => existsSync(file));
    if (!checkerFile) unavailable(`instruction-structure check after editing ${relative} is unavailable: ${CHECKER} is missing.`);
    const { checkInstructions } = await import(pathToFileURL(checkerFile).href);
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

// Bounded digest of the current content of the files that drive the reminders, so a material edit to an
// already-modified file produces a fresh reminder while an unchanged state stays silent.
function contentDigest(root, files) {
  const relevant = files
    .map(entry => entry.file)
    .filter(file => file === 'CUSTOM_SETTINGS.md' || Object.values(PATTERNS).some(pattern => pattern.test(file)))
    .sort()
    .slice(0, STOP_DIGEST_LIMIT);
  const digest = createHash('sha256');
  for (const file of relevant) {
    digest.update(`${file}\0`);
    try {
      digest.update(readFileSync(path.join(root, file)));
    } catch {
      digest.update('<absent>');
    }
    digest.update('\0');
  }
  return digest.digest('hex');
}

function stop(input) {
  if (input?.stop_hook_active) return; // Claude is already continuing because of a Stop hook: never loop.
  const active = activeRoot(inputCwd(input));
  if (!active || !active.git) unavailable(`co-change reminders are unavailable: ${inputCwd(input)} is not inside a Git work tree.`);
  if (active.foreign) unavailable(`co-change reminders skipped: ${active.root} is not governed by this instruction system.`);
  const root = active.root;

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
    .update(JSON.stringify({
      files: files.map(entry => `${entry.status} ${entry.file}`).sort(),
      content: contentDigest(root, files),
      reminders,
    }))
    .digest('hex');
  const stateFile = statePath(root, STOP_STATE);
  if (readJson(stateFile)?.fingerprint === fingerprint) return;
  try {
    writeJson(stateFile, { fingerprint, at: new Date().toISOString() });
  } catch (error) {
    unavailable(`cannot record the reminder state in ${stateFile}: ${error.message}`);
  }
  feedback([
    'Before finishing, check these co-change reminders:',
    ...reminders.map(reminder => `  - ${reminder}`),
    'Address each one or state why it does not apply; this reminder is repeated only when the changed files or their relevant content change.',
  ]);
}

// ---------- main ----------

const handlers = { 'pre-bash': preBash, 'post-bash': postBash, 'post-edit': postEdit, stop };

if (!handlers[event]) {
  unavailable(`unknown hook event '${event ?? ''}'; expected one of: ${Object.keys(handlers).join(', ')}`);
}

try {
  await handlers[event](readInput());
} catch (error) {
  unavailable(`the ${event} check failed unexpectedly: ${error?.message ?? error}`);
}
process.exit(0);
