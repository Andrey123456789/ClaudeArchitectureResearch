// Kind: ENF | Scope: common | Capability: — | Loading: run by hooks, verify, add-dependency or manually: node .claude/scripts/check-manifests.mjs [--root <dir>] | Checks NuGet and npm manifests against the dependency standards
import path from 'node:path';
import { existsSync } from 'node:fs';
import {
  EnforcementError, rootFromArgs, loadEnforcement, listFiles, parseProjectFile, readText, formatFindings, isMainModule,
} from './lib/common.mjs';

const PRERELEASE = /-(alpha|beta|rc|preview|pre|dev|nightly|next|canary)/i;

function nugetFindings(root, policy, violations, warnings) {
  const propsPath = 'Directory.Packages.props';
  const projectFiles = listFiles(root, '.', (p) => p.toLowerCase().endsWith('.csproj'));
  const denied = new Map(policy.nuget.denied.map((d) => [d.id.toLowerCase(), d.reason]));
  const watch = policy.nuget.approvalWatch;
  const checkId = (where, id) => {
    const reason = denied.get(id.toLowerCase());
    if (reason) {
      violations.push(`${where}: ${id} is on the denied list (${reason}).`);
      return;
    }
    const watched = watch.find((w) => id.toLowerCase() === w.prefix.toLowerCase() || id.toLowerCase().startsWith(`${w.prefix.toLowerCase()}.`));
    if (watched) {
      warnings.push(`${where}: ${id} is on the approval watch-list (${watched.reason}).`);
    }
  };

  const central = new Map();
  let centralEnabled = false;
  if (existsSync(path.join(root, propsPath))) {
    const props = parseProjectFile(readText(root, propsPath));
    centralEnabled = props.centralManagement;
    for (const entry of props.packageVersions) {
      central.set(entry.Include.toLowerCase(), entry.Version ?? '');
      const version = entry.Version ?? '';
      if (version === '' || version.includes('*') || /^[[(]/.test(version)) {
        violations.push(`${propsPath}: ${entry.Include} has a non-exact version "${version}" (see add-dependency → 2. Select the version).`);
      } else if (PRERELEASE.test(version)) {
        warnings.push(`${propsPath}: ${entry.Include} ${version} is a prerelease version (see add-dependency → 2. Select the version).`);
      }
      checkId(propsPath, entry.Include);
    }
  } else if (projectFiles.length > 0) {
    violations.push(`${propsPath} is missing (see .claude/rules/common/dependencies.md → NuGet).`);
  }

  for (const file of projectFiles) {
    const info = parseProjectFile(readText(root, file));
    for (const reference of info.packageReferences) {
      const id = reference.Include ?? reference.Update;
      checkId(file, id);
      if (centralEnabled) {
        if (reference.Version !== undefined) {
          violations.push(`${file}: ${id} declares a Version attribute under Central Package Management (see .claude/rules/common/dependencies.md → NuGet).`);
        }
        if (reference.VersionOverride !== undefined) {
          warnings.push(`${file}: ${id} uses VersionOverride (see .claude/rules/common/dependencies.md → NuGet).`);
        }
        if (reference.Include && !central.has(id.toLowerCase()) && reference.VersionOverride === undefined) {
          violations.push(`${file}: ${id} has no PackageVersion in ${propsPath} (see add-dependency → 5. Install).`);
        }
      }
    }
  }
}

function npmFindings(root, policy, frontend, violations, warnings) {
  const manifests = listFiles(root, '.', (p) => p.endsWith('package.json') && path.posix.basename(p) === 'package.json');
  const tooling = [...policy.npm.devToolingPackages, ...(frontend?.devToolingPackages ?? [])];
  const watch = frontend?.npmApprovalWatch ?? [];
  for (const manifest of manifests) {
    let json;
    try {
      json = JSON.parse(readText(root, manifest));
    } catch (error) {
      violations.push(`${manifest}: not valid JSON (${error.message}).`);
      continue;
    }
    const lockfile = path.posix.join(path.posix.dirname(manifest), 'package-lock.json');
    const sections = { dependencies: json.dependencies ?? {}, devDependencies: json.devDependencies ?? {} };
    if (Object.keys(sections.dependencies).length + Object.keys(sections.devDependencies).length > 0
      && !existsSync(path.join(root, lockfile))) {
      warnings.push(`${manifest}: no package-lock.json next to it (see .claude/rules/common/dependencies.md → npm).`);
    }
    for (const [section, packages] of Object.entries(sections)) {
      for (const [name, spec] of Object.entries(packages)) {
        const where = `${manifest} ${section}`;
        if (spec === '*' || spec === 'latest' || spec === 'next' || spec === '') {
          violations.push(`${where}: ${name} uses a floating version "${spec}" (see add-dependency → 2. Select the version).`);
        } else if (PRERELEASE.test(spec)) {
          warnings.push(`${where}: ${name} ${spec} is a prerelease version (see add-dependency → 2. Select the version).`);
        }
        if (section === 'dependencies' && tooling.some((t) => (t.endsWith('/') ? name.startsWith(t) : name === t))) {
          warnings.push(`${where}: ${name} is build or test tooling listed under dependencies (see .claude/rules/common/dependencies.md → npm).`);
        }
        const watched = watch.find((w) => new RegExp(w.match, 'i').test(name));
        if (watched) {
          warnings.push(`${where}: ${name} is on the approval watch-list (${watched.reason}).`);
        }
      }
    }
  }
}

export function checkManifests(root) {
  const { policy, frontend } = loadEnforcement(root);
  const violations = [];
  const warnings = [];
  nugetFindings(root, policy, violations, warnings);
  npmFindings(root, policy, frontend, violations, warnings);
  return { violations, warnings };
}

function main() {
  try {
    const root = rootFromArgs(process.argv.slice(2));
    const { violations, warnings } = checkManifests(root);
    if (warnings.length > 0) {
      console.log(formatFindings('Manifest warnings (report the reason or route through add-dependency):', warnings));
    }
    if (violations.length > 0) {
      console.log(formatFindings('Manifest violations:', violations));
      process.exit(1);
    }
    console.log('Manifest check: PASS');
  } catch (error) {
    console.error(`Manifest check could not run: ${error instanceof EnforcementError ? error.message : error.stack}`);
    process.exit(3);
  }
}

if (isMainModule(import.meta.url)) {
  main();
}
