// Kind: ENF | Scope: repo/meta | Capability: — | Loading: hook entry point (.claude/settings.json); events: pre-bash, post-edit, stop
'use strict';

// Exit codes follow the Claude Code hook contract: 0 = continue, 2 = feedback to Claude
// (PreToolUse: blocks the tool call; PostToolUse: tool already ran; Stop: continue working),
// any other non-zero code = visible hook error. The project root is derived from this file's
// location, so no shell variable expansion is needed in the hook command.

const path = require('path');
const lib = require('../scripts/lib.cjs');

const ROOT = lib.rootFrom(__dirname, 2);

function readStdin() {
  return new Promise((resolve, reject) => {
    let data = '';
    process.stdin.setEncoding('utf8');
    process.stdin.on('data', chunk => { data += chunk; });
    process.stdin.on('end', () => resolve(data));
    process.stdin.on('error', reject);
  });
}

// ---------- pre-bash: dependency commands ----------

const SEGMENT_SPLIT = /&&|\|\||[;|\n]/;
const FLOATING_TAGS = new Set(['', '*', 'x', 'latest', 'next']);

function tokens(segment) {
  return (segment.match(/"[^"]*"|'[^']*'|\S+/g) || []).map(t => t.replace(/^["']|["']$/g, ''));
}

function npmSpecHasVersion(spec) {
  if (/^(\.|\/|file:|git\+|git:|https?:|github:)/.test(spec)) return true; // local or URL source
  const at = spec.lastIndexOf('@');
  if (at <= 0) return false; // no version (a leading @ is the scope)
  return !FLOATING_TAGS.has(spec.slice(at + 1).toLowerCase());
}

function analyzeCommand(command) {
  const problems = [];
  for (const raw of String(command || '').split(SEGMENT_SPLIT)) {
    const segment = raw.trim();
    const t = tokens(segment);
    const exe = (t[0] || '').toLowerCase().replace(/\.(exe|cmd)$/, '');
    if (exe === 'dotnet') {
      const isAdd = (t[1] === 'add' && t.includes('package')) || (t[1] === 'package' && t[2] === 'add');
      if (isAdd && !t.some(x => x === '--version' || x === '-v' || x.startsWith('--version='))) {
        problems.push(`\`${segment}\` adds a NuGet package without an explicit version`);
      }
    } else if (exe === 'npm' || exe === 'pnpm' || exe === 'yarn') {
      if (t.some(x => x === '--force' || x === '-f' || x === '--legacy-peer-deps')) {
        problems.push(`\`${segment}\` uses --force/--legacy-peer-deps (peer-dependency conflicts: add-dependency)`);
        continue;
      }
      const sub = (t[1] || '').toLowerCase();
      if (['install', 'i', 'add', 'update', 'up', 'upgrade'].includes(sub)) {
        const specs = t.slice(2).filter(x => !x.startsWith('-'));
        const unversioned = specs.filter(s => !npmSpecHasVersion(s));
        if (unversioned.length) {
          problems.push(`\`${segment}\` installs ${unversioned.join(', ')} without an explicit version`);
        }
      }
    }
  }
  return problems;
}

function preBash(input) {
  const problems = analyzeCommand(input.tool_input && input.tool_input.command);
  if (!problems.length) return 0;
  process.stderr.write(
    `Dependency command blocked:\n- ${problems.join('\n- ')}\n` +
    'Run the add-dependency workflow first, then re-run the command with the exact version it selected.\n');
  return 2;
}

// ---------- post-edit: manifests, product inputs, instruction files ----------

const INSTRUCTION_FILE = /^(CLAUDE\.md|docs\/architecture\/decision-register\.md|\.claude\/(MAP\.md|settings\.json|rules\/|skills\/|agents\/|capabilities\/|hooks\/|scripts\/))/;

function postEdit(input) {
  const ti = input.tool_input || {};
  const filePath = ti.file_path || ti.notebook_path;
  if (!filePath) return 0;
  const rel = lib.relInside(ROOT, filePath);
  if (!rel) return 0;
  const messages = [];

  const manifests = require('../scripts/check-manifests.cjs');
  if (manifests.isManifest(rel)) {
    const findings = manifests.checkFile(ROOT, rel);
    if (findings.length) messages.push(`Manifest check:\n${lib.formatFindings(findings)}`);
  }
  if (rel === 'CUSTOM_SETTINGS.md') {
    messages.push('CUSTOM_SETTINGS.md changed: run the custom-settings workflow to synchronize affected surfaces.');
  }
  if (rel === 'SPECIFICATION.md') {
    messages.push('SPECIFICATION.md changed: check consistency with CUSTOM_SETTINGS.md (CLAUDE.md, Product sources) and synchronize affected code, tests, and docs (development-workflow).');
  }
  if (INSTRUCTION_FILE.test(rel)) {
    const structure = require('../scripts/check-instructions.cjs');
    const errors = structure.check(ROOT).filter(f => f.severity === 'error');
    if (errors.length) messages.push(`Instruction-structure check:\n${lib.formatFindings(errors)}\n(template-maintenance workflow)`);
  }
  if (!messages.length) return 0;
  process.stderr.write(`${messages.join('\n\n')}\n`);
  return 2;
}

// ---------- stop: co-change reminders ----------

function stop(input) {
  if (input.stop_hook_active) return 0; // never re-block a continuation triggered by this hook
  const cochange = require('../scripts/check-cochange.cjs');
  const result = cochange.run(ROOT, 'hook');
  if (!result.applicable) {
    process.stdout.write(`${JSON.stringify({ systemMessage: 'Co-change reminders inactive: the project is not a Git work tree.' })}\n`);
    return 0;
  }
  if (!result.reminders.length) return 0;
  process.stderr.write(
    `Co-change reminders (reported once for this set of changes):\n${cochange.format(result.reminders)}\n` +
    'Address each item or state why it does not apply, then finish.\n');
  return 2;
}

const HANDLERS = { 'pre-bash': preBash, 'post-edit': postEdit, stop };

async function run(event) {
  const handler = HANDLERS[event];
  if (!handler) throw new Error(`Unknown hook event "${event}"`);
  const raw = await readStdin();
  let input;
  try {
    input = raw.trim() ? JSON.parse(raw) : {};
  } catch (err) {
    throw new Error(`Hook input is not valid JSON (${err.message})`);
  }
  return handler(input);
}

function main(event) {
  run(event).then(
    code => { process.exitCode = code; },
    err => {
      process.stderr.write(`[hook ${event}] failed: ${err && err.stack ? err.stack : err}\n`);
      process.exitCode = 1;
    });
}

module.exports = { main, analyzeCommand };
