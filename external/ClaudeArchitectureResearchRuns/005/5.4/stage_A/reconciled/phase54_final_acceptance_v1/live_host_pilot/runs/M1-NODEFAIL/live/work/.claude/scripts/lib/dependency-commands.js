'use strict';
// Classifies shell commands (Bash or PowerShell text) that add, update, or remove
// NuGet/npm dependencies or change .NET project references. One parse drives both
// PreToolUse routing (analyzeCommand) and the PostToolUse manifest re-check
// (changesManifests), so the two phases cannot disagree.
// The command text is split into simple commands (quotes, comments, separators,
// redirections, heredocs), wrappers are removed, and each package manager's own
// global options are skipped before its subcommand is identified.
// An approval marker counts only in the trailing comment of the line that holds
// the command it approves. Messages point to the owning workflow and do not
// restate policy.

const DEPENDENCY_WORKFLOW = '.claude/skills/add-dependency/SKILL.md';
const REFERENCE_WORKFLOW = '.claude/skills/project-structure/SKILL.md';
const CHECKED = /#\s*add-dependency:\s*checked\b/i;
const REFERENCE_CHECKED = /#\s*project-reference:\s*checked\b/i;

// ---------- lexing ----------

// Removes heredoc bodies (Bash) and here-string bodies (PowerShell): they are data, not commands.
function stripHereDocs(text) {
  const lines = text.split(/\r?\n/);
  const kept = [];
  let terminator = null;
  for (const line of lines) {
    if (terminator) {
      if (terminator.test(line)) terminator = null;
      continue;
    }
    kept.push(line);
    const bash = /<<-?\s*(['"]?)([A-Za-z_][\w.-]*)\1/.exec(line);
    const here = /@(['"])\s*$/.exec(line);
    if (bash) terminator = new RegExp(`^\\s*${bash[2].replace(/[.*+?^${}()|[\]\\]/g, '\\$&')}\\s*$`);
    else if (here && line.split(here[1]).length % 2 === 0) terminator = new RegExp(`^\\s*${here[1]}@`);
  }
  return kept.join('\n');
}

// Line continuation: backslash in Bash, backtick in PowerShell (either when the shell is unknown).
const CONTINUATION = { Bash: /\\\r?\n/g, PowerShell: /`\r?\n/g };

// Splits command text into simple commands: [{ tokens, comment }]. The comment is the
// trailing comment of the physical line the command is on.
function segmentsOf(text, shell) {
  const source = stripHereDocs(String(text || '')).replace(CONTINUATION[shell] || /[\\`]\r?\n/g, ' ');
  const segments = [];
  for (const line of source.split(/\r?\n/)) {
    const lineSegments = [];
    let tokens = [];
    let token = null;
    let dropNext = false;
    let comment = '';
    const endToken = () => {
      if (token !== null) {
        if (dropNext) dropNext = false;
        else tokens.push(token);
      }
      token = null;
    };
    const endSegment = () => {
      endToken();
      if (tokens.length) lineSegments.push(tokens);
      tokens = [];
    };
    for (let i = 0; i < line.length; i++) {
      const c = line[i];
      if (c === "'" || c === '"') {
        let j = i + 1;
        let value = '';
        while (j < line.length && line[j] !== c) {
          if (c === '"' && (line[j] === '\\' || line[j] === '`') && line[j + 1] === '"') j++;
          value += line[j];
          j++;
        }
        token = (token || '') + value;
        i = j;
      } else if (/\s/.test(c)) {
        endToken();
      } else if (c === '#' && token === null) {
        comment = line.slice(i);
        break;
      } else if (c === '>' || c === '<') {
        if (token !== null && /^(\d+|\*)$/.test(token)) token = null;
        endToken();
        while (line[i + 1] === '>' || line[i + 1] === '<') i++;
        if (line[i + 1] === '&') {
          i++;
          while (/[\d-]/.test(line[i + 1] || '')) i++;
        } else {
          dropNext = true;
        }
      } else if (c === ';' || c === '|' || c === '(' || c === ')') {
        endSegment();
        if (line[i + 1] === c) i++;
      } else if (c === '&') {
        if (line[i + 1] === '>') continue;
        if (line[i + 1] === '&') {
          endSegment();
          i++;
        } else if (tokens.length === 0 && token === null) {
          // PowerShell call operator at the start of a command.
        } else {
          endSegment();
        }
      } else if ((c === '{' || c === '}') && token === null && (i + 1 === line.length || /\s/.test(line[i + 1]))) {
        endSegment();
      } else {
        token = (token || '') + c;
      }
    }
    endSegment();
    for (const t of lineSegments) segments.push({ tokens: t, comment });
  }
  return segments;
}

// ---------- command model ----------

const WRAPPERS = new Set(['sudo', 'env', 'time', 'command', 'exec', 'nohup', 'call', 'if', 'then', 'else', 'elif', 'do', 'while', 'until', '!', 'start']);
// Shells whose command-string argument is classified as a nested command.
const POSIX_SHELL = { flag: /^-[A-Za-z]*c[A-Za-z]*$/, shell: 'Bash' };
const POWERSHELL = { flag: /^-c(?:o(?:m(?:m(?:a(?:n(?:d)?)?)?)?)?)?$/i, shell: 'PowerShell' };
const SHELLS = { bash: POSIX_SHELL, sh: POSIX_SHELL, zsh: POSIX_SHELL, dash: POSIX_SHELL, cmd: { flag: /^\/[ck]$/i, shell: null }, pwsh: POWERSHELL, powershell: POWERSHELL };

function exeName(token) {
  return token.split(/[\\/]/).pop().toLowerCase().replace(/\.(exe|cmd|bat|ps1)$/, '');
}

function isOption(t) {
  return /^-{1,2}[A-Za-z]/.test(t) || t === '--';
}

function optionName(t) {
  return t.split('=')[0].toLowerCase();
}

// Separates options from positional arguments. valueOptions consume the next token;
// an unknown option consumes the next token only when that token is not a known verb.
function splitArgs(args, valueOptions, knownVerbs) {
  const options = [];
  const positionals = [];
  for (let i = 0; i < args.length; i++) {
    const t = args[i];
    if (t === '--') {
      positionals.push(...args.slice(i + 1));
      break;
    }
    if (!isOption(t)) {
      positionals.push(t);
      continue;
    }
    options.push(optionName(t));
    if (t.includes('=')) continue;
    const next = args[i + 1];
    if (next === undefined || isOption(next)) continue;
    if (valueOptions.has(optionName(t))) {
      options.push(`${optionName(t)}=${next}`);
      i++;
    } else if (!t.startsWith('--') || positionals.length || knownVerbs.has(next.toLowerCase())) {
      continue;
    } else if (!valueOptions.boolean || !valueOptions.boolean.has(optionName(t))) {
      // Unknown long option before the verb: treat the following non-verb token as its value.
      i++;
    }
  }
  return { options, positionals };
}

function withBooleans(values, booleans) {
  const set = new Set(values);
  set.boolean = new Set(booleans);
  return set;
}

// addition: the command adds a named package (otherwise it updates or removes).
function packageOp(manager, verb, positionals, options, mode, addition = false) {
  return { type: 'package', manager, verb, packages: positionals, options, mode, addition: addition && positionals.length > 0 };
}

// mode: 'change' (routed to add-dependency), 'restore' (installs from manifests: force-flag policy only).
const NPM_VERBS = new Map([
  ...['install', 'i', 'in', 'ins', 'inst', 'insta', 'instal', 'isnt', 'isnta', 'isntal', 'isntall', 'add'].map((v) => [v, 'install']),
  ...['uninstall', 'unlink', 'remove', 'rm', 'r', 'un'].map((v) => [v, 'remove']),
  ...['update', 'up', 'upgrade', 'udpate'].map((v) => [v, 'update']),
  ...['ci', 'clean-install', 'ic', 'install-clean', 'isntall-clean', 'install-test', 'it', 'install-ci-test', 'cit'].map((v) => [v, 'restore']),
  ['audit', 'audit'],
  ...['exec', 'x'].map((v) => [v, 'exec']),
]);
const NPM_VALUE_OPTIONS = withBooleans(
  ['--prefix', '-c', '--workspace', '-w', '--registry', '--cache', '--userconfig', '--globalconfig', '--loglevel', '--tag', '--before', '--omit', '--include', '--install-strategy', '--location', '--otp', '--scope', '--os', '--cpu', '--libc', '--package', '-p', '--call'],
  ['--global', '--save-dev', '--save-exact', '--save-optional', '--save-peer', '--save-prod', '--no-save', '--force', '--legacy-peer-deps', '--dry-run', '--workspaces', '--include-workspace-root', '--yes', '--no', '--silent', '--verbose', '--quiet', '--prefer-offline', '--offline', '--ignore-scripts', '--fix']
);

const PNPM_VERBS = new Map([
  ['add', 'install'],
  ...['install', 'i'].map((v) => [v, 'install']),
  ...['remove', 'rm', 'uninstall', 'un'].map((v) => [v, 'remove']),
  ...['update', 'up', 'upgrade'].map((v) => [v, 'update']),
  ['audit', 'audit'],
  ...['exec', 'dlx'].map((v) => [v, 'exec']),
]);
const PNPM_VALUE_OPTIONS = withBooleans(
  ['--dir', '-c', '--filter', '-f', '--reporter', '--loglevel', '--store-dir', '--registry', '--workspace-concurrency', '--test-pattern', '--changed-files-ignore-pattern', '--config-dir', '--modules-dir', '--virtual-store-dir', '--package'],
  ['--recursive', '--workspace-root', '--save-dev', '--save-exact', '--save-optional', '--global', '--silent', '--stream', '--parallel', '--color', '--no-color', '--aggregate-output', '--frozen-lockfile', '--offline', '--prefer-offline', '--force', '--fix', '--latest', '--interactive']
);

const YARN_VERBS = new Map([
  ['add', 'install'],
  ['install', 'install'],
  ['remove', 'remove'],
  ...['upgrade', 'up', 'upgrade-interactive'].map((v) => [v, 'update']),
  ...['exec', 'dlx'].map((v) => [v, 'exec']),
  ['workspace', 'workspace'],
  ['global', 'global'],
]);
const YARN_VALUE_OPTIONS = withBooleans(
  ['--cwd', '--mutex', '--cache-folder', '--modules-folder', '--global-folder', '--link-folder', '--network-timeout', '--registry', '--use-yarnrc', '--network-concurrency', '--child-concurrency', '--otp', '--package', '-p'],
  ['--dev', '-d', '--exact', '-e', '--optional', '--peer', '--tilde', '--silent', '--verbose', '--offline', '--frozen-lockfile', '--immutable', '--force', '--ignore-scripts', '--latest', '--interactive']
);

const NG_VERBS = new Map([['add', 'install'], ['update', 'update'], ['new', 'scaffold']]);

function classifyNode(manager, args, verbs, valueOptions) {
  const { options, positionals } = splitArgs(args, valueOptions, new Set(verbs.keys()));
  if (!positionals.length) return manager === 'yarn' ? [packageOp(manager, 'install', [], options, 'restore')] : [];
  const verbToken = positionals[0].toLowerCase();
  const rest = args.slice(args.indexOf(positionals[0]) + 1);
  const kind = verbs.get(verbToken);
  const pkgs = positionals.slice(1);
  if (manager === 'yarn' && verbToken === 'ng') return classifyTokens(['ng', ...rest]);
  if (!kind) return [];
  switch (kind) {
    case 'install':
      return [packageOp(manager, verbToken, pkgs, options, pkgs.length ? 'change' : 'restore', true)];
    case 'remove':
    case 'update':
      return [packageOp(manager, verbToken, pkgs, options, 'change')];
    case 'restore':
      return [packageOp(manager, verbToken, pkgs, options, 'restore')];
    case 'audit':
      return options.includes('--fix') || pkgs[0] === 'fix' ? [packageOp(manager, 'audit fix', pkgs.slice(1), options, 'change')] : [];
    case 'exec': {
      const { positionals: inner } = splitArgs(rest, valueOptions, new Set());
      const start = rest.indexOf(inner[0]);
      return start >= 0 ? classifyTokens(rest.slice(start)) : [];
    }
    case 'workspace':
      return pkgs.length ? classifyNode(manager, rest.slice(rest.indexOf(pkgs[0]) + 1), verbs, valueOptions) : [];
    case 'global':
      return classifyNode(manager, rest, verbs, valueOptions);
    default:
      return [];
  }
}

// dotnet add|remove [<PROJECT>] package|reference ..., and the noun-first
// dotnet package add|remove|update / dotnet reference add|remove forms.
function classifyDotnet(args) {
  let i = 0;
  while (i < args.length && ['-d', '--diagnostics'].includes(args[i].toLowerCase())) i++;
  const verb = (args[i] || '').toLowerCase();
  const rest = args.slice(i + 1);
  const positionals = rest.filter((t) => !isOption(t));
  const options = rest.filter(isOption).map(optionName);
  if (verb === 'add' || verb === 'remove') {
    const first = (positionals[0] || '').toLowerCase();
    const explicitProject = first !== 'package' && first !== 'reference';
    const noun = (explicitProject ? positionals[1] || '' : first).toLowerCase();
    const operands = positionals.slice(explicitProject ? 2 : 1);
    const project = explicitProject ? positionals[0] : null;
    if (noun === 'package') return [packageOp('dotnet', `${verb} package`, operands.slice(0, 1), options, 'change', verb === 'add')];
    if (noun === 'reference') return [{ type: 'reference', verb, project, targets: operands }];
    return [];
  }
  if (verb === 'package') {
    const sub = (positionals[0] || '').toLowerCase();
    if (['add', 'remove', 'update'].includes(sub)) return [packageOp('dotnet', `package ${sub}`, positionals.slice(1), options, 'change', sub === 'add')];
    return [];
  }
  if (verb === 'reference') {
    const sub = (positionals[0] || '').toLowerCase();
    const p = rest.findIndex((t) => optionName(t) === '--project');
    if (['add', 'remove'].includes(sub)) return [{ type: 'reference', verb: sub, project: p >= 0 ? rest[p + 1] : null, targets: positionals.slice(1).filter((t) => p < 0 || t !== rest[p + 1]) }];
    return [];
  }
  if (verb === 'new' || verb === 'sln' || verb === 'solution') return [{ type: 'scaffold', tool: 'dotnet', verb }];
  return [];
}

function classifyFrameworkCli(args) {
  const { options, positionals } = splitArgs(args, new Set(), new Set(NG_VERBS.keys()));
  const verb = (positionals[0] || '').toLowerCase();
  const kind = NG_VERBS.get(verb);
  if (kind === 'scaffold') return [{ type: 'scaffold', tool: 'ng', verb }];
  if (kind === 'install') return positionals.length > 1 ? [packageOp('ng', verb, positionals.slice(1), options, 'change', true)] : [];
  if (kind === 'update') return positionals.length > 1 || options.includes('--all') ? [packageOp('ng', verb, positionals.slice(1), options, 'change')] : [];
  return [];
}

// Classifies one simple command given as tokens; returns a list of operations.
function classifyTokens(tokens) {
  let t = tokens.slice();
  while (t.length && (WRAPPERS.has(t[0].toLowerCase()) || /^[A-Za-z_][A-Za-z0-9_]*=/.test(t[0]) || /^\$env:/i.test(t[0]))) {
    if (/^\$env:/i.test(t[0]) && t[1] === '=') t = t.slice(3);
    else t = t.slice(1);
  }
  if (!t.length) return [];
  const exe = exeName(t[0]);
  const args = t.slice(1);
  if (Object.prototype.hasOwnProperty.call(SHELLS, exe)) {
    const flag = args.findIndex((a) => SHELLS[exe].flag.test(a));
    return flag >= 0 ? segmentsOf(args.slice(flag + 1).join(' '), SHELLS[exe].shell).flatMap((s) => classifyTokens(s.tokens)) : [];
  }
  switch (exe) {
    case 'npm':
      return classifyNode('npm', args, NPM_VERBS, NPM_VALUE_OPTIONS);
    case 'pnpm':
      return classifyNode('pnpm', args, PNPM_VERBS, PNPM_VALUE_OPTIONS);
    case 'yarn':
      return classifyNode('yarn', args, YARN_VERBS, YARN_VALUE_OPTIONS);
    case 'npx':
    case 'pnpx':
    case 'corepack': {
      const { positionals } = splitArgs(args, NPM_VALUE_OPTIONS, new Set());
      const start = args.indexOf(positionals[0]);
      return start >= 0 ? classifyTokens(args.slice(start)) : [];
    }
    case 'ng':
      return classifyFrameworkCli(args);
    case 'dotnet':
      return classifyDotnet(args);
    case 'nuget': {
      const verb = (args.find((a) => !isOption(a)) || '').toLowerCase();
      return ['install', 'update', 'delete'].includes(verb) ? [packageOp('nuget', verb, [], args.filter(isOption).map(optionName), 'change')] : [];
    }
    case 'install-package':
    case 'update-package':
    case 'uninstall-package':
      return [packageOp('nuget', exe, args.filter((a) => !isOption(a)).slice(0, 1), args.filter(isOption).map(optionName), 'change', exe === 'install-package')];
    default:
      return [];
  }
}

// Every dependency or project-reference operation in the command text, each with the
// trailing comment of its own line and the simple command it came from.
// shell: the tool that runs the text ('Bash' or 'PowerShell'); optional.
function classifyCommand(command, shell) {
  const ops = [];
  for (const segment of segmentsOf(command, shell)) {
    for (const op of classifyTokens(segment.tokens)) ops.push({ ...op, comment: segment.comment, text: segment.tokens.join(' ') });
  }
  return ops;
}

const FORCE_OPTIONS = new Set(['--force', '-f', '--legacy-peer-deps']);
const FORCE_MANAGERS = new Set(['npm', 'pnpm', 'yarn']);

function forceFlag(op) {
  if (op.type !== 'package' || !FORCE_MANAGERS.has(op.manager)) return null;
  return op.options.find((o) => FORCE_OPTIONS.has(o) && (o !== '-f' || op.manager === 'npm')) || null;
}

function versionNotes(op) {
  const notes = [];
  const text = [...op.packages, ...op.options].join(' ');
  if (op.options.includes('--prerelease') || /@(?:next|canary|beta|alpha|rc)\b/i.test(text)) notes.push('The command requests a prerelease version.');
  if (/--version=["']?\*|@\*(?:\s|$)|@latest\b/i.test(text) || (op.options.includes('--version') && /(?:^|\s)\*(?:\s|$)/.test(op.text))) {
    notes.push('The command requests a floating or unresolved version.');
  }
  return notes;
}

function describe(op) {
  if (op.type === 'reference') return `project reference ${op.verb}`;
  const what = op.manager === 'dotnet' || op.manager === 'nuget' ? 'NuGet package' : op.manager === 'ng' ? 'frontend package' : `${op.manager} package`;
  return `${what} ${op.addition ? 'addition' : 'change'}`;
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

// Repository-changing Git commands, after wrappers and nested shells: [{ sub, text }]. Kept apart from
// classifyCommand, so changesManifests (the post-command manifest re-check) does not change meaning.
function gitOperations(command, shell, depth = 0) {
  const hits = [];
  for (const segment of segmentsOf(command, shell)) {
    let t = segment.tokens.slice();
    while (t.length && (WRAPPERS.has(t[0].toLowerCase()) || /^[A-Za-z_][A-Za-z0-9_]*=/.test(t[0]) || /^\$env:/i.test(t[0]))) {
      if (/^\$env:/i.test(t[0]) && t[1] === '=') t = t.slice(3);
      else t = t.slice(1);
    }
    if (!t.length) continue;
    const exe = exeName(t[0]);
    const args = t.slice(1);
    if (Object.prototype.hasOwnProperty.call(SHELLS, exe)) {
      const flag = args.findIndex((a) => SHELLS[exe].flag.test(a));
      if (flag >= 0 && depth < 3) hits.push(...gitOperations(args.slice(flag + 1).join(' '), SHELLS[exe].shell, depth + 1));
      continue;
    }
    if (exe === 'git') {
      const sub = classifyGit(args);
      if (sub) hits.push({ sub, text: t.join(' ') });
    }
  }
  return hits;
}

// Returns { block: boolean, ask?: boolean, message?: string }. A dependency or reference block always wins;
// otherwise a repository-changing Git command asks.
function analyzeCommand(command, shell) {
  const verdict = dependencyVerdict(command, shell);
  if (verdict.block) return verdict;
  const git = gitOperations(command, shell);
  return git.length ? { block: false, ask: true, message: gitAskReason(git) } : verdict;
}

// Returns { block: boolean, message?: string }.
function dependencyVerdict(command, shell) {
  const ops = classifyCommand(command, shell);
  const peerConfig = segmentsOf(command, shell).find((s) => /^(\S*[\\/])?npm(\.cmd)?\s.*\bconfig\s+set\s+(legacy-peer-deps|force)(=true|\s+true)\b/i.test(s.tokens.join(' ')));
  if (peerConfig || (/\bnpm_config_(force|legacy_peer_deps)\s*=\s*['\"]?(true|1)\b/i.test(String(command)) && /\bnpm(\.cmd)?\s/i.test(String(command)))) {
    return {
      block: true,
      message: 'npm peer-dependency bypass configured for this command.\n'
        + `Resolve the actual compatibility problem instead (${DEPENDENCY_WORKFLOW}, Install). No confirmation, comment marker, or approval opens this route.\n`,
    };
  }
  for (const op of ops) {
    const flag = forceFlag(op);
    if (flag) {
      return {
        block: true,
        message:
          `Peer-dependency override flag detected (${flag}) in: ${op.text}\n` +
          `Resolve the actual compatibility problem instead (${DEPENDENCY_WORKFLOW}, Install).\n` +
          'No confirmation, comment marker, or approval opens this route.\n',
      };
    }
  }
  const references = ops.filter((op) => op.type === 'reference' && !REFERENCE_CHECKED.test(op.comment));
  if (references.length) {
    return {
      block: true,
      message:
        `Project-reference change detected (${describe(references[0])}) in: ${references[0].text}\n` +
        `Apply the project-structure workflow first (${REFERENCE_WORKFLOW}, Changing Project References): it checks the change against the dependency direction and the frame's reference layout and routes Reserved reference-graph changes to the architecture-decision workflow.\n` +
        'After completing it, re-run the same command with the trailing comment: # project-reference: checked\n' +
        'The post-command architecture check then validates the resulting project references.\n',
    };
  }
  const changes = ops.filter((op) => op.type === 'package' && op.mode === 'change' && !CHECKED.test(op.comment));
  if (!changes.length) return { block: false };
  const op = changes[0];
  const notes = versionNotes(op);
  return {
    block: true,
    message:
      `Dependency change detected (${describe(op)}) in: ${op.text}\n` +
      `Run the add-dependency workflow first (${DEPENDENCY_WORKFLOW}): need and approval check, package choice, latest stable compatible version, deprecation, vulnerability, and license checks.\n` +
      (notes.length ? `${notes.join(' ')}\n` : '') +
      'After completing it, re-run the same command with the trailing comment: # add-dependency: checked\n',
  };
}

// Commands after which manifests or project references may have changed.
function changesManifests(command, shell) {
  return classifyCommand(command, shell).length > 0;
}

module.exports = { analyzeCommand, changesManifests, classifyCommand, gitOperations, classifyGit };
