#!/usr/bin/env node
// PostToolUse (Edit|Write|MultiEdit): deterministic checks after a file changes.
// - project/package manifests: Central Package Management, floating/prerelease versions,
//   denied and approval-required packages, project-reference direction (architecture check);
// - SPECIFICATION.md / CUSTOM_SETTINGS.md: synchronization reminder.
// Findings are written to stderr with exit code 2 so Claude sees them; nothing is printed otherwise.
import { existsSync } from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import {
  SetupError, loadJsonFacet, matchesAny, packageMatches, parseCsproj, parseSelection, readStdinJson, readText,
  resolveRoot, toRepoRelative,
} from '../scripts/lib/project.mjs';
import { checkArchitecture } from '../scripts/check-architecture.mjs';

const here = path.dirname(fileURLToPath(import.meta.url));

function isPrerelease(version) {
  return /^\d+(\.\d+){0,3}-[0-9A-Za-z]/.test(String(version || '').trim().replace(/^[\^~=<>v\s[(]+/, ''));
}

function packageRules(root, selection) {
  const policy = JSON.parse(readText(path.join(here, 'manifest-policy.json')));
  const frame = loadJsonFacet(root, selection, 'architecture', 'check');
  const testing = loadJsonFacet(root, selection, 'backend-testing', 'enforcement');
  const frontend = loadJsonFacet(root, selection, 'frontend', 'enforcement');
  return {
    policy,
    nugetDenied: policy.nuget.denied,
    nugetApproval: [
      ...policy.nuget.approvalRequired,
      ...((frame && frame.approvalRequiredPackages) || []),
      ...((testing && testing.approvalRequiredPackages) || []),
    ],
    frontend,
  };
}

function checkNugetIds(ids, rules, rel, findings) {
  for (const id of ids) {
    for (const r of packageMatches(id, rules.nugetDenied)) findings.push(`${rel}: '${id}' must not be added — ${r.reason} (owner: ${r.owner}).`);
    for (const r of packageMatches(id, rules.nugetApproval)) findings.push(`${rel}: '${id}' requires approval — ${r.reason} (owner: ${r.owner}). Remove it unless the user approved it.`);
  }
}

function checkCsproj(root, rel, text, rules, findings) {
  const info = parseCsproj(text);
  for (const pkg of info.packages) {
    if (pkg.version) {
      findings.push(`${rel}: PackageReference '${pkg.id}' declares a version; versions belong only in Directory.Packages.props (owner: .claude/rules/3-project/package-management.md).`);
    } else if (pkg.versionOverride) {
      findings.push(`${rel}: PackageReference '${pkg.id}' uses VersionOverride; keep it only for a concrete reason and report that reason (owner: .claude/rules/3-project/package-management.md).`);
    }
  }
  checkNugetIds(info.packages.map((p) => p.id), rules, rel, findings);
  if (info.projects.length > 0 || info.frameworks.length > 0 || info.packages.length > 0) {
    const { violations } = checkArchitecture(root);
    for (const v of violations) findings.push(`architecture: ${v}`);
  }
}

function checkPackagesProps(rel, text, rules, findings) {
  if (!/<ManagePackageVersionsCentrally>\s*true\s*<\/ManagePackageVersionsCentrally>/i.test(text)) {
    findings.push(`${rel}: ManagePackageVersionsCentrally must stay true (owner: .claude/rules/3-project/package-management.md).`);
  }
  const ids = [];
  for (const m of text.matchAll(/<PackageVersion\b([^>]*)\/?>/gi)) {
    const id = (m[1].match(/Include\s*=\s*"([^"]*)"/i) || [])[1];
    const version = (m[1].match(/Version\s*=\s*"([^"]*)"/i) || [])[1] || '';
    if (!id) continue;
    ids.push(id);
    if (version.includes('*') || version.trim() === '') findings.push(`${rel}: '${id}' uses a floating or empty version '${version}'; pin the latest stable compatible version (owner: add-dependency).`);
    else if (isPrerelease(version)) findings.push(`${rel}: '${id}' ${version} is a prerelease; allowed only when explicitly requested (owner: add-dependency).`);
  }
  checkNugetIds(ids, rules, rel, findings);
}

function checkPackageJson(rel, text, rules, findings) {
  let manifest;
  try { manifest = JSON.parse(text); } catch { findings.push(`${rel}: package.json is not valid JSON.`); return; }
  const frontendRules = rules.frontend && matchesAny(rel, rules.frontend.manifestGlobs) ? rules.frontend.approvalRequiredPackages : [];
  for (const section of ['dependencies', 'devDependencies', 'peerDependencies', 'optionalDependencies']) {
    for (const [name, version] of Object.entries(manifest[section] || {})) {
      const v = String(version).trim();
      if (rules.policy.npm.floatingVersions.includes(v)) findings.push(`${rel}: ${section}.${name} uses floating version '${v}' (owner: add-dependency).`);
      else if (isPrerelease(v)) findings.push(`${rel}: ${section}.${name} ${v} is a prerelease; allowed only when explicitly requested (owner: add-dependency).`);
      for (const r of packageMatches(name, frontendRules)) findings.push(`${rel}: '${name}' requires a concrete need and approval — ${r.reason} (owner: ${r.owner}).`);
    }
  }
}

async function main() {
  const input = await readStdinJson();
  const filePath = input.tool_input && (input.tool_input.file_path || input.tool_input.notebook_path);
  if (!filePath) process.exit(0);

  const root = resolveRoot();
  const rel = toRepoRelative(root, filePath);
  if (!rel) process.exit(0);
  const name = path.posix.basename(rel);
  const findings = [];

  if (rel === 'SPECIFICATION.md' || rel === 'CUSTOM_SETTINGS.md') {
    findings.push(`${rel} changed: keep SPECIFICATION.md and CUSTOM_SETTINGS.md consistent (CLAUDE.md § Product inputs) and run the custom-settings workflow to synchronize affected code, validation, configuration, tests, documentation, and frontend.`);
  } else if (/\.(csproj|props|json)$/i.test(name)) {
    const abs = path.resolve(root, rel);
    if (!existsSync(abs)) process.exit(0);
    const selection = parseSelection(root);
    const rules = packageRules(root, selection);
    const text = readText(abs);
    if (name.toLowerCase().endsWith('.csproj')) checkCsproj(root, rel, text, rules, findings);
    else if (name === 'Directory.Packages.props') checkPackagesProps(rel, text, rules, findings);
    else if (name === 'package.json' && !rel.includes('node_modules/')) checkPackageJson(rel, text, rules, findings);
  }

  if (findings.length > 0) {
    process.stderr.write(`Post-edit checks:\n- ${findings.join('\n- ')}\n`);
    process.exit(2);
  }
  process.exit(0);
}

main().catch((error) => {
  const prefix = error instanceof SetupError ? 'Hook setup problem' : 'Hook failure';
  process.stderr.write(`${prefix} (post-edit-checks): ${error.message}\n`);
  process.exit(2);
});
