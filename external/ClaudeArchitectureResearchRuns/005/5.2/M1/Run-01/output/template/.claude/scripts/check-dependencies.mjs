// Dependency check: NuGet Central Package Management, floating/prerelease
// versions, deny-listed packages, default-excluded frontend packages, and npm
// lockfiles. Policy owners: dependencies.md, docs/technology-stack.md, and the
// add-dependency workflow.
// Usage: node .claude/scripts/check-dependencies.mjs [--root <dir>]
import path from 'node:path';
import { pathToFileURL } from 'node:url';
import { TemplateError, resolveRoot, exists, readText, walk, loadCapabilities, globToRegExp, report } from './lib/template.mjs';

const isFloating = v => /\*|^latest$|^x$/i.test(v.trim()) || v.trim() === '';
const isPrerelease = v => /\d-[0-9A-Za-z]/.test(v) && !/^[\^~]?\d+\.\d+\.\d+$/.test(v);

export function runDependencyChecks(root) {
  const errors = [], warnings = [], info = [];
  const policy = JSON.parse(readText(root, '.claude/scripts/dependency-policy.json'));
  const deny = new Map(policy.deny.map(d => [d.package.toLowerCase(), d.reason]));
  const warn = new Map(policy.warn.map(d => [d.package.toLowerCase(), d.reason]));
  const { modules } = loadCapabilities(root);
  const notByDefault = (modules.frontend?.manifest?.properties?.notByDefaultPackages ?? []).map(globToRegExp);

  const checkPackage = (where, name) => {
    const key = name.toLowerCase();
    if (deny.has(key)) errors.push(`${where}: ${name} is not allowed — ${deny.get(key)}`);
    else if (warn.has(key)) warnings.push(`${where}: ${name} — ${warn.get(key)}`);
  };

  const projects = walk(root, '.').filter(p => p.endsWith('.csproj'));
  if (projects.length) {
    if (!exists(root, 'Directory.Packages.props')) errors.push('Directory.Packages.props is missing; NuGet Central Package Management is required (dependencies.md)');
    else {
      const props = readText(root, 'Directory.Packages.props');
      if (!/<ManagePackageVersionsCentrally>\s*true\s*<\/ManagePackageVersionsCentrally>/i.test(props)) errors.push('Directory.Packages.props: ManagePackageVersionsCentrally must be true');
      for (const m of props.matchAll(/<PackageVersion\b[^>]*\bInclude="([^"]+)"[^>]*\bVersion="([^"]*)"/g)) {
        const [, name, version] = m;
        checkPackage('Directory.Packages.props', name);
        if (isFloating(version)) errors.push(`Directory.Packages.props: ${name} uses floating/empty version "${version}"`);
        else if (isPrerelease(version)) warnings.push(`Directory.Packages.props: ${name} ${version} is a prerelease; allowed only when explicitly requested`);
      }
    }
    for (const rel of projects) {
      const xml = readText(root, rel);
      for (const m of xml.matchAll(/<PackageReference\b([^>]*?)(\/>|>([\s\S]*?)<\/PackageReference>)/g)) {
        const attrs = m[1];
        const name = /\bInclude="([^"]+)"/.exec(attrs)?.[1] ?? '?';
        checkPackage(rel, name);
        if (/\bVersion="/.test(attrs) || /<Version>/.test(m[3] ?? '')) errors.push(`${rel}: PackageReference ${name} declares a version; versions belong in Directory.Packages.props`);
        if (/\bVersionOverride="/.test(attrs)) warnings.push(`${rel}: PackageReference ${name} uses VersionOverride; justify it or centralize the version`);
      }
    }
  }

  for (const rel of walk(root, '.').filter(p => path.posix.basename(p) === 'package.json')) {
    let pkg;
    try { pkg = JSON.parse(readText(root, rel)); } catch (e) { errors.push(`${rel}: invalid JSON (${e.message})`); continue; }
    if (!exists(root, path.posix.join(path.posix.dirname(rel), 'package-lock.json'))) warnings.push(`${rel}: no package-lock.json next to it; npm lockfile must be maintained (dependencies.md)`);
    for (const section of ['dependencies', 'devDependencies', 'optionalDependencies', 'peerDependencies']) {
      for (const [name, version] of Object.entries(pkg[section] ?? {})) {
        checkPackage(rel, name);
        if (isFloating(String(version))) errors.push(`${rel}: ${section}.${name} uses floating version "${version}"`);
        else if (isPrerelease(String(version))) warnings.push(`${rel}: ${section}.${name} ${version} is a prerelease; allowed only when explicitly requested`);
        if (notByDefault.some(re => re.test(name))) warnings.push(`${rel}: ${name} is excluded by default by the frontend stack decision; keep it only for a concrete requirement`);
      }
    }
  }
  info.push(`checked ${projects.length} project file(s)`);
  return { errors, warnings, info };
}

function main() {
  try {
    const i = process.argv.indexOf('--root');
    const root = resolveRoot(i > 0 ? process.argv[i + 1] : undefined);
    const result = runDependencyChecks(root);
    console.log(report('Dependencies', result));
    process.exit(result.errors.length ? 1 : 0);
  } catch (e) {
    console.error(`check-dependencies: ${e instanceof TemplateError ? e.message : e.stack}`);
    process.exit(2);
  }
}

if (import.meta.url === pathToFileURL(process.argv[1]).href) main();
