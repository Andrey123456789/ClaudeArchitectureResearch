#!/usr/bin/env node
// PostToolUse (Edit|Write|MultiEdit, Bash|PowerShell) and PostToolUseFailure (Bash|PowerShell):
// deterministic checks of the actual resulting state of the active project (resolved from the hook
// input cwd or the edited file through Git, so linked worktrees and nested directories are checked
// in their own checkout).
// - edited file: package/project manifest checks, product-source synchronization reminder;
// - shell call (successful or failed): compares a per-worktree manifest snapshot (HEAD + content hash
//   of every tracked or untracked, non-ignored .csproj / Directory.*.props / package.json) with the
//   previous one and validates what actually changed — whatever the command text was. The first
//   observation of a worktree validates every manifest once; unchanged state stays quiet.
// Findings go to stderr with exit code 2 (shown to Claude); the hook never blocks a completed call.
import { existsSync, readFileSync } from 'node:fs';
import path from 'node:path';
import {
  EncodingError, SetupError, isManifestPath, loadJsonFacet, matchesAny, packageMatches, parseCsproj, parseSelection, readHookInput,
  readJson, readState, readText, requireConfigRoot, resolveContext, samePath, sha256, snapshotManifests, stateFile, toPosix, toRepoRelative,
  writeState,
} from '../scripts/lib/project.mjs';
import { checkArchitecture } from '../scripts/check-architecture.mjs';

const SHELL_TOOLS = new Set(['Bash', 'PowerShell']);
const PACKAGE_RULE = '.claude/rules/3-project/package-management.md';

function isPrerelease(version) {
  return /^\d+(\.\d+){0,3}-[0-9A-Za-z]/.test(String(version || '').trim().replace(/^[\^~=<>v\s[(]+/, ''));
}

function packageRules(configRoot) {
  const selection = parseSelection(configRoot);
  const policy = readJson(path.join(configRoot, '.claude', 'hooks', 'manifest-policy.json'));
  const frame = loadJsonFacet(configRoot, selection, 'architecture', 'enforcement');
  const testing = loadJsonFacet(configRoot, selection, 'backend-testing', 'enforcement');
  const frontend = loadJsonFacet(configRoot, selection, 'frontend', 'enforcement');
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

function checkProjectFile(rel, text, rules, findings) {
  const info = parseCsproj(text);
  for (const pkg of info.packages) {
    if (pkg.version) {
      findings.push(`${rel}: PackageReference '${pkg.id}' declares a version; versions belong only in Directory.Packages.props (owner: ${PACKAGE_RULE}).`);
    } else if (pkg.versionOverride) {
      findings.push(`${rel}: PackageReference '${pkg.id}' uses VersionOverride; keep it only for a concrete reason and report that reason (owner: ${PACKAGE_RULE}).`);
    }
  }
  checkNugetIds(info.packages.map((p) => p.id), rules, rel, findings);
}

function checkPackagesProps(rel, text, rules, findings) {
  if (!/<ManagePackageVersionsCentrally>\s*true\s*<\/ManagePackageVersionsCentrally>/i.test(text)) {
    findings.push(`${rel}: ManagePackageVersionsCentrally must stay true (owner: ${PACKAGE_RULE}).`);
  }
  const ids = [];
  for (const m of text.matchAll(/<(?:PackageVersion|GlobalPackageReference)\b([^>]*)\/?>/gi)) {
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

// Validates one manifest of the active root; returns true when it is a project-graph input.
function checkManifest(activeRoot, rel, rules, findings) {
  const name = path.posix.basename(rel);
  let text;
  try { text = readText(path.join(activeRoot, rel)); } catch (error) {
    if (!(error instanceof EncodingError)) throw error;
    findings.push(`${rel}: cannot read manifest — ${error.message}.`);
    return /\.(csproj|props)$/i.test(name);
  }
  if (/\.csproj$/i.test(name) || name === 'Directory.Build.props') { checkProjectFile(rel, text, rules, findings); return true; }
  if (name === 'Directory.Packages.props') { checkPackagesProps(rel, text, rules, findings); return true; }
  if (name === 'package.json') checkPackageJson(rel, text, rules, findings);
  return false;
}

function architectureFindings(ctx, configRoot, findings) {
  const { violations } = checkArchitecture({ activeRoot: ctx.activeRoot, configRoot });
  for (const v of violations) findings.push(`architecture: ${v}`);
}

function report(header, findings) {
  if (findings.length === 0) process.exit(0);
  process.stderr.write(`${header}\n- ${findings.join('\n- ')}\n`);
  process.exit(2);
}

// ---- edited file ---------------------------------------------------------------------------------

function onFileEdit(input) {
  const filePath = input.tool_input && (input.tool_input.file_path || input.tool_input.notebook_path);
  if (!filePath) process.exit(0);
  const abs = path.resolve(typeof input.cwd === 'string' ? input.cwd : process.cwd(), filePath);
  const ctx = resolveContext(existsSync(path.dirname(abs)) ? path.dirname(abs) : input.cwd);
  if (!ctx.activeRoot) process.exit(0);
  const rel = toRepoRelative(ctx.activeRoot, abs);
  if (!rel) process.exit(0);
  const findings = [];

  if (rel === 'SPECIFICATION.md' || rel === 'CUSTOM_SETTINGS.md') {
    findings.push(`${rel} changed: keep SPECIFICATION.md and CUSTOM_SETTINGS.md consistent (CLAUDE.md § Product inputs) and run the custom-settings workflow to synchronize affected code, validation, configuration, tests, documentation, and frontend.`);
  } else if (isManifestPath(rel) && existsSync(abs)) {
    const configRoot = requireConfigRoot(ctx);
    const graph = checkManifest(ctx.activeRoot, rel, packageRules(configRoot), findings);
    if (graph) architectureFindings(ctx, configRoot, findings);
    // Keep the shell snapshot current so the next shell call does not report this edit again.
    const file = stateFile(ctx, 'manifest-state');
    const previous = readState(file);
    if (previous && previous.version === 1) {
      try {
        previous.files[rel] = sha256(readFileSync(abs));
        writeState(file, previous);
      } catch { /* snapshot refresh is best effort */ }
    }
  }
  report('Post-edit checks:', findings);
}

// ---- shell call ----------------------------------------------------------------------------------

function onShell(input, failed) {
  const ctx = resolveContext(typeof input.cwd === 'string' ? input.cwd : process.cwd());
  if (!ctx.activeRoot) process.exit(0);
  const configRoot = requireConfigRoot(ctx);
  const file = stateFile(ctx, 'manifest-state');
  const previous = readState(file);
  const current = snapshotManifests(ctx);
  const fresh = !previous || previous.version !== 1 || !previous.root || !samePath(previous.root, current.root);

  const changed = [];
  const removed = [];
  if (fresh) {
    changed.push(...Object.keys(current.files));
  } else {
    for (const [rel, hash] of Object.entries(current.files)) if (previous.files[rel] !== hash) changed.push(rel);
    // A path that left the listing but still exists (newly ignored or skipped) is not a removal.
    for (const rel of Object.keys(previous.files)) if (!(rel in current.files) && !existsSync(path.join(ctx.activeRoot, rel))) removed.push(rel);
  }
  if (changed.length === 0 && removed.length === 0) {
    if (fresh || previous.head !== current.head) writeState(file, current);
    process.exit(0);
  }

  const rules = packageRules(configRoot);
  const findings = [];
  const moved = new Set();
  for (const rel of removed) {
    const target = changed.find((c) => current.files[c] === previous.files[rel] && !(c in previous.files));
    if (target) {
      moved.add(target);
      findings.push(`manifest moved: ${rel} → ${target}; confirm the move was intended (project structure: project-structure workflow; project-graph changes: CLAUDE.md § Decision control).`);
    } else {
      findings.push(`manifest removed: ${rel}; confirm the removal was intended (dependencies: add-dependency; projects and references: CLAUDE.md § Decision control).`);
    }
  }
  let graph = removed.some((rel) => /\.(csproj|props)$/i.test(rel));
  for (const rel of changed) graph = checkManifest(ctx.activeRoot, rel, rules, findings) || graph;
  if (graph) architectureFindings(ctx, configRoot, findings);
  // Advance the snapshot only after validation ran, so a setup failure re-validates next time.
  writeState(file, current);

  const where = toPosix(ctx.activeRoot);
  const headNote = !fresh && previous.head !== current.head ? ` HEAD moved ${previous.head.slice(0, 12)} → ${current.head.slice(0, 12)}.` : '';
  const header = fresh
    ? `Initial manifest validation of ${where} (first shell call observed for this worktree):`
    : failed
      ? `Manifest state check after a FAILED shell call in ${where} — the call still changed manifests.${headNote}`
      : `Manifest state check after a shell call in ${where}.${headNote}`;
  report(header, findings);
}

async function main() {
  const input = await readHookInput();
  if (!input.ok) {
    process.stderr.write(`Post-change checks skipped: ${input.error}.\n`);
    process.exit(1);
  }
  const tool = input.value.tool_name;
  if (SHELL_TOOLS.has(tool)) onShell(input.value, input.value.hook_event_name === 'PostToolUseFailure');
  else onFileEdit(input.value);
}

main().catch((error) => {
  const prefix = error instanceof SetupError ? 'Hook setup problem' : 'Hook failure';
  process.stderr.write(`${prefix} (post-change-checks): ${error.message}\n`);
  process.exit(2);
});
