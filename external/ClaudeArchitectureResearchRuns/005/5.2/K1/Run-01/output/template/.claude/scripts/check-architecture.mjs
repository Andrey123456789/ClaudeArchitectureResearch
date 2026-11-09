// Kind: ENF | Scope: backend | Capability: — | Loading: run by hooks, verify, the test adapter or manually: node .claude/scripts/check-architecture.mjs [--root <dir>] | Checks backend project references and packages against the architecture enforcement facets
import path from 'node:path';
import {
  EnforcementError, rootFromArgs, loadEnforcement, listFiles, parseProjectFile, readText, toRootRelative, formatFindings, isMainModule,
} from './lib/common.mjs';

function classify(projectName, architecture) {
  for (const test of architecture.testProjects) {
    if (projectName.toLowerCase().endsWith(test.suffix.toLowerCase())) {
      return { kind: 'test', rule: test };
    }
  }
  for (const role of architecture.roles) {
    if (projectName.toLowerCase().endsWith(`.${role.toLowerCase()}`)) {
      return { kind: 'production', role };
    }
  }
  return { kind: 'unclassified' };
}

function inwardClosure(role, allowed) {
  const result = new Set([role]);
  const stack = [role];
  while (stack.length > 0) {
    for (const next of allowed[stack.pop()] ?? []) {
      if (!result.has(next)) {
        result.add(next);
        stack.push(next);
      }
    }
  }
  return result;
}

export function checkArchitecture(root) {
  const { architecture, facets } = loadEnforcement(root);
  const owner = architecture.owner;
  const violations = [];
  const notes = [];
  const projectFiles = listFiles(root, architecture.projectRoot, (p) => p.toLowerCase().endsWith('.csproj'));

  if (projectFiles.length === 0) {
    notes.push(`No projects under ${architecture.projectRoot}/; nothing to check.`);
    return { violations, notes };
  }

  const infrastructureOnly = facets.flatMap((f) => f.infrastructureOnlyPackagePrefixes ?? []);
  const projects = new Map();
  for (const file of projectFiles) {
    const name = path.posix.basename(file, '.csproj');
    projects.set(file.toLowerCase(), { file, name, info: parseProjectFile(readText(root, file)), type: classify(name, architecture) });
  }

  for (const project of projects.values()) {
    const { file, name, info, type } = project;

    if (type.kind === 'unclassified') {
      violations.push(`${file}: project "${name}" matches no layer role or test-project convention (see CLAUDE.md → Decision control and ${owner}).`);
      continue;
    }

    let allowedRoles;
    if (type.kind === 'production') {
      allowedRoles = new Set(architecture.allowedReferences[type.role] ?? []);
      for (const framework of info.frameworkReferences) {
        if ((architecture.forbiddenFrameworkReferences[type.role] ?? []).includes(framework)) {
          violations.push(`${file}: ${type.role} references framework ${framework} (see ${owner}).`);
        }
      }
      if ((architecture.forbiddenSdks[type.role] ?? []).includes(info.sdk)) {
        violations.push(`${file}: ${type.role} uses SDK ${info.sdk} (see ${owner}).`);
      }
      if (architecture.innerRoles.includes(type.role)) {
        for (const reference of info.packageReferences) {
          const id = reference.Include ?? reference.Update;
          const prefix = infrastructureOnly.find((p) => id.toLowerCase().startsWith(p.toLowerCase()));
          if (prefix) {
            violations.push(`${file}: ${type.role} references persistence-technology package ${id} (see ${owner}, .claude/rules/backend/persistence-technology.md).`);
          }
        }
      }
    } else {
      allowedRoles = type.rule.layer
        ? inwardClosure(type.rule.layer, architecture.allowedReferences)
        : new Set(type.rule.mayReference ?? []);
    }

    for (const include of info.projectReferences) {
      const targetFile = toRootRelative(root, path.resolve(root, path.posix.dirname(file), include.replace(/\\/g, '/')));
      const target = targetFile ? projects.get(targetFile.toLowerCase()) : undefined;
      if (!target) {
        violations.push(`${file}: project reference "${include}" does not resolve to a project under ${architecture.projectRoot}/.`);
        continue;
      }
      if (target.type.kind !== 'production') {
        violations.push(`${file}: references ${target.name}, which is not a production layer project (${owner}).`);
        continue;
      }
      if (!allowedRoles.has(target.type.role)) {
        const subject = type.kind === 'production' ? type.role : `test project ${name}`;
        violations.push(`${file}: ${subject} → ${target.type.role} is not an allowed reference (see ${owner} → Dependency direction / Backend test projects).`);
      }
    }
  }

  notes.push(`Checked ${projects.size} backend project(s).`);
  return { violations, notes };
}

function main() {
  try {
    const root = rootFromArgs(process.argv.slice(2));
    const { violations, notes } = checkArchitecture(root);
    for (const note of notes) {
      console.log(note);
    }
    if (violations.length > 0) {
      console.log(formatFindings('Architecture violations:', violations));
      process.exit(1);
    }
    console.log('Architecture check: PASS');
  } catch (error) {
    console.error(`Architecture check could not run: ${error instanceof EnforcementError ? error.message : error.stack}`);
    process.exit(3);
  }
}

if (isMainModule(import.meta.url)) {
  main();
}
