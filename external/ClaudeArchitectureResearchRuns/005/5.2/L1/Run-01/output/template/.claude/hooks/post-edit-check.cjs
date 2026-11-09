// Level: 3-project | Owns: PostToolUse check after edits and package/project commands —
// manifest conventions (check-packages), project references (check-architecture), and a
// synchronization reminder when product inputs change. Feedback uses Claude Code JSON
// output on stdout with exit code 0 (shell-independent); exit 1 + stderr = check error.
'use strict';

const path = require('path');
const lib = require('../scripts/lib/project.cjs');
const { checkPackages } = require('../scripts/check-packages.cjs');
const { checkArchitecture } = require('../scripts/check-architecture.cjs');

const MANIFEST = /(\.csproj|Directory\.Packages\.props|Directory\.Build\.props|package\.json)$/i;
const MANIFEST_COMMAND = /\b(dotnet(\.exe)?\s+(add|remove|new|sln|package)|npm(\.cmd)?\s+(install|i|add|uninstall|un|remove|rm|update|up))\b/i;

function productInputMessage(rel) {
  if (rel === 'CUSTOM_SETTINGS.md') {
    return 'CUSTOM_SETTINGS.md changed: run `custom-settings` to synchronize every affected surface, and confirm it stays consistent with SPECIFICATION.md (product governance).';
  }
  if (rel === 'SPECIFICATION.md') {
    return 'SPECIFICATION.md changed: confirm it stays consistent with CUSTOM_SETTINGS.md (product governance) and that implementation, tests, and documentation follow the approved behavior (`develop`).';
  }
  return null;
}

function main() {
  try {
    const input = lib.readStdinJson();
    const tool = input.tool_name || '';
    const toolInput = input.tool_input || {};
    const root = lib.resolveRoot(__dirname);
    const messages = [];
    let runChecks = false;

    if (['Edit', 'MultiEdit', 'Write'].includes(tool) && typeof toolInput.file_path === 'string') {
      const abs = path.resolve(root, toolInput.file_path);
      const rel = lib.toPosix(path.relative(root, abs));
      if (rel.startsWith('..') || path.isAbsolute(rel)) process.exit(0);
      const reminder = productInputMessage(rel);
      if (reminder) messages.push(reminder);
      if (MANIFEST.test(rel)) runChecks = true;
    } else if (tool === 'Bash' && typeof toolInput.command === 'string') {
      const moduleCommands = lib.moduleDependencyPatterns(root);
      if (MANIFEST_COMMAND.test(toolInput.command)
        || moduleCommands.some(({ regex }) => regex.test(toolInput.command))) runChecks = true;
    }

    if (runChecks) {
      const packages = checkPackages(root);
      const architecture = checkArchitecture(root);
      const violations = [...packages.violations, ...architecture.violations];
      if (violations.length) {
        messages.push(`Manifest/architecture check found ${violations.length} violation(s):\n  - ${violations.join('\n  - ')}`);
      }
      if (packages.warnings.length) {
        messages.push(`Warnings:\n  - ${packages.warnings.join('\n  - ')}`);
      }
    }

    if (messages.length) {
      const text = `[post-edit-check]\n${messages.join('\n')}`;
      const blocking = messages.some((m) => !m.startsWith('Warnings:'));
      process.stdout.write(JSON.stringify(blocking
        ? { decision: 'block', reason: text }
        : { hookSpecificOutput: { hookEventName: 'PostToolUse', additionalContext: text } }));
    }
    process.exit(0);
  } catch (error) {
    process.stderr.write(`[post-edit-check] could not run: ${error.message}\n`);
    process.exit(1);
  }
}

main();
