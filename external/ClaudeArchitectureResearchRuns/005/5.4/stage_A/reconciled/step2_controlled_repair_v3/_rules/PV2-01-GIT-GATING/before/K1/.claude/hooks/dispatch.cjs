// Kind: ENF | Scope: repo/meta | Capability: — | Loading: hook entry point (.claude/settings.json, exec form): node <launcher>/.claude/hooks/dispatch.cjs <HookEvent>
// Conforms: docs/architecture/decision-register.md
'use strict';

// Two roots, never mixed:
// - launcher root: where this file lives (located through ${CLAUDE_PROJECT_DIR}); it only locates the implementation;
// - active root: the repository/worktree that contains the hook input `cwd`; every inspection, relative path,
//   and state file uses it, so a linked worktree or nested directory is checked where Claude is working.
// Exit codes follow the Claude Code hook contract: 0 = continue, 2 = feedback to Claude (PreToolUse: blocks the
// tool call). PreToolUse guards policy-critical commands and fails closed: any internal error, unreadable or
// mismatched input exits 2 (settings.json additionally sets onFailure "block" for host-level failures).
// Post and Stop events are advisory: internal errors exit 1 (visible, non-blocking).

const path = require('path');
const lib = require('../scripts/lib.cjs');

const REGISTER = 'docs/architecture/decision-register.md';
const SHELL_TOOLS = new Set(['Bash', 'PowerShell']);
const EDIT_TOOLS = new Set(['Edit', 'Write', 'MultiEdit']);

function readStdin() {
  return new Promise((resolve, reject) => {
    const chunks = [];
    process.stdin.on('data', chunk => chunks.push(chunk));
    process.stdin.on('end', () => resolve(Buffer.concat(chunks)));
    process.stdin.on('error', reject);
  });
}

/** Parse hook input: UTF-8 with or without BOM, BOM-tagged UTF-16, CRLF. Throws on empty or malformed input. */
function parseInput(buffer) {
  const text = lib.decodeText(buffer, 'hook input').replace(/^﻿/, '').trim();
  if (!text) throw new Error('hook input is empty');
  let input;
  try {
    input = JSON.parse(text);
  } catch (err) {
    throw new Error(`hook input is not valid JSON (${err.message})`);
  }
  if (!input || typeof input !== 'object' || Array.isArray(input)) throw new Error('hook input is not a JSON object');
  return input;
}

const workingDirectory = input => (typeof input.cwd === 'string' && input.cwd ? input.cwd : process.cwd());

// ---------- PreToolUse: dependency and project-reference commands (before execution) ----------

function describe(f) {
  switch (f.kind) {
    case 'dependency-version':
      return `\`${f.segment}\`: ${f.specs.join(', ')} without an exact version -> add-dependency workflow (version selection)`;
    case 'dependency-update':
      return `\`${f.segment}\`: updates dependencies without exact versions -> add-dependency workflow`;
    case 'dependency-removal':
      return `\`${f.segment}\`: removes ${f.specs.length ? f.specs.join(', ') : 'a dependency'} -> add-dependency workflow (removal)`;
    case 'peer-bypass':
      return `\`${f.segment}\`: --force/--legacy-peer-deps bypasses peer-dependency resolution -> add-dependency workflow (peer-dependency conflicts). No confirmation, comment marker, or approval opens this route.`;
    case 'reference-change':
      return `\`${f.segment}\`: changes the project reference graph (${f.edges.map(e => `${e.from} -> ${e.to}`).join(', ') || 'unnamed project'}), a Reserved decision without a recorded approval -> architecture-decision workflow (approval recorded as \`From -> To\` in ${REGISTER}, Accepted decisions)`;
    default:
      return `\`${f.segment}\`: command could not be classified (wrapper nesting too deep); run the command directly`;
  }
}

function preToolUse(input) {
  if (!SHELL_TOOLS.has(input.tool_name)) return 0;
  const command = input.tool_input && input.tool_input.command;
  if (typeof command !== 'string') throw new Error('tool_input.command is missing');
  const cwd = workingDirectory(input);
  let findings = require('../scripts/classify-command.cjs').classify(command, { cwd });
  if (findings.some(f => f.kind === 'reference-change')) {
    const manifests = require('../scripts/check-manifests.cjs');
    const approvals = manifests.acceptedDecisionText(lib.activeRoot(cwd));
    findings = findings.filter(f => f.kind !== 'reference-change' || !f.edges.length || f.edges.some(e => !manifests.isApprovedEdge(approvals, e.from, e.to)));
  }
  if (!findings.length) return 0;
  process.stderr.write(`Blocked before execution (dependency and project-reference guard):\n- ${findings.map(describe).join('\n- ')}\n`);
  return 2;
}

// ---------- PostToolUse / PostToolUseFailure: actual state of the active root ----------

function report(result, preface) {
  const messages = [];
  if (result.findings.length) messages.push(`Manifest and project-reference check:\n${lib.formatFindings(result.findings)}`);
  if (result.instructionErrors.length) messages.push(`Instruction-structure check:\n${lib.formatFindings(result.instructionErrors)}\n(template-maintenance workflow)`);
  messages.push(...result.reminders);
  if (!messages.length) return 0;
  process.stderr.write(`${preface ? `${preface}\n` : ''}${messages.join('\n\n')}\n`);
  return 2;
}

function postToolUse(input) {
  const cwd = workingDirectory(input);
  const root = lib.activeRoot(cwd);
  const observe = require('../scripts/actual-state.cjs').observe;
  if (SHELL_TOOLS.has(input.tool_name)) return report(observe(root), '');
  if (!EDIT_TOOLS.has(input.tool_name)) return 0;
  const ti = input.tool_input || {};
  const filePath = ti.file_path || ti.notebook_path;
  if (!filePath) return 0;
  const rel = lib.relInside(root, path.resolve(cwd, filePath));
  if (!rel) return 0;
  return report(observe(root, { only: rel }), '');
}

function postToolUseFailure(input) {
  if (!SHELL_TOOLS.has(input.tool_name)) return 0;
  const root = lib.activeRoot(workingDirectory(input));
  return report(require('../scripts/actual-state.cjs').observe(root), 'The failed command still changed relevant files:');
}

// ---------- Stop: co-change reminders ----------

function stop(input) {
  if (input.stop_hook_active) return 0; // never re-block a continuation triggered by this hook
  const cochange = require('../scripts/check-cochange.cjs');
  const result = cochange.run(lib.activeRoot(workingDirectory(input)), 'hook');
  if (!result.applicable) {
    process.stdout.write(`${JSON.stringify({ systemMessage: 'Co-change reminders inactive: the project is not a Git work tree.' })}\n`);
    return 0;
  }
  if (!result.reminders.length) return 0;
  process.stderr.write(
    `Co-change reminders (reported once per content state):\n${cochange.format(result.reminders)}\n` +
    'Address each item or state why it does not apply, then finish.\n');
  return 2;
}

const EVENTS = { PreToolUse: preToolUse, PostToolUse: postToolUse, PostToolUseFailure: postToolUseFailure, Stop: stop };
const CRITICAL = new Set(['PreToolUse']);

async function run(event) {
  const handler = EVENTS[event];
  if (!handler) throw new Error(`unknown hook event "${event}"`);
  const input = parseInput(await readStdin());
  if (input.hook_event_name && input.hook_event_name !== event) {
    throw new Error(`hook input is for "${input.hook_event_name}" but this handler was configured for "${event}"`);
  }
  return handler(input);
}

function main(event) {
  run(event).then(
    code => {
      process.exitCode = code;
    },
    err => {
      const critical = CRITICAL.has(event);
      process.stderr.write(`[hook ${event}] ${critical ? 'blocked (fail closed)' : 'failed'}: ${err && err.message ? err.message : err}\n`);
      process.exitCode = critical ? 2 : 1;
    });
}

module.exports = { main, EVENTS, parseInput };

if (require.main === module) main(process.argv[2]);
