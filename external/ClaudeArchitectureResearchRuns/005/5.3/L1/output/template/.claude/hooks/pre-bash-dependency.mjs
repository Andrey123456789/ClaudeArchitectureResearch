#!/usr/bin/env node
// PreToolUse (Bash|PowerShell), critical and fail-closed (settings: onFailure "block").
// Routes commands before they run:
// - package dependency changes (NuGet/npm/pnpm/yarn, framework CLI commands declared by the selected
//   frontend module) → deny once with a pointer to the add-dependency workflow;
// - project-reference changes (dotnet add/remove reference, dotnet reference add/remove) → deny once
//   with a pointer to decision control and the project-structure workflow;
// - peer-dependency bypass flags (--force, -f, --legacy-peer-deps) → user confirmation.
// The identical command is allowed when retried within the grace window (after the workflow ran).
// Unreadable input, missing configuration, and internal errors deny the command instead of allowing it.
// Command-text routing only; the post-change hook validates the actual resulting state.
import path from 'node:path';
import { pathToFileURL } from 'node:url';
import {
  loadJsonFacet, parseSelection, readHookInput, readState, requireConfigRoot, resolveContext, stateFile, writeState,
} from '../scripts/lib/project.mjs';

const GRACE_MS = 30 * 60 * 1000;

// ---- command tokenizer -------------------------------------------------------------------------

// Splits a command line into segments at && || ; | & and newlines outside quotes, and each segment
// into words with quotes removed. Good enough for routing; it is not a full shell parser.
export function segments(command) {
  const out = [];
  let words = [];
  let word = '';
  let inWord = false;
  let quote = null;
  const pushWord = () => { if (inWord) words.push(word); word = ''; inWord = false; };
  const pushSegment = () => { pushWord(); if (words.length) out.push(words); words = []; };
  const s = String(command || '');
  for (let i = 0; i < s.length; i++) {
    const c = s[i];
    if (quote) {
      if (c === quote) { quote = null; continue; }
      if (quote === '"' && c === '\\' && (s[i + 1] === '"' || s[i + 1] === '\\')) { word += s[++i]; continue; }
      word += c; continue;
    }
    if (c === '"' || c === "'") { quote = c; inWord = true; continue; }
    if (c === '\r' || c === '\n' || c === ';') { pushSegment(); continue; }
    if (c === '&' || c === '|') {
      if (s[i + 1] === c) i++;
      // PowerShell call operator "& npm ..." starts a command rather than ending one.
      if (c === '&' && !inWord && words.length === 0) continue;
      pushSegment(); continue;
    }
    if (c === '(' || c === ')' || c === '{' || c === '}') { pushSegment(); continue; }
    if (/\s/.test(c)) { pushWord(); continue; }
    word += c; inWord = true;
  }
  pushSegment();
  return out;
}

const exeName = (w) => path.basename(String(w).replace(/\\/g, '/')).toLowerCase().replace(/\.(exe|cmd|bat|ps1)$/, '');
const WRAPPERS = new Set(['sudo', 'env', 'command', 'exec', 'time', 'nohup', 'call', 'start', 'xargs']);
const SHELLS = new Set(['bash', 'sh', 'zsh', 'cmd', 'powershell', 'pwsh']);

// Removes leading environment assignments and wrapper commands; expands nested shell invocations.
function normalize(words, depth, results) {
  let i = 0;
  while (i < words.length && /^[A-Za-z_][A-Za-z0-9_]*=/.test(words[i])) i++;
  while (i < words.length && WRAPPERS.has(exeName(words[i]))) {
    i++;
    while (i < words.length && (words[i].startsWith('-') || /^[A-Za-z_][A-Za-z0-9_]*=/.test(words[i]))) i++;
  }
  const rest = words.slice(i);
  if (!rest.length) return null;
  const exe = exeName(rest[0]);
  if (SHELLS.has(exe) && depth < 3) {
    const scriptFlag = exe === 'cmd' ? /^\/[ck]$/i : exe === 'powershell' || exe === 'pwsh' ? /^-(c|command)$/i : /^-[A-Za-z]*c[A-Za-z]*$/;
    const idx = rest.findIndex((w, k) => k > 0 && scriptFlag.test(w));
    if (idx > 0 && rest[idx + 1] !== undefined) {
      collect(rest.slice(idx + 1).join(' '), depth + 1, results);
      return null;
    }
  }
  return rest;
}

// Long options compare case-insensitively; short options keep their case (-f force vs -F filter).
const optionKey = (w) => (w.startsWith('--') ? w.toLowerCase() : w);

// ---- package-manager grammars ------------------------------------------------------------------

const NPM_VALUE_OPTIONS = new Set(['--prefix', '-C', '--workspace', '-w', '--userconfig', '--globalconfig', '--registry', '--cache',
  '--loglevel', '--location', '--tag', '--omit', '--include', '--install-strategy', '--save-prefix', '--otp', '--before']);
const PNPM_VALUE_OPTIONS = new Set(['--dir', '-C', '--filter', '-F', '--workspace-dir', '--store-dir', '--registry', '--reporter', '--loglevel']);
const YARN_VALUE_OPTIONS = new Set(['--cwd', '--modules-folder', '--cache-folder', '--registry', '--mutex', '--network-timeout']);
const FORCE_FLAGS = new Set(['--force', '-f', '--legacy-peer-deps', '--force=true', '--legacy-peer-deps=true']);

const NPM_INSTALL = new Set(['install', 'i', 'in', 'ins', 'inst', 'insta', 'instal', 'isnt', 'isnta', 'isntal', 'isntall', 'add']);
const NPM_REMOVE = new Set(['uninstall', 'remove', 'rm', 'r', 'un', 'unlink']);
const NPM_UPDATE = new Set(['update', 'up', 'upgrade', 'udpate']);
const NPM_CLEAN = new Set(['ci', 'clean-install', 'ic', 'install-clean', 'isntall-clean', 'install-ci-test', 'cit', 'install-test', 'it']);

// Splits words after the executable into { verb, args } while skipping global options and their values.
function verbAndArgs(words, valueOptions) {
  let k = 1;
  const flags = [];
  while (k < words.length && words[k].startsWith('-')) {
    const opt = optionKey(words[k]);
    flags.push(opt);
    k += !opt.includes('=') && valueOptions.has(opt) ? 2 : 1;
  }
  const verb = (words[k] || '').toLowerCase();
  const args = [];
  for (let j = k + 1; j < words.length; j++) {
    const w = words[j];
    if (w.startsWith('-')) {
      const opt = optionKey(w);
      flags.push(opt);
      if (!opt.includes('=') && valueOptions.has(opt)) j++;
    } else args.push(w);
  }
  return { verb, args, flags };
}

function classifyNodeManager(exe, words, result) {
  if (exe === 'yarn' && (words[1] || '').toLowerCase() === 'workspace' && words.length > 2) words = [words[0], ...words.slice(3)];
  if (exe === 'yarn' && (words[1] || '').toLowerCase() === 'workspaces' && (words[2] || '').toLowerCase() === 'foreach') {
    const v = words.findIndex((w, k) => k > 2 && !w.startsWith('-'));
    if (v > 0) words = [words[0], ...words.slice(v)];
  }
  const options = exe === 'npm' ? NPM_VALUE_OPTIONS : exe === 'pnpm' ? PNPM_VALUE_OPTIONS : YARN_VALUE_OPTIONS;
  const { verb, args, flags } = verbAndArgs(words, options);
  const force = flags.some((f) => FORCE_FLAGS.has(f));
  const hasArgs = args.length > 0;
  let dependency = false;
  let installLike = false;
  if (exe === 'npm') {
    if (NPM_INSTALL.has(verb)) { installLike = true; dependency = hasArgs; }
    else if (NPM_REMOVE.has(verb)) { installLike = true; dependency = hasArgs; }
    else if (NPM_UPDATE.has(verb)) { installLike = true; dependency = true; }
    else if (NPM_CLEAN.has(verb)) installLike = true;
    else if (verb === 'audit' && (args[0] || '').toLowerCase() === 'fix') { installLike = true; dependency = true; }
    else if (verb === 'pkg' && ['set', 'delete'].includes((args[0] || '').toLowerCase())) {
      dependency = args.slice(1).some((a) => /^(dev|peer|optional)?dependencies[.[]/i.test(a));
    } else if (verb === 'config' && ['set', 'add'].includes((args[0] || '').toLowerCase())) {
      const kv = args.slice(1).join('=').toLowerCase();
      if (/^(legacy-peer-deps|force)(=|$)/.test(kv) && !/=(false|0)$/.test(kv)) result.forceFlag = true;
    }
  } else if (exe === 'pnpm') {
    if (verb === 'add') { installLike = true; dependency = hasArgs; }
    else if (['install', 'i'].includes(verb)) { installLike = true; dependency = hasArgs; }
    else if (['remove', 'rm', 'uninstall', 'un'].includes(verb)) { installLike = true; dependency = hasArgs; }
    else if (['update', 'up', 'upgrade'].includes(verb)) { installLike = true; dependency = true; }
    else if (verb === 'audit' && flags.includes('--fix')) { installLike = true; dependency = true; }
  } else {
    if (verb === '' && !hasArgs) installLike = true; // bare "yarn" installs from the lockfile
    else if (verb === 'add') { installLike = true; dependency = hasArgs; }
    else if (verb === 'install') { installLike = true; dependency = hasArgs; }
    else if (verb === 'remove') { installLike = true; dependency = hasArgs; }
    else if (['upgrade', 'up', 'upgrade-interactive'].includes(verb)) { installLike = true; dependency = true; }
  }
  if (dependency) result.dependency = true;
  if (force && installLike) result.forceFlag = true;
  if (['exec', 'dlx', 'x'].includes(verb) && args.length) collectWords(args, 1, result);
}

function classifyDotnet(words, result) {
  let k = 1;
  while (k < words.length && words[k].startsWith('-')) k++;
  const verb = (words[k] || '').toLowerCase();
  const next = (words[k + 1] || '').toLowerCase();
  if (verb === 'add' || verb === 'remove') {
    let positional = 0;
    for (let j = k + 1; j < words.length && positional < 3; j++) {
      const w = words[j].toLowerCase();
      if (w.startsWith('-')) continue;
      if (w === 'package') { result.dependency = true; return; }
      if (w === 'reference') { result.reference = true; return; }
      positional++;
    }
  } else if (verb === 'package' && ['add', 'remove', 'update'].includes(next)) {
    result.dependency = true;
  } else if (verb === 'reference' && ['add', 'remove'].includes(next)) {
    result.reference = true;
  } else if (verb === 'tool' && ['install', 'update', 'uninstall'].includes(next)
      && !words.slice(k + 2).some((w) => ['-g', '--global', '--tool-path'].includes(w.toLowerCase()))) {
    result.dependency = true;
  }
}

function classifyModuleCommand(exe, words, moduleCommands, result) {
  for (const def of moduleCommands) {
    if (exeName(def.executable || '') !== exe) continue;
    const sub = (words[1] || '').toLowerCase();
    if (!(def.subcommands || []).includes(sub)) continue;
    const args = words.slice(2).filter((w) => !w.startsWith('-'));
    if (!def.requiresArgument || args.length > 0) result.dependency = true;
  }
}

function collectWords(words, depth, result) {
  const rest = normalize(words, depth, result);
  if (!rest) return;
  const exe = exeName(rest[0]);
  if (exe === 'dotnet') classifyDotnet(rest, result);
  else if (exe === 'npm' || exe === 'pnpm' || exe === 'yarn') classifyNodeManager(exe, rest, result);
  else if (exe === 'npx' || exe === 'pnpx') collectWords(rest.slice(1).filter((w, k) => k > 0 || !w.startsWith('-')), depth + 1, result);
  else if (['install-package', 'update-package', 'uninstall-package'].includes(exe)) result.dependency = true;
  else classifyModuleCommand(exe, rest, result.moduleCommands, result);
}

function collect(command, depth, result) {
  for (const words of segments(command)) collectWords(words, depth, result);
}

// moduleCommands: framework CLI dependency commands declared by the selected modules' enforcement data.
export function classify(command, moduleCommands = []) {
  const result = { dependency: false, reference: false, forceFlag: false, moduleCommands };
  collect(command, 0, result);
  return { dependency: result.dependency, reference: result.reference, forceFlag: result.forceFlag };
}

// ---- hook entry point --------------------------------------------------------------------------

function decide(decision, reason) {
  process.stdout.write(JSON.stringify({
    hookSpecificOutput: { hookEventName: 'PreToolUse', permissionDecision: decision, permissionDecisionReason: reason },
  }));
  process.exit(0);
}

function moduleCommandsFor(configRoot) {
  const selection = parseSelection(configRoot);
  const frontend = loadJsonFacet(configRoot, selection, 'frontend', 'enforcement');
  return (frontend && frontend.dependencyCommands) || [];
}

async function main() {
  const input = await readHookInput();
  if (!input.ok) decide('deny', `Command not checked: ${input.error}. The dependency guard fails closed; retry the command.`);
  const command = input.value.tool_input && input.value.tool_input.command;
  if (typeof command !== 'string' || !command.trim()) decide('deny', 'Command not checked: hook input has no tool_input.command. The dependency guard fails closed.');

  const ctx = resolveContext(typeof input.value.cwd === 'string' ? input.value.cwd : process.cwd());
  const configRoot = requireConfigRoot(ctx);
  const { dependency, reference, forceFlag } = classify(command, moduleCommandsFor(configRoot));
  if (!dependency && !reference && !forceFlag) process.exit(0);

  const force = 'Peer-dependency bypass flag (--force, -f, --legacy-peer-deps): add-dependency requires resolving the actual compatibility problem; confirm only if the user explicitly wants this.';
  if (!dependency && !reference) decide('ask', force);

  const file = stateFile(ctx, 'dependency-commands');
  const now = Date.now();
  const state = readState(file) || {};
  for (const [key, ts] of Object.entries(state)) if (typeof ts !== 'number' || now - ts > GRACE_MS) delete state[key];
  const key = command.trim().replace(/\s+/g, ' ');
  if (state[key]) {
    delete state[key];
    try { writeState(file, state); } catch { /* the retry is still allowed */ }
    if (forceFlag) decide('ask', force);
    process.exit(0);
  }
  state[key] = now;
  try { writeState(file, state); } catch (error) {
    decide('ask', `Dependency or project-reference command detected, but hook state cannot be recorded (${error.message}). Run the routed workflow before confirming.`);
  }
  const reasons = [];
  if (dependency) reasons.push('Dependency change detected: run the add-dependency workflow first (need, approved technology, latest stable compatible version, deprecation, vulnerability, and license checks).');
  if (reference) reasons.push('Project-reference change detected: the project reference graph is Reserved beyond the frame layout (CLAUDE.md § Decision control); confirm it matches architecture.layout via the project-structure workflow or record approval with architecture-decision.');
  if (forceFlag) reasons.push(force);
  decide('deny', `${reasons.join(' ')} Then re-run the identical command within 30 minutes.`);
}

if (import.meta.url === pathToFileURL(process.argv[1] || '').href) {
  main().catch((error) => {
    try {
      decide('deny', `Command not checked: dependency guard failure (${error.message}). The guard fails closed; fix the instruction template or retry.`);
    } catch {
      process.stderr.write(`Dependency guard failure: ${error.message}\n`);
      process.exit(2);
    }
  });
}
