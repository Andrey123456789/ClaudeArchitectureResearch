// Kind: ENF | Scope: common | Capability: — | Loading: PostToolUse hook for Edit, MultiEdit, Write, Bash and PowerShell (.claude/settings.json) | Runs manifest and architecture checks after manifest changes; reminds about product-input synchronization
import { EnforcementError, projectRoot, readStdinJson, loadEnforcement, toRootRelative, formatFindings } from '../scripts/lib/common.mjs';
import { checkManifests } from '../scripts/check-manifests.mjs';
import { checkArchitecture } from '../scripts/check-architecture.mjs';
import { classifyCommand } from './lib/dependency-commands.mjs';

const MANIFEST = /(^|\/)([^/]+\.csproj|Directory\.Packages\.props|Directory\.Build\.props|[^/]+\.slnx|package\.json)$/i;
const PRODUCT_INPUTS = new Set(['specification.md', 'custom_settings.md']);

function emit(output) {
  process.stdout.write(`${JSON.stringify(output)}\n`);
}

function runChecks(root, policy) {
  const manifests = checkManifests(root);
  const architecture = checkArchitecture(root);
  const violations = [...manifests.violations, ...architecture.violations];
  if (violations.length > 0) {
    emit({
      decision: 'block',
      reason: `${formatFindings('Manifest or architecture violations after this change:', violations)}\n${policy.messages.manifestOwner}`,
    });
  } else if (manifests.warnings.length > 0) {
    emit({
      hookSpecificOutput: {
        hookEventName: 'PostToolUse',
        additionalContext: formatFindings('Manifest warnings (report the reason or route through add-dependency):', manifests.warnings),
      },
    });
  }
}

async function main() {
  const input = await readStdinJson();
  const root = projectRoot();
  const enforcement = loadEnforcement(root);
  const toolName = input.tool_name ?? '';

  if (toolName === 'Bash' || toolName === 'PowerShell') {
    const command = input?.tool_input?.command ?? '';
    if (classifyCommand(command, enforcement).manifestChange) {
      runChecks(root, enforcement.policy);
    }
    return 0;
  }

  const relative = toRootRelative(root, input?.tool_input?.file_path);
  if (!relative || relative.split('/').includes('node_modules')) {
    return 0;
  }
  if (PRODUCT_INPUTS.has(relative.toLowerCase())) {
    emit({ hookSpecificOutput: { hookEventName: 'PostToolUse', additionalContext: enforcement.policy.messages.productInputs } });
    return 0;
  }
  if (MANIFEST.test(relative)) {
    runChecks(root, enforcement.policy);
  }
  return 0;
}

main().then(
  (code) => process.exit(code),
  (error) => {
    const detail = error instanceof EnforcementError ? error.message : error.stack;
    process.stderr.write(`Post-edit enforcement hook failed (manifest and architecture checks did not run): ${detail}\n`);
    process.exit(1);
  },
);
