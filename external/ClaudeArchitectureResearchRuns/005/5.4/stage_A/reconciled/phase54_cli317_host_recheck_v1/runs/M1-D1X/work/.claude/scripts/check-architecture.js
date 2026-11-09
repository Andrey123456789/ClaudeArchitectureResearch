#!/usr/bin/env node
'use strict';
// Architecture check: backend project-reference direction, test-project
// reference breadth, and forbidden namespaces in inner layers.
// The specification comes from the selected architecture frame's manifest
// (enforcement.architecture); persistence-technology namespaces come from the
// selected persistence manifest. Policy owner: .claude/rules/architecture.md.
// Checks the repository or worktree that contains the working directory.
// Usage (any directory inside it; file arguments are relative to that directory):
//   node "$(git rev-parse --show-toplevel)/.claude/scripts/check-architecture.js" [file.cs ...]   (default: whole backend)

const path = require('path');
const common = require('./lib/common.js');

function finding(level, file, message) {
  return { level, file, message };
}

function loadSpec() {
  const modules = common.loadSelectedModules();
  const frame = common.moduleFor(modules, 'architecture');
  if (!frame) throw new Error('no architecture frame is selected in docs/capability-selection.md');
  const spec = frame.manifest.enforcement && frame.manifest.enforcement.architecture;
  if (!spec) throw new Error(`${frame.file} has no enforcement.architecture specification`);
  const placeholders = {};
  for (const m of modules) {
    for (const [key, value] of Object.entries(m.manifest.enforcement || {})) {
      if (Array.isArray(value)) placeholders[`{${m.slot}.${key}}`] = value;
    }
  }
  const forbidden = {};
  for (const [role, list] of Object.entries(spec.forbiddenNamespaces || {})) {
    forbidden[role] = list.flatMap((entry) => (placeholders[entry] ? placeholders[entry] : entry.startsWith('{') ? [] : [entry]));
  }
  const testing = common.moduleFor(modules, 'backend-testing');
  return {
    spec,
    owner: spec.owner || '.claude/rules/architecture.md',
    forbidden,
    testFrameworkPackages: (testing && testing.manifest.enforcement && testing.manifest.enforcement.testFrameworkPackages) || [],
  };
}

function classify(name, ctx, xml) {
  const tests = [...ctx.spec.testProjects].sort((a, b) => b.suffix.length - a.suffix.length);
  const test = tests.find((t) => name.endsWith(t.suffix));
  if (test) return { kind: 'test', rule: test };
  const isTestByPackage = common.xmlElements(xml || '', 'PackageReference').some((e) => e.attrs && ctx.testFrameworkPackages.includes(e.attrs.Include));
  if (isTestByPackage || /\.Tests$/.test(name)) return { kind: 'test', rule: null };
  const layer = ctx.spec.layers.find((l) => name.endsWith(l.suffix));
  if (layer) return { kind: 'layer', rule: layer };
  return { kind: 'unknown', rule: null };
}

// Referenced project names, and the ProjectReference elements that cannot be read reliably.
function projectReferences(xml) {
  const names = [];
  const unreadable = [];
  for (const e of common.xmlElements(xml, 'ProjectReference')) {
    if (e.problem) unreadable.push(e);
    if (e.attrs && e.attrs.Include) names.push(path.basename(e.attrs.Include.replace(/\\/g, '/'), '.csproj'));
  }
  return { names, unreadable };
}

function checkReferences(ctx, findings) {
  const root = ctx.spec.projectRoot || 'backend';
  const projects = common.walk(root).filter((f) => f.endsWith('.csproj'));
  const info = new Map();
  for (const file of projects) {
    const xml = common.readXml(file);
    const name = path.basename(file, '.csproj');
    info.set(name, { file, xml, cls: classify(name, ctx, xml) });
  }
  for (const [name, p] of info) {
    const { names: refs, unreadable } = projectReferences(p.xml);
    if (p.cls.kind === 'unknown') {
      findings.push(finding('WARN', p.file, `project ${name} does not match a frame layer or test-project role; adding a project or layer is Reserved (${ctx.owner}).`));
      continue;
    }
    for (const e of unreadable) {
      findings.push(finding('WARN', p.file, `${name}: ProjectReference at line ${e.line} cannot be read reliably (${e.problem}); the reference check is incomplete (${ctx.owner}).`));
    }
    for (const ref of refs) {
      const target = info.get(ref);
      const tcls = target ? target.cls : classify(ref, ctx, '');
      if (tcls.kind === 'test') {
        findings.push(finding('ERROR', p.file, `${name} references test project ${ref}.`));
        continue;
      }
      if (tcls.kind !== 'layer') {
        findings.push(finding('WARN', p.file, `${name} references ${ref}, which matches no frame layer (${ctx.owner}).`));
        continue;
      }
      if (p.cls.kind === 'layer') {
        if (!p.cls.rule.mayReference.includes(tcls.rule.role)) {
          findings.push(finding('ERROR', p.file, `${name} (${p.cls.rule.role}) must not reference ${ref} (${tcls.rule.role}); dependencies point inward (${ctx.owner}, Dependency Direction).`));
        }
      } else if (p.cls.rule && !p.cls.rule.mayReference.includes(tcls.rule.role)) {
        findings.push(finding('WARN', p.file, `test project ${name} references ${ref} (${tcls.rule.role}); keep test references as narrow as the test scope requires (${ctx.owner}, Test Project References).`));
      }
    }
  }
  return info;
}

function layerOfFile(rel, info) {
  let best = null;
  for (const [name, p] of info) {
    const dir = path.posix.dirname(p.file);
    if ((rel === dir || rel.startsWith(`${dir}/`)) && (!best || dir.length > best.dir.length)) best = { name, dir, cls: p.cls };
  }
  return best;
}

function checkNamespaces(ctx, info, files, findings) {
  const targets = files && files.length ? files.filter((f) => f.endsWith('.cs')) : common.walk(ctx.spec.projectRoot || 'backend').filter((f) => f.endsWith('.cs'));
  for (const rel of targets) {
    if (!common.exists(rel)) continue;
    const owner = layerOfFile(rel, info);
    if (!owner || owner.cls.kind !== 'layer') continue;
    const forbidden = ctx.forbidden[owner.cls.rule.role] || [];
    if (!forbidden.length) continue;
    const lines = common.readText(rel).split(/\r?\n/);
    lines.forEach((line, i) => {
      const m = /^\s*(?:global\s+)?using\s+(?:static\s+)?(?:\w+\s*=\s*)?([\w.]+)\s*;/.exec(line);
      if (!m) return;
      const ns = m[1];
      const hit = forbidden.find((f) => ns === f || ns.startsWith(`${f}.`));
      if (hit) {
        findings.push(finding('ERROR', `${rel}:${i + 1}`, `${owner.cls.rule.role} code imports ${ns}; ${hit} types must not be used in this layer (${ctx.owner}).`));
      }
    });
  }
}

function checkArchitecture(files) {
  common.projectRoot();
  const ctx = loadSpec();
  const findings = [];
  const info = checkReferences(ctx, findings);
  checkNamespaces(ctx, info, files, findings);
  return { findings, projectCount: info.size };
}

module.exports = { checkArchitecture };

if (require.main === module) {
  try {
    const files = process.argv.slice(2).map((f) => {
      const rel = common.relativeInsideRoot(f, process.cwd());
      if (!rel) throw new Error(`file outside the project root: ${f}`);
      return rel;
    });
    const { findings, projectCount } = checkArchitecture(files);
    if (findings.length) console.log(common.formatFindings(findings));
    const errors = findings.filter((f) => f.level === 'ERROR').length;
    console.log(`check-architecture: ${projectCount} backend project(s), ${errors} error(s), ${findings.length - errors} warning(s)`);
    process.exit(errors ? 1 : 0);
  } catch (e) {
    console.error(`check-architecture: cannot run: ${e.message}`);
    process.exit(2);
  }
}
