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
