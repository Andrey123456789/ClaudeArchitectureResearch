// Level: 3 Project | PostToolUse hook (Edit|Write|MultiEdit|Bash|PowerShell).
// - SPECIFICATION.md / CUSTOM_SETTINGS.md edits -> synchronization reminder (CLAUDE.md, custom-settings).
// - Package/project manifest edits or package/reference commands -> check-manifests.cjs.
// - Instruction-system edits (CLAUDE.md, .claude/**) -> check-instructions.cjs.
// Messages point to owners; they do not restate policy.
'use strict';

const path = require('path');
const { projectRoot, readInput, relativeToRoot, feedback, fail, splitCommands, classifyDependencyCommand } = require('./lib.cjs');

const root = projectRoot();
const input = readInput();
const tool = input.tool_name || '';
const toolInput = input.tool_input || {};

function runManifestChecks(trigger) {
  let findings;
  try {
    const { checkManifests, format } = require(path.join(root, '.claude', 'scripts', 'check-manifests.cjs'));
    findings = checkManifests(root);
    if (findings.some(f => f.severity === 'error')) {
      feedback(`Manifest check failed after ${trigger}:\n${format(findings)}`);
    }
  } catch (error) {
    fail(`post-edit: manifest check could not run (${error.message}).`);
  }
}

function runInstructionChecks(file) {
  try {
    const { checkInstructions } = require(path.join(root, '.claude', 'scripts', 'check-instructions.cjs'));
    const result = checkInstructions(root);
    if (result.errors.length) {
      feedback(`Instruction-structure check failed after editing ${file}:\n` +
        result.errors.map(e => `ERROR ${e}`).join('\n') +
        '\nFix the structure (template-maintenance skill) or run: node .claude/scripts/check-instructions.cjs');
    }
  } catch (error) {
    fail(`post-edit: instruction check could not run (${error.message}).`);
  }
}

if (tool === 'Bash' || tool === 'PowerShell') {
  const hit = splitCommands(toolInput.command).map(classifyDependencyCommand).find(Boolean);
  if (hit) runManifestChecks(`"${hit.segment}"`);
  process.exit(0);
}

const file = relativeToRoot(root, toolInput.file_path || toolInput.notebook_path || '');
if (!file || file.startsWith('..')) process.exit(0);
const base = path.posix.basename(file);

if (file === 'SPECIFICATION.md') {
  feedback('SPECIFICATION.md changed. Check it against CUSTOM_SETTINGS.md and stop on a conflict ' +
    '(CLAUDE.md, Product Governance); keep the implementation synchronized through develop.');
}
if (file === 'CUSTOM_SETTINGS.md') {
  feedback('CUSTOM_SETTINGS.md changed. Run the custom-settings workflow (.claude/skills/custom-settings/SKILL.md) ' +
    'to synchronize every affected surface.');
}
if (/\.csproj$/.test(base) || ['Directory.Packages.props', 'Directory.Build.props', 'package.json'].includes(base)) {
  runManifestChecks(`editing ${file}`);
}
if (file === 'CLAUDE.md' || (file.startsWith('.claude/') && /\.(md|json|cjs)$/.test(file) && !file.startsWith('.claude/hooks/.state/'))) {
  runInstructionChecks(file);
}
process.exit(0);
