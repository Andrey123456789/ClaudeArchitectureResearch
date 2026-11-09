// Level: 3 Project | Manifest and architecture checks (enforcement asset).
// Checks: NuGet Central Package Management, floating/prerelease versions, package deny/approval
// lists, backend project-reference direction, test-project reference breadth, npm floating versions.
// Owners: 2-technology/package-management.md, 1-architecture/backend-layers.md, add-dependency skill.
// Usage: node .claude/scripts/check-manifests.cjs [--json]
'use strict';

const fs = require('fs');
const path = require('path');

const SKIP_DIRS = new Set(['node_modules', 'bin', 'obj', '.git', 'dist', '.angular', '.vs', 'TestResults', 'coverage']);
const LAYER_RANK = { Domain: 0, Application: 1, Infrastructure: 2, Api: 3 };

function resolveRoot() {
  const configured = process.env.CLAUDE_PROJECT_DIR || process.cwd();
  const root = path.resolve(configured);
  if (!fs.existsSync(path.join(root, '.claude'))) {
    throw new Error(`check-manifests: cannot locate the project root (no .claude directory in "${root}"). ` +
      'Run from the repository root or set CLAUDE_PROJECT_DIR.');
  }
  return root;
}

function walk(dir, out) {
  for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
    if (entry.isDirectory()) {
      if (!SKIP_DIRS.has(entry.name)) walk(path.join(dir, entry.name), out);
    } else {
      out.push(path.join(dir, entry.name));
    }
  }
  return out;
}

function rel(root, file) {
  return path.relative(root, file).split(path.sep).join('/');
}

function loadPolicy(root) {
  const file = path.join(root, '.claude', 'scripts', 'dependency-policy.json');
  if (!fs.existsSync(file)) {
    throw new Error(`check-manifests: missing policy file ${rel(root, file)}.`);
  }
  return JSON.parse(fs.readFileSync(file, 'utf8'));
}

function isFloatingOrPrerelease(version) {
  if (!version) return null;
  const v = version.trim();
  if (v.includes('*')) return 'floating version';
  if (/^[\[(]/.test(v)) return 'version range';
  if (/-[0-9A-Za-z]/.test(v)) return 'prerelease version';
  return null;
}

function classifyProject(name) {
  if (/IntegrationTests$/.test(name)) return { kind: 'integration-tests' };
  const test = name.match(/\.(Domain|Application|Infrastructure|Api)\.Tests$/);
  if (test) return { kind: 'tests', layer: test[1] };
  if (/\.Tests$/.test(name)) return { kind: 'tests', layer: null };
  const prod = name.match(/\.(Domain|Application|Infrastructure|Api)$/);
  if (prod) return { kind: 'production', layer: prod[1] };
  return { kind: 'unknown' };
}

function attr(tag, name) {
  const m = tag.match(new RegExp(`\\b${name}\\s*=\\s*"([^"]*)"`, 'i'));
  return m ? m[1] : null;
}

function checkPackageName(findings, file, ecosystem, name, policy) {
  const exceptions = new Set(policy.approvedExceptions || []);
  if (exceptions.has(name)) return;
  const lists = policy[ecosystem] || {};
  if (lists.denied && lists.denied[name]) {
    findings.push({ severity: 'error', file, message: `package "${name}" is not allowed: ${lists.denied[name]}` });
  } else if (lists.approvalRequired && lists.approvalRequired[name]) {
    findings.push({ severity: 'error', file, message: `package "${name}" requires an accepted Decision Request: ${lists.approvalRequired[name]} (run architecture-decision; then add it to approvedExceptions)` });
  }
}

function checkManifests(root = resolveRoot()) {
  const policy = loadPolicy(root);
  const files = walk(root, []);
  const findings = [];
  const projects = files.filter(f => f.endsWith('.csproj'));
  const hasCentral = files.some(f => path.basename(f) === 'Directory.Packages.props');

  for (const file of files.filter(f => path.basename(f) === 'Directory.Packages.props')) {
    const text = fs.readFileSync(file, 'utf8');
    for (const tag of text.match(/<PackageVersion\b[^>]*>/gi) || []) {
      const name = attr(tag, 'Include');
      const problem = isFloatingOrPrerelease(attr(tag, 'Version'));
      if (problem) findings.push({ severity: 'error', file: rel(root, file), message: `${name}: ${problem} — use the latest stable compatible version unless explicitly requested (add-dependency, step 2)` });
      if (name) checkPackageName(findings, rel(root, file), 'nuget', name, policy);
    }
  }

  const byName = new Map(projects.map(p => [path.basename(p, '.csproj'), p]));
  for (const file of projects) {
    const text = fs.readFileSync(file, 'utf8');
    const name = path.basename(file, '.csproj');
    const r = rel(root, file);
    const packageRefs = text.match(/<PackageReference\b[^>]*\/>|<PackageReference\b[^>]*>[\s\S]*?<\/PackageReference>/gi) || [];
    if (packageRefs.length && !hasCentral) {
      findings.push({ severity: 'error', file: r, message: 'PackageReference without Directory.Packages.props — Central Package Management is required (2-technology/package-management.md)' });
    }
    for (const ref of packageRefs) {
      const pkg = attr(ref, 'Include');
      if (attr(ref, 'Version') || attr(ref, 'VersionOverride') || /<Version>/i.test(ref)) {
        findings.push({ severity: 'error', file: r, message: `${pkg}: version in .csproj — versions belong in Directory.Packages.props (2-technology/package-management.md)` });
      }
      if (pkg) checkPackageName(findings, r, 'nuget', pkg, policy);
    }

    const self = classifyProject(name);
    if (self.kind === 'unknown' && r.startsWith('backend/')) {
      findings.push({ severity: 'warning', file: r, message: `project "${name}" is not a recognized layer (Domain/Application/Infrastructure/Api or a test project); adding a production project is Reserved (CLAUDE.md, Decision Control)` });
    }
    for (const tag of text.match(/<ProjectReference\b[^>]*>/gi) || []) {
      const include = attr(tag, 'Include');
      if (!include) continue;
      const targetName = path.basename(include.replace(/\\/g, '/'), '.csproj');
      const target = classifyProject(targetName);
      if (!byName.has(targetName)) {
        findings.push({ severity: 'warning', file: r, message: `ProjectReference "${include}" does not resolve to a project in the repository` });
      }
      if (self.kind === 'production') {
        if (target.kind !== 'production') {
          findings.push({ severity: 'error', file: r, message: `production project references "${targetName}" — production code must not reference test or unrecognized projects (1-architecture/backend-layers.md)` });
        } else if (LAYER_RANK[target.layer] >= LAYER_RANK[self.layer]) {
          findings.push({ severity: 'error', file: r, message: `${self.layer} -> ${target.layer} points outward or sideways — dependencies must point inward (1-architecture/backend-layers.md)` });
        }
      } else if (self.kind === 'tests' && self.layer) {
        if (target.kind !== 'production' || LAYER_RANK[target.layer] > LAYER_RANK[self.layer]) {
          findings.push({ severity: 'error', file: r, message: `${name} references "${targetName}" — test-project references must stay as narrow as the test scope (1-architecture/backend-layers.md)` });
        }
      }
    }
  }

  for (const file of files.filter(f => path.basename(f) === 'package.json')) {
    let json;
    try {
      json = JSON.parse(fs.readFileSync(file, 'utf8'));
    } catch (error) {
      findings.push({ severity: 'error', file: rel(root, file), message: `invalid JSON: ${error.message}` });
      continue;
    }
    for (const section of ['dependencies', 'devDependencies']) {
      for (const [pkg, version] of Object.entries(json[section] || {})) {
        if (/^(\*|x|latest|next)?$/i.test(String(version).trim())) {
          findings.push({ severity: 'error', file: rel(root, file), message: `${pkg}: floating version "${version}" — pin a stable compatible version (add-dependency, step 2)` });
        }
        checkPackageName(findings, rel(root, file), 'npm', pkg, policy);
      }
    }
  }
  return findings;
}

function format(findings) {
  return findings.map(f => `${f.severity.toUpperCase()} ${f.file}: ${f.message}`).join('\n');
}

module.exports = { checkManifests, format, resolveRoot };

if (require.main === module) {
  try {
    const findings = checkManifests();
    if (process.argv.includes('--json')) {
      console.log(JSON.stringify(findings, null, 2));
    } else {
      console.log(findings.length ? format(findings) : 'check-manifests: no findings.');
    }
    process.exit(findings.some(f => f.severity === 'error') ? 1 : 0);
  } catch (error) {
    console.error(error.message);
    process.exit(2);
  }
}
