// Level: 3 Project | PreToolUse hook (Bash|PowerShell): routes package and project-reference commands
// to their workflows before they run. Owners: add-dependency, project-structure, architecture-decision.
'use strict';

const { projectRoot, readInput, feedback, splitCommands, classifyDependencyCommand } = require('./lib.cjs');

projectRoot();
const input = readInput();
const command = (input.tool_input && input.tool_input.command) || '';
const checked = /#\s*add-dependency:checked\b/i.test(command);

const hits = splitCommands(command).map(classifyDependencyCommand).filter(Boolean);

const force = hits.find(h => h.kind === 'force');
if (force && !checked) {
  feedback(`Blocked: "${force.segment}" uses --force or --legacy-peer-deps.\n` +
    'Resolve the peer-dependency conflict instead (add-dependency skill, step 5: .claude/skills/add-dependency/SKILL.md).');
}

const pkg = hits.find(h => h.kind === 'package');
if (pkg && !checked) {
  feedback(`Blocked: "${pkg.segment}" adds or updates a package.\n` +
    'Run the add-dependency workflow first (.claude/skills/add-dependency/SKILL.md). After its checks pass, ' +
    're-run the command with the marker comment "# add-dependency:checked" appended.');
}

const reference = hits.find(h => h.kind === 'reference');
if (reference && !/#\s*project-structure:approved\b/i.test(command)) {
  feedback(`Blocked: "${reference.segment}" changes the project reference graph.\n` +
    'Changing project references is Reserved (CLAUDE.md, Decision Control) and must follow ' +
    '1-architecture/backend-layers.md. Use project-structure (and architecture-decision when approval is missing); ' +
    'once approved, re-run with the marker comment "# project-structure:approved".');
}

process.exit(0);
