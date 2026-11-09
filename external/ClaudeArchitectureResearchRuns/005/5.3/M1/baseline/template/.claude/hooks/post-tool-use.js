'use strict';
// PostToolUse hook entry point (Write, Edit, MultiEdit, Bash, PowerShell).
// After a change it runs the deterministic checks that apply to the touched
// file: manifests (central package management, versions, deny-list, project
// references), inner-layer namespaces, product-source synchronization
// reminders, and the instruction-structure check. Findings are returned to
// Claude as hook JSON (see scripts/lib/hook-output.js); a hook failure is
// reported visibly.

const common = require('../scripts/lib/common.js');
const out = require('../scripts/lib/hook-output.js');
const { changesManifests } = require('../scripts/lib/dependency-commands.js');
const { checkManifests, isManifest } = require('../scripts/check-manifests.js');
const { checkArchitecture } = require('../scripts/check-architecture.js');
const instructions = require('../scripts/check-instructions.js');

const MAX_LINES = 25;

function changedText(toolInput) {
  if (!toolInput) return '';
  if (typeof toolInput.content === 'string') return toolInput.content;
  if (typeof toolInput.new_string === 'string') return toolInput.new_string;
  if (Array.isArray(toolInput.edits)) return toolInput.edits.map((e) => e.new_string || '').join('\n');
  return '';
}

function report(findings, title) {
  const relevant = findings.filter((f) => f.level === 'ERROR' || f.level === 'WARN');
  if (!relevant.length) return [];
  const lines = common.formatFindings(relevant).split('\n');
  const shown = lines.slice(0, MAX_LINES);
  if (lines.length > MAX_LINES) shown.push(`... ${lines.length - MAX_LINES} more`);
  return [`${title}:`, ...shown];
}

function fileChecks(rel, text) {
  const msgs = [];
  if (isManifest(rel)) {
    msgs.push(...report(checkManifests([rel]), `Manifest check for ${rel} (.claude/rules/dependencies.md)`));
    if (rel.endsWith('.csproj')) msgs.push(...report(checkArchitecture([]).findings, 'Architecture check (.claude/rules/architecture.md)'));
    if (/PackageReference|PackageVersion|"(?:dev)?[dD]ependencies"/.test(text) || rel.endsWith('package.json')) {
      msgs.push(`Dependency entries changed in ${rel}: confirm the add-dependency workflow was applied (.claude/skills/add-dependency/SKILL.md).`);
    }
  }
  if (rel.startsWith('backend/') && rel.endsWith('.cs')) {
    const errors = checkArchitecture([rel]).findings.filter((f) => f.level === 'ERROR' && f.file.startsWith(rel));
    msgs.push(...report(errors, 'Layer boundary check (.claude/rules/architecture.md)'));
  }
  if (rel === 'SPECIFICATION.md') {
    msgs.push('SPECIFICATION.md changed: keep it consistent with CUSTOM_SETTINGS.md (CLAUDE.md, Product Sources); record approved behavior through the architecture-decision workflow.');
  }
  if (rel === 'CUSTOM_SETTINGS.md') {
    msgs.push('CUSTOM_SETTINGS.md changed: run the custom-settings workflow (.claude/skills/custom-settings/SKILL.md) to synchronize every affected surface.');
  }
  if (instructions.isInstructionPath(rel)) {
    const { findings } = instructions.run();
    msgs.push(...report(findings.filter((f) => f.level === 'ERROR'), 'Instruction-structure check (template-maintenance workflow)'));
  }
  return msgs;
}

try {
  common.projectRoot();
  const input = common.readStdinJson();
  const tool = input.tool_name || '';
  const toolInput = input.tool_input || {};
  let messages = [];
  if (['Write', 'Edit', 'MultiEdit'].includes(tool)) {
    const rel = common.relativeInsideRoot(toolInput.file_path);
    if (rel) messages = fileChecks(rel, changedText(toolInput));
  } else if (['Bash', 'PowerShell'].includes(tool) && changesManifests(toolInput.command)) {
    messages = [
      ...report(checkManifests([]), 'Manifest check (.claude/rules/dependencies.md)'),
      ...report(checkArchitecture([]).findings, 'Architecture check (.claude/rules/architecture.md)'),
    ];
  }
  if (messages.length) out.block(messages.join('\n'));
  out.allow();
} catch (e) {
  out.fail('post-tool-use', e, 'post-change checks were not applied');
}
