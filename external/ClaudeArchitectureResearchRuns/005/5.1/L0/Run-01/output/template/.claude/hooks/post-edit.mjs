// Level: 3 Project · Owns: PostToolUse checks after file edits (product inputs, manifests, instruction structure) · Enforcement asset
import path from 'node:path';
import { readHookInput, projectDir, toRepoPath, feedback } from './lib.mjs';
import { checkManifestFile } from '../scripts/check-manifests.mjs';
import { checkInstructions } from '../scripts/check-instructions.mjs';

const input = readHookInput();
const root = projectDir(input);
const filePath = input?.tool_input?.file_path ?? input?.tool_input?.notebook_path ?? '';
if (!filePath) process.exit(0);

const relativePath = toRepoPath(root, filePath);
if (relativePath.startsWith('..')) process.exit(0);
const base = path.posix.basename(relativePath);
const messages = [];

if (relativePath === 'SPECIFICATION.md') {
  messages.push('SPECIFICATION.md changed: check consistency with CUSTOM_SETTINGS.md and approval status (.claude/rules/0-core/product-governance.md).');
}
if (relativePath === 'CUSTOM_SETTINGS.md') {
  messages.push('CUSTOM_SETTINGS.md changed: run the custom-settings workflow (obligation: .claude/rules/0-core/product-governance.md).');
}

if (base.endsWith('.csproj') || base === 'Directory.Packages.props' || base === 'package.json') {
  const findings = checkManifestFile(root, relativePath);
  if (findings.length) {
    messages.push(`Manifest check for ${relativePath} (procedure: add-dependency workflow):`, ...findings.map((finding) => `- ${finding}`));
  }
}

const isInstructionFile = relativePath === 'CLAUDE.md' || relativePath === '.claude/INSTRUCTION-MAP.md' ||
  /^\.claude\/(rules|skills|agents)\//.test(relativePath);
if (isInstructionFile) {
  const { failures } = checkInstructions(root);
  if (failures.length) {
    messages.push(
      'Instruction-structure check failed (instruction changes follow the user-invoked template-maintenance workflow):',
      ...failures.slice(0, 15).map((failure) => `- ${failure}`),
    );
  }
}

feedback(messages);
