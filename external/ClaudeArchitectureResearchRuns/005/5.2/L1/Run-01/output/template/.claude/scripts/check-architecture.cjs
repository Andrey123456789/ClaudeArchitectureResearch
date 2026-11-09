#!/usr/bin/env node
// Level: 3-project | Owns: neutral architecture check — project classification, allowed
// project references, test-framework packages. Specification comes from the selected
// frame (architecture.check) and test-framework adapter (backend-testing.check).
// Usage: node .claude/scripts/check-architecture.cjs   (exit 0 pass, 1 violations, 2 environment error)
'use strict';

const fs = require('fs');
const path = require('path');
const lib = require('./lib/project.cjs');

function classify(name, spec) {
  const byLongestSuffix = (a, b) => b.suffix.length - a.suffix.length;
  for (const entry of [...spec.testProjects].sort(byLongestSuffix)) {
    if (name.endsWith(entry.suffix)) return { kind: 'test', layer: entry.suffix.replace(/^\./, ''), entry };
  }
  for (const entry of [...spec.projects].sort(byLongestSuffix)) {
    if (name.endsWith(entry.suffix)) return { kind: 'production', layer: entry.layer, entry };
  }
  return null;
}

function checkArchitecture(root) {
  const frame = lib.requireModuleJson(root, 'architecture', 'check.json');
  const adapter = lib.requireModuleJson(root, 'backend-testing', 'check.json');
  const violations = [];
  const notes = [];

  const backendRoot = path.join(root, frame.backendRoot || 'backend');
  const projectFiles = lib.walk(backendRoot, (name) => name.endsWith('.csproj'));
  if (projectFiles.length === 0) {
    notes.push(`No .csproj files under ${frame.backendRoot || 'backend'}/ — nothing to check.`);
    return { violations, notes };
  }

  const projects = new Map();
  for (const file of projectFiles) {
    const name = path.basename(file, '.csproj');
    projects.set(path.resolve(file).toLowerCase(), {
      name,
      file,
      rel: lib.toPosix(path.relative(root, file)),
      cls: classify(name, frame),
      msbuild: lib.parseMsbuild(lib.readText(file)),
    });
  }

  const competing = new Set((adapter.competingFrameworkPackages || []).map((p) => p.toLowerCase()));

  for (const project of projects.values()) {
    const { cls, rel, msbuild } = project;
    if (!cls) {
      violations.push(`${rel}: project is not classified by architecture.check — adding a project or layer is Reserved; after approval classify it in the frame's check.json.`);
      continue;
    }
    for (const ref of msbuild.projectReferences) {
      if (!ref.include) continue;
      const target = path.resolve(path.dirname(project.file), ref.include.replace(/\\/g, '/'));
      const targetProject = projects.get(target.toLowerCase());
      const targetName = targetProject ? targetProject.name : path.basename(target, '.csproj');
      const targetCls = targetProject ? targetProject.cls : classify(targetName, frame);
      if (!targetCls) {
        violations.push(`${rel}: references unclassified project ${targetName}.`);
        continue;
      }
      if (targetCls.kind === 'test') {
        violations.push(`${rel}: references test project ${targetName}.`);
        continue;
      }
      if (!cls.entry.mayReference.includes(targetCls.layer)) {
        violations.push(`${rel}: ${cls.layer} must not reference ${targetCls.layer} (${targetName}); allowed: ${cls.entry.mayReference.join(', ') || 'none'} — see architecture.boundaries.`);
      }
    }
    const packages = msbuild.packageReferences.map((p) => (p.include || '').toLowerCase());
    for (const pkg of packages) {
      if (competing.has(pkg)) violations.push(`${rel}: competing test framework package ${pkg} — a second test framework needs a concrete reason (backend-testing.rules).`);
    }
    if (cls.kind === 'test') {
      for (const required of adapter.frameworkPackages || []) {
        if (!packages.includes(required.toLowerCase())) {
          violations.push(`${rel}: test project lacks ${required} (backend-testing.scaffold).`);
        }
      }
    }
  }
  notes.push(`Checked ${projects.size} backend project(s).`);
  return { violations, notes };
}

function main() {
  let root;
  try {
    root = lib.resolveRoot(__dirname);
    const { violations, notes } = checkArchitecture(root);
    for (const note of notes) console.log(note);
    if (violations.length) {
      console.log(`Architecture check: ${violations.length} violation(s)`);
      for (const v of violations) console.log(`  - ${v}`);
      process.exit(1);
    }
    console.log('Architecture check: PASS');
  } catch (error) {
    console.error(`Architecture check could not run: ${error.message}`);
    process.exit(2);
  }
}

if (require.main === module) main();

module.exports = { checkArchitecture };
