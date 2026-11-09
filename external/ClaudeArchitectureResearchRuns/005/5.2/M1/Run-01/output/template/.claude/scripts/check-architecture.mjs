// Architecture check: validates backend project references and technology
// package placement against the selected architecture frame's specification and
// the selected persistence and backend-testing manifests.
// Usage: node .claude/scripts/check-architecture.mjs [--root <dir>]
import path from 'node:path';
import { pathToFileURL } from 'node:url';
import { TemplateError, resolveRoot, readText, walk, loadCapabilities, globToRegExp, report } from './lib/template.mjs';

const projectName = rel => path.posix.basename(rel).replace(/\.csproj$/i, '');

function attrValues(xml, element) {
  return [...xml.matchAll(new RegExp(`<${element}\\b[^>]*\\bInclude="([^"]+)"`, 'g'))].map(m => m[1]);
}

export function runArchitectureChecks(root) {
  const errors = [], warnings = [], info = [];
  const { modules } = loadCapabilities(root);
  const frame = modules.architecture?.manifest;
  if (!frame) throw new TemplateError('No selected architecture frame manifest; run check-instructions.mjs');
  const layers = frame.properties.layers;
  const testSpecs = frame.properties.testProjects ?? [];
  const persistence = modules.persistence?.manifest?.properties ?? {};
  const techPackages = (persistence.technologyPackages ?? []).map(globToRegExp);
  const forbiddenRoles = new Set(persistence.technologyForbiddenInRoles ?? []);
  const testMarkers = new Set(modules['backend-testing']?.manifest?.properties?.testProjectMarkers ?? []);

  const projects = walk(root, 'backend').filter(p => p.endsWith('.csproj'));
  if (projects.length === 0) {
    info.push('No backend projects under backend/; architecture check not applicable.');
    return { errors, warnings, info };
  }

  const classify = name => {
    const test = [...testSpecs].sort((a, b) => b.suffix.length - a.suffix.length).find(t => name.endsWith(t.suffix));
    if (test) return { kind: 'test', spec: test };
    const layer = layers.find(l => name.endsWith(l.suffix));
    return layer ? { kind: 'layer', spec: layer } : null;
  };
  const layerOf = name => layers.find(l => name.endsWith(l.suffix))?.name ?? null;
  const known = new Map(projects.map(p => [projectName(p), classify(projectName(p))]));

  for (const rel of projects) {
    const name = projectName(rel);
    const role = known.get(name);
    const xml = readText(root, rel);
    if (!role) { warnings.push(`${rel}: project matches no layer or test-project suffix of the architecture frame (adding a production project is Reserved)`); continue; }
    const allowed = new Set(role.spec.allowedReferences);
    for (const ref of attrValues(xml, 'ProjectReference')) {
      const target = projectName(ref.replace(/\\/g, '/'));
      const targetRole = known.get(target) ?? classify(target);
      if (targetRole?.kind === 'test') { errors.push(`${rel}: references test project ${target}`); continue; }
      const targetLayer = layerOf(target);
      if (!targetLayer) { warnings.push(`${rel}: references ${target}, which matches no layer of the architecture frame`); continue; }
      if (!allowed.has(targetLayer)) errors.push(`${rel}: reference to ${target} (${targetLayer}) is not allowed for ${role.kind === 'test' ? 'test project' : 'layer'} ${role.kind === 'test' ? role.spec.suffix : role.spec.name}; allowed: ${[...allowed].join(', ') || 'none'} (architecture-style.md)`);
    }
    const packages = attrValues(xml, 'PackageReference');
    if (role.kind === 'layer' && forbiddenRoles.has(role.spec.role)) {
      for (const pkg of packages) if (techPackages.some(re => re.test(pkg))) errors.push(`${rel}: persistence-technology package ${pkg} is not allowed in the ${role.spec.role} (persistence-technology.md)`);
    }
    if (role.kind === 'layer') for (const pkg of packages) if (testMarkers.has(pkg)) errors.push(`${rel}: production project references test-framework package ${pkg}`);
  }
  info.push(`checked ${projects.length} backend project(s)`);
  return { errors, warnings, info };
}

function main() {
  try {
    const i = process.argv.indexOf('--root');
    const root = resolveRoot(i > 0 ? process.argv[i + 1] : undefined);
    const result = runArchitectureChecks(root);
    console.log(report('Architecture', result));
    process.exit(result.errors.length ? 1 : 0);
  } catch (e) {
    console.error(`check-architecture: ${e instanceof TemplateError ? e.message : e.stack}`);
    process.exit(2);
  }
}

if (import.meta.url === pathToFileURL(process.argv[1]).href) main();
