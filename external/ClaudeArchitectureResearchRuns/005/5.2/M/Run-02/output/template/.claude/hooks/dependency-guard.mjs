#!/usr/bin/env node
// Claude Code hook for shell tool calls (Bash and PowerShell).
//   PreToolUse:  blocks npm installs that bypass peer-dependency resolution
//                (--force, -f, --legacy-peer-deps).
//   PostToolUse: after a dependency-changing command, checks the manifests and
//                routes Claude to the add-dependency workflow.
// Configured in .claude/settings.json as: node .claude/hooks/dependency-guard.mjs
// Manual test: echo '{"hook_event_name":"PreToolUse","tool_input":{"command":"npm i x --force"}}' | node .claude/hooks/dependency-guard.mjs

import { readInput, projectRoot, blockTool, postToolBlock, postToolContext, done, fail } from './hook-io.mjs';
import { checkManifests, formatResult } from '../scripts/check-manifests.mjs';

const NPM_INSTALL_LIKE = new Set([
  'install', 'i', 'in', 'ins', 'inst', 'insta', 'instal', 'isnt', 'isnta', 'isntal', 'add',
  'ci', 'clean-install', 'ic', 'install-clean', 'isntall-clean',
  'update', 'up', 'upgrade', 'udpate',
]);
const NPM_CHANGING = new Set([
  'install', 'i', 'in', 'ins', 'inst', 'insta', 'instal', 'isnt', 'isnta', 'isntal', 'add',
  'uninstall', 'un', 'unlink', 'remove', 'rm', 'r',
  'update', 'up', 'upgrade', 'udpate',
]);
const NPM_NEEDS_PACKAGE_ARG = new Set(['install', 'i', 'in', 'ins', 'inst', 'insta', 'instal', 'isnt', 'isnta', 'isntal', 'add']);

const input = readInput();
const event = input.hook_event_name;
const command = input.tool_input?.command;
if (typeof command !== 'string' || command.trim() === '') done();

const segments = command
  .split(/&&|\|\||[;|\r\n]/)
  .map((segment) => segment.trim().split(/\s+/).filter(Boolean).map(unquote))
  .filter((tokens) => tokens.length > 0)
  .map((tokens) => ({ tool: executable(tokens[0]), args: tokens.slice(1), text: tokens.join(' ') }));

if (event === 'PreToolUse') {
  for (const segment of segments) {
    if (segment.tool !== 'npm') continue;
    const sub = firstPositional(segment.args);
    const bypassFlag = segment.args.some((arg) => /^(--force|-f|--legacy-peer-deps)(=.*)?$/i.test(arg));
    const legacyConfig = segment.args.some((arg) => /legacy-peer-deps/i.test(arg));
    if ((NPM_INSTALL_LIKE.has(sub) && bypassFlag) || (sub === 'config' && legacyConfig)) {
      blockTool(
        `Blocked: "${segment.text}" bypasses npm peer-dependency resolution. ` +
        'Resolve the actual compatibility problem instead; see .claude/skills/add-dependency/SKILL.md (Apply, npm).',
      );
    }
  }
  done();
}

if (event === 'PostToolUse') {
  const changing = segments.filter(isDependencyChange);
  if (changing.length === 0) done();
  const root = projectRoot();
  const result = checkManifests(root);
  const lines = formatResult(result);
  const commands = changing.map((s) => s.text).join('; ');
  if (result.violations.length > 0) {
    postToolBlock(
      `Dependency command ran (${commands}) and the manifest check found violations:\n${lines.join('\n')}\n` +
      'Fix them following the owners named above; dependency changes follow the add-dependency workflow.',
    );
  }
  const notes = lines.length > 0 ? `\nManifest notes:\n${lines.join('\n')}` : '';
  postToolContext(
    `Dependency change detected (${commands}). If not already done, complete the add-dependency workflow ` +
    '(latest stable compatible version from the registry, deprecation/vulnerability/license checks, approval gates).' + notes,
  );
}

fail(`unexpected hook event "${event}"; register this script for PreToolUse/PostToolUse on Bash|PowerShell.`);

function unquote(token) {
  return token.replace(/^['"]+|['"]+$/g, '');
}

function executable(token) {
  const name = token.replace(/\\/g, '/').split('/').pop().toLowerCase();
  return name.replace(/\.(cmd|exe|ps1|bat)$/, '');
}

function firstPositional(args) {
  return (args.find((arg) => !arg.startsWith('-')) ?? '').toLowerCase();
}

function isDependencyChange(segment) {
  const { tool, args } = segment;
  const lower = args.map((a) => a.toLowerCase());
  if (tool === 'dotnet') {
    if ((lower[0] === 'add' || lower[0] === 'remove') && lower.includes('package')) return true;
    if (lower[0] === 'package' && ['add', 'remove', 'update'].includes(lower[1])) return true;
    return false;
  }
  if (tool === 'npm') {
    const sub = firstPositional(args);
    if (!NPM_CHANGING.has(sub)) return false;
    if (!NPM_NEEDS_PACKAGE_ARG.has(sub)) return true;
    const afterSub = args.slice(args.findIndex((a) => a.toLowerCase() === sub) + 1);
    return afterSub.some((arg) => !arg.startsWith('-'));
  }
  if (tool === 'pnpm' || tool === 'yarn') {
    return ['add', 'remove', 'rm', 'up', 'update', 'upgrade'].includes(firstPositional(args));
  }
  if (tool === 'ng') return firstPositional(args) === 'add';
  if (tool === 'npx') {
    const rest = args.filter((a) => !a.startsWith('-')).map((a) => a.toLowerCase());
    return (rest[0] === 'ng' || rest[0] === '@angular/cli') && rest[1] === 'add';
  }
  return false;
}
