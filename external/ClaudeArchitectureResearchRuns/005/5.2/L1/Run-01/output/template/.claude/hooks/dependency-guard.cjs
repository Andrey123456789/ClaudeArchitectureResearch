// Level: 3-project | Owns: PreToolUse(Bash) guard routing package changes to add-dependency.
// Denies dependency commands without an explicit version, floating/prerelease flags,
// update commands, and npm peer-dependency bypass flags. Reads framework-specific
// dependency commands from the selected modules' check.json files.
// Decisions use Claude Code JSON output on stdout with exit code 0, so they survive any
// shell wrapper; exit code 1 + stderr reports an evaluation error visibly.
'use strict';

const lib = require('../scripts/lib/project.cjs');

const ROUTE = 'Run the `add-dependency` workflow (approved stack, latest stable compatible version, deprecation, vulnerabilities, license), then re-run the command with the explicit verified version.';

function segments(command) {
  return command.split(/&&|\|\||;|\|/).map((s) => s.trim()).filter(Boolean);
}

function tokens(text) {
  return (text.match(/"[^"]*"|'[^']*'|\S+/g) || []).map((t) => t.replace(/^["']|["']$/g, ''));
}

const NPM_VALUE_FLAGS = new Set(['--prefix', '-w', '--workspace', '--registry', '--tag', '-C']);

function npmSpecs(args) {
  const specs = [];
  for (let i = 0; i < args.length; i += 1) {
    const a = args[i];
    if (NPM_VALUE_FLAGS.has(a)) { i += 1; continue; }
    if (a.startsWith('-')) continue;
    specs.push(a);
  }
  return specs;
}

function hasExplicitVersion(spec) {
  if (/^(\.|\/|file:|git|https?:|github:)/i.test(spec)) return true; // local or URL source
  const at = spec.lastIndexOf('@');
  if (at <= 0) return false;
  return /^[~^]?\d+(\.\d+){0,2}([-+][0-9A-Za-z.-]+)?$/.test(spec.slice(at + 1));
}

function checkSegment(segment, extraPatterns) {
  const t = tokens(segment);
  const problems = [];

  // npm
  const npmAt = t.findIndex((x) => /^npm(\.cmd)?$/i.test(x));
  if (npmAt >= 0) {
    const sub = (t[npmAt + 1] || '').toLowerCase();
    const args = t.slice(npmAt + 2);
    if (['install', 'i', 'add', 'update', 'up', 'upgrade', 'ci'].includes(sub)) {
      if (args.some((a) => a === '--force' || a === '-f' || a === '--legacy-peer-deps')) {
        problems.push('npm peer-dependency conflicts must be resolved, not bypassed with --force or --legacy-peer-deps (add-dependency).');
      }
    }
    if (['update', 'up', 'upgrade'].includes(sub)) {
      problems.push('`npm update` changes versions implicitly; install each package with an explicit verified version instead.');
    } else if (['install', 'i', 'add'].includes(sub)) {
      const missing = npmSpecs(args).filter((s) => !hasExplicitVersion(s));
      if (missing.length) problems.push(`npm package(s) without an explicit version: ${missing.join(', ')}.`);
    }
  }

  // dotnet add/package/tool
  const dnAt = t.findIndex((x) => /^dotnet(\.exe)?$/i.test(x));
  if (dnAt >= 0) {
    const rest = t.slice(dnAt + 1).map((x) => x.toLowerCase());
    const isAddPackage = (rest[0] === 'add' && rest.includes('package')) || (rest[0] === 'package' && rest[1] === 'add');
    const isToolInstall = rest[0] === 'tool' && (rest[1] === 'install' || rest[1] === 'update');
    if (rest[0] === 'package' && rest[1] === 'update') {
      problems.push('`dotnet package update` changes versions implicitly; set explicit verified versions in Directory.Packages.props instead.');
    }
    if (isAddPackage || isToolInstall) {
      if (rest.includes('--prerelease')) problems.push('`--prerelease` selects a floating prerelease; pass an explicit version (prereleases only when explicitly requested).');
      const vAt = rest.findIndex((x) => x === '--version' || x === '-v');
      if (vAt < 0 || !rest[vAt + 1] || rest[vAt + 1].includes('*')) {
        problems.push(`\`dotnet ${rest.slice(0, 3).join(' ')} …\` without an explicit --version.`);
      }
    }
  }

  // framework-specific dependency commands declared by selected modules
  for (const { regex, description } of extraPatterns) {
    const match = regex.exec(segment);
    if (match) {
      const specs = npmSpecs(tokens(match.groups && match.groups.specs ? match.groups.specs : ''));
      const missing = specs.filter((s) => !hasExplicitVersion(s));
      if (specs.length === 0 || missing.length) {
        problems.push(`${description} without an explicit version: ${missing.join(', ') || '(no package)'}.`);
      }
    }
  }
  return problems;
}

function main() {
  try {
    const input = lib.readStdinJson();
    const command = input && input.tool_input && input.tool_input.command;
    if (typeof command !== 'string' || !command.trim()) process.exit(0);
    const root = lib.resolveRoot(__dirname);
    const extra = lib.moduleDependencyPatterns(root);
    const problems = segments(command).flatMap((s) => checkSegment(s, extra));
    if (problems.length) {
      process.stdout.write(JSON.stringify({
        hookSpecificOutput: {
          hookEventName: 'PreToolUse',
          permissionDecision: 'deny',
          permissionDecisionReason: `[dependency-guard] Blocked dependency command.\n- ${problems.join('\n- ')}\n${ROUTE}`,
        },
      }));
    }
    process.exit(0);
  } catch (error) {
    process.stderr.write(`[dependency-guard] could not evaluate the command: ${error.message}\n`);
    process.exit(1);
  }
}

main();
