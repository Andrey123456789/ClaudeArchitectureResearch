// Kind: ENF | Scope: repo/meta | Owner: Claude Code hook dispatcher — pre-command gates (dependency changes, project-reference graph, repository-changing Git), validation of the actual worktree state after edits and shell commands, product-input reminders, co-change reminders at stop | Loading: hook events configured in .claude/settings.json
//
// Launch (exec form, .claude/settings.json): node <launcher root>/.claude/hooks/hook.cjs <event>, hook input JSON on stdin.
// The launcher root only locates this script. Every check runs against the active repository or worktree, resolved
// from the hook input `cwd` (or the edited file) through Git; state is kept per worktree in .claude/.hook-state/.
// Events: pre-tool-use (fail-closed: any error or unreadable input denies the command), post-tool-use,
// post-tool-use-failure (a failed shell command may still have changed files), stop.
// Output: Claude Code hook JSON on stdout with exit code 0. Exit code 1 with a message on stderr means a
// non-critical hook could not run. Messages point to the owning workflow or standard; they do not restate policy.
'use strict';

const fs = require('fs');
const path = require('path');

const EVENTS = ['pre-tool-use', 'post-tool-use', 'post-tool-use-failure', 'stop'];
const SHELL_TOOLS = ['Bash', 'PowerShell'];
const EDIT_TOOLS = ['Edit', 'Write', 'MultiEdit', 'NotebookEdit'];
const DEPENDENCY_MARKER = /#\s*add-dependency:\s*reviewed\b/i;
const REFERENCE_MARKER = /#\s*project-references:\s*approved\b/i;
const REGISTER = 'docs/architecture/decision-register.md';

function script(name) {
  return require(path.join(__dirname, '..', 'scripts', name));
}

function fail(message) {
  process.stderr.write(`[hook] ${message}\n`);
  process.exit(1);
}

function emit(output) {
  process.stdout.write(`${JSON.stringify(output)}\n`);
  process.exit(0);
}

function preDecision(decision, lines) {
  emit({ hookSpecificOutput: { hookEventName: 'PreToolUse', permissionDecision: decision, permissionDecisionReason: lines.join('\n') } });
}

function postFeedback(event, lines) {
  const reason = lines.join('\n');
  if (event === 'post-tool-use-failure') emit({ hookSpecificOutput: { hookEventName: 'PostToolUseFailure', additionalContext: reason } });
  emit({ decision: 'block', reason });
}

// Hook input: JSON object on stdin; a UTF-8 byte-order mark and BOM-tagged UTF-16 are accepted.
function readInput() {
  let bytes;
  try {
    bytes = fs.readFileSync(0);
  } catch (error) {
    throw new Error(`cannot read hook input from stdin: ${error.message}`);
  }
  const decoded = script('repo.cjs').decodeText(bytes);
  if (decoded.error) throw new Error(`hook input ${decoded.error}`);
  const text = decoded.text.trim();
  if (!text) throw new Error('hook input is empty');
  let input;
  try {
    input = JSON.parse(text);
  } catch (error) {
    throw new Error(`hook input is not valid JSON: ${error.message}`);
  }
  if (!input || typeof input !== 'object' || Array.isArray(input)) throw new Error('hook input is not a JSON object');
  return input;
}

// ---------------------------------------------------------------------------
// Command classification (pre-execution routing only; the post-change checks inspect the actual state)
// ---------------------------------------------------------------------------

function tokenize(segment) {
  const tokens = [];
  for (const m of segment.matchAll(/"((?:[^"\\]|\\.)*)"|'([^']*)'|(\S+)/g)) {
    if (m[3] !== undefined && m[3].startsWith('#')) break; // comment
    tokens.push(m[1] ?? m[2] ?? m[3]);
  }
  return tokens;
}

// Command segments split at newlines, ;, &, &&, | and || outside quotes.
function segmentsOf(command) {
  const segments = [];
  let current = '';
  let quote = null;
  for (const ch of String(command)) {
    if (quote) {
      if (ch === quote) quote = null;
      current += ch;
    } else if (ch === '"' || ch === "'") {
      quote = ch;
      current += ch;
    } else if ('\n;&|'.includes(ch)) {
      segments.push(current);
      current = '';
    } else {
      current += ch;
    }
  }
  segments.push(current);
  return segments.map((s) => s.trim()).filter(Boolean);
}

function baseName(token) {
  return String(token).toLowerCase().split(/[\\/]/).pop().replace(/\.(exe|cmd|bat|ps1)$/, '');
}

// Splits arguments into positionals, skipping options and the values of options that take one.
function positionalsOf(args, valueOptions) {
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

const FORCE_FLAG = /^(--force|--legacy-peer-deps)(=.*)?$/i;

// Node package managers: subcommand → 'change' (always a dependency change), 'spec' (a change when a package
// is named), 'restore' (installs from the lockfile; a change only with a force/legacy-peer bypass flag).
const NODE_PM = {
  npm: {
    valueOptions: ['--prefix', '--workspace', '-w', '--registry', '--cache', '--loglevel', '--userconfig', '--globalconfig', '--location', '--tag', '--omit', '--include', '--install-strategy'],
    force: ['-f'],
    subcommands: {
      install: 'spec', i: 'spec', in: 'spec', ins: 'spec', inst: 'spec', insta: 'spec', instal: 'spec', isnt: 'spec', isnta: 'spec', isntal: 'spec', isntall: 'spec', add: 'spec',
      ci: 'restore', 'clean-install': 'restore', ic: 'restore', 'install-clean': 'restore', 'isntall-clean': 'restore',
      update: 'change', up: 'change', upgrade: 'change', udpate: 'change', dedupe: 'change', ddp: 'change',
      uninstall: 'change', unlink: 'change', remove: 'change', rm: 'change', r: 'change', un: 'change',
      audit: 'fix',
    },
  },
  pnpm: {
    valueOptions: ['--dir', '-C', '--filter', '-F', '--registry', '--loglevel', '--reporter', '--workspace-dir'],
    force: [],
    subcommands: {
      add: 'change', install: 'spec', i: 'spec',
      update: 'change', up: 'change', upgrade: 'change',
      remove: 'change', rm: 'change', uninstall: 'change', un: 'change',
    },
  },
  yarn: {
    valueOptions: ['--cwd', '--registry', '--modules-folder', '--cache-folder', '--mutex', '--network-timeout'],
    force: [],
    subcommands: { add: 'change', remove: 'change', upgrade: 'change', up: 'change', 'upgrade-interactive': 'change', install: 'spec' },
  },
};

function classifyNodePackageManager(tool, args) {
  const spec = NODE_PM[tool];
  const valueOptions = new Set(spec.valueOptions);
  const force = args.some((a) => FORCE_FLAG.test(a) || spec.force.includes(a));
  const positionals = positionalsOf(args, valueOptions);
  let [sub, ...rest] = positionals;
  if (tool === 'yarn' && sub === 'workspace') [, , sub, ...rest] = positionals; // yarn workspace <name> <command>
  const kind = sub === undefined ? (tool === 'yarn' ? 'restore' : null) : spec.subcommands[sub.toLowerCase()];
  if (kind === 'change' || (kind === 'spec' && rest.length > 0) || (kind === 'fix' && rest[0] === 'fix')) return { force };
  if ((kind === 'spec' || kind === 'restore') && force) return { force };
  return null;
}

const DOTNET_VALUE_OPTIONS = new Set(['--version', '-v', '--source', '-s', '--framework', '-f', '--package-directory', '--project', '--verbosity']);

// dotnet add/remove [<project>] package|reference …, dotnet package add|remove|update …, dotnet reference add|remove ….
function classifyDotnet(args) {
  const positionals = positionalsOf(args, DOTNET_VALUE_OPTIONS).map((p) => p.toLowerCase());
  const [verb, first, second] = positionals;
  if (verb === 'add' || verb === 'remove') {
    if (first === 'package' || first === 'reference') return first;
    if (second === 'package' || second === 'reference') return second;
    return null;
  }
  if (verb === 'package' && ['add', 'remove', 'update'].includes(first)) return 'package';
  if (verb === 'reference' && ['add', 'remove'].includes(first)) return 'reference';
  return null;
}

// Git: table-driven read-only vs repository-changing classification, after global options such as -C <path>.
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
  branch: (args) => !hasAny(args, ['-d', '-D', '--delete', '-m', '-M', '--move', '-c', '-C', '--copy', '-u', '--set-upstream-to', '--unset-upstream', '--edit-description', '-f', '--force', '-t', '--track', '--no-track'])
    && (hasAny(args, ['-l', '--list', '-a', '--all', '-r', '--remotes', '--contains', '--no-contains', '--merged', '--no-merged', '--points-at', '--show-current', '-v', '-vv', '--verbose', '--format', '--sort'])
      || positionalsOf(args, new Set()).length === 0),
  tag: (args) => !hasAny(args, ['-d', '--delete', '-a', '--annotate', '-s', '--sign', '-u', '--local-user', '-f', '--force', '-m', '--message', '-F', '--file'])
    && (hasAny(args, ['-l', '--list', '-n', '--contains', '--no-contains', '--merged', '--no-merged', '--points-at', '--sort', '--format', '-v', '--verify'])
      || positionalsOf(args, new Set()).length === 0),
  stash: (args) => ['list', 'show'].includes(positionalsOf(args, new Set())[0]),
  worktree: (args) => positionalsOf(args, new Set())[0] === 'list',
  remote: (args) => { const [sub] = positionalsOf(args, new Set()); return sub === undefined || ['show', 'get-url'].includes(sub); },
  config: (args) => hasAny(args, ['--get', '--get-all', '--get-regexp', '--get-urlmatch', '--list', '-l'])
    || (['get', 'list'].includes(positionalsOf(args, new Set())[0]))
    || (!hasAny(args, ['--unset', '--unset-all', '--add', '--replace-all', '--rename-section', '--remove-section', '-e', '--edit'])
      && positionalsOf(args, new Set(['--file', '-f', '--type', '--default'])).length === 1),
  notes: (args) => { const [sub] = positionalsOf(args, new Set()); return sub === undefined || ['list', 'show'].includes(sub); },
  reflog: (args) => { const [sub] = positionalsOf(args, new Set()); return sub === undefined || !['expire', 'delete'].includes(sub); },
  submodule: (args) => { const [sub] = positionalsOf(args, new Set()); return sub === undefined || ['status', 'summary'].includes(sub); },
  'symbolic-ref': (args) => !hasAny(args, ['-d', '--delete']) && positionalsOf(args, new Set(['-m'])).length <= 1,
  bisect: (args) => ['log', 'visualize', 'view', 'terms'].includes(positionalsOf(args, new Set())[0]),
  'sparse-checkout': (args) => positionalsOf(args, new Set())[0] === 'list',
  apply: (args) => hasAny(args, ['--check', '--stat', '--numstat', '--summary']) && !hasAny(args, ['--index', '--cached', '--apply', '-3', '--3way']),
  checkout: (args) => args.length === 0,
  'hash-object': (args) => !hasAny(args, ['-w']),
};

function hasAny(args, flags) {
  return args.some((a) => flags.includes(a) || flags.some((f) => f.startsWith('--') && a.startsWith(`${f}=`)));
}

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

const SHELL_LAUNCHERS = { bash: ['-c'], sh: ['-c'], cmd: ['/c', '/k'], pwsh: ['-c', '-command'], powershell: ['-c', '-command'] };

function classifyTokens(tokens, found) {
  for (let i = 0; i < tokens.length; i += 1) {
    const tool = baseName(tokens[i]);
    const args = tokens.slice(i + 1);
    const text = tokens.slice(i).join(' ');
    const launch = SHELL_LAUNCHERS[tool] ? args.findIndex((a) => SHELL_LAUNCHERS[tool].includes(a.toLowerCase())) : -1;
    if (launch >= 0 && args.length > launch + 1) {
      for (const segment of segmentsOf(args.slice(launch + 1).join(' '))) classifyTokens(tokenize(segment), found);
    } else if (NODE_PM[tool]) {
      const hit = classifyNodePackageManager(tool, args);
      if (hit) found.dependency.push({ text, force: hit.force });
    } else if (tool === 'ng' || (tool === 'npx' && baseName(positionalsOf(args, new Set(['-p', '--package']))[0] ?? '') === 'ng')) {
      const ngArgs = tool === 'ng' ? args : args.slice(args.findIndex((a) => baseName(a) === 'ng') + 1);
      const [sub, ...rest] = positionalsOf(ngArgs, new Set());
      if (sub === 'add' || (sub === 'update' && rest.length > 0)) found.dependency.push({ text, force: ngArgs.some((a) => FORCE_FLAG.test(a)) });
    } else if (tool === 'dotnet') {
      const kind = classifyDotnet(args);
      if (kind === 'package') found.dependency.push({ text, force: false });
      if (kind === 'reference') found.reference.push(text);
    } else if (tool === 'nuget' && ['install', 'update'].includes(String(args[0]).toLowerCase())) {
      found.dependency.push({ text, force: false });
    } else if (['install-package', 'update-package', 'uninstall-package'].includes(tool)) {
      found.dependency.push({ text, force: false });
    } else if (tool === 'git') {
      const sub = classifyGit(args);
      if (sub) found.git.push({ sub, text });
    } else {
      continue;
    }
    break; // the rest of the segment belongs to the recognized command
  }
}

function classifyCommand(command) {
  const found = { dependency: [], reference: [], git: [] };
  for (const segment of segmentsOf(command)) classifyTokens(tokenize(segment), found);
  return found;
}

function preToolUse(input) {
  if (!SHELL_TOOLS.includes(input.tool_name)) return;
  const command = input.tool_input?.command;
  if (typeof command !== 'string') throw new Error('hook input has no tool_input.command string');
  const found = classifyCommand(command);
  const deny = [];
  if (found.reference.length > 0 && !REFERENCE_MARKER.test(command)) {
    deny.push(
      `Project-reference graph change: ${found.reference.join(' | ')}`,
      'Changing the project reference graph is Reserved (CLAUDE.md § Decisions) unless an accepted decision already requires the reference, even when the new reference would be legal.',
      'Follow `project-structure` § Changing project references (Decision Request: `architecture-decision`), then re-run the command with the trailing comment `# project-references: approved`.',
    );
  }
  if (found.dependency.length > 0 && !DEPENDENCY_MARKER.test(command)) {
    deny.push(
      `Dependency change detected: ${found.dependency.map((d) => d.text).join(' | ')}`,
      'Run the `add-dependency` workflow first; when its checks are complete, re-run the command with the trailing comment `# add-dependency: reviewed`.',
    );
    if (found.dependency.some((d) => d.force)) deny.push('The command uses --force or --legacy-peer-deps: resolve the actual peer-dependency conflict instead (`add-dependency` § 5).');
  }
  if (deny.length > 0) preDecision('deny', deny);
  if (found.git.length > 0) {
    preDecision('ask', [
      `Repository-changing Git command (${[...new Set(found.git.map((g) => g.sub))].join(', ')}): ${found.git.map((g) => g.text).join(' | ')}`,
      'Run it only when the user explicitly requested it or pre-approved this operation and scope (CLAUDE.md § Git); procedure: `git-workflow`.',
    ]);
  }
}

// ---------------------------------------------------------------------------
// Post-change validation of the actual worktree state
// ---------------------------------------------------------------------------

function tools() {
  return { repo: script('repo.cjs'), dependencies: script('check-dependencies.cjs') };
}

// What a path means for the hook: 'manifest', 'instructions', 'product' or null.
function surfaceOf(rel, t) {
  if (rel === 'SPECIFICATION.md' || rel === 'CUSTOM_SETTINGS.md') return 'product';
  if (rel === 'CLAUDE.md' || rel === REGISTER) return 'instructions';
  if (rel.startsWith('.claude/')) return rel.startsWith('.claude/.hook-state/') || rel === '.claude/settings.local.json' ? null : 'instructions';
  return t.dependencies.isTrackedManifest(rel) ? 'manifest' : null;
}

function stateFile(root, name) {
  return path.join(root, '.claude', '.hook-state', name);
}

function readState(root, name) {
  try {
    return JSON.parse(fs.readFileSync(stateFile(root, name), 'utf8'));
  } catch {
    return null;
  }
}

function writeState(root, name, value) {
  const file = stateFile(root, name);
  try {
    fs.mkdirSync(path.dirname(file), { recursive: true });
    const ignore = path.join(path.dirname(file), '.gitignore');
    if (!fs.existsSync(ignore)) fs.writeFileSync(ignore, '*\n');
    const temporary = `${file}.${process.pid}.tmp`;
    fs.writeFileSync(temporary, JSON.stringify(value));
    fs.renameSync(temporary, file);
  } catch (error) {
    process.stderr.write(`[hook] could not persist hook state in ${path.dirname(file)}: ${error.message}\n`);
  }
}

// Snapshot entry of one surface path: content hash, plus the project references of a .csproj.
function entryFor(root, rel, surface, t) {
  const hash = t.repo.hashFile(path.join(root, rel));
  if (!hash) return null;
  if (surface !== 'manifest' || !rel.endsWith('.csproj')) return { hash };
  const decoded = t.repo.readText(path.join(root, rel));
  return { hash, refs: decoded.text ? t.dependencies.projectReferences(decoded.text).sort() : [] };
}

function nulList(stdout) {
  return stdout.split('\0').filter((p) => p && !p.endsWith('/')).map((p) => p.replace(/\\/g, '/'));
}

function statusPaths(root, t) {
  const status = t.repo.git(root, ['status', '--porcelain=v1', '-z', '--untracked-files=all', '--no-renames']);
  if (!status.ok) throw new Error(`git status failed in ${root}: ${status.stderr}`);
  return nulList(status.stdout).map((entry) => entry.slice(3));
}

// Every surface path: Git index plus untracked, non-ignored files (nested repositories and worktrees are not
// entered); without Git, a bounded walk of a root that holds this instruction system.
function listSurface(root, isGit, t) {
  let paths = [];
  if (isGit) {
    const listed = t.repo.git(root, ['ls-files', '-z', '--cached', '--others', '--exclude-standard', '--',
      '*.csproj', '*Directory.Packages.props', '*package.json', 'CLAUDE.md', 'SPECIFICATION.md', 'CUSTOM_SETTINGS.md', '.claude', REGISTER]);
    if (!listed.ok) throw new Error(`git ls-files failed in ${root}: ${listed.stderr}`);
    paths = nulList(listed.stdout);
  } else {
    let budget = 20000;
    const walk = (dir) => {
      for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
        if ((budget -= 1) < 0) throw new Error(`${root} is not a Git work tree and too large to observe; initialize Git or work inside a repository.`);
        const full = path.join(dir, entry.name);
        if (entry.isDirectory() && !['node_modules', 'bin', 'obj', '.git', 'dist'].includes(entry.name) && !fs.existsSync(path.join(full, '.git'))) walk(full);
        else if (entry.isFile()) paths.push(path.relative(root, full).split(path.sep).join('/'));
      }
    };
    walk(root);
  }
  return paths.filter((p) => surfaceOf(p, t));
}

// Compares the worktree with its snapshot (.claude/.hook-state/worktree.json). The first observation records a
// full baseline and validates it; later observations look only at paths Git reports as changed — the working
// tree and index status now and at the last observation, plus everything that differs between the old and new HEAD.
function observeWorktree(root, isGit, t) {
  const previous = readState(root, 'worktree.json');
  const fresh = previous?.version !== 1;
  const head = isGit ? (t.repo.git(root, ['rev-parse', '--verify', '--quiet', 'HEAD']).stdout.trim() || null) : null;
  const status = isGit ? statusPaths(root, t).filter((p) => surfaceOf(p, t)) : [];
  const files = fresh ? {} : { ...previous.files };
  let candidates;
  if (fresh || !isGit) {
    candidates = [...listSurface(root, isGit, t), ...Object.keys(files)];
  } else {
    candidates = [...status, ...previous.status, ...Object.keys(files).filter((p) => !fs.existsSync(path.join(root, p)))];
    if (head !== previous.head) {
      const diff = previous.head && head ? t.repo.git(root, ['diff', '--name-only', '-z', '--no-renames', previous.head, head]) : { ok: false };
      candidates.push(...(diff.ok ? nulList(diff.stdout) : listSurface(root, true, t))); // first commit or unknown old HEAD: full list
    }
  }
  const changes = [];
  for (const rel of new Set(candidates)) {
    const surface = surfaceOf(rel, t);
    if (!surface) continue;
    const before = files[rel];
    const after = entryFor(root, rel, surface, t);
    if (after) files[rel] = after; else delete files[rel];
    if (fresh) {
      if (after && surface !== 'product') changes.push({ rel, surface, type: 'baseline', after });
    } else if (before?.hash !== after?.hash) {
      changes.push({ rel, surface, type: !before ? 'added' : !after ? 'removed' : 'changed', before, after });
    }
  }
  writeState(root, 'worktree.json', { version: 1, head, status, files });
  return changes;
}

// A removed manifest whose exact content reappears under another path was moved.
function pairMoves(changes) {
  for (const removed of changes.filter((c) => c.type === 'removed' && c.surface === 'manifest')) {
    const target = changes.find((c) => c.type === 'added' && c.surface === 'manifest' && c.after.hash === removed.before.hash);
    if (target) {
      Object.assign(target, { type: 'moved', from: removed.rel });
      removed.type = 'moved-away';
    }
  }
  return changes.filter((c) => c.type !== 'moved-away');
}

function sameList(a = [], b = []) {
  return a.length === b.length && a.every((value, i) => value === b[i]);
}

// Validates changed surface paths and returns the findings. `graphHint`: an edit touched ProjectReference
// text of a manifest whose previous content is unknown.
function reactToChanges(root, changes, t, graphHint) {
  const messages = [];
  const validated = new Set();
  const validate = (rel) => {
    if (validated.has(rel)) return;
    validated.add(rel);
    const result = t.dependencies.checkFile(root, rel);
    for (const e of result.errors) messages.push(`[manifest] ${e}`);
    for (const n of result.notices) messages.push(`[manifest notice] ${n}`);
  };
  let projectRemoved = false;
  let instructionsChanged = false;
  for (const change of pairMoves(changes)) {
    const { rel, surface, type } = change;
    if (surface === 'instructions') {
      instructionsChanged = true;
    } else if (surface === 'product') {
      if (rel === 'CUSTOM_SETTINGS.md') messages.push('CUSTOM_SETTINGS.md changed: run the `custom-settings` workflow to synchronize every affected surface (rules: CLAUDE.md § Product sources).');
      else messages.push('SPECIFICATION.md changed: confirm it stays consistent with CUSTOM_SETTINGS.md and records only approved behavior (CLAUDE.md § Product sources).');
    } else if (type === 'removed') {
      messages.push(`[manifest] ${rel} was removed: removing a project or manifest changes the project graph or the dependency set — confirm it was intended and approved (CLAUDE.md § Decisions; \`project-structure\`, \`add-dependency\`).`);
      projectRemoved ||= rel.endsWith('.csproj');
    } else {
      if (type === 'moved') {
        messages.push(`[manifest] ${change.from} was moved to ${rel}: update every reference to it (\`project-structure\`).`);
        projectRemoved ||= rel.endsWith('.csproj');
      }
      validate(rel);
      const refsBefore = type === 'changed' ? change.before.refs : [];
      const graphChanged = type === 'edited' ? graphHint : !sameList(refsBefore, change.after.refs);
      if (rel.endsWith('.csproj') && type !== 'baseline' && graphChanged) {
        messages.push(`[manifest] the project references of ${rel} changed: changing the project reference graph is Reserved (CLAUDE.md § Decisions) — confirm it was approved and recorded (\`architecture-decision\`), or revert it.`);
      }
    }
  }
  if (projectRemoved) {
    for (const rel of t.dependencies.checkRepository(root).files.filter((f) => f.endsWith('.csproj'))) validate(rel);
  }
  if (instructionsChanged && fs.existsSync(path.join(root, '.claude'))) {
    for (const e of script('check-instructions.cjs').check(root).errors) messages.push(`[instructions] ${e}`);
  }
  return messages;
}

function activeRoot(input, t, start) {
  return t.repo.resolveRoot(start || (typeof input.cwd === 'string' && input.cwd ? input.cwd : process.cwd()));
}

function postShell(event, input, t) {
  const resolved = activeRoot(input, t);
  if (!resolved || (!resolved.git && !fs.existsSync(path.join(resolved.root, '.claude')))) return; // not a repository of this system
  const messages = reactToChanges(resolved.root, observeWorktree(resolved.root, resolved.git, t), t, false);
  if (messages.length === 0) return;
  const what = event === 'post-tool-use-failure' ? 'the failed shell command (its partial changes count)' : 'the shell command';
  postFeedback(event, [`Worktree state after ${what} — ${resolved.root}:`, ...messages]);
}

function postEdit(event, input, t) {
  const target = input.tool_input?.file_path ?? input.tool_input?.notebook_path;
  if (typeof target !== 'string' || !target) return;
  const absolute = path.resolve(typeof input.cwd === 'string' && input.cwd ? input.cwd : process.cwd(), target);
  const resolved = activeRoot(input, t, path.dirname(absolute)); // the repository that contains the edited file
  const rel = resolved && t.repo.toRelative(resolved.root, absolute);
  const surface = rel && surfaceOf(rel, t);
  if (!surface) return;
  const { root } = resolved;
  const state = readState(root, 'worktree.json');
  const tracked = state?.version === 1;
  const before = tracked ? state.files[rel] : undefined;
  const after = entryFor(root, rel, surface, t);
  if (tracked) {
    if (after) state.files[rel] = after; else delete state.files[rel];
    writeState(root, 'worktree.json', state);
  }
  if (!after || before?.hash === after.hash) return;
  const edited = [input.tool_input.old_string, input.tool_input.new_string, input.tool_input.content, ...(input.tool_input.edits || []).flatMap((e) => [e.old_string, e.new_string])];
  const graphHint = edited.some((s) => typeof s === 'string' && /<ProjectReference\b/.test(s));
  const change = before ? { rel, surface, type: 'changed', before, after } : { rel, surface, type: 'edited', after };
  const messages = reactToChanges(root, [change], t, graphHint);
  if (messages.length > 0) postFeedback(event, messages);
}

// ---------------------------------------------------------------------------
// stop: co-change reminders (seed data, migrations, tests, custom settings) keyed to the material state
// ---------------------------------------------------------------------------

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

function stop(input, t) {
  if (input.stop_hook_active) return; // never loop on our own continuation
  const resolved = t.repo.resolveRoot(typeof input.cwd === 'string' && input.cwd ? input.cwd : process.cwd());
  if (!resolved || !resolved.git) fail(`co-change check skipped: ${resolved ? resolved.root : input.cwd} is not inside a Git work tree.`);
  const { root } = resolved;
  const paths = statusPaths(root, t).filter((p) => !p.startsWith('.claude/.hook-state/'));
  const identity = (list) => list.map((p) => `${p}@${t.repo.hashFile(path.join(root, p)) || 'deleted'}`).join(',');
  const isTest = (p) => /(^|\/)[^/]*Tests\//.test(p) || /\.spec\.ts$/.test(p);
  const reminders = [];

  const model = paths.filter((p) => /^backend\/[^/]+\.Domain\/.+\.cs$/.test(p)
    || /^backend\/[^/]+\.Infrastructure\/Persistence\/(Configurations\/.+|AppDbContext)\.cs$/.test(p));
  const seeder = paths.filter((p) => /\/Seeding\//.test(p) || /DbSeeder\.cs$/.test(p));
  if (model.length > 0 && seeder.length === 0 && findFile(path.join(root, 'backend'), 'DbSeeder.cs')) {
    reminders.push({ key: `seed:${identity(model)}`, text: 'Domain/persistence model changed without a seeder change: confirm seeded entities are unaffected or update the development seeder (`development-workflow` § Persistence or model change).' });
  }

  const migrations = paths.filter((p) => /^backend\/.+\/Migrations\/[^/]+\.cs$/.test(p) && !/(\.Designer|ModelSnapshot)\.cs$/.test(p));
  if (migrations.length > 0) {
    reminders.push({ key: `migration:${identity(migrations)}`, text: `Migration added or changed (${migrations.join(', ')}): review it before committing (\`development-workflow\` § Persistence or model change).` });
  }

  const production = paths.filter((p) => (/^backend\/.+\.cs$/.test(p) || /^frontend\/.+\.ts$/.test(p)) && !isTest(p) && !/\/Migrations\//.test(p));
  if (production.length > 0 && !paths.some(isTest)) {
    reminders.push({ key: `tests:${identity(production)}`, text: 'Production code changed without test changes: confirm existing coverage or add tests (`development-workflow` § Bug fix, `verify` § 4).' });
  }

  if (paths.includes('CUSTOM_SETTINGS.md')) {
    reminders.push({ key: `custom-settings:${identity(['CUSTOM_SETTINGS.md'])}`, text: 'CUSTOM_SETTINGS.md changed: confirm the `custom-settings` workflow synchronized every affected surface.' });
  }

  if (reminders.length === 0) return;
  const fingerprint = t.repo.hashText(reminders.map((r) => r.key).sort().join('|'));
  if (readState(root, 'stop.json')?.fingerprint === fingerprint) return; // this exact state was already reminded
  writeState(root, 'stop.json', { fingerprint });
  emit({ decision: 'block', reason: ['Co-change check before finishing:', ...reminders.map((r) => `- ${r.text}`)].join('\n') });
}

// ---------------------------------------------------------------------------

function main() {
  const event = process.argv.slice(2).find((arg) => EVENTS.includes(arg));
  if (!event) fail(`missing or unknown hook event; expected one of: ${EVENTS.join(', ')}`);
  if (event === 'pre-tool-use') {
    try {
      preToolUse(readInput());
    } catch (error) {
      preDecision('deny', [`[hook] the pre-command policy check could not run, so the command was blocked: ${error.message}`]);
    }
    process.exit(0);
  }
  let input;
  try {
    input = readInput();
  } catch (error) {
    fail(error.message);
  }
  try {
    const t = tools();
    if (event === 'stop') stop(input, t);
    else if (SHELL_TOOLS.includes(input.tool_name)) postShell(event, input, t);
    else if (event === 'post-tool-use' && EDIT_TOOLS.includes(input.tool_name)) postEdit(event, input, t);
  } catch (error) {
    fail(`${event} check failed: ${error.message}`);
  }
  process.exit(0);
}

if (require.main === module) main();

module.exports = { EVENTS, classifyCommand };
