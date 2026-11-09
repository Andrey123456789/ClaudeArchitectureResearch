// Kind: ENF | Scope: repo/meta | Owns: PreToolUse guard for package-changing and repository-changing Git commands | Loads: PreToolUse hook (Bash|PowerShell)
//
// Routes package changes to the add-dependency workflow and repository-changing Git commands to
// CLAUDE.md § Git Safety. A command is let through when it carries the acknowledgment comment
// named in the message (a trailing comment is ignored by both bash and PowerShell).

import { readHookInput, fail, feedback } from './hook-io.mjs';

const HOOK = 'pre-command-guard';
export const DEPENDENCY_MARKER = '# add-dependency: done';
export const GIT_MARKER = '# git: user-requested';

const NPM_CHANGE = new Set(['install', 'i', 'add', 'uninstall', 'un', 'remove', 'rm', 'r', 'update', 'up', 'upgrade']);
const NPM_ARGLESS_CHANGE = new Set(['uninstall', 'un', 'remove', 'rm', 'r', 'update', 'up', 'upgrade']);
const GIT_ALWAYS_CHANGING = new Set([
  'commit', 'push', 'pull', 'merge', 'rebase', 'reset', 'revert', 'cherry-pick', 'clean', 'restore',
  'checkout', 'switch', 'add', 'rm', 'mv', 'am', 'apply', 'update-ref', 'filter-branch', 'replace',
]);
const GIT_READ_ONLY_FORMS = {
  branch: (args) => args.length === 0 || args.every((a) => /^(-a|-r|-v|-vv|--all|--remotes|--list|-l|--show-current|--verbose|--contains|--merged|--no-merged|--format=.*|--sort=.*|--color.*|--no-color)$/.test(a)),
  tag: (args) => args.length === 0 || args.every((a) => /^(-l|--list|-n\d*|--contains|--merged|--no-merged|--sort=.*|--format=.*|--points-at)$/.test(a)),
  stash: (args) => args.length > 0 && ['list', 'show'].includes(args[0]),
  worktree: (args) => args.length > 0 && args[0] === 'list',
  submodule: (args) => args.length === 0 || ['status', 'summary', 'foreach'].includes(args[0]),
  remote: (args) => args.length === 0 || ['-v', 'show', 'get-url'].includes(args[0]),
  notes: (args) => args.length === 0 || ['list', 'show'].includes(args[0]),
};

export function splitSegments(command) {
  return command
    .split(/\r?\n|&&|\|\||;|\|/)
    .map((segment) => segment.replace(/(^|\s)#.*$/, '').trim())
    .filter(Boolean);
}

export function tokenize(segment) {
  return (segment.match(/"[^"]*"|'[^']*'|\S+/g) ?? []).map((token) => token.replace(/^["']|["']$/g, ''));
}

function stripLauncher(tokens) {
  // Allow "& git ...", "npx ng ...", "cmd /c ..." style prefixes.
  let rest = tokens;
  while (rest.length && ['&', 'call', 'cmd', '/c', 'npx', 'pwsh', 'powershell', '-Command', '-c'].includes(rest[0])) {
    rest = rest.slice(1);
  }
  return rest;
}

export function isDependencyChange(segment) {
  const tokens = stripLauncher(tokenize(segment));
  if (!tokens.length) return false;
  const tool = tokens[0].toLowerCase().replace(/\.(exe|cmd)$/, '');
  const args = tokens.slice(1);
  const positional = args.filter((a) => !a.startsWith('-'));

  if (tool === 'dotnet') {
    if (positional[0] === 'add' && positional.includes('package')) return true;
    if (positional[0] === 'remove' && positional.includes('package')) return true;
    if (positional[0] === 'package' && ['add', 'remove', 'update'].includes(positional[1])) return true;
    return false;
  }
  if (tool === 'npm' || tool === 'pnpm' || tool === 'yarn') {
    const sub = positional[0];
    if (!sub) return false;
    if (args.some((a) => a === '--force' || a === '-f' || a === '--legacy-peer-deps')) return true;
    if (!NPM_CHANGE.has(sub)) return false;
    if (NPM_ARGLESS_CHANGE.has(sub) || tool !== 'npm') return true;
    return positional.length > 1; // "npm install" alone restores from the lockfile
  }
  if (tool === 'ng') {
    return ['add', 'update'].includes(positional[0]) && positional.length > 1;
  }
  return false;
}

export function isRepositoryChangingGit(segment) {
  const tokens = stripLauncher(tokenize(segment));
  if (!tokens.length || tokens[0].toLowerCase().replace(/\.exe$/, '') !== 'git') return false;
  let index = 1;
  while (index < tokens.length && tokens[index].startsWith('-')) {
    index += ['-C', '-c', '--git-dir', '--work-tree', '--namespace'].includes(tokens[index]) ? 2 : 1;
  }
  const sub = tokens[index];
  if (!sub) return false;
  const args = tokens.slice(index + 1);
  if (GIT_ALWAYS_CHANGING.has(sub)) return true;
  const readOnly = GIT_READ_ONLY_FORMS[sub];
  return readOnly ? !readOnly(args) : false;
}

export function evaluate(command) {
  const messages = [];
  const segments = splitSegments(command);
  if (!command.includes(DEPENDENCY_MARKER)) {
    const hits = segments.filter(isDependencyChange);
    if (hits.length) {
      messages.push(
        `Package change detected: ${hits.join(' | ')}\n` +
        'Follow the add-dependency workflow first (.claude/skills/add-dependency/SKILL.md).\n' +
        `When its steps are complete, re-run the same command with the trailing comment \`${DEPENDENCY_MARKER}\`.`,
      );
    }
  }
  if (!command.includes(GIT_MARKER)) {
    const hits = segments.filter(isRepositoryChangingGit);
    if (hits.length) {
      messages.push(
        `Repository-changing Git command detected: ${hits.join(' | ')}\n` +
        'Policy: CLAUDE.md § Git Safety. Procedure: .claude/skills/git-workflow/SKILL.md.\n' +
        `Re-run with the trailing comment \`${GIT_MARKER}\` only when the user explicitly requested this operation.`,
      );
    }
  }
  return messages;
}

const isEntryPoint = process.argv[1] && import.meta.url.endsWith(process.argv[1].split(/[\\/]/).pop());
if (isEntryPoint) {
  const input = await readHookInput(HOOK);
  const command = input?.tool_input?.command;
  if (typeof command !== 'string') {
    fail(HOOK, `tool "${input?.tool_name ?? 'unknown'}" provided no tool_input.command`);
  }
  const messages = evaluate(command);
  if (messages.length) {
    feedback(messages.join('\n\n'));
  }
  process.exit(0);
}
