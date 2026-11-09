#!/usr/bin/env node
// Claude Code hook for shell tool calls (Bash and PowerShell).
//   PreToolUse:  blocks npm installs that bypass peer-dependency resolution
//                (--force, -f, --legacy-peer-deps, or the equivalent npm config
//                and npm_config_* settings), and asks the user to confirm
//                repository-changing Git commands (K0's table; read-only Git
//                runs; a block always wins over the Git ask).
//   PostToolUse: after a dependency-changing or project-reference-changing
//                command, checks the manifests of the active repository root
//                (derived from the input "cwd") and routes Claude to the owner:
//                add-dependency for packages, architecture.md for project
//                references. After any other shell command, validates the
//                manifests whose content changed since the last manifest check
//                (hook-io.mjs, manifest state; one initial snapshot per
//                worktree) and reports removed manifests, so no shell mechanism
//                bypasses check-manifests; unchanged manifests are not re-checked.
//   PostToolUseFailure: a failed command may have changed some, all, or none of
//                what it targeted, so it is judged by the state it left behind:
//                manifests changed since the last manifest check are validated
//                as above (a dependency or reference command keeps its full
//                check and routing); nothing is reported when none changed.
// Registered in .claude/settings.json in exec form:
//   "command": "node", "args": ["${CLAUDE_PROJECT_DIR}/.claude/hooks/dependency-guard.mjs"]
// Invalid input fails closed in the script (exit 2): unreadable, empty or
// non-JSON input, JSON that is not an object, an event this script does not
// handle, and - for a PreToolUse shell call - a missing tool_name, tool_input or
// non-empty tool_input.command string. A PreToolUse call for another tool has
// nothing to gate and is allowed. onFailure "block" stays the backstop for a
// crash or timeout.
// Manual test (from the repository root; "cwd" defaults to the current directory):
//   echo '{"hook_event_name":"PreToolUse","tool_name":"Bash","tool_input":{"command":"npm --prefix frontend i x --force"}}' | node .claude/hooks/dependency-guard.mjs
//
// Command parsing is deliberately minimal: line continuations (\ or ` before a
// line break) are joined, segments split on ; | && || and line breaks, then
// whitespace-separated tokens. Leading VAR=value assignments and
// the PowerShell call operator are skipped, and a shell wrapper (cmd /c,
// bash -c, powershell -Command, ...) also yields its inner command as a
// segment. npm global options are skipped with
// their values (NPM_VALUE_OPTIONS); a non-option token that is not an npm command
// is treated as the value of an unlisted option, so it cannot hide the real
// subcommand. Not covered: npx npm ..., PowerShell -EncodedCommand, and an
// unlisted option whose value happens to be an npm command name.

import { readInput, startDirectory, activeRepository, manifestChanges, repoRelative, blockTool, askTool, postToolBlock, postToolContext, done, fail } from './hook-io.mjs';
import { resolveActiveRepository } from '../scripts/repo-root.mjs';
import { checkManifests, formatResult } from '../scripts/check-manifests.mjs';

const NPM_INSTALL = ['install', 'i', 'in', 'ins', 'inst', 'insta', 'instal', 'isnt', 'isnta', 'isntal', 'isntall', 'add'];
const NPM_CI = ['ci', 'clean-install', 'ic', 'install-clean', 'isntall-clean'];
const NPM_INSTALL_TEST = ['install-test', 'it', 'install-ci-test', 'cit', 'clean-install-test', 'sit'];
const NPM_UPDATE = ['update', 'up', 'upgrade', 'udpate'];
const NPM_UNINSTALL = ['uninstall', 'un', 'unlink', 'remove', 'rm', 'r'];
const NPM_CONFIG = ['config', 'c', 'set'];

const NPM_INSTALL_LIKE = new Set([...NPM_INSTALL, ...NPM_CI, ...NPM_INSTALL_TEST, ...NPM_UPDATE]);
const NPM_CHANGING = new Set([...NPM_INSTALL, ...NPM_UNINSTALL, ...NPM_UPDATE]);
const NPM_NEEDS_PACKAGE_ARG = new Set(NPM_INSTALL);

// Every npm command and alias, so that a token which is none of them is known
// to be an option value rather than the subcommand.
const NPM_COMMANDS = new Set([
  ...NPM_INSTALL, ...NPM_CI, ...NPM_INSTALL_TEST, ...NPM_UPDATE, ...NPM_UNINSTALL, ...NPM_CONFIG,
  'access', 'adduser', 'add-user', 'login', 'logout', 'audit', 'bugs', 'issues', 'cache', 'completion',
  'dedupe', 'ddp', 'deprecate', 'undeprecate', 'diff', 'dist-tag', 'dist-tags', 'docs', 'home', 'doctor',
  'edit', 'exec', 'x', 'explain', 'why', 'explore', 'find-dupes', 'fund', 'get', 'help', 'help-search',
  'hook', 'init', 'create', 'innit', 'link', 'ln', 'ls', 'list', 'la', 'll', 'org', 'ogr', 'outdated',
  'owner', 'author', 'pack', 'ping', 'pkg', 'prefix', 'profile', 'prune', 'publish', 'query', 'rebuild',
  'rb', 'repo', 'restart', 'root', 'run', 'run-script', 'rum', 'urn', 'sbom', 'search', 'find', 's', 'se',
  'shrinkwrap', 'star', 'stars', 'start', 'stop', 'team', 'test', 'tst', 't', 'token', 'unpublish',
  'unstar', 'version', 'verison', 'view', 'info', 'show', 'v', 'whoami',
]);

// npm options that take a separate value ("--prefix frontend").
const NPM_VALUE_OPTIONS = new Set([
  '--prefix', '-C', '--workspace', '-w', '--registry', '--userconfig', '--globalconfig', '--cache',
  '--loglevel', '--tag', '--otp', '--scope', '--include', '--omit', '--install-strategy', '--before',
  '--cafile', '--location',
]);

// Shell wrappers and the option that introduces the command they run.
const POSIX_COMMAND_FLAG = /^-[a-z]*c$/;
const POWERSHELL_COMMAND_FLAG = /^-c(o(m(m(a(n(d)?)?)?)?)?)?$/i;
const SHELL_WRAPPERS = new Map([
  ['cmd', /^\/[ck]$/i], ['bash', POSIX_COMMAND_FLAG], ['sh', POSIX_COMMAND_FLAG], ['zsh', POSIX_COMMAND_FLAG],
  ['pwsh', POWERSHELL_COMMAND_FLAG], ['powershell', POWERSHELL_COMMAND_FLAG],
]);

const BYPASS_FLAG = /^(--force|-f|--legacy-peer-deps)(=(.*))?$/i;
const BYPASS_CONFIG_KEY = /legacy-peer-deps|^force(=|$)/i;
const BYPASS_ENV = /\bnpm_config_(force|legacy_peer_deps)\s*=/i;

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

// Quote-aware split for the Git check: segments on unquoted ; | & && || and line
// breaks, then words. (The dependency parsing above stays deliberately minimal.)
function shellSegments(command) {
  const out = [];
  let words = [];
  let word = '';
  let started = false;
  let quote = null;
  const endWord = () => { if (started) words.push(word); word = ''; started = false; };
  const endSegment = () => { endWord(); if (words.length > 0) out.push(words); words = []; };
  const text = command.replace(/[\\`]\r?\n/g, ' ');
  for (let i = 0; i < text.length; i += 1) {
    const c = text[i];
    if (quote) {
      if (c === quote) quote = null;
      else word += c;
      continue;
    }
    if (c === '"' || c === "'") { quote = c; started = true; continue; }
    if (c === '&' && (text[i - 1] === '>' || text[i + 1] === '>')) { word += c; started = true; continue; } // 2>&1, &> redirections
    if (c === ';' || c === '|' || c === '&' || c === '\n' || c === '\r') { endSegment(); continue; }
    if (/\s/.test(c)) { endWord(); continue; }
    word += c;
    started = true;
  }
  endSegment();
  return out;
}

const GIT_PREFIXES = new Set(['env', 'cross-env', 'sudo', 'time', 'nohup', 'command', 'exec', 'call']);

// Repository-changing Git commands in the command text, inside shell wrappers too: [{ sub, text }].
function gitCommands(command, depth = 0) {
  const hits = [];
  for (let words of shellSegments(command)) {
    while (words.length > 0 && (GIT_PREFIXES.has(executable(words[0])) || /^[A-Za-z_][A-Za-z0-9_]*=/.test(words[0]))) words = words.slice(1);
    if (words.length === 0) continue;
    const tool = executable(words[0]);
    const commandFlag = SHELL_WRAPPERS.get(tool);
    if (commandFlag) {
      const at = words.findIndex((w, i) => i > 0 && commandFlag.test(w));
      if (at > 0 && depth < 3) hits.push(...gitCommands(words.slice(at + 1).join(' '), depth + 1));
      continue;
    }
    if (tool === 'git') {
      const sub = classifyGit(words.slice(1));
      if (sub) hits.push({ sub, text: words.join(' ') });
    }
  }
  return hits;
}

const input = readInput(invalidInput);
if (input === null || typeof input !== 'object' || Array.isArray(input)) invalidInput('hook input is not a JSON object');
const event = input.hook_event_name;
if (!['PreToolUse', 'PostToolUse', 'PostToolUseFailure'].includes(event)) {
  invalidInput(`hook input has no hook_event_name this script handles (got ${JSON.stringify(event)})`);
}
if (event === 'PreToolUse') {
  if (typeof input.tool_name !== 'string') invalidInput('PreToolUse hook input has no tool_name string');
  if (!['Bash', 'PowerShell'].includes(input.tool_name)) done(); // not a shell call: nothing for this guard to gate
  const toolInput = input.tool_input;
  if (toolInput === null || typeof toolInput !== 'object' || Array.isArray(toolInput)) invalidInput('PreToolUse hook input has no tool_input object');
  if (typeof toolInput.command !== 'string' || toolInput.command.trim() === '') invalidInput('PreToolUse hook input has no non-empty tool_input.command string');
}
const command = input.tool_input?.command;
if (typeof command !== 'string' || command.trim() === '') done(); // PostToolUse / PostToolUseFailure: nothing to check

const segments = command
  .replace(/[\\`]\r?\n/g, ' ')
  .split(/&&|\|\||[;|\r\n]/)
  .map((segment) => commandTokens(segment.trim().split(/\s+/).filter(Boolean).map(unquote)))
  .filter((tokens) => tokens.length > 0)
  .flatMap(unwrapShell)
  .map((tokens) => ({ tool: executable(tokens[0]), args: tokens.slice(1), text: tokens.join(' ') }));

if (event === 'PreToolUse') {
  const npmSegments = segments.filter((segment) => segment.tool === 'npm').map((segment) => ({ ...segment, npm: parseNpm(segment.args) }));
  if (BYPASS_ENV.test(command) && npmSegments.some((segment) => NPM_INSTALL_LIKE.has(segment.npm.sub))) {
    blockTool(
      'Blocked: the command sets npm_config_force or npm_config_legacy_peer_deps for an npm install, which ' +
      'bypasses npm peer-dependency resolution. Resolve the actual compatibility problem instead; see ' +
      '.claude/skills/add-dependency/SKILL.md (Apply, npm).',
    );
  }
  for (const { npm, text } of npmSegments) {
    const bypassFlag = npm.options.some(isBypassFlag);
    const bypassConfig = NPM_CONFIG.includes(npm.sub) &&
      (npm.positionals.some((arg) => BYPASS_CONFIG_KEY.test(arg)) || npm.options.some((arg) => /legacy-peer-deps/i.test(arg)));
    if ((NPM_INSTALL_LIKE.has(npm.sub) && bypassFlag) || bypassConfig) {
      blockTool(
        `Blocked: "${text}" bypasses npm peer-dependency resolution. ` +
        'Resolve the actual compatibility problem instead; see .claude/skills/add-dependency/SKILL.md (Apply, npm).',
      );
    }
  }
  const gitHits = gitCommands(command);
  if (gitHits.length > 0) askTool(gitAskReason(gitHits));
  done();
}

if (event === 'PostToolUse' || event === 'PostToolUseFailure') {
  const failed = event === 'PostToolUseFailure';
  const packageChanges = segments.filter((segment) => changeKind(segment) === 'package');
  const referenceChanges = segments.filter((segment) => changeKind(segment) === 'reference');
  const knownCommand = packageChanges.length > 0 || referenceChanges.length > 0;
  const commandOwners = [];
  if (packageChanges.length > 0) {
    commandOwners.push('complete the add-dependency workflow (latest stable compatible version from the registry, ' +
      'deprecation/vulnerability/license checks, approval gates)');
  }
  if (referenceChanges.length > 0) {
    commandOwners.push('confirm the project references follow .claude/rules/architecture.md (Project References) and that a ' +
      'changed production reference graph went through CLAUDE.md § Decision Control');
  }

  // Any other shell command, and any failed one: validate only the manifests
  // whose content changed since the last manifest check (sed, Set-Content, git
  // checkout, scripts, a partly completed dependency command...).
  if (!knownCommand || failed) {
    let repo;
    try {
      repo = resolveActiveRepository(startDirectory(input));
    } catch {
      if (knownCommand) activeRepository(input); // a failed dependency command: report that checks were NOT run
      done(); // outside every checkout; a change made from here is caught by the next check inside one
    }
    const { root } = repo;
    const manifests = manifestChanges(repo);
    const { changed, removed } = manifests;
    if (changed.length === 0 && removed.length === 0) {
      manifests.save();
      done();
    }
    // A removal can break what remains (package versions, project references),
    // so it is followed by a repository-wide manifest check, as is a failed
    // dependency or reference command (the check it gets when it succeeds).
    const result = removed.length > 0 || knownCommand ? checkManifests(root) : checkManifests(root, changed);
    manifests.save();
    const lines = formatResult(result);
    const what = [
      failed ? 'The shell command failed; the manifests were checked in the state it left behind' : '',
      manifests.first ? `Initial manifest check of ${root} (first check in this worktree)`
        : manifests.snapshot ? `Manifest snapshot of ${root} (the recorded HEAD could not be compared)`
        : changed.length > 0 ? `Manifests changed since the last manifest check: ${changed.map((file) => repoRelative(root, file)).join(', ')}` : '',
      removed.length > 0 ? `Manifests removed: ${removed.join(', ')}` : '',
    ].filter(Boolean).join('. ');
    const owners = (commandOwners.length > 0 ? commandOwners.join('; and ')
      : 'dependency changes follow the add-dependency workflow and project references follow ' +
        '.claude/rules/architecture.md (Project References)') +
      (removed.length > 0 ? '; a removed project or package-version file changes the project graph or dependency set, ' +
        'which goes through CLAUDE.md § Decision Control' : '');
    if (result.violations.length > 0) {
      postToolBlock(
        `${what}. The manifest check of ${root} found violations:\n${lines.join('\n')}\n` +
        `Fix them following the owners named above; ${owners}.`,
        event,
      );
    }
    // Initial or re-taken snapshot in which nothing violates (a failed
    // dependency or reference command is still routed, as when it succeeds).
    if (manifests.snapshot && removed.length === 0 && !knownCommand) done();
    postToolContext(
      `${what}; the manifest check of ${root} found no violations. If not already done, ${owners}.` +
      (lines.length > 0 ? `\nManifest notes:\n${lines.join('\n')}` : ''),
      event,
    );
  }

  const repo = activeRepository(input);
  const { root } = repo;
  const manifests = manifestChanges(repo);
  const result = checkManifests(root);
  manifests.save();
  const lines = formatResult(result);
  const commands = [...packageChanges, ...referenceChanges].map((s) => s.text).join('; ');
  if (result.violations.length > 0) {
    postToolBlock(
      `Command ran (${commands}) and the manifest check of ${root} found violations:\n${lines.join('\n')}\n` +
      `Fix them following the owners named above; also ${commandOwners.join('; and ')}.`,
    );
  }
  const notes = lines.length > 0 ? `\nManifest notes:\n${lines.join('\n')}` : '';
  postToolContext(
    `Manifest-changing command detected (${commands}); the manifest check of ${root} found no violations. ` +
    `If not already done, ${commandOwners.join('; and ')}.${notes}`,
  );
}

fail(`unexpected hook event "${event}"; register this script for PreToolUse/PostToolUse/PostToolUseFailure on Bash|PowerShell.`);

// Invalid hook input: the guard cannot classify the call, so it blocks (exit 2).
function invalidInput(reason) {
  blockTool(`Blocked: ${reason}. The dependency guard cannot classify this shell call, so it fails closed; report the hook input problem to the user.`);
}

function unquote(token) {
  return token.replace(/^['"]+|['"]+$/g, '');
}

// Drops leading VAR=value assignments and the PowerShell call operator.
function commandTokens(tokens) {
  let start = 0;
  while (start < tokens.length && (tokens[start] === '&' || tokens[start] === 'env' || tokens[start] === 'cross-env' || /^[A-Za-z_][A-Za-z0-9_]*=/.test(tokens[start]))) start += 1;
  return tokens.slice(start);
}

// A shell wrapper segment plus the command it runs ("cmd /c npm i x").
function unwrapShell(tokens) {
  const commandFlag = SHELL_WRAPPERS.get(executable(tokens[0]));
  if (!commandFlag) return [tokens];
  const flag = tokens.findIndex((token, i) => i > 0 && commandFlag.test(token));
  const inner = flag > 0 ? commandTokens(tokens.slice(flag + 1)) : [];
  return inner.length > 0 ? [tokens, ...unwrapShell(inner)] : [tokens];
}

function executable(token) {
  const name = token.replace(/\\/g, '/').split('/').pop().toLowerCase();
  return name.replace(/\.(cmd|exe|ps1|bat)$/, '');
}

// npm argument list -> { sub, positionals (after sub), options }.
function parseNpm(args) {
  const result = { sub: '', positionals: [], options: [] };
  for (let i = 0; i < args.length; i += 1) {
    const arg = args[i];
    if (arg === '--') break; // the rest belongs to a script, not to npm
    if (arg.startsWith('-')) {
      result.options.push(arg);
      if (!arg.includes('=') && NPM_VALUE_OPTIONS.has(arg)) i += 1;
    } else if (result.sub) {
      result.positionals.push(arg);
    } else if (NPM_COMMANDS.has(arg.toLowerCase())) {
      result.sub = arg.toLowerCase();
    }
    // else: the value of an option not listed in NPM_VALUE_OPTIONS
  }
  return result;
}

function isBypassFlag(option) {
  const m = BYPASS_FLAG.exec(option);
  return m !== null && (m[3] ?? '').toLowerCase() !== 'false';
}

// 'package' | 'reference' | null
function changeKind(segment) {
  const { tool, args } = segment;
  if (tool === 'dotnet') {
    const words = args.filter((a) => !a.startsWith('-')).map((a) => a.toLowerCase());
    if (words[0] === 'add' || words[0] === 'remove') {
      // dotnet add|remove [<PROJECT>] package|reference ...
      const noun = ['package', 'reference'].includes(words[1]) ? words[1] : words[2];
      return noun === 'package' || noun === 'reference' ? noun : null;
    }
    if (words[0] === 'package' && ['add', 'remove', 'update'].includes(words[1])) return 'package';
    if (words[0] === 'reference' && ['add', 'remove'].includes(words[1])) return 'reference';
    return null;
  }
  if (tool === 'npm') {
    const npm = parseNpm(args);
    if (!NPM_CHANGING.has(npm.sub)) return null;
    if (!NPM_NEEDS_PACKAGE_ARG.has(npm.sub)) return 'package';
    return npm.positionals.length > 0 ? 'package' : null;
  }
  const words = args.filter((a) => !a.startsWith('-')).map((a) => a.toLowerCase());
  if (tool === 'pnpm' || tool === 'yarn') {
    return ['add', 'remove', 'rm', 'up', 'update', 'upgrade'].includes(words[0]) ? 'package' : null;
  }
  if (tool === 'ng') return words[0] === 'add' ? 'package' : null;
  if (tool === 'npx') {
    return (words[0] === 'ng' || words[0] === '@angular/cli') && words[1] === 'add' ? 'package' : null;
  }
  return null;
}
