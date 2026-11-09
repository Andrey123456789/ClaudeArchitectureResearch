// Level: 3 Project · Owns: PreToolUse routing of dependency commands to the add-dependency workflow · Enforcement asset
// Policy owners: .claude/rules/0-core/dependency-hygiene.md, .claude/rules/2-technology/angular.md
import { readHookInput, feedback } from './lib.mjs';

const input = readHookInput();
const command = String(input?.tool_input?.command ?? '');
if (!command) process.exit(0);

const WORKFLOW_MARKER = /#\s*add-dependency\b/;

const FORCED_PEER_INSTALL = /\bnpm\b[^\n;&|]*\s--(force|legacy-peer-deps)\b/;

const DEPENDENCY_COMMANDS = [
  /\bdotnet\s+add\b[^\n;&|]*\bpackage\b/,
  /\bdotnet\s+remove\b[^\n;&|]*\bpackage\b/,
  /\bdotnet\s+package\s+(add|remove|update)\b/,
  /\bdotnet\s+tool\s+(install|update)\b/,
  /\bnpm\s+(i|install|add)\s+(-\S+\s+)*(?!-)[^\s;&|]/,
  /\bnpm\s+(uninstall|un|remove|rm|r|update|up|upgrade)\b/,
  /\bng\s+(add|update)\b/,
  /\b(yarn|pnpm)\s+(add|remove|up|upgrade|update)\b/,
];

if (FORCED_PEER_INSTALL.test(command)) {
  feedback([
    'Blocked: npm --force / --legacy-peer-deps.',
    'Owner: .claude/rules/2-technology/angular.md. Resolve the compatibility problem through the build-fix or add-dependency workflow.',
  ]);
}

if (DEPENDENCY_COMMANDS.some((pattern) => pattern.test(command)) && !WORKFLOW_MARKER.test(command)) {
  feedback([
    'Dependency change detected: package additions, updates and removals go through the add-dependency workflow',
    '(obligations: .claude/rules/0-core/dependency-hygiene.md).',
    'After completing that workflow\'s checks, rerun the command with the trailing comment "# add-dependency".',
  ]);
}

process.exit(0);
