// Pure copied definitions from K0 hook lines 18..19 and 72..275. No entry point or filesystem operations.
const DEPENDENCY_MARKER = /#\s*add-dependency:\s*reviewed\b/i;
const REFERENCE_MARKER = /#\s*project-references:\s*approved\b/i;
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

const cases = [
 {kind:'dependency', command:'npm install example-package --cache "# add-dependency: reviewed"'},
 {kind:'reference', command:'dotnet add reference "dir/# project-references: approved/Other.csproj"'},
];
const results = cases.map(c => ({...c, classification:classifyCommand(c.command), markerMatches:(c.kind==='dependency'?DEPENDENCY_MARKER:REFERENCE_MARKER).test(c.command), markerInsideQuotedArgument:true}));
console.log(JSON.stringify({pureClassifierOnly:true,commandsExecuted:false,results}, null, 2));
