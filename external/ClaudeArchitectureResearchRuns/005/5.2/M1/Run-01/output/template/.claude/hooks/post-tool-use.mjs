// PostToolUse hook (Edit|Write|MultiEdit and Bash|PowerShell).
// Routes dependency commands, manifest edits, product-source edits, and
// instruction-system edits to their owning workflow and runs the fast
// mechanical checks. Messages point to owners; they do not restate policy.
import path from 'node:path';
import { TemplateError, resolveRoot, relFromRoot, loadCapabilities } from '../scripts/lib/template.mjs';
import { runDependencyChecks } from '../scripts/check-dependencies.mjs';
import { runArchitectureChecks } from '../scripts/check-architecture.mjs';
import { runInstructionChecks } from '../scripts/check-instructions.mjs';

const BASE_DEPENDENCY_COMMANDS = [
  /\bdotnet\s+add\s+(?:\S+\s+)?package\b/i,
  /\bdotnet\s+remove\s+(?:\S+\s+)?package\b/i,
  /\bdotnet\s+package\s+(?:add|remove|update)\b/i,
  /\b(?:Install|Update|Uninstall)-Package\b/i,
  /\b(?:npm|pnpm|yarn)\s+(?:install|i|add|update|up|upgrade|uninstall|remove|rm|un)\s+(?!-)[^\s;&|]+/i,
];
const MANIFEST = /(^|\/)(?:[^/]+\.csproj|Directory\.Packages\.props|Directory\.Build\.props|package\.json)$/i;
const PRODUCT = /^(SPECIFICATION|CUSTOM_SETTINGS)\.md$/;
const INSTRUCTIONS = /^(CLAUDE\.md|docs\/[^/]+\.md|\.claude\/.+)$/;

async function readPayload() {
  let raw = '';
  for await (const chunk of process.stdin) raw += chunk;
  // Windows PowerShell 5.1 prefixes piped input with a UTF-8 byte-order mark.
  try { return JSON.parse(raw.replace(/^﻿/, '') || '{}'); } catch { throw new TemplateError('hook input is not valid JSON'); }
}

function dependencyCommandPatterns(root) {
  const patterns = [...BASE_DEPENDENCY_COMMANDS];
  const { modules } = loadCapabilities(root);
  for (const mod of Object.values(modules)) {
    for (const cmd of mod.manifest.properties?.dependencyCommands ?? []) {
      patterns.push(new RegExp('\\b' + cmd.trim().split(/\s+/).map(s => s.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')).join('\\s+') + '\\b', 'i'));
    }
  }
  return patterns;
}

function collect(result, label, violations) {
  for (const e of result.errors) violations.push(`${label}: ${e}`);
}

export async function handle(payload) {
  const root = resolveRoot(process.env.CLAUDE_PROJECT_DIR, payload.cwd);
  const tool = payload.tool_name ?? '';
  const input = payload.tool_input ?? {};
  const notes = [];
  const violations = [];
  let manifests = false;

  if (/^(Bash|PowerShell)$/.test(tool)) {
    const command = String(input.command ?? '');
    if (dependencyCommandPatterns(root).some(re => re.test(command))) {
      notes.push('Dependency command detected: the add-dependency workflow applies (version selection, deprecation, vulnerability and license checks, Central Package Management).');
      manifests = true;
    }
  } else if (/^(Edit|Write|MultiEdit)$/.test(tool) && input.file_path) {
    const rel = relFromRoot(root, path.resolve(payload.cwd ?? root, String(input.file_path)));
    if (rel) {
      if (MANIFEST.test(rel)) manifests = true;
      if (PRODUCT.test(rel)) notes.push(`${rel} changed: keep SPECIFICATION.md and CUSTOM_SETTINGS.md consistent (CLAUDE.md → Product Sources)${rel.startsWith('CUSTOM') ? ' and run the custom-settings workflow' : ''}.`);
      if (INSTRUCTIONS.test(rel) && !rel.startsWith('.claude/.cache/')) collect(runInstructionChecks(root), 'check-instructions', violations);
    }
  }
  if (manifests) {
    collect(runDependencyChecks(root), 'check-dependencies', violations);
    collect(runArchitectureChecks(root), 'check-architecture', violations);
  }

  if (violations.length) {
    return { decision: 'block', reason: [...notes, 'Fix these mechanical violations (owners are named in each message):', ...violations.map(v => `- ${v}`)].join('\n') };
  }
  if (notes.length) return { hookSpecificOutput: { hookEventName: 'PostToolUse', additionalContext: notes.join('\n') } };
  return null;
}

try {
  const output = await handle(await readPayload());
  if (output) process.stdout.write(JSON.stringify(output));
  process.exit(0);
} catch (e) {
  process.stderr.write(`post-tool-use hook failed: ${e instanceof TemplateError ? e.message : e.stack}\n`);
  process.exit(1);
}
