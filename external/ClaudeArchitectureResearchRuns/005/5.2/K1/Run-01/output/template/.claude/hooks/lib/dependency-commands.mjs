// Kind: ENF | Scope: common | Capability: — | Loading: imported by the PreToolUse and PostToolUse hooks | Detects dependency and project-reference commands in Bash/PowerShell input
function compile(patterns = []) {
  return patterns.map((p) => new RegExp(p, 'i'));
}

// Splits a command line into segments separated by shell operators so each npm invocation is inspected alone.
function segments(command) {
  return command.split(/&&|\|\||;|\||\r?\n/).map((s) => s.trim()).filter(Boolean);
}

function npmChange(segment, policy) {
  const tokens = segment.split(/\s+/);
  const npmIndex = tokens.findIndex((t) => /^npm(\.cmd)?$/i.test(t));
  if (npmIndex === -1) {
    return { install: false, force: false };
  }
  const subcommand = tokens[npmIndex + 1]?.toLowerCase();
  const args = tokens.slice(npmIndex + 2);
  const force = args.some((a) => policy.npmForceFlags.includes(a.toLowerCase()));
  const install = policy.npmInstallCommands.includes(subcommand)
    && args.some((a) => !a.startsWith('-'));
  return { install, force };
}

export function classifyCommand(command, enforcement) {
  const { policy, facets } = enforcement;
  const dependencyPatterns = compile([
    ...policy.dependencyCommandPatterns,
    ...facets.flatMap((f) => f.dependencyCommandPatterns ?? []),
  ]);
  const referencePatterns = compile(policy.referenceCommandPatterns);

  let dependency = dependencyPatterns.some((r) => r.test(command));
  let force = false;
  for (const segment of segments(command)) {
    const npm = npmChange(segment, policy);
    dependency ||= npm.install;
    force ||= npm.force;
  }
  const manifestChange = dependency || referencePatterns.some((r) => r.test(command));
  return { dependency, force, manifestChange };
}
